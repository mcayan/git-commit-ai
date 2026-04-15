"""CLI 入口模块

提供命令行交互界面，串联 git 操作、LLM 调用和用户确认流程。
"""

from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from git_commit_ai.config import load_config
from git_commit_ai.git import commit, get_staged_diff, get_staged_files, is_git_repo
from git_commit_ai.llm import generate_commit_message

# 初始化 Typer 应用和 Rich 控制台
app = typer.Typer(
    name="git-commit-ai",
    help="🤖 自动生成高质量 Git 提交信息",
    add_completion=False,
)
console = Console()


@app.command()
def main(
    model: Annotated[
        Optional[str],
        typer.Option("--model", "-m", help="指定 LLM 模型名称"),
    ] = None,
    lang: Annotated[
        str,
        typer.Option("--lang", "-l", help="输出语言: zh(中文) / en(英文)"),
    ] = "zh",
    yes: Annotated[
        bool,
        typer.Option("--yes", "-y", help="跳过确认直接提交"),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="只生成 commit message，不执行提交"),
    ] = False,
) -> None:
    """🤖 根据暂存区的变更自动生成 Git 提交信息"""

    # 加载配置
    load_config()

    # 检查是否在 Git 仓库中
    if not is_git_repo():
        console.print("❌ 当前目录不是 Git 仓库", style="bold red")
        raise typer.Exit(1)

    # 获取暂存区 diff
    console.print("📝 正在读取暂存区变更...", style="dim")
    diff = get_staged_diff()

    if not diff:
        console.print(
            "⚠️  暂存区没有变更内容，请先执行 [bold]git add[/bold] 添加文件",
            style="yellow",
        )
        raise typer.Exit(1)

    # 获取变更文件列表
    files = get_staged_files()
    console.print(f"📂 变更文件: [cyan]{', '.join(files)}[/cyan]")

    # 展示 diff 摘要
    diff_lines = diff.count("\n") + 1
    console.print(f"📊 diff 共 {diff_lines} 行\n", style="dim")

    # 调用 LLM 生成 commit message
    console.print("🤖 正在生成提交信息...", style="bold blue")
    message = generate_commit_message(diff, files, model=model, lang=lang)

    # 展示生成的 commit message
    console.print()
    console.print(
        Panel(
            Syntax(message, "text", theme="monokai", word_wrap=True),
            title="✨ 生成的提交信息",
            border_style="green",
            padding=(1, 2),
        )
    )

    # 如果是 dry-run 模式，只展示不提交
    if dry_run:
        console.print("\n🔍 [dim]dry-run 模式，不执行提交[/dim]")
        raise typer.Exit(0)

    # 确认或直接提交
    if yes:
        # 直接提交
        commit(message)
        console.print("\n✅ 提交成功！", style="bold green")
    else:
        # 交互式确认
        console.print()
        action = typer.prompt(
            "请选择操作: [y]提交 / [e]编辑后提交 / [r]重新生成 / [n]取消",
            default="y",
        )

        if action.lower() == "y":
            commit(message)
            console.print("\n✅ 提交成功！", style="bold green")
        elif action.lower() == "e":
            # 让用户编辑 commit message
            edited = typer.edit(message)
            if edited and edited.strip():
                commit(edited.strip())
                console.print("\n✅ 提交成功！", style="bold green")
            else:
                console.print("❌ 提交信息为空，已取消", style="red")
                raise typer.Exit(1)
        elif action.lower() == "r":
            # 重新生成
            console.print("\n🔄 正在重新生成...", style="bold blue")
            new_message = generate_commit_message(diff, files, model=model, lang=lang)
            console.print()
            console.print(
                Panel(
                    Syntax(new_message, "text", theme="monokai", word_wrap=True),
                    title="✨ 重新生成的提交信息",
                    border_style="green",
                    padding=(1, 2),
                )
            )
            confirm = typer.confirm("是否使用这条提交信息？")
            if confirm:
                commit(new_message)
                console.print("\n✅ 提交成功！", style="bold green")
            else:
                console.print("已取消", style="dim")
                raise typer.Exit(0)
        else:
            console.print("已取消", style="dim")
            raise typer.Exit(0)


if __name__ == "__main__":
    app()
