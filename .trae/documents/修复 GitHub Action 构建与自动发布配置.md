# 修复 GitHub 提交与 Release 自动发布问题

经过排查，发现当前存在以下问题：
1.  **提交未推送**：您的本地分支比远程分支超前 1 个提交，需要执行推送。
2.  **构建脚本阻塞**：`build_exe.bat` 中包含 `pause` 命令，会导致 GitHub Actions 在构建 Windows 版本时无限等待直至超时失败。
3.  **缺少 Release 配置**：GitHub Actions 工作流文件 (`build.yml`) 中只配置了上传 Artifacts，缺少创建 Release 发布的步骤。

## 修复计划

### 1. 修正构建脚本
- **操作**：修改 `build_exe.bat`。
- **内容**：删除末尾的 `pause` 命令，确保自动化构建能正常结束。

### 2. 配置自动发布 (Release)
- **操作**：升级 `.github/workflows/build.yml`。
- **新增功能**：
    - 添加 `workflow_dispatch` 触发器（允许手动触发构建）。
    - 添加 `tags` 触发器（当推送 `v*` 标签时自动触发）。
    - 集成 `softprops/action-gh-release`，实现构建完成后自动创建 Release 并上传 `.exe` 和 `.dmg` 文件。

### 3. 提交与验证
- **操作**：
    1. 提交上述代码更改。
    2. 创建一个新的版本标签（`v1.0.1`）。
    3. 推送代码和标签到 GitHub。
- **预期结果**：这将直接触发新的 GitHub Action，自动构建并发布 `v1.0.1` 版本 Release。

执行完毕后，您只需等待 Action 运行完成，即可在 GitHub 仓库的 "Releases" 页面看到生成的安装包。