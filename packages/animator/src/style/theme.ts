import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

// Brand palette. Keep in sync with docs/CHARACTERS.md.
export const C = {
  paper: '#F4EFE4',
  ink: '#1B1B1F',
  white: '#FFFDF8',
  kip: '#FF6B1A',
  dex: '#13A0A0',
  hi: '#FFE14D',
  red: '#E63946',
  sky: '#4D9DE0',
  leaf: '#3BB273',
  grid: '#A9C3DB',
  margin: '#E79A9A',
} as const;

// Fonts are bundled in public/fonts (OFL licence) so renders work offline and
// look identical on every machine. loadFont blocks rendering until they load.
export const FONT = 'Poppins';
loadFont({family: FONT, url: staticFile('fonts/poppins-latin-600-normal.woff2'), weight: '600'});
loadFont({family: FONT, url: staticFile('fonts/poppins-latin-800-normal.woff2'), weight: '800'});

// Shorts canvas
export const W = 1080;
export const H = 1920;
export const FPS = 30;
