import {C} from '../style/theme';
import type {CharacterSpec} from './types';

/** Kip: the curious lead. Big round head, cowlick, orange scarf. */
export const KIP: CharacterSpec = {
  id: 'kip',
  headR: 64,
  neck: 12,
  torso: 140,
  shoulderDrop: 16,
  upperArm: 82,
  forearm: 78,
  thigh: 92,
  shin: 92,
  foot: 20,
  stroke: 13,
  ink: C.ink,
  headFill: C.white,
  accent: C.kip,
  eyeSpacing: 34,
  cowlick: true,
  scarf: true,
  brows: true,
};

/** Dex: the deadpan expert. Taller, thinner, round glasses, teal bow tie. */
export const DEX: CharacterSpec = {
  id: 'dex',
  headR: 54,
  neck: 18,
  torso: 168,
  shoulderDrop: 18,
  upperArm: 94,
  forearm: 88,
  thigh: 110,
  shin: 108,
  foot: 20,
  stroke: 12,
  ink: C.ink,
  headFill: C.white,
  accent: C.dex,
  eyeSpacing: 32,
  glasses: true,
  bowtie: true,
  brows: true,
};
