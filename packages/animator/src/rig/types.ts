export type Expression =
  | 'neutral'
  | 'happy'
  | 'excited'
  | 'shocked'
  | 'mindblown'
  | 'smug'
  | 'confused'
  | 'scared'
  | 'angry'
  | 'sleepy'
  | 'determined'
  | 'deadpan';

export const EXPRESSIONS: Expression[] = [
  'neutral', 'happy', 'excited', 'shocked', 'mindblown', 'smug',
  'confused', 'scared', 'angry', 'sleepy', 'determined', 'deadpan',
];

/** [root angle, joint angle]. Root angle is screen-absolute: 0 = straight down,
 * +90 = pointing forward (the way the character faces), 180 = straight up.
 * Joint angle is relative to the parent segment. */
export type Limb = [number, number];

/** Everything numeric so poses can be interpolated. Authored facing right. */
export type Pose = {
  x: number; // hip x in canvas px
  lift: number; // px above the ground (jumps)
  lean: number; // torso tilt in degrees, + = top leans forward
  head: number; // head tilt relative to the torso
  armB: Limb; // back arm (drawn behind)
  armF: Limb; // front arm
  legB: Limb;
  legF: Limb;
  squash: number; // 1 = normal torso length
  mouth: number; // 0..1 mouth open (talking)
  lookX: number; // -1..1 pupil offset
  lookY: number;
  hair: number; // Kip's cowlick: -1 droop, 0 normal, 1 sprung straight up
  hairQ: number; // 0..1 morph toward a question-mark curl
  wind: number; // 0..1 scarf blown back
};

export type CharacterSpec = {
  id: string;
  headR: number;
  neck: number;
  torso: number;
  shoulderDrop: number;
  upperArm: number;
  forearm: number;
  thigh: number;
  shin: number;
  foot: number;
  stroke: number;
  ink: string;
  headFill: string;
  accent: string;
  eyeSpacing: number;
  cowlick?: boolean;
  scarf?: boolean;
  glasses?: boolean;
  bowtie?: boolean;
  brows?: boolean;
};

export type Pt = {x: number; y: number};

export type Joints = {
  hip: Pt;
  neckBase: Pt;
  shoulder: Pt;
  headC: Pt;
  headAngle: number; // world rotation of the head, already mirrored
  facing: 1 | -1;
  armB: {root: Pt; joint: Pt; end: Pt; endAngle: number};
  armF: {root: Pt; joint: Pt; end: Pt; endAngle: number};
  legB: {root: Pt; joint: Pt; end: Pt; endAngle: number};
  legF: {root: Pt; joint: Pt; end: Pt; endAngle: number};
  up: Pt; // torso up vector (world)
  perp: Pt; // torso forward vector (world)
};
