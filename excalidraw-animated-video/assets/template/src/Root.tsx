import { Composition } from "remotion";
import { ExcalidrawVideo } from "./compositions/ExcalidrawVideo";
import { VIDEO_CONFIG } from "./config";

export const RemotionRoot = () => {
  return (
    <Composition
      id="ExcalidrawVideo"
      component={ExcalidrawVideo}
      durationInFrames={VIDEO_CONFIG.defaultDuration * VIDEO_CONFIG.fps}
      fps={VIDEO_CONFIG.fps}
      width={VIDEO_CONFIG.width}
      height={VIDEO_CONFIG.height}
      defaultProps={{
        title: "手绘动画视频",
        scenes: [],
        excalidrawData: {},
      }}
    />
  );
};
