# 官方证据读取说明｜2026-09-06

本轮知识来自当日实际打开的 DJI 原页与官方 PDF，不将旧注册表作为核验来源。事实正文为中文改述；`source_refs.quote` 与 `official.excerpt` 保留最短定位锚点，结合章节/PDF页码回查，避免复制整篇官方内容。锚点出现只能证明定位一致，不能由程序独立证明整句改述正确。

## 使用范围

- Pocket4、Pocket4P 为重点主库；初代、Pocket2、Pocket3 已读材料只保留代际对照。
- `verified` 表示此次已在来源对应位置读到该原子事实，不等于原帖使用了该功能，也不保证后续永不变化。
- 共享培训复核当前官网并登记`product`来源、绑定`product_fact`断言；仅LH13专项要求映射claim注册表，不能将该门槛套到一般共享培训。
- 来源记录 `checked_at` 是本次阅读日期，不是产品发布日期、固件版本日期或用户已更新日期。
- 手册只做文本阅读，未将未看过的嵌入图片、演示视频或图中动作当作证据。

## 已发现的来源差异与限制

1. **4P手柄续航数字冲突**：`DJI-P4P-GUIDE` 的3.5.5与第05节分别出现约150和约130分钟，后者列出测试条件。`PKF-P4P-015` 为 pending；暂不推荐引用增时数字。[原页](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)
2. **内存不能跨型号代入**：本轮成功读取的 Pocket4 快速攻略与4P攻略给出的可用容量不同，各自登记，未复制历史共享claim推断同容量。[Pocket4原页](https://repair.dji.com/help/content?customId=01700043653&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)
3. **Pocket2手册标记**：当日官方downloads HTML提供的中文PDF带 `Not final`。仅保存来源发现，不以它独立支撑verified断言；Pocket2已入库事实来自FAQ和专项支持文。[该PDF](https://dl.djicdn.com/downloads/DJI_Pocket_2/20210312UM/DJI_Pocket_2_User_Manual_v1.2_CHS.pdf)
4. **主站读取不足**：4/4P部分主站产品、商城、支持和下载地址报错、返回空页或跳通用支持首页。未以搜索结果摘要补全原页参数。4P的完整手册和固件说明仍缺。
5. **版本不能省略**：已读初代、Pocket3、Pocket4历史固件文件；不把它们称作当日最新固件。未经复核的固件后续变化另列缺口。
6. **操作类别区分**：对焦专项文已明确人脸追焦不带动云台，基础智能跟随才会带动；不同模式可用性按该文对应型号小节分别记录。[原页](https://repair.dji.com/help/content?customId=01700009262&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)

## 交给后续维护的重点

先补4P手册/固件/模式组合、4与4P最新麦克风兼容表及低光/色彩/倍率限制，再根据真实写作检索缺口补单项。数值存在冲突时记录冲突而不多数表决。产品事实用官方核验；主观体验和人群口吻用真实语料；原帖画面归因仍需原帖的操作/设置/结果证据。

## 2026-09-06 同日补核：主库具体操作

当前129条事实（127 verified、2 pending），24个来源；其中82条唯一事实适用于主库4/4P。跨型号共同记录在各型号统计中重复计入，不能把型号计数相加当唯一事实数。

新增实际打开来源：

- `DJI-P4P-STORE-GB`：[英国官方商店 FAQ](https://store.dji.com/uk/product/osmo-pocket-4p-vlog-combo?set_region=GB&vid=241311)。读取产品FAQ、镜头/实体键/色彩/模式/FrameTap及尾部脚注；未读演示视频。所有来源新增region/locale，相关事实保留地区与未声明固件条件。
- `DJI-S-LUT`：[Log与LUT型号表](https://repair.dji.com/help/content?customId=01700007105&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)。只核对4/4P行，未下载或测试LUT。
- `DJI-S-VERTICAL`：[竖拍操作](https://repair.dji.com/help/content?customId=01700007470&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)。读取Pocket系列条目；没有从OM等其他产品的FrameTap操作补推4P。
- `DJI-S-WEBCAM`：[网络摄像头指引](https://repair.dji.com/help/content?customId=zh-cn03400006962&lang=zh-CN&re=CN&spaceId=34)。采用明确点名4/4P的FrameTap、USB与Mic2条目；页面早段泛称1080P，后段明确列4系列支持更高分辨率。未以泛称覆盖各型号，也未据“其他机型”推断4P所有限制。

新增待核冲突：`PKF-P4P-007`。中国攻略胶片影调支持视频和慢动作，英国商店说仅Video；两页没有可比较固件条件。`pending`表示这个通用可用范围不能投放到写作事实包，不意味已经证明其中一页错误。App美颜与机内美肤是不同功能，不能混成同一个冲突。

仍未完成的检索：菲律宾4P支持页搜索结果显示音频备份细则，但实际web open及HTTP打开跳到通用支持页；英国支持页同样跳转。因此没有把搜索文本做成verified音频备份、四声道或FrameTap实体键事实，也没有把那个失败入口登记为已读官方正文来源。4P完整手册/固件历史、各镜头完整低光/帧率/色彩矩阵、传输峰值条件及FrameTap升级步骤继续列缺口。

短摘使用说明：official.jsonl的excerpt为逐条quote去重后的原句短词定位合集；summary_anchor另存阅读范围概述。短词命中只验证引用存在，语义必须回到locator所指的完整问答/章节检查；这不是完整网页存档。

## 4P机身操作补核

实际读取中国攻略3.1实体按键与拍摄界面两张静态图，并按正文2.2/2.3/3.2/3.6核对步骤边界。新增PKF-P4P-031至038，020/021补CN图依据；图文件、官方CDN原地址及SHA-256见DJI-P4P-GUIDE的image_evidence。未读视频不算已读，其他型号段落不移用于4P。4P音频备份、录制中切模式及水印个案仍无完整依据。
