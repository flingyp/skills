# Nano Banana API 规范

本文档详细说明 Nano Banana API 的端点、参数和响应格式。

## 基础信息

- **基础地址**: `https://grsai.dakka.com.cn`
- **内容类型**: `application/json`
- **认证方式**: Bearer Token

## 接口端点

### 1. 生成图像

#### 端点

```
POST /v1/draw/nano-banana
```

#### 请求头

```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer {api_key}"
}
```

#### 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| model | string | 是 | - | 模型名称 |
| prompt | string | 是 | - | 图像生成提示词 |
| aspectRatio | string | 否 | auto | 输出图像比例 |
| imageSize | string | 否 | 1K | 输出图像大小 |
| urls | array | 否 | - | 参考图URL或Base64 |
| webHook | string | 否 | - | 回调URL，"-1"表示轮询 |
| shutProgress | boolean | 否 | false | 关闭进度回复 |

#### model 参数

支持的模型值：
- `nano-banana-fast` - 最快速度
- `nano-banana` - 标准速度
- `nano-banana-pro` - 高质量
- `nano-banana-pro-vt` - 视觉特效优化
- `nano-banana-pro-cl` - 色彩增强
- `nano-banana-pro-vip` - 专业级
- `nano-banana-pro-4k-vip` - 超高清

#### aspectRatio 参数

支持的值：
- `auto` - 自动选择
- `1:1` - 正方形
- `16:9` - 宽屏
- `9:16` - 竖屏
- `4:3`, `3:4` - 传统比例
- `3:2`, `2:3` - 摄影标准
- `5:4`, `4:5` - 画框标准
- `21:9` - 超宽屏

#### imageSize 参数

支持的值：
- `1K` - 标准分辨率（最快）
- `2K` - 高清分辨率
- `4K` - 超高清分辨率（仅部分模型支持）

#### urls 参数

参考图像数组，支持以下格式：
- HTTP/HTTPS URL：`["https://example.com/image.png"]`
- Base64 Data URL：`["data:image/png;base64,iVBORw0KG..."]`

#### webHook 参数

- 不设置或 `null`：流式响应，实时返回进度和结果
- `"-1"`：轮询模式，立即返回任务ID，通过结果接口查询

#### shutProgress 参数

- `false`：显示进度（配合 webHook 使用）
- `true`：隐藏进度，只返回最终结果

#### 响应格式（流式）

```json
{
  "id": "f44bcf50-f2d0-4c26-a467-26f2014a771b",
  "results": [
    {
      "url": "https://example.com/generated-image.jpg",
      "content": "这是一只可爱的猫咪在草地上玩耍"
    }
  ],
  "progress": 100,
  "status": "succeeded",
  "failure_reason": "",
  "error": ""
}
```

#### 响应参数说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 任务ID |
| results | array | 生成结果数组 |
| results[].url | string | 图片URL（有效期2小时） |
| results[].content | string | 生成内容描述 |
| progress | number | 任务进度（0-100） |
| status | string | 任务状态 |
| failure_reason | string | 失败原因 |
| error | string | 错误详细信息 |

#### status 字段

- `running` - 进行中
- `succeeded` - 成功
- `failed` - 失败

#### failure_reason 字段

- `output_moderation` - 输出违规
- `input_moderation` - 输入违规
- `error` - 其他错误

#### 响应格式（轮询）

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "id": "f44bcf50-f2d0-4c26-a467-26f2014a771b"
  }
}
```

### 2. 获取结果

#### 端点

```
POST /v1/draw/result
```

#### 请求头

```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer {api_key}"
}
```

#### 请求参数

```json
{
  "id": "task-id-here"
}
```

#### 响应格式

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "id": "f44bcf50-f2d0-4c26-a467-26f2014a771b",
    "results": [
      {
        "url": "https://example.com/generated-image.jpg",
        "content": "这是一只可爱的猫咪在草地上玩耍"
      }
    ],
    "progress": 100,
    "status": "succeeded",
    "failure_reason": "",
    "error": ""
  }
}
```

#### code 字段

- `0` - 成功
- `-22` - 任务不存在
- 其他 - 其他错误

## Gemini 官方格式兼容

API 支持 Gemini 官方接口格式：

**基础地址替换为 Grsai 地址**，模型名称 `gemini-2.5-flash-image` 改为 `nano-banana-fast`

#### 端点示例

```
POST /v1beta/models/nano-banana-fast:streamGenerateContent
```

## 模型与尺寸兼容性

| 模型 | 支持 imageSize |
|------|----------------|
| nano-banana-fast | 1K |
| nano-banana | 1K |
| nano-banana-pro | 1K, 2K |
| nano-banana-pro-vt | 无 |
| nano-banana-pro-cl | 1K, 2K |
| nano-banana-pro-vip | 1K, 2K |
| nano-banana-pro-4k-vip | 4K |

## 注意事项

- 图片 URL 有效期为 2 小时
- 4K 分辨率生成时间较长
- 分辨率越高，生成时间越长
- 当触发 `error` 时，可尝试重新提交任务
- 输入验证失败会返回 422 状态码
- 认证失败会返回 401 状态码
