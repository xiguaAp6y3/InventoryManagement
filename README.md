# Inventory Management API

Python Flask + Azure SQL Server 仓库管理系统后端。

## 快速开始

1. 创建虚拟环境并安装依赖：

```powershell
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

4. 初始化数据库表：

```powershell
flask init-db
```

5. 创建管理员账号：

```powershell
flask create-admin admin admin@example.com your-password
```

6. 启动 API：

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

