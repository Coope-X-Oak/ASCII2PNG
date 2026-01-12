# GitHub 自动构建 EXE 和 DMG 计划

既然您希望保持本地项目整洁，我们将把构建逻辑全部集成到 GitHub Actions 中，不在本地创建额外的构建脚本文件。

## 1. 代码适配 (`web_app.py`)
为了让云端构建出来的程序能正常运行，必须修改主程序：
-   **资源路径适配**：添加对 `sys._MEIPASS` 的支持，确保程序能找到打包进 exe 的网页模板和样式文件。
-   **输出路径适配**：确保生成的图片保存在用户可见的目录（exe 同级目录），而不是系统的临时文件夹。

## 2. 依赖配置 (`requirements.txt`)
-   添加 `pyinstaller`，这是构建所需的唯一额外库。

## 3. GitHub Actions 配置 (`.github/workflows/build.yml`)
我们将直接在配置文件中定义构建命令，区分 Windows 和 macOS 的语法差异：
-   **Windows Job**：执行 `pyinstaller --onefile --add-data "templates;templates" ...` 生成 `.exe`。
-   **macOS Job**：执行 `pyinstaller --onefile --add-data "templates:templates" ...` 生成二进制文件，并使用 `create-dmg` 打包为 `.dmg`。
-   **Release Job**：当您打 `v*` 标签时，自动发布并上传这两个文件。

## 执行结果
您只需提交代码并推送标签（如 `v1.0`），GitHub 就会自动开始构建，完成后您可以在 Releases 页面直接下载 `ASCII2PNG-Windows.exe` 和 `ASCII2PNG-macOS.dmg`。

请确认是否执行此计划？