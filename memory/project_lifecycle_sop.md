# Project Lifecycle SOP

> **调度层索引**：快速定位项目生命周期管理的各个子模块。

---

## 0. 核心原则

### 项目的本质

**项目 = 配置 + 代码 + 上下文**

- **配置层**：`.gaproject`（项目元数据和运行时配置）
- **代码层**：源代码文件（实际的项目内容）
- **上下文层**：`docs branch`（设计决策和演化追踪）

### 生命周期是连续的

```
创建 → 发现 → 加载 → 工作 → 演化 → 归档
```

### 设计哲学

1. **配置驱动**：通过 `.gaproject` 声明项目属性，GA 自动发现和加载
2. **上下文追踪**：通过 `docs branch` 记录设计决策和演化历史
3. **自动化优先**：减少手动操作，提高一致性
4. **灵活但有规范**：提供默认值，允许自定义

---

## 1. 快速参考卡

### 最小配置示例

```json
{
  "version": "1.0",
  "project_name": "my-project",
  "project_root": "."
}
```

### 核心命令

```bash
ga init my-project           # 初始化新项目
ga project list              # 列出所有项目
ga project switch my-project # 切换项目
```

### 典型场景

```bash
# 创建新项目
ga init my-project && cd my-project

# 接入现有项目
cd existing-project && echo '{"version":"1.0","project_name":"existing-project"}' > .gaproject

# 更新 handoff
git checkout docs && vim handoff.md && git commit -m "docs: update" && git checkout main
```

### 故障排查

1. **GA 未发现项目** → 检查 `.gaproject` 格式
2. **路径错误** → 确认 `project_root` 相对路径
3. **docs branch 冲突** → 永不合并，只 checkout 切换

---

## 2. 生命周期概览

### 6 个阶段

| 阶段 | 目的 | 关键操作 | 详细指南 |
|------|------|---------|---------|
| **创建（Init）** | 建立项目结构 | `ga init` | [→ Lifecycle Guide](project_lifecycle_guide.md#创建阶段) |
| **发现（Discovery）** | 自动识别项目 | 进入目录 | [→ Lifecycle Guide](project_lifecycle_guide.md#发现阶段) |
| **加载（Load）** | 读取配置和上下文 | GA 自动执行 | [→ Lifecycle Guide](project_lifecycle_guide.md#加载阶段) |
| **工作（Runtime）** | 日常开发 | 编码 + 更新 handoff | [→ Lifecycle Guide](project_lifecycle_guide.md#工作阶段) |
| **演化（Evolution）** | 追踪决策变化 | docs branch 提交 | [→ Lifecycle Guide](project_lifecycle_guide.md#演化阶段) |
| **归档（Archive）** | 项目结束 | 移动 + 移除配置 | [→ Lifecycle Guide](project_lifecycle_guide.md#归档阶段) |

---

## 3. 子模块索引

### 详细指南

| 子模块 | 用途 | 何时查阅 |
|--------|------|---------|
| [project_config_guide.md](project_config_guide.md) | 配置规范、命令参考、文件结构 | 需要配置项目或查阅命令选项 |
| [project_lifecycle_guide.md](project_lifecycle_guide.md) | 6 个生命周期阶段的详细流程 | 需要了解某个阶段的详细操作 |
| [project_best_practices.md](project_best_practices.md) | 最佳实践、避坑指南、典型场景 | 遇到问题或需要参考案例 |
| [project_integration_guide.md](project_integration_guide.md) | 与 nmem、waza、goal mode 集成 | 需要与其他 SOP 协同工作 |
| [project_dev_notes.md](project_dev_notes.md) | 决策记录、实现细节、技术债务 | 维护者需要了解设计决策 |

### 模板和脚本

```
project_templates/          # 项目模板
├── python/                 # Python 项目模板
├── node/                   # Node.js 项目模板
└── generic/                # 通用项目模板

scripts/                    # 自动化脚本
├── init_project.sh         # 初始化脚本
└── update_handoff.sh       # handoff 更新脚本
```

---

## 4. 实现状态

### 已实现

- ✅ `.gaproject` 配置规范
- ✅ 项目发现机制（自动检测 `.gaproject`）
- ✅ docs branch 机制（独立分支管理上下文）
- ✅ handoff 文档规范

### 待实现

- ⏳ `ga init` 命令（自动创建项目结构）
- ⏳ `ga project` 命令（项目管理）
- ⏳ `/project` Session 命令（会话内切换）
- ⏳ 项目模板（Python、Node、Generic）
- ⏳ 自动化脚本（init_project.sh、update_handoff.sh）

### 未来扩展

- 🔮 项目依赖管理（跨项目依赖追踪）
- 🔮 项目模板市场（社区贡献模板）
- 🔮 项目健康检查（配置验证、文件完整性）

---

## 5. 与其他 SOP 的关系

- **nmem**：项目上下文可存储到 nmem，实现跨会话记忆
- **waza**：项目开发流程可使用 waza 工作流（think/check/hunt）
- **goal_mode**：长期项目可使用 goal mode 管理目标和进度
- **autonomous_operation_sop**：项目任务可委托给自主模式执行

详见 [→ Integration Guide](project_integration_guide.md)

---

**版本**：v2.0（轻量级调度层）  
**创建日期**：2026-05-30  
**最后更新**：2026-05-30  
**维护者**：GenericAgent Team
