#!/usr/bin/env python3
"""
Nano Banana API 客户端
用于调用 Grsai Nano Banana 图像生成 API
"""

import os
import time
import json
import requests
from typing import Dict, List, Optional, Union


class NanoBananaAPI:
    """Nano Banana API 客户端"""

    BASE_URL = "https://grsai.dakka.com.cn"
    DEFAULT_MODEL = "nano-banana-fast"

    # 支持的模型列表
    SUPPORTED_MODELS = [
        "nano-banana-fast",
        "nano-banana",
        "nano-banana-pro",
        "nano-banana-pro-vt",
        "nano-banana-pro-cl",
        "nano-banana-pro-vip",
        "nano-banana-pro-4k-vip",
    ]

    # 支持的宽高比
    SUPPORTED_ASPECT_RATIOS = [
        "auto",
        "1:1",
        "16:9",
        "9:16",
        "4:3",
        "3:4",
        "3:2",
        "2:3",
        "5:4",
        "4:5",
        "21:9",
    ]

    # 支持的图像尺寸
    SUPPORTED_IMAGE_SIZES = ["1K", "2K", "4K"]

    # 模型支持的尺寸
    MODEL_SIZE_SUPPORT = {
        "nano-banana-fast": ["1K"],
        "nano-banana": ["1K"],
        "nano-banana-pro": ["1K", "2K"],
        "nano-banana-pro-vt": [],
        "nano-banana-pro-cl": ["1K", "2K"],
        "nano-banana-pro-vip": ["1K", "2K"],
        "nano-banana-pro-4k-vip": ["4K"],
    }

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 API 客户端

        Args:
            api_key: API 密钥，默认从环境变量 GRSAI_API_KEY 读取
        """
        self.api_key = api_key or os.getenv("GRSAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API Key 未设置。请设置环境变量 GRSAI_API_KEY "
                "或在初始化时传入 api_key 参数"
            )

    def generate(
        self,
        prompt: str,
        model: str = "nano-banana-fast",
        aspect_ratio: str = "auto",
        image_size: str = "1K",
        urls: Optional[List[str]] = None,
        webhook: Optional[str] = None,
        progress: bool = True,
    ) -> Dict:
        """
        生成图像

        Args:
            prompt: 图像生成的文本描述
            model: 模型名称，默认 nano-banana-fast
            aspect_ratio: 图像比例，默认 auto
            image_size: 图像尺寸，默认 1K
            urls: 参考图URL或Base64字符串数组
            webhook: 回调URL，"-1" 表示轮询模式，None 表示流式响应
            progress: 是否显示进度，默认 True

        Returns:
            dict: 生成结果
        """
        # 验证参数
        self._validate_model(model)
        self._validate_aspect_ratio(aspect_ratio)
        self._validate_image_size(model, image_size)

        # 构建请求体
        payload = {
            "model": model,
            "prompt": prompt,
            "aspectRatio": aspect_ratio,
            "imageSize": image_size,
            "shutProgress": not progress,
        }

        if urls:
            payload["urls"] = urls

        if webhook is not None:
            payload["webHook"] = webhook

        # 发送请求
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        url = f"{self.BASE_URL}/v1/draw/nano-banana"

        try:
            response = requests.post(url, json=payload, headers=headers, stream=True)
            response.raise_for_status()

            # 如果设置 webhook="-1"，返回轮询模式结果
            if webhook == "-1" or webhook is not None:
                return response.json()

            # 流式响应：解析 SSE 格式
            final_result = None
            for line in response.iter_lines():
                if line:
                    line_str = line.decode("utf-8")
                    # SSE 格式: data: {json}
                    if line_str.startswith("data: "):
                        json_str = line_str[6:]  # 去掉 "data: " 前缀
                        try:
                            data = json.loads(json_str)
                            status = data.get("status")

                            # 打印进度
                            if status == "running" and progress:
                                p = data.get("progress", 0)
                                print(f"生成进度: {p}%", end="\r")

                            # 保存最后的结果
                            final_result = data

                            # 检查是否完成或失败
                            if status == "succeeded":
                                print()  # 新行
                                return final_result
                            elif status == "failed":
                                print()  # 新行
                                failure_reason = data.get("failure_reason", "unknown")
                                error = data.get("error", "unknown error")
                                raise Exception(
                                    f"任务失败: {failure_reason}, 详情: {error}"
                                )
                        except json.JSONDecodeError:
                            continue

            return final_result

        except requests.exceptions.RequestException as e:
            raise Exception(f"API 请求失败: {str(e)}")

    def poll_result(
        self, task_id: str, max_retries: int = 20, interval: int = 3
    ) -> Dict:
        """
        轮询任务结果

        Args:
            task_id: 任务ID
            max_retries: 最大重试次数，默认 20
            interval: 轮询间隔（秒），默认 3

        Returns:
            dict: 任务结果
        """
        url = f"{self.BASE_URL}/v1/draw/result"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(url, json={"id": task_id}, headers=headers)
                response.raise_for_status()
                result = response.json()

                # 检查任务状态
                if result.get("code") == 0:
                    data = result.get("data", {})
                    status = data.get("status")

                    if status == "succeeded":
                        return result
                    elif status == "failed":
                        failure_reason = data.get("failure_reason", "unknown")
                        error = data.get("error", "unknown error")
                        raise Exception(f"任务失败: {failure_reason}, 详情: {error}")
                    elif status == "running":
                        print(f"任务进行中... 进度: {data.get('progress', 0)}%")
                        time.sleep(interval)
                    else:
                        time.sleep(interval)
                else:
                    # 任务不存在或其他错误
                    error_msg = result.get("msg", "unknown error")
                    raise Exception(f"查询失败: {error_msg}")

            except requests.exceptions.RequestException as e:
                raise Exception(f"API 请求失败: {str(e)}")

        raise Exception(f"任务超时: 已尝试 {max_retries} 次")

    def _validate_model(self, model: str):
        """验证模型名称"""
        if model not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"不支持的模型: {model}。支持的模型: {', '.join(self.SUPPORTED_MODELS)}"
            )

    def _validate_aspect_ratio(self, aspect_ratio: str):
        """验证宽高比"""
        if aspect_ratio not in self.SUPPORTED_ASPECT_RATIOS:
            raise ValueError(
                f"不支持的宽高比: {aspect_ratio}。"
                f"支持的宽高比: {', '.join(self.SUPPORTED_ASPECT_RATIOS)}"
            )

    def _validate_image_size(self, model: str, image_size: str):
        """验证图像尺寸是否与模型兼容"""
        if image_size not in self.SUPPORTED_IMAGE_SIZES:
            raise ValueError(
                f"不支持的图像尺寸: {image_size}。"
                f"支持的尺寸: {', '.join(self.SUPPORTED_IMAGE_SIZES)}"
            )

        supported_sizes = self.MODEL_SIZE_SUPPORT.get(model, [])
        if image_size not in supported_sizes:
            raise ValueError(
                f"模型 {model} 不支持 {image_size} 尺寸。"
                f"支持的尺寸: {', '.join(supported_sizes) if supported_sizes else '无'}"
            )


def main():
    """命令行使用示例"""
    import argparse

    parser = argparse.ArgumentParser(description="Nano Banana 图像生成")
    parser.add_argument("prompt", help="图像生成提示词")
    parser.add_argument("--model", default="nano-banana-fast", help="模型名称")
    parser.add_argument("--aspect-ratio", default="auto", help="宽高比")
    parser.add_argument("--image-size", default="1K", help="图像尺寸")
    parser.add_argument("--webhook", help="轮询模式使用 -1")
    parser.add_argument("--task-id", help="查询任务结果")

    args = parser.parse_args()

    api = NanoBananaAPI()

    if args.task_id:
        result = api.poll_result(args.task_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        result = api.generate(
            prompt=args.prompt,
            model=args.model,
            aspect_ratio=args.aspect_ratio,
            image_size=args.image_size,
            webhook=args.webhook,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
