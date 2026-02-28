import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Sequence,
  AbsoluteFill,
} from "remotion";
import { ExcalidrawPlayer } from "./ExcalidrawPlayer";
import { SceneConfig, ExcalidrawData } from "../types/excalidraw";
import { VIDEO_CONFIG } from "../config";

interface SceneComposerProps {
  scenes: SceneConfig[];
  excalidrawData: Record<string, ExcalidrawData>;
}

export const SceneComposer: React.FC<SceneComposerProps> = ({
  scenes,
  excalidrawData,
}) => {
  const { fps } = useVideoConfig();

  let currentFrame = 0;

  return (
    <AbsoluteFill style={{ backgroundColor: "#ffffff" }}>
      {scenes.map((scene, index) => {
        const sceneStartFrame = currentFrame;
        const sceneDuration = scene.duration * fps;
        currentFrame += sceneDuration;

        const sceneData = excalidrawData[scene.id];

        return (
          <Sequence
            key={scene.id}
            from={sceneStartFrame}
            durationInFrames={sceneDuration}
          >
            <SceneTransition index={index} totalScenes={scenes.length}>
              {sceneData ? (
                <ExcalidrawPlayer
                  elements={sceneData.elements}
                  currentSceneFrame={0}
                />
              ) : (
                <div
                  style={{
                    width: "100%",
                    height: "100%",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 48,
                    color: "#374151",
                    fontFamily: "Caveat, sans-serif",
                  }}
                >
                  {scene.title}
                </div>
              )}
            </SceneTransition>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

const SceneTransition: React.FC<{
  index: number;
  totalScenes: number;
  children: React.ReactNode;
}> = ({ index, totalScenes, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fadeIn = interpolate(frame, [0, 10], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const fadeOut = interpolate(frame, [-10, 0], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        opacity: fadeIn,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

export default SceneComposer;
