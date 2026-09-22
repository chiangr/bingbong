"""Builders for new KiCad 9 schematic objects (root sheet only)."""
import uuid as U

ROOT = '/e7d26e72-3287-4d9d-b245-45d7d8c953b0'


def uid():
    return str(U.uuid4())


def label(text, x, y, rot=0, just='left bottom'):
    return ['\t(label "%s"' % text, f'\t\t(at {x} {y} {rot})', '\t\t(effects',
            '\t\t\t(font', '\t\t\t\t(size 1.27 1.27)', '\t\t\t)',
            f'\t\t\t(justify {just})', '\t\t)', f'\t\t(uuid "{uid()}")', '\t)']


def wire(x1, y1, x2, y2):
    return ['\t(wire', '\t\t(pts', f'\t\t\t(xy {x1} {y1}) (xy {x2} {y2})', '\t\t)',
            '\t\t(stroke', '\t\t\t(width 0)', '\t\t\t(type default)', '\t\t)',
            f'\t\t(uuid "{uid()}")', '\t)']


def _sym(lib, ref, x, y, fields, npins, rot=0, dnp=False):
    out = ['\t(symbol', f'\t\t(lib_id "{lib}")', f'\t\t(at {x} {y} {rot})', '\t\t(unit 1)',
           '\t\t(exclude_from_sim no)', '\t\t(in_bom yes)', '\t\t(on_board yes)',
           '\t\t(dnp %s)' % ('yes' if dnp else 'no'),
           '\t\t(fields_autoplaced yes)', f'\t\t(uuid "{uid()}")']
    for i, (k, v, hide) in enumerate(fields):
        out += [f'\t\t(property "{k}" "{v}"',
                f'\t\t\t(at {x + 2.54} {y - 1.27 + i * 0.01} 90)',
                '\t\t\t(effects', '\t\t\t\t(font', '\t\t\t\t\t(size 1.27 1.27)', '\t\t\t\t)']
        if hide:
            out += ['\t\t\t\t(hide yes)']
        out += ['\t\t\t)', '\t\t)']
    for n in range(1, npins + 1):
        out += [f'\t\t(pin "{n}"', f'\t\t\t(uuid "{uid()}")', '\t\t)']
    out += ['\t\t(instances', '\t\t\t(project "bingbong"', f'\t\t\t\t(path "{ROOT}"',
            f'\t\t\t\t\t(reference "{ref}")', '\t\t\t\t\t(unit 1)', '\t\t\t\t)',
            '\t\t\t)', '\t\t)', '\t)']
    return out


def resistor(ref, val, x, y, rot=0):
    return _sym('Device:R', ref, x, y, [
        ('Reference', ref, False), ('Value', val, False),
        ('Footprint', 'Resistor_SMD:R_0402_1005Metric', True),
        ('Datasheet', '~', True), ('Description', 'Resistor', True)], 2, rot)


def capacitor(ref, val, x, y, rot=0, dnp=False, desc='Unpolarized capacitor'):
    return _sym('Device:C', ref, x, y, [
        ('Reference', ref, False), ('Value', val, False),
        ('Footprint', 'Capacitor_SMD:C_0402_1005Metric', True),
        ('Datasheet', '~', True), ('Description', desc, True)], 2, rot, dnp)


def power(lib, ref, x, y, val, rot=0):
    desc = f'Power symbol creates a global label with name \\"{val}\\"'
    return _sym(lib, ref, x, y, [
        ('Reference', ref, True), ('Value', val, False),
        ('Footprint', '', True), ('Datasheet', '', True),
        ('Description', desc, True)], 1, rot)
