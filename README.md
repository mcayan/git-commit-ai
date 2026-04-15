# git-commit-ai

自动生成高质量 Git 提交信息的 CLI 工具。

读取 `git diff --staged` 的内容，发送给 LLM（OpenAI），自动生成符合 [Conventional Commits](https://www.conventionalcommits.org/) 规范的提交信息。

## 功能特性

- 自动读取暂存区的变更内容
- 调用 OpenAI API 智能生成提交信息
- 严格遵循 Conventional Commits 规范
- 支持中文/英文提交信息
- 支持提交前预览、编辑、重新生成
- 支持自定义 API 地址（兼容 DeepSeek 等第三方服务）

## 安装

### 全局安装（推荐，可在任意项目中使用）

安装后 `git-commit-ai` 会成为系统级命令，在任何 Git 仓库目录下都能直接调用。

#### 使用 uv tool（推荐）

```bash
# 从本地路径安装
uv tool install /path/to/git-commit-ai

# 或从 Git 仓库安装
git clone https://github.com/mcayan/git-commit-ai.git
uv tool install ./git-commit-ai
```

#### 使用 pipx（隔离环境）

```bash
pipx install /path/to/git-commit-ai
```

#### 使用 pip

```bash
pip install /path/to/git-commit-ai
```

### 开发模式安装（仅开发此项目时使用）

```bash
git clone https://github.com/mcayan/git-commit-ai.git
cd git-commit-ai

# uv 方式
uv sync

# 或 pip 方式
pip install -e .
```

### 卸载

```bash
# 如果使用 uv tool 安装的
uv tool uninstall git-commit-ai

# 如果使用 pipx 安装的
pipx uninstall git-commit-ai

# 如果使用 pip 安装的
pip uninstall git-commit-ai
```

## 配置

### 方式一：全局环境变量

在 `~/.zshrc` 或 `~/.bashrc` 中添加：

```bash
export OPENAI_API_KEY=sk-your-api-key-here
```

### 方式二：全局配置文件（推荐）

在用户主目录创建 `~/.git-commit-ai.env`，配置一次即可在所有项目中使用：

```bash
OPENAI_API_KEY=sk-your-api-key-here
# OPENAI_BASE_URL=https://api.deepseek.com/v1
# OPENAI_MODEL=gpt-4o-mini
```

### 方式三：项目级 .env 文件

在项目根目录创建 `.env` 文件（优先级高于全局配置）：

```bash
cp .env.example .env
vim .env
```

> **配置加载优先级：** 项目目录 `.env` > 用户主目录 `~/.git-commit-ai.env` > 环境变量

### 配置项说明

| 配置项 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `OPENAI_API_KEY` | 是 | - | OpenAI API Key |
| `OPENAI_BASE_URL` | 否 | OpenAI 官方地址 | 自定义 API 地址 |
| `OPENAI_MODEL` | 否 | `gpt-4o-mini` | 使用的模型名称 |

## 使用方法

> **注意：** 本工具只读取 Git 暂存区（staged）的变更，使用前请先执行 `git add` 将改动添加到暂存区。

### 基本用法

```bash
# 进入任意 Git 项目
cd /path/to/your-project

# 先暂存你的变更
git add .

# 运行工具，自动生成提交信息
git-commit-ai
```

### 命令行参数

```bash
# 指定模型
git-commit-ai --model gpt-4o

# 使用英文生成提交信息
git-commit-ai --lang en

# 跳过确认直接提交
git-commit-ai --yes

# 只生成不提交（预览模式）
git-commit-ai --dry-run
```

### 参数列表

| 参数 | 短参数 | 默认值 | 说明 |
|------|--------|--------|------|
| `--model` | `-m` | 配置文件中的值 | 指定 LLM 模型 |
| `--lang` | `-l` | `zh` | 输出语言（zh/en） |
| `--yes` | `-y` | `false` | 跳过确认直接提交 |
| `--dry-run` | - | `false` | 只生成不提交 |

### 交互流程

运行 `git-commit-ai` 后，工具会显示生成的提交信息，并提供以下选项：

- **`y`** - 确认并提交
- **`e`** - 编辑后再提交（会打开系统默认编辑器）
- **`r`** - 不满意？重新生成一条
- **`n`** - 取消操作

## Conventional Commits 规范

生成的提交信息遵循以下格式：

```
<type>(<scope>): <描述>

[可选的详细说明]
```

支持的 type 类型：

| Type | 含义 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档变更 |
| `style` | 代码格式调整 |
| `refactor` | 代码重构 |
| `test` | 测试相关 |
| `chore` | 构建、依赖等杂项 |
| `ci` | CI/CD 配置 |
| `perf` | 性能优化 |

## 使用第三方兼容服务

本工具支持任何兼容 OpenAI API 格式的服务，只需修改 `OPENAI_BASE_URL`：

```bash
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_API_KEY=your-deepseek-key
OPENAI_MODEL=deepseek-chat
```

## 许可证

MIT License
