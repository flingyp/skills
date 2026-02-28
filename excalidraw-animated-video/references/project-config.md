# 项目配置规范

## 目录结构

```
project-name/
├── src/
│   ├── Root.tsx                 # Remotion 入口
│   ├── config.ts                # 配置常量
│   ├── types/
│   │   └── excalidraw.ts        # 类型定义
│   ├── components/
│   │   ├── ExcalidrawPlayer.tsx # Excalidraw 渲染器
│   │   └── SceneComposer.tsx    # 场景组合器
│   └── compositions/
│       └── ExcalidrawVideo.tsx  # 主 Composition
├── excalidraw/
│   ├── scene-1.excalidraw       # 场景 1 Excalidraw 文件
│   ├── scene-2.excalidraw       # 场景 2 Excalidraw 文件
│   └── ...
├── public/
│   └── fonts/                   # 字体文件
├── out/                         # 输出目录
│   ├── video.mp4
│   └── video.webm
├── video.script.md              # 语音文本脚本 (Phase 1 生成)
├── storyboard.json              # 分镜脚本
├── package.json
├── tsconfig.json
└── remotion.config.ts           # Remotion 配置
```

---

## 配置文件

### config.ts

```ts
export const VIDEO_CONFIG = {
  width: 1920,        // 16:9 横屏宽度
  height: 1080,       // 16:9 横屏高度
  fps: 30,            // 帧率
  defaultDuration: 30, // 默认时长（秒）
} as const;

export const ANIMATION_CONFIG = {
  drawSpeed: 2,         // 绘制速度
  fadeInDuration: 15,   // 淡入帧数
  staggerDelay: 5,      // 元素间延迟帧数
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
```

### remotion.config.ts

```ts
import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
```

### package.json scripts

```json
{
  "scripts": {
    "start": "remotion studio",
    "preview": "remotion preview",
    "build": "remotion render ExcalidrawVideo out/video.mp4",
    "build:webm": "remotion render ExcalidrawVideo out/video.webm --codec=vp9",
    "build:all": "npm run build && npm run build:webm"
  }
}
```

---

## 分镜脚本格式

### storyboard.json

```json
{
  "title": "视频标题",
  "duration": 60,
  "scenes": [
    {
      "id": "scene-1",
      "title": "开场",
      "voiceover": "欢迎来到本期视频，今天我们将讲解...",
      "duration": 5,
      "diagramType": "freeform"
    },
    {
      "id": "scene-2",
      "title": "核心概念",
      "voiceover": "首先让我们来看核心概念...",
      "duration": 10,
      "diagramType": "mindmap"
    },
    {
      "id": "scene-3",
      "title": "流程演示",
      "voiceover": "接下来是具体流程...",
      "duration": 15,
      "diagramType": "flowchart"
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 场景唯一标识，对应 excalidraw 文件名 |
| `title` | string | 是 | 场景标题 |
| `voiceover` | string | 否 | 语音文本 |
| `duration` | number | 是 | 场景时长（秒） |
| `diagramType` | string | 是 | 图表类型：flowchart/mindmap/hierarchy/relationship/comparison/timeline/matrix/freeform |

---

## 视频规格

### 输出格式

| 格式 | 编码 | 命令 |
|------|------|------|
| MP4 | H.264 | `npx remotion render ExcalidrawVideo out/video.mp4` |
| WebM | VP9 | `npx remotion render ExcalidrawVideo out/video.webm --codec=vp9` |

### 画布规格

- **分辨率**：1920 x 1080（16:9 横屏）
- **帧率**：30 fps
- **背景色**：#ffffff（白色）

### 替代规格（竖屏）

如需竖屏（9:16）：

```ts
export const VIDEO_CONFIG = {
  width: 1080,
  height: 1920,
  fps: 30,
  defaultDuration: 30,
} as const;
```

---

## 依赖安装

```bash
# 初始化项目
npm init -y

# 安装核心依赖
npm install remotion @remotion/player react react-dom

# 安装手绘渲染
npm install roughjs

# 安装开发依赖
npm install -D typescript @types/react @types/react-dom
```

---

## 开发工作流

### 1. 本地预览

```bash
npx remotion studio
```

访问 http://localhost:3000 预览视频。

### 2. 调整动画

修改 `ANIMATION_CONFIG` 或场景配置后自动刷新。

### 3. 渲染输出

```bash
# 单独格式
npm run build        # MP4
npm run build:webm   # WebM

# 全部格式
npm run build:all
```

---

## 语音文本脚本

语音文本脚本在 Phase 1 完成后立即生成，使用以下命令：

```bash
node scripts/generate-script.js storyboard.json video.script.md
```

输出格式：

```markdown
# 视频标题

## Scene: 开场 (0:00 - 0:05)

欢迎来到本期视频，今天我们将讲解...

## Scene: 核心概念 (0:05 - 0:15)

首先让我们来看核心概念...

## Scene: 流程演示 (0:15 - 0:30)

接下来是具体流程...

---

总时长: 60秒
```
