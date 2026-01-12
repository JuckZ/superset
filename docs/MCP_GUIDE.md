# Superset MCP 服务 Docker 部署与 Cursor 集成指南

本指南将帮助您使用 Docker 方式运行 Superset MCP 服务。

## 🐳 使用 Docker 运行 MCP 服务

### 使用 docker-compose-dev-light.yml 

这是最简单的方式，适合开发和测试环境：

```bash
# 构建并启动 Superset 和 MCP 服务
docker-compose -p superset-dev -f docker-compose-dev-light.yml --profile mcp build
docker-compose -p superset-dev -f docker-compose-dev-light.yml --profile mcp up -d
docker-compose -p superset-dev -f docker-compose-dev-light.yml --profile mcp down

```
### 配置 MCP 服务

MCP 服务的配置在 `superset_config.py` 中。对于 Docker 部署，配置文件通常位于：
- `docker/pythonpath_dev/superset_config_docker_light.py` (light 模式)
- `docker/pythonpath_dev/superset_config.py` (完整模式)

**开发环境配置示例：**

```python
# MCP Service Configuration
MCP_DEV_USERNAME = "admin"  # 用于 MCP 认证的 Superset 用户名
MCP_AUTH_ENABLED = True
MCP_SERVICE_HOST = "0.0.0.0"  # 监听所有接口
MCP_SERVICE_PORT = 5008

# Superset Web 服务器地址（用于截图生成）
SUPERSET_WEBSERVER_ADDRESS = "http://localhost:9001"
WEBDRIVER_BASEURL = "http://localhost:9001/"
```

**生产环境配置示例：**

```python
# MCP Service Configuration (生产环境)
MCP_AUTH_ENABLED = True
MCP_JWT_ISSUER = "https://your-auth-provider.com"
MCP_JWT_AUDIENCE = "superset-mcp"
MCP_JWT_ALGORITHM = "RS256"
MCP_JWKS_URI = "https://auth.example.com/.well-known/jwks.json"
MCP_DEV_USERNAME = None  # 禁用开发认证

MCP_SERVICE_HOST = "0.0.0.0"
MCP_SERVICE_PORT = 5008
```

**检查服务状态：**
```bash

curl -i POST 'http://127.0.0.1:5008/mcp' \
-H 'Accept: application/json, text/event-stream' \
-H 'Content-Type: application/json' \
-d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'

```
