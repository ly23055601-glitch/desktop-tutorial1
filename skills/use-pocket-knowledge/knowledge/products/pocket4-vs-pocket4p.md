# Pocket4 与 Pocket4P：按拍摄环节查差异

主体依据2026-09-06已核事实整理，2026-09-07补充卖点与操作入口；当前卖点与来源差异见[卖点指南](../selling_points/guide.md)。这是提问和检索入口，不作购买排名。每个事实ID链接回完整卡片，使用时连同`conditions`、`not_infer`和原始官方位置读取；缺少证据表示本库待核，不表示设备不支持。

下文“中国”指CN/zh-CN来源；“英国”指GB/en-GB来源。英国FAQ未标可比较的固件版本，涉及模式组合时须核对目标地区与本机版本。各节“编辑推想”仅给出可以进一步问的问题，没有借用真实用户经历，也不是人群共识。完整未闭合问题见[主题覆盖表](topic-coverage.md)。

## 1. 构图前：需要哪个焦段，按键会切到哪里？

| 型号 | 已核入口与关键条件 |
|---|---|
| Pocket4 | [PKF-P4-007](facts.jsonl:53)：变焦键单击到2x、双击到4x，再按可回1x；**4x仅部分模式可用**。这张卡不证明存在4P的20mm/60mm双摄。[4英文手册](https://dl.djicdn.com/downloads/DJI_Osmo_Pocket_4/UM/v1.0/Osmo_Pocket_4_User_Manual_en.pdf)，印刷p18。 |
| Pocket4P | [PKF-P4P-001](facts.jsonl:62)、[PKF-P4P-002](facts.jsonl:63)、[PKF-P4P-020](facts.jsonl:96)：20mm广角与60mm中焦两颗镜头，每次只一颗工作；单击结果先看当前倍率，双击6x、长按匀速放大。不能理解为两路同时录制或连续光学变焦。[4P中国攻略](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)，3.1图/第05节；单击1x→3x、其他倍率→1x的明确措辞另见[4P英国FAQ](https://store.dji.com/uk/product/osmo-pocket-4p-vlog-combo?set_region=GB&vid=241311)。 |

4P的12x排除照片、低光、慢动作、延时，是**英国来源的限定**，且不补推各模式最大倍率（[PKF-P4P-024](facts.jsonl:100)）。两款录制中切倍率的完整分辨率/帧率/色彩矩阵仍待核。

**编辑推想：**当前要保留环境还是拍紧一些；是否站得足够近；这段采用什么模式，是否已经开始录制。先确认这些，才有条件谈镜头选择。

## 2. 架好机位：怎样选中人、启动和退出跟随？

| 型号 | 已核入口与关键条件 |
|---|---|
| Pocket4 | [PKF-P4-016](facts.jsonl:90)、[PKF-P4-008](facts.jsonl:54)：手势控制须先开启；官方建议2米以内、避免挡住头部，以屏幕识别提示为准。全景、静止/轨迹延时、旋转运镜及横持FPV不支持跟随。[4英文手册](https://dl.djicdn.com/downloads/DJI_Osmo_Pocket_4/UM/v1.0/Osmo_Pocket_4_User_Manual_en.pdf)，印刷p22/p26–27。现补[PKF-P4-022](facts.jsonl)：屏幕双击目标启动，点框外或单击摇杆退出；按该事实模式条件使用。 |
| Pocket4P | [PKF-P4P-033](facts.jsonl:113)、[PKF-P4P-005](facts.jsonl:66)：拍摄画面双击选智能跟随对象，摇杆单击可退出；单击也可能是返回菜单，要看当前界面。开启手势控制后，手掌启停跟随，V手势触发3秒倒计时照片或启停录像；不保证所有距离都识别。[4P中国攻略](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)，3.1图/3.4.4。 |

两款都要区分**焦点锁在人脸**与**云台带镜头转动**（[PKF-S-010](facts.jsonl:86)；[中国对焦指引](https://repair.dji.com/help/content?customId=01700009262&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)）。4P模式排除项另查[PKF-P4P-028](facts.jsonl:104)的[4P英国FAQ](https://store.dji.com/uk/product/osmo-pocket-4p-vlog-combo?set_region=GB&vid=241311)，不要拿4的2米建议充当4P范围。

**编辑推想：**人离开屏幕后由谁确认取景；想锁焦还是让镜头跟着转；怎样结束这一段。尚无证据时，不替原帖认定用了跟随或一定不会丢失目标。

## 3. 开拍说话：连哪只麦，是否还要单独留一份声音？

| 型号 | 已核入口与关键条件 |
|---|---|
| Pocket4 | [PKF-P4-004](facts.jsonl:50)、[PKF-P4-009](facts.jsonl:55)：可同时连接两台兼容DJI发射器，型号须复核支持列表。开启音频备份后，外部无线麦录像同时用内置麦录音，可存独立AAC或附加音轨；**延时、Webcam、DisplayPort传输不支持该备份**。[4中国攻略](https://repair.dji.com/help/content?customId=01700043653&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)，3.5.1；[4英文手册](https://dl.djicdn.com/downloads/DJI_Osmo_Pocket_4/UM/v1.0/Osmo_Pocket_4_User_Manual_en.pdf)，印刷p22。 |
| Pocket4P | [PKF-P4P-009](facts.jsonl:70)：最多两台所列兼容发射器直连，无需接收器；下拉菜单→系统设置→无线麦克风按提示对频，顶部音量条用于确认连接。具体麦型和固件须核对；成功配对后可自动重连。[4P中国攻略](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)，3.5.1。**4P相机音频备份格式、声道和禁用模式仍待核**。 |

**编辑推想：**是一人还是两人讲话；现有发射器是哪款；需要的是相机备份还是发射器自身内录。连接成功不能证明两种备份都开着，也不能把4的备份规则移给4P。

## 4. 拍人和后期：准备直出，还是自己还原、调色？

| 型号 | 已核入口与关键条件 |
|---|---|
| Pocket4 | [PKF-P4-003](facts.jsonl:49)、[PKF-S-014](facts.jsonl:106)：美肤与胶片影调不能同时开启；官方提供4视频D-Log对应的Rec.709 LUT，表中未列照片D-Log，本轮未下载测试LUT。[4中国攻略](https://repair.dji.com/help/content?customId=01700043653&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)，3.4.3；[中国LUT指引](https://repair.dji.com/help/content?customId=01700007105&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)。4的完整Log规格和软件导出步骤仍待核。 |
| Pocket4P | [PKF-P4P-008](facts.jsonl:69)、[PKF-P4P-018](facts.jsonl:94)、[PKF-S-015](facts.jsonl:107)：美肤与胶片影调互斥；左滑图像/音频菜单可设D-Log 2。官方为D-Log与D-Log 2分别提供LUT，须按实际Log类型匹配，不能保证自动变成某位作者的效果。[4P中国攻略](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)，3.2.3/3.4.5；[中国LUT指引](https://repair.dji.com/help/content?customId=01700007105&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)。 |

4P的10-bit D-Log 2仅1x这一限制来自[PKF-P4P-022](facts.jsonl:98)的[4P英国FAQ](https://store.dji.com/uk/product/osmo-pocket-4p-vlog-combo?set_region=GB&vid=241311)，不能套到3x中焦或忽略目标固件。胶片影调是否支持慢动作存在CN/GB冲突（[PKF-P4P-007](facts.jsonl:68)，`pending`），不能写成已解决的通用能力。

**编辑推想：**拍摄后愿意留多少时间处理；素材到底用了哪种色彩模式；想调整肤色、整片风格还是还原Log。不能只凭成片观感倒推作者的设置或后期意愿。

## 5. 拍完传手机：连线、无线、电脑和遥控器怎样安排？

| 型号 | 已核入口与关键条件 |
|---|---|
| Pocket4 | [PKF-P4-010](facts.jsonl:56)、[PKF-P4-011](facts.jsonl:57)：手机可经Mimo相册下载或有线传输；开机连接电脑并选择文件传输后，不能同时拍照录像。连接可用不等于手机能编辑所有素材格式。[4英文手册](https://dl.djicdn.com/downloads/DJI_Osmo_Pocket_4/UM/v1.0/Osmo_Pocket_4_User_Manual_en.pdf)，印刷p29–30。 |
| Pocket4P | [PKF-P4P-038](facts.jsonl:118)、[PKF-P4P-014](facts.jsonl:75)：已核拍后手机/电脑导出路径，电脑有USB 3.1数据线方式；连接Mimo前先关FrameTap，两者不能同时连接。Wi-Fi原句未给出电脑直接无线接收步骤，峰值速率也不是保证值。[4P中国攻略](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)，3.6.3；[中国连接排查](https://repair.dji.com/help/content?customId=01700009275&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)，提示3。 |

两款手机OTG都须先确认支持情况、数据线及接口，再在机身选择OTG；Android、iPhone15 USB-C和需供电的Lightning方案不能混写（[PKF-S-005](facts.jsonl:81)；[中国OTG指引](https://repair.dji.com/help/content?customId=zh-cn03400007307&lang=zh-CN&re=CN&spaceId=34)）。4P传输中能否拍摄、完整手机剪辑和部分素材加水印的条件仍待核。

**编辑推想：**素材最终到哪台设备；是看回放、保存原片还是剪辑；当前FrameTap是否仍连接。先拆开这几个动作，再定位“传不了”的具体一步。

## 6. 结束拍摄：哪些配件要先取下，下次如何取用？

| 型号 | 已核入口与关键条件 |
|---|---|
| Pocket4 | [PKF-P4-001](facts.jsonl:47)：下次取用时先取下云台夹，再顺时针旋屏或短按拍摄键开机。[4中国攻略](https://repair.dji.com/help/content?customId=01700043653&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)，2.2。**4关机时补光灯/增广镜拆卸顺序、保护件完整安装步骤仍待核**，不能直接抄4P流程。 |
| Pocket4P | [PKF-P4P-013](facts.jsonl:74)、[PKF-P4P-031](facts.jsonl:111)：先取下补光灯和增广镜，再关闭相机；正文把长按拍摄键或逆时针旋屏关机限定在非拍摄状态。[4P中国攻略](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)，2.2/3.7。保护夹、包袋的完整安装和长期存放要求仍待核。 |

**编辑推想：**这次装了哪些配件；是在暂停拍摄还是准备装包；下次取出前需要恢复哪些步骤。不能把“随身携带”扩写成所有配件装着都能随手关机入袋。

---

后续写作先回到当前帖子证据。上述编辑问题只能帮助选择材料，不证明真实作者的设备、经历、动机或需求。共享培训产品断言按`product/product_fact`链复核；LH13专项另遵守claim登记要求。
