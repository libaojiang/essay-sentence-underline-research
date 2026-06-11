# 全量公开上传说明

当前仓库已经按公开求助帖方式初始化，文档和公开 demo 已经提交。

如果需要把本地资料包中的所有原始素材一起公开，包括：

- `assets/*.jpg`
- `demos/*.py`
- `sample_images/README.md`
- 根目录研究文档

可以在本地执行下面命令。

## 1. 克隆仓库

```bash
git clone https://github.com/libaojiang/essay-sentence-underline-research.git
cd essay-sentence-underline-research
```

## 2. 覆盖为本地完整资料包内容

把下载的完整项目包解压后，将解压目录中的全部内容复制到当前仓库目录。

推荐目录结构：

```text
essay-sentence-underline-research/
├── README.md
├── 01_版本迭代与demo.md
├── 02_算法与计算公式.md
├── 03_测试过程与效果.md
├── 04_正式流程.md
├── 05_素材与demo索引.md
├── assets/
├── demos/
├── sample_images/
├── .gitignore
├── requirements.txt
└── GITHUB_UPLOAD_NOTE.md
```

## 3. 提交所有文件

```bash
git add -A
git commit -m "Publish full research package"
git push origin main
```

## 4. 说明

这个仓库用于公开求助和研究交流。图片来源为公开网络素材时，可以直接保留在 `assets/` 目录。

注意：`demos/` 中的早期实验脚本依赖原项目环境、Nacos 配置、本地服务或模型 API key。公开后别人不一定能直接运行，但可以阅读算法过程和工程链路。
