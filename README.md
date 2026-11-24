# 代码工程 SOP 专家团（code-sop-team）

把"聊完就散"的开发协作变成**先规划、可验收、能连跑**的团队级工程流程。转化自 Super Cursor v5.1.15 的 SOP（`E:\cursor-ai`），面向 WorkBuddy 重新设计。

## 类型

Team 型（**13 角色，4 常驻 + 9 按需**）：主理人 + 规划/审查/发版 3 位常驻，加上产品、架构、测试、安全、设计、数据、调研、鼓励、事务 9 位按需专家。

## 角色

> **13 人是菜单，不是仪仗队。** 默认只请 4 位常驻（主理人 + 规划 + 审查 + 发版），其余 9 位按需求信号触发。判断标准只有一条：**这个人有没有独立的、别人替代不了的判断？**
>
> 只有**立场对立**的角色才值得拆成独立的人——规划想开工、审查想拦住、安全想假设已被攻击、数据想先能回滚、设计想一屏一个主按钮。测试/调试/性能/重构是同一立场下的不同方法，所以只出 1 位测试工程师，不拆 4 个。

### 常驻核心（4）

| Agent ID | 花名 | 职业 | 职责 | 只读 |
|---|---|---|---|---|
| code-sop-team-team-lead | 齐活林 | 交付总监（主理人） | 路由、编排、驱动执行、守卫四道闸门 | 否 |
| sprint-planner | 许清楚 | Sprint 规划师 | 冻结 Goal/Done/Out of scope、MECE 拆 TASK、plan 维护 | 否（只写 plan） |
| code-reviewer | 严过关 | 代码审查官 | 双轴审查 Standards/Spec、按栈核对、问题分级 | ✅ |
| release-engineer | 毕达成 | 发版工程师 | verify、CHANGELOG、版本、tag、push 策略 | 否 |

### 按需专家（9）

| Agent ID | 花名 | 职业 | 何时请 | 只读 |
|---|---|---|---|---|
| product-manager | 文知需 | 产品经理 | 需求说不清、诉求冲突、要做取舍、验收标准写不成命令 | ✅ |
| architect | 梁定边 | 架构师 | 新项目起步、跨模块改、要不要重构、加中间件 | ✅ |
| qa-engineer | 查必现 | 测试工程师 | 设计验收命令、定回归范围、缺陷复现、反复失败 | 可写测试文件 |
| security-engineer | 卫无漏 | 安全工程师 | 登录权限、密钥、支付、上传、对外 API、隐私数据 | ✅ |
| ux-designer | 颜可悦 | UI/UX 设计师 | 新页面、导航乱、体验差、设计规范缺失 | ✅ |
| data-engineer | 石不移 | 数据工程师 | 加表改字段、迁移、查询慢、数据对不上 | ✅ |
| tech-spiker | 高见远 | 技术调研员 | 方案选型、可行性、根因分析 | ✅ |
| morale-booster | 古小励 | 程序员鼓励师 | 仅情绪节点：BLOCK / 验收失败 / 打回 / 收尾 / 发版成功 | ✅（不刷屏） |
| engineering-steward | 舒井然 | 工程事务官 | 环境/依赖/仓库整洁、SOP 归档、README/CHANGELOG 草稿 | ✅（仅草稿可写） |

## 能力资产（8 个 skill）

| Skill | 内容 | 谁挂载 |
|---|---|---|
| `sop-gate` | 四道闸门执行器 + 闸门语义 + 14 种人格话术 + **团队宪法** + **异常/边界/兜底手册** | 全团 |
| `stack-conventions` | 技术栈约定：TS/JS/ESLint、React/Vue/Svelte/Next、Python/Go/Java、Rust/C/C++ | 主理人、审查官、测试、安全、设计、数据 |
| `quality-checklists` | 安全清单、API 契约、测试分层、调试循环、**补丁循环拦截**、性能手册、重构协议 | 审查官、测试、调研员 |
| `product-spec` | 需求澄清四问、用户故事、**验收标准可执行化**、MVP 取舍、范围谈判 | 产品经理 |
| `architecture-design` | 边界划分、依赖方向、ADR、技术债、数据层（schema/迁移/索引/备份/一致性） | 架构师、数据工程师、安全 |
| `ux-design` | 信息架构、交互流程、**六态设计**、视觉 token、可用性走查 | 设计师 |
| `delivery-contracts` | 交付七维验收、测试报告契约、使用说明书契约 | 发版官、事务官 |
| `release-ops` | Git 纪律、发版 4 选 1 + semver、部署、脚手架、长程三层 | 主理人、规划师、发版官、事务官 |

## 核心：四道硬闸门

1. **规划闸** `gate-check`：无 PLAN_APPROVED 或 PLANNING=true → 禁止写业务代码。`approve` 自带前置校验：VERIFY 未设或 plan-check 未过直接 BLOCK。
2. **验收闸** `task-verify`：每任务验收命令必须 PASS 才能标 ✅/commit；描述性验收 fail-closed 直接 FAIL；`manual:` 验收须 `--evidence` 留证（否则 rc=3，不算 PASS）。
3. **出口闸** `verify`：Sprint 收尾/打版前，要求**任务全部 ✅ + VERIFY 命令退出码 0**，两者都过才收口；残项需 `--force` 且用户明确接受。`VERIFY` 由规划师写 plan 时设定——这是出口闸可达的唯一保证。若 plan 未设 VERIFY，脚本会回退探测既有入口（`scripts/verify.py|test.py` → `package.json` → pytest → `scripts/*.sh`）并标 `[AUTO-DETECTED]`，但**不放宽任何 PASS 标准**。
4. **补丁循环闸** `followup`：`task-verify` 每次失败会累加该任务的连续失败轮次，**第 2 次失败**即输出 `FOLLOWUP-GATE`，禁止继续打补丁，必须立 `SPIKE-*` 定位根因。任务真 PASS 后计数自动清零。这是「别把一个 bug 修成架构债」的硬保护。

### 跨机器设计（重点）

硬约束不依赖原仓的 bash 脚本 + Cursor hooks（那套依赖 Git Bash/jq/固定目录，换机就废）。本专家团改为：

| 层 | 实现 |
|---|---|
| 闸门执行 | `bin/sop_gate.py`，Python 标准库、零依赖、Win/Mac/Linux 通吃 |
| 回归测试 | `tests/test_sop_gate.py`，43 用例、零依赖，改闸门后必跑 |
| 状态存放 | `<项目根>/.workbuddy/sop/plan.md`，自动探测项目根（`--root` > `SOP_PROJECT_ROOT` > 向上找 `.git` > cwd） |
| 脚本定位 | 三级探测：`$SOP_GATE` > `~/.workbuddy/plugins/marketplaces/*/plugins/code-sop-team/bin/` > 项目级 `.workbuddy/plugins/*/`，不写死用户名与目录 |
| 运行时 | **不需要用户自己装 Python**：WorkBuddy 桌面版内置受管 Python（本机 3.13.12，`~/.workbuddy/binaries/python/versions/3.13.12/python.exe`，通常不在 PATH）；普通 Windows 本身不自带 Python。在会话里用当前解释器即可 |
| 触发 | 软约束（MD 铁律强制跑命令并贴输出）+ 可选硬约束（`install-hook` 装 git pre-commit，提交前跑 plan-check + gate-check 双闸；**钩子内嵌当前解释器绝对路径，不依赖 PATH**；仅内嵌路径与 PATH 都失效时才告警软降级；重复执行自动升级旧钩子） |
| 推进 | `next-task --apply` 把下一个 ACTIVE 写回 plan.md；`approve` 带 VERIFY + plan-check 前置校验 |
| 自检 | `doctor` 一次查完 Python/脚本/skill/项目根/plan 解析/批准格式/证据/状态锁/钩子及钩子内嵌路径有效性；新机器或闸门报错时先跑它 |
| 并发与异常 | `.workbuddy/sop/.lock` 原子锁保护状态读-改-写（陈旧锁自动清理）；批准值/任务 ID/状态格强校验；超时杀进程树；`failure-playbook.md` 覆盖降级模式 |

脚本随专家包走，安装到任意 Windows 机器后，在任意项目里启用专家团即可用，状态自动在项目内生成。

### 人工验收的证据链

`manual:` 验收不再是免检通道：

```bash
# 1) 首次跑：返回退出码 3（MANUAL-PENDING），明确不算 PASS
python sop_gate.py task-verify TASK-002
# 2) 按验收要求人工核对后，带证据重跑 → PASS，证据入档
python sop_gate.py task-verify TASK-002 --evidence "复核人:张三, 订单页 1280x800 无遮挡, 截图 docs/qa/order.png"
```

证据存于 `.workbuddy/sop/evidence.json`（任务、证据正文、时间戳、原始验收要求），可随时复核。

### 异常与兜底（不只是 happy path）

`skills/sop-gate/references/failure-playbook.md` 是异常矩阵的 SSOT：退出码语义、批准值伪造、重复 ID / 状态歧义、空白证据、证据损坏、状态锁竞争、超时与 Ctrl+C、钩子残留、非 git 仓库、**工具缺失时的降级模式**，以及团队侧「卡片/建团/spawn 不可用、成员无响应、结论冲突、会话中断恢复」。

三条铁律：**判定不了 = 不通过**；**工具不可用 = 显式声明降级**；**绝不伪造闸门输出或成员结论**。主理人 MD 里也内嵌了常见异常分支表。

## 使用示例

- 我要开发一个功能，请先用规划师冻结目标、拆解任务，等我确认后再执行。
- 帮我审查当前改动能不能合并，按严重度列出 Blocker 和 High。
- 这两个技术方案帮我对比一下，给出明确推荐和任务拆分建议。
- 帮我规划这个需求，拆成 Sprint，我确认后再开工。
- 按清单发个版，先跑 verify，绿了再打 tag。
- 核对一下依赖和环境有没有不一致，顺便看看仓库脏不脏。
- 我快崩了，给点鼓励（连续补测两轮还没过）。
- 这 bug 我已经修了三次还没好，帮我判断该不该换个思路。
- 这个 Epic 要跨好几个 Sprint，帮我按三层拆一下。
- 这需求我自己都说不清，帮我理清楚要解决谁的什么问题。
- 这个项目的结构该怎么分层？哪些地方三个月后会疼？
- 这个接口谁都能传 userId，帮我看看安全上有没有洞。
- 我要加个字段还要写迁移，怎么保证能回滚？
- 后台这个列表页用户总说找不到入口，帮我看看信息架构。

## 开场交互（多轮卡片问询）

会话开始前主理人会用 `AskUserQuestion` 逐张卡片问询，一项一张、填完再问下一张，收齐才开工：

1. **沟通人格**（全局覆盖，可选；14 种：卡片列 4 种 + 自由输入其余 10 种）→ 2. **项目归属** → 3. **功能与问题** → 4. **协作阵容**（多选：常驻四人组 / 产品&架构 / 测试&安全 / 设计&数据）→ 5. **代码目录** → 汇总确认 → 建团队按阵容派成员。

第 4 张卡是这次新增的：**由你决定请哪些专家**。主理人会根据第 3 张卡的需求给建议（比如检测到登录鉴权就提示勾选"测试&安全"），但拍板权在你。跳过不选就用常驻 4 人。

若你首条消息已给全信息，会跳过问询直接路由，缺哪项只补问哪项。无 AskUserQuestion 工具时降级为正文逐项提问，每次只问一项。

## 人格（两层）

- **默认层**：13 位成员各有绑定语气——齐活林=专业搭档、许清楚=知音、严过关=严师、毕达成=御姐、文知需=分析师、梁定边=架构师、查必现=探针、卫无漏=守卫、颜可悦=匠人、石不移=守望、高见远=老者、古小励=萝莉、舒井然=女仆。共 14 种人格（含未绑定的"硬汉"）。不选时团队像"性格各异的一群人"。
- **覆盖层**：开场第 1 张卡选的人格一次性覆盖全团措辞，也可指定某专家保持本色。

人格只影响语气，**不降低任何验收标准**（审查分级、发版失败即停永远从严）。映射与话术见 `skills/sop-gate/references/personas.md`。

**语气是人的属性，不是阶段的属性**：许清楚在规划、执行、报告阶段都是知音，严过关在哪一阶段都是严师——不会因为「进入执行阶段」就换一种人格。要让全团统一气质，用开场第 1 张卡的覆盖层，而不是给每个流程换语气。

## 头像

`avatars/` 含 **13 张成员头像 + 1 张团队封面 `team.png`**（512×512，≤500KB，绿调日系插画 + 手持职业道具 + 悬浮示意图，统一画风）。如需替换：PNG/JPG，512×512，≤500KB，保持绿调统一。

## 安装

专家已注册到 `<WorkBuddy 专家目录>/plugins/marketplaces/my-experts/plugins/code-sop-team`，重启/刷新 WorkBuddy 后在【专家中心-我的专家】可见。分享给他人：把 `code-sop-team.zip` 解压到对方专家目录后运行注册脚本。

## 变更记录

**v1.5.3**（2026-11-18）— 修复专家中心解析失败（43 用例全绿）
- `plugin.json` 的 `members[]` 字段由 `displayName` 改为官方运行时要求的 `name`（`{en, zh}`）。此前客户端报「members[0].name 的 en/zh 均为必填」，导致专家团无法加载。
- `displayDescription.zh` 从 61 字压到 46 字，满足规范的 40–50 字要求，校验脚本不再告警。

**v1.5.2**（2026-11-18）— 钩子有效性自检（43 用例全绿）
- `doctor` 现在解析 git pre-commit 内嵌的 `_SOP_PY` / `_SOP_PY_BIN` 并校验路径：专家包移动、受管 Python 升级后不再只是「报 OK」，而是显式 FAIL（PATH 也无 Python 时），杜绝「医生绿灯、钩子却软降级」。
- README 去掉硬编码本机专家目录，改为通用占位；头像数量描述修正为 13 张成员图 + 1 张团队封面。

**v1.5.1**（2026-11-18）— Python 运行时适配（42 用例全绿）
- **普通 Windows 不自带 Python**：官方文档明确 Windows 不含系统级 Python，`python` 常只是 Microsoft Store 占位入口；**WorkBuddy 桌面版自带受管 Python 3.13**，但通常不在 PATH。
- `install-hook` 现在把**当前解释器绝对路径**内嵌进 git 钩子（沿用 POSIX 单引号转义，兼容含 `$`/空格的路径），钩子不再依赖 PATH；仅当内嵌路径与 PATH 都找不到 Python 时，才打印告警并软降级。
- `sop-gate/SKILL.md`、`failure-playbook.md`、README 与异常矩阵补充三种运行时情形（普通 Windows / WorkBuddy 受管 Python / 完全无 Python）的定位与兜底。
- 回归套件 41 → 42 用例，新增钩子内嵌解释器断言。

**v1.5.0**（2026-11-18）— 异常 / 边界 / 兜底专项加固（41 用例全绿）
- **批准值可伪造**：`PLAN_APPROVED: hacked` 任意非空字符串都能解锁 `gate-check`。现只认 `YYYY-MM-DD` 真实日期，`set` 也按键校验（布尔/计数/任务 ID 同样校验）。
- **空白人工证据放行**：`--evidence "   "` 会写入 evidence.json 并 PASS。现空白视同未提供（rc=3），超长证据截断并提示改存文件。
- **重复任务 ID / 状态歧义**：重复 ID 会被字典后者覆盖造成假完成，`⬜ ✅` 混写让 plan-check 与 verify 各取所需半边。现两者均 fail-closed，plan-check / verify 直接 FAIL。
- **多反引号取错命令**：「在 `src/` 目录执行 `echo ok`」会去执行路径片段。现优先挑「像命令」的反引号内容。
- **钩子残留标记**：只有 `BEGIN` 没有 `END` 时重装会产生双标记，卸载会误删用户自己的钩子。现拒绝安装且**不改动原文件**。
- **超大超时 Traceback**：`SOP_VERIFY_TIMEOUT` 传超大整数会在 Windows `time.monotonic` 里 OverflowError。现钳到 24h 并警告；负数/非法值也有明确退化。
- **环境指错静默跑错项目**：`SOP_PROJECT_ROOT` 无效时原先静默退回 cwd。现 rc=2 显式拒绝。
- **plan 路径是目录 / 文件被占用**：不再 Traceback；读取异常按空处理让闸门 fail-closed，写入失败明确报错并短重试。顶层兜底把任何意外异常转为 `INTERNAL-ERROR` + rc=1，绝不漏出假绿灯。
- **并发状态竞态**：plan / evidence / followup 的读-改-写统一加 `.lock` 原子锁（120s 陈旧自动清理，等待超时 BLOCK），`next-task --apply` 拿锁后重读 plan 以遵守编辑主权；负的失败计数钳到 0（否则补丁闸被静默关闭）。
- **`.gitignore` 幂等增强**：识别 `.workbuddy/sop/*` 等已有写法，不再每次 init 重复追加；hook 与 gitignore 写入也改原子写。
- **---force 零任务显式 WARN**；`doctor` 新增批准格式与状态锁自检。
- **新增 `failure-playbook.md`**：工具/团队协作的异常矩阵与降级模式；主理人 MD 与宪法同步；回归套件 26 → 41 用例。

**v1.4.3**（2026-11-18）— 穷举测试后再修 8 处
- **验收命令被表格管道符截断**：`parse_tasks` 直接 `split("|")`，`echo a | grep a` 被切成两列 → 执行半截命令（轻则失败，重则变成另一条能跑通的命令 = fail-open）。现保护 `\|` 转义并在未转义时把多余列并回 Acceptance，命令不再被截断。
- **VERIFY 回退探测硬编码 `python`**：只有 `python3` 的 Linux/macOS 上探测出的命令必然失败。改用当前解释器名。
- **钩子路径被 shell 展开**：专家包装在含 `$` 的路径（如 `dir$name`）时，双引号里的 `$name` 被展开 → 脚本路径残缺、闸门静默失效。改用 POSIX 单引号转义（`'` → `'\''`）；同时脚本不存在时由放行改为 **BLOCK**。
- **超时保护是假的**：`shell=True` + `timeout` 只杀 shell，子进程继续占着 stdout 管道，`communicate()` 照样等到天荒地老。改用 `Popen` + 进程组，超时杀整棵树（Windows 用 `taskkill /T /F`，POSIX 用 `killpg`）。
- **畸形 evidence 崩溃**：`{"TASK-001": 123}` 让 `have.get(...)` 抛 `AttributeError`。`load_evidence` 加结构校验；doctor 报出「内容损坏」。
- **任务 ID 无锚定**：`TASK-001abc` 被当成合法主任务。正则加 `$`。
- **元数据注入**：`set` 的 value 含 `-->` / `<!--` / 换行会破坏 plan 结构，现直接拒绝（rc=2）。
- **新增回归测试套件** `tests/test_sop_gate.py`（26 用例，标准库零依赖），把以上全部 bug 与四道闸门语义固化；doctor 检查套件存在性。改动闸门脚本后必须跑全绿才可打包。

**v1.4.2**（2026-11-18）— 全量复审
- **人工证据与验收要求解绑**（fail-open）： Acceptance 改过之后，旧 `--evidence` 仍会让 `task-verify` 直接 PASS。现证据与留证时的验收要求绑定，要求变化即失效（返回 3 要求重留）；老版本无 `acceptance` 字段的证据同样要求重留。
- **状态文件不再入库**：`init` 幂等自动把 `.workbuddy/sop/` 写进 `.gitignore`（此前只口头建议，实测 commit 会把 plan 与验收证据一起提交 → 多会话互相覆盖）。已跟踪的文件给出 `git rm --cached -r` 修法；`doctor` 检查跟踪状态。
- **验收命令加超时**：默认 10 分钟，`SOP_VERIFY_TIMEOUT=<秒>` 可覆盖，`0` 表示不限。防止 watch 模式 / 交互命令 / 死循环把闸门永久挂死。
- 文档同步：`sop-gate/SKILL.md`、`gate-semantics.md` 补上三条新行为。

**v1.4.1**（2026-11-18）
- **修一个 fail-open 缺陷**：`verify`（出口闸）在 plan 解析不到任何 `TASK` 行时会直接放行——「plan 被改坏」会被误判成「全部完成」。现改为 fail-closed（解析到 0 个主任务 → FAIL，`--force` 才放行），并顺带把未完成的 SPIKE/REV/DOC 列出来提示。
- 状态文件（plan / evidence / followup）改为**原子写**（临时文件 + `os.replace`）。此前直接 `write_text`，中断或并发写会留半截文件，而读取侧的 `except` 会把它当空——证据静默丢失。
- 新增 **`sop-gate/references/constitution.md`（团队宪法）**：三公理（意图主权/信号可信/认知可审计）+ **编辑主权**（多 agent/多会话并发写同一仓库的纪律，吸收 `.cursor` 的 multi-session-edits）+ 反幻觉纪律（吸收 agent-discipline）。主理人 spawn 成员时随任务下发。
- 三个新 skill 完成**分层重构**：`product-spec` / `architecture-design` / `ux-design` 从单文件（112–162 行）改为「SKILL.md 路由 + 3–4 份 references」，与原有 4 个 skill 结构统一，加载成本显著下降。
- 补 3 处 skill 绑定缺口：安全、数据、设计都挂上 `stack-conventions`（安全要看 `dangerouslySetInnerHTML`/SQL 拼接，数据要看迁移语法，设计要给前端可落地的值）。

**v1.4.0**（2026-11-18）
- 团队扩编 7→13 人，形成**4 常驻 + 9 按需**两层结构（13 人是菜单不是仪仗队）。
- 新增 6 位专家：产品经理（文知需）、架构师（梁定边）、测试工程师（查必现）、安全工程师（卫无漏）、UI/UX 设计师（颜可悦）、数据工程师（石不移）。
- 新增 3 个 skill：`product-spec`（需求澄清 + **验收标准可执行化**）、`architecture-design`（边界/依赖/ADR/技术债/数据层）、`ux-design`（IA/交互/**六态设计**/视觉 token/可用性走查，吸收 .cursor 的 ux+ia）。
- 人格池 8→14 种：新增 analyst / architect / prober / guard / artisan / curator。
- 主理人开场加第 4 张卡「协作阵容」（多选），由用户决定请哪些专家，主理人按需求预判给建议。
- 新增 Workflow G（需求澄清）/ H（结构设计）/ I（UI 设计与走查）/ J（数据变更）；Phase 0 需求澄清前置；Phase 2 加安全与数据强制触发规则。
- 生成 6 张统一画风头像。

**v1.3.0**（2026-11-18）
- 补齐 `.cursor` 重要 SOP 缺口，新增 skill `stack-conventions`（吸收 13 份 `rules/tech/*.mdc`）。
- `quality-checklists` 新增 `api-contract.md`（吸收 api skill + input-bounds.mdc）与 `patch-loop.md`（吸收 async-progress / long-running-ui / modal-layering / error-context / single-detector / scope.mdc）。
- 新增**第四道闸门·补丁循环闸**：`task-verify` 失败自动累加轮次，≥2 轮触发 `FOLLOWUP-GATE` 强制转 SPIKE；新增 `followup` 子命令（查看/清零）。
- `verify` 增加 VERIFY 回退探测（跨平台有序），`doctor` 报告探测结果与补丁计数。
- 全团 MD 从「三道闸门」升级为「四道闸门」。

**v1.2.0**（2026-11-18）
- `plan-check` 区分 WARN/INFO：全部任务 ✅ 不再判 FAIL，修复钩子永久拦住 commit 的致命问题。
- git pre-commit 改为**双闸**（plan-check + gate-check），旧版钩子可原地升级。
- `manual:` 验收改为 rc=3 + `--evidence` 留证（原为免检直放）。

**v1.1.0**（2026-11-18）
- 团队扩编 5→7 人：新增程序员鼓励师（古小励）、工程事务官（舒井然）；人格池 6→8 种。
- 修 7 处闭环断点：规划师写 plan 并设 VERIFY、plan-check 查 VERIFY、approve 前置校验、next-task --apply、脚本路径三级探测、git 策略统一、人格覆盖写入 spawn prompt。
- 吸收原仓 13 个 skill → 3 个新 skill（quality-checklists / delivery-contracts / release-ops）。
- 新增 Workflow 0（空项目起步）、Workflow F（长程分层）。

## 打包分享

```bash
python3 scripts/package_expert.py <expert-dir> [output-dir]
```
