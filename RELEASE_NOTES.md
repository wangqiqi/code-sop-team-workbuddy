# 版本发布说明

## v1.5.4（2026-11-24）

新增 GitHub Actions CI/CD：验证通过后自动打包并发布 Release。

### 本次变化

- 新增 `.github/workflows/ci.yml`：PR / push main 时在 Ubuntu + Windows 双平台跑 schema 校验与 43 用例回归，通过后打包 zip 作为构建产物。
- 新增 `.github/workflows/release.yml`：推送 `v*` 标签时复用 CI，校验标签与插件版本一致后自动创建/更新 GitHub Release 并上传 `code-sop-team.zip`。
- 新增 `scripts/validate_package.py`：弥补官方校验器不检查 `members[].name`（en/zh）的缺口，把客户端解析失败固化成 CI 断言。
- 新增 `scripts/build_package.py`：标准库打包，先校验后压缩，排除 CI/开发脚本与缓存，产物可复现。
- 补齐仓库中的 `settings.json`（Team 类型必需，此前只存在于已发布 zip 中）。

### 包含内容

- 13 名成员、8 个技能、14 种人格话术
- 四道硬闸门：规划闸 `gate-check`、验收闸 `task-verify`、出口闸 `verify`、补丁循环闸 `followup`
- `sop_gate.py` 闸门脚本、43 个零依赖回归用例
- 13 张成员头像 + 1 张团队封面

### 安装方式

1. 在本仓库 **Releases** 页面下载 `code-sop-team.zip`
2. 解压到 `<WorkBuddy 专家目录>/plugins/marketplaces/my-experts/plugins/`
3. 重启或刷新 WorkBuddy，在【专家中心-我的专家】中查看

源码方式：克隆本仓库后，把仓库根目录作为专家包目录使用。

### 自检

在新机器或闸门报错时，先运行：

```bash
python bin/sop_gate.py doctor --root <你的项目根>
```

回归套件：

```bash
python tests/test_sop_gate.py
```
