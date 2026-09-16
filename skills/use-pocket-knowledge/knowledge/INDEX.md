# Pocket 产品与用户表达库｜个人调用版

重点Pocket4、Pocket4P。资料随个人技能携带，可在其他项目或对话读取；维护源仍为原op项目，按明确更新请求重新封装，不自动同步。

日常先读[一页使用入口](START.md)。历史采集按原范围封存；后续仅按用户明确授权的新批次更新，缺口与实际完成范围分别记录。

## 按需入口

| 任务 | 资料 |
|---|---|
| 拍摄观感、个人审美与真实接话 | [观感与表达](aesthetics/README.md)；有限画面、作者处理说明、单组讨论和用户原句反馈，完整实拍作品仍待补 |
| 卖点与使用价值 | [卖点指南](selling_points/guide.md)；能力、用途解释、条件和取舍 |
| 详细场景与培训选材 | [细场景指南](use_cases/guide.md)、[选材入口](TRAINING.md)；可按型号正查与按卖点反查 |
| 两款功能与操作差别 | [按使用环节对照](products/pocket4-vs-pocket4p.md)、[主题与缺口](products/topic-coverage.md) |
| 产品事实及官方依据 | [事实表](products/facts.jsonl)、[官方来源](sources/official.jsonl) |
| 用户为什么开口、怎样提问和承接 | [表达入口](voice/README.md)、[表达卡](voice/cards.jsonl) |
| 已确认上下文、本人素材与明确反馈 | [上下文](context/README.md)、[反馈与归属](feedback/README.md)；不等同于公共反馈或认可范文 |
| 比较设备、保留其他选择与不升级 | [比较专题](comparisons/README.md)、[可检索比较卡](comparisons/cards.jsonl)；历史与新批次分别标注 |
| 使用场景与需求 | [场景说明](scenarios/README.md)、[场景卡](scenarios/cards.jsonl) |
| 研究原件、增量与验收 | [研究批次](research/README.md) |
| 当前覆盖与边界 | [覆盖](COVERAGE.md)、[待核](GAPS.md) |
| 追溯与刷新 | [封装说明](PACKAGE.md)、[包内路径映射](package-map.json) |

主款 80 条已核事实、2 条待核事实；33 张表达卡（其中历史种子 12 张）、13 张需求卡、5 张比较表达卡、16 张卖点卡和 22 张详细场景卡。已入库评论 526 条：B站 34 条、小红书 492 条。历史评论种子另计 372 条；停止附件另存 58 条，不参与学习。评论数包含保留的学习/留出分组，不代表全部可供学习或全平台覆盖。

完整动态计数、旧基线与本次增量见[统计及基线核验](corpus-statistics.json)。卖点使用价值为编辑解释，场景中的证据与假设按卡片标注，不自动增加真实用户样本。历史样本和已取消的150/30规模保留追溯，不充当新批次的完成或扩量要求。

## 查询方式

先从技能所在目录定位本文件的同级scripts，不依赖当前工作目录。例如将 `<知识目录>` 替换为本文件所在绝对目录：

```bash
python3 "<知识目录>/scripts/pocket_knowledge.py" search '人物 中焦 收音' --model pocket_4p
python3 "<知识目录>/scripts/pocket_knowledge.py" search '收纳 麻烦 闲置' --platform xiaohongshu
python3 "<知识目录>/scripts/pocket_knowledge.py" audit --format json
```

默认排除holdout，查不到不等于不支持。产品断言核对当前官网；网友原话不证明功能。pattern/case只说明已见表达证据范围，编辑假设不冒称心理调研。个人素材指原资料中的说话者，不赋给其他对话的任意使用者。日常统一简报命令见[统一入口](START.md)，能力登记见[library.json](library.json)。

[两帖历史对照](evaluation/small-sample/README.md)含留出材料，仅供回顾验收，不是写手学习或认可范文。

需要评论时读取[共享写手](../../write-consumer-comments/MODULE.md)和[Pocket边界](../../write-dji-pocket-comments/MODULE.md)；知识问答无需先进入写作。旧报告、研究示例和已封存规则均为历史材料，不覆盖当前写手。
