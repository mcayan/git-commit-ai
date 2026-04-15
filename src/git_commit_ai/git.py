"""Git 操作封装模块

提供 git diff、git commit 等操作的 Python 封装。
"""

import subprocess


def is_git_repo() -> bool:
    """检查当前目录是否为 Git 仓库

    Returns:
        如果当前目录在 Git 仓库内则返回 True
    """
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            check=True,
            text=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_staged_diff() -> str:
    """获取暂存区的 diff 内容

    执行 `git diff --staged` 获取已暂存的变更内容。

    Returns:
        diff 内容字符串，如果没有暂存内容则返回空字符串

    Raises:
        SystemExit: 如果执行 git 命令失败
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--staged"],
            capture_output=True,
            check=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise SystemExit(f"[错误] 获取 git diff 失败: {e.stderr}") from e


def get_staged_files() -> list[str]:
    """获取暂存区的文件列表

    Returns:
        暂存区中的文件路径列表
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--staged", "--name-only"],
            capture_output=True,
            check=True,
            text=True,
        )
        return [f for f in result.stdout.strip().split("\n") if f]
    except subprocess.CalledProcessError:
        return []


def commit(message: str) -> bool:
    """执行 git commit

    Args:
        message: 提交信息

    Returns:
        提交是否成功

    Raises:
        SystemExit: 如果提交失败
    """
    try:
        subprocess.run(
            ["git", "commit", "-m", message],
            check=True,
            text=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        raise SystemExit(f"[错误] git commit 执行失败: {e}") from e
