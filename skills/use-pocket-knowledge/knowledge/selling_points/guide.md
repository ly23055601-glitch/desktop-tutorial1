# Pocket4 / Pocket4P 卖点与用户价值

本层把产品事实转成可讨论的使用价值，方便问答、场景选材和培训准备。范围仅 Pocket4、Pocket4P；2026-09-07建立16张卡，不是产品排名，也不是用户研究。

## 使用顺序

先确认具体型号、要完成的动作与愿意承担的后期/配件步骤。再选一至两张相关卖点，读取关联事实的完整条件与来源，最后进入[详细使用场景](../use_cases/guide.md)。事实说明设备能做什么；`user_value`、`relevant_needs`、`tradeoffs`和场景方向均为编辑解释或待验证假设，不能写回真实用户经历。

每张卡保留`models`、`fact_ids`、`conditions`、`not_infer`、`tradeoffs`和`source_check_ids`。双型号卡使用`model_notes`分别绑定事实；单型号检索只消费该型号的能力和事实，不能因为卡片列了两款就迁移参数。零命中或缺口不表示产品不支持。

## 从需求找卖点

| 卖点 | 型号 | 适合先问的需求 |
|---|---|---|
| PSP-001 Pocket4：明暗反差场景的成像基础 | Pocket4 | 同时照顾人物与明亮背景；在夕阳或夜色中保留环境层次 |
| PSP-002 Pocket4P：广角D-Log 2为大反差素材留后期余地 | Pocket4P | 明亮窗景与室内人物同框；保存日落天空和人物的层次 |
| PSP-003 Pocket4P：环境广角与人物中焦各有独立镜头 | Pocket4P | 既拍场景又拍人物表情；不总把镜头贴近被拍者；在桌面拍摄中确认可用距离 |
| PSP-004 手持移动时用机械增稳减轻画面抖动 | Pocket4/Pocket4P | 移动镜头更易观看；手持记录时兼顾构图与走位 |
| PSP-005 选定主体后让云台参与持续取景 | Pocket4/Pocket4P | 一个人出镜时维持取景；主体移动时减少手动转镜头 |
| PSP-006 Pocket4P：多人同框与优先主角分别设置 | Pocket4P | 多人都进入画面；在人群中保持明确主角 |
| PSP-007 站到出镜位置后用手势启停 | Pocket4/Pocket4P | 一个人开拍和收尾；固定机位拍动作或穿搭 |
| PSP-008 Pocket4P：在出镜位置查看构图并遥控 | Pocket4P | 独自拍摄时确认构图；机身不在手边也能调整取景 |
| PSP-009 两位讲话者可分别佩戴兼容发射器 | Pocket4/Pocket4P | 双人对话；出镜者离相机较远时收声 |
| PSP-010 Pocket4：外部人声之外保留机身声音备份 | Pocket4 | 外接麦时还想保留现场声；为声音整理多留一个选择 |
| PSP-011 把短暂动作录成可慢放的素材 | Pocket4/Pocket4P | 看清短暂动作细节；为剪辑安排少量慢放段落 |
| PSP-012 按型号和Log种类安排还原与调色 | Pocket4/Pocket4P | 希望自己调色；多段素材色彩整理；拍摄时检查Log监看 |
| PSP-013 拍摄时先决定人物修饰程度 | Pocket4/Pocket4P | 减少逐段手工修饰；在拍摄前统一人物呈现 |
| PSP-014 实体变焦键缩短倍率切换操作 | Pocket4/Pocket4P | 减少寻找屏幕倍率按钮；快速切换构图范围 |
| PSP-015 内置存储让临时拍摄少依赖一张卡 | Pocket4/Pocket4P | 临时拿起就拍；短途携带少一个存储准备项；保留扩展空间选择 |
| PSP-016 按旅途和回家两种环境选择导出路径 | Pocket4/Pocket4P | 外出先取少量片段；回家集中整理原片；减少素材滞留机身 |

## 证据与边界

- [结构化卖点卡](cards.jsonl)只引用主库中`verified`且型号匹配的事实；[本轮官方核验记录](current-official-review.json)逐项保存实际读取的来源与范围。卖点卡日期不等于底层整表事实已刷新。
- 依据包括[DJI Pocket4中国快速攻略](https://repair.dji.com/help/content?customId=01700043653&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[Pocket4英文手册](https://dl.djicdn.com/downloads/DJI_Osmo_Pocket_4/UM/v1.0/Osmo_Pocket_4_User_Manual_en.pdf)、[Pocket4瑞士英文FAQ](https://www.dji.com/ch/osmo-pocket-4/faq)、[Pocket4德国产品概览](https://www.dji.com/de/osmo-pocket-4)、[Pocket4P中国快速攻略](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)、[Pocket4P英国商品FAQ](https://store.dji.com/uk/product/osmo-pocket-4p-vlog-combo?set_region=GB&vid=241311)、[官方LUT表](https://repair.dji.com/help/content?customId=01700007105&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)及[官方连接提示](https://repair.dji.com/help/content?customId=01700009275&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)。本轮是官方文本核验，没有样张、声音或实机测量。
- Pocket4P胶片影调慢动作范围、续航手柄增时两条原有冲突仍为`pending`，不进入卖点肯定依据。Pocket4 FAQ自身的慢动作影调表述也未在本轮解决，普通视频美肤卡不依赖该争议。
- 17挡与Pocket4P广角1× D-Log 2绑定；4K高帧率按慢动作与镜头分别理解；三轴增稳、锁焦和云台跟随是不同功能。机内美肤、App美颜、Log还原与成片风格分别处理。
- 地区页没有可比较固件时，保留CN/GB/CH/DE来源范围，不宣称同一地区或任何固件已经统一。现有P4P-020的CN图证据仍保留2026-09-06，本轮只重核其GB按键子依据。
- 不把品类能力写成独家，不默认Pocket4P全面优于Pocket4；中焦、后期余地、多人取景和遥控是否有价值，取决于真实任务。

## 维护

新增卖点先补完整型号事实与官方出处，再解释使用价值。`checked_at`只更新实际核读过的依据；保留未覆盖项和失败访问。数量不设填充目标，同一能力只有需要、动作或取舍存在实质差异才另建卡。知识库更新后由主入口显式刷新个人快照；本层不承诺后台同步，不触发社媒采集或评论生产。
