---
name: create-nano-banana
description: Nano Banana 图像生成API集成，支持多种模型(nano-banana-fast/pro)、自定义图片尺寸(1K/2K/4K)和比例。使用环境变量GRSAI_API_KEY配置API密钥。支持流式响应和结果轮询两种模式。当用户需要生成图像时触发此技能。
---

# Create Nano Banana

使用 Grsai 的 Nano Banana API 生成高质量图像。

## 快速开始

### 基础生成

```python
from scripts.nano_banana_api import NanoBananaAPI

api = NanoBananaAPI()
result = api.generate("一只可爱的猫咪在草地上玩耍")
print(result)
```

### 指定模型和尺寸

```python
result = api.generate(
    prompt="夕阳下的海滩",
    model="nano-banana-pro",
    aspect_ratio="16:9",
    image_size="2K"
)
```

### 使用参考图

```python
result = api.generate(
    prompt="生成类似的风景图",
    urls=["https://example.com/reference.png"]
)
```

## API Key 配置

在使用前设置环境变量：

```bash
export GRSAI_API_KEY="your-api-key-here"
```

或添加到 `~/.zshrc` 或 `~/.bashrc`：

```bash
echo 'export GRSAI_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

## 模型选择

| 模型 | 速度 | 质量 | 支持尺寸 | 适用场景 |
|------|------|------|----------|----------|
| nano-banana-fast | ⚡ | ⭐⭐ | 1K | 快速预览、批量测试 |
| nano-banana | ⚡⚡ | ⭐⭐⭐ | 1K | 日常使用、平衡之选 |
| nano-banana-pro | ⚢ | ⭐⭐⭐⭐ | 1K, 2K | 高质量创作 |
| nano-banana-pro-vt | ⚢ | ⭐⭐⭐⭐ | - | 视觉特效优化 |
| nano-banana-pro-cl | ⚢ | ⭐⭐⭐⭐ | 1K, 2K | 色彩增强 |
| nano-banana-pro-vip | ⚢ | ⭐⭐⭐⭐⭐ | 1K, 2K | 专业级质量 |
| nano-banana-pro-4k-vip | ⚣ | ⭐⭐⭐⭐⭐ | 4K | 超高清输出 |

## 核心参数

### model (必填)

模型名称，默认 `nano-banana-fast`

支持的值：
- `nano-banana-fast`
- `nano-banana`
- `nano-banana-pro`
- `nano-banana-pro-vt`
- `nano-banana-pro-cl`
- `nano-banana-pro-vip`
- `nano-banana-pro-4k-vip`

### prompt (必填)

图像生成的文本描述

### aspect_ratio (选填)

输出图像比例，默认 `auto`

支持的值：
- `auto` - 自动选择
- `1:1` - 正方形
- `16:9` - 宽屏
- `9:16` - 竖屏
- `4:3` - 传统
- `3:4` - 竖向
- `3:2`, `2:3` - 摄影标准
- `5:4`, `4:5` - 画框标准
- `21:9` - 超宽屏

### image_size (选填)

输出图像大小，默认 `1K`

支持的值：
- `1K` - 标准 (最快)
- `2K` - 高清
- `4K` - 超高清 (仅部分模型支持)

注意：分辨率越高，生成时间越长

### urls (选填)

参考图像URL或Base64字符串数组

示例：
```python
urls=["https://example.com/image.png"]
# 或
urls=["data:image/png;base64,iVBORw0KG..."]
```

## 响应模式

### 流式响应（默认）

实时获取生成进度和结果，适合交互式使用

```python
result = api.generate("海滩风景")
```

响应格式：
```json
{
  "id": "xxxxx",
  "results": [
    {
      "url": "https://example.com/image.png",
      "content": "这是一只可爱的猫咪在草地上玩耍"
    }
  ],
  "progress": 100,
  "status": "succeeded",
  "failure_reason": "",
  "error": ""
}
```

### 轮询模式

先获取任务ID，稍后查询结果，适合异步场景

```python
result = api.generate("海滩风景", webhook="-1")
task_id = result["data"]["id"]
print(f"任务ID: {task_id}")

# 稍后查询结果
result = api.poll_result(task_id)
```

响应格式：
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "id": "f44bcf50-f2d0-4c26-a467-26f2014a771b"
  }
}
```

## 错误处理

### 常见错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 0 | 成功 | - |
| -22 | 任务不存在 | 检查 task_id 是否正确 |
| 其他 | API 错误 | 查看错误详情 |

### failure_reason

| 原因 | 说明 | 解决方案 |
|------|------|----------|
| output_moderation | 输出违规 | 调整提示词，避免敏感内容 |
| input_moderation | 输入违规 | 检查提示词和参考图 |
| error | 其他错误 | 重新提交任务 |

## 完整示例

### 示例 1：基础生成

```python
from scripts.nano_banana_api import NanoBananaAPI

api = NanoBananaAPI()
result = api.generate("一只金毛犬在公园里奔跑")
print(result["results"][0]["url"])
```

### 示例 2：指定参数

```python
result = api.generate(
    prompt="赛博朋克城市的夜景",
    model="nano-banana-pro",
    aspect_ratio="21:9",
    image_size="2K"
)
```

### 示例 3：使用参考图

```python
result = api.generate(
    prompt="生成类似的梦幻森林",
    urls=["https://example.com/forest-reference.jpg"]
)
```

### 示例 4：轮询模式

```python
# 提交任务
submit_result = api.generate(
    prompt="宏伟的城堡",
    webhook="-1"
)
task_id = submit_result["data"]["id"]

# 等待完成并获取结果
final_result = api.poll_result(task_id)
print(final_result["data"]["results"][0]["url"])
```

### 示例 5：批量生成

```python
prompts = ["日出", "海滩", "山脉"]
results = []

for prompt in prompts:
    result = api.generate(prompt)
    results.append(result["results"][0]["url"])

print(results)
```

## 注意事项

- API Key 必须通过环境变量 `GRSAI_API_KEY` 设置
- 图片URL有效期为2小时，请及时下载
- 4K 分辨率生成时间较长，建议耐心等待
- 如遇 moderation 错误，请调整提示词内容
