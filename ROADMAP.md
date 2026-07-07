# 简单仓库管理系统路线图

技术方向：Python Flask + SQL Server + HTTP API

## 1. 系统目标

构建一个轻量级仓库管理后端系统，通过 HTTP API 向网页端、移动端、桌面端或其他系统提供库存业务能力。

核心能力：

- 商品资料管理
- 仓库和库位管理
- 入库管理
- 出库管理
- 库存查询
- 库存流水记录
- 用户登录与权限控制

## 2. 技术架构

```text
客户端 / 前端
    |
    | HTTP / JSON
    v
Flask API 服务
    |
    | SQLAlchemy / pyodbc
    v
SQL Server 数据库
```

推荐技术栈：

- Python
- Flask
- Flask Blueprint 或 Flask-RESTful
- SQL Server
- SQLAlchemy / pyodbc
- JWT 登录认证
- Marshmallow 或 Pydantic 参数校验
- Swagger / OpenAPI 接口文档

## 3. 数据库核心表

建议先设计以下基础表：

```text
users              用户表
roles              角色表
products           商品表
warehouses         仓库表
locations          库位表
inventory          当前库存表
stock_in_orders    入库单表
stock_in_items     入库明细表
stock_out_orders   出库单表
stock_out_items    出库明细表
stock_movements    库存流水表
suppliers          供应商表
customers          客户表
```

设计原则：

- `inventory` 保存当前库存数量，便于快速查询。
- `stock_movements` 保存所有库存变动记录，便于追溯。
- 入库、出库必须同时更新当前库存并写入库存流水。
- 出库前必须校验库存是否足够。

## 4. API 模块规划

### 阶段一：基础框架

认证接口：

```text
POST /api/auth/login
GET  /api/auth/profile
POST /api/auth/logout
```

商品接口：

```text
GET    /api/products
POST   /api/products
GET    /api/products/{id}
PUT    /api/products/{id}
DELETE /api/products/{id}
```

仓库与库位接口：

```text
GET  /api/warehouses
POST /api/warehouses
GET  /api/locations
POST /api/locations
```

### 阶段二：库存业务

库存查询：

```text
GET /api/inventory
GET /api/inventory/{product_id}
```

入库：

```text
POST /api/stock-in
GET  /api/stock-in
GET  /api/stock-in/{id}
```

出库：

```text
POST /api/stock-out
GET  /api/stock-out
GET  /api/stock-out/{id}
```

库存流水：

```text
GET /api/stock-movements
GET /api/stock-movements?product_id=1
```

### 阶段三：报表与查询

```text
GET /api/reports/inventory-summary
GET /api/reports/low-stock
GET /api/reports/stock-in-summary
GET /api/reports/stock-out-summary
```

## 5. 开发阶段路线

### 第 1 周：项目初始化

- 创建 Flask 项目结构
- 配置 SQL Server 连接
- 建立数据库模型
- 实现统一 API 返回格式
- 实现统一错误处理
- 实现 JWT 登录认证

推荐目录：

```text
warehouse-api/
  app/
    __init__.py
    config.py
    models/
    routes/
    services/
    schemas/
    utils/
  migrations/
  run.py
  requirements.txt
```

### 第 2 周：基础资料管理

- 用户管理
- 商品管理
- 仓库管理
- 库位管理
- 供应商管理
- 客户管理

目标：完成稳定的 CRUD API。

### 第 3 周：入库与出库

- 创建入库单
- 创建出库单
- 自动更新库存
- 自动写入库存流水
- 出库时校验库存是否足够

目标：完成系统核心业务闭环。

### 第 4 周：库存查询与报表

- 当前库存查询
- 商品库存明细
- 库存流水查询
- 低库存预警
- 入库统计
- 出库统计

### 第 5 周：安全与优化

- API 权限控制
- 参数校验
- 分页查询
- 日志记录
- SQL 查询优化
- Swagger / OpenAPI 文档

## 6. 核心业务流程

入库流程：

```text
创建入库单
 -> 写入入库明细
 -> 增加 inventory 库存
 -> 写入 stock_movements 流水
 -> 返回入库结果
```

出库流程：

```text
创建出库单
 -> 检查库存是否足够
 -> 写入出库明细
 -> 扣减 inventory 库存
 -> 写入 stock_movements 流水
 -> 返回出库结果
```

## 7. 最小可用版本 MVP

建议优先完成以下功能：

- 登录
- 商品管理
- 仓库管理
- 入库
- 出库
- 当前库存查询
- 库存流水查询

MVP 目标：先形成完整业务闭环，再逐步扩展高级功能。

## 8. 后续扩展方向

- 条码 / 二维码管理
- 扫码入库出库
- 批次号管理
- 有效期管理
- 多仓调拨
- 盘点功能
- 审核流程
- 操作日志
- Excel 导入导出
- 前端管理后台
- Docker 部署
- Nginx 反向代理

推荐实施顺序：

```text
基础资料 -> 入库出库 -> 库存流水 -> 报表 -> 权限与部署
```
