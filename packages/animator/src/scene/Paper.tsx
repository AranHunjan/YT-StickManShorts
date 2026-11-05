import React from 'react';
import {C} from '../style/theme';

/** Lab-notebook paper: warm paper, faint blue grid, red margin line, light grain. */
export const Paper: React.FC<{w: number; h: number; grid?: number; marginX?: number}> = ({w, h, grid = 54, marginX = 96}) => (
  <g>
    <defs>
      <pattern id="grid" width={grid} height={grid} patternUnits="userSpaceOnUse">
        <path d={`M ${grid} 0 L 0 0 0 ${grid}`} fill="none" stroke={C.grid} strokeWidth={2} />
      </pattern>
      <filter id="grain" x="0" y="0" width="100%" height="100%">
        <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={4} />
        <feColorMatrix type="saturate" values="0" />
        <feComponentTransfer>
          <feFuncA type="table" tableValues="0 0.07" />
        </feComponentTransfer>
      </filter>
      <radialGradient id="vignette" cx="50%" cy="45%" r="75%">
        <stop offset="70%" stopColor="#000" stopOpacity={0} />
        <stop offset="100%" stopColor="#5a4a2a" stopOpacity={0.16} />
      </radialGradient>
    </defs>
    <rect width={w} height={h} fill={C.paper} />
    <rect width={w} height={h} fill="url(#grid)" opacity={0.45} />
    <line x1={marginX} y1={0} x2={marginX} y2={h} stroke={C.margin} strokeWidth={3} opacity={0.7} />
    <rect width={w} height={h} filter="url(#grain)" />
    <rect width={w} height={h} fill="url(#vignette)" />
  </g>
);

/** Hand-drawn "line boil": a subtle wobble that changes every few frames. */
export const BoilDefs: React.FC<{frame: number; every?: number; scale?: number}> = ({frame, every = 4, scale = 2.4}) => (
  <defs>
    <filter id="boil" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves={1} seed={Math.floor(frame / every) % 6} result="n" />
      <feDisplacementMap in="SourceGraphic" in2="n" scale={scale} xChannelSelector="R" yChannelSelector="G" />
    </filter>
  </defs>
);
