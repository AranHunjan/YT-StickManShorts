import type {Limb, Pose} from './types';

/**
 * Short motions layered on top of whatever pose a character holds (beats.json "moves").
 * They let the listener react mid-line and the speaker stress a word, with the camera
 * still. `u` runs 0 -> 1 over the gesture; `env` eases in over 0.25 s and out over 0.3 s,
 * for gestures that hold (tilt).
 */
type Gesture = {dur: number; hold?: boolean; delta: (u: number, env: number) => Partial<Pose>};

const clamp = (x: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, x));
const smooth = (a: number, b: number, x: number) => {
  const t = clamp((x - a) / (b - a), 0, 1);
  return t * t * (3 - 2 * t);
};
const bump = (u: number) => Math.sin(Math.PI * clamp(u, 0, 1)); // 0 -> 1 -> 0

export const GESTURES = {
  /** Two small dips of the head: agreeing, following along. */
  nod: {dur: 0.6, delta: (u) => {
    const d = (1 - Math.cos(4 * Math.PI * u)) / 2;
    return {head: 9 * d, lookY: 0.3 * d};
  }},
  /** Curious head tilt that holds (use "until"); Kip's cowlick curls toward a "?". */
  tilt: {dur: 1.4, hold: true, delta: (_u, env) => ({head: 13 * env, lookY: -0.35 * env, hairQ: 0.8 * env})},
  /** Glance away, then snap back with a jolt: "wait, what?" */
  doubleTake: {dur: 1.0, delta: (u) => {
    const away = smooth(0, 0.25, u) * (1 - smooth(0.3, 0.38, u));
    const snap = smooth(0.3, 0.4, u) * (1 - smooth(0.55, 1, u));
    return {lookX: -1.2 * away + 0.4 * snap, head: 5 * away - 12 * snap, lean: -9 * snap, lift: 14 * snap, hair: 0.8 * snap, squash: 0.04 * snap};
  }},
  /** Warm chuckle: head back, small shoulder bounces. Dex's amused reaction. */
  laugh: {dur: 1.0, delta: (u) => {
    const e = bump(u);
    return {head: -7 * e, lean: -3 * e, squash: 0.03 * Math.sin(12 * Math.PI * u) * e, lift: 4 * Math.abs(Math.sin(6 * Math.PI * u)) * e};
  }},
  /** Two quick excited hops. */
  bounce: {dur: 0.6, delta: (u) => ({lift: 16 * Math.abs(Math.sin(2 * Math.PI * u)), armF: [12 * bump(u), 0] as Limb, armB: [-12 * bump(u), 0] as Limb})},
  /** "No, no": a small head shake. */
  shake: {dur: 0.7, delta: (u) => {
    const s = Math.sin(6 * Math.PI * u) * bump(u);
    return {head: 6 * s, lookX: 0.5 * s};
  }},
  /** The speaker's beat on a key word: a forward arm push and a small lean. */
  emphasis: {dur: 0.45, delta: (u) => {
    const e = bump(u);
    return {armF: [18 * e, -12 * e] as Limb, head: 4 * e, lean: 3 * e};
  }},
} satisfies Record<string, Gesture>;

export type GestureName = keyof typeof GESTURES;

export type Move = {
  who: 'kip' | 'dex';
  at: string; // "L05@0.45"
  pose?: string; // switch pose mid-line
  expr?: string; // switch expression mid-line
  gesture?: GestureName;
  dur?: number; // seconds, overrides the gesture's default
  until?: string; // end time for holding gestures (tilt)
};

function sum(a: Partial<Pose>, b: Partial<Pose>): Partial<Pose> {
  const out: Record<string, number | Limb> = {...(a as Record<string, number | Limb>)};
  for (const [k, v] of Object.entries(b) as [string, number | Limb][]) {
    const cur = out[k];
    if (cur === undefined) out[k] = v;
    else if (Array.isArray(v)) out[k] = [(cur as Limb)[0] + v[0], (cur as Limb)[1] + v[1]];
    else out[k] = (cur as number) + v;
  }
  return out as Partial<Pose>;
}

/** The summed deltas of every gesture this character is doing at `sec`, or null if none. */
export function gestureDelta(moves: Move[], who: 'kip' | 'dex', sec: number, T: (ref: string) => number): Partial<Pose> | null {
  let out: Partial<Pose> | null = null;
  for (const m of moves) {
    if (m.who !== who || !m.gesture) continue;
    const g: Gesture = GESTURES[m.gesture];
    const start = T(m.at);
    const end = m.until ? T(m.until) : start + (m.dur ?? g.dur);
    if (sec < start || sec > end) continue;
    const u = (sec - start) / Math.max(end - start, 1e-3);
    const env = smooth(start, start + 0.25, sec) * (1 - smooth(end - 0.3, end, sec));
    const d = g.delta(u, env);
    out = out ? sum(out, d) : d;
  }
  return out;
}

/** Keep stacked deltas inside the ranges the rig draws well. */
export const clampPose = (p: Pose): Pose => ({
  ...p,
  hair: clamp(p.hair, -1, 1),
  hairQ: clamp(p.hairQ, 0, 1),
  lookX: clamp(p.lookX, -1.2, 1.2),
  lookY: clamp(p.lookY, -1.2, 1.2),
});
