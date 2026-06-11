# 05 素材与 Demo 索引

这个文件记录资料包里图片、demo 脚本和输出目录的来源，方便后续把研究过程同步到 GitHub 时追溯。

## 代表图片来源

| 资料包图片 | 来源文件 | 用途 |
| --- | --- | --- |
| `assets/v01_raw_ocr_c6_incomplete.jpg` | `tmp/essay_c6_horizontal_fix_20260513_125326/chinese_c6/chinese_c6_page3_annotated.jpg` | 早期直接使用 OCR 坐标的效果 |
| `assets/v02_grid_snap_c6_contact.jpg` | `tmp/essay_c6_grid_snap_demo_20260528/c6_grid_snap_contact.jpg` | 作文纸横线吸附 demo |
| `assets/v03_white_band_c6_contact.jpg` | `tmp/essay_c6_white_band_demo_20260529/c6_white_band_contact.jpg` | c6 白带检测 demo |
| `assets/binary_01_crop_input.jpg` | `tmp/essay_line_whiteband_demo_20260603_180707/page01_08da3f0c22d380810ae800017a4d42e6_crop_input.jpg` | 二值化前的裁剪输入 |
| `assets/binary_02_text_mask.jpg` | `tmp/essay_line_whiteband_demo_20260603_180707/page01_08da3f0c22d380810ae800017a4d42e6_text_mask.jpg` | 二值化后的文字 mask |
| `assets/binary_03_ink_score.jpg` | `tmp/essay_line_whiteband_demo_20260603_180707/page01_08da3f0c22d380810ae800017a4d42e6_ink_score.jpg` | 墨迹强度和投影参考图 |
| `assets/v04_physical_line_boxes_normal.jpg` | `tmp/essay_line_whiteband_demo_20260603_180707/page01_08da3f0c22d380810ae800017a4d42e6_line_boxes.jpg` | 物理行切分框选效果 |
| `assets/v04_white_band_detection_normal.jpg` | `tmp/essay_line_whiteband_demo_20260603_180707/page01_08da3f0c22d380810ae800017a4d42e6_white_bands.jpg` | 行间白带检测效果 |
| `assets/v05_physical_line_english_underlines.jpg` | `tmp/essay_formal_physical_line_draw_20260605_152746/e6_underlines.jpg` | 英文作文物理行画线 |
| `assets/final_chinese_c6_page3_underlines.jpg` | `tmp/essay_api_formal_full_20260608_171207/annotated/chinese_c6_page3_underlines.jpg` | 正式接口中文 c6 效果 |
| `assets/final_english_e6_page1_underlines.jpg` | `tmp/essay_api_formal_full_20260608_171207/annotated/english_e6_page1_underlines.jpg` | 正式接口英文 e6 效果 |
| `assets/test_contact_chinese.jpg` | `tmp/essay_contact_sheets_20260531_1615/chinese_positions_contact.jpg` | 语文样例总览 |
| `assets/test_contact_english.jpg` | `tmp/essay_contact_sheets_20260531_1615/english_positions_contact.jpg` | 英文样例总览 |
| `assets/test_contact_normal.jpg` | `tmp/essay_contact_sheets_20260531_1615/normal_positions_contact.jpg` | 普通测试集总览 |

## Demo 脚本

这些脚本已经复制到本资料包的 `demos/` 目录。表里的历史 `tmp` 路径只作为来源追溯，GitHub 发布时以 `demos/` 里的文件为准。

| 脚本 | 主要用途 |
| --- | --- |
| `demos/run_essay_multimodal_demo_20260512.py` | 最早期多模态作文识别/批改 demo |
| `demos/run_essay_api_timing_20260512.py` | 接口耗时拆分测试 |
| `demos/run_essay_batch_correction_test_20260511.py` | 批量作文批改测试 |
| `demos/run_essay_local_chinese_test_20260520.py` | 本地中文作文专项测试 |
| `demos/run_essay_local_full_test_20260520.py` | 本地较完整样例测试 |
| `demos/run_essay_three_sets_full_20260531.py` | 三个测试集全量测试 |
| `demos/run_essay_three_sets_full_8039.py` | 指定本地端口的三测试集全量测试 |
| `demos/essay_line_whiteband_demo_20260603.py` | 行间白带检测 demo |
| `demos/essay_selected_sentence_demo_20260604.py` | 选中句子定位 demo |
| `demos/essay_overall_parallel_demo_20260604.py` | 总评和分句点评并发 demo |
| `demos/essay_precise_sentence_match_demo_20260605.py` | 精确句子匹配 demo |
| `demos/essay_english_physical_line_demo_20260605.py` | 英文物理行识别 demo |
| `demos/essay_sentence_rating_demo_20260608.py` | 候选句分句评级 demo |
| `demos/essay_line_filter_demo_20260608.py` | 行过滤和候选清洗 demo |
| `demos/essay_sentence_guard_demo_20260610.py` | 分句点评防误评规则 demo |
| `demos/essay_visual_locator_demo_20260610.py` | 视觉定位尝试 demo |
| `demos/essay_grounding_bbox_demo_20260610.py` | 视觉 grounding 框尝试 demo |
| `demos/essay_two_pass_locator_demo_20260610.py` | 两阶段定位尝试 demo |

## 关键输出目录

| 输出目录 | 说明 |
| --- | --- |
| `tmp/essay_c6_grid_snap_demo_20260528` | c6 作文纸横线吸附版本 |
| `tmp/essay_c6_white_band_demo_20260529` | c6 白带检测版本 |
| `tmp/essay_line_cut_demo_batch_20260530_1715` | 多样例物理行切分批量输出 |
| `tmp/essay_line_whiteband_demo_20260603_180707` | 灰底图、白带、行框综合输出 |
| `tmp/essay_formal_physical_line_draw_20260605_152746` | 英文物理行下划线输出 |
| `tmp/essay_api_formal_full_20260608_171207` | 正式接口全量测试输出 |
| `tmp/essay_contact_sheets_20260531_1615` | 中文、英文、普通测试集总览图 |

## 测试集路径

```text
tmp/语文作文素材
tmp/英语作文素材
tmp/普通测试集
```

## 复现思路

完整复现不建议直接依赖历史 tmp 输出，因为中间 demo 曾经多次变更。更稳定的方式是：

1. 启动本地后端。
2. 使用 `run_essay_three_sets_full_8039.py` 或同类全量测试脚本调用正式接口。
3. 保存接口响应 JSON。
4. 用响应里的 `sentenceComments[*].positions` 画图。
5. 生成 contact sheet 做人工巡检。
