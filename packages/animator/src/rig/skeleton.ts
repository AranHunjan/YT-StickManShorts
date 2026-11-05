import type {CharacterSpec, Joints, Limb, Pose, Pt} from './types';

const rad = (d: number) => (d * Math.PI) / 180;
const add = (a: Pt, b: Pt): Pt => ({x: a.x + b.x, y: a.y + b.y});
const mul = (a: Pt, k: number): Pt => ({x: a.x * k, y: a.y * k});

/** Unit vector for a "hanging" angle: 0 = down, +90 = forward (+x). */
export const hang = (deg: number): Pt => ({x: Math.sin(rad(deg)), y: Math.cos(rad(deg))});

const limb = (root: Pt, [a, b]: Limb, l1: number, l2: number) => {
  const joint = add(root, mul(hang(a), l1));
  const end = add(joint, mul(hang(a + b), l2));
  return {root, joint, end, endAngle: a + b};
};

/**
 * Forward kinematics. The pose is authored facing right in local space with the
 * hip at the origin; the hip height is then solved so the lowest foot rests on
 * `groundY` (minus `lift`), and everything is mirrored when facing left.
 */
export function solve(spec: CharacterSpec, pose: Pose, groundY: number, facing: 1 | -1 = 1): Joints {
  const o: Pt = {x: 0, y: 0};
  const up: Pt = {x: Math.sin(rad(pose.lean)), y: -Math.cos(rad(pose.lean))};
  const perp: Pt = {x: Math.cos(rad(pose.lean)), y: Math.sin(rad(pose.lean))};
  const torso = spec.torso * pose.squash;
  const neckBase = add(o, mul(up, torso));
  const shoulder = add(o, mul(up, torso - spec.shoulderDrop));
  const headAngle = pose.lean + pose.head;
  const headUp: Pt = {x: Math.sin(rad(headAngle)), y: -Math.cos(rad(headAngle))};
  const headC = add(neckBase, mul(headUp, spec.neck + spec.headR));

  const legB = limb(o, pose.legB, spec.thigh, spec.shin);
  const legF = limb(o, pose.legF, spec.thigh, spec.shin);
  const armB = limb(shoulder, pose.armB, spec.upperArm, spec.forearm);
  const armF = limb(shoulder, pose.armF, spec.upperArm, spec.forearm);

  const lowest = Math.max(legB.end.y, legF.end.y) + spec.stroke / 2;
  const hipY = groundY - lowest - pose.lift;

  const w = (p: Pt): Pt => ({x: pose.x + facing * p.x, y: hipY + p.y});
  const wl = (l: ReturnType<typeof limb>) => ({
    root: w(l.root),
    joint: w(l.joint),
    end: w(l.end),
    endAngle: facing * l.endAngle,
  });

  return {
    hip: w(o),
    neckBase: w(neckBase),
    shoulder: w(shoulder),
    headC: w(headC),
    headAngle: facing * headAngle,
    facing,
    armB: wl(armB),
    armF: wl(armF),
    legB: wl(legB),
    legF: wl(legF),
    up: {x: facing * up.x, y: up.y},
    perp: {x: facing * perp.x, y: perp.y},
  };
}
