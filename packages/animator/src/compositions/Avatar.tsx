import React from 'react';
import {AbsoluteFill} from 'remotion';
import {DEX, KIP} from '../rig/characters';
import {Face} from '../rig/Face';
import {cowlickPath} from '../rig/Stickman';
import type {CharacterSpec, Expression} from '../rig/types';
import {C} from '../style/theme';

// Profile pictures are seen as small as ~32 px, so lines are much thicker than in
// the episodes (30 px at 800 px is still ~1.2 px at 32 px).
const OUTLINE = 30;

type HeadProps = {
  spec: CharacterSpec;
  expr: Expression;
  cx: number;
  cy: number;
  r: number;
  tilt?: number;
  facing?: 1 | -1;
  hair?: number;
  hairQ?: number;
  lookX?: number;
  hideRightEye?: boolean;
};

const Head: React.FC<HeadProps> = ({spec, expr, cx, cy, r, tilt = 0, facing = 1, hair = 0, hairQ = 0, lookX = 0}) => {
  const k = r / 60;
  return (
    <g transform={`translate(${cx} ${cy}) rotate(${tilt}) scale(${facing * k} ${k})`}>
      <circle r={60} fill={C.white} stroke={C.ink} strokeWidth={OUTLINE / k} />
      <Face spec={spec} expr={expr} mouth={0} lookX={lookX} lookY={0} blink={1} />
      {spec.cowlick ? <path d={cowlickPath(hair, hairQ)} stroke={C.ink} strokeWidth={(OUTLINE * 0.85) / k} fill="none" strokeLinecap="round" /> : null}
    </g>
  );
};

/** Kip's scarf and a hint of body under a big head. */
const ScarfAndBody: React.FC<{cx: number; bottom: number; w: number}> = ({cx, bottom, w}) => {
  const y = bottom + w * 0.22;
  const knot = {x: cx + w * 0.42, y: y + 4};
  return (
    <g strokeLinecap="round" strokeLinejoin="round" fill="none">
      <path d={`M ${cx} ${bottom - 20} L ${cx - 6} 820`} stroke={C.ink} strokeWidth={OUTLINE} />
      <path d={`M ${knot.x} ${knot.y} L ${knot.x - 18} ${knot.y + w * 0.75} L ${knot.x - 48} ${knot.y + w * 1.3}`} stroke={C.ink} strokeWidth={w * 0.5 + 20} />
      <path d={`M ${knot.x} ${knot.y} L ${knot.x - 18} ${knot.y + w * 0.75} L ${knot.x - 48} ${knot.y + w * 1.3}`} stroke={C.kip} strokeWidth={w * 0.5 - 8} />
      <path d={`M ${cx - w} ${y} L ${cx + w} ${y}`} stroke={C.ink} strokeWidth={w * 0.62 + 24} />
      <path d={`M ${cx - w} ${y} L ${cx + w} ${y}`} stroke={C.kip} strokeWidth={w * 0.62 - 4} />
      <circle cx={knot.x} cy={knot.y} r={w * 0.26} fill={C.kip} stroke={C.ink} strokeWidth={14} />
    </g>
  );
};

/** Magnifying glass over Kip's (viewer's) right eye, with the eye enlarged inside. */
const Magnifier: React.FC<{ex: number; ey: number; r: number; eyeScale: number}> = ({ex, ey, r, eyeScale}) => {
  const d = r * 0.7071;
  return (
    <g>
      <path d={`M ${ex + d + 6} ${ey + d + 6} L ${ex + d + 150} ${ey + d + 150}`} stroke={C.ink} strokeWidth={58} strokeLinecap="round" />
      <path d={`M ${ex + d + 40} ${ey + d + 40} L ${ex + d + 142} ${ey + d + 142}`} stroke={C.kip} strokeWidth={26} strokeLinecap="round" />
      <circle cx={ex} cy={ey} r={r} fill={C.white} />
      <circle cx={ex} cy={ey} r={r} fill={C.sky} opacity={0.16} />
      <ellipse cx={ex + 6} cy={ey + 4} rx={7.5 * eyeScale} ry={10.5 * eyeScale} fill={C.ink} />
      <circle cx={ex + 6 + 2.8 * eyeScale} cy={ey + 4 - 4.2 * eyeScale} r={2.8 * eyeScale} fill={C.white} />
      <path d={`M ${ex - r * 0.62} ${ey - r * 0.22} A ${r * 0.66} ${r * 0.66} 0 0 1 ${ex - r * 0.18} ${ey - r * 0.64}`} stroke={C.white} strokeWidth={16} fill="none" strokeLinecap="round" opacity={0.95} />
      <circle cx={ex} cy={ey} r={r} fill="none" stroke={C.ink} strokeWidth={OUTLINE + 4} />
    </g>
  );
};

export type AvatarVariant = 'curious' | 'magnifier' | 'duo';

export const Avatar: React.FC<{variant: AvatarVariant; bg: string}> = ({variant, bg}) => {
  const halo = bg === C.ink ? 0.08 : 0.14;
  let art: React.ReactNode;

  if (variant === 'curious') {
    const cx = 392;
    const cy = 400;
    const r = 205;
    art = (
      <>
        <ScarfAndBody cx={cx} bottom={cy + r} w={150} />
        <Head spec={KIP} expr="intrigued" cx={cx} cy={cy} r={r} tilt={-5} lookX={0.2} />
      </>
    );
  } else if (variant === 'magnifier') {
    const cx = 368;
    const cy = 405;
    const r = 205;
    const k = r / 60;
    // Kip's right eye in head-local coords is (27, -6); the lens sits a little
    // further right so his normal eye stays fully visible beside it.
    const ex = cx + 27 * k + 34;
    const ey = cy - 6 * k;
    art = (
      <>
        <ScarfAndBody cx={cx} bottom={cy + r} w={145} />
        <Head spec={KIP} expr="intrigued" cx={cx} cy={cy} r={r} />
        <Magnifier ex={ex} ey={ey} r={108} eyeScale={k * 1.8} />
      </>
    );
  } else {
    art = (
      <>
        <Head spec={DEX} expr="deadpan" cx={545} cy={330} r={150} facing={-1} />
        <ScarfAndBody cx={320} bottom={430 + 190} w={130} />
        <Head spec={KIP} expr="intrigued" cx={320} cy={430} r={190} tilt={-4} hairQ={1} />
      </>
    );
  }

  return (
    <AbsoluteFill style={{background: bg}}>
      <svg width={800} height={800} viewBox="0 0 800 800">
        <circle cx={400} cy={400} r={330} fill={C.white} opacity={halo} />
        {art}
      </svg>
    </AbsoluteFill>
  );
};
