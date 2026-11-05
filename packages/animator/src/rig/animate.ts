import {Easing, random} from 'remotion';
import type {Expression, Limb, Pose} from './types';

export type EaseName = 'linear' | 'inOut' | 'out' | 'in' | 'outBack' | 'snap';

const EASE: Record<EaseName, (t: number) => number> = {
  linear: (t) => t,
  inOut: Easing.inOut(Easing.cubic),
  out: Easing.out(Easing.cubic),
  in: Easing.in(Easing.cubic),
  outBack: Easing.out(Easing.back(1.8)),
  snap: Easing.out(Easing.exp),
};

const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
const lerpLimb = (a: Limb, b: Limb, t: number): Limb => [lerp(a[0], b[0], t), lerp(a[1], b[1], t)];

export function lerpPose(a: Pose, b: Pose, t: number): Pose {
  return {
    x: lerp(a.x, b.x, t),
    lift: lerp(a.lift, b.lift, t),
    lean: lerp(a.lean, b.lean, t),
    head: lerp(a.head, b.head, t),
    armB: lerpLimb(a.armB, b.armB, t),
    armF: lerpLimb(a.armF, b.armF, t),
    legB: lerpLimb(a.legB, b.legB, t),
    legF: lerpLimb(a.legF, b.legF, t),
    squash: lerp(a.squash, b.squash, t),
    mouth: lerp(a.mouth, b.mouth, t),
    lookX: lerp(a.lookX, b.lookX, t),
    lookY: lerp(a.lookY, b.lookY, t),
    hair: lerp(a.hair, b.hair, t),
    hairQ: lerp(a.hairQ, b.hairQ, t),
    wind: lerp(a.wind, b.wind, t),
  };
}

/** Add small deltas (for procedural overlays such as breathing). */
export function addPose(p: Pose, d: Partial<Pose>): Pose {
  const out = {...p};
  for (const k of Object.keys(d) as (keyof Pose)[]) {
    const v = d[k];
    if (v === undefined) continue;
    if (Array.isArray(v)) {
      const cur = out[k] as Limb;
      (out[k] as Limb) = [cur[0] + v[0], cur[1] + v[1]];
    } else {
      (out[k] as number) = (out[k] as number) + (v as number);
    }
  }
  return out;
}

export type Key = {
  f: number; // frame
  p?: Partial<Pose>; // overrides, accumulated from earlier keys
  e?: EaseName; // easing used to arrive at this key
  expr?: Expression;
};

/** Sample a keyframe track. Keys accumulate, so each key only lists what changes. */
export function sample(base: Pose, keys: Key[], frame: number): {pose: Pose; expr: Expression} {
  const sorted = [...keys].sort((a, b) => a.f - b.f);
  const full: Pose[] = [];
  let acc = base;
  for (const k of sorted) {
    acc = {...acc, ...(k.p ?? {})};
    full.push(acc);
  }
  let expr: Expression = 'neutral';
  for (const k of sorted) if (k.expr && k.f <= frame) expr = k.expr;

  if (sorted.length === 0) return {pose: base, expr};
  if (frame <= sorted[0].f) return {pose: full[0], expr};
  for (let i = 0; i < sorted.length - 1; i++) {
    const a = sorted[i];
    const b = sorted[i + 1];
    if (frame >= a.f && frame < b.f) {
      const t = (frame - a.f) / Math.max(b.f - a.f, 1);
      return {pose: lerpPose(full[i], full[i + 1], EASE[b.e ?? 'inOut'](t)), expr};
    }
  }
  return {pose: full[full.length - 1], expr};
}

/** Breathing idle so a character is never frozen. */
export function idle(frame: number, seed: number): Partial<Pose> {
  const s = Math.sin(frame * 0.11 + seed);
  return {
    squash: 0.012 * s,
    head: 1.2 * Math.sin(frame * 0.06 + seed * 2),
    armB: [1.5 * s, 0],
    armF: [-1.5 * s, 0],
  };
}

/** Walk cycle between two x positions. Returns overrides (not deltas). */
export function walk(frame: number, start: number, end: number, x0: number, x1: number, step = 14): Partial<Pose> | null {
  if (frame < start || frame > end) return null;
  const t = (frame - start) / Math.max(end - start, 1);
  const ph = ((frame - start) / step) * Math.PI;
  const s = Math.sin(ph);
  const lift = 7 * Math.abs(Math.cos(ph));
  const kneeF = -38 * Math.max(0, Math.cos(ph));
  const kneeB = -38 * Math.max(0, -Math.cos(ph));
  return {
    x: lerp(x0, x1, t),
    lift,
    lean: 5,
    legF: [26 * s, kneeF],
    legB: [-26 * s, kneeB],
    armF: [-22 * s, 18],
    armB: [22 * s, 18],
    wind: 0.7,
  };
}

/** Choppy, natural-looking mouth flaps while talking (changes every 2 frames). */
export function talk(frame: number, seed: string): number {
  const r = random(`${seed}-${Math.floor(frame / 2)}`);
  return 0.15 + 0.85 * r;
}

/** 0..1 eye openness with an occasional 4-frame blink. */
export function blink(frame: number, seed: number): number {
  const period = 96 + Math.floor(random(`blink-${seed}`) * 40);
  const ph = (frame + seed * 37) % period;
  if (ph < 2) return 1 - ph * 0.45;
  if (ph < 4) return 0.1 + (ph - 2) * 0.45;
  return 1;
}
