import React from 'react';
import {AbsoluteFill} from 'remotion';
import {DEX, KIP} from '../rig/characters';
import {pose} from '../rig/poses';
import {Paper} from '../scene/Paper';
import {BRAND} from '../style/brand';
import {C, FONT} from '../style/theme';
import {Avatar} from './Avatar';
import {Mini} from './CharacterSheet';

/** YouTube profile picture (800x800, shown as a circle): Kip peering through a
 * magnifying glass on Dex teal. Chosen after testing variants at 32-260 px on dark
 * and light mode; see docs/review/avatar-comparison.png and Avatar.tsx. */
export const ChannelAvatar: React.FC = () => <Avatar variant="magnifier" bg={C.dex} />;

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
