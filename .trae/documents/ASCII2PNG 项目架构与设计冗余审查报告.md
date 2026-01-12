# ASCII2PNG 项目架构与设计冗余审查报告

基于对项目代码库的深入静态分析，我为您整理了关于系统架构、代码实现、数据存储和部署运维四个层面的详细审查报告。

## 1. 系统架构层面 (System Architecture)

### 🔴 **核心业务逻辑严重重复**
- **表现**：`main.py` (Desktop GUI) 和 `web_app.py` (Web Service) 独立且重复地实现了 "解析(Parse) -> 布局(Layout) -> 渲染(Render)" 的全流程逻辑。
- **影响**：
    - **维护困难**：修改渲染逻辑（如新增布局模式）需同时修改两处代码。
    - **行为不一致**：目前 Web 端和 GUI 端对颜色（Hex vs RGB）的处理逻辑已存在差异，导致相同输入可能产生不同输出。
- **优化建议**：
    - **高优先级**：创建 `ascii2png.core` 模块，封装 `ProcessService` 类，统一处理参数校验、主题解析和渲染调用。`main.py` 和 `web_app.py` 仅作为轻量级的接入层（Controller）。

## 2. 代码实现层面 (Code Implementation)

### 🟠 **硬编码与工具类缺失**
- **表现**：
    - **颜色解析**：GUI 使用自定义 `hex_to_rgb`，Web 使用 `PIL.ImageColor`，缺乏统一的 `ColorUtils`。
    - **文件名生成**：`render.py` 中的 `_save_png` 强制使用时间戳命名格式，调用者无法自定义输出文件名，导致 Web 端只能通过 hack 方式传递信息。
- **优化建议**：
    - 提取 `ascii2png.utils` 模块，统一处理颜色转换、文件命名和路径管理。
    - 修改 `render_scene` 接口，支持传入完整的 `output_path` 而非仅 `output_dir`。

## 3. 数据存储层面 (Data Storage)

### 🔴 **文件存储泄露与无限增长**
- **表现**：
    - **Web 端无清理**：`web_app.py` 将生成的图片永久保存在 `output/` 目录，缺乏定期清理机制（TTL），长期运行将耗尽服务器磁盘。
    - **临时文件残留**：`render.py` 的 `_shrink_png` 函数在压缩尝试过程中会生成 `_opt0.png`, `_opt1.png` 等中间文件，若最终选择了后续版本，**前面的失败尝试文件未被删除**。
- **优化建议**：
    - **高优先级**：修复 `_shrink_png`，使用 `tempfile` 库或显式删除中间文件。
    - Web 端引入后台任务（如 APScheduler）定期清理过期文件，或改用内存流（BytesIO）直接返回图片而不落盘。

## 4. 部署运维层面 (Deployment & Ops)

### 🟡 **CI/CD 流程冗余**
- **表现**：
    - **双重依赖安装**：`.github/workflows/build.yml` 中先执行了 `pip install -r requirements.txt`，随后调用的 `build_exe.bat` 内部**再次**执行了相同的安装命令。这浪费了 CI 构建时间。
    - **依赖管理混淆**：`pyinstaller` 被列在 `requirements.txt` 中（通常视为运行时依赖），但实际上它仅是构建时工具。
- **优化建议**：
    - 优化 `build_exe.bat`，增加参数跳过依赖安装，或在 CI 中仅调用脚本。
    - 将 `pyinstaller` 移至 `dev-requirements.txt` 或仅在 CI 流程中安装。

## 总结与行动计划

| 优先级 | 问题领域 | 核心动作 | 预期收益 |
| :--- | :--- | :--- | :--- |
| **P0 (最高)** | 架构 | 提取 `CoreService` 统一业务逻辑 | 消除 50% 重复代码，确保多端一致性 |
| **P0 (最高)** | 存储 | 修复 `render.py` 临时文件泄露 | 防止磁盘空间无端浪费 |
| **P1** | 运维 | 优化 CI/CD 脚本与依赖安装 | 缩短构建时间，规范依赖管理 |
| **P2** | 代码 | 统一颜色处理与工具类 | 提升代码可读性与健壮性 |

建议首先着手解决 **P0 级别的架构统一与文件泄露问题**，这将为后续功能的稳健扩展打下基础。