---
name: excalidraw-animated-video
description: |
  生成手绘风格的 Excalidraw 动画讲解视频。结合 excalidraw-diagram 和 remotion-best-practices skills。
  
  触发场景：
  - 用户说"生成动画讲解视频"、"手绘动画视频"、"Excalidraw 视频教程"
  - 需要将概念图/流程图/架构图转换为动态演示视频
  - 需要制作教学、产品演示、技术讲解类短视频
  
  输出：MP4 + WebM 视频文件，语音文本脚本在 Phase 1 完成后立即生成
metadata:
  tags: excalidraw, remotion, video, animation, 手绘风格, 教学视频
  dependencies:
    - excalidraw-diagram
    - remotion-best-practices
---

# Excalidraw Animated Video

将文本内容转换为手绘风格动画讲解视频。

## 工作流程

```
用户输入主题/脚本
       │
       ▼
┌─────────────────────┐
│ Phase 1: 内容规划    │  生成分镜脚本 + 语音文本脚本
└─────────────────────┘
       │
       ▼
┌─────────────────────┐
│ Phase 2: 图表生成    │  调用 excalidraw-diagram (Animated 模式)
└─────────────────────┘
       │
       ▼
┌─────────────────────┐
│ Phase 3: 项目构建    │  从模板创建 Remotion 项目
└─────────────────────┘
       │
       ▼
┌─────────────────────┐
│ Phase 4: 视频渲染    │  输出 MP4 + WebM
└─────────────────────┘
```

---

## Phase 1: 内容规划

分析用户输入，生成结构化的分镜脚本。

### 输出文件

```json
// storyboard.json
{
  "title": "视频标题",
  "duration": 60,
  "scenes": [
    {
      "id": "scene-1",
      "title": "开场",
      "voiceover": "欢迎来到本期视频...",
      "duration": 5,
      "diagramType": "freeform"
    }
  ]
}
```

### 分镜设计原则

- 单个视频建议 3-10 个镜头
- 每个镜头 3-15 秒
- 每个镜头聚焦一个核心概念
- 为每个镜头生成语音讲解文本

### 生成语音文本脚本

Phase 1 完成后，立即生成语音文本脚本：

```bash
node scripts/generate-script.js storyboard.json out/{name}.script.md
```

输出示例：

```markdown
# 视频标题

## Scene: 开场 (0:00 - 0:05)

欢迎来到本期视频...

## Scene: 核心概念 (0:05 - 0:15)

首先让我们来看核心概念...

---

总时长: 60秒
```

---

## Phase 2: Excalidraw 图表生成

调用 `excalidraw-diagram` skill 生成带动画标记的图表。

### 关键配置

1. **使用 Animated 模式**：触发词使用 `Excalidraw动画` 或 `animate`
2. **动画顺序设置**：
   - 标题：order = 1
   - 主要框架：order = 2-4
   - 连接线/箭头：order = 5-7
   - 细节文字：order = 8-10

### 画布规格

- **尺寸**：1920 x 1080（16:9 横屏）
- **元素范围**：四周留 80px padding
- **字体**：fontFamily: 5（Excalifont）

### 输出文件

```
{project}/
├── excalidraw/
│   ├── scene-1.excalidraw
│   ├── scene-2.excalidraw
│   └── ...
└── storyboard.json
```

---

## Phase 3: Remotion 项目构建

从模板创建项目并配置 Composition。

### 项目初始化

```bash
# 从模板复制
cp -r assets/template/ {project-name}/
cd {project-name}
npm install
```

### Composition 配置

```tsx
// src/Root.tsx
<Composition
  id="ExcalidrawVideo"
  component={ExcalidrawVideo}
  durationInFrames={900}  // 30秒 @ 30fps
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{
    scenes: [
      { id: "scene-1", excalidrawFile: "scene-1.excalidraw" }
    ]
  }}
/>
```

### 核心组件

| 组件 | 功能 | 文档 |
|------|------|------|
| `ExcalidrawPlayer` | 渲染 Excalidraw 元素 | [excalidraw-player.md](references/excalidraw-player.md) |
| `HandDrawAnimation` | 手绘效果动画 | [animation-presets.md](references/animation-presets.md) |
| `SceneComposer` | 多场景组合 | [animation-presets.md](references/animation-presets.md) |

---

## Phase 4: 视频渲染

### 预览

```bash
npx remotion preview
```

### 渲染输出

```bash
# MP4
npx remotion render ExcalidrawVideo out/video.mp4

# WebM
npx remotion render ExcalidrawVideo out/video.webm --codec=vp9
```

### 输出文件清单

```
out/
├── {name}.mp4          # H.264 编码
└── {name}.webm         # VP9 编码

{project}/
└── {name}.script.md    # 语音文本脚本 (Phase 1 生成)
```

---

## 详细文档

- [excalidraw-player.md](references/excalidraw-player.md) - ExcalidrawPlayer 组件开发指南
- [animation-presets.md](references/animation-presets.md) - 动画预设库
- [project-config.md](references/project-config.md) - 项目配置规范

---

## 依赖 Skills

使用此 skill 时会自动调用：

1. **excalidraw-diagram** - 生成带动画标记的 Excalidraw 图表
2. **remotion-best-practices** - Remotion 开发最佳实践

加载依赖 skill 获取详细指导：

```
load skill: excalidraw-diagram
load skill: remotion-best-practices
```
