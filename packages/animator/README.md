# Animator (Remotion)

The stickman rig, the characters (Kip and Dex), motion-graphics pieces, and the episode compositions.

## Run it on Windows

1. Install **Node.js 22 LTS** from nodejs.org.
2. In PowerShell:

```powershell
cd packages\animator
npm install
npm run studio
```

`npm run studio` opens Remotion Studio in your browser. You can scrub the timeline, see every composition, and change props live.

Render the review files:

```powershell
npm run render:sheet     # out\character-sheet.png
npm run render:rigtest   # out\rig-test.mp4 (9 s test clip)
```

The first render downloads a headless Chrome automatically. Fonts are bundled in `public/fonts` (Poppins, OFL licence), so rendering works offline.

## Layout

| Path | What |
|---|---|
| `src/rig/types.ts` | Pose model: every value is a number, so poses can be interpolated |
| `src/rig/skeleton.ts` | Forward kinematics. Feet stay on the ground automatically; characters mirror with `facing` |
| `src/rig/Stickman.tsx` | Draws a character: limbs, head, cowlick, scarf, bow tie, hands |
| `src/rig/Face.tsx` | 12 expressions, blinking, talking mouth, glasses, brows |
| `src/rig/poses.ts` | Named poses (wave, point, think, mindblown, ...) |
| `src/rig/animate.ts` | Keyframe tracks, easing, breathing idle, walk cycle, talk flaps, blinks |
| `src/rig/characters.ts` | Kip and Dex proportions and accessories |
| `src/scene/*` | Notebook paper, line boil, highlighter captions, burst, index card, safe zones |
| `src/compositions/*` | Character sheet and rig test |

## Conventions

- **Angles:** 0 = hanging straight down, +90 = pointing the way the character faces, 180 = straight up. Elbows and knees are relative to the parent segment.
- **Arms near the head:** keep the elbows outside the head circle, so arms never cross the face. The comments in `poses.ts` cover this.
- **Safe zones:** keep important things out of the red areas in the `RigTestSafeZones` composition, where the Shorts UI sits.
