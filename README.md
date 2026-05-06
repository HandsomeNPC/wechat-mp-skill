# 微信公众号运营工具箱 (wechat-mp-skill)

基于 [wechatpy](https://github.com/wechatpy/wechatpy) 的微信公众号一站式 CLI 工具，覆盖文章、菜单、素材、消息、评论、用户、标签、数据分析、二维码、回调解析等运营场景。

## 功能模块

| 模块 | 说明 |
|---|---|
| 🔐 login | 凭证管理（appid/secret） |
| 📝 article | 文章/草稿/发布 |
| 🗂 material | 素材管理（图片、语音、视频） |
| 🧩 menu | 自定义菜单/个性化菜单 |
| 💬 message | 客服/群发/模板/订阅消息 |
| 🗨 comment | 已发布文章评论管理 |
| 👤 user | 粉丝管理 |
| 🏷 tag | 标签 / 黑名单 |
| 📊 data | 数据分析（datacube） |
| 🔗 qrcode | 带参二维码 |
| 🎧 customservice | 多客服账号与会话 |
| 📡 callback | 服务器配置回调解析 |
| 🛠 misc | 杂项（服务器 IP、网络检测） |

## 环境要求

- Python >= 3.9
- 依赖：`pip install -r requirements.txt`

## 快速开始

### 1. 配置凭证

```bash
python main.py login set_credentials '{
  "appid": "wx1234567890abcdef",
  "secret": "abcdef1234567890",
  "token": "可选-用于回调验签",
  "aes_key": "可选-用于安全模式回调",
  "persist": true
}'
```

凭证默认持久化到 `~/.hermes/wechat-credentials.json`（权限 0600），可通过环境变量 `WECHAT_CREDENTIAL_FILE` 覆盖。

也可使用环境变量直接提供：`WECHAT_APPID` / `WECHAT_SECRET` / `WECHAT_ACCESS_TOKEN` / `WECHAT_TOKEN` / `WECHAT_AES_KEY`。

### 2. 验证凭证

```bash
python main.py login verify '{}'
```

### 3. 调用业务模块

```bash
python main.py <模块> <动作> '<参数JSON>'
```

CLI 自动加载凭证文件,无需手动传入。

## 使用示例

### 发布一篇图文

```bash
# 上传缩略图
python main.py material add '{"media_type":"image","file_path":"./cover.jpg"}'

# 新建草稿
python main.py article draft_add '{"articles":[{"title":"标题","content":"<p>正文HTML</p>","thumb_media_id":"<上一步返回>"}]}'

# 发布
python main.py article publish '{"media_id":"<draft_add返回>"}'
```

### 创建自定义菜单

```bash
python main.py menu create '{
  "buttons": [
    {"type":"click","name":"今日热门","key":"V1001_HOT"},
    {"name":"更多","sub_button":[
      {"type":"view","name":"官网","url":"https://example.com"}
    ]}
  ]
}'
```

### 查询用户数据

```bash
python main.py data user_summary '{"begin_date":"2026-01-01","end_date":"2026-01-07"}'
```

## 常见坑

| 坑 | 说明 |
|---|---|
| 白名单 IP | 调用接口的服务器 IP 必须加入公众号后台「IP白名单」,否则报 `40164` |
| 图文发布 | `article draft_add` 需先通过 `material add` 上传缩略图 |
| 群发限频 | 同一公众号一天群发 ≤ 4 次,超过返回 `45028` |
| 数据接口窗口 | 单次最长 7 天且 `begin_date` ≥ 今天-180 天 |
| 客服消息 48h | 仅可向 48 小时内有交互的粉丝发送,否则报 `45015` |
| comment 接口 | 使用 `msg_data_id`(群发返回),不是 `article_id` |
| 临时素材 3 天过期 | 长期使用走 `material add` |

## 健康检查

```bash
python main.py login verify '{}'
python main.py menu get '{}'
python main.py user list_followers '{}'
```

## 完整文档

详见 [SKILL.md](./SKILL.md),包含所有模块、动作及参数说明。

## License

MIT
