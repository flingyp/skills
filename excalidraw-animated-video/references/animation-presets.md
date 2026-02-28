# 动画预设库

## 目录

1. [基础动画](#基础动画)
2. [手绘效果](#手绘效果)
3. [转场动画](#转场动画)
4. [文本动画](#文本动画)

---

## 基础动画

### 淡入淡出

```tsx
import { interpolate } from "remotion";

const opacity = interpolate(
  frame,
  [startFrame, startFrame + fadeInDuration],
  [0, 1],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
);
```

### 弹性缩放

```tsx
import { spring, useVideoConfig } from "remotion";

const { fps } = useVideoConfig();

const scale = spring({
  frame: frame - startFrame,
  fps,
  config: {
    damping: 15,
    stiffness: 100,
    mass: 0.5,
  },
});
```

### 平移进入

```tsx
const translateX = interpolate(
  frame,
  [startFrame, startFrame + duration],
  [-100, 0],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
);
```

---

## 手绘效果

### 逐帧绘制 (strokeDashoffset)

适用于线条、箭头等 path 元素：

```tsx
const totalLength = calculatePathLength(pathPoints);
const drawProgress = interpolate(
  frame,
  [startFrame, startFrame + drawDuration],
  [0, 1],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
);

<path
  d={pathData}
  strokeDasharray={totalLength}
  strokeDashoffset={totalLength * (1 - drawProgress)}
/>
```

### 形状绘制 (clipPath)

适用于矩形、椭圆等形状：

```tsx
const clipProgress = interpolate(
  frame,
  [startFrame, startFrame + drawDuration],
  [100, 0],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
);

<g style={{ clipPath: `inset(0 ${clipProgress}% 0 0)` }}>
  {/* shape content */}
</g>
```

### 手绘抖动 (roughjs)

使用 roughjs 生成手绘风格：

```tsx
import rough from "roughjs/bin/rough";

const rc = rough.svg(svgElement);
const shape = rc.rectangle(x, y, width, height, {
  stroke: "#1e1e1e",
  strokeWidth: 2,
  roughness: 1,
  bowing: 2,
});
```

---

## 转场动画

### 淡入转场

```tsx
const SceneTransition = ({ children }) => {
  const frame = useCurrentFrame();
  
  const opacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  
  return <div style={{ opacity }}>{children}</div>;
};
```

### 滑动转场

```tsx
const SlideTransition = ({ children, direction = "left" }) => {
  const frame = useCurrentFrame();
  
  const offset = interpolate(frame, [0, 20], [100, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  
  const transform = direction === "left" 
    ? `translateX(-${offset}%)` 
    : `translateX(${offset}%)`;
  
  return <div style={{ transform }}>{children}</div>;
};
```

### 缩放转场

```tsx
const ScaleTransition = ({ children }) => {
  const { fps } = useVideoConfig();
  const frame = useCurrentFrame();
  
  const scale = spring({
    frame,
    fps,
    config: { damping: 20, stiffness: 200 },
  });
  
  return <div style={{ transform: `scale(${scale})` }}>{children}</div>;
};
```

---

## 文本动画

### 打字机效果

```tsx
const TypewriterText = ({ text, startFrame }) => {
  const frame = useCurrentFrame();
  
  const visibleChars = Math.floor(
    interpolate(
      frame,
      [startFrame, startFrame + text.length * 2],
      [0, text.length],
      { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
    )
  );
  
  return <span>{text.slice(0, visibleChars)}</span>;
};
```

### 逐行淡入

```tsx
const LineFadeIn = ({ lines, lineDelay = 10 }) => {
  const frame = useCurrentFrame();
  
  return lines.map((line, i) => {
    const opacity = interpolate(
      frame,
      [i * lineDelay, i * lineDelay + 10],
      [0, 1],
      { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
    );
    
    return <p key={i} style={{ opacity }}>{line}</p>;
  });
};
```

### 字符跳动

```tsx
const BouncingText = ({ text }) => {
  const frame = useCurrentFrame();
  
  return text.split("").map((char, i) => {
    const delay = i * 2;
    const y = spring({
      frame: frame - delay,
      fps: 30,
      config: { damping: 10, stiffness: 200 },
    }) * 20 - 20;
    
    return (
      <span key={i} style={{ display: "inline-block", transform: `translateY(${y}px)` }}>
        {char}
      </span>
    );
  });
};
```

---

## 动画配置常量

```ts
export const ANIMATION_CONFIG = {
  // 绘制速度（帧/像素）
  drawSpeed: 2,
  
  // 淡入时长（帧）
  fadeInDuration: 15,
  
  // 元素间延迟（帧）
  staggerDelay: 5,
  
  // Spring 配置
  springConfig: {
    damping: 15,
    stiffness: 100,
    mass: 0.5,
  },
};
```

## 使用场景推荐

| 场景 | 推荐动画 | 配置 |
|------|----------|------|
| 开场标题 | 弹性缩放 + 淡入 | damping: 10, stiffness: 200 |
| 流程图展示 | 逐帧绘制 + staggerDelay | drawSpeed: 2, staggerDelay: 5 |
| 概念解释 | 逐行淡入 | lineDelay: 10 |
| 场景切换 | 淡入转场 | 15 帧 |
| 强调重点 | 弹性缩放 | damping: 15, stiffness: 100 |
