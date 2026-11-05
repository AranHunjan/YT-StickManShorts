import React from 'react';
import {C} from '../style/theme';
import type {CharacterSpec, Expression} from './types';

type BrowSet = {l: [number, number]; r: [number, number]}; // [outer dy, inner dy], negative = up

const BROWS: Record<Expression, BrowSet> = {
  neutral: {l: [0, 0], r: [0, 0]},
  happy: {l: [-2, -2], r: [-2, -2]},
  excited: {l: [-6, -6], r: [-6, -6]},
  shocked: {l: [-9, -9], r: [-9, -9]},
  mindblown: {l: [-13, -13], r: [-13, -13]},
  smug: {l: [0, 1], r: [-9, -4]},
  confused: {l: [1, 2], r: [-11, -6]},
  scared: {l: [3, -8], r: [3, -8]},
  angry: {l: [-4, 7], r: [-4, 7]},
  sleepy: {l: [2, 2], r: [2, 2]},
  determined: {l: [-2, 4], r: [-2, 4]},
  deadpan: {l: [1, 1], r: [1, 1]},
};

const TALKS: Expression[] = ['neutral', 'happy', 'excited', 'smug', 'confused', 'determined', 'deadpan', 'angry', 'scared'];

type Props = {
  spec: CharacterSpec;
  expr: Expression;
  mouth: number;
  lookX: number;
  lookY: number;
  blink: number;
  jitter?: number;
};

/** Face in head-local coordinates (head centre at 0,0, facing right, R = 60 scale). */
export const Face: React.FC<Props> = ({spec, expr, mouth, lookX, lookY, blink, jitter = 0}) => {
  const ink = spec.ink;
  const sw = 5;
  const cx = 10;
  const ey = -6;
  const half = spec.eyeSpacing / 2;
  const eyes: [number, number][] = [
    [cx - half, ey],
    [cx + half, ey],
  ];
  const lx = lookX * 5 + jitter;
  const ly = lookY * 4;
  const mx = cx + 3;

  const dot = (x: number, y: number, rx: number, ry: number, key: string) => (
    <ellipse key={key} cx={x + lx} cy={y + ly} rx={rx} ry={Math.max(ry * blink, 1.2)} fill={ink} />
  );
  const ring = (x: number, y: number, r: number, pr: number, key: string) => (
    <g key={key}>
      <ellipse cx={x} cy={y} rx={r} ry={Math.max(r * blink, 1.5)} fill={C.white} stroke={ink} strokeWidth={4.5} />
      {blink > 0.5 ? <circle cx={x + lx * 0.8} cy={y + ly * 0.8} r={pr} fill={ink} /> : null}
    </g>
  );
  const lid = (x: number, y: number, key: string) => (
    <g key={key}>
      <ellipse cx={x + lx} cy={y + 2} rx={6.5} ry={7} fill={ink} />
      <rect x={x - 11} y={y - 12} width={22} height={13} fill={spec.headFill} />
      <line x1={x - 10} y1={y + 1} x2={x + 10} y2={y + 1} stroke={ink} strokeWidth={4.5} strokeLinecap="round" />
    </g>
  );

  let eyeEls: React.ReactNode[] = [];
  let mouthEl: React.ReactNode = null;

  switch (expr) {
    case 'happy':
      eyeEls = eyes.map(([x, y], i) => (
        <path key={i} d={`M ${x - 8} ${y + 3} Q ${x} ${y - 10} ${x + 8} ${y + 3}`} stroke={ink} strokeWidth={sw} fill="none" strokeLinecap="round" />
      ));
      mouthEl = <path d={`M ${mx - 15} 18 Q ${mx} 42 ${mx + 17} 18 Z`} fill={ink} strokeLinejoin="round" stroke={ink} strokeWidth={3} />;
      break;
    case 'excited':
      eyeEls = eyes.map(([x, y], i) => (
        <g key={i}>
          {dot(x, y, 8, 11, `d${i}`)}
          {blink > 0.5 ? <circle cx={x + lx + 2.5} cy={y + ly - 4} r={2.6} fill={C.white} /> : null}
        </g>
      ));
      mouthEl = <path d={`M ${mx - 17} 16 Q ${mx} 48 ${mx + 19} 16 Z`} fill={ink} stroke={ink} strokeWidth={3} strokeLinejoin="round" />;
      break;
    case 'shocked':
      eyeEls = eyes.map(([x, y], i) => ring(x, y - 2, 12, 4.5, `r${i}`));
      mouthEl = <ellipse cx={mx} cy={31} rx={8} ry={11} fill={ink} />;
      break;
    case 'mindblown':
      eyeEls = eyes.map(([x, y], i) => ring(x, y - 3, 15.5, 3.5, `r${i}`));
      mouthEl = <ellipse cx={mx} cy={33} rx={12} ry={16} fill={ink} />;
      break;
    case 'smug':
      eyeEls = eyes.map(([x, y], i) => lid(x, y, `l${i}`));
      mouthEl = <path d={`M ${mx - 11} 25 Q ${mx + 3} 28 ${mx + 15} 16`} stroke={ink} strokeWidth={sw} fill="none" strokeLinecap="round" />;
      break;
    case 'confused':
      eyeEls = [dot(eyes[0][0], eyes[0][1], 6.5, 9.5, 'a'), dot(eyes[1][0], eyes[1][1] - 2, 5, 7, 'b')];
      mouthEl = <path d={`M ${mx - 13} 25 Q ${mx - 6} 19 ${mx} 25 Q ${mx + 6} 31 ${mx + 13} 25`} stroke={ink} strokeWidth={sw} fill="none" strokeLinecap="round" />;
      break;
    case 'scared':
      eyeEls = eyes.map(([x, y], i) => ring(x, y - 1, 11, 2.6, `r${i}`));
      mouthEl = <path d={`M ${mx - 14} 28 Q ${mx - 7} 22 ${mx} 28 Q ${mx + 7} 34 ${mx + 14} 28`} stroke={ink} strokeWidth={sw} fill="none" strokeLinecap="round" />;
      break;
    case 'angry':
      eyeEls = eyes.map(([x, y], i) => dot(x, y + 1, 6, 7, `d${i}`));
      mouthEl = <path d={`M ${mx - 11} 30 Q ${mx} 20 ${mx + 11} 30`} stroke={ink} strokeWidth={sw} fill="none" strokeLinecap="round" />;
      break;
    case 'sleepy':
      eyeEls = eyes.map(([x, y], i) => (
        <path key={i} d={`M ${x - 8} ${y + 1} Q ${x} ${y + 7} ${x + 8} ${y + 1}`} stroke={ink} strokeWidth={sw} fill="none" strokeLinecap="round" />
      ));
      mouthEl = <ellipse cx={mx} cy={27} rx={4.5} ry={5.5} fill="none" stroke={ink} strokeWidth={4} />;
      break;
    case 'determined':
      eyeEls = eyes.map(([x, y], i) => dot(x, y, 6.5, 8.5, `d${i}`));
      mouthEl = <path d={`M ${mx - 11} 25 L ${mx + 11} 25`} stroke={ink} strokeWidth={sw} strokeLinecap="round" />;
      break;
    case 'deadpan':
      eyeEls = eyes.map(([x, y], i) => lid(x, y, `l${i}`));
      mouthEl = <path d={`M ${mx - 8} 25 L ${mx + 8} 25`} stroke={ink} strokeWidth={sw} strokeLinecap="round" />;
      break;
    case 'neutral':
    default:
      eyeEls = eyes.map(([x, y], i) => dot(x, y, 6.5, 9.5, `d${i}`));
      mouthEl = <path d={`M ${mx - 11} 22 Q ${mx} 29 ${mx + 11} 22`} stroke={ink} strokeWidth={sw} fill="none" strokeLinecap="round" />;
  }

  if (mouth > 0.02 && TALKS.includes(expr)) {
    const wide = expr === 'happy' || expr === 'excited' ? 12 : 9;
    mouthEl = <ellipse cx={mx} cy={26} rx={wide} ry={2.5 + 11 * mouth} fill={ink} />;
  }

  const browY = spec.glasses ? ey - 25 : ey - 19;
  const b = BROWS[expr];
  const brows = spec.brows ? (
    <g stroke={ink} strokeWidth={4.5} strokeLinecap="round">
      <line x1={eyes[0][0] - 8} y1={browY + b.l[0]} x2={eyes[0][0] + 8} y2={browY + b.l[1]} />
      <line x1={eyes[1][0] - 8} y1={browY + b.r[1]} x2={eyes[1][0] + 8} y2={browY + b.r[0]} />
    </g>
  ) : null;

  const glasses = spec.glasses ? (
    <g fill="none" stroke={ink} strokeWidth={4.5} strokeLinecap="round">
      <path d={`M ${eyes[0][0] + 16} ${ey - 3} Q ${cx} ${ey - 9} ${eyes[1][0] - 16} ${ey - 3}`} />
      <path d={`M ${eyes[0][0] - 16} ${ey - 4} L ${eyes[0][0] - 36} ${ey - 8}`} />
    </g>
  ) : null;

  return (
    <g>
      {spec.glasses
        ? eyes.map(([x, y], i) => <circle key={`lens${i}`} cx={x} cy={y - 2} r={16} fill={C.white} stroke={ink} strokeWidth={4.5} />)
        : null}
      {eyeEls}
      {glasses}
      {brows}
      {mouthEl}
      {expr === 'scared' ? (
        <path d="M 52 -30 Q 60 -16 52 -10 Q 44 -16 52 -30 Z" fill={C.sky} stroke={ink} strokeWidth={3} strokeLinejoin="round" />
      ) : null}
    </g>
  );
};
