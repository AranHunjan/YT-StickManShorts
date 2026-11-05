import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, FONT} from '../style/theme';

export type Word = {t: string; hi?: boolean; color?: string};

/** Parse "Named after *fixing mistakes.*" -> words; everything between stars gets
 * the highlighter (single words or multi-word spans). */
export const words = (s: string): Word[] => {
  const out: Word[] = [];
  let on = false;
  for (const raw of s.split(' ')) {
    let t = raw;
    let hi = on;
    if (t.startsWith('*')) {
      t = t.slice(1);
      hi = true;
      on = true;
    }
    if (t.endsWith('*')) {
      t = t.slice(0, -1);
      on = false;
    }
    out.push({t, hi});
  }
  return out;
};

type Props = {
  text: string;
  from: number; // start frame (absolute)
  to: number; // end frame (absolute)
  y: number; // vertical centre in px
  size?: number;
  maxWidth?: number;
};

/** Big caption that pops in, with a yellow highlighter swipe behind key words. */
export const Caption: React.FC<Props> = ({text, from, to, y, size = 86, maxWidth = 860}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (frame < from || frame > to) return null;
  const local = frame - from;
  const pop = spring({frame: local, fps, config: {damping: 11, stiffness: 220, mass: 0.6}});
  const out = interpolate(frame, [to - 4, to], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const list = words(text);

  return (
    <div
      style={{
        position: 'absolute',
        left: '50%',
        top: y,
        transform: `translate(-50%, -50%) scale(${0.6 + 0.4 * pop})`,
        opacity: Math.min(pop * 1.4, 1) * out,
        width: maxWidth,
        textAlign: 'center',
        fontFamily: FONT,
        fontWeight: 800,
        fontSize: size,
        lineHeight: 1.12,
        letterSpacing: -1,
        color: C.ink,
      }}
    >
      {list.map((w, i) => {
        const swipe = interpolate(local, [3 + i * 0.6, 8 + i * 0.6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return (
          <span key={i} style={{position: 'relative', display: 'inline-block', margin: '0 0.14em'}}>
            {w.hi ? (
              <span
                style={{
                  position: 'absolute',
                  left: '-0.12em',
                  right: '-0.12em',
                  top: '0.16em',
                  bottom: '0.06em',
                  background: C.hi,
                  borderRadius: '0.18em',
                  transform: `skewX(-8deg) scaleX(${swipe})`,
                  transformOrigin: 'left center',
                  zIndex: 0,
                }}
              />
            ) : null}
            <span style={{position: 'relative', zIndex: 1, color: w.color ?? C.ink}}>{w.t}</span>
          </span>
        );
      })}
    </div>
  );
};
