"""Resolve absolute schematic coordinates of every symbol pin.

KiCad schematic transform: library pin (px, py) with symbol placed at (X, Y)
with rotation R and optional mirror. Library Y is up, schematic Y is down.
"""
import io, re, math


def _lib_pins(text):
    """{lib_id: {pin_number: (x, y)}} from the (lib_symbols ...) block."""
    out = {}
    # each top-level library symbol inside lib_symbols
    for m in re.finditer(r'\n\t\t\(symbol "([^"]+)"\n', text):
        name = m.group(1)
        start = m.start()
        depth, i = 0, start + 1
        while i < len(text):
            if text[i] == '"':
                i += 1
                while i < len(text) and text[i] != '"':
                    i += 2 if text[i] == '\\' else 1
            elif text[i] == '(':
                depth += 1
            elif text[i] == ')':
                depth -= 1
                if depth == 0:
                    break
            i += 1
        body = text[start:i]
        pins = {}
        for pm in re.finditer(
                r'\(pin \w+ \w+\s*\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\).*?\(number "([^"]+)"',
                body, re.S):
            x, y, _ang, num = float(pm.group(1)), float(pm.group(2)), pm.group(3), pm.group(4)
            pins[num] = (x, y)
        if pins:
            out[name] = pins
    return out


def resolve(path='bingbong.kicad_sch'):
    """-> {ref: {pin: (x, y)}} in absolute schematic mm."""
    text = io.open(path, encoding='utf-8').read()
    libs = _lib_pins(text)
    res = {}

    for m in re.finditer(r'\n\t\(symbol\n', text):
        start = m.start() + 1
        depth, i = 0, start
        while i < len(text):
            if text[i] == '"':
                i += 1
                while i < len(text) and text[i] != '"':
                    i += 2 if text[i] == '\\' else 1
            elif text[i] == '(':
                depth += 1
            elif text[i] == ')':
                depth -= 1
                if depth == 0:
                    break
            i += 1
        blk = text[start:i]

        # a (lib_name ...) override takes precedence over (lib_id ...)
        lm = re.search(r'\(lib_name "([^"]+)"\)', blk) or re.search(r'\(lib_id "([^"]+)"\)', blk)
        am = re.search(r'\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\)', blk)
        rm = re.search(r'\(reference "([^"]+)"', blk)
        if not (lm and am and rm):
            continue
        lib, ref = lm.group(1), rm.group(1)
        X, Y, R = float(am.group(1)), float(am.group(2)), float(am.group(3))
        mirror = re.search(r'\(mirror (x|y)\)', blk)
        mir = mirror.group(1) if mirror else None

        if lib not in libs:
            continue
        pins = {}
        th = math.radians(R)
        c, s = math.cos(th), math.sin(th)
        for num, (px, py) in libs[lib].items():
            x, y = px, py
            if mir == 'y':
                x = -x
            elif mir == 'x':
                y = -y
            # rotate then flip Y for screen coords
            rx = x * c - y * s
            ry = x * s + y * c
            pins[num] = (round(X + rx, 3), round(Y - ry, 3))
        res[ref] = pins
    return res


if __name__ == '__main__':
    import sys
    p = resolve()
    for ref in sys.argv[1:]:
        print(ref, {k: v for k, v in sorted(p.get(ref, {}).items())})
