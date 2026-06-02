# PRD: Skill Hunter — GitHub Claude Code Skill 爬虫

## Problem Statement

Claude Code Skills 是一个快速增长的社区生态，每天都有开发者在 GitHub 上发布新的 Skill（以 `SKILL.md` 为入口文件）。但目前没有一个工具能够帮助用户及时发现和了解这些新上线的 Skill。用户只能从 skills.sh 等第三方索引站点被动获取信息，而 skills.sh 依赖作者手动提交 Issue 收录，会漏掉大量优秀的 Skill。用户需要一种自动化方式，快速发现过去一周 GitHub 上所有新发布或更新的 Claude Code Skill，并生成一份包含中英文描述的阅读报告。

## Solution

`/skill-hunter` 是一个 Claude Code Skill，每次被调用时自动执行以下流程：

1. 通过 GitHub Repository Search API 搜索过去 7 天内提及 "SKILL.md" 和 "claude code" 的新建或更新仓库
2. 与本地索引 `skill-index.json` 比对，过滤已发现且无更新的仓库
3. 下载候选仓库的 `SKILL.md` 原文和仓库元数据（作者、日期、star 数）
4. 由 AI 判断每个候补是否是真正的 Claude Code Skill
5. 对确认为 Skill 的条目，AI 生成中英文描述
6. 输出 `Github Report [Date].md`（人读报告），更新 `skill-index.json`（机器索引）

用户只需在 Claude Code 中输入 `/skill-hunter`，等待几分钟后即可在项目目录下看到一份整洁的报告。

## User Stories

1. As a Claude Code 用户，我想要一次性搜索过去一周 GitHub 上所有新发布的 Claude Code Skill，以便我及时了解社区动态
2. As a Claude Code 用户，我想要一个 `/skill-hunter` 命令来自动化整个搜索和整理流程，以便我不需要手动在 GitHub 上翻页搜索
3. As a Claude Code 用户，我希望 crawler 能帮我判断搜索结果是不是真正的 Claude Code Skill（而非碰巧同名的文件），以便我只看到有价值的内容
4. As a Claude Code 用户，我希望每个 Skill 都附带 AI 生成的中文和英文描述，以便我快速判断是否值得深入了解
5. As a Claude Code 用户，我希望报告中也包含仓库作者、star 数、发布日期等元数据，以便我评估 Skill 的受欢迎程度和新鲜度
6. As a Claude Code 用户，我希望有一个本地索引来记录已发现的 Skill，以便下次运行时不会重复报告相同的 Skill
7. As a Claude Code 用户，对于之前发现过但仓库有更新的 Skill，我希望能再次被提醒，以便我关注后续变化
8. As a Claude Code 用户，我希望 GitHub API token 是可选的，以便我没有 token 时也能运行（只是速度慢些）
9. As a Claude Code 用户，我希望运行时能看到实时进度提示，以便我知道当前在处理哪一步
10. As a Claude Code 用户，我希望报告以 Markdown 文件形式保存在项目目录下，以便我随时查阅和分享
11. As a Claude Code 用户，我希望同一个仓库下的多个 Skill 被合并为一个条目，以便报告简洁易读
12. As a 开发者，我希望 `skill-index.json` 中的白名单能跳过已验证的 Skill，以便减少每次运行时 AI 判断的重复工作

## Implementation Decisions

### 技术选型
- **脚本语言**：Python，利用 `requests` 库调 GitHub API，原生 JSON 读写
- **分工边界**：Python 脚本负责确定性工作（搜索、下载、读写文件），Agent 负责判断性工作（真伪辨别、描述生成、报告撰写）

### 模块架构

**Python 侧（脚本）**：
- **Config** — 读取 `skill-hunter/config.json`，提供 token、回溯天数等配置
- **GitHubClient** — 封装 GitHub Repository Search API 和内容获取 API
- **IndexManager** — 读写 `skill-index.json`，去重比对，返回"新发现"和"有更新"两类候选
- **Crawler** — 串联搜索→去重→下载→输出 raw-data.json 的主流程

**Agent 侧（Claude 执行）**：
- **SkillFilter** — 读取每个候选的 SKILL.md 全文，判断是否是真的 Claude Code Skill（通过 YAML frontmatter 和内容特征）
- **DescriptionGenerator** — 读取 SKILL.md 全文，生成中文和英文详细描述
- **Reporter** — 写 `Github Report [Date].md` 报告，更新 `skill-index.json` 索引

### 搜索策略
- 单一搜索 query：`"SKILL.md" "claude code" pushed:>YYYY-MM-DD`
- 使用 GitHub Repository Search API（支持 `pushed:` 日期限定符）
- 日期范围默认回溯 7 天，通过 `config.json` 可配置

### 索引设计
- 文件：`skill-index.json`
- 字段：`owner`（作者）、`repo`（仓库名）、`publish_date`（发布日期）、`last_update`（最后更新日期）、`last_discovered`（最后发现时间）
- 功能一：去重——已存在且 `last_update` 不晚于 `last_discovered` 则跳过
- 功能二：白名单缓存——已验证过的仓库下次无需 AI 重新判断

### 报告格式
- 文件名：`Github Report YYYY-MM-DD.md`
- 内容：每个仓库一个条目，含仓库名+作者、发现日期、英文描述、中文描述、star 数
- 按仓库聚合，多个 Skill 统一汇总描述

### 配置
- 文件：`skill-hunter/config.json`
- 字段：`github_token`（可选）、`lookback_days`（默认 7）、`max_results`（搜索结果上限）
- 无 token 时打印提示，降低 API 调用频率但仍可运行

### 进度提示
- 实时打印："正在搜索..." → "找到 N 个候选" → "正在下载 SKILL.md..." → "正在 AI 判断..." → "正在生成描述 N/M..." → "报告已生成"

### 完全自动化
- 用户触发 `/skill-hunter` 后无需任何交互，跑完直接输出结果

## Testing Decisions

### 测试原则
- 只测外部行为，不测实现细节
- 测试应能在重构后继续通过

### 测试范围
- 只测试 **IndexManager** 模块——它是唯一包含判断逻辑的模块（去重比对、日期比较、新面孔 vs 有更新决策）
- Config 是纯 JSON 读取，不值得测试
- GitHubClient 是 HTTP 调用封装，维护 mock 成本过高
- Crawler 是胶水代码，适合手动验证

### IndexManager 测试场景
- 空索引——所有候选都是新发现
- 已有索引——已存在且无更新的仓库被过滤
- 已有索引——已存在但有更新的仓库被标记为"有变更"
- 索引读/写正确性——写入后读取保持一致

## Out of Scope

- 持续集成/定时自动运行——本次只实现手动触发
- 增量更新之外的长期趋势分析
- Skill 质量评分或排序
- Skill 内容翻译（保留英文原文 + 中文描述为 AI 摘要，非翻译）
- Web 界面或通知推送——本地文件输出即可
- 多语言搜索支持（仅搜索英文关键词）
- 对 Skill 执行安装或任何写操作——只读搜索和报告

## Further Notes

- 此项目本身也将被实现为一个 Claude Code Skill（`/skill-hunter`），用 Claude Code 的 API 做 AI 判断
- 用户可通过修改 `config.json` 中的 API endpoint 更换更便宜的模型
- 项目目录结构：`skill-hunter/` 包含 Python 脚本、`SKILL.md`、`config.json`；报告和索引输出到项目根目录
- 项目遵循 CLAUDE.md 中的工作原则：所有文件操作委派给 Agent 执行
