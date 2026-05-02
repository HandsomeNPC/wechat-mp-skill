---
name: wechat-skill
description: 微信公众号运营工具箱 — 文章管理、菜单管理、用户/标签、评论管理、客服与回复、数据分析、回调解析，一站式覆盖。
version: 1.0.0
type: code
implementation: python
interface: cli-and-api
runtime: python>=3.9
languages:
  - zh-CN
tags:
  - wechat
  - mp
  - official-account
  - wechatpy
  - article-ops
  - menu-ops
  - comment-ops
  - message-ops
  - subscriber-ops
  - analytics
license: MIT
entry_point: main.py
install: pip install -r requirements.txt
---

# 微信公众号运营工具箱 (wechat-skill)

基于 [wechatpy](https://github.com/wechatpy/wechatpy) 的 微信公众号一站式工具，覆盖 文章管理、菜单管理、素材、客服消息、群发、模板/订阅消息、评论管理、用户/标签、数据分析、带参二维码、回调解析等全部能力。

---

## 何时激活

当用户**明确请求**以下操作时激活：

| 触发词 | 模块 |
|---|---|
| 发文、草稿、群发图文、发布、撤回文章 | 📝 article |
| 上传素材、图片、缩略图、永久素材、临时素材 | 🗂 material |
| 菜单、个性化菜单、按钮 | 🧩 menu |
| 客服消息、私信、模板消息、订阅通知、群发文本/图片 | 💬 message |
| 评论、精选、回复评论、删评 | 🗨 comment |
| 粉丝、关注列表、备注、openid | 👤 user |
| 标签、黑名单、拉黑 | 🏷 tag |
| 数据、统计、阅读、分享、增减粉丝 | 📊 data |
| 带参二维码、推广二维码、扫码场景 | 🔗 qrcode |
| 客服账号、多客服、会话、聊天记录 | 🎧 customservice |
| 回调、签名校验、解密、安全模式 | 📡 callback |

---

## 🔐 凭证管理

公众号 API 仅需 `appid + secret`（access_token 由 wechatpy 自动获取）。**没有扫码登录流程**。

**Step 1 — 配置凭证（首次/更换公众号时）**
```bash
python main.py login set_credentials '{
  "appid": "wx1234567890abcdef",
  "secret": "abcdef1234567890",
  "token": "可选-用于回调验签",
  "aes_key": "可选-用于安全模式回调",
  "persist": true
}'
```
持久化路径默认 `~/.hermes/wechat-credentials.json` (0600)，可通过 `WECHAT_CREDENTIAL_FILE` 环境变量覆盖。

**Step 2 — 检验**
```bash
python main.py login verify '{}'
```
返回 `{"success": true, "appid": "...", "access_token_masked": "..."}` 即可。

**Step 3 — 调用任意业务模块** — CLI 自动加载凭证。

> ⚠️ 也可通过 `WECHAT_APPID` / `WECHAT_SECRET` / `WECHAT_ACCESS_TOKEN` / `WECHAT_TOKEN` / `WECHAT_AES_KEY` 环境变量提供。

---

## ⚠️ 常见坑

| 坑 | 说明 |
|---|---|
| **白名单 IP** | 调用接口的服务器 IP 必须在公众号后台的「IP白名单」中，否则报 `40164`。可用 `python main.py misc server_ips '{}'` 查看微信回调的 IP。 |
| **图文发布需先上传缩略图** | `article draft_add` 需要 `thumb_media_id`，必须先 `material add` 上传图片获得。 |
| **群发限频** | 同一个公众号一天群发 ≤ 4 次，超过返回 `45028`。 |
| **数据接口 7 天/180 天限制** | `data.*` 单次最长 7 天窗口，且 `begin_date` ≥ 今天-180 天。 |
| **客服消息 48h 窗口** | `message send_*`（kf 消息）只能给 48 小时内有交互的粉丝发，否则报 `45015`。 |
| **comment 接口的 msg_data_id** | 不是 article_id，必须用 **群发** 时返回的 `msg_data_id`。 |
| **临时素材 3 天过期** | `material upload_temp` 仅 3 天可用，长期使用走 `material add`。 |

---

## CLI 调用格式

```bash
python main.py <模块> <动作> '<参数JSON>'
```

CLI **自动加载** `~/.hermes/wechat-credentials.json`，无需手动传凭证。

---

## 模块速查

### 🔐 login — 凭证管理

| 动作 | 参数 | 示例 |
|---|---|---|
| `set_credentials` | `appid`, `secret`, `access_token?`, `token?`, `aes_key?`, `persist=true` | `python main.py login set_credentials '{"appid":"wx..","secret":".."}'` |
| `verify` | — | `python main.py login verify '{}'` |
| `refresh` | — | `python main.py login refresh '{}'` |
| `show` | — | `python main.py login show '{}'` |
| `logout` | — | `python main.py login logout '{}'` |

> ✅ `verify` 不暴露完整 token，`show` 仅返回脱敏字段

---

### 📝 article — 文章 / 草稿 / 发布

| 动作 | 参数 | 说明 |
|---|---|---|
| `draft_add` | `articles`(list) | 新增草稿，`articles[*]` 必含 `title/content/thumb_media_id`，可选 `author/digest/content_source_url/need_open_comment/only_fans_can_comment` |
| `draft_get` | `media_id` | 获取草稿内容 |
| `draft_update` | `media_id`, `index`, `articles` | 修改草稿中第 N 篇（index 从 0 起） |
| `draft_delete` | `media_id` | 删除草稿 |
| `draft_list` | `offset=0`, `count=20`, `no_content=0` | 草稿列表 |
| `draft_count` | — | 草稿总数 |
| `publish` | `media_id` | 发布草稿 → 返回 `publish_id` |
| `publish_status` | `publish_id` | 轮询发布状态 |
| `publish_get` | `article_id` | 通过 article_id 查已发布图文 |
| `publish_list` | `offset=0`, `count=20`, `no_content=0` | 已成功发布列表 |
| `publish_delete` | `article_id`, `index=0` | 删除已发布（`index=0` 删除全部子图文） |

**典型流程**：
```bash
# 1. 上传缩略图获取 thumb_media_id
python main.py material add '{"media_type":"image","file_path":"./cover.jpg"}'

# 2. 新建草稿
python main.py article draft_add '{"articles":[{"title":"标题","content":"<p>正文HTML</p>","thumb_media_id":"<上一步返回>"}]}'

# 3. 提交发布
python main.py article publish '{"media_id":"<draft_add返回>"}'
```

> ✅ 需要凭证

---

### 🗂 material — 素材管理

| 动作 | 参数 | 说明 |
|---|---|---|
| `add` | `media_type` (image/voice/video/thumb), `file_path`, `title?`, `introduction?` | 上传永久素材，video 必须传标题+简介 |
| `get` | `media_id` | 下载/获取永久素材 |
| `delete` | `media_id` | 删除永久素材 |
| `list` | `media_type` (image/voice/video/news), `offset=0`, `count=20` | 素材列表 |
| `count` | — | 素材总数 |
| `upload_temp` | `media_type`, `file_path` | 上传临时素材（3天过期） |
| `download_temp` | `media_id`, `output_path?` | 下载临时素材 |
| `get_temp_url` | `media_id` | 临时素材直链 |
| `upload_image` | `file_path` | 上传图文内嵌图片，返回 CDN URL |

> ✅ 需要凭证

---

### 🧩 menu — 自定义菜单

| 动作 | 参数 | 说明 |
|---|---|---|
| `get` | — | 当前已发布菜单 |
| `get_info` | — | 后台配置的菜单（含个性化） |
| `create` | `buttons`(list) | 创建/覆盖菜单 |
| `update` | `buttons`(list) | 同 create（微信无独立 update 接口） |
| `delete` | — | 删除菜单 |
| `add_conditional` | `buttons`, `matchrule` | 个性化菜单，`matchrule` 含 `tag_id/sex/country/province/city/...` |
| `del_conditional` | `menu_id` | 删除个性化菜单 |
| `try_match` | `user_id` | 测试用户命中哪个个性化菜单 |

**示例**：
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

> ✅ 需要凭证

---

### 💬 message — 消息 (客服/群发/模板/订阅)

#### 客服消息（48h 窗口内单发）

| 动作 | 参数 |
|---|---|
| `send_text` | `openid`, `content`, `kf_account?` |
| `send_image` | `openid`, `media_id`, `kf_account?` |
| `send_voice` | `openid`, `media_id`, `kf_account?` |
| `send_video` | `openid`, `media_id`, `title?`, `description?`, `kf_account?` |
| `send_articles` | `openid`, `articles`(list 或 mpnews media_id) |
| `send_link` | `openid`, `title`, `description`, `url`, `thumb_url` |
| `send_card` | `openid`, `card_id`, `card_ext?` |
| `send_miniprogram` | `openid`, `miniprogrampage`{title,appid,pagepath,thumb_media_id} |
| `send_menu` | `openid`, `head_content`, `list_items`, `tail_content?` |

#### 群发

| 动作 | 参数 |
|---|---|
| `mass_text` | `content`, `tag_or_users`(int=tag / list=openids), `is_to_all?`, `preview?`, `client_msg_id?` |
| `mass_image` | `media_id` + 同上 |
| `mass_voice` | `media_id` + 同上 |
| `mass_video` | `media_id`, `title?`, `description?` + 同上 |
| `mass_article` | `media_id` (mpnews) + 同上 |
| `mass_status` | `msg_id` |
| `mass_delete` | `msg_id` |

#### 模板 & 订阅

| 动作 | 参数 |
|---|---|
| `send_template` | `openid`, `template_id`, `data`, `url?`, `mini_program?` |
| `send_subscribe` | `openid`, `template_id`, `data`, `page?`, `miniprogram?` |
| `send_subscribe_one_time` | `openid`, `template_id`, `scene`, `title`, `data`, `url?` |
| `auto_reply_info` | — | 读取自动回复规则 |

> ✅ 需要凭证；模板消息要求服务号；客服消息 48h 内有效

---

### 🗨 comment — 已发布文章评论管理

文章定位 = `msg_data_id`（群发返回）+ `index`（多图文位置，从 1 起）

| 动作 | 参数 |
|---|---|
| `open` | `msg_data_id`, `index=1` |
| `close` | `msg_data_id`, `index=1` |
| `list` | `msg_data_id`, `index=1`, `begin=0`, `count=50`, `type=0`(0全部/1精选/2非精选) |
| `mark_elect` | `msg_data_id`, `index`, `user_comment_id` |
| `unmark_elect` | `msg_data_id`, `index`, `user_comment_id` |
| `delete` | `msg_data_id`, `index`, `user_comment_id` |
| `reply` | `msg_data_id`, `index`, `user_comment_id`, `content` |
| `delete_reply` | `msg_data_id`, `index`, `user_comment_id` |

> ✅ 需要凭证；只对 **已开启评论** 的图文有效

---

### 👤 user — 粉丝管理

| 动作 | 参数 |
|---|---|
| `get` | `openid`, `lang=zh_CN` |
| `batch_get` | `openid_list`(list of str 或 list of {openid,lang}) |
| `list_followers` | `next_openid?` | 一页（最多 10000） |
| `list_all_followers` | `limit?` | 翻页拉取全部 openid |
| `update_remark` | `openid`, `remark` |
| `change_openid` | `from_appid`, `openid_list` | 主体迁移后转换 openid |

> ✅ 需要凭证

---

### 🏷 tag — 标签 / 黑名单

| 动作 | 参数 |
|---|---|
| `create` | `name` |
| `list` | — |
| `update` | `tag_id`, `name` |
| `delete` | `tag_id` |
| `tag_users` | `tag_id`, `openid_list` |
| `untag_users` | `tag_id`, `openid_list` |
| `user_tags` | `openid` |
| `tag_members` | `tag_id`, `next_openid?` |
| `tag_members_all` | `tag_id`, `limit?` |
| `blacklist` | `begin_openid?` |
| `block` | `openid_list` (≤20) |
| `unblock` | `openid_list` |

> ✅ 需要凭证；批量 ≤ 20

---

### 📊 data — 数据分析（datacube）

所有动作支持 `begin_date` / `end_date`（YYYY-MM-DD），不传则默认最近 7 天。

| 类别 | 动作 |
|---|---|
| 用户 | `user_summary`, `user_cumulate` |
| 图文 | `article_summary`, `article_total`, `user_read`, `user_read_hour`, `user_share`, `user_share_hour` |
| 消息 | `upstream_msg`, `upstream_msg_hour`, `upstream_msg_week`, `upstream_msg_month`, `upstream_msg_dist` |
| 接口 | `interface_summary`, `interface_summary_hour` |

```bash
python main.py data user_summary '{"begin_date":"2025-01-01","end_date":"2025-01-07"}'
```

> ✅ 需要凭证；窗口 ≤ 7 天 & ≥ 今天-180 天

---

### 🔗 qrcode — 带参二维码

| 动作 | 参数 |
|---|---|
| `temp_id` | `scene_id` (1..100000), `expire_seconds=1800` |
| `temp_str` | `scene_str`, `expire_seconds=1800` |
| `perm_id` | `scene_id` (1..100000) |
| `perm_str` | `scene_str` |
| `show_url` | `ticket` |
| `download` | `ticket`, `output_path` | 下载二维码 PNG |

> ✅ 需要凭证

---

### 🎧 customservice — 多客服 (账号 + 会话)

| 动作 | 参数 |
|---|---|
| `add_account` | `account` (`prefix@gh_id`), `nickname`, `password` |
| `update_account` | `account`, `nickname`, `password` |
| `delete_account` | `account` |
| `list_accounts` | — |
| `list_online` | — |
| `upload_avatar` | `account`, `file_path` |
| `create_session` | `openid`, `account`, `text?` |
| `close_session` | `openid`, `account`, `text?` |
| `get_session` | `openid` |
| `list_sessions` | `account` |
| `waiting` | — | 未接入会话 |
| `records` | `start_time`(unix), `end_time`(unix), `msgid=1`, `number=10000` |

> ✅ 需要凭证；`records` 单次不能跨日

---

### 📡 callback — 服务器配置回调

| 动作 | 参数 | 说明 |
|---|---|---|
| `verify` | `signature`, `timestamp`, `nonce`, `echostr` | 服务器配置 URL 校验时使用 |
| `parse` | `xml`, `signature?`, `timestamp?`, `nonce?`, `msg_signature?`, `mode=plain` (plain/compat/safe) | 解析（必要时解密）回调 XML，返回结构化字典 |
| `reply_text` | `from_user`, `to_user`, `content`, `encrypt=false`, `timestamp?`, `nonce?` | 构造文本被动回复 XML |
| `reply_articles` | `from_user`, `to_user`, `articles`(list), `encrypt=false` | 构造图文被动回复 XML |

> 模式说明：plain=普通模式 / compat=兼容模式 / safe=安全模式（需 aes_key）

> ✅ verify/parse 不需要凭证（仅需 token，安全模式额外需要 aes_key）

---

### 🛠 misc — 杂项

| 动作 | 参数 |
|---|---|
| `server_ips` | — | 微信服务器回调 IP |
| `check_network` | `action=all` (dns/ping/all), `operator=DEFAULT` (CHINANET/UNICOM/CAP/DEFAULT) |
| `short_url` | `long_url` | ⚠️ 微信已废弃 |

---

## 凭证 / 权限速查

| 模块 | 需要凭证？ | 备注 |
|---|---|---|
| 🔐 login | ❌ (它就是配置凭证) | |
| 📝 article | ✅ | |
| 🗂 material | ✅ | |
| 🧩 menu | ✅ | 服务号/订阅号均可 |
| 💬 message | ✅ | 模板要服务号；订阅要订阅号/服务号 + 用户授权 |
| 🗨 comment | ✅ | 仅对已开评论的图文 |
| 👤 user | ✅ | |
| 🏷 tag | ✅ | |
| 📊 data | ✅ | |
| 🔗 qrcode | ✅ | |
| 🎧 customservice | ✅ | |
| 📡 callback | ❌ (但需 token / aes_key) | 不调用接口，仅本地解析 |
| 🛠 misc | ✅ | |

凭证文件：`~/.hermes/wechat-credentials.json` (0600)，CLI 自动加载。

---

## 验证

快速健康检查：
```bash
python main.py login verify '{}'
python main.py menu get '{}'
python main.py user list_followers '{}'
```

---

> **文档风格**：中文、表格化、运营导向。每个模块用表格而非大段文字；坑点前置；CLI 自动加载凭证，无需手动配置。
