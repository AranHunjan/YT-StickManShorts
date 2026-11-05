import React from 'react';
import {Composition, Still} from 'remotion';
import {CharacterSheet} from './compositions/CharacterSheet';
import {RigTest} from './compositions/RigTest';
import {FPS, H, W} from './style/theme';

export const Root: React.FC = () => (
  <>
    <Still id="CharacterSheet" component={CharacterSheet} width={1920} height={1080} />
    <Composition id="RigTest" component={RigTest} durationInFrames={270} fps={FPS} width={W} height={H} defaultProps={{showSafeZones: false}} />
    <Composition id="RigTestSafeZones" component={RigTest} durationInFrames={270} fps={FPS} width={W} height={H} defaultProps={{showSafeZones: true}} />
  </>
);
