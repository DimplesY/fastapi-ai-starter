# FastAPI Celery Starter

A FastAPI template with Celery integration for asynchronous task processing.

## 📦 项目概述

本项目是一个基于 [FastAPI](https://fastapi.tiangolo.com/) 和 [Celery](https://docs.celeryq.dev/en/stable/) 的模板项目，适用于构建高性能的异步任务处理服务。项目包含以下核心功能：

- 基于 JWT 的用户认证
- PostgreSQL 数据库集成（通过 SQLAlchemy 和 SQLModel）
- 异步任务调度（通过 RabbitMQ + Celery）
- 自动化 Alembic 数据库迁移
- 支持分页查询（通过 fastapi-pagination）

## 🧰 技术栈

- **Python** >= 3.12
- **FastAPI**
- **SQLModel / Alembic**
- **PostgreSQL**
- **Celery (RabbitMQ broker)**
- **Loguru** 日志管理
- **Passlib** 密码哈希加密
- **PyJWT** 用户身份验证

## 🚀 快速开始

### 安装依赖

使用 [uv](https://github.com/astral-sh/uv):

```bash
  uv sync
```


### 初始化数据库

```bash
  alembic upgrade head
```


### 启动服务

#### 使用 Docker（推荐）

```bash
  docker-compose up -d
```


服务地址：
- FastAPI: http://localhost:8000
- RabbitMQ: http://localhost:15672
- PostgreSQL: localhost:5432

#### 本地运行

```bash
  supervisord -c supervisord.conf
```


或单独运行：

```bash
    uv run main.py
    uv run celery -A celery_tasks worker --loglevel=INFO
    uv run celery -A celery_tasks beat --loglevel=INFO
```


## 🧪 示例接口

- 获取所有用户：`GET /api/v1/users`
- 测试接口：`GET /api/v1/test1`
- 登录认证：`POST /api/v1/login`（需自行实现登录接口）

## 📜 数据库迁移

生成新迁移脚本：

```bash
  ./scripts/migration.sh "描述信息"
```


应用迁移到最新版本：

```bash
  ./scripts/migrate.sh
```


## 📝 许可证

MIT License

--- 

如需进一步扩展功能（例如添加 Swagger 文档、测试用例、CI/CD 配置等），请根据需求补充相关内容。