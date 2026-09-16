# 产品事实与表达用途

当前调用入口是[个人Pocket知识索引](/Users/luocaihua/.codex/skills/use-pocket-knowledge/knowledge/INDEX.md)，结构化事实在[个人快照products/facts.jsonl](/Users/luocaihua/.codex/skills/use-pocket-knowledge/knowledge/products/facts.jsonl)，每条保留型号、使用条件、用途、不可推断内容、来源定位和核验日期。主库聚焦Pocket4/Pocket4P，按当前帖检索相关项，无需一次读取全库；检索脚本使用[项目写作入口](../SKILL.md)中的个人技能绝对路径，不依赖当前工作目录。本页保留写作边界，不重复知识卡正文

[原项目Pocket知识库](/Users/luocaihua/Documents/ChatGPT/op/knowledge/pocket/INDEX.md)仍是维护源，修改后显式刷新个人技能快照。真实表达保留来源和个案／规律层级，场景中的编辑假设不是用户研究；历史来源不能证明当前帖内容，独立培训人物不写回真实语料或产品事实。已读知识或写作入口只消费必要资料，不循环加载

当前写作从[项目写作入口](../SKILL.md)调用共享表达库。产品断言需重读当前官方资料，保留型号、条件、来源定位和核验日期，并按共享[训练契约](/Users/luocaihua/.codex/skills/write-consumer-comments/references/training-contract.md)放入该帖的`product`来源，绑定最终正文中的`product_fact`断言与实际证据原文。知识卡是查证索引，短定位锚点不等于整条断言已被充分证明；训练人物也不能为产品能力补证

只有真实材料专项核验或旧LH13稿复核才使用`product_facts`与claim注册接口。2026-09-05基线使用过的双镜头/3倍物理镜头、实体变焦键、旋转运镜、跟随等claim继续在 [product-claims.json](product-claims.json)查询；旧核验日期不是今天已核验。在该接口中，未登记的说法先核当前官网再补登记，知识库尚未覆盖的旧claim也须按注册来源复核后使用，不因缺卡就把历史稿判成新事实

LH13允许`pocket_1`、`pocket_2`的明确型号映射，裸`Pocket`仍为代际未知。登记型号只解决映射，不授予所有型号共享某功能。新事实`claim_id=null`表示尚未接入LH13验收注册表，不能拿知识卡ID冒充claim_id；它不要求共享培训流程另跑LH13或补该注册表

产品点名、功能成立和画面因果是三件不同的事：作者标签可以提供型号线索，官方可以证明功能存在，原片若没有操作或对比证据，就不能证明某个效果由该功能带来。用户拥有设备也不证明这三者中的任何一个额外事实

同理，未标设备的2019年旅行片只能触发今天想带Pocket去拍的愿望，不能被写成由Pocket4P拍摄。漂亮人像不证明直出、滤镜、美肤或未调色；只有抽样帧时不补对白、音乐、准确切点或完整教程结论

对新参数、价格、续航、配件、固件功能及竞品比较，先核官方限定条件。找不到可确认的事实，可换成没有该断言的兴趣或明确提问；不把一条带预设的广告断言仅加问号就当作疑问。注册表 [product-claims.json](product-claims.json)供LH13机器映射已知事实；两种模式的产品说法都仍需逐句语义审稿
