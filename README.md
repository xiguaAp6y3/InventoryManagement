# Inventory Management API

Python 3.13 + Flask + Azure SQL Server 仓库管理系统后端。

## 快速开始

1. 确认使用 Python 3.13，然后创建虚拟环境并安装依赖：

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. 复制环境变量模板：

```powershell
Copy-Item .env.example .env
```

3. 修改 `.env` 中的 Azure SQL Server 信息：

```text
AZURE_SQL_SERVER=your-server.database.windows.net
AZURE_SQL_DATABASE=your-database
AZURE_SQL_USERNAME=your-sql-user
AZURE_SQL_PASSWORD=your-sql-password
```

4. 先测试数据库连接：

```powershell
flask check-db
```

5. 初始化数据库表：

```powershell
flask init-db
```

6. 创建管理员账号：

```powershell
flask create-admin admin admin@example.com your-password
```

7. 启动 API：

```powershell
flask run
```

默认地址：

```text
http://127.0.0.1:5000
```

## 当前接口

```text
GET  /api/health
POST /api/auth/login
GET  /api/auth/profile

GET  /api/products
POST /api/products
GET  /api/products/{id}
PUT  /api/products/{id}
DELETE /api/products/{id}

GET  /api/warehouses
POST /api/warehouses
GET  /api/locations
POST /api/locations

GET  /api/inventory
POST /api/stock-in
POST /api/stock-out
GET  /api/stock-movements
```

## 公网部署

推荐用 Caddy 作为反向代理：

```text
公网 80/443 -> Caddy -> Flask 127.0.0.1:5000
```

配置文件见 [Caddyfile](Caddyfile)，Windows 部署步骤见 [docs/caddy-windows.md](docs/caddy-windows.md)。

## Azure SQL 连接排错

如果 `flask init-db` 出现 `Login failed for user` 或 `18456`，通常不是 Flask 代码错误，而是 Azure SQL 登录未通过。请先运行：

```powershell
flask check-db
```

重点检查：

- `AZURE_SQL_SERVER` 使用完整地址，例如 `xxx.database.windows.net`。
- `AZURE_SQL_DATABASE` 是数据库名称，不是服务器名称。
- `AZURE_SQL_USERNAME` 和 `AZURE_SQL_PASSWORD` 是 SQL authentication 账号密码。
- 如果使用 Azure SQL 服务器级登录，可以尝试 `AZURE_SQL_USERNAME=用户名@服务器短名`，例如 `stdu_admin@myserver`。
- Azure Portal 中 SQL Server 防火墙已允许当前客户端 IP。
- 该登录在目标数据库中有用户和建表权限。
