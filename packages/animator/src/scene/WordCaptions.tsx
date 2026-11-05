import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, FONT} from '../style/theme';

export type TimedWord = {w: string; s: number; e: number; hi?: boolean};

/** Group words into short caption chunks (1-3 words), breaking at punctuation and pauses. */
export function chunkWords(words: TimedWord[], maxWords = 3, maxChars = 18): TimedWord[][] {
  const chunks: TimedWord[][] = [];
  let cur: TimedWord[] = [];
  words.forEach((w, i) => {
    const len = cur.reduce((n, x) => n + x.w.length + 1, 0) + w.w.length;
    const prev = words[i - 1];
    const pause = prev ? w.s - prev.e > 0.3 : false;
    if (cur.length && (cur.length >= maxWords || len > maxChars || pause)) {
      chunks.push(cur);
      cur = [];
    }
    cur.push(w);
    if (/[.?!,…]$/.test(w.w)) {
      chunks.push(cur);
      cur = [];
    }
  });
  if (cur.length) chunks.push(cur);
  return chunks;
}

/**
 * Captions that show exactly what is being said, when it is said: one short
 * chunk at a time, the current word emphasised, *starred* keywords highlighted.
 */
export const WordCaptions: React.FC<{words: TimedWord[]; y: number; size?: number}> = ({words, y, size = 96}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const chunks = chunkWords(words);
  const idx = chunks.findIndex((c, i) => {
    const start = c[0].s - 0.05;
    const nextStart = chunks[i + 1] ? chunks[i + 1][0].s - 0.05 : Infinity;
    const end = Math.min(nextStart, c[c.length - 1].e + 0.6);
    return t >= start && t < end;
  });
  if (idx < 0) return null;
  const chunk = chunks[idx];
  const local = Math.round((t - (chunk[0].s - 0.05)) * fps);
  const pop = spring({frame: local, fps, config: {damping: 12, stiffness: 260, mass: 0.5}});

  return (
    <div
      style={{
        position: 'absolute',
        left: 60,
        right: 60,
        top: y,
        transform: `translateY(-50%) scale(${0.85 + 0.15 * pop})`,
        textAlign: 'center',
        fontFamily: FONT,
        fontWeight: 800,
        fontSize: size,
        lineHeight: 1.1,
        letterSpacing: -1,
        color: C.ink,
      }}
    >
      {chunk.map((w, i) => {
        const active = t >= w.s - 0.03 && t < w.e + 0.08;
        const swipe = interpolate(t, [w.s - 0.05, w.s + 0.12], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return (
          <span
            key={i}
            style={{
              position: 'relative',
              display: 'inline-block',
              margin: '0 0.12em',
              transform: `scale(${active ? 1.08 : 1})`,
              transition: 'none',
            }}
          >
            {w.hi ? (
              <span
                style={{
                  position: 'absolute',
                  left: '-0.1em',
                  right: '-0.1em',
                  top: '0.14em',
                  bottom: '0.04em',
                  background: C.hi,
                  borderRadius: '0.16em',
                  transform: `skewX(-8deg) scaleX(${swipe})`,
                  transformOrigin: 'left center',
                }}
              />
            ) : null}
            <span style={{position: 'relative', color: active && !w.hi ? C.kip : C.ink}}>{w.w}</span>
          </span>
        );
      })}
    </div>
  );
};
