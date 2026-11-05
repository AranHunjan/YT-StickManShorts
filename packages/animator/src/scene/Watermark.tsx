import React from 'react';
import {BRAND} from '../style/brand';
import {C, FONT} from '../style/theme';

/** Tiny Kip head (with cowlick) used as the channel's logo mark. */
export const KipMark: React.FC<{size?: number}> = ({size = 46}) => (
  <svg width={size} height={size} viewBox="-70 -110 140 180" style={{display: 'block'}}>
    <path d="M 2 -56 C 6 -84, -16 -98, -26 -84 C -32 -75, -22 -66, -14 -73" stroke={C.paper} strokeWidth={11} fill="none" strokeLinecap="round" />
    <circle r={58} fill={C.white} stroke={C.paper} strokeWidth={10} />
    <ellipse cx={-7} cy={-6} rx={7} ry={10} fill={C.ink} />
    <ellipse cx={27} cy={-6} rx={7} ry={10} fill={C.ink} />
    <path d="M -2 18 Q 13 40 30 18 Z" fill={C.ink} />
  </svg>
);

type Props = {
  episode?: number;
  /** Faint handle under the characters, so the video can't be cropped to remove it. */
  antiCrop?: boolean;
  antiCropY?: number;
};

/**
 * Burned-in channel watermark:
 *  1. a brand pill in the top-left, inside the Shorts safe area (below the top UI band);
 *  2. a faint handle just under the characters, above the bottom UI band.
 */
export const Watermark: React.FC<Props> = ({episode, antiCrop = true, antiCropY = 1500}) => (
  <>
    <div
      style={{
        position: 'absolute',
        left: 124,
        top: 168,
        display: 'flex',
        alignItems: 'center',
        gap: 14,
        padding: '8px 22px 8px 12px',
        background: C.ink,
        borderRadius: 40,
        transform: 'rotate(-2deg)',
        opacity: 0.94,
        boxShadow: '0 4px 0 rgba(0,0,0,0.12)',
      }}
    >
      <KipMark />
      <span style={{fontFamily: FONT, fontWeight: 800, fontSize: 32, color: C.paper, letterSpacing: 0.5}}>
        {BRAND.name.toUpperCase()}
      </span>
      {episode !== undefined ? (
        <span style={{fontFamily: FONT, fontWeight: 800, fontSize: 32, color: C.hi}}>#{String(episode).padStart(3, '0')}</span>
      ) : null}
    </div>
    {antiCrop ? (
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: antiCropY,
          textAlign: 'center',
          fontFamily: FONT,
          fontWeight: 600,
          fontSize: 30,
          color: C.ink,
          opacity: 0.35,
          letterSpacing: 1,
        }}
      >
        {BRAND.handle}
      </div>
    ) : null}
  </>
);
