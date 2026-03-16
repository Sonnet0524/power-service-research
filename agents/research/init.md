# Research Agent 初始化指南

> 如何使用SEARCH-R方法论创建和管理研究课题

**版本**: v3.0 | **更新**: 2026-03-16

---

## 🎯 设计理念

### 架构定位

```
SEARCH-R (方法论框架)
├─ agents/research/         # Agent定义（只读）
│   ├─ AGENTS.md            # Agent核心定义
│   ├─ init.md              # 本文件
│   └─ skills/              # 技能库
│
└─ research/                # 研究内容（实例化时创建）
    ├─ registry.md          # 课题注册表
    ├─ current-topic.md     # 当前课题引用
    └─ topics/ 或 topic.md  # 课题定义
    
    ↓ 作为模板复制
    ↓ 实例化
研究项目 (具体研究仓库)
├─ agents/research/         # Agent定义
└─ research/                # 研究内容
```

### 核心原则

1. **职责分离**：agents/ 只放Agent定义，research/ 只放研究内容
2. **课题独立**：每个课题拥有完整的文档体系
3. **统一入口**：通过registry.md管理所有课题概览

---

## 📁 目录结构

### 单课题模式

适用于只有一个研究主题的项目：

```
my-research/
├── agents/research/
│   ├── AGENTS.md
│   ├── init.md
│   ├── ESSENTIALS.md
│   └── skills/
│
├── research/
│   ├── registry.md           # 课题注册表（只有一个课题）
│   ├── current-topic.md      # 引用当前课题
│   │
│   ├── topic.md              # 课题定义
│   ├── catch-up.md           # 追更文档
│   ├── session-log.md        # 会话日志
│   │
│   ├── observations/         # 观察笔记
│   ├── retrievals/           # 检索报告
│   ├── theory/               # 理论文档
│   ├── reflections/          # 反思笔记
│   └── references/           # 参考资料
│
├── methodology/
├── templates/
└── opencode.json
```

### 多课题模式

适用于有多个相关研究主题的项目：

```
my-research/
├── agents/research/
│   └── ...
│
├── research/
│   ├── registry.md           # 课题注册表（所有课题概览）
│   ├── current-topic.md      # 当前激活课题引用
│   │
│   └── topics/
│       ├── agent-memory/     # 课题1：完整文档体系
│       │   ├── topic.md
│       │   ├── catch-up.md
│       │   ├── session-log.md
│       │   ├── observations/
│       │   ├── retrievals/
│       │   ├── theory/
│       │   ├── reflections/
│       │   └── references/
│       │
│       └── agent-metacognition/  # 课题2
│           ├── topic.md
│           ├── catch-up.md
│           └── ...
│
├── methodology/
├── templates/
└── opencode.json
```

---

## 🚀 场景A：创建新的研究项目

### 对话式创建流程

**用户**：我想研究Agent的记忆系统设计

**Research Agent**：
```
好的！我将帮你创建一个新的研究项目。

📋 请提供以下基本信息：

1. **项目名称** (用于目录名，建议用英文):
   示例: agent-memory-system-research
   
2. **项目路径** (项目创建在哪里):
   示例: D:\opencode\github\
   或直接回车使用默认路径

3. **研究模式**:
   - single: 单课题模式（推荐）
   - multi: 多课题模式

4. **研究背景** (简短描述，1-2句话即可):
   为什么要研究这个课题？
   
5. **核心问题** (最重要的问题，1-3个):
   你想通过研究解决什么问题？

💡 提示：先提供基本信息即可开始，后续可以逐步完善
```

**用户**：
```
1. agent-memory-research
2. D:\opencode\github\
3. single
4. Agent需要有效的记忆系统来支持长期对话和知识积累
5. 记忆应该分为哪些类型？如何实现记忆的压缩和遗忘？
```

**Research Agent**：
```
✅ 收到信息，正在创建研究项目...

[执行以下操作]

1. 创建项目目录结构
2. 复制SEARCH-R方法论模板
3. 创建opencode.json配置
4. 创建研究课题配置
5. 创建课题注册表
6. 激活研究课题

✅ 项目创建完成！

📁 项目位置: D:\opencode\github\agent-memory-research
📄 课题定义: research/topic.md
📊 课题注册表: research/registry.md
🎯 当前状态: 已激活

📊 研究课题概览：
- 研究背景: Agent需要有效的记忆系统...
- 核心问题: 记忆分类、记忆压缩、记忆遗忘
- 当前阶段: Survey (观察调研)
- 下一步: 开始第一次调研

是否现在开始研究？
```

---

## 🔄 场景B：在现有项目中添加课题

### 对话式添加流程

**用户**：我想在当前项目中研究Agent的元认知能力

**Research Agent**：
```
好的！我将在当前项目中创建新的研究课题。

📋 当前项目信息：
- 项目：agent-memory-research
- 当前课题：Agent记忆系统设计 (active)

📋 新课题基本信息：

1. **课题名称**: Agent元认知能力研究
   (建议用中文名称，便于理解)

2. **研究背景** (1-2句话):
   为什么要研究这个课题？

3. **核心问题** (1-3个):
   你想解决什么问题？

4. **优先级**: high/medium/low
   (相对于当前课题的优先级)
```

**用户**：
```
2. Agent需要知道自己什么时候不知道，这是质量门控的基础
3. 元认知如何定义？如何评估Agent的元认知水平？
4. medium
```

**Research Agent**：
```
检测到当前项目是单课题模式，是否转换为多课题模式？
- 转换后，原课题将移至 research/topics/agent-memory/
- 新课题将创建在 research/topics/agent-metacognition/

是否继续？(y/n)
```

**用户**：y

**Research Agent**：
```
✅ 转换项目结构并创建新课题...

[迁移原课题]
- 移动 research/topic.md → research/topics/agent-memory/topic.md
- 移动 research/observations/ → research/topics/agent-memory/observations/
- ...

[创建新课题]
- 创建 research/topics/agent-metacognition/topic.md
- 创建 research/topics/agent-metacognition/catch-up.md
- ...

[更新配置]
- 更新 research/registry.md
- 更新 research/current-topic.md

✅ 课题创建完成！

📁 课题配置: research/topics/agent-metacognition/topic.md
📊 当前状态: paused (优先级medium)
🎯 当前课题: 仍为"Agent记忆系统设计"

💡 提示：
- 新课题状态为paused，不会干扰当前研究
- 可以随时切换："切换到Agent元认知能力研究"
- 建议完成当前课题的重要节点后再切换

是否需要切换到新课题？
```

---

## 📝 核心文件说明

### registry.md（课题注册表）

**作用**：管理所有课题的概览和状态

**位置**：`research/registry.md`

**模板**：
```markdown
---
updated: YYYY-MM-DD
total_topics: N
active_topics: M
---

# 课题注册表

## 📊 课题概览

| 课题名称 | 状态 | 优先级 | 阶段 | 完成度 | 最后更新 |
|---------|------|--------|------|--------|----------|
| Agent记忆系统 | active | high | Survey | 30% | 2026-03-16 |
| Agent元认知 | paused | medium | Explore | 10% | 2026-03-15 |

## 📁 课题路径

- **Agent记忆系统**: `topics/agent-memory/`
- **Agent元认知**: `topics/agent-metacognition/`

## 🎯 当前焦点

**活跃课题**: Agent记忆系统

**关键问题**:
1. 记忆如何分类？
2. 如何实现记忆压缩？

**下一步**: 完成Survey阶段的资料收集

---

**维护者**: Research Agent
**更新时间**: 2026-03-16
```

### current-topic.md（当前课题引用）

**作用**：指向当前激活的课题

**位置**：`research/current-topic.md`

**单课题模式模板**：
```markdown
---
topic: Agent记忆系统
mode: single
---

# 当前研究课题

**课题名称**: Agent记忆系统

**模式**: 单课题模式

**路径**: `topic.md`

**状态**: active

---

**激活时间**: 2026-03-16
```

**多课题模式模板**：
```markdown
---
topic: Agent记忆系统
path: topics/agent-memory
mode: multi
---

# 当前研究课题

**课题名称**: Agent记忆系统

**模式**: 多课题模式

**路径**: `topics/agent-memory/`

**状态**: active

**快速链接**:
- [课题定义](topics/agent-memory/topic.md)
- [追更文档](topics/agent-memory/catch-up.md)
- [会话日志](topics/agent-memory/session-log.md)

---

**激活时间**: 2026-03-16
```

### topic.md（课题定义）

**作用**：定义研究课题的核心信息

**位置**：
- 单课题：`research/topic.md`
- 多课题：`research/topics/[topic-name]/topic.md`

**模板**：参考 `research/templates/topic-template.md`

### catch-up.md（追更文档）

**作用**：记录课题的最新进展，便于快速恢复上下文

**位置**：
- 单课题：`research/catch-up.md`
- 多课题：`research/topics/[topic-name]/catch-up.md`

**内容结构**：
```markdown
# Catch-Up 文档

## 📍 当前位置
- 阶段：Survey
- 进度：30%

## 🎯 核心问题
1. 记忆如何分类？
2. 如何实现记忆压缩？

## 📝 最近进展
- [2026-03-16] 分析了三种记忆类型...

## ⏭️ 下一步
1. 检索相关文献
2. 构建记忆分类框架

## 💾 关键上下文
（保存重要的上下文信息，便于下次快速恢复）
```

---

## 🔄 课题状态管理

### 状态定义

```
active    - 正在进行的研究
paused    - 暂停的研究
completed - 已完成的研究
planned   - 计划中的研究
```

### 状态转换规则

```
创建课题 → paused (初始状态)
paused → active (激活课题)
active → paused (暂停课题)
active → completed (完成课题)
planned → active (启动计划课题)
```

### 多课题管理建议

```
建议策略：
├─ 同时active的课题不超过2个
├─ 高优先级课题优先处理
├─ 定期回顾paused的课题
└─ 完成的课题及时归档

课题切换：
1. 保存当前课题进展
2. 更新当前课题状态为paused
3. 更新新课题状态为active
4. 更新 research/current-topic.md
5. 读取新课题的 catch-up.md
6. 继续研究
```

---

## 🔧 迁移指南

### 从旧结构迁移

```
旧结构 → 新结构

agents/research/current-topic.md
    → research/current-topic.md

agents/research/research-topics/[topic].md
    → research/topics/[topic]/topic.md

agents/research/observations/
    → research/topics/[topic]/observations/
    或 research/observations/ (单课题)

agents/research/session-log.md
    → research/topics/[topic]/session-log.md
    或 research/session-log.md (单课题)
```

### 迁移步骤

1. 创建 `research/` 目录结构
2. 创建 `research/registry.md`
3. 迁移课题配置：
   - 单课题：移动到 `research/topic.md`
   - 多课题：移动到 `research/topics/[name]/topic.md`
4. 迁移研究产出到对应课题目录
5. 创建每个课题的 `catch-up.md`
6. 更新 `research/current-topic.md`
7. 清理 `agents/research/` 中的旧内容

---

## 🎓 最佳实践

### 创建研究项目

1. **从对话开始** - 让Agent引导你创建
2. **最小化启动** - 只填写必填信息即可开始
3. **后续完善** - 在研究过程中逐步补充细节

### 管理多个课题

1. **限制active数量** - 同时进行不超过2个
2. **明确优先级** - 帮助决策研究顺序
3. **定期回顾** - 每周回顾paused课题
4. **及时归档** - 完成课题移至completed

### 课题文档维护

1. **及时更新进展** - 每次会话后更新topic.md
2. **维护catch-up** - 每次会话结束更新catch-up.md
3. **同步注册表** - 切换课题时更新registry.md
4. **记录关键决策** - 在session-log中留痕

---

## 📖 使用示例

### 示例1：快速创建单课题研究项目

```
Human: "我想研究代码自动生成的质量保证方法"

Agent: "好的！请提供：
1. 项目名称: code-generation-qa-research
2. 项目路径: [使用默认]
3. 研究模式: single
4. 研究背景: 代码生成工具的输出质量参差不齐，需要系统化的质量保证方法
5. 核心问题: 如何评估生成代码的质量？如何自动化质量检查？

创建中... ✅ 完成！是否开始研究？"

Human: "开始研究"

Agent: "进入Survey阶段..."
```

### 示例2：转换为多课题模式

```
Human: "我想在当前项目中研究代码生成的测试覆盖"

Agent: "当前项目是单课题模式，添加新课题需要转换为多课题模式。
原课题将移至 topics/code-generation-qa/
新课题将创建在 topics/test-coverage/

是否继续？"

Human: "y"

Agent: "转换中... ✅ 完成！

当前课题: code-generation-qa (active)
新课题: test-coverage (paused)

是否切换到新课题？"
```

### 示例3：切换研究课题

```
Human: "切换到测试覆盖研究"

Agent: "切换课题中...
1. 保存当前课题进展
   - 已完成: 质量评估框架设计
   - 下一步: 实现评估工具
   
2. 激活新课题
   - 课题: 测试覆盖研究
   - 状态: active
   - 读取: catch-up.md
   
✅ 切换完成！
当前课题: 测试覆盖研究
下一步: 开始调研测试覆盖最佳实践"
```

---

## 🔗 相关文档

### 核心文档
- [Agent身份和能力](AGENTS.md) - Research Agent核心定义
- [核心要点速查](ESSENTIALS.md) - 快速参考

### 方法论文档
- [SEARCH-R方法论](../../methodology/search-r-cycle.md) - 完整的7阶段研究循环
- [研究深度定义](../../methodology/research-depth.md) - Level 0-3深度标准
- [Human角色定义](../../methodology/human-role.md) - Human双重角色和参与最小化

### 模板文档
- [课题模板](../../research/templates/topic-template.md)
- [注册表模板](../../research/templates/registry-template.md)

---

## 📝 版本历史

- **v3.0** (2026-03-16) - 目录结构重构
  - 明确agents/和research/职责分离
  - 支持单课题和多课题两种模式
  - 新增课题注册表机制
  - 每个课题拥有完整文档体系

- **v2.0** (2026-03-13) - 简化优化
  - 明确两种使用场景
  - 提供最小化模板
  - 强调对话式创建

- **v1.1** (2026-03-07) - 多课题管理支持
  - 分离研究主体和研究课题
  - 添加课题切换机制

- **v1.0** (2026-03-07) - 初始版本

---

**维护者**: SEARCH-R Framework  
**更新时间**: 2026-03-16  
**文档类型**: 初始化指南
