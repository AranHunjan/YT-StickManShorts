import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {addPose, blink, idle, sample, talk, type Key} from '../rig/animate';
import {DEX, KIP} from '../rig/characters';
import {POSES, STAND} from '../rig/poses';
import {Stickman} from '../rig/Stickman';
import type {Expression, Pose} from '../rig/types';
import {BottleTap, Banner, KetchupBottle, ProductShelf, QuestionMark, Stamp, TomatoPile, TrainAd} from '../props/Kitchen';
import {BreadSlice, CrumbBall, DateStamp, GumBlob, NameTag, Paper, Pencil, PriestleyNote, RubberBand, RubberCube, RubberDuck, Sandwich, Tire} from '../props/Props';
import {Caption} from '../scene/Caption';
import {WordCaptions, type TimedWord} from '../scene/WordCaptions';
import {Burst, IndexCard} from '../scene/Effects';
import {Paper as NotebookPaper} from '../scene/Paper';
import {Watermark} from '../scene/Watermark';
import {C, H, W} from '../style/theme';

export type Timing = {duration: number; lines: {id: string; speaker: string; delivery: string; start: number; end: number; text: string; caption?: string; words?: TimedWord[]}[]};
type PoseRef = [string, string];
export type Beats = {
  lines: Record<string, {kip: PoseRef; dex: PoseRef}>;
  props: Record<string, unknown>[];
  burst?: string;
  kipHold?: Record<string, [string, string]>;
  dexCard?: {lines: string[]; in: string; out: string};
  sfx: [string, string, number][];
};

const GROUND = 1440;
const KIP_X = 350;
const DEX_X = 730;
const CHAR_SCALE = 1.2;
const TAIL = 0.9; // seconds held after the last line
const PROP_SCALE = 1.3; // props read bigger on a phone than at design size
const PROP_DY = -48; // keep scaled props clear of the characters' heads

/** Resolve "L05@0.45" (or "END") to seconds using the voice timing. */
export function at(timing: Timing, ref: string): number {
  if (ref === 'END') return timing.duration + TAIL;
  const [id, frac] = ref.split('@');
  const ln = timing.lines.find((l) => l.id === id);
  if (!ln) throw new Error(`unknown line ${id}`);
  return ln.start + (ln.end - ln.start) * Number(frac ?? 0);
}

export const episodeFrames = (timing: Timing, fps: number) => Math.ceil((timing.duration + TAIL) * fps);

const poseOf = (name: string): Partial<Pose> => (POSES as Record<string, Partial<Pose>>)[name] ?? {};

/** Keyframes: hold each line's pose, switching quickly at the line start. */
function track(timing: Timing, beats: Beats, who: 'kip' | 'dex', x: number, fps: number): Key[] {
  const keys: Key[] = [{f: 0, p: {...STAND, x, ...poseOf(beats.lines[timing.lines[0].id][who][0])}, expr: beats.lines[timing.lines[0].id][who][1] as Expression}];
  timing.lines.forEach((ln, i) => {
    if (i === 0) return;
    const [pose, expr] = beats.lines[ln.id][who];
    const prev = beats.lines[timing.lines[i - 1].id][who][0];
    const f = Math.round(ln.start * fps);
    keys.push({f: Math.max(f - 3, 1), p: {...STAND, x, ...poseOf(prev)}});
    keys.push({f: f + 7, p: {...STAND, x, ...poseOf(pose)}, e: 'outBack', expr: expr as Expression});
  });
  return keys;
}

export const Episode: React.FC<{timing: Timing; beats: Beats; episode: number}> = ({timing, beats, episode}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const sec = frame / fps;
  const T = (ref: string) => at(timing, ref);
  const F = (ref: string) => Math.round(T(ref) * fps);
  const cur = [...timing.lines].reverse().find((l) => sec >= l.start - 0.12) ?? timing.lines[0];

  // Characters
  const kipS = sample(STAND, track(timing, beats, 'kip', KIP_X, fps), frame);
  const dexS = sample(STAND, track(timing, beats, 'dex', DEX_X, fps), frame);
  let kp = addPose(kipS.pose, idle(frame, 1));
  let dp = addPose(dexS.pose, idle(frame, 2.5));
  const talking = (who: string) => timing.lines.some((l) => l.speaker === who && sec >= l.start && sec <= l.end);
  if (talking('kip')) kp = {...kp, mouth: talk(frame, 'kip')};
  if (talking('dex')) dp = {...dp, mouth: talk(frame, 'dex') * 0.7};
  const kipPose = beats.lines[cur.id].kip[0];
  if (kipPose === 'think') kp = {...kp, hairQ: 1};
  if (kipPose === 'mindblown') kp = {...kp, hair: 1};

  // Camera: rock steady (no wobble filter, no shake); only a very slow push-in.
  const burstF = beats.burst ? F(beats.burst) : -999;
  const zoom = 1 + interpolate(frame, [0, episodeFrames(timing, fps)], [0, 0.02]);

  // Props
  const props = beats.props.map((p) => {
    const inF = F(p.in as string);
    const outF = F(p.out as string);
    if (frame < inF || frame > outF) return null;
    const pop = spring({frame: frame - inF, fps, config: {damping: 10, stiffness: 180, mass: 0.6}});
    const leave = interpolate(frame, [outF - 5, outF], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    const prog = (key: string) => {
      const r = p[key] as [string, string] | undefined;
      return r ? interpolate(sec, [T(r[0]), T(r[1])], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
    };
    const xs = p.x as number | [number, number];
    const x = Array.isArray(xs) ? xs[0] + (xs[1] - xs[0]) * prog('move') : xs;
    const y = (p.y as number) + PROP_DY;
    const s = PROP_SCALE * ((p.scale as number) ?? 1) * pop * leave;
    const roll = p.roll ? prog('move') * 540 : 0;
    let el: React.ReactNode = null;
    switch (p.kind) {
      case 'paper': el = <Paper id={p.id as string} scribble={prog('scribble')} erased={prog('erase')} />; break;
      case 'bread': el = <BreadSlice />; break;
      case 'crumb': el = <CrumbBall />; break;
      case 'sandwich': el = <Sandwich />; break;
      case 'note': el = <PriestleyNote />; break;
      case 'datestamp': el = <DateStamp text={(p.text as string) ?? '1770'} />; break;
      case 'gum': el = <GumBlob stretch={Math.sin(Math.PI * prog('stretch'))} />; break;
      case 'cube': el = <RubberCube />; break;
      case 'nametag': el = <NameTag word={p.word as string} typed={prog('type')} hi={(p.hi as number) ?? 0} />; break;
      case 'tire': el = <Tire />; break;
      case 'band': el = <RubberBand />; break;
      case 'duck': el = <RubberDuck />; break;
      case 'bottle': el = <KetchupBottle big57={Boolean(p.big57)} />; break;
      case 'tomatoes': el = <TomatoPile squish={Math.sin(Math.PI * 0.5 * prog('squish'))} />; break;
      case 'stamp': el = <Stamp text={p.text as string} color={p.color === 'ink' ? C.ink : C.red} />; break;
      case 'trainad': el = <TrainAd />; break;
      case 'banner': el = <Banner text={p.text as string} />; break;
      case 'shelf': el = <ProductShelf fill={prog('fill')} />; break;
      case 'question': el = <QuestionMark />; break;
      case 'bottletap': el = <BottleTap tap={prog('tap')} pour={prog('pour')} />; break;
    }
    return (
      <g key={p.id as string} transform={`translate(${x} ${y}) rotate(${roll}) scale(${s})`}>
        {el}
      </g>
    );
  });

  const pencil = beats.kipHold?.pencil;
  const pencilOn = pencil && sec >= T(pencil[0]) && sec <= T(pencil[1]);
  const card = beats.dexCard;
  const cardOn = card && sec >= T(card.in) && sec <= T(card.out);
  const kipHead = {x: KIP_X - 30, y: GROUND - 470};

  return (
    <AbsoluteFill style={{backgroundColor: C.paper}}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
        <NotebookPaper w={W} h={H} />
        <g transform={`translate(540 ${GROUND}) scale(${CHAR_SCALE * zoom}) translate(-540 ${-GROUND})`}>
          <ellipse cx={kp.x} cy={GROUND + 10} rx={110} ry={14} fill={C.ink} opacity={0.08} />
          <ellipse cx={dp.x} cy={GROUND + 10} rx={110} ry={14} fill={C.ink} opacity={0.08} />
          {beats.burst ? <Burst x={kipHead.x} y={kipHead.y} frame={frame} from={burstF} fps={fps} r={150} /> : null}
          <g>
            <Stickman spec={DEX} pose={dp} expr={dexS.expr} groundY={GROUND} frame={frame} facing={-1} seed={2} blink={blink(frame, 2)}>
              {(j) => (cardOn && card ? <IndexCard x={j.armF.end.x - 24} y={j.armF.end.y - 62} rot={6} scale={0.8} lines={card.lines} /> : null)}
            </Stickman>
            <Stickman spec={KIP} pose={kp} expr={kipS.expr} groundY={GROUND} frame={frame} seed={1} blink={blink(frame, 1)}>
              {(j) =>
                pencilOn ? (
                  <g transform={`translate(${j.armF.end.x} ${j.armF.end.y}) rotate(${-25 + 6 * Math.sin(frame * 0.5)}) scale(0.55)`}>
                    <Pencil />
                  </g>
                ) : null
              }
            </Stickman>
          </g>
        </g>
        <g>{props}</g>
      </svg>
      <Watermark episode={episode} antiCropY={1495} />
      {timing.lines.some((l) => l.words) ? (
        <WordCaptions words={timing.lines.flatMap((l) => (l.words ?? []).map((w) => ({...w, sp: l.speaker})))} y={372} />
      ) : (
        timing.lines.map((ln, i) => {
          const next = timing.lines[i + 1];
          const from = Math.round(ln.start * fps) - 2;
          const to = next ? Math.round(next.start * fps) - 3 : episodeFrames(timing, fps);
          return <Caption key={ln.id} text={ln.caption ?? ''} from={from} to={to} y={378} size={80} />;
        })
      )}
    </AbsoluteFill>
  );
};
