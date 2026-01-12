# ASCII2PNG Web

ASCII2PNG 是一个基于 Web 的工具，用于将 ASCII 树状图/层级知识架构图转换为适配微信阅读的 PNG 图片（宽度 1080px，高度自适应）。

## 特性

- **Web 界面**：简洁易用的浏览器界面，支持实时预览。
- **多种主题**：支持 WeChat、Light、Dark 等多种配色主题。
- **智能布局**：自动解析 ASCII 树形结构，生成清晰的 PNG 图片。
- **移动端优化**：固定宽度 1080px，字体大小适中，适合在手机上阅读。
- **文件优化**：自动控制输出文件大小在 1MB 以内，方便分享。

## 使用方式

### 方法一：Windows 一键启动（推荐）

直接双击运行项目目录下的 `start.bat`。
- 脚本会自动检查依赖并启动服务。
- 浏览器会自动打开 [http://localhost:5000](http://localhost:5000)。

### 方法二：命令行启动

1. **环境要求**
   - Python 3.8+
   - pip

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动应用**
   ```bash
   python web_app.py
   ```
   启动后，浏览器会自动访问 [http://localhost:5000](http://localhost:5000)。

### 方法三：Docker 部署

本项目支持 Docker 容器化部署：

1. **构建镜像**
   ```bash
   docker build -t ascii2png .
   ```

2. **运行容器**
   ```bash
   docker run -p 5000:5000 ascii2png
   ```
   访问 [http://localhost:5000](http://localhost:5000) 使用。

## API 接口

应用提供 REST API 用于自动化集成：

- **POST /generate**
    - JSON Body:
        - `text`: ASCII 文本内容 (必填)
        - `theme`: 主题 (可选: `wechat`, `light`, `dark`, 默认 `minimal`)
        - `width`: 图片宽度 (可选, 默认 1080)
        - `font`: 字体大小 (可选, 默认 24)
    - 返回: `{"image_url": "/output/..."}`

## 目录结构

- `web_app.py`: Web 应用入口 (Flask)
- `start.bat`: Windows 一键启动脚本
- `Dockerfile`: Docker 构建文件
- `ascii2png/`: 核心逻辑包
    - `core.py`: 转换核心服务
    - `render.py`: 渲染引擎
    - `parser.py`: 文本解析
- `templates/`: HTML 模板
- `static/`: 静态资源
- `tests/`: 单元测试

## 许可
本项目用于示例与个人使用，可自由扩展。
