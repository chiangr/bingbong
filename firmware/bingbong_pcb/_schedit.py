"""Minimal, careful editor for KiCad 9 .kicad_sch symbol properties.

Only touches (property "<name>" "<value>") inside the symbol block whose
instance reference matches. Never moves geometry, never touches wires.
"""
import io, re


def load(path='bingbong.kicad_sch'):
    return io.open(path, encoding='utf-8').read().split('\n')


def save(lines, path='bingbong.kicad_sch'):
    io.open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))


def symbol_blocks(lines):
    """Yield (ref, start, end) for each top-level (symbol ...) block."""
    for i, l in enumerate(lines):
        if l != '\t(symbol':
            continue
        depth, j = 0, i
        while j < len(lines):
            depth += lines[j].count('(') - lines[j].count(')')
            if depth == 0 and j > i:
                break
            j += 1
        block = lines[i:j + 1]
        m = re.search(r'\(property "Reference" "([^"]+)"', '\n'.join(block))
        ref = m.group(1) if m else None
        # prefer the instances reference (authoritative)
        m2 = re.search(r'\(reference "([^"]+)"', '\n'.join(block))
        if m2:
            ref = m2.group(1)
        yield ref, i, j


def find(lines, ref):
    for r, a, b in symbol_blocks(lines):
        if r == ref:
            return a, b
    raise KeyError(f'symbol {ref} not found')


def get_prop(lines, ref, prop):
    a, b = find(lines, ref)
    for i in range(a, b + 1):
        m = re.match(r'\t\t\(property "%s" "(.*)"$' % re.escape(prop), lines[i])
        if m:
            return m.group(1), i
    return None, None


def set_prop(lines, ref, prop, value):
    """Replace an existing property's value. Returns old value."""
    old, i = get_prop(lines, ref, prop)
    if i is None:
        raise KeyError(f'{ref} has no property {prop}')
    lines[i] = '\t\t(property "%s" "%s"' % (prop, value)
    return old
