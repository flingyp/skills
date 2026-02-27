# 视觉风格配置

浅米色手绘风格的完整视觉规范。

## 核心配色

### 背景色

```json
{
  "background": "#faf8f5"
}
```

用途：视频整体背景、画布底色

### 线条色

| 用途 | 色值 | 说明 |
|------|------|------|
| 主要线条 | `#2d3748` | 深灰蓝，模拟钢笔/铅笔 |
| 次要线条 | `#718096` | 中灰，辅助元素 |
| 强调线条 | `#c53030` | 砖红，重点标注 |

### 填充色

| 色值 | 语义 | 使用场景 |
|------|------|----------|
| `#e8f4f8` | 浅蓝 | 输入、数据源 |
| `#e8f5e9` | 浅绿 | 成功、输出 |
| `#fff3e0` | 浅橙 | 警告、待处理 |
| `#f3e5f5` | 浅紫 | 处理中、中间件 |
| `#ffebee` | 浅红 | 错误、关键 |
| `#fffde7` | 浅黄 | 备注、决策 |

### 文字色

| 用途 | 色值 | 字号范围 |
|------|------|----------|
| 标题 | `#1a202c` | 24-32px |
| 正文 | `#2d3748` | 16-20px |
| 注释 | `#718096` | 14-16px |
| 强调 | `#c53030` | 与正文同 |

## 字体规范

### Excalifont (fontFamily: 5)

所有文本统一使用手写字体：

```json
{
  "fontFamily": 5,
  "lineHeight": 1.25
}
```

### 字号规则

```json
{
  "title": { "fontSize": 28, "min": 24 },
  "subtitle": { "fontSize": 22, "min": 18 },
  "body": { "fontSize": 18, "min": 16 },
  "caption": { "fontSize": 14, "min": 12 }
}
```

**禁止低于 12px**

## 手绘效果

### Roughness 参数

```json
{
  "roughness": 1
}
```

- `0` - 平滑（不推荐）
- `1` - 轻微抖动（推荐）
- `2` - 明显抖动（可选）

### 线条样式

| 样式 | 值 | 用途 |
|------|------|------|
| 实线 | `"solid"` | 主要连接 |
| 虚线 | `"dashed"` | 可选路径 |
| 点线 | `"dotted"` | 弱关联 |

## 元素模板

### 矩形框

```json
{
  "type": "rectangle",
  "strokeColor": "#2d3748",
  "backgroundColor": "#e8f4f8",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roughness": 1,
  "roundness": { "type": 3 }
}
```

### 文本

```json
{
  "type": "text",
  "text": "显示文字",
  "fontSize": 18,
  "fontFamily": 5,
  "strokeColor": "#1a202c",
  "textAlign": "center",
  "lineHeight": 1.25
}
```

### 箭头

```json
{
  "type": "arrow",
  "strokeColor": "#2d3748",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "points": [[0, 0], [100, 0]]
}
```

### 椭圆

```json
{
  "type": "ellipse",
  "strokeColor": "#2d3748",
  "backgroundColor": "#fff3e0",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roughness": 1
}
```

## 动画顺序规范

为 Animated 模式设置合理的绘制顺序：

```json
{
  "customData": {
    "animate": {
      "order": 1,
      "duration": 500
    }
  }
}
```

### 推荐顺序

```
1. 标题/主题
2. 主要框架（矩形、椭圆）
3. 连接箭头
4. 节点标签
5. 补充说明
```

## 完整示例

### 简单概念图

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "id": "title-1",
      "type": "text",
      "x": 400, "y": 50,
      "text": "核心概念",
      "fontSize": 28,
      "fontFamily": 5,
      "strokeColor": "#1a202c",
      "customData": { "animate": { "order": 1, "duration": 500 } }
    },
    {
      "id": "box-1",
      "type": "rectangle",
      "x": 300, "y": 150,
      "width": 200, "height": 80,
      "strokeColor": "#2d3748",
      "backgroundColor": "#e8f4f8",
      "roughness": 1,
      "customData": { "animate": { "order": 2, "duration": 600 } }
    },
    {
      "id": "label-1",
      "type": "text",
      "x": 350, "y": 180,
      "text": "组件 A",
      "fontSize": 18,
      "fontFamily": 5,
      "strokeColor": "#2d3748",
      "customData": { "animate": { "order": 3, "duration": 400 } }
    }
  ],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#faf8f5"
  },
  "files": {}
}
```
