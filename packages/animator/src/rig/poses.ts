import type {Pose} from './types';

/** Neutral standing pose. Every named pose is a partial override of this. */
export const STAND: Pose = {
  x: 540,
  lift: 0,
  lean: 0,
  head: 0,
  armB: [-12, 8],
  armF: [12, 10],
  legB: [-7, 0],
  legF: [7, 0],
  squash: 1,
  mouth: 0,
  lookX: 0,
  lookY: 0,
  hair: 0,
  hairQ: 0,
  wind: 0,
};

export const POSES = {
  stand: {},
  wave: {armF: [120, 40], armB: [-14, 10], head: 4},
  point: {armF: [92, 0], armB: [-18, 14], lean: 4, lookX: 1},
  pointUp: {armF: [165, 5], armB: [-14, 10], head: -6, lookY: -1},
  shrug: {armF: [55, 95], armB: [-55, -95], head: 8, squash: 0.97},
  think: {armF: [60, 125], armB: [-10, 70], head: 10, lookY: -0.8, lookX: 0.6},
  // Arm angles below keep elbows outside the head circle so arms never cross the face.
  mindblown: {
    armF: [115, 45], armB: [-100, -60], lean: -12, head: -10, lift: 30,
    legB: [-22, 18], legF: [24, -30], hair: 1, squash: 1.04,
  },
  shocked: {armF: [70, 70], armB: [-70, -70], lean: -8, head: -6, hair: 0.7},
  scratchHead: {armB: [-108, -81], armF: [14, 10], head: 8, hairQ: 1},
  crossArms: {armF: [25, -110], armB: [-25, 110], head: -3},
  holdCard: {armF: [120, -10], armB: [-12, 20], head: 6, lookX: 0.4},
  adjustGlasses: {armF: [112, 115], armB: [-12, 20], head: 2},
  celebrate: {armF: [125, 20], armB: [-125, -20], lift: 24, legB: [-20, 30], legF: [20, -30], hair: 0.6},
  sad: {armF: [6, 0], armB: [-6, 0], lean: 6, head: 16, hair: -1, squash: 0.95, lookY: 1},
} satisfies Record<string, Partial<Pose>>;

export type PoseName = keyof typeof POSES;

export const pose = (name: PoseName, extra: Partial<Pose> = {}): Pose => ({
  ...STAND,
  ...(POSES[name] as Partial<Pose>),
  ...extra,
});
