import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(95);
Config.setOverwriteOutput(true);
// Standard limited-range BT.709 video (what YouTube expects). Without the colour
// space, JPEG frames come out as full-range yuvj420p and colours can shift.
Config.setPixelFormat('yuv420p');
Config.setColorSpace('bt709');

// Optional: point Remotion at an already-installed Chrome Headless Shell.
// Leave REMOTION_BROWSER unset on a normal PC and Remotion downloads its own.
if (process.env.REMOTION_BROWSER) {
  Config.setBrowserExecutable(process.env.REMOTION_BROWSER);
}
