export type ExcalidrawElementType = 
  | "rectangle" 
  | "ellipse" 
  | "diamond" 
  | "arrow" 
  | "line" 
  | "text" 
  | "freedraw";

export interface ExcalidrawAnimation {
  order: number;
  duration?: number;
}

export interface ExcalidrawElement {
  id: string;
  type: ExcalidrawElementType;
  x: number;
  y: number;
  width: number;
  height: number;
  angle: number;
  strokeColor: string;
  backgroundColor: string;
  fillStyle: "solid" | "hachure" | "zigzag" | "cross-hatch";
  strokeWidth: number;
  strokeStyle: "solid" | "dashed" | "dotted";
  roughness: number;
  opacity: number;
  groupIds: string[];
  roundness: { type: number } | null;
  seed: number;
  version: number;
  isDeleted: boolean;
  boundElements: unknown[] | null;
  updated: number;
  link: string | null;
  locked: boolean;
  customData?: {
    animate?: ExcalidrawAnimation;
  };
}

export interface TextElement extends ExcalidrawElement {
  type: "text";
  text: string;
  fontSize: number;
  fontFamily: number;
  textAlign: "left" | "center" | "right";
  verticalAlign: "top" | "middle" | "bottom";
  containerId: string | null;
  originalText: string;
  autoResize: boolean;
  lineHeight: number;
}

export interface ArrowElement extends ExcalidrawElement {
  type: "arrow" | "line";
  points: { x: number; y: number }[];
  startBinding: unknown | null;
  endBinding: unknown | null;
  startArrowhead: string | null;
  endArrowhead: string | null;
}

export interface ExcalidrawData {
  type: "excalidraw";
  version: number;
  source: string;
  elements: ExcalidrawElement[];
  appState: {
    gridSize: number | null;
    viewBackgroundColor: string;
  };
  files: Record<string, unknown>;
}

export interface SceneConfig {
  id: string;
  title: string;
  voiceover?: string;
  duration: number;
  diagramType: string;
  excalidrawFile?: string;
}

export interface Storyboard {
  title: string;
  duration: number;
  scenes: SceneConfig[];
}
