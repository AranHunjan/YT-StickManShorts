import React from 'react';
import {C, FONT} from '../style/theme';

// Flat props in the house style: ink outlines, palette fills, no gradients.
// Each prop is drawn centred on (0,0); place it with <g transform>.
const O = {stroke: C.ink, strokeWidth: 7, strokeLinejoin: 'round' as const, strokeLinecap: 'round' as const};
const BREAD = '#F3D9A4';
const CRUST = '#C98A4B';
const WOOD = '#E8C9A0';
const PENCIL = '#F2C230';
const RUBBER = '#B5835A';

/** Pre-1770 pencil: no eraser on the end yet. Points right. */
export const Pencil: React.FC = () => (
  <g>
    <rect x={-150} y={-22} width={230} height={44} rx={6} fill={PENCIL} {...O} />
    <line x1={-150} y1={0} x2={80} y2={0} stroke={C.ink} strokeWidth={3} opacity={0.35} />
    <path d="M 80 -22 L 150 0 L 80 22 Z" fill={WOOD} {...O} />
    <path d="M 126 -7 L 150 0 L 126 7 Z" fill={C.ink} />
  </g>
);

/** Sheet of paper with a pencil scribble; `erased` 0..1 wipes it left to right. */
export const Paper: React.FC<{scribble: number; erased: number; id: string}> = ({scribble, erased, id}) => {
  const d = 'M -120 -20 C -90 -70, -60 30, -30 -30 S 30 40, 60 -20 S 110 30, 125 -35';
  const len = 520;
  return (
    <g>
      <defs>
        <clipPath id={`erase-${id}`}>
          <rect x={-160 + 320 * erased} y={-120} width={340} height={240} />
        </clipPath>
      </defs>
      <rect x={-170} y={-120} width={340} height={240} rx={10} fill={C.white} {...O} />
      {[-60, -10, 40, 90].map((y) => (
        <line key={y} x1={-150} y1={y} x2={150} y2={y} stroke={C.grid} strokeWidth={3} />
      ))}
      <path
        d={d}
        clipPath={`url(#erase-${id})`}
        fill="none"
        stroke="#4A4A55"
        strokeWidth={9}
        strokeLinecap="round"
        strokeDasharray={len}
        strokeDashoffset={len * (1 - scribble)}
      />
    </g>
  );
};

export const BreadSlice: React.FC = () => (
  <g>
    <path d="M -80 90 L -80 -10 C -115 -20, -110 -95, -40 -95 C -20 -125, 20 -125, 40 -95 C 110 -95, 115 -20, 80 -10 L 80 90 Z" fill={CRUST} {...O} />
    <path d="M -62 72 L -62 -18 C -88 -28, -86 -78, -34 -78 C -16 -102, 16 -102, 34 -78 C 86 -78, 88 -28, 62 -18 L 62 72 Z" fill={BREAD} stroke="none" />
    {[[-25, -30], [20, 10], [-10, 40], [30, -45]].map(([x, y], i) => (
      <ellipse key={i} cx={x} cy={y} rx={5} ry={3} fill={CRUST} opacity={0.6} />
    ))}
  </g>
);

export const CrumbBall: React.FC = () => (
  <g>
    <path d="M -34 0 C -36 -24, -14 -38, 4 -34 C 28 -32, 38 -12, 34 6 C 32 28, 10 38, -8 34 C -28 32, -34 18, -34 0 Z" fill={BREAD} {...O} />
    <circle cx={-8} cy={-10} r={4} fill={CRUST} opacity={0.6} />
    <circle cx={12} cy={8} r={3} fill={CRUST} opacity={0.6} />
  </g>
);

export const Sandwich: React.FC = () => (
  <g>
    <rect x={-120} y={8} width={240} height={46} rx={20} fill={BREAD} {...O} />
    <path d="M -128 2 Q -100 -18 -70 2 Q -40 -18 -10 2 Q 20 -18 50 2 Q 80 -18 110 2 L 128 2" fill="none" stroke={C.leaf} strokeWidth={16} strokeLinecap="round" />
    <rect x={-105} y={-14} width={210} height={16} rx={8} fill={C.red} {...O} strokeWidth={5} />
    <path d="M -120 -16 C -120 -70, 120 -70, 120 -16 Z" fill={BREAD} {...O} />
    <path d="M -100 -28 C -96 -60, 96 -60, 100 -28" fill="none" stroke={CRUST} strokeWidth={10} strokeLinecap="round" />
  </g>
);

/** Aged note with Priestley's 1770 footnote, abbreviated. */
export const PriestleyNote: React.FC = () => (
  <g transform="rotate(-4)">
    <path d="M -170 -110 L 170 -110 L 170 110 L -170 110 Z" fill="#EBD9B4" {...O} />
    <text x={0} y={-62} textAnchor="middle" fontFamily="Georgia, serif" fontStyle="italic" fontSize={30} fill={C.ink}>
      &ldquo;...wiping from paper
    </text>
    <text x={0} y={-22} textAnchor="middle" fontFamily="Georgia, serif" fontStyle="italic" fontSize={30} fill={C.ink}>
      the mark of black-lead
    </text>
    <text x={0} y={18} textAnchor="middle" fontFamily="Georgia, serif" fontStyle="italic" fontSize={30} fill={C.ink}>
      pencil.&rdquo;
    </text>
    <text x={110} y={78} textAnchor="end" fontFamily={FONT} fontWeight={800} fontSize={26} fill={C.ink} opacity={0.75}>
      J. Priestley, 1770
    </text>
  </g>
);

/** The new stuff: a stretchy tree gum. `stretch` 0..1 pulls it wide. */
export const GumBlob: React.FC<{stretch: number}> = ({stretch}) => (
  <g transform={`scale(${1 + 0.5 * stretch} ${1 - 0.25 * stretch})`}>
    <path d="M -70 10 C -80 -40, -30 -60, 0 -50 C 40 -62, 82 -36, 72 6 C 80 46, 30 60, 0 52 C -40 62, -64 44, -70 10 Z" fill={RUBBER} {...O} />
    <path d="M -36 -26 C -20 -36, 10 -38, 26 -30" fill="none" stroke={C.white} strokeWidth={8} strokeLinecap="round" opacity={0.6} />
  </g>
);

/** A little rubber cube, as Nairne sold them. */
export const RubberCube: React.FC = () => (
  <g>
    <path d="M -50 -20 L 0 -46 L 50 -20 L 0 6 Z" fill="#C99A72" {...O} />
    <path d="M -50 -20 L 0 6 L 0 60 L -50 34 Z" fill={RUBBER} {...O} />
    <path d="M 50 -20 L 0 6 L 0 60 L 50 34 Z" fill="#9C6E4A" {...O} />
  </g>
);

export const Tire: React.FC = () => (
  <g>
    <circle r={78} fill={C.ink} />
    {Array.from({length: 16}).map((_, i) => {
      const a = (i / 16) * Math.PI * 2;
      return <line key={i} x1={Math.cos(a) * 66} y1={Math.sin(a) * 66} x2={Math.cos(a) * 80} y2={Math.sin(a) * 80} stroke="#444" strokeWidth={8} />;
    })}
    <circle r={40} fill="#B8BCC4" {...O} strokeWidth={6} />
    <circle r={12} fill={C.ink} />
  </g>
);

export const RubberBand: React.FC = () => (
  <g>
    <ellipse rx={70} ry={42} fill="none" stroke={C.ink} strokeWidth={22} />
    <ellipse rx={70} ry={42} fill="none" stroke={C.red} strokeWidth={12} />
  </g>
);

export const RubberDuck: React.FC = () => (
  <g>
    <path d="M -75 10 C -80 60, 60 70, 80 20 C 90 -5, 60 -10, 40 0 C 20 -20, -60 -30, -75 10 Z" fill={C.hi} {...O} />
    <circle cx={30} cy={-38} r={36} fill={C.hi} {...O} />
    <path d="M 60 -40 L 92 -32 L 62 -22 Z" fill={C.kip} {...O} strokeWidth={5} />
    <circle cx={38} cy={-46} r={6} fill={C.ink} />
    <path d="M -40 16 C -20 30, 10 30, 24 16" fill="none" stroke={C.ink} strokeWidth={5} strokeLinecap="round" opacity={0.5} />
  </g>
);

/** Label that "types" a word; `typed` 0..1, with the first `hi` letters highlighted. */
export const NameTag: React.FC<{word: string; typed: number; hi?: number}> = ({word, typed, hi = 0}) => {
  const n = Math.round(word.length * typed);
  const shown = word.slice(0, n);
  return (
    <g>
      <rect x={-230} y={-80} width={460} height={160} rx={18} fill={C.white} {...O} />
      <rect x={-230} y={-80} width={460} height={44} rx={18} fill={C.dex} {...O} />
      <text x={0} y={-48} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize={28} fill={C.white}>
        HELLO, MY NAME IS
      </text>
      <text x={0} y={52} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize={72} fill={C.ink} letterSpacing={4}>
        <tspan fill={C.red}>{shown.slice(0, hi)}</tspan>
        {shown.slice(hi)}
        {n < word.length ? '_' : ''}
      </text>
    </g>
  );
};

/** Big date that drops in like a rubber stamp. */
export const DateStamp: React.FC<{text: string}> = ({text}) => (
  <g transform="rotate(-8)">
    <rect x={-150} y={-62} width={300} height={124} rx={16} fill="none" stroke={C.red} strokeWidth={10} />
    <text x={0} y={34} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize={96} fill={C.red}>
      {text}
    </text>
  </g>
);
