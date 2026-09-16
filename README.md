# 阿豹追猎 · 20 Skills 总控版

一个总控接单，按阶段单点触发，全部候选完成后统一去重质检。

```text
总控 S0 → 材料 S1 → 当前品线事实 S2 → 共享写手 S3
                                              ↓
交付 ← 全批主评/回复去重、事实、表达、格式 Q
          └─ 有问题：定点返工 → 全批复检
```

保留原包20个SKILL：1个总控、1个日批规划、1个材料读取、5个知识、1个共享写手、5个只读适配、6个兼容调用名。Q是总控的终审流程，不增加技能数量。

- [安装与DeepSeek使用](INSTALL.md)
- [可粘贴总提示词](SYSTEM_PROMPT.md)
- [总控入口](skills/write-consumer-training-comments/SKILL.md)
- [阶段与返工规则](skills/write-consumer-training-comments/references/stage-contract.md)
- [统一质检](skills/write-consumer-training-comments/references/final-quality.md)
- [全批机器检查脚本](scripts/check_batch_quality.py)及[批次模板](examples/batch.template.json)

脚本检查结构、版本绑定和文本相似候选，语义、事实与自然度仍需逐项审阅。没有脚本运行能力时可以内容复核，但不声称机器检查通过。适配元数据是否生效取决于宿主，不能仅靠上传ZIP保证平台级串行锁。

源文件来自用户提供的“阿豹追猎.zip”。保留原知识、写作表达参考及来源资料；打包日期不代表已重新核验产品事实。默认产物为标明性质的培训草稿，不包含自动发布或账号操作。
