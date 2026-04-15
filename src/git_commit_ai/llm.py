"""LLM 调用模块

封装 OpenAI API 调用逻辑，发送 diff 内容并获取生成的 commit message。
"""

from openai import OpenAI

from git_commit_ai.config import get_api_key, get_base_url, get_model
from git_commit_ai.prompt import build_user_prompt, get_system_prompt


def generate_commit_message(
    diff: str,
    files: list[str],
    model: str | None = None,
    lang: str = "zh",
) -> str:
    """调用 LLM 生成 commit message

    Args:
        diff: git diff 内容
        files: 变更的文件列表
        model: 指定的模型名称，为 None 时使用配置中的默认模型
        lang: 输出语言，"zh" 中文（默认），"en" 英文

    Returns:
        生成的 commit message 字符串

    Raises:
        SystemExit: 如果 API 调用失败
    """
    # 初始化 OpenAI 客户端
    client = OpenAI(
        api_key=get_api_key(),
        base_url=get_base_url(),
    )

    # 获取实际使用的模型名称
    actual_model = get_model(model)

    # 构建提示词
    system_prompt = get_system_prompt(lang)
    user_prompt = build_user_prompt(diff, files)

    try:
        # 调用 OpenAI Chat Completions API
        response = client.chat.completions.create(
            model=actual_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,  # 较低的温度以获得更稳定的输出
            max_tokens=500,
        )

        # 提取生成的内容
        message = response.choices[0].message.content
        if not message:
            raise SystemExit("[错误] LLM 返回了空内容，请重试")

        # 清理输出：去除可能的多余引号和代码块标记
        message = message.strip().strip("`").strip('"').strip("'")

        # 如果返回被 ```  包裹，去掉它
        if message.startswith("```") and message.endswith("```"):
            message = message[3:-3].strip()

        return message

    except Exception as e:
        error_msg = str(e)
        # 提供友好的错误提示
        if "401" in error_msg or "Unauthorized" in error_msg:
            raise SystemExit("[错误] API Key 无效，请检查 OPENAI_API_KEY 配置") from e
        if "429" in error_msg or "rate_limit" in error_msg:
            raise SystemExit("[错误] API 请求频率超限，请稍后重试") from e
        if "timeout" in error_msg.lower():
            raise SystemExit("[错误] API 请求超时，请检查网络连接") from e
        raise SystemExit(f"[错误] LLM 调用失败: {error_msg}") from e
