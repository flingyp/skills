import React from "react";
import { AbsoluteFill } from "remotion";
import { SceneComposer } from "../components/SceneComposer";
import { SceneConfig, ExcalidrawData } from "../types/excalidraw";

export type ExcalidrawVideoProps = {
  title: string;
  scenes: SceneConfig[];
  excalidrawData: Record<string, ExcalidrawData>;
};

export const ExcalidrawVideo: React.FC<ExcalidrawVideoProps> = ({
  title,
  scenes,
  excalidrawData,
}) => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#ffffff" }}>
      <SceneComposer scenes={scenes} excalidrawData={excalidrawData} />
    </AbsoluteFill>
  );
};

export default ExcalidrawVideo;
