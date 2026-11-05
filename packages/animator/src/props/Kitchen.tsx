import React from 'react';
import {C, FONT} from '../style/theme';

// Generic kitchen props (no real brand logos or label designs).
const O = {stroke: C.ink, strokeWidth: 7, strokeLinejoin: 'round' as const, strokeLinecap: 'round' as const};
const KETCHUP = '#D7262E';
const GLASS = '#F7EFEA';

/** Glass ketchup bottle, upright, centred at its middle. `tap` 0..1 flashes the neck. */
export const KetchupBottle: React.FC<{big57?: boolean; tap?: number}> = ({big57 = false, tap = 0}) => (
  <g>
    {/* body + neck silhouette */}
    <path
      d="M -26 -190 L 26 -190 L 26 -150 C 26 -110, 34 -90, 52 -60 C 70 -30, 74 0, 74 40 L 74 150 C 74 170, 60 182, 40 182 L -40 182 C -60 182, -74 170, -74 150 L -74 40 C -74 0, -70 -30, -52 -60 C -34 -90, -26 -110, -26 -150 Z"
      fill={GLASS}
      {...O}
    />
    {/* ketchup inside */}
    <path
      d="M -20 -130 L 20 -130 C 22 -100, 30 -84, 46 -56 C 62 -28, 66 0, 66 40 L 66 148 C 66 164, 56 174, 40 174 L -40 174 C -56 174, -66 164, -66 148 L -66 40 C -66 0, -62 -28, -46 -56 C -30 -84, -22 -100, -20 -130 Z"
      fill={KETCHUP}
    />
    {/* cap */}
    <rect x={-32} y={-224} width={64} height={40} rx={8} fill={C.white} {...O} />
    {/* neck band with 57 */}
    <g transform={`translate(0 -112) scale(${1 + 0.15 * tap})`}>
      <path d="M -30 -20 L 30 -20 L 36 20 L -36 20 Z" fill={C.white} {...O} strokeWidth={5} />
      <text x={0} y={13} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize={big57 ? 34 : 28} fill={KETCHUP}>
        57
      </text>
    </g>
    {/* body label */}
    <rect x={-60} y={10} width={120} height={84} rx={10} fill={C.white} {...O} strokeWidth={5} />
    <text x={0} y={60} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize={26} fill={C.ink}>
      KETCHUP
    </text>
    {/* glass shine */}
    <path d="M 40 -40 C 56 -10, 60 20, 58 60" fill="none" stroke={C.white} strokeWidth={8} strokeLinecap="round" opacity={0.7} />
  </g>
);

export const Tomato: React.FC<{squish?: number}> = ({squish = 0}) => (
  <g transform={`scale(${1 + 0.35 * squish} ${1 - 0.45 * squish})`}>
    <ellipse rx={46} ry={40} fill={KETCHUP} {...O} />
    <path d="M -18 -40 L 0 -30 L 18 -40 L 8 -26 L 20 -18 L 0 -22 L -20 -18 L -8 -26 Z" fill={C.leaf} {...O} strokeWidth={4} />
    <path d="M -24 -12 C -18 -22, -6 -26, 4 -24" fill="none" stroke={C.white} strokeWidth={6} strokeLinecap="round" opacity={0.6} />
  </g>
);

/** Row of tomatoes with a "x57" label; `squish` 0..1 flattens them. */
export const TomatoPile: React.FC<{squish: number}> = ({squish}) => (
  <g>
    {[-150, -75, 0, 75, 150].map((x, i) => (
      <g key={i} transform={`translate(${x} ${i % 2 ? -18 : 0})`}>
        <Tomato squish={squish} />
      </g>
    ))}
    <text x={0} y={110} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize={56} fill={C.ink}>
      ×57
    </text>
  </g>
);

/** Rubber-stamp label sized to its text. */
export const Stamp: React.FC<{text: string; color?: string}> = ({text, color = C.red}) => {
  const w = 60 + text.length * 56;
  return (
    <g transform="rotate(-9)">
      <rect x={-w / 2} y={-62} width={w} height={124} rx={16} fill="none" stroke={color} strokeWidth={10} />
      <text x={0} y={32} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize={88} fill={color}>
        {text}
      </text>
    </g>
  );
};

/** An 1890s-style train ad card. */
export const TrainAd: React.FC = () => (
  <g>
    <rect x={-250} y={-150} width={500} height={300} rx={14} fill="#E9DDC4" {...O} />
    <rect x={-226} y={-126} width={452} height={252} rx={6} fill="none" stroke={C.ink} strokeWidth={4} />
    <text x={0} y={-50} textAnchor="middle" fontFamily="Georgia, serif" fontWeight={700} fontSize={84} fill={C.ink}>
      21 STYLES
    </text>
    <text x={0} y={6} textAnchor="middle" fontFamily="Georgia, serif" fontStyle="italic" fontSize={44} fill={C.ink}>
      of Shoes
    </text>
    {/* shoe icon */}
    <path d="M -70 90 L -70 40 L -30 40 C -20 60, 10 64, 40 66 C 70 68, 80 80, 80 90 Z" fill={C.ink} />
  </g>
);

/** Ribbon banner. */
export const Banner: React.FC<{text: string}> = ({text}) => {
  const w = 120 + text.length * 40;
  return (
    <g>
      <path d={`M ${-w / 2 - 60} -30 L ${-w / 2} -30 L ${-w / 2} 40 L ${-w / 2 - 60} 40 L ${-w / 2 - 36} 5 Z`} fill="#A81E24" {...O} />
      <path d={`M ${w / 2 + 60} -30 L ${w / 2} -30 L ${w / 2} 40 L ${w / 2 + 60} 40 L ${w / 2 + 36} 5 Z`} fill="#A81E24" {...O} />
      <rect x={-w / 2} y={-50} width={w} height={80} rx={6} fill={KETCHUP} {...O} />
      <text x={0} y={8} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize={52} fill={C.white} letterSpacing={2}>
        {text}
      </text>
    </g>
  );
};

/** Shelf of products with a big "60+" tag. `fill` 0..1 reveals items one by one. */
export const ProductShelf: React.FC<{fill: number}> = ({fill}) => {
  const items = 15;
  const shown = Math.round(items * fill);
  const colors = [KETCHUP, C.leaf, C.hi, C.kip, C.sky];
  return (
    <g>
      {[0, 1, 2].map((r) => (
        <line key={r} x1={-260} y1={-70 + r * 90} x2={260} y2={-70 + r * 90} stroke={C.ink} strokeWidth={8} strokeLinecap="round" />
      ))}
      {Array.from({length: items}).map((_, i) => {
        if (i >= shown) return null;
        const r = Math.floor(i / 5);
        const c = i % 5;
        const x = -200 + c * 100;
        const y = -70 + r * 90;
        return i % 2 ? (
          <rect key={i} x={x - 22} y={y - 62} width={44} height={62} rx={8} fill={colors[(i + r) % 5]} {...O} strokeWidth={5} />
        ) : (
          <path key={i} d={`M ${x - 18} ${y} L ${x - 18} ${y - 40} C ${x - 18} ${y - 56}, ${x - 8} ${y - 60}, ${x - 8} ${y - 70} L ${x + 8} ${y - 70} C ${x + 8} ${y - 60}, ${x + 18} ${y - 56}, ${x + 18} ${y - 40} L ${x + 18} ${y} Z`} fill={colors[(i + r + 2) % 5]} {...O} strokeWidth={5} />
        );
      })}
      <g transform="translate(250 -150) rotate(10)">
        <circle r={70} fill={C.hi} {...O} />
        <text x={0} y={20} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize={60} fill={C.ink}>
          60+
        </text>
      </g>
    </g>
  );
};

export const QuestionMark: React.FC = () => (
  <text x={0} y={70} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize={220} fill={C.hi} stroke={C.ink} strokeWidth={8} paintOrder="stroke">
    ?
  </text>
);

/** Tilted bottle with a tap at the neck; `tap` 0..1 impact, `pour` 0..1 ketchup out. */
export const BottleTap: React.FC<{tap: number; pour: number}> = ({tap, pour}) => (
  <g>
    <g transform="rotate(-50)">
      <KetchupBottle tap={Math.sin(Math.PI * tap)} big57 />
    </g>
    {/* impact lines at the neck */}
    {tap > 0 && tap < 1
      ? [0, 1, 2, 3, 4].map((i) => {
          const a = (-150 + i * 30) * (Math.PI / 180);
          const cx = -86;
          const cy = -72;
          return <line key={i} x1={cx + Math.cos(a) * 46} y1={cy + Math.sin(a) * 46} x2={cx + Math.cos(a) * 80} y2={cy + Math.sin(a) * 80} stroke={C.ink} strokeWidth={7} strokeLinecap="round" />;
        })
      : null}
    {tap > 0 ? (
      <text x={-150} y={-150} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize={64} fill={C.red} opacity={Math.min(1, tap * 3)}>
        TAP!
      </text>
    ) : null}
    {/* ketchup coming out of the mouth */}
    {pour > 0 ? (
      <path
        d={`M -150 -150 C -170 ${-110 + 60 * pour}, -190 ${-60 + 120 * pour}, -200 ${-20 + 170 * pour}`}
        fill="none"
        stroke="#D7262E"
        strokeWidth={26}
        strokeLinecap="round"
      />
    ) : null}
  </g>
);
