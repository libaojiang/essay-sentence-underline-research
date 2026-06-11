# Demo 脚本说明

这个目录保存作文批改分句划线研究过程中用过的 demo 脚本。后续如果只发布 `作文批改分句划线研究过程` 这个文件夹，脚本、代表效果图和说明文档都会一起带上。

## 目录定位

这些脚本主要用于记录研究过程，不是正式生产接口代码。部分脚本需要原项目环境、测试图片、Nacos 配置或本地后端服务才能完整运行。

发布到 GitHub 时建议把它们当作“实验过程代码”阅读：

1. 先看根目录 `README.md` 理解最终方案。
2. 再看 `01_版本迭代与demo.md` 了解每一版为什么被保留或淘汰。
3. 需要公式时看 `02_算法与计算公式.md`。
4. 需要追溯具体实验时再看本目录脚本。

## 脚本分类

### 接口链路和耗时测试

| 脚本 | 说明 |
| --- | --- |
| `run_essay_multimodal_demo_20260512.py` | 最早期多模态作文识别和批改尝试 |
| `run_essay_api_timing_20260512.py` | 上传、OCR、LLM 批改等环节耗时拆分 |
| `run_essay_batch_correction_test_20260511.py` | 批量作文批改测试 |
| `run_essay_local_chinese_test_20260520.py` | 中文作文本地专项测试 |
| `run_essay_local_full_test_20260520.py` | 本地多样例完整流程测试 |
| `run_essay_three_sets_full_20260531.py` | 语文、英语、普通测试集全量测试 |
| `run_essay_three_sets_full_8039.py` | 指定本地端口的全量测试入口 |

### 图像定位和划线算法

| 脚本 | 说明 |
| --- | --- |
| `essay_line_whiteband_demo_20260603.py` | 二值化、物理行切分、白带检测、斜线划线核心 demo |
| `essay_selected_sentence_demo_20260604.py` | 选中句子定位和画线尝试 |
| `essay_precise_sentence_match_demo_20260605.py` | 精确句子匹配 demo |
| `essay_english_physical_line_demo_20260605.py` | 英文作文物理行识别 demo |
| `essay_line_filter_demo_20260608.py` | 行过滤、候选清洗、去除无效行 demo |

### 分句点评和模型实验

| 脚本 | 说明 |
| --- | --- |
| `essay_overall_parallel_demo_20260604.py` | 总评和分句点评并发生成实验 |
| `essay_sentence_rating_demo_20260608.py` | 候选句分句评级实验 |
| `essay_sentence_guard_demo_20260610.py` | 防止点评标点、错别字、非句子问题的规则实验 |
| `essay_visual_locator_demo_20260610.py` | 视觉模型直接定位句子实验 |
| `essay_grounding_bbox_demo_20260610.py` | 视觉 grounding 框实验 |
| `essay_two_pass_locator_demo_20260610.py` | 两阶段视觉定位实验 |

## 公开注意点

脚本里不应写死真实 token、OSS 签名或账号密码。如果后续继续补 demo，建议继续使用环境变量、配置文件读取或占位参数。

代表效果图已经整理到 `../assets`，不要再依赖历史 `tmp` 输出目录作为 GitHub 展示内容。

如果需要运行引用本地图片的早期 demo，可以把自己的测试图放到 `../sample_images`。公开资料包默认不放原始学生作文图。
