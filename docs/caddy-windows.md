# Caddy Windows 公网部署

目标结构：

```text
公网 80/443
    -> Caddy
        -> Flask 127.0.0.1:5000
```

## 1. 安装 Caddy

任选一种方式：

```powershell
winget install CaddyServer.Caddy
```

如果 winget 找不到，可以使用官方下载页下载 Windows 版 `caddy.exe`：

```text
https://caddyserver.com/download
```

## 2. 配置 Flask

Flask 保持只监听本机：

```powershell
flask run --host 127.0.0.1 --port 5000
```

## 3. 配置 Caddy

如果有域名，例如 `api.example.com`，把项目根目录的 `Caddyfile` 改成：

```caddyfile
api.example.com {
	reverse_proxy 127.0.0.1:5000
}
```

然后在域名 DNS 中添加：

```text
类型: A
主机记录: api
值: 你的公网 IP
```

Caddy 会自动申请 HTTPS 证书，所以路由器和防火墙需要开放：

```text
80/tcp
443/tcp
```

如果暂时只有公网 IP、没有域名，使用 HTTP。项目默认 `Caddyfile` 已经是这个模式：

```caddyfile
{
	default_bind 0.0.0.0
}

:80 {
	reverse_proxy 127.0.0.1:5000
}
```

访问：

```text
http://你的公网IP/api/health
```

更多模板见项目根目录的 `Caddyfile.example`。

## 4. 启动 Caddy

在项目根目录运行：

```powershell
caddy run --config Caddyfile
```

如果要后台运行并在配置变更后重载：

```powershell
caddy reload --config Caddyfile
```

## 5. 路由器端口映射

如果服务器在家用或公司内网，需要在路由器做端口转发：

```text
公网IP:80   -> 服务器内网IP:80
公网IP:443  -> 服务器内网IP:443
```

服务器内网 IP 可以用下面命令查看：

```powershell
ipconfig
```

## 6. Windows 防火墙

允许 Caddy 接收入站流量：

```powershell
New-NetFirewallRule -DisplayName "Caddy HTTP" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow
New-NetFirewallRule -DisplayName "Caddy HTTPS" -Direction Inbound -Protocol TCP -LocalPort 443 -Action Allow
```

如果 `netstat -ano` 看到 `127.0.0.1:80 LISTENING`，说明只监听本机；重新启动 Caddy 后应看到 `0.0.0.0:80 LISTENING`。

## 7. 验证

```powershell
curl http://127.0.0.1:5000/api/health
curl http://你的公网IP/api/health
```

有域名和 HTTPS 后：

```powershell
curl https://api.example.com/api/health
```
