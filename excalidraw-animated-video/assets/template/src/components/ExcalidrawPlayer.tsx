import React, { useMemo } from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import rough from "roughjs/bin/rough";
import { ExcalidrawElement, TextElement, ArrowElement } from "../types/excalidraw";
import { ANIMATION_CONFIG } from "../config";

interface ExcalidrawPlayerProps {
  elements: ExcalidrawElement[];
  currentSceneFrame?: number;
}

export const ExcalidrawPlayer: React.FC<ExcalidrawPlayerProps> = ({
  elements,
  currentSceneFrame = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const canvasRef = React.useRef<HTMLCanvasElement>(null);

  const sortedElements = useMemo(() => {
    return [...elements].sort((a, b) => {
      const orderA = a.customData?.animate?.order ?? 999;
      const orderB = b.customData?.animate?.order ?? 999;
      return orderA - orderB;
    });
  }, [elements]);

  const animationGroups = useMemo(() => {
    const groups: Map<number, ExcalidrawElement[]> = new Map();
    sortedElements.forEach((el) => {
      const order = el.customData?.animate?.order ?? 999;
      if (!groups.has(order)) {
        groups.set(order, []);
      }
      groups.get(order)!.push(el);
    });
    return groups;
  }, [sortedElements]);

  const getElementVisibility = (element: ExcalidrawElement): number => {
    const order = element.customData?.animate?.order ?? 999;
    const groupElements = animationGroups.get(order) || [];
    const groupIndex = groupElements.indexOf(element);
    const orderStartFrame = (order - 1) * ANIMATION_CONFIG.staggerDelay * 3;
    const elementStartFrame = orderStartFrame + groupIndex * 2;
    
    return interpolate(
      frame - currentSceneFrame,
      [elementStartFrame, elementStartFrame + ANIMATION_CONFIG.fadeInDuration],
      [0, 1],
      { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
    );
  };

  const getDrawProgress = (element: ExcalidrawElement): number => {
    const order = element.customData?.animate?.order ?? 999;
    const duration = element.customData?.animate?.duration ?? 500;
    const durationInFrames = (duration / 1000) * fps;
    const startFrame = (order - 1) * ANIMATION_CONFIG.staggerDelay * 3;
    
    return interpolate(
      frame - currentSceneFrame,
      [startFrame, startFrame + durationInFrames],
      [0, 1],
      { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
    );
  };

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        position: "relative",
        backgroundColor: "#ffffff",
      }}
    >
      <svg
        width="100%"
        height="100%"
        viewBox="0 0 1920 1080"
        style={{ position: "absolute", top: 0, left: 0 }}
      >
        {sortedElements.map((element) => {
          const opacity = getElementVisibility(element);
          if (opacity <= 0) return null;

          if (element.type === "text") {
            return (
              <TextRenderer
                key={element.id}
                element={element as TextElement}
                opacity={opacity}
              />
            );
          }

          if (element.type === "arrow" || element.type === "line") {
            return (
              <ArrowRenderer
                key={element.id}
                element={element as ArrowElement}
                opacity={opacity}
                drawProgress={getDrawProgress(element)}
              />
            );
          }

          return (
            <ShapeRenderer
              key={element.id}
              element={element}
              opacity={opacity}
              drawProgress={getDrawProgress(element)}
            />
          );
        })}
      </svg>
    </div>
  );
};

const TextRenderer: React.FC<{
  element: TextElement;
  opacity: number;
}> = ({ element, opacity }) => {
  return (
    <text
      x={element.x + element.width / 2}
      y={element.y + element.height / 2}
      fill={element.strokeColor}
      fontSize={element.fontSize}
      fontFamily="Caveat, Segoe UI Emoji, sans-serif"
      textAnchor="middle"
      dominantBaseline="middle"
      opacity={opacity}
      style={{
        lineHeight: element.lineHeight,
      }}
    >
      {element.text}
    </text>
  );
};

const ArrowRenderer: React.FC<{
  element: ArrowElement;
  opacity: number;
  drawProgress: number;
}> = ({ element, opacity, drawProgress }) => {
  const points = element.points || [];
  if (points.length < 2) return null;

  const totalLength = points.reduce((acc, _, i) => {
    if (i === 0) return 0;
    const dx = points[i].x - points[i - 1].x;
    const dy = points[i].y - points[i - 1].y;
    return acc + Math.sqrt(dx * dx + dy * dy);
  }, 0);

  const pathData = points
    .map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.y}`)
    .join(" ");

  const dashArray = totalLength;
  const dashOffset = totalLength * (1 - drawProgress);

  return (
    <g transform={`translate(${element.x}, ${element.y})`}>
      <path
        d={pathData}
        stroke={element.strokeColor}
        strokeWidth={element.strokeWidth}
        strokeDasharray={`${dashArray}`}
        strokeDashoffset={dashOffset}
        fill="none"
        opacity={opacity}
        markerEnd={element.type === "arrow" ? "url(#arrowhead)" : undefined}
      />
    </g>
  );
};

const ShapeRenderer: React.FC<{
  element: ExcalidrawElement;
  opacity: number;
  drawProgress: number;
}> = ({ element, opacity, drawProgress }) => {
  const rc = rough.svg(document.createElementNS("http://www.w3.org/2000/svg", "svg"));
  
  let shape: SVGGElement;
  const options = {
    stroke: element.strokeColor,
    strokeWidth: element.strokeWidth,
    fill: element.backgroundColor === "transparent" ? undefined : element.backgroundColor,
    fillStyle: element.fillStyle,
    roughness: element.roughness,
    bowing: 2,
  };

  switch (element.type) {
    case "rectangle":
      shape = rc.rectangle(0, 0, element.width, element.height, options);
      break;
    case "ellipse":
      shape = rc.ellipse(element.width / 2, element.height / 2, element.width, element.height, options);
      break;
    case "diamond":
      const hw = element.width / 2;
      const hh = element.height / 2;
      shape = rc.path(`M ${hw} 0 L ${element.width} ${hh} L ${hw} ${element.height} L 0 ${hh} Z`, options);
      break;
    default:
      return null;
  }

  return (
    <g transform={`translate(${element.x}, ${element.y})`} opacity={opacity}>
      <g
        dangerouslySetInnerHTML={{
          __html: shape.innerHTML,
        }}
        style={{
          clipPath: `inset(0 ${(1 - drawProgress) * 100}% 0 0)`,
        }}
      />
    </g>
  );
};

export default ExcalidrawPlayer;
