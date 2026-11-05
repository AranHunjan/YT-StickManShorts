import React from 'react';
import {AbsoluteFill} from 'remotion';
import {DEX, KIP} from '../rig/characters';
import {pose} from '../rig/poses';
import {Paper} from '../scene/Paper';
import {BRAND} from '../style/brand';
import {C, FONT} from '../style/theme';
import {Mini} from './CharacterSheet';

/** YouTube profile picture: 800x800, shown as a circle, so everything stays central. */
export const ChannelAvatar: React.FC = () => (
  <AbsoluteFill style={{background: C.hi}}>
    <svg width={800} height={800} viewBox="0 0 800 800">
      <defs>
        <pattern id="agrid" width={50} height={50} patternUnits="userSpaceOnUse">
          <path d="M 50 0 L 0 0 0 50" fill="none" stroke={C.ink} strokeWidth={2} opacity={0.08} />
        </pattern>
      </defs>
      <rect width={800} height={800} fill="url(#agrid)" />
      {/* Kip's head fills the circle; the scarf peeks in at the bottom. */}
      <Mini spec={KIP} p={pose('stand', {head: 6, lookX: 0.3})} expr="happy" cx={400} gy={1640} s={3.1} />
    </svg>
  </AbsoluteFill>
);

/**
 * YouTube banner: 2560x1440. Only the centre 1235x338 is visible on every device,
 * so the name, tagline and characters live there (x 662-1897, y 551-889).
 */
export const ChannelBanner: React.FC<{showSafeArea?: boolean}> = ({showSafeArea = false}) => {
  const ground = 886;
  return (
    <AbsoluteFill>
      <svg width={2560} height={1440} viewBox="0 0 2560 1440" style={{position: 'absolute'}}>
        <Paper w={2560} h={1440} marginX={240} grid={60} />
        <Mini spec={KIP} p={pose('wave')} expr="excited" cx={790} gy={ground} s={0.65} />
        <Mini spec={DEX} p={pose('crossArms')} expr="smug" cx={1780} gy={ground} s={0.66} facing={-1} />
        {showSafeArea ? (
          <rect x={662.5} y={551} width={1235} height={338} fill="none" stroke={C.red} strokeWidth={4} strokeDasharray="16 10" />
        ) : null}
      </svg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 590, textAlign: 'center', fontFamily: FONT, color: C.ink}}>
        <div style={{fontWeight: 800, fontSize: 136, lineHeight: 1, letterSpacing: -2}}>
          KIP <span style={{background: C.hi, padding: '0 14px', borderRadius: 14}}>N</span> DEX
        </div>
        <div style={{fontWeight: 600, fontSize: 42, marginTop: 14}}>{BRAND.tagline}</div>
        <div
          style={{
            display: 'inline-block',
            marginTop: 14,
            padding: '5px 20px',
            background: C.ink,
            color: C.paper,
            fontWeight: 800,
            fontSize: 27,
            borderRadius: 30,
          }}
        >
          A NEW SHORT EVERY DAY · {BRAND.handle}
        </div>
      </div>
    </AbsoluteFill>
  );
};
