# RF study — source register

Added September 24, 2026. Open the lab at `/#rf-lab`.

## Construction authority

- `DESIGN_MANUFACTURING_REPORT_2026-09-19.md`, §3 C-5: adopted vertical spring contact, L-shaped cap tab, sealed ring aperture, and shortened board.
- Same report, §§5.4–5.6: whole-device radiating structure, counterpoise, fields, feed reference plane, materials, keepout, matching topology, and explicitly unverified performance/values.
- `cad-v3/tools/sheet_rf.py` and `cad-v3/bingbong/rf.kicad_sch`: working component references and connections. The overview schematic shows the populated proposed path; the detailed inspector covers all 16 references, including the DNP trim and harmonic-trap positions.
- Existing `site/src/assembly-data.js`: visual construction terminology.

The v3 schematic was already present as untracked working material when this task began. It was read and not modified.

## Primary references

- [Nordic nRF9151 ANT integration](https://docs.nordicsemi.com/r/bundle/nwp_056/page/wp/nwp_054/ant_if.html) and [pin assignments](https://docs.nordicsemi.com/r/bundle/ps_nrf9151/page/pin.html): single-ended 50 Ω antenna interface, pin 35.
- [TI SWRA726](https://www.ti.com/lit/an/swra726/swra726.pdf): antenna impedance measurement, enclosure/hand detuning, calibration, and matching. Its lossless-antenna examples must not be interpreted as proof that all accepted power radiates. This study explicitly separates reflection, component loss, antenna/environment loss, and radiation.
- [Analog Devices impedance matching tutorial](https://www.analog.com/en/resources/technical-articles/impedance-matching-and-smith-chart-impedance-maxim-integrated.html): complex impedance and series/shunt impedance transformations.
- [NI quadrature mixing](https://www.ni.com/docs/en-US/bundle/pxie-5820/page/quadrature-mixing.html): orthogonal references, I/Q modulation, and demodulation.
- [MIT Electromagnetic Fields and Energy, chapter 12](https://ocw.mit.edu/courses/res-6-001-electromagnetic-fields-and-energy-spring-2008/pages/chapter-12/): electrodynamic fields, radiation, and energy flow.
- [3GPP / ETSI TS 36.211, Release 13](https://www.etsi.org/deliver/etsi_ts/136200_136299/136211/13.11.00_60/ts_136211v131100p.pdf): LTE modulation and baseband generation. The lesson explicitly distinguishes the nominal carrier reference from the spectrum of a changing signal, and the single-carrier QPSK example from LTE’s downlink OFDM and uplink SC-FDMA processing.

## Discrepancy handled explicitly

Report §5.6 Step 12 describes probing the antenna through J301, whereas the v3 schematic wires the common/probe side to the IC and the normally closed branch to the antenna. The study follows the actual v3 drawing and explains this in its source notes. An antenna-side fixture and appropriate calibration are needed for antenna impedance measurements. The schematic drawing and contact geometry do not establish measured RF performance.

## Teaching model

`src/rf-model.js` implements a radio-side shunt C, followed by a series L with constant Q = 50, feeding a hypothetical series R–C antenna load. The 50 Ω feed is assumed lossless and omitted. Values can be varied from 650–850 MHz, 0–65 nH, and 0–24 pF.

- Bare: Rradiation = 6 Ω, Rloss = 4 Ω, Cantenna = 1/(2π × 722 MHz × 150 Ω), giving 10 − j150 Ω at 722 MHz.
- Hand: Rloss = 14 Ω and antenna C increased 23%.
- Poor contact: Rloss = 19 Ω, including a severe illustrative 15 Ω contact fault.
- Dummy load: ideal 50 Ω resistor, no radiation.
- Open feed: open antenna branch; any remaining shunt capacitance is still visible at the input, with total reflection and no real power transfer.

Inductor ESR is ωL/Q; capacitors are ideal. All accepted power is divided by the series resistances. The four power fractions sum to one. Radiation/loss resistance is held constant across the sweep. There is no calibrated geometry model, range prediction, antenna radiation pattern, actual dual-band solution, or claim of automatic hardware tuning.

The field illustration represents charge and current in an idealized standing-wave mode. It is neither a Maxwell field solution nor a computed radiation pattern. The QPSK illustration uses the explicit Gray mapping 00/01/11/10 → 45/135/225/315 degrees and does not implement an LTE PHY. The message journey includes the cellular network and delivery service instead of implying direct keychain-to-keychain RF.

## Detailed first-principles models

- **Charge and fields:** the quantitative capacitor example uses 1 pF, 1 V peak, and 722 MHz. `q = Cv` and `i = dq/dt` give 1 pC and 4.54 mA peaks. It is a charge-storage example, not the measured cap input impedance. The outgoing plane-wave slice uses `cos[ω(t − z/c)]`; normalized E and cB are in phase and drawn vertically offset, with their actual perpendicular directions explained. Reactive near fields and far-field radiation are explicitly distinguished.
- **Individual parts:** voltage and current are calculated for isolated ideal capacitors/inductors at 1 V peak and 722 MHz. Energy readouts use `½Cv²` and `½Li²`. These are not circuit-node voltages or a simulation of the assembled network. The ESD example only models its provisional off-state capacitance. DNP means no fitted element, not zero pad parasitics.
- **Parallel LC:** L302 = 15 nH and C302 = 1 pF share an imposed sinusoidal voltage. Current amplitudes are `1/(ωL)` and `ωC`, with opposite signs. At approximately 1299.495 MHz, input currents cancel while branch currents remain. Finite Q and self-resonance are omitted; the resulting infinite ideal impedance is not a hardware prediction. The UI rounds the resonance preset to 0.01 MHz, so it shows a large finite impedance near the peak. The series-LC trap is explained separately.
- **Reflections:** incident/reflected voltage superposition includes the complex phase of Γ from the bench. The drawn transmission line is one wavelength long, lossless, and 50 Ω to make propagation readable. It does not represent the actual PCB length. Reflected voltage amplitude is |Γ| and power is |Γ|².
- **Message recovery:** 1–6 printable ASCII characters become bytes and two-bit symbols. The normalized carrier has four cycles per symbol; no physical LTE symbol rate is implied. Rectangular windows and abrupt transitions are idealizations; real pulse shaping, occupied bandwidth, and timing recovery are explained. The code performs midpoint integration of `2r cos(reference)` and `−2r sin(reference)` with 256 samples per complete window and full-symbol normalization. Partial integrals are never presented as completed decisions. The four integer carrier cycles make the double-frequency term average to zero in the clean reference case.
- **Channel and pilot:** the desired amplitude is 0.65. Phase rotation spans ±90°. An ideal, noiseless known 00/45° pilot provides I/Q; `atan2(Qp, Ip) − 45°` measures the channel offset used by both local references. This deliberate simplification is stated next to the control; real receivers have estimation error. Interference combines a co-channel tone and an 11-cycle-per-symbol tone with repeatable phase variation, not AWGN or a statistical BER model. It affects data, not this ideal pilot. Hard quadrant decisions have no error correction. Error counts compare with the known transmitted bits; a real receiver cannot directly make that comparison on unknown data. Non-printable recovered bytes display a replacement character and retain their byte values.

All animations are manually started, pause on close/chapter changes, and offer manual phase or symbol controls. Reduced-motion users step phases or recover the message without playback. The phone receiver keeps a compact result visible while its controls are adjusted.

## Verification

Run `npm run build`, `npm run artifact`, then the production preview on port 4173, `node scripts/rf-check.mjs`, and `node scripts/rf-lessons-check.mjs`. Results and representative screenshots are saved in this directory and `deep/`. The scripts check analytical reference cases, passive energy conservation, known I/Q identities, ASCII round-trips, pilot recovery, LC cancellation, component controls, reduced motion, keyboard tabs/sliders, animation lifecycle, history/focus return, a paused background renderer, all panels with axe, narrow layouts, no-JS reading, and standalone operation.
