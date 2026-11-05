import React from 'react';
import {AbsoluteFill} from 'remotion';
import {DEX, KIP} from '../rig/characters';
import {Face} from '../rig/Face';
import {pose, type PoseName} from '../rig/poses';
import {Stickman} from '../rig/Stickman';
import {EXPRESSIONS, type CharacterSpec, type Expression, type Pose} from '../rig/types';
import {IndexCard} from '../scene/Effects';
import {Paper} from '../scene/Paper';
import {C, FONT} from '../style/theme';

const SW = 1920;
const SH = 1080;

const Label: React.FC<{x: number; y: number; size?: number; color?: string; anchor?: 'start' | 'middle' | 'end'; weight?: number; children: React.ReactNode}> = ({
  x, y, size = 24, color = C.ink, anchor = 'middle', weight = 600, children,
}) => (
  <text x={x} y={y} fontFamily={FONT} fontWeight={weight} fontSize={size} fill={color} textAnchor={anchor}>
    {children}
  </text>
);

/** A character drawn small at (cx, groundY) with a uniform scale. */
const Mini: React.FC<{spec: CharacterSpec; p: Pose; expr: Expression; cx: number; gy: number; s: number; facing?: 1 | -1; card?: boolean}> = ({
  spec, p, expr, cx, gy, s, facing = 1, card,
}) => (
  <g transform={`translate(${cx} ${gy}) scale(${s}) translate(-540 0)`}>
    <Stickman spec={spec} pose={{...p, x: 540}} expr={expr} groundY={0} frame={0} facing={facing}>
      {card ? (j) => <IndexCard x={j.armF.end.x + facing * 30} y={j.armF.end.y - 70} lines={['SOURCES: 2', 'always', 'checked']} /> : undefined}
    </Stickman>
  </g>
);

export const CharacterSheet: React.FC = () => {
  const ground = 900;
  return (
    <AbsoluteFill>
      <svg width={SW} height={SH} viewBox={`0 0 ${SW} ${SH}`}>
        <Paper w={SW} h={SH} marginX={70} />

        <Label x={110} y={118} size={78} anchor="start" weight={800}>KIP & DEX</Label>
        <Label x={112} y={162} size={28} anchor="start">Character sheet v1 · working title: Stick to the Facts</Label>

        {/* Hero figures */}
        <Mini spec={KIP} p={pose('stand', {head: 4})} expr="happy" cx={330} gy={ground} s={1} />
        <Mini spec={DEX} p={pose('holdCard')} expr="deadpan" cx={730} gy={ground} s={1} facing={-1} card />
        <Label x={330} y={ground + 52} size={34} weight={800} color={C.kip}>KIP</Label>
        <Label x={330} y={ground + 84} size={21}>curious, impulsive,</Label>
        <Label x={330} y={ground + 110} size={21}>gets mind-blown</Label>
        <Label x={730} y={ground + 52} size={34} weight={800} color={C.dex}>DEX</Label>
        <Label x={730} y={ground + 84} size={21}>deadpan expert,</Label>
        <Label x={730} y={ground + 110} size={21}>brings the receipts</Label>

        {/* Callouts */}
        <g stroke={C.ink} strokeWidth={3} fill="none" strokeDasharray="8 7">
          <path d="M 190 262 Q 250 300 300 372" />
          <path d="M 205 640 Q 250 610 290 572" />
        </g>
        <Label x={110} y={250} size={22} anchor="start" weight={800}>cowlick = emotion meter</Label>
        <Label x={100} y={668} size={22} anchor="start" weight={800}>orange scarf</Label>
        <Label x={100} y={696} size={22} anchor="start" weight={800}>= brand colour</Label>

        {/* Poses */}
        <Label x={960} y={225} size={30} anchor="start" weight={800}>POSES</Label>
        {(
          [
            ['wave', 'happy', KIP],
            ['point', 'excited', KIP],
            ['think', 'confused', KIP],
            ['mindblown', 'mindblown', KIP],
            ['sad', 'sleepy', KIP],
            ['adjustGlasses', 'smug', DEX],
          ] as [PoseName, Expression, CharacterSpec][]
        ).map(([pn, ex, spec], i) => (
          <g key={pn}>
            <Mini spec={spec} p={pose(pn)} expr={ex} cx={1020 + i * 150} gy={548} s={0.52} />
            <Label x={1020 + i * 150} y={590} size={20}>{pn}</Label>
          </g>
        ))}

        {/* Expressions */}
        <Label x={960} y={660} size={30} anchor="start" weight={800}>EXPRESSIONS</Label>
        {EXPRESSIONS.map((ex, i) => {
          const col = i % 6;
          const row = Math.floor(i / 6);
          const x = 1020 + col * 150;
          const y = 760 + row * 190;
          return (
            <g key={ex}>
              <g transform={`translate(${x} ${y}) scale(0.62)`}>
                <g transform={`scale(${KIP.headR / 60})`}>
                  <circle r={60} fill={C.white} stroke={C.ink} strokeWidth={KIP.stroke / (KIP.headR / 60)} />
                  <Face spec={KIP} expr={ex} mouth={0} lookX={0} lookY={0} blink={1} />
                </g>
              </g>
              <Label x={x} y={y + 76} size={20}>{ex}</Label>
            </g>
          );
        })}

        {/* Palette */}
        {(
          [
            ['paper', C.paper], ['ink', C.ink], ['kip', C.kip], ['dex', C.dex],
            ['highlight', C.hi], ['red', C.red], ['sky', C.sky], ['leaf', C.leaf],
          ] as [string, string][]
        ).map(([n, c], i) => (
          <g key={n} transform={`translate(${1000 + i * 108} 92)`}>
            <rect x={0} y={0} width={86} height={38} rx={8} fill={c} stroke={C.ink} strokeWidth={3} />
            <Label x={43} y={64} size={17}>{c}</Label>
          </g>
        ))}
      </svg>
    </AbsoluteFill>
  );
};
