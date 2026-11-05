import React from 'react';
import {Face} from './Face';
import {hang, solve} from './skeleton';
import type {CharacterSpec, Expression, Joints, Pose, Pt} from './types';

// Cowlick key shapes at R = 60 (P0 C c1 c2 P1 C c3 c4 P2), facing right.
type Shape = [number, number][];
const HAIR: Record<'normal' | 'up' | 'droop' | 'question', Shape> = {
  normal: [[2, -56], [6, -84], [-16, -98], [-26, -84], [-32, -75], [-22, -66], [-14, -73]],
  up: [[2, -56], [4, -80], [-3, -98], [2, -116], [6, -130], [20, -128], [16, -116]],
  droop: [[2, -56], [-8, -70], [-30, -74], [-46, -62], [-54, -55], [-55, -44], [-50, -38]],
  question: [[2, -56], [2, -70], [-10, -78], [-12, -92], [-14, -112], [18, -118], [22, -100]],
};
const mix = (a: Shape, b: Shape, t: number): Shape => a.map(([x, y], i) => [x + (b[i][0] - x) * t, y + (b[i][1] - y) * t]);

/** Cowlick path in head-local coordinates (R = 60, facing right). */
export function cowlickPath(hair: number, hairQ: number, wig = 0): string {
  let s = hair >= 0 ? mix(HAIR.normal, HAIR.up, hair) : mix(HAIR.normal, HAIR.droop, -hair);
  s = mix(s, HAIR.question, hairQ);
  s = s.map(([x, y], i) => [x + wig * (i / 6), y]);
  return `M ${s[0][0]} ${s[0][1]} C ${s[1][0]} ${s[1][1]}, ${s[2][0]} ${s[2][1]}, ${s[3][0]} ${s[3][1]} C ${s[4][0]} ${s[4][1]}, ${s[5][0]} ${s[5][1]}, ${s[6][0]} ${s[6][1]}`;
}

const p2 = (p: Pt) => `${p.x.toFixed(1)} ${p.y.toFixed(1)}`;
const add = (a: Pt, b: Pt, k = 1): Pt => ({x: a.x + b.x * k, y: a.y + b.y * k});

type Props = {
  spec: CharacterSpec;
  pose: Pose;
  expr: Expression;
  groundY: number;
  frame: number;
  facing?: 1 | -1;
  seed?: number;
  blink?: number;
  /** Props held in hands etc. Drawn on top, in world coordinates. */
  children?: (j: Joints) => React.ReactNode;
};

export const Stickman: React.FC<Props> = ({spec, pose, expr, groundY, frame, facing = 1, seed = 0, blink = 1, children}) => {
  const j = solve(spec, pose, groundY, facing);
  const ink = spec.ink;
  const sw = spec.stroke;
  const k = spec.headR / 60;

  const limbPath = (l: Joints['armF'], foot = 0) => {
    let d = `M ${p2(l.root)} L ${p2(l.joint)} L ${p2(l.end)}`;
    if (foot) d += ` l ${(facing * foot).toFixed(1)} 2`;
    return d;
  };
  const line = {stroke: ink, strokeWidth: sw, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const, fill: 'none'};

  // Cowlick
  let hairEl: React.ReactNode = null;
  if (spec.cowlick) {
    const wig = pose.hair > 0.5 ? 3 * Math.sin(frame * 0.9) : 1.2 * Math.sin(frame * 0.15 + seed);
    const d = cowlickPath(pose.hair, pose.hairQ, wig);
    hairEl = <path d={d} stroke={ink} strokeWidth={sw * 0.8 / k} fill="none" strokeLinecap="round" />;
  }

  // Scarf (world space)
  let scarfBack: React.ReactNode = null;
  let scarfFront: React.ReactNode = null;
  if (spec.scarf) {
    const n = j.neckBase;
    const a = add(add(n, j.up, 6), j.perp, -21);
    const b = add(add(n, j.up, 6), j.perp, 21);
    const knot = add(add(n, j.up, 2), j.perp, 14);
    const sway = 6 * Math.sin(frame * 0.18 + seed);
    const tail = (lenA: number, lenB: number, off: number) => {
      const a1 = facing * (-10 - pose.wind * 70 + off) + sway;
      const m = add(knot, hang(a1), lenA);
      const a2 = a1 + facing * (-12 - pose.wind * 12) + sway * 0.6;
      const e = add(m, hang(a2), lenB);
      return `M ${p2(knot)} L ${p2(m)} L ${p2(e)}`;
    };
    const t1 = tail(46, 40, 0);
    const t2 = tail(36, 28, 14);
    scarfBack = (
      <g strokeLinecap="round" strokeLinejoin="round" fill="none">
        <path d={t2} stroke={ink} strokeWidth={22} />
        <path d={t2} stroke={spec.accent} strokeWidth={13} />
        <path d={t1} stroke={ink} strokeWidth={24} />
        <path d={t1} stroke={spec.accent} strokeWidth={15} />
      </g>
    );
    scarfFront = (
      <g strokeLinecap="round" fill="none">
        <path d={`M ${p2(a)} L ${p2(b)}`} stroke={ink} strokeWidth={28} />
        <path d={`M ${p2(a)} L ${p2(b)}`} stroke={spec.accent} strokeWidth={19} />
        <circle cx={knot.x} cy={knot.y} r={9} fill={spec.accent} stroke={ink} strokeWidth={4} />
      </g>
    );
  }

  // Bow tie (world space)
  let bow: React.ReactNode = null;
  if (spec.bowtie) {
    const c = add(j.neckBase, j.up, -10);
    const w = (s: number) => {
      const tip1 = add(add(c, j.perp, 23 * s), j.up, 12);
      const tip2 = add(add(c, j.perp, 23 * s), j.up, -12);
      return `M ${p2(c)} L ${p2(tip1)} L ${p2(tip2)} Z`;
    };
    bow = (
      <g fill={spec.accent} stroke={ink} strokeWidth={4} strokeLinejoin="round">
        <path d={w(1)} />
        <path d={w(-1)} />
        <circle cx={c.x} cy={c.y} r={6.5} />
      </g>
    );
  }

  const headEnd = add(j.headC, j.up, -spec.headR);

  return (
    <g>
      <path d={limbPath(j.armB)} {...line} />
      <path d={limbPath(j.legB, spec.foot)} {...line} />
      {scarfBack}
      <path d={`M ${p2(j.hip)} L ${p2(j.neckBase)} L ${p2(headEnd)}`} {...line} />
      <path d={limbPath(j.legF, spec.foot)} {...line} />
      {bow}
      <g transform={`translate(${j.headC.x.toFixed(1)} ${j.headC.y.toFixed(1)}) rotate(${j.headAngle.toFixed(2)}) scale(${facing * k} ${k})`}>
        <circle r={60} fill={spec.headFill} stroke={ink} strokeWidth={sw / k} />
        <Face
          spec={spec}
          expr={expr}
          mouth={pose.mouth}
          lookX={pose.lookX}
          lookY={pose.lookY}
          blink={blink}
          jitter={expr === 'scared' ? 1.2 * Math.sin(frame * 2.3) : 0}
        />
        {hairEl}
      </g>
      {scarfFront}
      <path d={limbPath(j.armF)} {...line} />
      <circle cx={j.armF.end.x} cy={j.armF.end.y} r={sw * 0.62} fill={ink} />
      <circle cx={j.armB.end.x} cy={j.armB.end.y} r={sw * 0.62} fill={ink} />
      {children ? children(j) : null}
    </g>
  );
};
