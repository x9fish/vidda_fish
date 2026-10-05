# vidda_fish

Home Assistant 自定义集成，通过本地 MQTT 控制海信 VIDAA 电视。

## 功能

- 15 个遥控按键：电源、音量±、静音、方向、OK、返回、首页、菜单、应用、直播、AI识图
- 长连接复用（首次按键建 MQTT，之后复用）
- 断线自动重连
- `remote` 实体 + 15 个 `button` 实体

## 支持设备

- Vidda 85V7N Ultra（已测）
- 无需客户端证书的 Hisense VIDAA 电视

## 安装

1. 添加自定义仓库：`https://github.com/x9fish/vidda_fish`（类别 Integration）
2. HACS 里下载 vidda_fish
3. 重启 HA
4. 设置 → 设备与服务 → 添加集成 → 搜索 vidda_fish

## 已知限制

- 信号源 / 设置键走海信云端，本地 MQTT 不支持
- `remote.is_on` 恒为 True，不反映真实开关状态
- 仅适用于无需证书的 VIDAA 固件

## 作者

x9fish — https://github.com/x9fish/vidda_fish
