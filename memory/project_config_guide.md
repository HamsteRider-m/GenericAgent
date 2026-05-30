# Project Configuration Guide

> 详细的项目配置规范、命令参考和文件结构说明

---

## 1. `.gaproject` 配置文件

### 1.1 最小配置

```json
{
  "version": "1.0",
  "project_name": "my-project",
  "project_root": "."
}
```

### 1.2 完整配置

```json
{
  "version": "1.0",
  "project_name": "my-project",
  "project_root": ".",
  "temp_dir": ".ga_temp",
  "venv_path": ".venv",
  "build_command": "python -m build",
  "test_command": "pytest",
  "lint_command": "ruff check .",
  "ignore_patterns": [
    ".git/",
    ".ga_temp/",
    "__pycache__/",
    "node_modules/",
    "dist/",
    "build/"
  ],
  "context_files": [
    "README.md",
    "AGENTS.md",
    "PRD.md",
    "CURRENT.md"
  ],
  "custom_prompt": "",
  "env_file": ".env"
}
```

### 1.3 字段说明

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `version` | string | ✅ | 配置文件版本（当前 "1.0"） |
| `project_name` | string | ✅ | 项目名称（用于 UI 显示和 session 标识） |
| `project_root` | string | ✅ | 项目根目录（相对于 .gaproject 文件） |
| `temp_dir` | string | ❌ | 临时文件目录（默认 `.ga_temp`） |
| `venv_path` | string | ❌ | Python 虚拟环境路径 |
| `build_command` | string | ❌ | 构建命令 |
| `test_command` | string | ❌ | 测试命令 |
| `lint_command` | string | ❌ | 代码检查命令 |
| `ignore_patterns` | array | ❌ | 文件搜索时忽略的模式 |
| `context_files` | array | ❌ | 项目上下文文件（自动注入到系统 prompt） |
| `custom_prompt` | string | ❌ | 项目级自定义 prompt（类似 Cursor 的 .cursorrules） |
| `env_file` | string | ❌ | 环境变量文件路径 |

---

## 2. 命令行工具

### 2.1 `ga init` - 初始化项目

```bash
ga init [PROJECT_NAME] [--template TEMPLATE]
```

**功能**：
- 检测项目类型（Python/Node.js/Rust/Go 等）
- 生成 `.gaproject` 配置文件
- 创建 `.ga_temp/` 目录
- 初始化 Git 仓库（如果不存在）
- 创建 `docs` branch
- 生成初始 handoff.md
- 添加 `.gitignore` 规则

**模板类型**：
- `python`: Python 项目（检测 pyproject.toml / setup.py）
- `node`: Node.js 项目（检测 package.json）
- `rust`: Rust 项目（检测 Cargo.toml）
- `go`: Go 项目（检测 go.mod）
- `generic`: 通用项目

**示例**：
```bash
# 在当前目录初始化
ga init my-project

# 使用特定模板
ga init my-api --template python

# 在指定位置初始化
cd ~/Projects/GenericAgent/temp/internal/
ga init my-project
```

### 2.2 `ga project` - 项目管理

```bash
ga project list              # 列出最近项目
ga project switch <name>     # 切换到指定项目
ga project info              # 显示当前项目信息
ga project clean             # 清理临时文件
ga project remove <name>     # 从项目列表移除（不删除文件）
```

**示例**：
```bash
# 列出所有项目
ga project list

# 切换项目
ga project switch my-api

# 查看当前项目信息
ga project info

# 清理临时文件
ga project clean
```

### 2.3 `/project` - Session 内命令

```
/project info               # 显示当前项目配置
/project reload             # 重新加载项目配置
/project build              # 执行 build_command
/project test               # 执行 test_command
/project lint               # 执行 lint_command
```

---

## 3. 文件结构规范

### 3.1 项目根目录结构

```
my-project/
├── .gaproject              # 项目配置文件
├── .ga_temp/               # 临时文件目录
│   ├── sessions/           # session 级临时文件
│   ├── cache/              # 缓存文件
│   ├── logs/               # 日志文件
│   └── artifacts/          # 生成的产物
├── .git/                   # Git 仓库
├── .gitignore              # Git 忽略规则
├── README.md               # 项目说明
├── AGENTS.md               # AI Agent 协作指南（可选）
├── PRD.md                  # 产品需求文档（可选）
├── CURRENT.md              # 当前状态和待办（可选）
└── src/                    # 源代码目录
```

### 3.2 docs branch 结构

```
docs branch:
├── handoff.md              # 项目 handoff 文档
├── decisions/              # 设计决策记录
│   ├── 001-architecture.md
│   ├── 002-database.md
│   └── ...
└── evolution/              # 演化历史
    ├── v0.1.md
    ├── v0.2.md
    └── ...
```

### 3.3 临时文件管理

**原则**：所有临时文件必须放在项目的 `.ga_temp/` 目录下

**结构**：
```
.ga_temp/
├── sessions/           # session 级临时文件
│   └── <session_id>/
│       ├── scratch.py
│       └── temp_output.txt
├── cache/              # 缓存文件
│   ├── file_index.json
│   └── search_cache.db
├── logs/               # 日志文件
│   ├── session.log
│   └── error.log
└── artifacts/          # 生成的产物
    ├── diagrams/
    └── reports/
```

### 3.4 路径解析规则

1. **相对路径**：相对于项目根目录
   ```python
   "src/main.py"  # → {project_root}/src/main.py
   ```

2. **绝对路径**：保持不变
   ```python
   "/usr/local/bin/tool"  # → /usr/local/bin/tool
   ```

3. **`./` 前缀**：相对于当前 cwd
   ```python
   "./temp.txt"  # → {cwd}/temp.txt
   ```

4. **`~/` 前缀**：相对于用户 home 目录
   ```python
   "~/Documents/file.txt"  # → /Users/username/Documents/file.txt
   ```

---

## 4. 项目发现机制

### 4.1 自动发现规则

从当前目录向上查找，直到找到以下任一标志：

1. `.gaproject` 文件（最高优先级）
2. `.git/` 目录
3. `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod`
4. `.vscode/` / `.idea/` 目录

### 4.2 发现后行为

1. 读取 `.gaproject` 配置（如果存在）
2. 设置 `session.cwd` 为项目根目录
3. 创建 `temp_dir`（如果不存在）
4. 加载 `context_files` 到 session context
5. 应用 `custom_prompt`

### 4.3 未发现项目时

- 使用当前目录作为项目根目录
- 使用默认配置
- 提示用户是否初始化项目（`ga init`）

---

## 5. 配置优先级

**优先级顺序**（从高到低）：

1. **项目配置**：`.gaproject` 文件中的配置
2. **全局配置**：`~/.config/ga/config.json`
3. **默认值**：GA 内置默认值

**示例**：
```json
// 项目配置 (.gaproject)
{
  "temp_dir": ".ga_temp"  // 优先级最高
}

// 全局配置 (~/.config/ga/config.json)
{
  "temp_dir": ".ga_global_temp"  // 优先级次之
}

// 默认值
{
  "temp_dir": ".ga_temp"  // 优先级最低
}
```

---

## 6. Git 集成

### 6.1 Git 仓库要求

- **强烈建议**：项目应该是 git 仓库（便于版本控制、回滚、协作）
- **不强制**：允许非 git 项目（临时实验、学习项目等）

### 6.2 初始化行为

`ga init` 时：
1. 检测是否是 git 仓库
2. 如果不是，询问："This directory is not a git repository. Initialize git? (Y/n)"
3. 如果用户拒绝，继续初始化但给出警告："⚠️  Warning: Not a git repository. Version control is recommended."
4. 自动添加 `.ga_temp/` 到 `.gitignore`

### 6.3 .gitignore 规则

```gitignore
# GA 临时文件
.ga_temp/

# Python
__pycache__/
*.py[cod]
.venv/
.pytest_cache/

# Node.js
node_modules/
npm-debug.log

# 构建产物
dist/
build/
*.egg-info/
```

---

## 7. 环境变量

### 7.1 项目级环境变量

通过 `env_file` 字段指定：

```json
{
  "env_file": ".env"
}
```

### 7.2 .env 文件格式

```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Database
DATABASE_URL=postgresql://localhost/mydb

# 其他配置
DEBUG=true
LOG_LEVEL=info
```

### 7.3 加载行为

- GA 在加载项目时自动读取 `.env` 文件
- 环境变量仅在当前 session 有效
- 不会覆盖系统环境变量

---

## 8. 常见问题

### Q1: 如何修改项目配置？

直接编辑 `.gaproject` 文件，然后运行 `/project reload` 重新加载。

### Q2: 如何迁移现有项目？

```bash
cd existing-project
ga init  # 会检测现有文件并生成配置
```

### Q3: 如何清理临时文件？

```bash
ga project clean  # 清理 .ga_temp/ 目录
```

### Q4: 如何备份项目配置？

`.gaproject` 文件应该提交到 git，随项目一起版本控制。

---

**返回**：[← Project Lifecycle SOP](project_lifecycle_sop.md)

**版本**：v1.0  
**最后更新**：2026-05-30
