import _schedit as se

L = se.load()
log = []


def P(ref, prop, val, why):
    old = se.set_prop(L, ref, prop, val)
    log.append((ref, prop, old, val, why))


# --- H-3: charge termination is broken -------------------------------------
# ITERM = 100 mA with RPROG3 = 10 k, which is at/above the achievable charge
# current, so CV termination never fires. Rule: RPROG3 ~= 10 x RPROG1.
P('R15', 'Value', '100k', 'H-3 ITERM 100mA -> 10mA')

# --- LOW-18: U1 had no MPN at all, on the part that drives +12 V into J5 ----
P('U1', 'Value', 'R1200N002A-TR-FE', 'LOW-18 record MPN')
P('U1', 'Datasheet',
  'https://www.nisshinbo-microdevices.co.jp/en/pdf/datasheet/r1200-ea.pdf',
  'LOW-18 record datasheet')

# --- LOW-9: schematic Value disagreed with the ordered part -----------------
# Land (SOD-923) is already correct for the ESD9B5.0ST5G. Fix the metadata,
# NOT the footprint - reverting the footprint would mis-land the ordered part.
for r in ('CR1', 'CR2', 'CR3'):
    P(r, 'Value', 'ESD9B5.0ST5G', 'LOW-9 match ordered part')

# --- H-6: buck inductor was a 500 mA multilayer DECOUPLING part -------------
# TPS62172 high-side current limit reaches 1.35 A. Need Isat >= 1.4 A.
# L_1008_2520Metric (2.5 x 2.0 mm) fits the TDK VLS252012HBX-3R3 class.
P('L1', 'Value', '3.3uH', 'H-6 inductor value for low VIN')
P('L1', 'Footprint', 'Inductor_SMD:L_1008_2520Metric', 'H-6 real power inductor land')

# --- H-6 / M-7: DC-bias derating. 22 uF 6.3V 0402 X5R on 3.3 V keeps a
# fraction of its marked value; TI asks for 22 uF actual.
for r in ('C10', 'C13'):
    P(r, 'Footprint', 'Capacitor_SMD:C_0805_2012Metric', 'H-6 22uF actual, 10V part')

# --- LOW-5: C15 is 10 uF 10V 0402 X5R at 5 V bias on VBUS ------------------
P('C15', 'Footprint', 'Capacitor_SMD:C_0603_1608Metric', 'LOW-5 16-25V part fits')

# --- LOW-8: schematic said FDN340P, BOM ordered FDN338P --------------------
# Both P-channel. FDN338P is logic-level, which suits the -3.2 V Vgs here.
P('Q2', 'Value', 'FDN338P', 'LOW-8 match ordered part, logic-level')

# --- LOW-14: 1 k from 3.3 V through a ~2.0 V green LED = ~1.3 mA (dim) -----
# R12 drives D3 (red) and can stay at 1 k.
for r in ('R11', 'R13'):
    P(r, 'Value', '680R', 'LOW-14 green LED brightness')
P('D1', 'Value', 'LED Red 630nm', 'LOW-14 record colour')
P('D2', 'Value', 'LED Green 573nm', 'LOW-14 record colour')
P('D3', 'Value', 'LED Red 630nm', 'LOW-14 record colour')
P('D4', 'Value', 'LED Green 573nm', 'LOW-14 record colour')

# --- Section 1.6: the ZIF/display had no MPN anywhere in the project -------
P('J5', 'Value', 'ER-CON26HT-1', 'record ZIF MPN')
P('J5', 'Datasheet', 'https://www.buydisplay.com/download/connector/ER-CON26HT-1.pdf',
  'record ZIF datasheet')
P('J5', 'Description',
  'ZIF FFC 26-pin 0.5mm for buydisplay ER-OLED018-1 (SSD1326 256x32 OLED). '
  'Pin order VERIFIED 26/26 against datasheet section 5 / Table 5.1 on 2026-09-04 - '
  'pad N = display pin N, DIRECT map. Do not renumber.',
  'record display + verified pin order')

se.save(L)

w = max(len(x[0]) for x in log)
for ref, prop, old, new, why in log:
    print(f'{ref:<{w}} {prop:<10} {str(old)[:34]:<34} -> {new[:40]:<40} [{why}]')
print(f'\n{len(log)} property edits applied')
