# Project Best Practices

> 最佳实践、避坑指南和典型场景

---

## 1. 最佳实践

### 1.1 项目组织

**✅ DO**：
- 使用标准位置：`~/Projects/GenericAgent/temp/internal/`
- 一个项目一个独立的 Git 仓库
- 使用 `.gaproject` 声明项目配置
- 临时文件统一放在 `.ga_temp/`

**❌ DON'T**：
- 不要在 `~/Projects/GenericAgent/temp/` 根目录创建项目（会污染临时目录）
- 不要在项目外创建临时文件（难以清理）
- 不要手动管理项目列表（让 GA 自动发现）

### 1.2 配置管理

**✅ DO**：
- 提交 `.gaproject` 到 Git（团队共享配置）
- 使用 `.env` 文件管理环境变量
- 在 `.gitignore` 中排除 `.ga_temp/` 和 `.env`
- 使用 `custom_prompt` 定制项目级 AI 行为

**❌ DON'T**：
- 不要在 `.gaproject` 中硬编码绝对路径
- 不要提交 `.env` 文件到 Git（包含密钥）
- 不要在 `custom_prompt` 中包含敏感信息

### 1.3 Handoff 管理

**✅ DO**：
- 在重要决策时更新 handoff
- 使用结构化格式（任务 → 当前状态 → 下一步 → 开放问题）
- 记录"为什么"而不是"是什么"
- 定期回顾和精简 handoff

**❌ DON'T**：
- 不要把 handoff 当作代码注释（代码已经说明了实现）
- 不要在 handoff 中记录临时想法（使用 session notes）
- 不要让 handoff 过时（定期更新）

### 1.4 docs branch 管理

**✅ DO**：
- 永远不要合并 docs branch 到 main
- 使用 `git checkout docs` 切换分支
- 提交时使用 `docs:` 前缀（如 `docs: update handoff v0.2`）
- 保持 docs branch 的线性历史

**❌ DON'T**：
- 不要在 main branch 修改 handoff.md
- 不要使用 `git merge` 合并 docs branch
- 不要在 docs branch 修改代码文件

---

## 2. 避坑指南

### 2.1 常见错误

#### 错误 1：GA 未发现项目

**症状**：
```
$ cd my-project
$ /project info
Error: No project loaded
```

**原因**：
- 缺少 `.gaproject` 文件
- `.gaproject` 格式错误（JSON 语法错误）
- 项目目录不在 GA 的搜索路径中

**解决方案**：
```bash
# 检查 .gaproject 是否存在
ls -la .gaproject

# 验证 JSON 格式
cat .gaproject | python -m json.tool

# 重新初始化
ga init
```

#### 错误 2：路径解析错误

**症状**：
```
FileNotFoundError: [Errno 2] No such file or directory: 'src/main.py'
```

**原因**：
- `project_root` 配置错误
- 相对路径基于错误的目录

**解决方案**：
```json
// .gaproject
{
  "project_root": "."  // 确保是相对于 .gaproject 的路径
}
```

#### 错误 3：临时文件污染

**症状**：
```
$ git status
Untracked files:
  temp_output.txt
  scratch.py
  debug.log
```

**原因**：
- 临时文件创建在项目根目录
- `.ga_temp/` 未添加到 `.gitignore`

**解决方案**：
```bash
# 移动临时文件到 .ga_temp/
mv temp_output.txt .ga_temp/

# 添加到 .gitignore
echo ".ga_temp/" >> .gitignore
```

#### 错误 4：docs branch 冲突

**症状**：
```
$ git checkout docs
error: Your local changes to the following files would be overwritten by checkout:
  handoff.md
```

**原因**：
- 在 main branch 修改了 handoff.md
- 尝试合并 docs branch 到 main

**解决方案**：
```bash
# 永远不要在 main branch 修改 handoff.md
git checkout main
git checkout -- handoff.md  # 撤销修改

# 切换到 docs branch 再修改
git checkout docs
vim handoff.md
git commit -m "docs: update handoff"
git checkout main
```

#### 错误 5：配置优先级混乱

**症状**：
```
项目配置未生效，使用了全局配置
```

**原因**：
- 不理解配置优先级
- 项目配置被全局配置覆盖

**解决方案**：
```
优先级顺序（从高到低）：
1. 项目配置 (.gaproject)
2. 全局配置 (~/.config/ga/config.json)
3. 默认值

确保项目配置存在且格式正确
```

### 2.2 性能陷阱

#### 陷阱 1：过大的 context_files

**问题**：
```json
{
  "context_files": [
    "README.md",
    "docs/api.md",
    "docs/architecture.md",
    "docs/database.md",
    "docs/deployment.md",
    "docs/troubleshooting.md"
  ]
}
```

**影响**：
- Session 启动变慢
- 上下文窗口被占用

**解决方案**：
```json
{
  "context_files": [
    "README.md",
    "AGENTS.md"  // 只包含最核心的文件
  ]
}
```

#### 陷阱 2：过多的 ignore_patterns

**问题**：
```json
{
  "ignore_patterns": [
    ".git/", ".ga_temp/", "__pycache__/", "node_modules/",
    "dist/", "build/", "*.pyc", "*.pyo", "*.pyd", "*.so",
    "*.dylib", "*.dll", "*.egg-info/", ".pytest_cache/",
    ".mypy_cache/", ".ruff_cache/", ".coverage", "htmlcov/"
  ]
}
```

**影响**：
- 文件搜索变慢（需要匹配大量模式）

**解决方案**：
```json
{
  "ignore_patterns": [
    ".git/",
    ".ga_temp/",
    "__pycache__/",
    "node_modules/",
    "dist/",
    "build/"
  ]  // 只包含最常见的目录
}
```

---

## 3. 典型场景

### 场景 1：创建新的 Python 项目

```bash
# 1. 进入标准位置
cd ~/Projects/GenericAgent/temp/internal/

# 2. 初始化项目
ga init my-api --template python

# 3. 进入项目
cd my-api

# 4. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate

# 5. 安装依赖
pip install fastapi uvicorn pytest

# 6. 开始开发
vim src/main.py

# 7. 运行测试
/project test

# 8. 更新 handoff
git checkout docs
vim handoff.md
git commit -m "docs: add API design"
git checkout main
```

### 场景 2：接入现有项目

```bash
# 1. 克隆现有项目
cd ~/Projects/GenericAgent/temp/internal/
git clone https://github.com/user/existing-project.git
cd existing-project

# 2. 初始化 GA 项目
ga init

# 3. GA 自动检测项目类型并生成配置
# 检查生成的 .gaproject
cat .gaproject

# 4. 创建 docs branch（如果不存在）
git checkout -b docs
cat > handoff.md << 'EOF'
# Existing Project Handoff

## 当前状态
- 已接入 GA 项目管理
- 正在熟悉代码库

## 下一步
- 阅读 README 和文档
- 运行测试验证环境
- 识别技术债务

## 开放问题
- 项目的主要痛点是什么？
- 有哪些待优化的地方？
EOF
git add handoff.md
git commit -m "docs: initial handoff"
git checkout main

# 5. 开始工作
/project test
/project lint
```

### 场景 3：多项目并行开发

```bash
# 1. 列出所有项目
ga project list

# 输出：
# Projects:
#   my-api (active)
#   my-frontend
#   my-tool

# 2. 切换到前端项目
ga project switch my-frontend

# 3. 工作一段时间
vim src/App.tsx
/project test

# 4. 切换回 API 项目
ga project switch my-api

# 5. 继续之前的工作
# GA 自动恢复项目上下文
```

### 场景 4：项目重构

```bash
# 1. 记录重构决策
git checkout docs
cat > decisions/005-refactor-database-layer.md << 'EOF'
# 重构数据库层

## 背景
当前数据库层代码重复严重，难以维护。

## 决策
引入 Repository 模式，统一数据访问接口。

## 影响
- 代码量减少 30%
- 测试覆盖率提升到 90%
- 需要重写所有数据访问代码

## 实施计划
1. 定义 Repository 接口
2. 实现具体 Repository
3. 重写业务逻辑层
4. 更新测试用例
EOF
git add decisions/005-refactor-database-layer.md
git commit -m "docs: add database refactor decision"
git checkout main

# 2. 开始重构
vim src/repositories/base.py
vim src/repositories/user.py

# 3. 运行测试
/project test

# 4. 更新 handoff
git checkout docs
vim handoff.md  # 更新进度
git commit -m "docs: update refactor progress"
git checkout main
```

### 场景 5：项目归档

```bash
# 1. 清理临时文件
ga project clean

# 2. 更新 handoff 为最终状态
git checkout docs
vim handoff.md
# 添加：
# Status: Archived
# Reason: Project completed
# Date: 2026-05-30
git commit -m "docs: archive project"
git checkout main

# 3. 创建归档标签
git tag -a v1.0-archived -m "Project archived on 2026-05-30"

# 4. 推送到远程
git push origin main docs --tags

# 5. 从项目列表移除
ga project remove my-project

# 6. 项目文件仍然保留在磁盘上
ls ~/Projects/GenericAgent/temp/internal/my-project
```

---

## 4. 团队协作

### 4.1 共享项目配置

**提交 `.gaproject` 到 Git**：
```bash
git add .gaproject
git commit -m "chore: add GA project config"
git push
```

**团队成员克隆后自动生效**：
```bash
git clone https://github.com/team/project.git
cd project
# GA 自动发现并加载配置
```

### 4.2 共享 docs branch

**推送 docs branch**：
```bash
git checkout docs
git push origin docs
```

**团队成员拉取 docs branch**：
```bash
git fetch origin docs:docs
git checkout docs
```

### 4.3 Handoff 协作

**更新 handoff 时标注作者**：
```markdown
# Project Handoff

## 当前状态
- [Alice] 完成用户认证模块
- [Bob] 正在开发支付集成

## 下一步
- [Alice] 添加权限管理
- [Bob] 测试支付流程

## 开放问题
- [Alice] 是否需要支持 OAuth？
- [Bob] 支付网关选择哪个？
```

---

## 5. 故障排查流程

```
问题发生
    ↓
检查 .gaproject 是否存在且格式正确
    ↓
验证 project_root 路径
    ↓
检查 .ga_temp/ 是否在 .gitignore 中
    ↓
确认 docs branch 未被合并
    ↓
验证配置优先级
    ↓
查看 GA 日志（.ga_temp/logs/session.log）
    ↓
仍未解决？提交 issue 或寻求帮助
```

---

**返回**：[← Project Lifecycle SOP](project_lifecycle_sop.md)

**版本**：v1.0  
**最后更新**：2026-05-30
