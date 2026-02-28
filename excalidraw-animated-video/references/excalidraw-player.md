# ExcalidrawPlayer 组件开发指南

ExcalidrawPlayer 是渲染 Excalidraw 元素的核心组件。

## 基本用法

```tsx
import { ExcalidrawPlayer } from "./components/ExcalidrawPlayer";
import excalidrawData from "./excalidraw/scene-1.json";

<ExcalidrawPlayer 
  elements={excalidrawData.elements} 
/>
```

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `elements` | `ExcalidrawElement[]` | Yes | Excalidraw 元素数组 |
| `currentSceneFrame` | `number` | No | 当前场景的起始帧，默认 0 |

## 动画控制

### 动画顺序 (order)

元素通过 `customData.animate.order` 控制出现顺序：

```json
{
  "id": "title-1",
  "type": "text",
  "customData": {
    "animate": {
      "order": 1,
      "duration": 500
    }
  }
}
```

### 动画时长 (duration)

`duration` 单位为毫秒，控制绘制动画的时长。

## 支持的元素类型

| Type | 渲染方式 | 动画效果 |
|------|----------|----------|
| `rectangle` | SVG + roughjs | 逐帧绘制 |
| `ellipse` | SVG + roughjs | 逐帧绘制 |
| `diamond` | SVG + roughjs | 逐帧绘制 |
| `arrow` | SVG path | strokeDashoffset 动画 |
| `line` | SVG path | strokeDashoffset 动画 |
| `text` | SVG text | 淡入 |

## 样式配置

### 字体

文本元素使用 Excalifont (fontFamily: 5)，在 CSS 中映射为：

```css
font-family: "Caveat", "Segoe UI Emoji", sans-serif;
```

需要在项目中引入 Google Fonts：

```html
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&display=swap" rel="stylesheet">
```

### 颜色

参考 `src/config.ts` 中的 `COLORS` 常量：

```ts
export const COLORS = {
  stroke: "#1e1e1e",
  fill: {
    blue: "#a5d8ff",
    green: "#b2f2bb",
    // ...
  },
  text: {
    title: "#1e40af",
    body: "#374151",
    // ...
  },
};
```

## 扩展：自定义元素渲染

添加新的元素类型渲染器：

```tsx
// 在 ExcalidrawPlayer.tsx 中添加
case "freedraw":
  return (
    <FreedrawRenderer
      key={element.id}
      element={element as FreedrawElement}
      opacity={opacity}
      drawProgress={drawProgress}
    />
  );
```

## 性能优化

1. **元素排序缓存**：使用 `useMemo` 缓存排序后的元素
2. **动画组合**：相同 order 的元素共享动画时机
3. **SVG 优化**：避免重复创建 roughjs 实例

## 示例：完整渲染流程

```tsx
// 1. 加载 Excalidraw JSON
const sceneData = require("./excalidraw/scene-1.excalidraw");

// 2. 传递给 ExcalidrawPlayer
<ExcalidrawPlayer 
  elements={sceneData.elements}
  currentSceneFrame={0}
/>

// 3. 动画自动执行
// order=1 的元素在第 0 帧开始出现
// order=2 的元素在第 15 帧开始出现 (staggerDelay * 3)
// 以此类推...
```
