# Osmo 360 内容与运营团队培训知识库

第一版核验日期：2026-09-06。对象：需要解释功能、判断拍摄场景、检查产品表达的内容与运营团队。语言为简体中文，默认使用环境为中国大陆；海外来源、版本与不确定项单独注明。

## 项目其他对话直接调用

在同一op项目的对话中，可以直接说：

- “调用Osmo360知识库，解释两代导出流程的差异，给出依据和限制”
- “调用Osmo360卖点库，解释隐形自拍杆对独自旅行者有什么价值和条件”
- “这个骑行角色适合讲哪些卖点，已有运动相机什么时候就够用？”
- “调用Osmo360场景库，发散家庭、旅行和已有设备人群的培训文案选材”
- “调用360消费者心理库，深入分析骑行者为什么想拍、为什么可能不用，以及表达线索”
- “按项目360标准，用两个不同角色写培训评论，保留产品依据”

也可明确调用 `$use-osmo360-knowledge`。入口文件是[项目360技能](../../.agents/skills/use-osmo360-knowledge/SKILL.md)，由项目 `AGENTS.md` 和共用写手入口接入；不需要重读本次历史聊天。若当前对话尚未发现新技能，直接让它读取这个入口文件即可。

[人群与心理指南](../../.agents/skills/use-osmo360-knowledge/references/audience-guide.md)包括23种重叠情境标签、8个心理关注方向、使用阶段与访谈验证问题，均是待验证编辑假设。实际评论仍由共用写手库完成；[历史8条示例](../../outputs/osmo360/2026-09-06-audience-psychology/draft.md)只是待校准训练材料。

## 从这里开始

补充专题：[卖点与用户价值](selling-points.md)。按拍摄视角、影像表现、创作方式、使用便利、完整流程五组查阅，两代分别给出官方能力、可能收益、人群心理、场景、条件与取舍；另有[角色选材](selling-points.md#roles)及[选用与升级判断](selling-points.md#upgrades)。这是建立在事实卡上的解释层，`oq`与项目360技能均可调用。

详细选材：[48张使用场景卡](scenario-bank.md)，每卡提供事件、任务、主辅卖点、心理矛盾、拍摄到交付、条件及三个不同角度；从已有卖点反查[任务变化矩阵](training/scenario-to-copy.md#value-matrix)，组织讲解可看[心理分歧及训练命题](training/scenario-to-copy.md#psychology)。这些材料接入`oq`，不是固定评论模板。

体验材料补强：[空间视角与拍后选择](training/experience-materials.md)，保留原片、不同导出、必要处理与使用者偏好；[9份本地材料与缺口](materials/STATUS.md)区分实际作品、原话、讨论和假想稿。新增[两次试机的原话与上下文](materials/first-use.md)及[M09动作教学](materials/action-tutorial.md)，学习初学尝试、购买后练习、编辑负担与当次满意的区别。共用四类材料和逐句反馈由共享写手维护，不给每个品线限定一种卖点。

初次学习按下面八个模块阅读；查具体产品看型号入口；审核一句产品说法时，打开知识卡核对模式、条件和来源。这里的产品档案是培训摘要，最终依据是可追溯的事实卡。

| 顺序 | 模块 | 学习后能够完成的任务 |
|---|---|---|
| 1 | [全景相机基础](modules/01-basics.md) | 解释全景、单镜头、拼接和重构成片 |
| 2 | [两代产品与差异](modules/02-models.md) | 准确区分两代功能与拍摄规格 |
| 3 | [拍摄操作](modules/03-capture.md) | 描述准备、安装、拍摄、收音、传输的流程 |
| 4 | [后期工作流](modules/04-postproduction.md) | 分清机内拍摄、软件处理和最终导出 |
| 5 | [配件与维护](modules/05-accessories.md) | 解释兼容条件、镜片维护和水下限制 |
| 6 | [六类场景与内容理解](modules/06-scenarios.md) | 把功能对应到任务，并说明使用前提 |
| 7 | [竞品培训](modules/07-comparison.md) | 按相同维度比较产品，识别证据不足 |
| 8 | [问答、自测与培训组织](modules/08-learning.md) | 用问题复习，检查答案是否有依据 |

## 按型号查阅

| 型号 | 产品档案 | 结构化事实 |
|---|---|---|
| Osmo 360（第一代） | [档案](products/osmo_360.md) | [JSONL](products/osmo_360.facts.jsonl) |
| Osmo 360 II | [档案](products/osmo_360_ii.md) | [JSONL](products/osmo_360_ii.facts.jsonl) |
| Insta360 X6 | [档案](products/insta360_x6.md) | [JSONL](products/insta360_x6.facts.jsonl) |
| Insta360 X5 | [档案](products/insta360_x5.md) | [JSONL](products/insta360_x5.facts.jsonl) |
| GoPro MAX2 | [档案](products/gopro_max2.md) | [JSONL](products/gopro_max2.facts.jsonl) |

## 按问题查阅

- 基础概念、分辨率、两代差异：[FAQ Q01—Q08](training/faq.md#q01)。
- 自拍杆、近距离、水下、镜片、麦克风、电池：[FAQ Q09—Q18](training/faq.md#q09)。
- 激活、存储、文件、手机与电脑后期：[FAQ Q19—Q25](training/faq.md#q19)。
- 竞品、使用成本和比较结论：[FAQ Q26—Q30](training/faq.md#q26)。
- 全部知识与原始依据：[知识卡目录](CARDS.md)、[官方来源登记](sources/INDEX.md)。
- 未确认或有冲突的问题：[缺口清单](GAPS.md)。
- 如何增加资料和同步修订答案：[维护说明](MAINTENANCE.md)。
- 第一版完成情况、修订及验证：[建设记录](BUILD.md)、[首版验收](evaluation/acceptance.json)、[项目调用封装验收](evaluation/project-reuse-2026-09-06.md)。
- 卖点补充与本轮核验范围：[2026-09-07卖点验收](evaluation/selling-points-2026-09-07.md)、[一代来源复核](sources/recheck-selling-first-2026-09-07.md)、[II代来源复核](sources/recheck-selling-second-2026-09-07.md)。

本轮详细场景扩展：[官方依据复读](sources/recheck-scenarios-2026-09-07.md)、[验收记录](evaluation/scenario-expansion-2026-09-07.md)。

体验材料维护与验证：[2026-09-08补充记录](evaluation/experience-materials-2026-09-08.md)。

当前入口与事实检索烟测：[2026-09-09本地维护记录](evaluation/oq-smoke-2026-09-09.json)。仅验证当前文件和已存知识卡检索，不刷新官方来源或重新采集社媒。
本次学习验收：[2026-09-09验收记录](evaluation/learning-acceptance-2026-09-09.md)。以最新本地审计和19项测试为准；首版验收JSON保留历史快照。

## 本地检索

在项目根目录使用 Python 3。型号参数可选 `osmo_360`、`osmo_360_ii`、`insta360_x6`、`insta360_x5`、`gopro_max2`；明确参数优先，其次识别问题中的明确产品名，其余情况搜索全部五款。已核验答案连同限制条件返回，相关待核验或冲突卡在“相关缺口”中单列。精确卡号只匹配该卡，不返回其他型号的同尾号卡；无命中不代表设备不支持该功能。

```bash
python3 knowledge/osmo360/scripts/knowledge.py search '隐形 自拍杆 拼接' --model osmo_360
python3 knowledge/osmo360/scripts/knowledge.py search '跟随 导出' --model osmo_360_ii
python3 knowledge/osmo360/scripts/knowledge.py search '续航 条件' --format json
python3 knowledge/osmo360/scripts/knowledge.py audit
```

## 资料的含义

- **官方事实**：来自实际读取的品牌官方资料，核验日期和适用条件记录在卡片中。`verified` 不表示已经实机测试，也不保证以后版本不变。
- **编辑解释**：为教学而组织的概念、步骤和比较方法；不能当作品牌额外承诺。
- **假想场景**：说明在某种任务中如何考虑功能，不代表真实用户访谈、实拍效果或运营成绩。

本库交付产品培训资料和场景推演；消费者评论训练另按项目共用写手流程处理。假想案例不进入真实体验或官方事实记录。首版没有采集社交平台素材，也不以营销标语作为画质胜负证据。
