"""Prompt 模板管理模块

管理发送给 LLM 的系统提示词和用户提示词模板。
"""

# 最大 diff 字符数限制，超过此长度会被截断以避免超出 token 限制
MAX_DIFF_LENGTH = 8000

# 系统提示词：定义 LLM 的角色和输出规范
SYSTEM_PROMPT_ZH = """你是一个经验丰富的高级开发工程师，擅长编写清晰、简洁的 Git 提交信息。

请严格遵循以下规则：
1. 必须遵循 Conventional Commits 规范。
2. 格式: <type>(<scope>): <描述>
3. <描述> 使用中文，简洁明了，不超过 50 个字。
4. type 使用英文小写，scope 用英文小写表示受影响的模块或文件。
5. 如果变更较复杂，请在主题行下方空一行后添加详细说明（body），body 也使用中文。
6. 仔细分析 diff 内容来确定最合适的 type。
7. 只输出 commit message 本身，不要输出任何解释、引号或代码块标记。

可用的 type 类型：
- feat: 新功能
- fix: Bug 修复
- docs: 文档变更
- style: 代码格式调整（不影响功能）
- refactor: 代码重构
- test: 测试相关
- chore: 构建、依赖、配置等杂项
- ci: CI/CD 配置
- perf: 性能优化
"""

SYSTEM_PROMPT_EN = """You are an expert senior developer who writes clear, concise git commit messages.

Rules:
1. Follow the Conventional Commits specification strictly.
2. Format: <type>(<scope>): <description>
3. The <description> must be in imperative mood, lowercase, no period at the end.
4. Keep the first line under 72 characters.
5. If the change is complex, add a body separated by a blank line.
6. Analyze the diff carefully to determine the most appropriate type.
7. The scope should reflect the module or area affected.
8. Only output the commit message itself. Do not include any explanation, quotes, or code block markers.

Available types: feat, fix, docs, style, refactor, test, chore, ci, perf
"""

# 用户提示词模板
USER_PROMPT_TEMPLATE = """请根据以下 git diff 内容生成一条 commit message：

变更的文件：{files}

```diff
{diff}
```"""


def get_system_prompt(lang: str = "zh") -> str:
    """获取系统提示词

    Args:
        lang: 语言，"zh" 中文（默认），"en" 英文

    Returns:
        系统提示词字符串
    """
    if lang == "en":
        return SYSTEM_PROMPT_EN
    return SYSTEM_PROMPT_ZH


def build_user_prompt(diff: str, files: list[str]) -> str:
    """构建用户提示词

    将 diff 内容填充到提示词模板中。如果 diff 超过最大长度限制，会进行截断处理。

    Args:
        diff: git diff 内容
        files: 变更的文件列表

    Returns:
        完整的用户提示词字符串
    """
    # 如果 diff 过长，截断并提示
    if len(diff) > MAX_DIFF_LENGTH:
        diff = diff[:MAX_DIFF_LENGTH] + "\n\n... [diff 内容过长，已截断] ..."

    files_str = ", ".join(files) if files else "未知"

    return USER_PROMPT_TEMPLATE.format(diff=diff, files=files_str)
