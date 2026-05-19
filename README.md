# bili-utils

B 站账号批处理工具，基于 [bilibili-api](https://github.com/Nemo2011/bilibili-api) 开发。

## 参考

- 依赖仓库：[Nemo2011/bilibili-api](https://github.com/Nemo2011/bilibili-api)
- API 文档：[bilibili-api 文档](https://nemo2011.github.io/bilibili-api)


## 使用

### 找到 B 站账号凭证：

参考 [获取 Credential 类所需信息](https://nemo2011.github.io/bilibili-api/#/get-credential)

### GitHub Actions

1. 在仓库 **Settings → Secrets and variables → Actions** 中添加以下 Secrets：

| Secret          | 说明                           |
| --------------- | ------------------------------ |
| `SESSDATA`      | B 站 Cookie 中的 sessdata      |
| `BILI_JCT`      | B 站 Cookie 中的 bili_jct      |
| `BUVID3`        | B 站 Cookie 中的 buvid3        |
| `AC_TIME_VALUE` | B 站 Cookie 中的 ac_time_value |

1. 进入 **Actions** 页面，选择需要的workflow，点击 **Run workflow** 执行。

### 本地运行

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 新建文件 `.env` 并在文件中填入 B 站账号凭证：

```
sessdata="你的 sessdata"
bili_jct="你的 bili_jct"
buvid3="你的 buvid3"
ac_time_value="你的 ac_time_value"
```

## 功能

### 清理异常粉丝 (`remove_rob_fans.py`)

自动扫描粉丝列表，识别并移除以下异常粉丝：

- **已注销用户** — API 返回 `-404` 或用户名/签名包含"账号已注销"
- **封禁用户** — 用户 `silence` 字段为 1，或 API 返回异常错误码

### 执行脚本，支持通过 GitHub Actions 手动执行。

```bash
python remove_rob_fans.py
```

## 可能问题
可能批处理会触发412安全风控策略