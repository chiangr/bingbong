"""Custom symbols for bingbong v3. Pin numbers are the package ball/pin IDs from the
datasheets saved in firmware/bingbong_pcb/_mech/ (never from memory)."""
from schgen import ic_symbol

TI = "https://www.ti.com/lit/ds/symlink/"

CUSTOM = {
    # BQ25188 SLUSFJ3 Table 5-1, YBG DSBGA-8
    "BQ25188": ic_symbol(
        "BQ25188",
        left=[("A2", "IN", "power_in"), None, ("D1", "TS/MR", "bidirectional"),
              ("B1", "SCL", "input"), ("C1", "SDA", "bidirectional"), ("A1", "~{INT}", "open_collector")],
        right=[("B2", "SYS", "power_out"), None, None, None, ("C2", "BAT", "passive")],
        bottom=[("D2", "GND", "power_in")],
        footprint="Bingbong_v3:TI_YBG0008_DSBGA-8", datasheet=TI + "bq25188.pdf",
        description="1-cell 1 A linear charger, power path, I2C 0x6A"),
    # MAX17048 19-6171 pin description, WLP-8 bumps
    "MAX17048": ic_symbol(
        "MAX17048",
        left=[("A3", "VDD", "power_in"), ("A2", "CELL", "input"), None, ("A1", "CTG", "input"),
              ("B3", "QSTRT", "input")],
        right=[("B1", "SDA", "bidirectional"), ("B2", "SCL", "input"), None, ("B4", "~{ALRT}", "open_collector")],
        bottom=[("A4", "GND", "power_in")],
        footprint="Bingbong_v3:MAX_WLP-8_0.9x1.7", datasheet="https://www.analog.com/media/en/technical-documentation/data-sheets/MAX17048-MAX17049.pdf",
        description="1-cell ModelGauge fuel gauge, I2C 0x36"),
    # TPS62840 SLVSEC6D Pin Functions, DLC SON-8
    "TPS62840DLC": ic_symbol(
        "TPS62840DLC",
        left=[("2", "VIN", "power_in"), ("4", "EN", "input"), None, ("3", "MODE", "input"),
              ("6", "STOP", "input"), ("5", "VSET", "passive")],
        right=[("7", "SW", "power_out"), None, ("8", "VOS", "input")],
        bottom=[("1", "GND", "power_in")],
        footprint="Bingbong_v3:TI_DLC0008_SON-8_1.5x2", datasheet=TI + "tps62840.pdf",
        description="750 mA 60 nA-IQ buck, VOUT set by RSET"),
}

# nRF9151 LGA-113 — pin numbers from Nordic PS v1.0 pin table (docs.nordicsemi.com ps_nrf9151/pin.html),
# cross-checked against the makerdiary nRF9151 Connect Kit schematic (_mech/nrf9151_connectkit_sch.pdf p4).
_GPIO_PINS = {0: 56, 1: 57, 2: 58, 3: 59, 4: 61, 5: 62, 6: 63, 7: 64, 8: 67, 9: 68, 10: 69, 11: 70, 12: 72,
              13: 73, 14: 74, 15: 75, 16: 77, 17: 78, 18: 79, 19: 80, 20: 2, 21: 5, 22: 6, 23: 8, 24: 11,
              25: 12, 26: 44, 27: 45, 28: 47, 29: 48, 30: 49, 31: 50}
_AIN = {13: 0, 14: 1, 15: 2, 16: 3, 17: 4, 18: 5, 19: 6, 20: 7}
_gp = lambda n: (str(_GPIO_PINS[n]), f"P0.{n:02d}" + (f"/AIN{_AIN[n]}" if n in _AIN else ""), "bidirectional")
_GND = [1, 7, 13, 15, 20, 25, 30, 34, 36, 38, 39, 40, 41, 43, 46, 51, 55, 60, 66, 71, 76] + list(range(105, 114))
_RSV = [31, 32, 33] + list(range(81, 105))

CUSTOM["NRF9151"] = ic_symbol(
    "NRF9151",
    units=[
        # unit 1: power + RF
        dict(left=[("10", "ENABLE", "input"), None, None, ("14", "VDD", "power_in"), None, None,
                   ("65", "VDD_GPIO", "power_in"), None, None, ("24", "DEC0", "passive")],
             right=[("35", "ANT", "passive"), None, ("37", "AUX", "passive"), None, ("42", "GPS", "passive")]),
        # unit 2: GPIO
        dict(left=[_gp(n) for n in range(0, 16)], right=[_gp(n) for n in range(16, 32)]),
        # unit 3: debug, SIM, coexistence, MIPI RFFE
        dict(left=[("4", "SWDIO", "bidirectional"), ("3", "SWDCLK", "input"), ("9", "~{RESET}", "bidirectional"),
                   None, ("16", "SIM_RST", "output"), ("18", "SIM_CLK", "output"), ("17", "SIM_IO", "bidirectional"),
                   ("19", "SIM_1V8", "power_out"), ("26", "SIM_DET", "no_connect")],
             right=[("52", "COEX0", "bidirectional"), ("53", "COEX1", "bidirectional"), ("54", "COEX2", "bidirectional"),
                    None, ("21", "MAGPIO0", "bidirectional"), ("22", "MAGPIO1", "bidirectional"),
                    ("23", "MAGPIO2", "bidirectional"), None, ("27", "SDATA", "bidirectional"),
                    ("28", "SCLK", "output"), ("29", "VIO", "passive")]),
        # unit 4: reserved (solder for mechanics/thermal, no electrical connection)
        dict(left=[(str(n), f"RSV_{n}", "no_connect") for n in _RSV[:14]],
             right=[(str(n), f"RSV_{n}", "no_connect") for n in _RSV[14:]]),
        # unit 5: ground
        dict(left=[(str(n), "GND", "power_in") for n in _GND[:15]],
             right=[(str(n), "GND", "power_in") for n in _GND[15:]], width=15.24),
    ],
    footprint="Bingbong_v3:Nordic_nRF9151_LGA-113_12.1x11.1", datasheet="https://docs.nordicsemi.com/bundle/ps_nrf9151",
    description="nRF9151 LTE-M/NB-IoT SiP, Cortex-M33")

# MFF2 eUICC (ETSI TS 102 671), pinout per makerdiary Connect Kit U7 (MFFx_M2M_UICC)
CUSTOM["MFF2_eUICC"] = ic_symbol(
    "MFF2_eUICC",
    left=[("8", "VCC", "power_in"), ("7", "RST", "input"), ("6", "CLK", "input"), ("3", "IO", "bidirectional")],
    right=[("2", "NC", "no_connect"), ("4", "NC", "no_connect"), ("5", "NC", "no_connect")],
    bottom=[("1", "GND", "power_in")],
    footprint="Bingbong_v3:MFF2_DFN-8_5x6", datasheet="ETSI TS 102 671",
    description="MFF2 eUICC, ISO 7816-3 class C (1.8 V), SGP.32")

# SN74LVC2G34 SCES359J, DCK SC70-6: 1 1A, 2 GND, 3 2A, 4 2Y, 5 VCC, 6 1Y. Inputs 5.5 V tolerant, Ioff.
CUSTOM["SN74LVC2G34"] = ic_symbol(
    "SN74LVC2G34",
    units=[dict(left=[("1", "1A", "input")], right=[("6", "1Y", "output")]),
           dict(left=[("3", "2A", "input")], right=[("4", "2Y", "output")]),
           dict(top=[("5", "VCC", "power_in")], bottom=[("2", "GND", "power_in")])],
    footprint="Bingbong_v3:TI_DCK0006A_SC70-6", datasheet=TI + "sn74lvc2g34.pdf",
    description="Dual buffer, 5.5 V tolerant inputs, Ioff")

# TPD4E05U06 SLVSBO7O, DQA USON-10: D1+ 1, D1- 2, D2+ 4, D2- 5, GND 3/8, NC 6/7/9/10
CUSTOM["TPD4E05U06"] = ic_symbol(
    "TPD4E05U06",
    left=[("1", "D1+", "passive"), ("2", "D1-", "passive"), ("4", "D2+", "passive"), ("5", "D2-", "passive")],
    right=[("6", "NC", "no_connect"), ("7", "NC", "no_connect"), ("9", "NC", "no_connect"), ("10", "NC", "no_connect")],
    bottom=[("3", "GND", "power_in"), ("8", "GND", "power_in")],
    footprint="Bingbong_v3:TI_DQA0010_USON-10", datasheet=TI + "tpd4e05u06.pdf",
    description="4-ch ESD, 5.5 V VRWM, 0.5 pF")

# IQS211B Azoteq datasheet v2.8.1 Table 2.1, TSOT23-6
CUSTOM["IQS211B"] = ic_symbol(
    "IQS211B",
    left=[("5", "VDDHI", "power_in"), None, ("4", "VREG", "passive"), None, ("1", "IO1/SCL", "bidirectional"),
          ("3", "IO2/SDA", "bidirectional")],
    right=[("6", "Cx", "passive")], bottom=[("2", "VSS", "power_in")],
    footprint="Package_TO_SOT_SMD:TSOT-23-6", datasheet="https://www.azoteq.com/images/stories/pdf/iqs211AB_datasheet.pdf",
    description="Capacitive proximity/touch, I2C 0x47, RDY on SCL")

# DRV2625 SLOS879C Table 4-1, YFF DSBGA-9
CUSTOM["DRV2625"] = ic_symbol(
    "DRV2625",
    left=[("C2", "VDD", "power_in"), None, ("A1", "TRIG/INTZ", "bidirectional"), ("B1", "SDA", "bidirectional"),
          ("C1", "SCL", "input"), None, ("B2", "NRST", "input")],
    right=[("A3", "OUT+", "output"), None, ("C3", "OUT-", "output"), None, None, ("A2", "REG", "passive")],
    bottom=[("B3", "GND", "power_in")],
    footprint="Bingbong_v3:TI_YFF0009_DSBGA-9", datasheet=TI + "drv2625.pdf",
    description="LRA/ERM haptic driver, closed loop, I2C 0x5A")

# MX25R1635F Macronix v1.6 section 3, 8-USON 2x3 (verified: 5 = SI, 6 = SCLK)
CUSTOM["MX25R1635F"] = ic_symbol(
    "MX25R1635F",
    left=[("1", "CS#", "input"), ("6", "SCLK", "input"), ("5", "SI/SIO0", "input"), ("2", "SO/SIO1", "output")],
    right=[("3", "WP#/SIO2", "input"), ("7", "RESET#/SIO3", "input")],
    top=[("8", "VCC", "power_in")], bottom=[("4", "GND", "power_in")],
    footprint="Bingbong_v3:Macronix_USON-8_2x3", datasheet="https://www.macronix.com/Lists/Datasheet/Attachments/8702/MX25R1635F,%20Wide%20Range,%2016Mb,%20v1.6.pdf",
    description="16 Mbit SPI NOR, 1.65-3.6 V, ultra-low-power")

# TPS22916 SLVSDO5F Table 5-1, YFP 4-ball: A1 VOUT, A2 VIN, B1 GND, B2 ON
CUSTOM["TPS22916"] = ic_symbol(
    "TPS22916",
    left=[("A2", "VIN", "power_in"), ("B2", "ON", "input")], right=[("A1", "VOUT", "power_out")],
    bottom=[("B1", "GND", "power_in")],
    footprint="Bingbong_v3:TI_YFP0004_WCSP-4", datasheet=TI + "tps22916.pdf",
    description="1-5.5 V 2 A load switch, 10 nA off, QOD (C = slow)")

# MT6701QT-STD MagnTek Rev.1.5 pin list, QFN3x3-16 (I2C mode: MODE=VDD, Z=VDD per Figure 18)
CUSTOM["MT6701QT"] = ic_symbol(
    "MT6701QT",
    left=[("13", "VDD", "power_in"), ("14", "MODE", "input"), ("8", "Z/CSN", "input"), None,
          ("6", "A/SDA", "bidirectional"), ("7", "B/SCL", "input")],
    right=[("15", "OUT", "output"), ("5", "PUSH", "output"), ("11", "U/-A", "output"), ("12", "V/-B", "output"),
           ("9", "W/-Z", "output"), None, ("1", "NC", "no_connect"), ("2", "NC", "no_connect"),
           ("3", "NC", "no_connect"), ("4", "NC", "no_connect"), ("10", "NC", "no_connect")],
    bottom=[("16", "GND", "power_in"), ("EP", "EP", "no_connect")],
    footprint="Bingbong_v3:QFN-16_3x3_MT6701", datasheet="MagnTek MT6701 Rev.1.5 (firmware/bingbong_pcb/_mech/mt6701.pdf)",
    description="14-bit magnetic angle sensor, I2C 0x06, VDD 3.0-5.5 V")

# DRV5032DU SLVSDC7, DMR X2SON-4: 1 VCC, 2 GND, 3 OUT2 (south), 4 OUT1 (north), PAD NC
CUSTOM["DRV5032DU"] = ic_symbol(
    "DRV5032DU",
    left=[("1", "VCC", "power_in")], right=[("4", "OUT1_N", "output"), ("3", "OUT2_S", "output")],
    bottom=[("2", "GND", "power_in"), ("5", "PAD", "passive")],
    footprint="Bingbong_v3:TI_DMR0004_X2SON-4", datasheet=TI + "drv5032.pdf",
    description="Dual-unipolar Hall latch, 3.9 mT, 20 Hz, push-pull, 1.6 uA")

# AS5600L ams DS000545 v1-12, WLCSP-15 (Figure 6). 3.3 V mode: VDD5V + VDD3V3 tied (Figure 14).
CUSTOM["AS5600L_WLCSP"] = ic_symbol(
    "AS5600L_WLCSP",
    left=[("A3", "VDD5V", "power_in"), ("C3", "VDD3V3", "power_in"), None, ("D1", "SDA", "bidirectional"),
          ("B1", "SCL", "input"), None, ("A1", "DIR", "input"), ("E1", "PGO", "input")],
    right=[("D3", "OUT", "output"), None, ("B2", "NC", "no_connect"), ("B3", "NC", "no_connect"),
           ("C2", "NC", "no_connect"), ("D2", "NC", "no_connect")],
    bottom=[("E3", "GND", "power_in"), ("A2", "TEST", "passive"), ("C1", "TEST", "passive"), ("E2", "TEST", "passive")],
    footprint="Bingbong_v3:ams_WLCSP-15_2.07x2.63_P0.5", datasheet="https://www.infineon.com/assets/row/public/documents/24/49/infineon-as5600l-datasheet-en.pdf",
    description="12-bit magnetic angle sensor, I2C 0x40, 3.0-3.6 V (3.3 V mode)")

# TPS65631 SLVSBK1E Pin Functions, DPD WSON-12 3x3: 1 SWP, 2 PGND, 3 OUTP, 4 FBS, 5 AGND, 6 GND, 7 CTRL,
# 8 CT, 9 OUTN, 10 SWN, 11 AVIN, 12 PVIN, 13 exposed pad (to AGND + PGND)
CUSTOM["TPS65631"] = ic_symbol(
    "TPS65631",
    left=[("12", "PVIN", "power_in"), ("11", "AVIN", "power_in"), None, ("7", "CTRL", "input"), None,
          ("8", "CT", "passive")],
    right=[("1", "SWP", "output"), ("3", "OUTP", "power_out"), ("4", "FBS", "input"), None,
           ("10", "SWN", "output"), ("9", "OUTN", "power_out")],
    bottom=[("2", "PGND", "power_in"), ("5", "AGND", "power_in"), ("6", "GND", "power_in"), ("13", "EP", "passive")],
    footprint="Bingbong_v3:TI_DPD0012_WSON-12_3x3", datasheet=TI + "tps65631.pdf",
    description="AMOLED supply: boost VPOS 4.6 V + inverting VNEG -1.4..-4.4 V (CTRL pulse count), active discharge")

# TPS7A02 SBVS277C Table 5-1, DQN X2SON-4 1x1: 1 OUT, 2 GND, 3 EN, 4 IN, thermal pad = GND
CUSTOM["TPS7A02_DQN"] = ic_symbol(
    "TPS7A02_DQN",
    left=[("4", "IN", "power_in"), ("3", "EN", "input")], right=[("1", "OUT", "power_out")],
    bottom=[("2", "GND", "power_in"), ("5", "PAD", "passive")],
    footprint="Bingbong_v3:TI_DQN0004A_X2SON-4_1x1", datasheet=TI + "tps7a02.pdf",
    description="200 mA LDO, 25 nA IQ, EN pull-down, P = active output discharge")

# SN74LV1T34 SCLS743E Table 5-1, DCK SC70-5 / DBV: 1 NC, 2 A, 3 GND, 4 Y, 5 VCC. VIH 1.39 V max at VCC 3.0-3.3 V
CUSTOM["SN74LV1T34"] = ic_symbol(
    "SN74LV1T34",
    left=[("2", "A", "input"), ("1", "NC", "no_connect")], right=[("4", "Y", "output")],
    top=[("5", "VCC", "power_in")], bottom=[("3", "GND", "power_in")],
    footprint="Bingbong_v3:TI_DCK0005A_SC70-5", datasheet=TI + "sn74lv1t34.pdf",
    description="Single buffer, low-threshold (LVxT) inputs: 1.8 V -> 3.3 V up-translation, 5.5 V tolerant")

# TCA9406 SCPS221G Pin Functions, YZP DSBGA-8: A1 SDA_B, B1 GND, C1 VCCA, D1 SDA_A, D2 SCL_A, C2 OE, B2 VCCB, A2 SCL_B
CUSTOM["TCA9406_YZP"] = ic_symbol(
    "TCA9406_YZP",
    left=[("C1", "VCCA", "power_in"), ("C2", "OE", "input"), None, ("D1", "SDA_A", "bidirectional"),
          ("D2", "SCL_A", "bidirectional")],
    right=[("B2", "VCCB", "power_in"), None, None, ("A1", "SDA_B", "bidirectional"), ("A2", "SCL_B", "bidirectional")],
    bottom=[("B1", "GND", "power_in")],
    footprint="Bingbong_v3:TI_YZP0008_DSBGA-8", datasheet=TI + "tca9406.pdf",
    description="2-bit I2C level translator, internal 10k pull-ups, Hi-Z when OE low or either VCC = 0")
