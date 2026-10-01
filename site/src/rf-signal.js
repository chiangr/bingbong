// Explicit teaching models. No measured RF, LTE stack, or delivery service.
export const QPSK = [
  { bits: '00', phase: 45 }, { bits: '01', phase: 135 },
  { bits: '11', phase: 225 }, { bits: '10', phase: 315 }
];
export const radians = degrees => degrees * Math.PI / 180;
export const symbolFor = bits => QPSK.find(s => s.bits === bits);

export function encodeMessage(message) {
  if (!/^[\x20-\x7e]{1,6}$/.test(message)) return null;
  const bytes = [...message].map(char => ({ char, value: char.charCodeAt(0), bits: char.charCodeAt(0).toString(2).padStart(8, '0') }));
  const bits = bytes.map(byte => byte.bits).join('');
  return { bytes, bits, symbols: bits.match(/.{2}/g).map(symbolFor) };
}

export function decideQPSK(i, q) {
  // Gray mapping used throughout this lesson. A point on an axis is ambiguous.
  const bits = i >= 0 ? (q >= 0 ? '00' : '10') : (q >= 0 ? '01' : '11');
  return { bits, phase: symbolFor(bits).phase, margin: Math.min(Math.abs(i), Math.abs(q)) };
}

export function measurePilot(rotation, amplitude = .65) {
  // An ideal, noiseless known 00 pilot. Real pilot estimates are uncertain.
  const phase = radians(45 + rotation);
  const i = amplitude * Math.cos(phase), q = amplitude * Math.sin(phase);
  const observed = Math.atan2(q, i) * 180 / Math.PI;
  const estimate = ((observed - 45 + 540) % 360) - 180;
  return { i, q, observed, estimate };
}

export function receivedSample(t, symbol, index, { rotation = 0, interference = 0, amplitude = .65, cycles = 4 } = {}) {
  const carrier = 2 * Math.PI * cycles * t;
  const desired = amplitude * Math.cos(carrier + radians(symbol.phase + rotation));
  // Repeatable interference: a co-channel tone plus a higher-frequency tone.
  // This makes individual failures reproducible; it is NOT an AWGN/BER model.
  const disturbance = interference * (.7 * Math.cos(carrier + 1.2 + index * 2.399) + .35 * Math.sin(2 * Math.PI * 11 * t + index));
  return { desired, disturbance, value: desired + disturbance };
}

export function demodulateSymbol(symbol, index = 0, options = {}, progress = 1) {
  const samples = 256, cycles = options.cycles ?? 4;
  const duration = Math.min(1, Math.max(0, progress));
  const steps = Math.ceil(samples * duration);
  let i = 0, q = 0;
  const referencePhase = radians(options.locked ? measurePilot(options.rotation ?? 0, options.amplitude ?? .65).estimate : 0);
  // Midpoint integration with fixed full-symbol normalization. Partial values
  // are running integrals; decisions are made only at the symbol boundary.
  for (let n = 0; n < steps; n++) {
    const left = n / samples, right = Math.min((n + 1) / samples, duration);
    const t = (left + right) / 2, dt = right - left;
    const r = receivedSample(t, symbol, index, options).value;
    const reference = 2 * Math.PI * cycles * t + referencePhase;
    i += 2 * r * Math.cos(reference) * dt;
    q += -2 * r * Math.sin(reference) * dt;
  }
  return { i, q, ...decideQPSK(i,q) };
}

export function decodeMessage(encoded, options = {}, count = encoded.symbols.length) {
  const results = encoded.symbols.slice(0,count).map((symbol,index) => demodulateSymbol(symbol,index,options));
  const bits = results.map(s => s.bits).join('');
  const bytes = (bits.match(/.{8}/g) ?? []).map(byte => parseInt(byte,2));
  return { results, bits, bytes,
    text: bytes.map(byte => byte>=32 && byte<=126 ? String.fromCharCode(byte) : '�').join(''),
    errors: [...bits].filter((bit,index) => bit!==encoded.bits[index]).length };
}

export function reflectionVector(real, imaginary, z0 = 50) {
  if (!Number.isFinite(real)) return { real: 1, imaginary: 0, magnitude: 1, phase: 0 };
  const d = (real + z0) ** 2 + imaginary ** 2;
  const re = (real ** 2 + imaginary ** 2 - z0 ** 2) / d;
  const im = 2 * z0 * imaginary / d;
  return { real: re, imaginary: im, magnitude: Math.hypot(re,im), phase: Math.atan2(im,re) };
}

export function lcCurrents(frequency, phase, inductance = 15, capacitance = 1) {
  const w = 2 * Math.PI * frequency * 1e6, theta = radians(phase);
  const l = inductance * 1e-9, c = capacitance * 1e-12;
  // Apply the same 1 V peak sinusoid across both ideal parallel branches.
  const voltage = Math.cos(theta);
  const inductor = Math.sin(theta) / (w * l);
  const capacitor = -w * c * Math.sin(theta);
  return { voltage, inductor, capacitor, total: inductor + capacitor,
    magnetic: .5 * l * inductor ** 2, electric: .5 * c * voltage ** 2,
    resonance: 1 / (2 * Math.PI * Math.sqrt(l*c)) / 1e6 };
}
