# Remotion 项目模板

完整的 Remotion 视频项目结构和代码模板。

## 项目结构

```
video-project/
├── src/
│   ├── Root.tsx              # 入口，注册 Composition
│   ├── Composition.tsx       # 主组件
│   ├── scenes/
│   │   ├── IntroScene.tsx    # 开场场景
│   │   ├── MainScene.tsx     # 主体场景
│   │   └── OutroScene.tsx    # 结尾场景
│   ├── components/
│   │   ├── ExcalidrawFrame.tsx    # 图表渲染组件
│   │   └── AnimatedText.tsx       # 文字动画组件
│   └── config/
│       └── styles.ts         # 视觉风格配置
├── assets/
│   └── diagrams/             # Excalidraw 文件
│       ├── scene-1.excalidraw
│       └── scene-2.excalidraw
├── package.json
├── tsconfig.json
└── remotion.config.ts
```

## 依赖安装

```bash
# 创建项目
npx create-video@latest video-project

# 安装过渡效果
npm install @remotion/transitions @remotion/transitions

# 安装 Zod（参数化）
npm install zod @remotion/zod-types
```

## 核心文件模板

### package.json

```json
{
  "name": "excalidraw-video",
  "version": "1.0.0",
  "scripts": {
    "start": "remotion studio",
    "build": "remotion render src/index.ts ExcalidrawVideo out/video.mp4",
    "render": "remotion render"
  },
  "dependencies": {
    "@remotion/player": "^4.0.0",
    "@remotion/transitions": "^4.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "remotion": "^4.0.0",
    "zod": "^3.22.0",
    "@remotion/zod-types": "^4.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "typescript": "^5.0.0"
  }
}
```

### src/config/styles.ts

```typescript
export const STYLES = {
  background: "#faf8f5",
  stroke: "#2d3748",
  text: "#1a202c",
  accent: {
    red: "#c53030",
    blue: "#2b6cb0",
    green: "#38a169",
  },
  font: {
    family: 5,
    title: 28,
    body: 18,
    caption: 14,
  },
};
```

### src/Root.tsx

```tsx
import { Composition } from "remotion";
import { ExcalidrawVideo, videoSchema } from "./Composition";

export const RemotionRoot = () => {
  return (
    <Composition
      id="ExcalidrawVideo"
      component={ExcalidrawVideo}
      durationInFrames={450}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{
        title: "讲解视频",
        theme: "cream",
      }}
      schema={videoSchema}
    />
  );
};
```

### src/Composition.tsx

```tsx
import { z } from "zod";
import { zColor } from "@remotion/zod-types";
import { AbsoluteFill } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { IntroScene } from "./scenes/IntroScene";
import { MainScene } from "./scenes/MainScene";
import { OutroScene } from "./scenes/OutroScene";

export const videoSchema = z.object({
  title: z.string(),
  theme: z.enum(["cream"]),
  accentColor: zColor().optional(),
});

type VideoProps = z.infer<typeof videoSchema>;

export const ExcalidrawVideo: React.FC<VideoProps> = (props) => {
  const fps = 30;

  return (
    <AbsoluteFill style={{ backgroundColor: "#faf8f5" }}>
      <TransitionSeries>
        {/* 开场 */}
        <TransitionSeries.Sequence durationInFrames={150}>
          <IntroScene title={props.title} />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 15 })}
        />

        {/* 主体 */}
        <TransitionSeries.Sequence durationInFrames={300}>
          <MainScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 15 })}
        />

        {/* 结尾 */}
        <TransitionSeries.Sequence durationInFrames={180}>
          <OutroScene />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};
```

### src/scenes/IntroScene.tsx

```tsx
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { STYLES } from "../config/styles";

type IntroProps = {
  title: string;
};

export const IntroScene: React.FC<IntroProps> = ({ title }) => {
  const frame = useCurrentFrame();
  const fps = 30;

  const opacity = interpolate(frame, [0, 1 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });

  const scale = interpolate(frame, [0, 0.5 * fps], [0.9, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: STYLES.background,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <h1
        style={{
          fontFamily: "Virgil, Segoe UI Emoji, sans-serif",
          fontSize: 64,
          color: STYLES.text,
          opacity,
          transform: `scale(${scale})`,
          fontWeight: 400,
        }}
      >
        {title}
      </h1>
    </AbsoluteFill>
  );
};
```

### src/scenes/MainScene.tsx

```tsx
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { staticFile, Img } from "remotion";
import { STYLES } from "../config/styles";

export const MainScene: React.FC = () => {
  const frame = useCurrentFrame();
  const fps = 30;

  const diagramOpacity = interpolate(frame, [0, 1 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: STYLES.background,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* 方案1: 使用导出的 SVG/图片 */}
      <Img
        src={staticFile("diagrams/main-diagram.svg")}
        style={{
          opacity: diagramOpacity,
          maxWidth: "80%",
          maxHeight: "80%",
        }}
      />
    </AbsoluteFill>
  );
};
```

### src/scenes/OutroScene.tsx

```tsx
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { STYLES } from "../config/styles";

export const OutroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const fps = 30;

  const opacity = interpolate(
    frame,
    [0, 0.5 * fps, 4.5 * fps, 5 * fps],
    [0, 1, 1, 0],
    { extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: STYLES.background,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <h2
        style={{
          fontFamily: "Virgil, Segoe UI Emoji, sans-serif",
          fontSize: 48,
          color: STYLES.text,
          opacity,
          fontWeight: 400,
        }}
      >
        感谢观看
      </h2>
    </AbsoluteFill>
  );
};
```

## 图表集成方案

### 方案 A: SVG 导出（推荐）

1. 使用 Excalidraw 导出 SVG
2. 放入 `public/diagrams/` 目录
3. 使用 `staticFile()` + `<Img>` 渲染

### 方案 B: WebM 动画

1. 使用 excalidraw-animate 导出 WebM
2. 使用 `<Video>` 组件播放

```tsx
import { Video, staticFile } from "remotion";

<Video
  src={staticFile("diagrams/animated-diagram.webm")}
  style={{ width: "100%", height: "100%" }}
/>
```

### 方案 C: JSON 内嵌

直接将 Excalidraw JSON 嵌入 Remotion，用自定义渲染器绘制：

```tsx
import { ExcalidrawFrame } from "../components/ExcalidrawFrame";

<ExcalidrawFrame
  elements={excalidrawElements}
  animateFrom={0}
  animateDuration={10 * fps}
/>
```

## 渲染命令

```bash
# 开发预览
npm run start

# 渲染输出
npx remotion render src/index.ts ExcalidrawVideo out/video.mp4

# 高质量输出
npx remotion render src/index.ts ExcalidrawVideo out/video.mp4 \
  --quality 100 \
  --codec h264

# 不同分辨率
npx remotion render src/index.ts ExcalidrawVideo out/1080p.mp4 \
  --width 1920 --height 1080

npx remotion render src/index.ts ExcalidrawVideo out/4k.mp4 \
  --width 3840 --height 2160
```

## 参数化配置

通过 Remotion Studio 可视化编辑参数：

```tsx
// 访问 http://localhost:3000
// 右侧面板可调整 title、accentColor 等参数
```
