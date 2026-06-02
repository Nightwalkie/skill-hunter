# Github Report 2026-06-02

## New Skills

### FrancyJGLisboa/agent-skill-creator
- **Author**: FrancyJGLisboa
- **Stars**: 1288
- **Discovered**: 2026-06-02
- **First Published**: 2025-10-18
- **Status**: new

**English Description**: A Level 5 autonomous skill factory that converts raw workflow descriptions, files, URLs, screenshots, or even vague half-sentences into production-ready, cross-platform agent skills. It uses evidence-based intent derivation to extract implicit requirements from whatever material the user provides, then autonomously builds a complete skill package with SKILL.md, AGENTS.md, scripts, references, evaluations, and an installer. The generated skill works across 20+ platforms (Claude Code, Cursor, Codex, Gemini CLI, etc.) and is invocable via `/skill-name`. Use when you want to turn any repetitive workflow, documentation, or half-formed idea into a reusable agent skill without writing code yourself.

**中文描述**: 一个全自动的技能工厂（Level 5），能将任何原始材料——工作流描述、文件、链接、截图、甚至一句模糊的"帮我把这个自动化"——转化为生产级的跨平台 Agent 技能。它通过证据驱动的意图推导，自主提取隐含需求，然后端到端生成完整的技能包（包括 SKILL.md、AGENTS.md、Python 脚本、参考资料、评估用例和安装器），覆盖 Claude Code、Cursor、Codex、Gemini CLI 等 20+ 个平台。生成后的技能可通过 `/技能名` 一键调用。适合想把重复性工作变成可复用的 Agent 技能，但不想自己写代码的用户。

---

### O0000-code/paper-search-pro
- **Author**: O0000-code
- **Stars**: 27
- **Discovered**: 2026-06-02
- **First Published**: 2026-05-24
- **Status**: new

**English Description**: A multi-source academic literature search skill that orchestrates 5 data sources (OpenAlex, PubMed, arXiv, Semantic Scholar, CrossRef) with 4 adjustable depth tiers ranging from a 5-minute quick scan to a 3-hour systematic review prep. It uses parallel AI SubAgents for paper classification against an RCS rubric, produces a PRISMA-S compliant execution log, and outputs a Shadcn-styled HTML report with BibTeX/RIS/CSV exports. The skill supports PICO/SPIDER/PEO query frameworks, saturation curve analysis to decide when to stop searching, and citation network expansion. Use when doing any kind of literature search—from a quick "find me a few papers" to a full systematic review preparation.

**中文描述**: 一个多源学术文献检索技能，协调 5 个数据源（OpenAlex、PubMed、arXiv、Semantic Scholar、CrossRef），提供 4 档可调节深度——从 5 分钟快速扫描到 3 小时系统综述前期准备。它使用并行 AI 子代理按 RCS 评分标准对论文进行分类，生成符合 PRISMA-S 标准的执行日志，输出 Shadcn 风格 HTML 报告及 BibTeX/RIS/CSV 导出。支持 PICO/SPIDER/PEO 检索框架、饱和度曲线分析以决定何时停止检索，以及引文网络扩展。适用于任何文献检索场景——从轻量级"帮我找几篇论文"到正式的系统综述准备。

---

### moonrunnerkc/skillcheck
- **Author**: moonrunnerkc
- **Stars**: 13
- **Discovered**: 2026-06-02
- **First Published**: 2026-03-11
- **Status**: new

**English Description**: A CLI validation tool for SKILL.md files that checks spec-facing structure, sizing, references, and cross-agent compatibility. It reports errors, warnings, and info diagnostics with exit codes for CI integration. Beyond static checks, it supports AI-driven semantic self-critique (emitting prompts for agent review and ingesting the critique JSON) and capability graph visualization to analyze skill dependencies. Use when validating a single SKILL.md, auditing a skills directory, or integrating skill quality checks into a CI pipeline.

**中文描述**: 一个用于校验 SKILL.md 文件的 CLI 工具，检查规范结构、文件大小、引用完整性和跨平台兼容性。它输出错误、警告和信息诊断，并通过退出码支持 CI 集成。除了静态检查，它还支持 AI 驱动的语义自审（生成审阅提示并接收评审 JSON）和能力图谱可视化，用于分析技能间的依赖关系。适用于校验单个 SKILL.md、审计技能目录，或将技能质量检查集成到 CI 流水线中。

---

### tcsenpai/specification-website-skill
- **Author**: tcsenpai
- **Stars**: 9
- **Discovered**: 2026-06-02
- **First Published**: 2026-05-31
- **Status**: new

**English Description**: Bundles the complete Website Specification (128 topics across 10 categories including foundations, SEO, accessibility, security, agent readiness, performance, privacy, resilience, and internationalization) as an offline-capable agent skill. Every topic is tagged with a status contract (required/recommended/optional/avoid) and backed by primary sources from WHATWG, W3C, IETF RFCs, IANA, and WCAG. The skill provides a tickable checklist, per-category audit workflows, and optional MCP/HTTP routes for fresh data. Use when auditing a URL, answering "is X required?" questions, building a new site against web standards, or checking agent/AI readiness.

**中文描述**: 将完整的网站规范（128 个主题，覆盖 HTML 基础、SEO、无障碍、安全、Agent 就绪、性能、隐私、韧性、国际化等 10 个类别）打包为可离线使用的 Agent 技能。每个主题标有状态标签（必需/推荐/可选/避免），并引用了 WHATWG、W3C、IETF、IANA、WCAG 等一手标准来源。技能提供了可勾选的检查清单、按类别的审计工作流，以及可选的 MCP/HTTP 获取最新数据的方式。适用于审计网站、回答"某个特性是否必需"、按 Web 标准建站，或检查 AI Agent 就绪程度。

---

### Naoray/scribe
- **Author**: Naoray
- **Stars**: 5
- **Discovered**: 2026-06-02
- **First Published**: 2026-03-27
- **Status**: new

**English Description**: A package manager for AI coding-agent skills. Scribe maintains a canonical skill store at `~/.scribe/skills/` and links skills into Claude Code, Cursor, Codex, and other supported tools. It supports install, list, sync, remove, adopt (import unmanaged local skills), kit management (skill bundles with optional MCP servers), and snippet authoring. All commands support `--json` output for programmatic consumption. Use when you need to install, manage, share, or audit AI agent skills across multiple tools on a single machine.

**中文描述**: 一个面向 AI 编程 Agent 技能的包管理器。Scribe 在 `~/.scribe/skills/` 维护标准技能仓库，并将技能链接到 Claude Code、Cursor、Codex 等工具目录。支持安装、列表、同步、删除、adopt（导入未托管的本地技能）、kit 管理（技能套装，可绑定 MCP 服务器）和 snippet 编写。所有命令支持 `--json` 输出供程序化消费。适用于在同一台机器上跨多个工具安装、管理、分享或审计 AI Agent 技能。

---

### cxshoutghost/claude-code-skillforge
- **Author**: cxshoutghost
- **Stars**: 3
- **Discovered**: 2026-06-02
- **First Published**: 2026-03-08
- **Status**: new

**English Description**: A comprehensive SOP (standard operating procedure) for generating highly optimized Agent Skills for Claude Code and the Antigravity ecosystem. It implements the official "Progressive Disclosure" strategy with 27-item validation checklists and 10 authoring patterns. The skill supports three modes: Build (create new skills from scratch with marketplace discovery to avoid duplication), Upgrade (audit and modernize existing skills against current best practices), and Scan (health-check all installed skills). Use when building a new skill, upgrading an old one, or auditing installed skills for compliance.

**中文描述**: 用于生成高度优化的 Agent Skill 的完整 SOP（标准操作流程），面向 Claude Code 和 Antigravity 生态系统。实现了官方的"渐进式披露"策略，包含 27 项校验清单和 10 种编写模式。支持三种模式：Build（从零创建技能，含市场发现避免重复造轮子）、Upgrade（按最新最佳实践审计和升级现有技能）和 Scan（对所有已安装技能做健康检查）。适用于创建新技能、升级旧技能，或审计已安装技能的合规性。

---

### Husseincartographical320/writing-style-skill
- **Author**: Husseincartographical320
- **Stars**: 1
- **Discovered**: 2026-06-02
- **First Published**: 2026-04-17
- **Status**: new

**English Description**: A reusable writing style template skill with built-in automatic learning. It defines voice dimensions on a 1-10 scale (formal/casual, technical/accessible, etc.), writing rules, banned words, and sentence structure preferences. The defining feature is its observe-improve loop: AI writes a draft, the human edits it to satisfaction, and a diff script automatically extracts the human's edits as new rules that get written back into SKILL.md, making the skill progressively more accurate over time. Use as a starting point to capture and enforce a personal or brand writing style.

**中文描述**: 一个可复用的写作风格模板技能，内置自动学习机制。通过 1-10 分量表定义风格维度（正式/随意、技术/通俗等）、写作规则、禁用词和句式偏好。其核心特色是观察-改进循环：AI 生成初稿，用户修改到满意，diff 脚本自动提取修改内容并转化为新规则写回 SKILL.md，使技能越用越准。适合作为起点来捕捉和执行个人或品牌的写作风格。

---

### Sttrevens/air-game-dev-pm-skill
- **Author**: Sttrevens
- **Stars**: 1
- **Discovered**: 2026-06-02
- **First Published**: 2026-05-29
- **Status**: new

**English Description**: A game development project management methodology skill based on "Air's PM method." It guides teams from a player-centric Experience vision down through Mainstays (core pillars), Features (user-facing and capability), Levels (L1-L4 quality/validation states), Tasks, and Iters (sprints that produce playable "stones"). The skill emphasizes reversible decisions, lowest-cost validation, and continuous heatmap-based progress tracking. Use when planning an indie or small-team game project where design, tech, art, and production decisions need to stay visible and reversible.

**中文描述**: 一个基于"Air PM 方法"的游戏开发项目管理技能。它引导团队从以玩家为中心的游戏体验愿景出发，逐层分解为 Mainstays（核心支柱）、Features（用户面向和能力型功能）、Levels（L1-L4 质量/验证状态）、Tasks 和 Iters（产出可玩"石头"的冲刺周期）。技能强调决策可逆、最低成本验证和基于热力图的进度追踪。适用于需要保持设计、技术、美术和制作决策透明且可逆的独立游戏或小团队项目规划。

---

### nickyc1/mcp-setup-template
- **Author**: nickyc1
- **Stars**: 1
- **Discovered**: 2026-06-02
- **First Published**: 2026-05-13
- **Status**: new

**English Description**: A meta-skill for authoring reproducible first-time setup skills for any MCP (Model Context Protocol) server. It codifies a proven 8-step pattern (prereq check, auth setup, token exchange, install, config file, daemon, Claude registration, verify) used by Anthropic's own MCP setup skills. The skill walks through fact-gathering about the MCP server, scaffolds a standard file structure (SKILL.md, references, configure.sh), and enforces conventions like leading with auth, including copyable commands, and providing troubleshooting sections. Use when you need to create a new MCP onboarding skill or audit an existing one against the standard pattern.

**中文描述**: 一个元技能（meta-skill），用于为任何 MCP（模型上下文协议）服务器编写可复现的首次配置技能。它将 Anthropic 官方 MCP 配置技能使用的经过验证的 8 步模式（前置检查、认证配置、令牌交换、安装、配置文件、守护进程、Claude 注册、验证）固化为模板。技能引导收集 MCP 服务器信息、生成标准文件结构（SKILL.md、参考资料、configure.sh），并强制执行规范——如认证放在首位、每步提供可复制命令、必须包含排查章节。适用于创建新的 MCP 接入技能或按标准模式审计已有技能。

---

### RachelXiaolan/video-transcript
- **Author**: RachelXiaolan
- **Stars**: 0
- **Discovered**: 2026-06-02
- **First Published**: 2026-06-01
- **Status**: new

**English Description**: A multi-platform video transcription skill with a 3-tier fallback pipeline. Tier 1 grabs native subtitles via platform-specific APIs (YouTube, with pluggable adapters for more), Tier 2 downloads audio and transcribes via Deepgram Nova-3 (cloud, no GPU, ~$0.0043/min), and Tier 3 falls back to title+description metadata. The generic adapter covers 1500+ sites via yt-dlp. It includes a pre-flight confirmation step showing title/duration/subtitle availability before committing to paid transcription. Use when you share any video URL and want a transcript, regardless of whether the video has built-in subtitles.

**中文描述**: 一个多平台视频转录技能，采用三级回退管道。第一级通过平台特定 API 抓取原生字幕（YouTube 及可插拔适配器），第二级下载音频后用 Deepgram Nova-3 云端转录（无需 GPU，约 $0.0043/分钟），第三级仅提取标题和描述元数据。通用适配器通过 yt-dlp 支持 1500+ 网站。包含转录前的确认环节——先展示标题、时长、字幕可用性，再决定是否使用付费转录。适用于分享任何视频链接并获取文字稿的场景，无论视频是否有内置字幕。

---

### codeErrorSleep/auntie-letter-style
- **Author**: codeErrorSleep
- **Stars**: 0
- **Discovered**: 2026-06-02
- **First Published**: 2026-06-01
- **Status**: new

**English Description**: A style-transfer skill that transforms crude, vulgar, or modern colloquial Chinese into elegant semi-classical Chinese in the restrained, romantic-longing style of the film "给阿嬷的情书" (A Love Letter to Grandma). It applies a signature rhythm of short four-character phrases, classical nature imagery (moon, streams, wind), temporal-spatial anchors (nightfall, before the gate), and a closing vernacular phrase that lands the emotion. Outputs 3 variant lines (subtle, playful, classical) of 15-40 characters each, suitable for social media, greeting cards, or romantic messages. Use when someone wants to say something in a more refined, poetic way in Chinese.

**中文描述**: 一个风格转换技能，将粗俗、现代口语化或网络语的中文改写为《给阿嬷的情书》那种"半文半白、克制深情"的优雅中文。它运用四字短句节奏、古典自然意象（明月、溪水、竹影）、时空锚点（入夜、门前）以及白话收束句来承载情感。输出 3 条变体（含蓄、俏皮、古雅），每条 15-40 字，适合朋友圈、卡片文案或情书。适用于想把大白话变得更有诗意和质感的场景。

---

### realnaka/claim-verification
- **Author**: realnaka
- **Stars**: 0
- **Discovered**: 2026-06-02
- **First Published**: 2026-05-31
- **Status**: new

**English Description**: A rigorous fact-checking methodology skill that treats all second-hand information (tweets, news, research notes, other AIs' conclusions) as hypotheses by default. It follows a 5-step workflow: decompose complex claims into atomic checkable units, triage by credibility and impact, verify against an evidence ladder (from SEC filings and official sources down to anonymous posts), label each claim (confirmed/partial/wrong/unverified), and output a verification matrix. Includes 8 common distortion patterns (misattribution, circular citation, stale data, conflation, etc.) and three mandatory self-checks before concluding. Use when verifying any claim, fact-checking news, evaluating investment theses, or auditing another AI's output.

**中文描述**: 一个严谨的事实核查方法论技能，将所有二手信息（推文、新闻、研报、其他 AI 的结论）默认为待验证假设。遵循五步流程：将复杂论述分解为原子级可核查命题、按可信度和影响优先级排序、沿着证据等级阶梯（从 SEC 文件和官方公告到匿名帖子）追溯一手来源、为每个命题标注状态（确认/部分正确/错误/未验证）、输出核查矩阵。包含 8 种常见信息失真模式（张冠李戴、循环引用、数据过时、概念混淆等）和 3 项做出结论前的强制自检。适用于核实任何论断、核查新闻真伪、评估投资论点或审计其他 AI 的输出。

---

### SotongDJ/slidedeck
- **Author**: SotongDJ
- **Stars**: 0
- **Discovered**: 2026-06-02
- **First Published**: 2026-04-28
- **Status**: new

**English Description**: A card-based presentation skill that generates structured JSONL deck files (`{codename}_box.cards`) for the Card Box Viewer. The skill supports 30+ visualization patterns including tables, bar/radar/line/pie/donut/scatter/waterfall/funnel/candlestick/heatmap/sankey charts, plus text, image, audio, video, and embed content types under a v3 two-level layout system (4 layout modes x 5 content patterns). It enforces a data density cap of 10 data points per figure (with quartile downsampling) and semantic palette naming. Use when you want to turn structured content, reports, or data into an interactive card-based presentation viewable in a browser.

**中文描述**: 一个基于卡片的演示技能，为 Card Box Viewer 生成结构化 JSONL 牌组文件。支持 30+ 种可视化模式，包括表格、柱状图、雷达图、折线图、饼图、散点图、瀑布图、漏斗图、K线图、热力图、桑基图等，以及 v3 双层布局系统（4 种布局模式 x 5 种内容类型）。强制每张图表最多 10 个数据点（超过时按四分位降采样），并使用语义化调色板命名。适用于将结构化内容、报告或数据转化为可在浏览器中查看的交互式卡片演示。

---

## Updated Skills

None this week.
