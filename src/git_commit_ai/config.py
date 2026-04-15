"""配置管理模块

从环境变量和 .env 文件中读取配置项，包括 OpenAI API Key、模型名称等。
"""

import os
from pathlib import Path

from dotenv import load_dotenv


def load_config() -> None:
    """加载 .env 配置文件

    按优先级依次查找：当前目录 .env → 用户主目录 ~/.git-commit-ai.env
    """
    # 优先加载当前目录下的 .env
    local_env = Path.cwd() / ".env"
    if local_env.exists():
        load_dotenv(local_env)
        return

    # 其次加载用户主目录下的全局配置
    global_env = Path.home() / ".git-commit-ai.env"
    if global_env.exists():
        load_dotenv(global_env)
        return

    # 兜底：尝试加载默认的 .env
    load_dotenv()


def get_api_key() -> str:
    """获取 OpenAI API Key

    Returns:
        API Key 字符串

    Raises:
        SystemExit: 如果未配置 API Key
    """
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise SystemExit(
            "[错误] 未找到 OPENAI_API_KEY，请通过以下方式之一配置：\n"
            "   1. 设置环境变量: export OPENAI_API_KEY=sk-xxx\n"
            "   2. 在项目目录创建 .env 文件: OPENAI_API_KEY=sk-xxx\n"
            "   3. 在主目录创建 ~/.git-commit-ai.env 文件"
        )
    return api_key


def get_base_url() -> str | None:
    """获取 OpenAI API 的 Base URL（可选）

    支持自定义 API 地址，方便接入兼容 OpenAI 格式的第三方服务（如 DeepSeek）。

    Returns:
        Base URL 字符串，未配置时返回 None（使用 OpenAI 官方地址）
    """
    return os.getenv("OPENAI_BASE_URL") or None


def get_model(override: str | None = None) -> str:
    """获取要使用的模型名称

    Args:
        override: CLI 传入的模型名称，优先级最高

    Returns:
        模型名称字符串
    """
    if override:
        return override
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")
