import React from 'react';
import {AbsoluteFill, interpolate, random, useCurrentFrame, useVideoConfig} from 'remotion';
import {addPose, blink, idle, sample, talk, walk, type Key} from '../rig/animate';
import {DEX, KIP} from '../rig/characters';
import {POSES, STAND} from '../rig/poses';
import {Stickman} from '../rig/Stickman';
import type {Pose} from '../rig/types';
import {Caption} from '../scene/Caption';
import {Burst, IndexCard, SafeZones} from '../scene/Effects';
import {BoilDefs, Paper} from '../scene/Paper';
import {Watermark} from '../scene/Watermark';
import {C, H, W} from '../style/theme';

const GROUND = 1440;
const KIP_X = 390;
const DEX_X = 720;
const CHAR_SCALE = 1.3; // characters are drawn larger on the phone screen, scaled about (540, GROUND)

const P = (name: keyof typeof POSES) => POSES[name] as Partial<Pose>;
const inAny = (f: number, ranges: [number, number][]) => ranges.some(([a, b]) => f >= a && f <= b);

// Kip's keyframes (frames at 30 fps)
const KIP_KEYS: Key[] = [
  {f: 0, p: {...STAND, x: KIP_X}, expr: 'happy'},
  {f: 40, p: {...STAND, x: KIP_X, squash: 0.93}, e: 'out'},
  {f: 48, p: {squash: 1}, e: 'outBack'},
  {f: 56, p: P('wave'), e: 'outBack', expr: 'excited'},
  {f: 92, p: P('wave')},
  {f: 102, p: {...STAND, x: KIP_X, lookX: 1, head: 6}, e: 'inOut', expr: 'happy'},
  {f: 132, p: {lean: 6, lookX: 1, head: 8}, expr: 'neutral'},
  {f: 156, p: {lean: 9, lookX: 1}, expr: 'confused'},
  {f: 161, p: {...STAND, x: KIP_X, ...P('mindblown')}, e: 'snap', expr: 'mindblown'},
  {f: 186, p: {...STAND, x: KIP_X, ...P('mindblown'), lift: 0, legB: [-10, 0], legF: [10, 0]}, e: 'out'},
  {f: 204, p: {...STAND, x: KIP_X, ...P('scratchHead')}, e: 'outBack', expr: 'confused'},
  {f: 236, p: {...STAND, x: KIP_X, ...P('scratchHead')}},
  {f: 244, p: {...STAND, x: KIP_X, ...P('celebrate')}, e: 'outBack', expr: 'excited'},
  {f: 256, p: {lift: 0, legB: [-8, 0], legF: [8, 0]}, e: 'out'},
];

// Dex's keyframes (he enters from the right, facing left)
const DEX_KEYS: Key[] = [
  {f: 0, p: {...STAND, x: 1300}, expr: 'deadpan'},
  {f: 84, p: {x: 1300}},
  {f: 116, p: {...STAND, x: DEX_X, squash: 0.96}, e: 'out'},
  {f: 124, p: {squash: 1}, e: 'outBack'},
  {f: 136, p: {...STAND, x: DEX_X, ...P('holdCard')}, e: 'outBack'},
  {f: 156, p: {...STAND, x: DEX_X, ...P('holdCard')}},
  {f: 166, p: {...STAND, x: DEX_X, lean: -4, head: -4}, e: 'outBack', expr: 'smug'},
  {f: 196, p: {...STAND, x: DEX_X}},
  {f: 206, p: {...STAND, x: DEX_X, ...P('adjustGlasses')}, e: 'outBack', expr: 'smug'},
  {f: 238, p: {...STAND, x: DEX_X, ...P('adjustGlasses')}},
  {f: 246, p: {...STAND, x: DEX_X, ...P('crossArms')}, e: 'outBack', expr: 'smug'},
];

const KIP_TALK: [number, number][] = [[52, 88], [162, 182], [204, 234], [242, 266]];
const DEX_TALK: [number, number][] = [[100, 126], [136, 158]];

export const RigTest: React.FC<{showSafeZones?: boolean}> = ({showSafeZones = false}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // Kip
  let kip = sample(STAND, KIP_KEYS, frame);
  let kp = kip.pose;
  const kw = walk(frame, 0, 40, 150, KIP_X);
  if (kw) kp = {...kp, ...kw};
  kp = addPose(kp, idle(frame, 1));
  if (inAny(frame, KIP_TALK)) kp = {...kp, mouth: talk(frame, 'kip')};
  if (frame >= 161 && frame < 200) kp = {...kp, hair: 1};
  if (frame >= 56 && frame <= 92) kp = addPose(kp, {armF: [0, 24 * Math.sin((frame - 56) * 0.45)]});

  // Dex
  const dex = sample(STAND, DEX_KEYS, frame);
  let dp = dex.pose;
  const dw = walk(frame, 84, 116, 1300, DEX_X, 16);
  if (dw) dp = {...dp, ...dw, wind: 0};
  dp = addPose(dp, idle(frame, 2.5));
  if (inAny(frame, DEX_TALK)) dp = {...dp, mouth: talk(frame, 'dex') * 0.7};

  // Camera: slow push-in, punch-in and shake on the mind-blown beat
  const punch = interpolate(frame, [161, 166, 190], [0, 0.07, 0.02], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const zoom = CHAR_SCALE * (1 + interpolate(frame, [0, 270], [0, 0.04]) + punch);
  const shakeAmt = interpolate(frame, [161, 175], [16, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const sx = shakeAmt * (random(`sx${frame}`) - 0.5) * 2;
  const sy = shakeAmt * (random(`sy${frame}`) - 0.5) * 2;
  const fx = 540;
  const fy = GROUND;

  const kipHead = {x: KIP_X - 30, y: GROUND - 470};

  return (
    <AbsoluteFill style={{backgroundColor: C.paper}}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
        <BoilDefs frame={frame} />
        <Paper w={W} h={H} />
        <g transform={`translate(${sx} ${sy}) translate(${fx} ${fy}) scale(${zoom}) translate(${-fx} ${-fy})`}>
          <ellipse cx={kp.x} cy={GROUND + 10} rx={110} ry={14} fill={C.ink} opacity={0.08} />
          {dp.x < W + 100 ? <ellipse cx={dp.x} cy={GROUND + 10} rx={110} ry={14} fill={C.ink} opacity={0.08} /> : null}
          <Burst x={kipHead.x} y={kipHead.y} frame={frame} from={161} fps={fps} r={150} />
          <g filter="url(#boil)">
            <Stickman spec={DEX} pose={dp} expr={dex.expr} groundY={GROUND} frame={frame} facing={-1} seed={2} blink={blink(frame, 2)}>
              {(j) =>
                frame >= 132 && frame < 160 ? (
                  <IndexCard x={j.armF.end.x - 24} y={j.armF.end.y - 62} rot={6} scale={0.8} lines={['SOURCES: 2', 'always', 'checked']} />
                ) : null
              }
            </Stickman>
            <Stickman spec={KIP} pose={kp} expr={kip.expr} groundY={GROUND} frame={frame} seed={1} blink={blink(frame, 1)} />
          </g>
        </g>
        {showSafeZones ? <SafeZones w={W} h={H} /> : null}
      </svg>

      <Watermark episode={0} />

      <Caption text="Hi! I'm *KIP.*" from={50} to={94} y={540} />
      <Caption text="...and I'm *DEX.*" from={98} to={130} y={540} />
      <Caption text="Every fact? *TWO* sources." from={134} to={159} y={540} />
      <Caption text="EXCUSE *ME?!*" from={161} to={200} y={430} size={120} />
      <Caption text="Wild true stories behind *EVERYDAY* things." from={203} to={239} y={540} />
      <Caption text="A new one *EVERY* day." from={242} to={269} y={540} />
    </AbsoluteFill>
  );
};
