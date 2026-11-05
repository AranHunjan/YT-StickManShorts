import React from 'react';
import {interpolate, random, spring} from 'remotion';
import {C, FONT} from '../style/theme';

/** Mind-blown starburst behind a head. */
export const Burst: React.FC<{x: number; y: number; frame: number; from: number; fps: number; r?: number}> = ({x, y, frame, from, fps, r = 190}) => {
  if (frame < from) return null;
  const s = spring({frame: frame - from, fps, config: {damping: 9, stiffness: 160}});
  const fade = interpolate(frame - from, [24, 40], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const n = 14;
  const pts: string[] = [];
  for (let i = 0; i < n * 2; i++) {
    const a = (i / (n * 2)) * Math.PI * 2 + 0.1 * Math.sin(frame * 0.3);
    const rr = (i % 2 === 0 ? r : r * 0.55) * s;
    pts.push(`${(x + Math.cos(a) * rr).toFixed(1)},${(y + Math.sin(a) * rr).toFixed(1)}`);
  }
  return (
    <g opacity={fade}>
      <polygon points={pts.join(' ')} fill={C.hi} stroke={C.ink} strokeWidth={6} strokeLinejoin="round" />
      {Array.from({length: 7}).map((_, i) => {
        const a = random(`sp${i}`) * Math.PI * 2;
        const d = (r * 1.05 + 60 * random(`sd${i}`)) * s;
        return <Sparkle key={i} x={x + Math.cos(a) * d} y={y + Math.sin(a) * d} size={16 + 14 * random(`ss${i}`)} />;
      })}
    </g>
  );
};

export const Sparkle: React.FC<{x: number; y: number; size: number; color?: string}> = ({x, y, size, color = C.kip}) => (
  <path
    d={`M ${x} ${y - size} Q ${x} ${y} ${x + size} ${y} Q ${x} ${y} ${x} ${y + size} Q ${x} ${y} ${x - size} ${y} Q ${x} ${y} ${x} ${y - size} Z`}
    fill={color}
    stroke={C.ink}
    strokeWidth={3}
    strokeLinejoin="round"
  />
);

/** Dex's source card. Drawn in world space, upright. */
export const IndexCard: React.FC<{x: number; y: number; rot?: number; scale?: number; lines: string[]}> = ({x, y, rot = -6, scale = 1, lines}) => (
  <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${scale})`}>
    <rect x={-120} y={-80} width={240} height={160} rx={10} fill={C.white} stroke={C.ink} strokeWidth={6} />
    <line x1={-120} y1={-38} x2={120} y2={-38} stroke={C.dex} strokeWidth={6} />
    {[0, 1].map((i) => (
      <line key={i} x1={-104} y1={6 + i * 34} x2={104} y2={6 + i * 34} stroke={C.grid} strokeWidth={3} />
    ))}
    {lines.map((t, i) => (
      <text
        key={i}
        x={0}
        y={i === 0 ? -50 : -4 + i * 34}
        textAnchor="middle"
        fontFamily={FONT}
        fontWeight={800}
        fontSize={i === 0 ? 30 : 28}
        fill={i === 0 ? C.dex : C.ink}
      >
        {t}
      </text>
    ))}
  </g>
);

/** Red overlay marking where the YouTube Shorts UI covers the frame (review only). */
export const SafeZones: React.FC<{w: number; h: number}> = ({w, h}) => (
  <g fill={C.red} opacity={0.18}>
    <rect x={0} y={0} width={w} height={140} />
    <rect x={0} y={h * 0.8} width={w} height={h * 0.2} />
    <rect x={w * 0.85} y={h * 0.45} width={w * 0.15} height={h * 0.35} />
  </g>
);
