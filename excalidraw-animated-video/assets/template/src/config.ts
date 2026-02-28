export const VIDEO_CONFIG = {
  width: 1920,
  height: 1080,
  fps: 30,
  defaultDuration: 30,
} as const;

export const ANIMATION_CONFIG = {
  drawSpeed: 2,
  fadeInDuration: 15,
  staggerDelay: 5,
  springConfig: {
    damping: 15,
    stiffness: 100,
    mass: 0.5,
  },
} as const;

export const COLORS = {
  stroke: "#1e1e1e",
  fill: {
    blue: "#a5d8ff",
    green: "#b2f2bb",
    orange: "#ffd8a8",
    purple: "#d0bfff",
    red: "#ffc9c9",
    yellow: "#fff3bf",
    cyan: "#c3fae8",
    pink: "#eebefa",
  },
  text: {
    title: "#1e40af",
    subtitle: "#3b82f6",
    body: "#374151",
    emphasis: "#f59e0b",
  },
} as const;
