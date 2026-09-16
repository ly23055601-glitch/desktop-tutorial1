> 跨项目查询：将命令中的 `<技能目录>` 替换为当前个人技能 SKILL.md 所在绝对目录；不从工作目录猜原项目路径。

# Pocket表达库：当前可用版

服务Pocket4/Pocket4P写作，提供真实材料中的关注点、提问方式、偏好与表达机制。旧轮已按用户要求用现有材料收尾，停止采集和扩量；不再以150篇作品或30篇留出验收作为交付门槛。既有来源、分组和限制继续保留。

2026-09-10新增6张B站表达个案，来源为11条评论、5篇作品。其余本批评论归档；不全当产品反馈。见[本批真实讨论](../_provenance/project/outputs/social-comment-research/2026-09-10/op-pocket-7d-01/discussions.md)、[研究报告](../_provenance/project/outputs/social-comment-research/2026-09-10/op-pocket-7d-01/analysis.md)与[比较表达](../comparisons/README.md)。统计从[动态覆盖](../COVERAGE.md)读取；下表C1/C2数字保留原批次范围。

## 现在有什么

| 材料 | 当前内容 | 使用范围 |
|---|---|---|
| 新公共帖子原话 | 37篇已读train作品作者原话，存在[records.jsonl](records.jsonl) | `public_post`，是作者自述或主题，不是评论或楼中楼 |
| 新真实评论 | C1/C2共492条，存在[corpus/comments.jsonl](../corpus/comments.jsonl)；404条train、88条holdout | 已分析26篇合格train作品的346条；表达卡引用其中39条，不复制记录或重复计数；holdout不参与归纳和常规检索 |
| 历史评论种子 | 18篇作品、372条legacy评论，也在[records.jsonl](records.jsonl) | 学表达机制；历史Pocket3及未知型号不能代表4/4P人群 |
| 可检索表达卡 | [cards.jsonl](cards.jsonl)当前数量见动态覆盖；历史卡、帖子卡和各批评论卡分别标注 | 按每张卡的证据和边界使用，新批case不升级为规律 |

`voice/records.jsonl`本身共409条：372条legacy评论＋37条新帖子原话。新评论由检索器从`corpus/comments.jsonl`合并读取，原ID和来源不变。

## 从哪里开始用

先确定当前帖让人关心什么，再选少量相关卡，看其`need`、`mechanism`、原句和`not_transferable`。例如：

```bash
python3 "<技能目录>/knowledge/scripts/pocket_knowledge.py" search '旅行 人像 不看价格' --model pocket_4p --platform xiaohongshu
```

也可以直接提出：**“调用Pocket知识库，结合这条帖的具体处境，找相关产品条件和真实表达机制，再按项目标准写。”** 当前评论草稿仍走[当前项目写手入口](../../../write-dji-pocket-comments/SKILL.md)；实际写入的产品能力、模式和配件条件另核官方来源。

| 想找什么 | 入口 |
|---|---|
| 作者怎样说认可、不便、观感、流程负担和选择 | [8张公共帖子卡](public-post-cards.md) |
| 有明确父句时怎样追问、同感、保留不确定性 | [C1评论卡与真实父句](comment-c1-cards.md) |
| 4/4P选择条件、基础练习、配件问题及独立评论观点 | [C2补充与当前卡片范围](comment-c2-cards.md) |
| 历史语言机制及原来源 | [历史迁移统计](legacy-migration-report.json)、[18篇历史元数据](works.jsonl) |

## 使用边界

- 新pattern至少有3个独立作品、3个可核对作品发布账号支持；这是表达例证，不代表人口比例、购买转化或使用效果。case保留为单例或少量案例。
- “人群口吻”从句中处境、需求和立场来，不按年龄、性别、职业套固定人设。`stage`是表达处境，不是身份认证。
- 新帖子发言者是作品作者；新评论发言者是评论者。第一人称保持原归属，不能把别人的购买、持有或经历移植为写手亲历。
- C1选中回复有实际父句和根句可追溯；C2没有根/引用关系字段，全部`thread_role=unknown`，只能分析评论本身，不能补成对话。评论者账号未认证，昵称不作为独立个人证明。
- 本库读取的是实际导出文字，图片、连续视频、音轨和设备UI未读。原话里的效果、参数、价格、补贴与产品判断不是官方事实。

新帖子卡、C1评论卡和C2变更均有独立模型审读记录；这不是用户认可或真实消费者亲历认证。C2最终审读与检索检查见[comment-c2-independent-review.json](comment-c2-independent-review.json)，C1原始范围见[comment-c1-independent-review.json](comment-c1-independent-review.json)。

来源追溯保留原作品/评论ID、normalized行号、raw文件哈希、表格单元格及已知父句；缺失项不补写。重建脚本只用于维护现有材料，不执行采集；重建后的内容需重新核对，不能自动沿用旧审读结论。
