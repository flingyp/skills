# 场景规划模式

根据解析后的内容，规划视频的场景结构和动画时序。

## 图表类型选择

根据内容特征自动选择：

| 内容特征 | 图表类型 | 适用场景 |
|----------|----------|----------|
| 步骤序列 | 流程图 Flowchart | 工作流、操作步骤、数据流 |
| 概念发散 | 思维导图 Mind Map | 知识结构、主题拆解 |
| 层级关系 | 层级图 Hierarchy | 组织架构、分类体系 |
| 因素关联 | 关系图 Relationship | 系统交互、依赖关系 |
| 方案对比 | 对比图 Comparison | 优劣分析、版本差异 |
| 时间演进 | 时间线 Timeline | 发展历程、项目进度 |
| 双维度分类 | 矩阵图 Matrix | 优先级、象限分析 |

## 场景模板

### 开场场景

```
元素：
  - 主标题（居中，大字）
  - 副标题/引导语（可选）

动画顺序：
  order: 1 → 主标题淡入
  order: 2 → 副标题淡入

时长：5-8 秒
```

### 概念讲解场景

```
元素：
  - 场景标题
  - 核心图形（矩形/椭圆）
  - 说明文字
  - 连接关系（箭头）

动画顺序：
  order: 1 → 标题
  order: 2 → 主要图形
  order: 3 → 次要图形
  order: 4 → 连接箭头
  order: 5 → 说明文字

时长：8-15 秒
```

### 流程演示场景

```
元素：
  - 步骤节点（横向/纵向排列）
  - 流程箭头
  - 步骤编号
  - 简短说明

动画顺序：
  order: 1 → 步骤1
  order: 2 → 箭头1→2
  order: 3 → 步骤2
  ...依次类推

时长：10-15 秒
```

### 对比分析场景

```
元素：
  - 对比标题
  - 左右两栏框架
  - 各自要点
  - 对比指示

动画顺序：
  order: 1 → 标题
  order: 2 → 左侧框架
  order: 3 → 右侧框架
  order: 4 → 左侧要点
  order: 5 → 右侧要点
  order: 6 → 对比连线/标签

时长：10-15 秒
```

### 结尾场景

```
元素：
  - 总结标题
  - 核心要点回顾（3-5 条）
  - 行动建议/结尾语

动画顺序：
  order: 1 → 总结标题
  order: 2-4 → 要点依次出现
  order: 5 → 结尾语

时长：5-8 秒
```

## 时序计算

### 基础参数

```typescript
const FPS = 30; // 帧率
const BASE_DURATION = {
  title: 5 * FPS,      // 5秒
  concept: 10 * FPS,   // 10秒
  flow: 12 * FPS,      // 12秒
  summary: 6 * FPS,    // 6秒
};
```

### 配音时长计算

配音文本长度需与场景时长匹配：

| 场景类型 | 建议时长 | 建议字数 | 计算规则 |
|----------|----------|----------|----------|
| 开场 | 5-8s | 15-25 字 | 时长(秒) × 3 = 最大字数 |
| 概念 | 8-15s | 25-45 字 | 时长(秒) × 3 = 最大字数 |
| 流程 | 10-15s | 30-50 字 | 时长(秒) × 3 = 最大字数 |
| 结尾 | 5-8s | 15-25 字 | 时长(秒) × 3 = 最大字数 |

**语速参考：** 中文正常语速约 2.5-3 字/秒，预留呼吸停顿空间。

### 过渡时长

```typescript
const TRANSITION = {
  fadeIn: 15,    // 0.5秒
  fadeOut: 15,   // 0.5秒
  slide: 20,     // 0.67秒
};
```

### 总时长计算

```
总帧数 = Σ(场景时长) - Σ(过渡时长)
       = 开场 + 主体场景们 + 结尾 - 过渡次数 × 过渡时长
```

## 场景连接策略

### 过渡效果选择

| 场景切换类型 | 推荐过渡 | 效果 |
|--------------|----------|------|
| 开场 → 主体 | fade | 柔和进入 |
| 概念间切换 | slide | 方向感 |
| 流程步骤 | fade | 连贯性 |
| 主体 → 结尾 | fade | 平稳收尾 |

### Remotion 实现示例

```tsx
<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={150}>
    <IntroScene />
  </TransitionSeries.Sequence>
  
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 15 })}
  />
  
  <TransitionSeries.Sequence durationInFrames={300}>
    <MainScene />
  </TransitionSeries.Sequence>
  
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 15 })}
  />
  
  <TransitionSeries.Sequence durationInFrames={180}>
    <OutroScene />
  </TransitionSeries.Sequence>
</TransitionSeries>
```
