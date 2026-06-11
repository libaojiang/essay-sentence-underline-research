# GitHub 上传说明

这个目录已经按 GitHub 项目形式整理。建议仓库名：`essay-sentence-underline-research`。

## 内容定位

这是作文批改「分句点评 + 原图下划线定位」的研究过程包，包含：

- 根目录 5 份研究过程文档；
- `demos/`：实验脚本快照；
- `assets/`：代表效果图；
- `sample_images/`：放置自测图片的占位目录。

## 运行说明

`demos/` 里的脚本不是统一生产接口代码，部分依赖原项目环境、Nacos 配置、本地服务或测试图片。

基础依赖可先安装：

```bash
pip install -r requirements.txt
```

## 公开前检查

- 不要提交 `.env`、真实 token、OSS 签名、账号密码。
- 如果 `assets/` 中图片包含真实学生作文或个人信息，建议先脱敏，或者把仓库设为 private。
- 已添加 `.gitignore`，默认忽略本地配置、日志、临时输出目录。
