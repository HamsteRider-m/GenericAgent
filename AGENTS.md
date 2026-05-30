# GenericAgent Project Constraints

This file defines project-level constraints that override global rules (per CONSTITUTION §6).

## Task Evaluation & Tool Routing Protocol

**MANDATORY WORKFLOW** - Before responding to any user request, you MUST:

### Step 1: Task Complexity Assessment

Evaluate the task complexity using these criteria:

- **Simple Task**: Direct question with known answer, single-step operation, no design needed
- **Complex Task**: Requires planning, multiple approaches, tradeoffs, architecture decisions, or systematic analysis

### Step 2: Intent Recognition & Tool Routing

If the task is **COMPLEX**, check if it matches any of these intents and route to the appropriate Waza skill:

#### 🎯 Waza Think (方案设计)
**When to use:**
- User needs a solution design, architecture plan, or systematic approach
- Task involves comparing multiple options or evaluating tradeoffs
- Requires structured thinking: problem analysis → solution options → recommendation
- Keywords: 方案设计 / 出方案 / 架构规划 / 系统设计 / 如何设计 / 怎么实现

**Action:** Read `memory/waza_sop.md` and invoke `waza think`

#### 🔍 Waza Check (代码审查)
**When to use:**
- User asks to review, audit, or evaluate existing code
- Task involves security analysis, code quality assessment, or best practices review
- Requires systematic inspection of code structure, logic, or patterns
- Keywords: 代码审查 / 审查代码 / review / 安全审计 / 代码质量

**Action:** Read `memory/waza_sop.md` and invoke `waza check`

#### 🐛 Waza Hunt (报错定位)
**When to use:**
- User reports an error, bug, or unexpected behavior
- Task involves root cause analysis, debugging, or troubleshooting
- Requires systematic investigation: symptoms → hypothesis → verification
- Keywords: 报错 / 故障 / bug / 定位问题 / 排查 / debug

**Action:** Read `memory/waza_sop.md` and invoke `waza hunt`

#### 🏗️ Waza Design (架构设计)
**When to use:**
- User needs system architecture, component design, or technical blueprint
- Task involves defining modules, interfaces, data flow, or deployment strategy
- Requires high-level structural thinking beyond single-feature implementation
- Keywords: 架构设计 / 系统架构 / 技术架构 / 模块设计

**Action:** Read `memory/waza_sop.md` and invoke `waza design`

#### 👁️ Waza Read (UI评审)
**When to use:**
- User asks to evaluate UI/UX, interface design, or visual layout
- Task involves usability analysis, accessibility review, or design critique
- Requires systematic assessment of user experience and interaction patterns
- Keywords: UI评审 / 界面评估 / UX分析 / 设计评审

**Action:** Read `memory/waza_sop.md` and invoke `waza read`

#### 📝 Waza Write (文档写作)
**When to use:**
- User needs technical documentation, API docs, or architecture documentation
- Task involves structured writing: README, design docs, technical specs
- Requires clear explanation of complex technical concepts
- Keywords: 文档写作 / 技术文档 / 写文档 / API文档

**Action:** Read `memory/waza_sop.md` and invoke `waza write`

#### 📚 Waza Learn (技术研究)
**When to use:**
- User asks to research, investigate, or learn about a technical topic
- Task involves gathering information, comparing technologies, or understanding concepts
- Requires systematic exploration and knowledge synthesis
- Keywords: 技术研究 / 深度学习 / 调研 / 了解技术

**Action:** Read `memory/waza_sop.md` and invoke `waza learn`

#### 🏥 Waza Health (健康检查)
**When to use:**
- User asks to check system health, diagnose issues, or assess overall status
- Task involves comprehensive inspection of multiple components
- Requires systematic health assessment across different dimensions
- Keywords: 健康检查 / 系统诊断 / 检查状态 / 整体评估

**Action:** Read `memory/waza_sop.md` and invoke `waza health`

---

## Decision Logic

```
User Request
    ↓
[Complexity Assessment]
    ↓
Simple? → Answer directly with general knowledge
    ↓
Complex? → [Intent Recognition]
    ↓
Matches Waza intent? → Read waza_sop.md → Invoke appropriate skill
    ↓
No match? → Use general problem-solving approach
```

**This is a project-level constraint with HIGHEST priority.**

The goal is to leverage specialized tools for complex tasks while maintaining efficiency for simple queries.
