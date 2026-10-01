// A deliberately small, auditable teaching circuit. This is NOT a fitted
// electromagnetic model of bingbong or its proposed dual-band RF network.
export const REFERENCE_MHZ = 722;
export const Z0 = 50;
export const COIL_Q = 50;
const omega = mhz => 2 * Math.PI * mhz * 1e6;
const bareCapacitance = 1 / (omega(REFERENCE_MHZ) * 150);

export const loads = {
  bare: { name: 'Bare device', radiation: 6, loss: 4, capacitance: bareCapacitance,
    description: 'Assume 10 − j150 Ω at 722 MHz: 6 Ω represents radiation, 4 Ω represents heat. These are teaching values, not measured antenna data.' },
  hand: { name: 'Hand nearby', radiation: 6, loss: 14, capacitance: bareCapacitance * 1.23,
    description: 'This hypothetical hand adds capacitance and absorption. Keep the old match first, then retune: less reflection cannot recover energy absorbed by the hand.' },
  contact: { name: 'Poor contact', radiation: 6, loss: 19, capacitance: bareCapacitance,
    description: 'A severe contact fault adds 15 Ω of series loss in this example. Retuning may improve the match while the contact still wastes power. A healthy contact is in the milliohm range.' },
  resistor: { name: '50 Ω resistor', radiation: 0, loss: 50, capacitance: Infinity,
    description: 'An ideal 50 Ω dummy load accepts all the incident power with the match bypassed. It turns that power into heat. A perfect match alone does not make an antenna.' },
  open: { name: 'Broken feed', open: true,
    description: 'An ideal open circuit has no conductive feed path. In this simplified model all power is reflected. A real gap can retain some capacitive coupling.' }
};

export function evaluateRF({ frequency = REFERENCE_MHZ, inductance = 0, capacitance = 0, load = 'bare' } = {}) {
  const antenna = loads[load] ?? loads.bare;
  if (antenna.open) return { real: capacitance > 0 ? 0 : Infinity, imaginary: capacitance > 0 ? -1 / (omega(frequency) * capacitance * 1e-12) : 0, antennaReal: Infinity, antennaImaginary: 0, reflected: 1, radiated: 0, networkHeat: 0, loadHeat: 0, accepted: 0, returnLoss: 0, vswr: Infinity };
  const w = omega(frequency);
  const antennaReal = antenna.radiation + antenna.loss;
  const antennaImaginary = -1 / (w * antenna.capacitance);
  const coilResistance = w * inductance * 1e-9 / COIL_Q;
  const r = antennaReal + coilResistance;
  const x = antennaImaginary + w * inductance * 1e-9;
  // Admittance of the antenna + series coil, in parallel with the shunt C.
  const conductance = r / (r * r + x * x);
  const susceptance = -x / (r * r + x * x) + w * capacitance * 1e-12;
  const real = conductance / (conductance * conductance + susceptance * susceptance);
  const imaginary = -susceptance / (conductance * conductance + susceptance * susceptance);
  const reflected = Math.min(1, ((real - Z0) ** 2 + imaginary ** 2) / ((real + Z0) ** 2 + imaginary ** 2));
  const accepted = 1 - reflected;
  const gamma = Math.sqrt(reflected);
  return { real, imaginary, antennaReal, antennaImaginary, reflected, accepted,
    radiated: accepted * antenna.radiation / r,
    networkHeat: accepted * coilResistance / r,
    loadHeat: accepted * antenna.loss / r,
    returnLoss: reflected === 0 ? Infinity : -10 * Math.log10(reflected),
    vswr: gamma === 1 ? Infinity : (1 + gamma) / (1 - gamma) };
}

export function cancelReactance(frequency, load) {
  const antenna = loads[load];
  return antenna.open ? 0 : 1e9 / (omega(frequency) ** 2 * antenna.capacitance);
}

// Solve X² = R(50 − R), including the inductor's frequency-dependent ESR.
// The positive-X root supports a radio-side shunt capacitor.
export function matchRF(frequency, load) {
  const antenna = loads[load];
  if (antenna.open) return null;
  if (load === 'resistor') return { inductance: 0, capacitance: 0 };
  const w = omega(frequency), baseR = antenna.radiation + antenna.loss;
  let lo = cancelReactance(frequency, load), hi = 65;
  const residual = l => {
    const x = -1 / (w * antenna.capacitance) + w * l * 1e-9;
    const r = baseR + w * l * 1e-9 / COIL_Q;
    return x * x - r * (Z0 - r);
  };
  if (residual(lo) > 0 || residual(hi) < 0) return null;
  for (let i = 0; i < 60; i++) {
    const mid = (lo + hi) / 2;
    if (residual(mid) > 0) hi = mid; else lo = mid;
  }
  const inductance = (lo + hi) / 2;
  const x = -1 / (w * antenna.capacitance) + w * inductance * 1e-9;
  const r = baseR + w * inductance * 1e-9 / COIL_Q;
  return { inductance, capacitance: x / (w * Z0 * r) * 1e12 };
}

export function parallelLCReactance(frequency, inductance = 15, capacitance = 1) {
  const w = omega(frequency);
  return w * inductance * 1e-9 / (1 - w * w * inductance * 1e-9 * capacitance * 1e-12);
}
