# FastAPI AI Starter

> 🚀 一个现代化的 FastAPI 项目模板，集成 Celery 异步任务处理、PostgreSQL 数据库和 Redis 缓存

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ 特性

- 🌟 **现代 FastAPI** - 基于最新的 FastAPI 框架，支持自动 API 文档生成
- ⚡ **异步任务处理** - 集成 Celery + Redis，支持后台任务和定时任务
- 🗄️ **数据库集成** - PostgreSQL + SQLModel，支持自动迁移和类型安全
- 🔐 **身份认证** - JWT Token 认证，密码加密存储
- 📄 **分页查询** - 内置分页支持，优化大数据集查询性能
- 🐳 **容器化部署** - 完整的 Docker 配置，支持一键部署
- 📊 **进程管理** - Supervisord 配置，支持多进程管理
- 🔧 **开发工具** - 集成 Ruff、MyPy、Pre-commit 等开发工具
- 📝 **结构化日志** - Loguru 日志管理，支持结构化日志输出

## 🏗️ 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** - 现代、快速的 Web 框架
- **[Celery](https://docs.celeryq.dev/)** - 分布式任务队列
- **[SQLModel](https://sqlmodel.tiangolo.com/)** - SQL 数据库的类型安全 ORM

### 数据存储
- **[PostgreSQL](https://www.postgresql.org/)** - 主数据库（支持向量扩展）
- **[Redis](https://redis.io/)** - 缓存和消息代理

### 开发工具
- **[UV](https://github.com/astral-sh/uv)** - 现代 Python 包管理器
- **[Alembic](https://alembic.sqlalchemy.org/)** - 数据库迁移工具
- **[Ruff](https://github.com/astral-sh/ruff)** - 极速 Python 代码检查和格式化
- **[Loguru](https://github.com/Delgan/loguru)** - 简单易用的日志库

## 📦 项目结构

```
fastapi-ai-starter/
├── app/                      # 主应用目录
│   ├── api/                  # API 路由
│   │   ├── v1/              # API 版本 1
│   │   └── router.py        # 路由配置
│   ├── services/            # 业务服务层
│   │   ├── auth/            # 认证服务
│   │   ├── database/        # 数据库服务
│   │   └── settings/        # 配置管理
│   └── main.py              # FastAPI 应用创建
├── celery_tasks/            # Celery 任务
│   ├── workers/             # 任务定义
│   ├── celery.py           # Celery 应用
│   └── celeryconfig.py     # Celery 配置
├── alembic/                 # 数据库迁移文件
├── scripts/                 # 辅助脚本
├── nginx/                   # Nginx 配置
├── compose.yaml             # Docker Compose 配置
├── supervisord.conf         # 进程管理配置
└── pyproject.toml          # 项目配置
```

## 🚀 快速开始

### 环境要求

- Python 3.12+
- Docker & Docker Compose (推荐)
- PostgreSQL 16+ (本地开发)
- Redis 7+ (本地开发)

### 1. 克隆项目

```bash
git clone https://github.com/your-username/fastapi-ai-starter.git
cd fastapi-ai-starter
```

### 2. 安装依赖

使用 UV 安装依赖（推荐）：

```bash
# 安装 UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装项目依赖
uv sync
```

或使用 pip：

```bash
pip install -r requirements.txt
```

### 3. 启动服务

#### 方式一：Docker Compose（推荐）

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 方式二：本地开发

1. **启动数据库和 Redis**
   ```bash
   # 启动 PostgreSQL 和 Redis
   docker-compose up -d pgvector redis
   ```

2. **数据库迁移**
   ```bash
   # 执行数据库迁移
   alembic upgrade head
   ```

3. **启动应用**
   ```bash
   # 使用 Supervisord（推荐）
   supervisord -c supervisord.conf
   
   # 或分别启动各个服务
   uv run main.py                                    # FastAPI 应用
   uv run celery -A celery_tasks worker --loglevel=INFO  # Celery Worker
   uv run celery -A celery_tasks beat --loglevel=INFO    # Celery Beat
   ```

### 4. 验证安装

访问以下地址验证服务是否正常：

- **API 文档**: http://localhost:8000/docs
- **ReDoc 文档**: http://localhost:8000/redoc
- **API 健康检查**: http://localhost:8000/api/v1/test1

## 🔧 开发指南

### 数据库迁移

```bash
# 生成新的迁移文件
./scripts/migration.sh "添加新功能"

# 应用迁移
./scripts/migrate.sh

# 或直接使用 alembic
alembic revision --autogenerate -m "migration message"
alembic upgrade head
```

### 添加新的 API 端点

1. 在 `app/api/v1/` 下创建新的路由文件
2. 在 `app/api/v1/__init__.py` 中导入并注册路由
3. 编写相应的业务逻辑和数据模型

### 添加 Celery 任务

1. 在 `celery_tasks/workers/` 下创建任务文件
2. 在 `celery_tasks/celeryconfig.py` 中注册任务
3. 使用 `@app.task` 装饰器定义任务

### 代码质量检查

```bash
# 代码格式化和检查
uv run ruff check .
uv run ruff format .

# 类型检查
uv run mypy .

# 运行 pre-commit 钩子
pre-commit run --all-files
```

## 📚 API 文档

启动服务后，可以通过以下地址访问 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐳 部署指南

### Docker 部署

```bash
# 构建镜像
docker build -t fastapi-ai-starter .

# 启动服务
docker-compose up -d

# 扩展 Worker 数量
docker-compose up -d --scale web=3
```

### 生产环境配置

1. 修改 `compose.yaml` 中的环境变量
2. 配置 SSL 证书（nginx 配置）
3. 设置数据库连接密码
4. 配置日志持久化

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🆘 支持

如果你遇到问题或有任何建议，请：

1. 查看 [Issues](https://github.com/your-username/fastapi-ai-starter/issues)
2. 创建新的 Issue
3. 参与 [Discussions](https://github.com/your-username/fastapi-ai-starter/discussions)

---

⭐ 如果这个项目对你有帮助，请给它一个 Star！
