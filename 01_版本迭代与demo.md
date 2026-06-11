# 01 版本迭代与 Demo

## V1：直接使用 OCR 坐标

最初方案：

```text
图片 -> OCR -> 得到文字块和坐标 -> LLM 输出 target_text -> target_text 匹配 OCR 文本 -> 返回坐标
```

优点是实现简单，OCR 本身就有文字和坐标。问题是手写作文里 OCR 坐标不是按完整句子返回，而是按行、半行、短语返回。LLM 输出的句子又经常和 OCR 文本不完全一致，所以容易出现：

- 只画到半句话。
- 画到下一行。
- 线压在字中间。
- `target_text` 和坐标对应不上。

代表效果：

![V1 OCR 原始坐标效果](./assets/v01_raw_ocr_c6_incomplete.jpg)

结论：原始 OCR 坐标可以作为基础数据，但不能直接作为最终画线结果。

## V2：按作文纸横线吸附

第二个方向是尝试检测作文纸上的横线，把下划线吸附到横线附近。

Demo 目录：

```text
tmp/essay_c6_grid_snap_demo_20260528
```

代表效果：

![V2 方格横线吸附](./assets/v02_grid_snap_c6_contact.jpg)

这个方案在方格作文纸上有一定效果，但问题也明显：

- 不同作文纸格式不一样，不能假设都有规则方格。
- 有些图片没有横线，或者横线很浅。
- 有些手写字会压在线上，吸附作文纸横线仍然可能穿字。

结论：不能只检测作文纸格线。格线是纸的结构，不一定是适合画下划线的位置。

## V3：找文字行之间的空白带

后来改成检测“行字之间的白带”，而不是检测作文纸横线。

Demo 目录：

```text
tmp/essay_c6_white_band_demo_20260529
tmp/essay_line_whiteband_demo_20260603_180707
```

代表效果：

![V3 白带检测 c6](./assets/v03_white_band_c6_contact.jpg)

白带检测的核心想法：

```text
先把图片二值化
再去掉横线、竖线等规则线
只保留文字墨迹
在线附近找黑色像素最少、连续稳定的横向区域
```

这个方案比横线吸附更通用，因为不依赖作文纸样式。但它仍然依赖初始坐标，如果初始 OCR 框错了，白带也救不回来。

结论：白带适合做“下划线避让”，不适合单独解决句子定位。

## V4：物理行切分

真正明显改善的是物理行切分。

Demo 目录：

```text
tmp/essay_line_cut_demo_batch_20260530_1715
tmp/essay_line_whiteband_demo_20260603_180707
```

代表效果：

![V4 物理行框选](./assets/v04_physical_line_boxes_normal.jpg)

流程：

```text
原图
-> 图片增强
-> 灰度和二值化
-> 去规则线
-> 计算文字墨迹投影
-> 切出一行一行的文字区域
-> 给每一行计算左右边界和斜率
```

这一版解决了很多坐标问题：

- 坐标来自真实物理行，不再完全依赖 OCR 大框。
- 每一行可以有轻微斜率，最终可以画斜线。
- 对手写作文更自然。

同一批 demo 里还输出了白带检测图：

![V4 白带检测](./assets/v04_white_band_detection_normal.jpg)

结论：物理行切分是后面正式方案的基础。

## V5：物理行识别 + 英文样例

中文作文能切行后，又测试英文作文。英文的问题是单词之间空隙大，行内墨迹分布更碎，不能直接套中文参数。

Demo 目录：

```text
tmp/essay_formal_physical_line_draw_20260605_152746
```

代表效果：

![V5 英文物理行画线](./assets/v05_physical_line_english_underlines.jpg)

这一步主要验证：

- 英文行切分是否稳定。
- 倾斜行是否能画斜线。
- 下划线是否压到英文手写体。
- 句子跨行时是否能保留多个坐标段。

结论：物理行方案对英文也能用，但需要更严格的候选句过滤。

## V6：句子候选 + 分句点评

物理行只是“行”，但点评要的是“句子”。所以又加了句子候选构造：

```text
物理行文本 -> 按标点和上下文拼成句子候选 -> 给每个候选句生成 sentence_id
```

候选结构：

```json
{
  "sentence_id": "image_001_sentence_003",
  "source_image_index": 1,
  "text": "经过一夜火车的颠簸，我们终于在清晨抵达了山脚。"
}
```

然后要求 LLM：

```text
只能从 sentence_candidates 里选择问题句；
不要自己改写 target_text；
不要评价逗号、句号、不是完整句这类问题；
最多返回 3 条。
```

这样分句点评天然带有 `sentence_id`，后端可以反查对应坐标。

结论：让模型从可定位候选里选句，比“模型自由输出句子再匹配坐标”稳定。

## V7：正式接口全量验证

正式接口验证目录：

```text
tmp/essay_api_formal_full_20260608_171207
tmp/essay_contact_sheets_20260531_1615
```

代表效果：

![最终中文 c6](./assets/final_chinese_c6_page3_underlines.jpg)

![最终英文 e6](./assets/final_english_e6_page1_underlines.jpg)

结论：最终版本不追求每句话都画，而是只画“点评内容和坐标能对上”的句子。
