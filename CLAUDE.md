# CLAUDE.md

## 工作原则

本项目的所有任务（除用户对话外）必须委派给 Agent 执行。

## Agent 使用规则

1. **优先匹配已有 Agent**：根据任务类型，从已安装的 Agent 中选择最合适的。已知可用 Agent 列表见 `/agents` 命令输出。
2. **无合适 Agent 时临时配置**：如果现有 Agent 都不能胜任，才在当前会话中临时创建/配置适合的 Agent。
3. **独立任务并行**：多个互不依赖的任务应当并行派发多个 Agent，不串行等待。
4. **主会话仅负责**：
   - 与用户对话（回答问题、询问需求、汇报进度）
   - 阅读文件了解上下文后编写 Agent prompt
   - 汇总 Agent 返回结果告知用户
5. **Agent 负责**：所有文件读写、代码编写、Bash 执行、搜索、网页抓取等实际执行工作。

## Agent skills

### Issue tracker

Issues are tracked in the GitHub Issues of the linked repository. See `docs/agents/issue-tracker.md`.

### Triage labels

Uses the canonical five-role vocabulary with default names. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout: one `CONTEXT.md` at the repo root and `docs/adr/` for architectural decisions. See `docs/agents/domain.md`.