# Project Lifecycle Guide

> 详细的项目生命周期 6 个阶段说明

---

## 1. 创建阶段（Create）

### 1.1 目标

从零开始创建一个新项目，建立基础结构和配置。

### 1.2 操作步骤

```bash
# 1. 进入标准位置
cd ~/Projects/GenericAgent/temp/internal/

# 2. 初始化项目
ga init my-project

# 3. 进入项目目录
cd my-project
```

### 1.3 自动创建的内容

- **Git 仓库**：`git init`
- **docs branch**：用于存储设计决策和演化历史
- **`.gaproject`**：项目配置文件
- **`.ga_temp/`**：临时文件目录
- **`.gitignore`**：忽略规则（包含 `.ga_temp/`）
- **`handoff.md`**：初始 handoff 文档（在 docs branch）

### 1.4 项目类型检测

`ga init` 会自动检测项目类型：

| 检测文件 | 项目类型 | 生成配置 |
|---------|---------|---------|
| `pyproject.toml` / `setup.py` | Python | `build_command: python -m build`<br>`test_command: pytest` |
| `package.json` | Node.js | `build_command: npm run build`<br>`test_command: npm test` |
| `Cargo.toml` | Rust | `build_command: cargo build`<br>`test_command: cargo test` |
| `go.mod` | Go | `build_command: go build`<br>`test_command: go test` |
| 无特征文件 | Generic | 最小配置 |

### 1.5 手动指定模板

```bash
ga init my-api --template python
ga init my-frontend --template node
ga init my-tool --template rust
```

---

## 2. 发现阶段（Discover）

### 2.1 目标

让 GA 自动发现现有项目，无需手动配置。

### 2.2 发现机制

从当前目录向上查找，直到找到以下任一标志：

1. **`.gaproject` 文件**（最高优先级）
2. **`.git/` 目录**
3. **项目配置文件**：`package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod`
4. **IDE 配置目录**：`.vscode/` / `.idea/`

### 2.3 发现后行为

```python
# 伪代码
def discover_project(start_dir):
    current = start_dir
    while current != '/':
        if exists(current / '.gaproject'):
            return load_project(current)
        if exists(current / '.git'):
            return suggest_init(current)
        current = parent(current)
    return None
```

### 2.4 接入现有项目

**方式 1：自动初始化**
```bash
cd existing-project
ga init  # 检测现有文件并生成配置
```

**方式 2：手动创建配置**
```bash
cd existing-project
cat > .gaproject << 'EOF'
{
  "version": "1.0",
  "project_name": "existing-project",
  "project_root": "."
}
EOF
```

---

## 3. 加载阶段（Load）

### 3.1 目标

将项目配置加载到 GA session，设置工作环境。

### 3.2 加载流程

```
1. 读取 .gaproject 配置
2. 设置 session.cwd = project_root
3. 创建 temp_dir（如果不存在）
4. 加载 context_files 到 session context
5. 应用 custom_prompt
6. 加载环境变量（如果指定 env_file）
```

### 3.3 Session 状态

加载后，session 包含以下项目信息：

```python
session.project = {
    'name': 'my-project',
    'root': '/Users/maygo/Projects/GenericAgent/temp/internal/my-project',
    'cwd': '/Users/maygo/Projects/GenericAgent/temp/internal/my-project',
    'temp_dir': '.ga_temp',
    'config': {...}  # 完整的 .gaproject 内容
}
```

### 3.4 工具调用适配

- **`code_run`**：默认 cwd 为 `session.cwd`
- **`file_read/write`**：相对路径基于 `session.project_root`
- **`file_search`**：搜索范围为 `session.project_root`，排除 `ignore_patterns`

---

## 4. 工作阶段（Work）

### 4.1 目标

在项目中进行开发、测试、调试等日常工作。

### 4.2 典型工作流

**开发流程**：
```bash
# 1. 编辑代码
vim src/main.py

# 2. 运行测试
/project test

# 3. 检查代码质量
/project lint

# 4. 构建项目
/project build
```

**上下文管理**：
```bash
# 查看项目信息
/project info

# 重新加载配置
/project reload

# 清理临时文件
ga project clean
```

### 4.3 Handoff 更新

在重要决策或阶段性成果时更新 handoff：

```bash
# 切换到 docs branch
git checkout docs

# 编辑 handoff
vim handoff.md

# 提交更新
git add handoff.md
git commit -m "docs: update handoff v0.2 - add database schema"

# 切回主分支
git checkout main
```

### 4.4 多项目切换

```bash
# 列出所有项目
ga project list

# 切换到另一个项目
ga project switch my-api

# 返回之前的项目
ga project switch my-project
```

---

## 5. 演化阶段（Evolve）

### 5.1 目标

记录项目的设计决策和演化历史，便于回溯和理解。

### 5.2 docs branch 管理

**结构**：
```
docs branch:
├── handoff.md              # 当前状态和待办
├── decisions/              # 设计决策记录
│   ├── 001-architecture.md
│   ├── 002-database.md
│   └── 003-api-design.md
└── evolution/              # 演化历史
    ├── v0.1.md
    ├── v0.2.md
    └── v0.3.md
```

**工作流**：
```bash
# 1. 切换到 docs branch
git checkout docs

# 2. 记录新决策
cat > decisions/004-caching-strategy.md << 'EOF'
# 缓存策略

## 背景
API 响应时间过长，需要引入缓存。

## 决策
使用 Redis 作为缓存层，TTL 设置为 5 分钟。

## 影响
- 响应时间从 500ms 降低到 50ms
- 需要维护 Redis 实例
EOF

# 3. 提交
git add decisions/004-caching-strategy.md
git commit -m "docs: add caching strategy decision"

# 4. 切回主分支
git checkout main
```

### 5.3 版本演化记录

在重要里程碑时创建演化记录：

```bash
git checkout docs
cat > evolution/v0.3.md << 'EOF'
# v0.3 演化记录

## 时间
2026-05-30

## 主要变更
- 引入 Redis 缓存层
- 重构 API 路由结构
- 添加用户认证模块

## 技术债务
- 缓存失效策略需要优化
- 认证模块测试覆盖率不足

## 下一步
- 实现缓存预热机制
- 补充认证模块单元测试
EOF
git add evolution/v0.3.md
git commit -m "docs: add v0.3 evolution record"
git checkout main
```

---

## 6. 归档阶段（Archive）

### 6.1 目标

项目完成或暂停时，进行归档处理，保留完整的历史和上下文。

### 6.2 归档检查清单

- [ ] 所有代码已提交到 Git
- [ ] docs branch 已更新最终状态
- [ ] handoff.md 标记为"已完成"或"已暂停"
- [ ] 临时文件已清理（`.ga_temp/`）
- [ ] 环境变量和密钥已备份（如需要）
- [ ] README 已更新最终状态

### 6.3 归档操作

```bash
# 1. 清理临时文件
ga project clean

# 2. 更新 handoff 为最终状态
git checkout docs
vim handoff.md  # 添加 "Status: Archived" 标记
git commit -m "docs: archive project"
git checkout main

# 3. 创建归档标签
git tag -a v1.0-archived -m "Project archived on 2026-05-30"

# 4. 推送到远程（如果有）
git push origin main docs --tags

# 5. 从项目列表移除（不删除文件）
ga project remove my-project
```

### 6.4 归档后访问

归档的项目仍然可以重新加载：

```bash
# 进入归档项目目录
cd ~/Projects/GenericAgent/temp/internal/my-project

# GA 自动发现并加载
# 或手动切换
ga project switch my-project
```

---

## 7. 复用阶段（Reuse）

### 7.1 目标

将项目转化为可复用的模板或知识资产，供未来项目参考或直接使用。

### 7.2 复用形式

**1. 项目模板化**

将成功的项目结构转化为模板：

```bash
# 1. 清理项目特定内容
cd ~/Projects/GenericAgent/temp/internal/my-project
rm -rf node_modules/ .env .ga_temp/

# 2. 创建模板配置
cat > .gaproject.template << 'EOF'
{
  "version": "1.0",
  "project_name": "{{PROJECT_NAME}}",
  "project_type": "{{PROJECT_TYPE}}",
  "project_root": "."
}
EOF

# 3. 添加模板说明
cat > TEMPLATE.md << 'EOF'
# 项目模板说明

## 使用方法
1. 复制此目录到新位置
2. 重命名 .gaproject.template 为 .gaproject
3. 替换 {{PROJECT_NAME}} 和 {{PROJECT_TYPE}}
4. 运行 `ga init` 初始化

## 包含内容
- 基础项目结构
- 配置文件模板
- 常用脚本和工具
EOF

# 4. 归档为模板
git tag -a template-v1.0 -m "Project template v1.0"
```

**2. 知识提取**

从 docs branch 提取可复用的知识：

```bash
git checkout docs

# 提取设计模式
cat > patterns/api-design-pattern.md << 'EOF'
# API 设计模式

## 适用场景
RESTful API 设计，需要统一的错误处理和响应格式。

## 实现方式
- 统一响应格式：`{success, data, error}`
- 中间件错误捕获
- 标准 HTTP 状态码

## 优势
- 客户端易于处理
- 错误追踪清晰
- 可扩展性强
EOF

# 提取最佳实践
cat > best-practices/caching-strategy.md << 'EOF'
# 缓存策略最佳实践

## 经验总结
- Redis TTL 设置为 5 分钟适合大多数场景
- 缓存键使用命名空间前缀避免冲突
- 实现缓存预热机制提升首次访问性能

## 适用项目
需要高性能 API 响应的 Web 服务
EOF

git add patterns/ best-practices/
git commit -m "docs: extract reusable knowledge"
git checkout main
```

**3. 代码片段库**

提取可复用的代码片段：

```bash
# 在 docs branch 创建代码片段库
git checkout docs
mkdir -p snippets/

# 提取通用工具函数
cat > snippets/error-handler.js << 'EOF'
// 通用错误处理中间件
function errorHandler(err, req, res, next) {
  console.error(err.stack);
  res.status(err.status || 500).json({
    success: false,
    error: err.message
  });
}
EOF

git add snippets/
git commit -m "docs: add reusable code snippets"
git checkout main
```

### 7.3 复用检查清单

- [ ] 项目已完成并验证可用
- [ ] 移除项目特定的敏感信息（密钥、配置）
- [ ] 创建清晰的模板使用说明
- [ ] 提取通用的设计模式和最佳实践
- [ ] 标记模板版本（Git tag）
- [ ] 在 docs branch 记录复用指南

### 7.4 复用后维护

```bash
# 定期更新模板
cd ~/Projects/GenericAgent/temp/internal/my-project-template
git checkout docs
vim reuse-guide.md  # 更新复用指南
git commit -m "docs: update reuse guide"

# 创建新版本
git tag -a template-v1.1 -m "Updated template with new patterns"
```

---

## 8. 生命周期状态转换

```
┌─────────┐
│ Create  │ ──────────────────────────────┐
└────┬────┘                               │
     │                                     │
     ▼                                     │
┌─────────┐                               │
│Discover │ ◄─────────────────────┐       │
└────┬────┘                       │       │
     │                             │       │
     ▼                             │       │
┌─────────┐                       │       │
│  Load   │ ◄─────────┐           │       │
└────┬────┘           │           │       │
     │                 │           │       │
     ▼                 │           │       │
┌─────────┐           │           │       │
│  Work   │ ──────────┘           │       │
└────┬────┘                       │       │
     │                             │       │
     ▼                             │       │
┌─────────┐                       │       │
│ Evolve  │ ──────────────────────┘       │
└────┬────┘                               │
     │                                     │
     ▼                                     │
┌─────────┐                               │
│ Archive │ ───────────┐                  │
└────┬────┘            │                  │
     │                  │                  │
     ▼                  │                  │
┌─────────┐            │                  │
│  Reuse  │ ───────────┴──────────────────┘
└─────────┘
```

**状态说明**：
- **Create → Discover**：新项目创建后自动进入发现状态
- **Discover → Load**：发现项目后加载配置
- **Load → Work**：加载完成后进入工作状态
- **Work ↔ Load**：可以重新加载配置（`/project reload`）
- **Work → Evolve**：记录设计决策和演化历史
- **Evolve → Discover**：演化后可能需要重新发现（配置变更）
- **Archive → Reuse**：归档后可以转化为模板
- **Reuse → Create**：基于模板创建新项目

---

## 9. 最佳实践

### 9.1 创建阶段

- ✅ 使用标准位置：`~/Projects/GenericAgent/temp/internal/`
- ✅ 让 GA 自动检测项目类型
- ✅ 初始化 Git 仓库（便于版本控制）

### 9.2 工作阶段

- ✅ 频繁提交代码（小步快跑）
- ✅ 使用 `/project test` 和 `/project lint` 保证代码质量
- ✅ 定期更新 handoff（重要决策时）

### 9.3 演化阶段

- ✅ 记录"为什么"而不是"是什么"（代码已经说明了"是什么"）
- ✅ 使用决策记录模板（背景 → 决策 → 影响）
- ✅ 在里程碑时创建演化记录

### 9.4 归档阶段

- ✅ 完整的归档检查清单
- ✅ 使用 Git 标签标记归档版本
- ✅ 保留完整的 docs branch 历史

### 9.5 复用阶段

- ✅ 移除敏感信息后再模板化
- ✅ 提供清晰的模板使用说明
- ✅ 提取通用模式而非具体实现
- ✅ 标记模板版本便于追踪演化

---

**返回**：[← Project Lifecycle SOP](project_lifecycle_sop.md)

**版本**：v1.0  
**最后更新**：2026-05-30
