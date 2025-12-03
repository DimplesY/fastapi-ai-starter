# FastAPI AI Starter

> 🚀 一个现代化的 FastAPI 项目模板，集成 Celery 异步任务处理、PostgreSQL 数据库和 Redis 缓存，支持 AI 应用开发

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![Celery](https://img.shields.io/badge/Celery-5.5+-orange.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)
![Redis](https://img.shields.io/badge/Redis-7+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ 特性

- 🌟 **现代化 FastAPI 架构** - 基于 FastAPI 最新版本，支持自动 API 文档生成（Swagger UI & ReDoc）
- ⚡ **异步任务处理** - 集成 Celery + Redis，支持后台任务和定时任务调度
- 🗄️ **AI 就绪数据库** - PostgreSQL + pgvector 扩展，支持向量搜索和 AI 应用
- 🔐 **完整身份认证** - JWT Token 认证，密码加密存储，支持用户管理
- 📄 **智能分页查询** - 集成 fastapi-pagination，优化大数据集查询性能
- 🐳 **容器化部署** - 完整的 Docker + Docker Compose 配置，支持一键部署
- 📊 **进程管理** - Supervisord 配置，支持多进程管理和监控
- 🔧 **开发工具链** - 集成 Ruff、MyPy、Pre-commit 等现代化开发工具
- 📝 **结构化日志** - Loguru 日志管理，支持结构化日志输出和文件轮转
- 🔄 **数据库迁移** - Alembic 自动迁移，支持版本控制和回滚
- 🌐 **生产就绪** - Nginx 反向代理，CORS 配置，错误处理中间件

## 🏗️ 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** - 现代、快速（高性能）的 Web 框架
- **[Celery](https://docs.celeryq.dev/)** - 分布式任务队列，支持异步任务处理
- **[SQLModel](https://sqlmodel.tiangolo.com/)** - SQL 数据库的类型安全 ORM，基于 Pydantic 和 SQLAlchemy

### 数据存储
- **[PostgreSQL](https://www.postgresql.org/)** - 主数据库，支持事务和复杂查询
- **[pgvector](https://github.com/pgvector/pgvector)** - PostgreSQL 向量扩展，支持 AI 向量搜索
- **[Redis](https://redis.io/)** - 缓存和 Celery 消息代理

### 开发工具
- **[UV](https://github.com/astral-sh/uv)** - 现代 Python 包管理器，快速可靠
- **[Alembic](https://alembic.sqlalchemy.org/)** - 数据库迁移工具
- **[Ruff](https://github.com/astral-sh/ruff)** - 极速 Python 代码检查和格式化
- **[Loguru](https://github.com/Delgan/loguru)** - 简单易用的日志库
- **[MyPy](https://mypy.readthedocs.io/)** - 静态类型检查
- **[Pre-commit](https://pre-commit.com/)** - Git 预提交钩子管理

## 📦 项目结构

```
fastapi-ai-starter/
├── app/                          # 主应用目录
│   ├── api/                      # API 路由层
│   │   ├── v1/                   # API 版本 1
│   │   │   ├── __init__.py
│   │   │   └── test.py           # 示例路由：用户管理
│   │   ├── __init__.py
│   │   ├── router.py             # 路由注册器
│   │   └── util.py               # API 工具函数
│   ├── logging/                  # 日志配置
│   │   ├── __init__.py
│   │   └── logger.py             # Loguru 日志配置
│   ├── services/                 # 服务层（业务逻辑）
│   │   ├── auth/                 # 认证服务
│   │   │   ├── __init__.py
│   │   │   ├── factory.py
│   │   │   ├── service.py
│   │   │   └── utils.py
│   │   ├── database/             # 数据库服务
│   │   │   ├── models/           # 数据模型
│   │   │   │   └── user/         # 用户模型
│   │   │   │       ├── __init__.py
│   │   │   │       ├── model.py  # User 模型定义
│   │   │   │       └── crud.py   # CRUD 操作
│   │   │   ├── __init__.py
│   │   │   ├── factory.py
│   │   │   ├── service.py
│   │   │   └── utils.py
│   │   ├── settings/             # 配置服务
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── factory.py
│   │   │   └── service.py
│   │   ├── __init__.py
│   │   ├── base.py               # 服务基类
│   │   ├── deps.py               # 依赖注入
│   │   ├── factory.py            # 服务工厂
│   │   ├── manager.py            # 服务管理器
│   │   ├── schema.py             # 服务模式定义
│   │   └── util.py               # 服务工具函数
│   ├── util/                     # 工具函数
│   │   ├── __init__.py
│   │   └── concurrency.py        # 并发工具
│   ├── __init__.py
│   └── main.py                   # FastAPI 应用创建和配置
├── celery_tasks/                 # Celery 异步任务
│   ├── workers/                  # 任务工作器
│   │   ├── __init__.py
│   │   └── task_01.py            # 示例任务：加法计算
│   ├── __init__.py
│   ├── celery.py                 # Celery 应用创建
│   └── celeryconfig.py           # Celery 配置
├── alembic/                      # 数据库迁移
│   ├── versions/                 # 迁移版本文件
│   │   └── 84da034da8ea_add_user_model.py  # 用户表迁移
│   ├── env.py                    # Alembic 环境配置
│   ├── README
│   └── script.py.mako            # 迁移文件模板
├── scripts/                      # 辅助脚本
│   ├── migrate.sh                # 执行数据库迁移
│   └── migration.sh              # 生成新的迁移文件
├── nginx/                        # Nginx 配置
│   └── nginx.conf                # Nginx 配置文件
├── logs/                         # 日志目录
├── postgres/                     # PostgreSQL 数据目录
├── redis/                        # Redis 数据目录
├── .vscode/                      # VSCode 配置目录
├── .env                          # 环境变量配置
├── .gitignore                    # Git 忽略文件
├── .pre-commit-config.yaml       # 预提交钩子配置
├── alembic.ini                   # Alembic 数据库迁移配置
├── compose.yaml                  # Docker Compose 配置
├── Dockerfile                    # Docker 构建文件
├── main.py                       # 应用入口点（启动 Uvicorn）
├── pyproject.toml                # 项目依赖和配置
├── ruff.toml                     # Ruff 代码检查配置
├── supervisord.conf              # Supervisor 进程管理配置
└── uv.lock                       # UV 包管理器锁文件
```

## 🚀 快速开始

### 环境要求

- **Python 3.12+** (推荐使用 UV 包管理器)
- **Docker & Docker Compose** (推荐用于容器化部署)
- **PostgreSQL 16+** (本地开发可选)
- **Redis 7+** (本地开发可选)

### 1. 克隆项目

```bash
git clone https://github.com/your-username/fastapi-ai-starter.git
cd fastapi-ai-starter
```

### 2. 安装依赖

使用 UV 安装依赖（推荐）：

```bash
# 安装 UV（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装项目依赖
uv sync
```

### 3. 配置环境变量

复制环境变量模板并修改配置：

```bash
cp .env.example .env
# 编辑 .env 文件，根据需要修改配置
```

### 4. 启动服务

#### 方式一：Docker Compose（推荐，一键启动所有服务）

```bash
# 启动所有服务（FastAPI、Nginx、PostgreSQL、Redis）
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

#### 方式二：本地开发环境

1. **启动数据库和 Redis**

   ```bash
   # 启动 PostgreSQL + pgvector 和 Redis
   docker-compose up -d pgvector redis
   ```

2. **数据库迁移**

   ```bash
   # 执行数据库迁移
   ./scripts/migrate.sh

   # 或直接使用 alembic
   alembic upgrade head
   ```

3. **启动应用**

   ```bash
   # 使用 Supervisord（推荐，管理所有进程）
   supervisord -c supervisord.conf

   # 或分别启动各个服务
   uv run main.py                                    # FastAPI 应用（端口 8000）
   uv run celery -A celery_tasks worker --loglevel=INFO  # Celery Worker
   uv run celery -A celery_tasks beat --loglevel=INFO    # Celery Beat（定时任务）
   ```

### 5. 验证安装

访问以下地址验证服务是否正常：

- **Swagger UI API 文档**: http://localhost:8000/docs
- **ReDoc API 文档**: http://localhost:8000/redoc
- **API 端点示例**:
  - `GET /api/v1/test1` - 获取所有用户
  - `GET /api/v1/users` - 分页获取用户列表

## 🔧 开发指南

### 数据库迁移

```bash
# 生成新的迁移文件
./scripts/migration.sh "添加新功能描述"

# 应用迁移
./scripts/migrate.sh

# 或直接使用 alembic
alembic revision --autogenerate -m "迁移描述"
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

### 添加新的 API 端点

1. 在 `app/api/v1/` 下创建新的路由文件
2. 在 `app/api/v1/__init__.py` 中导入并注册路由
3. 在 `app/api/router.py` 中添加到路由列表
4. 编写相应的业务逻辑和数据模型

示例路由文件：

```python
# app/api/v1/example.py
from fastapi import APIRouter

router = APIRouter(tags=["example"])

@router.get("/example")
async def example_endpoint():
    return {"message": "Hello from example endpoint"}
```

### 添加数据模型

1. 在 `app/services/database/models/` 下创建模型目录
2. 定义 SQLModel 模型
3. 创建 CRUD 操作
4. 生成迁移文件

示例模型：

```python
# app/services/database/models/product/model.py
from sqlmodel import Field, SQLModel

class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    price: float
    description: str | None = None
```

### 添加 Celery 任务

1. 在 `celery_tasks/workers/` 下创建任务文件
2. 在 `celery_tasks/celeryconfig.py` 中注册任务到 `include` 列表
3. 使用 `@app.task` 装饰器定义任务

示例任务：

```python
# celery_tasks/workers/example_task.py
from celery_tasks.celery import app

@app.task
def process_data(data):
    # 处理数据的逻辑
    return {"status": "processed", "data": data}
```

### 代码质量检查

```bash
# 代码格式化和检查
uv run ruff check .          # 代码检查
uv run ruff format .         # 代码格式化

# 类型检查
uv run mypy .

# 运行 pre-commit 钩子
pre-commit run --all-files

# 安装 pre-commit 钩子（首次使用）
pre-commit install
```

## 📚 API 文档

启动服务后，可以通过以下地址访问 API 文档：

- **Swagger UI**: http://localhost:8000/docs - 交互式 API 文档，支持测试请求
- **ReDoc**: http://localhost:8000/redoc - 更美观的 API 文档展示

### 现有 API 端点

#### 用户管理
- `GET /api/v1/test1` - 获取所有用户列表
- `GET /api/v1/users` - 分页获取用户列表（支持分页参数）

## 🐳 部署指南

### Docker 部署

```bash
# 构建镜像
docker build -t fastapi-ai-starter .

# 启动服务
docker-compose up -d

# 扩展 Worker 数量
docker-compose up -d --scale web=3

# 查看服务日志
docker-compose logs -f web
docker-compose logs -f celery_worker
```

### 生产环境配置

1. **修改环境变量** - 更新 `.env` 文件中的生产配置
2. **配置 SSL 证书** - 在 `nginx/` 目录配置 SSL，证书放在 `/root/ssl/`
3. **数据库安全** - 修改 PostgreSQL 和 Redis 的默认密码
4. **日志管理** - 配置日志轮转和持久化存储
5. **监控告警** - 添加应用监控和告警配置

### 服务配置说明

- **FastAPI 应用**: 运行在端口 8000，通过 Nginx 反向代理
- **Nginx**: 运行在端口 80/443，提供 SSL 终止和负载均衡
- **PostgreSQL**: 运行在端口 5432，包含 pgvector 扩展
- **Redis**: 运行在端口 6379，作为缓存和 Celery 消息代理

## 🔍 项目特点详解

### 1. 现代化架构设计

- **分层架构**: 清晰的 API 层、服务层、数据层分离
- **依赖注入**: 使用 FastAPI 的依赖注入系统管理服务
- **工厂模式**: 服务工厂管理服务创建和生命周期
- **类型安全**: 全面的类型注解和 MyPy 检查

### 2. AI 就绪特性

- **向量数据库**: 使用 pgvector 扩展支持向量搜索
- **异步处理**: Celery 支持 AI 模型的异步推理
- **扩展性**: 易于集成 LangChain、OpenAI 等 AI 框架

### 3. 开发体验优化

- **热重载**: 开发模式下支持代码热重载
- **调试友好**: 详细的错误信息和日志输出
- **工具集成**: 完整的开发工具链配置

### 4. 生产就绪特性

- **健康检查**: 内置健康检查端点
- **错误处理**: 统一的异常处理中间件
- **CORS 配置**: 可配置的跨域资源共享
- **安全头**: 自动添加安全相关的 HTTP 头

### 开发规范

- 遵循 PEP 8 代码风格
- 添加类型注解
- 编写单元测试
- 更新相关文档
