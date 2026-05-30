# Project Integration Guide

> 项目生命周期与其他 SOP 和工具的集成

---

## 1. 与 nmem 的集成

### 1.1 项目上下文存储

项目的设计决策和演化历史可以存储到 nmem，实现跨会话记忆：

```bash
# 存储项目决策
nmem m add \
  --unit_type decision \
  --title "my-project: 选择 Redis 作为缓存层" \
  --content "背景：API 响应时间过长。决策：使用 Redis，TTL 5分钟。影响：响应时间从 500ms 降到 50ms。" \
  --labels project:my-project,tech:redis

# 存储项目里程碑
nmem m add \
  --unit_type event \
  --title "my-project v0.3 发布" \
  --content "主要变更：引入缓存层、重构 API 路由、添加用户认证。" \
  --event_start 2026-05-30 \
  --labels project:my-project,milestone:v0.3
```

### 1.2 项目上下文召回

在新 session 中自动召回项目相关记忆：

```bash
# 搜索项目相关决策
nmem m search "my-project 缓存"

# 查看项目演化历史
nmem m search "my-project milestone"
```

### 1.3 Handoff 与 nmem 的关系

- **Handoff**：项目内部的上下文追踪（Git 管理，docs branch）
- **nmem**：跨项目的知识积累（全局记忆，可搜索）

**使用建议**：
- 项目内部决策 → handoff.md 和 decisions/
- 可复用的经验教训 → nmem（如"Redis 缓存最佳实践"）
- 项目里程碑 → 两者都记录（handoff 记录详情，nmem 记录摘要）

---

## 2. 与 waza 的集成

### 2.1 项目开发流程

使用 waza 工作流管理项目开发：

**方案设计阶段**：
```bash
# 使用 waza think 设计方案
waza think "如何设计 my-project 的缓存层？"

# 方案批准后记录到 docs branch
git checkout docs
cat > decisions/004-caching-strategy.md << 'EOF'
[waza think 输出的方案]
EOF
git commit -m "docs: add caching strategy decision"
git checkout main
```

**代码审查阶段**：
```bash
# 使用 waza check 审查代码
waza check src/cache.py

# 修复问题后提交
git add src/cache.py
git commit -m "fix: address waza check findings"
```

**报错定位阶段**：
```bash
# 使用 waza hunt 定位问题
waza hunt "Redis 连接超时"

# 修复后更新 handoff
git checkout docs
vim handoff.md  # 记录问题和解决方案
git commit -m "docs: add Redis timeout troubleshooting"
git checkout main
```

### 2.2 项目健康检查

定期使用 waza health 检查项目状态：

```bash
# 检查项目健康度
waza health

# 输出示例：
# ✅ 测试覆盖率: 85%
# ⚠️  技术债务: 3 个待优化项
# ✅ 文档完整性: 良好
# ❌ 性能基准: 未设置
```

---

## 3. 与 goal_mode 的集成

### 3.1 长期项目管理

使用 goal mode 管理长期项目目标：

```bash
# 进入 goal mode
/goal

# 设置项目目标
Goal: 完成 my-project v1.0 开发
Conditions:
- 测试覆盖率 ≥ 90%
- API 响应时间 < 100ms
- 文档完整
- 无 P0/P1 bug

# GA 自动追踪进度并更新 handoff
```

### 3.2 里程碑追踪

在 handoff 中记录 goal mode 的进度：

```markdown
# Project Handoff

## 当前目标
- [Goal Mode] 完成 v1.0 开发
- 进度: 75%
- 预计完成: 2026-06-15

## 已完成
- ✅ 缓存层实现（2026-05-30）
- ✅ 用户认证模块（2026-06-05）

## 进行中
- 🔄 性能优化（预计 2026-06-10）

## 待办
- ⏳ 文档补充
- ⏳ 安全审计
```

---

## 4. 与 autonomous_operation_sop 的集成

### 4.1 自动化项目任务

将项目任务委托给自主模式执行：

```bash
# 启动自主模式
/autonomous

# 任务示例：
Task: 为 my-project 添加单元测试
Context: 当前测试覆盖率 60%，目标 90%
Constraints:
- 使用 pytest
- 遵循现有测试风格
- 每个模块至少 80% 覆盖率

# GA 自动执行并更新 handoff
```

### 4.2 定期维护任务

使用 scheduled_task_sop 定期执行项目维护：

```bash
# 每周运行测试和代码检查
schedule:
  - name: my-project-weekly-check
    cron: "0 9 * * 1"  # 每周一 9:00
    command: |
      cd ~/Projects/GenericAgent/temp/internal/my-project
      /project test
      /project lint
      # 如果失败，发送通知
```

---

## 5. 与其他工具的集成

### 5.1 CI/CD 集成

在 CI/CD 流程中使用项目配置：

```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Load GA project config
        run: |
          PROJECT_NAME=$(jq -r '.project_name' .gaproject)
          TEST_CMD=$(jq -r '.test_command' .gaproject)
          echo "Running tests for $PROJECT_NAME"
          $TEST_CMD
```

### 5.2 IDE 集成

使用 `.gaproject` 配置 IDE：

**VSCode settings.json**：
```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "tests/"
  ],
  "files.exclude": {
    ".ga_temp": true,
    "__pycache__": true
  }
}
```

**PyCharm**：
- 项目根目录：从 `.gaproject` 的 `project_root` 读取
- 测试命令：从 `.gaproject` 的 `test_command` 读取

### 5.3 Docker 集成

在 Dockerfile 中使用项目配置：

```dockerfile
FROM python:3.11

# 复制项目配置
COPY .gaproject /app/.gaproject

# 读取配置并设置环境
RUN PROJECT_ROOT=$(jq -r '.project_root' /app/.gaproject) && \
    cd /app/$PROJECT_ROOT && \
    pip install -r requirements.txt

# 使用项目配置的构建命令
RUN BUILD_CMD=$(jq -r '.build_command' /app/.gaproject) && \
    $BUILD_CMD
```

---

## 6. Session 集成

### 6.1 Session 状态

项目加载后，session 包含以下状态：

```python
session.project = {
    'name': 'my-project',
    'root': '/Users/maygo/Projects/GenericAgent/temp/internal/my-project',
    'cwd': '/Users/maygo/Projects/GenericAgent/temp/internal/my-project',
    'temp_dir': '.ga_temp',
    'config': {
        'version': '1.0',
        'project_name': 'my-project',
        'project_root': '.',
        'build_command': 'python -m build',
        'test_command': 'pytest',
        ...
    }
}
```

### 6.2 工具调用适配

项目加载后，工具调用自动适配：

**code_run**：
```python
# 默认 cwd 为项目根目录
code_run("pytest tests/")
# 等价于：
# cd /Users/maygo/Projects/GenericAgent/temp/internal/my-project
# pytest tests/
```

**file_read/write**：
```python
# 相对路径基于项目根目录
file_read("src/main.py")
# 等价于：
# /Users/maygo/Projects/GenericAgent/temp/internal/my-project/src/main.py
```

**file_search**：
```python
# 搜索范围为项目根目录，排除 ignore_patterns
file_search("def cache")
# 搜索范围：/Users/maygo/Projects/GenericAgent/temp/internal/my-project
# 排除：.git/, .ga_temp/, __pycache__/, ...
```

### 6.3 上下文注入

项目的 `context_files` 自动注入到 session context：

```json
{
  "context_files": [
    "README.md",
    "AGENTS.md"
  ]
}
```

**效果**：
- README.md 和 AGENTS.md 的内容自动添加到系统 prompt
- GA 可以理解项目的背景和协作规范

### 6.4 自定义 Prompt

项目的 `custom_prompt` 自动添加到系统 prompt：

```json
{
  "custom_prompt": "This is a FastAPI project. Always use async/await for database operations. Follow PEP 8 style guide."
}
```

**效果**：
- GA 理解项目的技术栈和编码规范
- 生成的代码符合项目风格

---

## 7. 跨项目协作

### 7.1 项目依赖

在 `.gaproject` 中声明项目依赖：

```json
{
  "dependencies": [
    {
      "name": "my-lib",
      "path": "../my-lib",
      "type": "local"
    },
    {
      "name": "shared-utils",
      "path": "../shared-utils",
      "type": "local"
    }
  ]
}
```

### 7.2 Monorepo 支持

在 monorepo 中管理多个项目：

```
monorepo/
├── .gaproject              # 根项目配置
├── packages/
│   ├── api/
│   │   └── .gaproject      # API 项目配置
│   ├── frontend/
│   │   └── .gaproject      # 前端项目配置
│   └── shared/
│       └── .gaproject      # 共享库配置
```

**切换子项目**：
```bash
cd monorepo/packages/api
# GA 自动加载 api 项目配置

cd ../frontend
# GA 自动切换到 frontend 项目配置
```

---

## 8. 最佳实践

### 8.1 项目配置管理

- ✅ 提交 `.gaproject` 到 Git（团队共享）
- ✅ 使用 `custom_prompt` 定制项目级 AI 行为
- ✅ 在 `context_files` 中包含关键文档

### 8.2 Handoff 与 nmem 协同

- ✅ 项目内部决策 → handoff.md
- ✅ 可复用经验 → nmem
- ✅ 定期将 handoff 中的经验提炼到 nmem

### 8.3 工作流集成

- ✅ 使用 waza 管理开发流程
- ✅ 使用 goal mode 追踪长期目标
- ✅ 使用 autonomous mode 自动化重复任务

### 8.4 团队协作

- ✅ 共享 `.gaproject` 和 docs branch
- ✅ 在 handoff 中标注作者
- ✅ 定期同步 docs branch

---

**返回**：[← Project Lifecycle SOP](project_lifecycle_sop.md)

**版本**：v1.0  
**最后更新**：2026-05-30
