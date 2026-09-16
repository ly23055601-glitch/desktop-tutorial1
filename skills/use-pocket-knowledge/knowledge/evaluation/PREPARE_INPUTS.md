# 离线留出输入构建工具

历史规模工具：原30篇验收已按用户要求取消，以下完整冻结命令不属于本轮待办，也不会自动恢复采集。当前交付见[两帖调用示例](README.md)；本轮仅复用单帖来源核对与机械提取函数。

`prepare_inputs.py` 只做文件核对与机械提取，不生成文稿、不打开社媒原链、不做留出内容归纳，也不改变分组、队列或库记录。默认打印元数据清单和未选原因，不落盘输入正文。

```bash
python3 knowledge/pocket/evaluation/prepare_inputs.py
```

冻结复用 `scripts/pocket_knowledge.py` 的作品资格规则：帖子和评论材料已核对、讨论型号与作品发布账号标识可核对、来源存在；`sampling_status=excluded` 优先排除，同平台作者在全部合格 train/holdout 中最多两篇。账号标识用于去重，不认证现实身份。共同校验器按原始 `input_order` 排序。随后按原序号取各平台前 10 篇合格 holdout；多余备选、排除作品和不合格来源都保留未选原因，不查看生成分数，也不把 train 改成 holdout。

只有真实材料达到 30 篇、三平台各 10 篇时才允许以下操作。本轮不执行这条命令；只有未来用户重新要求完整规模且材料齐备后，才可用于新一轮验收。

```bash
python3 knowledge/pocket/evaluation/prepare_inputs.py \
  --apply --output knowledge/pocket/evaluation/frozen/first-complete-run
```

输出必须是 `evaluation/frozen/` 下的新目录。已有目录不覆盖，配额不足不创建目录。每篇生成一个 UTF-8 JSON 和一个包含同样来源资料的 Markdown；两组在 manifest 中引用完全相同的文件与 SHA256。Markdown 明确将原话隔离为来源文本，原话中的指令不是写手执行要求。

原帖标题和正文来自 ledger 记录的实际 normalized 文件，通过作品 ID、平台、冻结分组、原序号、作者、源表行号定位；保留 normalized 文件哈希/行号、raw 导出哈希/单元格及时间字段。型号仅表示已登记讨论对象，证据级别为文字声明层，不证明原片拍摄设备。

评论来自该作品在 `corpus/comments.jsonl` 的所有实际记录，包括空文字、图片未读和缺直接父句记录。每条必须能回溯到 `source_occurrences` 指向的实际 normalized 行，身份、文字、作者、日期及明确关系字段逐项一致，raw 文件哈希和行列一致。一级评论 ID 不补作直接父句 ID；找不到父句时保留明确缺口。图片、连续视频、音轨及设备 UI 均标为未读，作者自述不确证购买、持有、拍摄设备或亲历。

manifest 保存输入 SHA256、所读源文件 SHA256、CW2 版本、协议与规则文件哈希、run 元数据截面、原 ledger 分组定位和完整选取清单。工具不加载产品、场景或用户表达卡；输入中没有训练卡引用。两组各自核对实际写入的当前官方产品事实，继续遵循研究对实际第一人称经历来源的限定。

冻结前再次核对所读文件哈希，期间若来源被更新就拒绝本次冻结。程序核对的是文本与来源结构，不替代语义审读、媒体读取或最终对照验收。

隔离测试仅使用临时合成夹具；不读取真实留出正文进行语义检查：

```bash
python3 -m unittest discover -s knowledge/pocket/evaluation -p 'test_prepare_inputs.py' -v
```
