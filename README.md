# 端口扫描工具

一个功能强大的端口扫描程序，支持命令行和Web界面两种使用方式，基于Python技术栈实现。

## 打包工具

项目已打包为独立的可执行文件（EXE），无需安装Python环境即可运行：

- **scan_tool.exe**：命令行快速扫描工具，位于`dist`目录
- **web_tool.exe**：Web服务和API启动工具，位于`dist`目录

**说明**：这些EXE文件是通过PyInstaller打包生成的，包含了所有必要的依赖项，可以在没有Python环境的Windows系统上直接运行。

## 项目结构

```
port-scanner/
├── port_scanner/           # 核心模块
│   └── scanner.py          # 端口扫描核心功能
├── templates/              # Web界面模板
│   └── index.html          # Web界面首页
├── static/                 # 静态文件目录
├── img/                    # 图标和图片资源
│   ├── cmd.ico             # 命令行工具图标
│   └── web.ico             # Web工具图标
├── dist/                   # 打包生成的EXE文件目录
│   ├── scan_tool.exe       # 命令行快速扫描工具
│   └── web_tool.exe        # Web服务和API启动工具
├── cli_wrapper.py          # 命令行包装脚本
├── web_wrapper.py          # Web服务包装脚本
├── requirements.txt        # 依赖包配置
└── README.md               # 使用说明文档
```

## 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/xiao-girls/port-scanner.git
   cd port-scanner
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

### 1. 命令行快速扫描工具（EXE）

**双击运行**：
1. 双击`scan_tool.exe`文件
2. 直接输入目标主机地址（单个或多个，用空格分隔）
3. 选择扫描类型（单个端口、端口范围或常用端口）
4. 根据选择的扫描类型填写相应的端口参数
5. 调整超时时间和线程数（可选）
6. 查看扫描结果
7. 回答是否再次扫描（y/n）
8. 如果选择 'y'，重复步骤 2-6
9. 如果选择 'n'，退出程序

**命令行运行**：
```bash
# 扫描单个主机
scan_tool.exe scan <主机地址> [选项]

# 扫描多个主机
scan_tool.exe scan --hosts "<主机地址1> <主机地址2> ..." [选项]
```

**选项**：
- `-H, --hosts`：指定多个主机，用空格分隔
- `-p, --port`：指定单个端口
- `-s, --start-port`：起始端口（默认1）
- `-e, --end-port`：结束端口（默认1024）
- `-c, --common`：扫描常用端口
- `-t, --timeout`：超时时间（默认1.0秒）
- `-n, --threads`：线程数（默认100）

**示例**：

- 扫描单个主机的单个端口：
  ```bash
  scan_tool.exe scan 127.0.0.1 -p 80
  ```

- 扫描多个主机的单个端口：
  ```bash
  scan_tool.exe scan --hosts "127.0.0.1 192.168.1.1" -p 80
  ```

- 扫描单个主机的端口范围：
  ```bash
  scan_tool.exe scan 127.0.0.1 -s 1 -e 100
  ```

- 扫描多个主机的端口范围：
  ```bash
  scan_tool.exe scan --hosts "127.0.0.1 192.168.1.1" -s 1 -e 100
  ```

- 扫描单个主机的常用端口：
  ```bash
  scan_tool.exe scan 127.0.0.1 -c
  ```

- 扫描多个主机的常用端口：
  ```bash
  scan_tool.exe scan --hosts "127.0.0.1 192.168.1.1" -c
  ```

### 2. Web服务和API工具（EXE）

**启动Web服务**：
```bash
web_tool.exe
```

**访问地址**：
```
http://localhost:5000
```

**使用步骤**：
1. 在"目标主机"输入框中输入要扫描的主机地址
2. 选择扫描类型（单个端口、端口范围或常用端口）
3. 根据选择的扫描类型填写相应的端口参数：
   - 单个端口：输入端口号
   - 端口范围：输入起始端口和结束端口
   - 常用端口：无需输入端口参数
4. 调整超时时间（默认1.0秒）和线程数（默认100）（可选）
5. 点击"开始扫描"按钮
6. 查看扫描结果：
   - 开放端口：显示为绿色边框
   - 关闭端口：显示为黄色边框
   - 错误端口：显示为红色边框

**API端点**：

- `POST /api/scan`：端口扫描接口，支持单个端口、端口范围和常用端口扫描

**请求示例**：

```bash
# 扫描单个端口
curl -X POST http://localhost:5000/api/scan \
  -H "Content-Type: application/json" \
  -d '{"host": "127.0.0.1", "port": 80, "timeout": 1.0, "threads": 100}'

# 扫描端口范围
curl -X POST http://localhost:5000/api/scan \
  -H "Content-Type: application/json" \
  -d '{"host": "127.0.0.1", "start_port": 1, "end_port": 100, "timeout": 1.0, "threads": 100}'

# 扫描常用端口
curl -X POST http://localhost:5000/api/scan \
  -H "Content-Type: application/json" \
  -d '{"host": "127.0.0.1", "common": true, "timeout": 1.0, "threads": 100}'
```

**响应示例**：

```json
# 单个端口扫描响应
{
  "host": "127.0.0.1",
  "port": 80,
  "status": {
    "port": 80,
    "status": "closed"
  }
}

# 端口范围/常用端口扫描响应
{
  "host": "127.0.0.1",
  "open_ports": [],
  "ports": [
    {
      "port": 80,
      "status": "closed"
    }
  ],
  "scan_time": 0.11
}
```

## 技术实现

- **核心扫描功能**：使用Python的`socket`模块实现端口扫描，`concurrent.futures`模块实现多线程并发扫描
- **命令行接口**：使用`click`库实现命令行参数解析和执行
- **API接口**：使用`Flask`框架实现RESTful API
- **Web界面**：使用HTML、CSS和JavaScript实现前端界面，通过AJAX与API交互
- **打包工具**：使用`PyInstaller`将项目打包为独立的可执行文件（EXE）

## 环境要求

### 运行环境
- **Python版本**：3.7+（如果直接运行源代码）
- **操作系统**：
  - 源代码：Windows、Linux、macOS
  - 打包后的EXE文件：仅Windows系统
- **网络权限**：需要网络访问权限以执行端口扫描
- **防火墙设置**：如果运行环境有防火墙，可能需要允许程序的网络访问

### 依赖项

项目使用以下主要依赖项：
- **Flask 2.0.1**：Web框架，用于实现API接口和Web服务
- **Click 8.0.1**：命令行参数解析库，用于实现命令行接口
- **Werkzeug 2.0.1**：WSGI工具库，Flask的依赖项

## 打包方法

如果需要重新打包项目，可以按照以下步骤操作：

### 前提条件
- 已安装Python 3.7+环境
- 已安装项目依赖项（`pip install -r requirements.txt`）
- 已安装PyInstaller（`pip install pyinstaller`）

### 打包步骤

1. **打包命令行工具**
   ```bash
   pyinstaller --onefile --icon=img/cmd.ico --name=scan_tool cli_wrapper.py
   ```

2. **打包Web服务工具**
   ```bash
   pyinstaller --onefile --icon=img/web.ico --name=web_tool web_wrapper.py
   ```

3. **打包结果**
   打包完成后，生成的EXE文件会位于`dist`目录中：
   - `dist/scan_tool.exe`：命令行快速扫描工具
   - `dist/web_tool.exe`：Web服务和API启动工具

### 打包注意事项
- 打包过程中会自动收集所有必要的依赖项
- 打包生成的EXE文件较大（约8-10MB），因为包含了完整的Python解释器和依赖项
- 打包后的EXE文件只能在Windows系统上运行
- 如果修改了项目代码，需要重新执行打包命令以更新EXE文件

## API接口

### 扫描接口

- **POST /api/scan**：端口扫描接口，支持单个端口、端口范围和常用端口扫描

#### 请求参数

| 参数名 | 类型 | 描述 | 必选 |
|--------|------|------|------|
| host | string | 目标主机地址 | 是 |
| port | integer | 单个端口号 | 否（与start_port、end_port、common三选一） |
| start_port | integer | 起始端口 | 否（与port、common三选一） |
| end_port | integer | 结束端口 | 否（与port、common三选一） |
| common | boolean | 是否扫描常用端口 | 否（与port、start_port、end_port三选一） |
| timeout | float | 超时时间（秒） | 否（默认1.0） |
| threads | integer | 线程数 | 否（默认100） |

#### 响应格式

##### 单个端口扫描响应

```json
{
  "host": "127.0.0.1",
  "port": 80,
  "status": {
    "port": 80,
    "status": "closed"
  }
}
```

##### 端口范围/常用端口扫描响应

```json
{
  "host": "127.0.0.1",
  "open_ports": [],
  "ports": [
    {
      "port": 80,
      "status": "closed"
    }
  ],
  "scan_time": 0.11
}
```

## 注意事项

1. **扫描权限**：请确保您有权限扫描目标主机，避免对未经授权的主机进行扫描
2. **扫描速度**：默认使用100个线程进行并发扫描，可以根据网络环境调整线程数
3. **防火墙**：部分主机可能有防火墙保护，会影响扫描结果
4. **网络环境**：网络延迟可能会影响扫描速度和准确性

## 常用端口列表

工具默认扫描的常用端口包括：
- 21 (FTP)
- 22 (SSH)
- 23 (Telnet)
- 25 (SMTP)
- 53 (DNS)
- 80 (HTTP)
- 110 (POP3)
- 143 (IMAP)
- 443 (HTTPS)
- 465 (SMTPS)
- 587 (SMTP submission)
- 993 (IMAPS)
- 995 (POP3S)
- 3306 (MySQL)
- 3389 (RDP)
- 8080 (HTTP alternate)
- 8443 (HTTPS alternate)