---
name: excalidraw-video-maker
description: 生成浅米色手绘风格的 Excalidraw 动画讲解视频。当用户需要创建概念讲解、流程演示、知识可视化等手绘风动画视频时触发。支持技术讲解、业务流程、教育培训、产品演示等场景。用户只需提供主题或内容，自动生成完整的 Remotion 视频项目代码。
---

# Excalidraw Video Maker

生成浅米色手绘风格的讲解动画视频，用户只需提供主题或内容，自动完成内容解析、场景规划、图表生成、Remotion 项目输出。

## 视觉风格

固定使用浅米色手绘风：

| 元素 | 配置 |
|------|------|
| 背景 | `#faf8f5` 浅米色 |
| 主线条 | `#2d3748` 深灰蓝 |
| 文字 | `#1a202c` 近黑 |
| 强调色 | `#c53030` 砖红 / `#2b6cb0` 深蓝 / `#38a169` 绿 |
| 字体 | `fontFamily: 5` Excalifont |
| 抖动 | `roughness: 1` |

## 工作流程

```
用户输入主题/内容
       │
       ▼
┌──────────────────┐
│ 1. 内容解析      │ → 提取核心概念、关系、层级
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ 2. 场景规划      │ → 拆分场景、确定时长、选择图表类型
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ 3. 配音文本生成  │ → 为每个场景生成配音文本（JSON 格式）
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ 4. 图表生成      │ → Excalidraw Animated 模式，设置动画顺序
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ 5. Remotion 项目 │ → 完整项目代码，集成图表、过渡效果
└──────────────────┘
```

## 详细参考

- 内容解析规则：见 [references/content-analysis.md](references/content-analysis.md)
- 场景规划模式：见 [references/scene-planning.md](references/scene-planning.md)
- 配音文本指南：见 [references/narration-guide.md](references/narration-guide.md)
- 视觉风格配置：见 [references/visual-style.md](references/visual-style.md)
- Remotion 项目模板：见 [references/remotion-template.md](references/remotion-template.md)

## 依赖 Skills

此 skill 依赖以下技能，使用时自动加载：

- `excalidraw-diagram` - 生成 Excalidraw 图表（Animated 模式）
- `remotion-best-practices` - Remotion 视频项目最佳实践

## 输出物

每次生成包含：

1. **配音文本文件** - `narration.json` 格式，每个场景对应一段配音
2. **Excalidraw 图表文件** - `.excalidraw` 格式，带动画顺序
3. **Remotion 项目代码** - 完整可运行的 React 项目
4. **渲染命令** - `npx remotion render` 指令

## 使用示例

```
用户: 生成一个关于 REST API 工作原理的手绘讲解视频

输出:
- narration.json (配音文本)
- scenes/api-flow.excalidraw (动画图表)
- remotion-project/ (完整项目)
- 渲染命令: npx remotion render src/index.ts RESTApiVideo out/video.mp4
```
