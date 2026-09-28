"""Minimal KiCad 10 schematic writer for the bingbong v3 sheets.

Sheets are described in Python (one script per sheet) so pin-to-net wiring is
exact and repeatable. Every generated sheet is checked with kicad-cli
(ERC + netlist) by tools/check.py.
"""
import math
import os
import re
import uuid

KICAD_SYM_DIR = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols"
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE)
PROJECT = "bingbong_v3"
SCH_VERSION = "20260306"
GRID = 1.27


def uid():
    return str(uuid.uuid4())


def q(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def snap(v):
    return round(round(v / GRID) * GRID, 4)


# ---------------------------------------------------------------- s-expr utils
def tokenize(text):
    return re.findall(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+', text)


def parse(tokens, i=0):
    out = []
    while i < len(tokens):
        t = tokens[i]
        if t == "(":
            sub, i = parse(tokens, i + 1)
            out.append(sub)
        elif t == ")":
            return out, i + 1
        else:
            out.append(t[1:-1] if t.startswith('"') else t)
            i += 1
    return out, i


def find_block(text, name):
    """Return the raw text of top-level `(symbol "name" ...)` in a library file."""
    m = re.search(r'\n\t\(symbol ' + re.escape(q(name)) + r'\n', text)
    if not m:
        raise KeyError(name)
    start = m.start() + 1
    depth = 0
    for j in range(start, len(text)):
        c = text[j]
        if c == '"':
            # skip strings
            k = j + 1
            while text[k] != '"':
                k += 2 if text[k] == "\\" else 1
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return text[start:j + 1]
    raise ValueError(name)


def pins_of(block_text):
    """pin number -> (x, y, angle, name, type) in library (Y-up) coordinates."""
    tree, _ = parse(tokenize(block_text))
    pins = {}

    def walk(node, unit=1):
        if isinstance(node, list) and node:
            if node[0] == "symbol" and len(node) > 1 and isinstance(node[1], str):
                m = re.search(r"_(\d+)_\d+$", node[1])
                if m:
                    unit = int(m.group(1)) or 1
            if node[0] == "pin":
                ptype = node[1]
                at = next(n for n in node if isinstance(n, list) and n[0] == "at")
                num = next(n for n in node if isinstance(n, list) and n[0] == "number")[1]
                nm = next(n for n in node if isinstance(n, list) and n[0] == "name")[1]
                pins[num] = (float(at[1]), float(at[2]), float(at[3]), nm, ptype, unit)
            for n in node:
                walk(n, unit)

    walk(tree)
    return pins


_lib_cache = {}


def stock(lib, name):
    path = os.path.join(KICAD_SYM_DIR, lib + ".kicad_sym")
    if path not in _lib_cache:
        _lib_cache[path] = open(path).read()
    block = find_block(_lib_cache[path], name)
    if "(extends" in block:
        raise ValueError(f"{lib}:{name} uses extends; flatten first")
    return block


# ------------------------------------------------------------ custom IC symbols
def _unit_body(left, right, top, bottom, pin_len, width):
    p = 2.54
    rows = max(len(left), len(right), 1)
    cols = max(len(top), len(bottom), 1)
    longest = max([len(x[1]) for x in list(left) + list(right) if x] + [4])
    w = width or max(snap(longest * 1.27 * 2 + 5.08), cols * p + 5.08)
    w = math.ceil(w / (2 * p)) * 2 * p
    h = math.ceil(max(rows + 1, 3) * p / (2 * p)) * 2 * p
    x0, y0 = -w / 2, h / 2
    pins = []

    def side(items, x_of, y_of, ang):
        for i, it in enumerate(items):
            if it:
                pins.append((it[0], it[1], it[2], x_of(i), y_of(i), ang))

    ly = lambda i: y0 - p * (i + 1)
    side(left, lambda i: x0 - pin_len, ly, 0)
    side(right, lambda i: -x0 + pin_len, ly, 180)
    tx = lambda i: x0 + p * (i + 1) + (w - p * (cols + 1)) / 2
    side(top, tx, lambda i: y0 + pin_len, 270)
    side(bottom, tx, lambda i: -y0 - pin_len, 90)
    return x0, y0, pins


def ic_symbol(name, left=(), right=(), top=(), bottom=(), ref="U", value=None,
              footprint="", datasheet="", description="", pin_len=2.54, width=None, units=None):
    """Rectangular IC symbol. Each side is a list of (number, name, etype) or None (gap).
    units: optional list of dicts(left=, right=, top=, bottom=, width=) for a multi-unit part."""
    units = units or [dict(left=left, right=right, top=top, bottom=bottom, width=width)]
    subs = []
    for ui, u in enumerate(units, 1):
        x0, y0, pins = _unit_body(u.get("left", ()), u.get("right", ()), u.get("top", ()),
                                  u.get("bottom", ()), pin_len, u.get("width"))
        if ui == 1:
            fx0, fy0 = x0, y0
        subs.append((ui, x0, y0, pins))
    x0, y0 = fx0, fy0
    body = ""
    for ui, ux0, uy0, pins in subs:
        body += _unit_text(name, ui, ux0, uy0, pins, pin_len)
    value = value or name
    return "\t" + f'''(symbol {q(name)}
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(property "Reference" {q(ref)} (at {x0:g} {y0 + 1.27:g} 0) (effects (font (size 1.27 1.27)) (justify left bottom)))
\t\t(property "Value" {q(value)} (at {x0:g} {-y0 - 1.27:g} 0) (effects (font (size 1.27 1.27)) (justify left top)))
\t\t(property "Footprint" {q(footprint)} (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t(property "Datasheet" {q(datasheet)} (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t(property "Description" {q(description)} (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
{body}\t\t(embedded_fonts no)
\t)'''


def _unit_text(name, ui, x0, y0, pins, pin_len):
    pl = []
    for num, nm, et, x, y, a in pins:
        pl.append(f'''\t\t\t(pin {et} line
\t\t\t\t(at {x:g} {y:g} {a:g})
\t\t\t\t(length {pin_len:g})
\t\t\t\t(name {q(nm)} (effects (font (size 1.016 1.016))))
\t\t\t\t(number {q(num)} (effects (font (size 1.016 1.016))))
\t\t\t)''')
    return f'''\t\t(symbol {q(f"{name}_{ui}_1")}
\t\t\t(rectangle (start {x0:g} {y0:g}) (end {-x0:g} {-y0:g}) (stroke (width 0.254) (type default)) (fill (type background)))
{chr(10).join(pl)}
\t\t)
'''


# ------------------------------------------------------------------ the sheet
DIRS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}


class Sym:
    def __init__(self, sheet, lib_id, block, x, y, rot, mirror=False, unit=1):
        self.sheet, self.lib_id, self.x, self.y, self.rot, self.mirror = sheet, lib_id, x, y, rot, mirror
        allp = pins_of(block)
        multi = len({v[5] for v in allp.values()}) > 1
        self.lib_pins = {k: v for k, v in allp.items() if not multi or v[5] == unit}
        name = lib_id.split(":")[1]
        mu = re.search(r'\(symbol ' + re.escape(q(f"{name}_{unit}_1")), block)
        rs = re.findall(r"\(rectangle \(start ([-\d.]+) ([-\d.]+)\)", block[mu.start():] if mu else block)
        self.half_w = abs(float(rs[0][0])) if rs else 2.54
        self.half_h = abs(float(rs[0][1])) if rs else 3.81

    def pin(self, num):
        px, py, pa = self.lib_pins[str(num)][:3]
        r = math.radians(self.rot)
        xr = px * math.cos(r) - py * math.sin(r)
        yr = px * math.sin(r) + py * math.cos(r)
        if self.mirror:          # KiCad: rotate first, then mirror about the Y axis
            xr = -xr
        return (snap(self.x + xr), snap(self.y - yr))

    def outward(self, num):
        """Direction pointing away from the symbol body at this pin."""
        pa = (self.lib_pins[str(num)][2] + 180 + self.rot) % 360
        if self.mirror:
            pa = (180 - pa) % 360
        return {0: "right", 90: "up", 180: "left", 270: "down"}[round(pa) % 360]


class Sheet:
    def __init__(self, filename, title, sheet_uuid_path, rev="v3-A1", paper="A3", project=PROJECT, subdir="bingbong"):
        self.filename, self.title, self.path, self.rev, self.paper = filename, title, sheet_uuid_path, rev, paper
        self.project, self.subdir = project, subdir
        self.lib_symbols = {}
        self.items = []

    # --- library
    def _use(self, lib_id, block):
        if lib_id not in self.lib_symbols:
            libname, name = lib_id.split(":")
            emb = block.replace(f'(symbol {q(name)}', f'(symbol {q(lib_id)}', 1)
            self.lib_symbols[lib_id] = emb
        return block

    # --- placement
    def place(self, lib_id, block, ref, value, x, y, rot=0, footprint="", datasheet="",
              fields=None, dnp=False, ref_off=None, val_off=None, hide_value=False, in_bom=True, mirror=False, unit=1):
        self._use(lib_id, block)
        if not footprint:        # inherit the library symbol's footprint (custom ICs carry theirs)
            m = re.search(r'\(property "Footprint" "([^"]*)"', block)
            footprint = m.group(1) if m else ""
        x, y = snap(x), snap(y)
        s = Sym(self, lib_id, block, x, y, rot, mirror, unit)
        pins = "".join(f'\t\t(pin {q(n)} (uuid "{uid()}"))\n' for n in s.lib_pins)
        is_power = lib_id.startswith("power:")
        if lib_id == "power:GND":
            hide_value = True
        rx, ry = ref_off or ((3.0, -1.3) if not is_power else (0, 3))
        vx, vy = val_off or ((3.0, 1.3) if not is_power else (0, -3.2))
        if is_power and rot in (90, 270):
            rx, ry, vx, vy = (0, 0, 0, 0)
        props = [("Reference", ref, rx, ry, is_power), ("Value", value, vx, vy, hide_value),
                 ("Footprint", footprint, 0, 0, True), ("Datasheet", datasheet, 0, 0, True),
                 ("Description", "", 0, 0, True)]
        for k, v in (fields or {}).items():
            props.append((k, v, 0, 0, True))
        ptxt = ""
        fang = rot if rot in (90, 270) and not is_power else 0
        for k, v, ox, oy, hide in props:
            just = "(justify left)" if (k in ("Reference", "Value") and not is_power) else ""
            h = " (hide yes)" if hide else ""
            ptxt += (f'\t\t(property {q(k)} {q(v)} (at {snap(x + ox):g} {snap(y + oy):g} {fang})'
                     f' (effects (font (size 1.27 1.27)) {just}{h}))\n')
        self.items.append(f'''\t(symbol
\t\t(lib_id {q(lib_id)})
\t\t(at {x:g} {y:g} {rot})
{"\t\t(mirror y)\n" if mirror else ""}\t\t(unit {unit})
\t\t(exclude_from_sim no)
\t\t(in_bom {"yes" if in_bom and not is_power else "no"})
\t\t(on_board {"no" if is_power else "yes"})
\t\t(dnp {"yes" if dnp else "no"})
\t\t(uuid "{uid()}")
{ptxt}{pins}\t\t(instances (project {q(self.project)} (path {q(self.path)} (reference {q(ref)}) (unit {unit}))))
\t)
''')
        return s

    # --- drawing primitives
    def wire(self, *pts):
        pts = [(snap(a), snap(b)) for a, b in pts]
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            if (x1, y1) == (x2, y2):
                continue
            self.items.append(f'\t(wire (pts (xy {x1:g} {y1:g}) (xy {x2:g} {y2:g})) (stroke (width 0) (type default)) (uuid "{uid()}"))\n')

    def link(self, a, b, first="h"):
        """Orthogonal wire a->b (first leg horizontal by default)."""
        if a[0] == b[0] or a[1] == b[1]:
            self.wire(a, b)
        elif first == "h":
            self.wire(a, (b[0], a[1]), b)
        else:
            self.wire(a, (a[0], b[1]), b)

    def junction(self, p):
        self.items.append(f'\t(junction (at {snap(p[0]):g} {snap(p[1]):g}) (diameter 0) (color 0 0 0 0) (uuid "{uid()}"))\n')

    def stub(self, p, d, n=2):
        dx, dy = DIRS[d]
        e = (snap(p[0] + dx * GRID * n), snap(p[1] + dy * GRID * n))
        self.wire(p, e)
        return e

    def label(self, p, net, d):
        ang = {"right": 0, "up": 90, "left": 180, "down": 270}[d]
        just = "left bottom" if d in ("right", "up") else "right bottom"
        self.items.append(f'\t(label {q(net)} (at {snap(p[0]):g} {snap(p[1]):g} {ang}) (effects (font (size 1.27 1.27)) (justify {just})) (uuid "{uid()}"))\n')

    def glabel(self, p, net, d, shape="bidirectional"):
        ang = {"right": 0, "up": 90, "left": 180, "down": 270}[d]
        just = "left" if d in ("right", "up") else "right"
        self.items.append(f'''\t(global_label {q(net)} (shape {shape}) (at {snap(p[0]):g} {snap(p[1]):g} {ang}) (fields_autoplaced yes)
\t\t(effects (font (size 1.27 1.27)) (justify {just})) (uuid "{uid()}")
\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at {snap(p[0]):g} {snap(p[1]):g} 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t)
''')

    def noconn(self, p):
        self.items.append(f'\t(no_connect (at {snap(p[0]):g} {snap(p[1]):g}) (uuid "{uid()}"))\n')

    def text(self, p, s, size=1.27, bold=False):
        b = " (bold yes)" if bold else ""
        self.items.append(f'\t(text {q(s)} (exclude_from_sim no) (at {p[0]:g} {p[1]:g} 0) (effects (font (size {size} {size}){b}) (justify left top)) (uuid "{uid()}"))\n')

    def box(self, a, b, title=None):
        self.items.append(f'\t(rectangle (start {a[0]:g} {a[1]:g}) (end {b[0]:g} {b[1]:g}) (stroke (width 0.254) (type dash) (color 72 72 72 1)) (fill (type none)) (uuid "{uid()}"))\n')
        if title:
            self.text((a[0] + 1.5, a[1] + 1.5), title, size=2.0, bold=True)

    # --- net helpers
    _pwr_rot = {"up": 0, "left": 90, "down": 180, "right": 270}
    _gnd_rot = {"down": 0, "right": 90, "up": 180, "left": 270}

    def rail(self, p, net, d="up", n=2):
        """Stub from p toward d, then a power symbol named `net` (global rail)."""
        e = self.stub(p, d, n) if n else p
        self._pwr_count = getattr(self, "_pwr_count", 0) + 1
        self.place("power:VCC", stock("power", "VCC"), f"#PWR{self._pwr_count:04d}", net, e[0], e[1],
                   rot=self._pwr_rot[d])
        return e

    def gnd(self, p, d="down", n=2):
        e = self.stub(p, d, n) if n else p
        self._pwr_count = getattr(self, "_pwr_count", 0) + 1
        self.place("power:GND", stock("power", "GND"), f"#PWR{self._pwr_count:04d}", "GND", e[0], e[1],
                   rot=self._gnd_rot[d])
        return e

    def flag(self, p, d="up", n=2):
        e = self.stub(p, d, n) if n else p
        self._flg = getattr(self, "_flg", 0) + 1
        self.place("power:PWR_FLAG", stock("power", "PWR_FLAG"), f"#FLG{self._flg:04d}", "PWR_FLAG",
                   e[0], e[1], rot=self._pwr_rot[d])
        return e

    def net(self, p, name, d, n=2):
        e = self.stub(p, d, n)
        self.label(e, name, d)
        return e

    def gnet(self, p, name, d, n=2, shape="bidirectional"):
        e = self.stub(p, d, n)
        self.glabel(e, name, d, shape)
        return e

    # --- output
    def write(self):
        libs = "\n".join(self.lib_symbols.values())
        body = "".join(self.items)
        out = f'''(kicad_sch
\t(version {SCH_VERSION})
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "{uid()}")
\t(paper {q(self.paper)})
\t(title_block (title {q(self.title)}) (date "2026-09-23") (rev {q(self.rev)}) (company "bingbong"))
\t(lib_symbols
{libs}
\t)
{body}\t(embedded_fonts no)
)
'''
        open(os.path.join(V3, self.subdir, self.filename), "w").write(out)


def root_paths(project=PROJECT, subdir="bingbong"):
    """Map sheet filename -> instance path '/root-uuid/sheet-uuid' from the root schematic."""
    root = open(os.path.join(V3, subdir, project + ".kicad_sch")).read()
    ruid = re.search(r'\(kicad_sch.*?\(uuid "([^"]+)"\)', root, re.S).group(1)
    paths = {}
    for m in re.finditer(r'\(sheet\n.*?\(uuid "([^"]+)"\).*?\(property "Sheetfile" "([^"]+)"', root, re.S):
        paths[m.group(2)] = f"/{ruid}/{m.group(1)}"
    return paths


def write_custom_lib(blocks):
    """Write lib/Bingbong_v3.kicad_sym from {name: block_text}."""
    body = "\n".join(blocks.values())
    open(os.path.join(V3, "lib", "Bingbong_v3.kicad_sym"), "w").write(
        f'(kicad_symbol_lib\n\t(version 20251024)\n\t(generator "kicad_symbol_editor")\n\t(generator_version "10.0")\n{body}\n)\n')
