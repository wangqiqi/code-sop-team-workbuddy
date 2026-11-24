# 版本发布说明

## v1.5.3（2026-11-24）

代码工程 SOP 专家团首次公开发布。

### 包含内容

- 13 名成员、8 个技能、14 种人格话术
- 四道硬闸门：规划闸 `gate-check`、验收闸 `task-verify`、出口闸 `verify`、补丁循环闸 `followup`
- `sop_gate.py` 闸门脚本、43 个零依赖回归用例
- 13 张成员头像 + 1 张团队封面

### 本版修复

- `plugin.json` 的 `members[]` 改用官方运行时要求的 `name` 字段（此前客户端报 `members[0].name 的 en/zh 均为必填`）
- `doctor` 增加 git 钩子内嵌脚本与解释器路径的有效性自检，避免「报 OK 但钩子已软降级」
- `displayDescription.zh` 压缩到规范要求的 40–50 字区间

### 安装方式

1. 在本仓库 **Releases** 页面下载 `code-sop-team.zip`
2. 解压到 `<WorkBuddy 专家目录>/plugins/marketplaces/my-experts/plugins/`
3. 重启或刷新 WorkBuddy，在【专家中心-我的专家】中查看

源码方式：克隆本仓库后，把仓库根目录作为专家包目录使用（`package_expert.py` 可直接对其打包）。

### 自检

在新机器或闸门报错时，先运行：

```bash
python bin/sop_gate.py doctor --root <你的项目根>
```

回归套件：

```bash
python tests/test_sop_gate.py
```
