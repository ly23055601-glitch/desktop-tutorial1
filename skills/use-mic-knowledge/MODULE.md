---
name: use-mic-knowledge
description: 调用 DJI Mic 产品与人群能力库，回答六款 Mic 的产品和连接问题，关联卖点、详细使用场景、角色心理与培训文案选材。适用于“调用Mic知识库”“Mic卖点”“Mic使用场景”“Mic使用人群”“Mic使用心理”及 dm 产品路径。评论培训接入共享写手；场景与用途价值不作为用户研究。
---

# DJI Mic 产品与人群能力库

这是可从任意项目使用的独立资料包。先按任务选择下述资料，无需读取原项目或历史聊天。包内数据是所列核验日期的快照；引用当前产品能力时复核对应官方来源。

## 产品问答

读取[产品索引](references/knowledge/INDEX.md)，按精确型号检索。将下面的 `<技能目录>` 替换为当前 MODULE.md 所在目录的绝对路径；命令不依赖工作目录，仅需 Python 3.9+ 标准库。

```bash
python3 "<技能目录>/scripts/mic.py" search '四个人接相机能分开声道吗' --model mic_3
python3 "<技能目录>/scripts/mic.py" search '手机版接收器怎么连接' --model mic_mini_2s --format json
python3 "<技能目录>/scripts/mic.py" audit --format json
```

六款型号：`mic`、`mic_2`、`mic_3`、`mic_mini`、`mic_mini_2`、`mic_mini_2s`。重点为 Mic 3、Mic Mini 2S；不确定型号时呈现各型号归属，不能默认最新款或把多款能力合并。

回答保留事实 ID、具体部件、连接方式、条件、限制、官方来源定位和实际核验日期。`pending`／`conflict` 不能成为肯定能力；[缺口](references/knowledge/GAPS.md)与明确不支持分别处理。发射器内录、接收器输出、宿主保存与平台音轨分别核对；标准和手机版接收器、蓝牙与 OsmoAudio 不能互推。官方冲突按条件、地区和版本处理，不能按页面种类或更有利的结论覆盖另一方。

## 卖点与用途价值

读取[卖点指南](references/knowledge/selling_points/guide.md)，按具体型号、任务或困扰选择相关卖点：

```bash
python3 "<技能目录>/scripts/mic.py" selling-points --model mic_3 --limit 20
python3 "<技能目录>/scripts/mic.py" selling-points '四人采访备份' --model mic_mini_2s --format json
```

每张卡关联官方事实、适用角色、用途价值、条件、限制及本次来源复核。用途价值是编辑推导，不能当作官方承诺、真实用户心理、实测优越或购买结果。选材围绕当前任务，不要求凑齐功能，不按一个卖点复制同一套人物心理。内录、输出与后期保存等多条件问题可拆开检索；卖点卡不能替代底层事实和当前官方核验。具体评论仍交共享写手表达。

需要进一步发散时读[需求与价值解读](references/knowledge/selling_points/value-expansion.md)，它把相同能力放进不同任务、使用阶段和偏好中。已知卖点编号时用[卖点反查场景](references/knowledge/writing_scenarios/selling-point-map.md)，按实际内容选一点，不把资料字段拼成评论模板。

## 详细场景与培训选材

需要发散使用场景、把卖点落到具体任务，或为培训文案选材时，读取[场景指南](references/knowledge/writing_scenarios/guide.md)，按角色、动作、时刻或协作任务检索：

```bash
python3 "<技能目录>/scripts/mic.py" scenes '手上拿着工具还要讲解' --model mic_mini_2s --limit 2
python3 "<技能目录>/scripts/mic.py" scenes '异地播客各自保存录音' --format json
python3 "<技能目录>/scripts/mic.py" scenes --family '商业与团队协作' --model mic_3
python3 "<技能目录>/scripts/mic.py" scenes --selling-point MIC3-SP003 --limit 10
```

卡片区分具体时刻、用户任务、可能心理、真实原帖中可触发的线索、分型号候选路线、关联卖点、可取的表达角度与不适用情形。路线只说明基于功能可考虑的方案，具体宿主和 App 仍需核验；检索按型号保留相关路线，无法核验的依赖单列待核。

分析字段用于选材，不能拼成固定句式；从当前原帖确实能接住的关注点取用，心理不默认是焦虑，兴趣也可以来自习惯、审美、参与感或细节好奇。`post_cues` 是待观察线索，不证明原帖存在该画面或声音。需要实际评论时由共享写手完成；人物、假想经历和最终稿保存在具体任务，不写回场景知识。场景指南中的扩展方法不覆盖共享层文风、数量或互动判断。

## 声音与真实使用材料

需要理解实际录制过程、声音听感、使用者原话或完整讨论时，读取[Mic体验材料指南](references/knowledge/training/experience-materials.md)，从[材料盘点](references/knowledge/materials/STATUS.md)按原帖子类型找已有作品候选。可看[三份轻量便笺](references/knowledge/materials/examples.md)、[原话／反馈范围](references/knowledge/materials/utterances-and-feedback.md)和[真实讨论选材](references/knowledge/materials/discussion-context.md)。当前53条记录包括P003的13主评＋5回复、P004的31主评＋3回复、P006的1条层级未知导购；8组直接父句关系有实际出处。P004的14条原页补读仅有本地编号，5条贴纸未读；数量对齐不等于全媒体内容完整，导购不作使用体验。个人说法与编辑理解不写回产品事实。[机器转写索引](references/knowledge/materials/asr-index.md)中的7次处理仅有4份中文待核定位、3份异常，均未听音复核。[录制过程](references/knowledge/materials/recording-process.md)保留P001／P004的界面状态与连接提示；[P009上手阶段](references/knowledge/materials/p009-first-use.md)提供动机、拆夹与佩戴计划的局部字幕。共重看17张历史帧，另查看3张新定点帧，仍不是完整教程或声音评测。

本地视频已存在不等于实际听过；实际听音、采访／边走边聊材料、未读贴纸与Mic逐句认可仍有缺口。发布文字、烧录字幕、本人随口语音、编辑观察与真实反馈分别保留性质，未确认型号、输入和后期不能靠听感或假想经历补齐。素材库不调用`scenes`生成真实经历，不把候选计为已完成声音评测。五品线共用收录规则使用相邻写手的[体验材料指南](../write-consumer-comments/references/experience-materials.md)，不复制另一套采集和写法。

另见[公开作者的录制选择与音频样本](references/knowledge/materials/published-experience.md)：7篇原出版物文字、1份Mini 2S公开WAV样本及3个步行／采访作品链接，独立于历史社媒与评论计数。作者的酒店工作、模拟噪声、操作偏好和后期取舍属于公开自述，不能当私聊、已核产品结论或消费者规律；样本仅下载与检查容器，尚未听取。[步行Vlog](references/knowledge/materials/walking-vlog.md)在Chrome核对原页及原生转写，播放被登录验证阻断；标准WAV输入也确认当前工具不支持听音。转写不作准确逐字稿或已看听成品。另有[Mic Mini 2两份采访](references/knowledge/materials/interview-pair.md)，作者分别说明未处理与后期处理；Sophia原页及转写首尾已读，Jo／Caroline仅核嵌入标题和链接，均未听音。原文型号称呼、宿主与条件保留出处，未知部分不补造，USB部件称呼冲突不静默纠正。

个人包携带盘点与说明；大视频、图片和原始历史证据仍在既有位置，迁移后须另外取得才可复核。只取当前材料最值得说的一点，不把完整过程拼成句式。知识维护和材料整理不登记为每日新稿。

## 真实评论资料

用户于 2026-09-10 停用本次接入的 Apify 付费采集工具；不再调用其话题发现入口。已有真实评论和来源可继续分析；需要读取抖音、小红书、B站时，将当前请求完整链接集合一次性交给[统一社媒读取](../read-social-links-with-social-helper/MODULE.md)。产品知识和默认培训路径继续使用，研究不计培训新稿 KPI。

## 人群、动机与心理表达

读取[角色心理指南](references/knowledge/audience/guide.md)，按任务检索角色卡：

```bash
python3 "<技能目录>/scripts/mic.py" audience '采访时不想打断对方' --format json
```

这些资料是 `editorial_hypothesis`，无消费者调研证据，均待用户校准。角色与工作方式标签允许交叉，不能据此声称真实用户占比、普遍心理或购买转化。用“触发情境—可能动机—矛盾与取舍—行为线索—表达方向—反例”解释；同一句需求可能有不同原因，不按职业给人贴心理标签。产品场景链接用于另行核对能力，不证明心理假设。只分析心理时，无需进入评论写作流程。

## 评论与教学演示

只有任务要求写评、改写或评论案例时，接入相邻个人技能[共享消费者写作](../write-consumer-comments/MODULE.md)，使用 `content_mode=training_fiction`、`product_line=mic`；补充[Mic 专属边界](../write-dji-mic-comments/references/product-knowledge.md)。已读入口不回调；共享路由只读取本包数据索引，避免循环。知识层不另定文风、数量、回复结构或检查器。

假想人物、经历与主观感受保存在具体任务，不能写成用户真实经历、官方事实或原帖证据。指南教学片段为待校准样例，不能自动升级为认可范文。实际产品断言绑定当前核验的 `product` 来源与 `product_fact`，知识 ID 不替代实时核验。社媒读取遵循共享层统一技能，不在本库另建采集流程。本技能不授权发布。

产品问答和心理分析可独立运行；评论生成依赖同机的共享写手及 Mic 专属资料。迁移到另一台机器时按[封装说明](references/package.md)处理依赖。
