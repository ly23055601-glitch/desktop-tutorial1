# Mic 知识库缺口与冲突

生成时间：2026-09-06T18:05:14+08:00。由 `scripts/build_reports.py` 按当前记录生成；生成时间不改变事实核验日期。

下面的条目不能作为肯定产品能力。明确不支持的已核验兼容记录不算缺口。

## MIC3-F039 · DJI Mic 3

状态：pending

热靴兼容名单中的各相机是否均可四声道录制，当前不能逐机确认。

待核原因：最新已读热靴表不含各机型声道数/固件列；需继续查具体相机官方手册。
- [DJI Mic 系列热靴转接件相机兼容列表](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/COMPATIBILITY/DJI_Mic_Series_Camera_Adapter_Compatibility_List_CHS_final.pdf)：PDF第1页：仅序号与相机型号两列（中国大陆；核验 2026-09-06）
- [DJI Mic 3 常见问题](https://www.dji.com/cn/mic-3/faq)：如何使用四声道模式？音频怎么分配？（中国大陆；核验 2026-09-06）

## MIC3-F040 · DJI Mic 3

状态：pending

通用手机名单未给每款手机的系统、App、接口和声道测试组合，不能逐项确认任意组合。

待核原因：手机表只有品牌型号，尚缺逐机系统版本与测试链路。
- [DJI Mic 系列手机兼容列表](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/COMPATIBILITY/DJI_MIC_Series_Mobile_Phone_Compatibility_List_CHS_final.pdf)：PDF第1—2页：品牌/型号表（中国大陆；核验 2026-09-06）
- [DJI Mic 系列第三方APP兼容列表](https://dl.djicdn.com/downloads/MIC_MINI_2/20260421/compatibility/DJI_Mic_Series_ThirdParty_App_Compatibility_List_CHS.pdf)：PDF第1页：蓝牙直连第三方App表（中国大陆；核验 2026-09-06）

## M2S-F035 · DJI Mic Mini 2S

状态：pending

当前官方手机、热靴及第三方App表没有逐项给出系统、App和最低固件版本；未列型号与某手机是否支持双声道仍须逐机核对。

待核原因：三份名单缺少版本条件与逐手机声道能力，无法形成这些组合的确定结论。
- [DJI Mic 系列手机兼容列表](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/COMPATIBILITY/DJI_MIC_Series_Mobile_Phone_Compatibility_List_CHS_final.pdf)：第1-2页表头与型号列（CN；核验 2026-09-06）
- [DJI Mic 系列热靴转接件相机兼容列表](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/COMPATIBILITY/DJI_Mic_Series_Camera_Adapter_Compatibility_List_CHS_final.pdf)：第1页表头与相机列（CN；核验 2026-09-06）
- [DJI Mic 系列第三方 App 兼容列表](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/COMPATIBILITY/DJI_Mic_Series_ThirdParty_App_Compatibility_List_CHS_final.pdf)：第1页表头（CN；核验 2026-09-06）

## M2S-F036 · DJI Mic Mini 2S

状态：pending

FAQ将自动增益调节默认状态写为关闭，2026-07-02 V30.00.03.00发布记录称防爆音功能默认开启；两者术语及版本适用范围尚未完全对应。

待核原因：防爆音可能指自动增益中的模式或独立处理功能，不能仅凭默认值不同定性冲突；需结合固件实际界面核对。
- [DJI Mic Mini 2S 常见问题](https://www.dji.com/cn/mic-mini-2s/faq)：“自动增益调节如何选择？”（CN；核验 2026-09-06）
- [DJI Mic Mini 2S 发布记录](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/RN/DJI_MIC_MINI_2S_RN_20260702_CHS.pdf)：第1页 本次更新（CN；核验 2026-09-06）

## M2S-F037 · DJI Mic Mini 2S

状态：conflict

清配对长按时长未统一：手册v1.0第11页写10秒，FAQ写12秒。

待核原因：相同操作在两份官方资料中时长不同，尚无明确修订解释。
- [DJI Mic Mini 2S 用户手册](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/UM/DJI_MICMINI2S_um_zh-cn.pdf)：第11页 清除设备配对信息（CN；核验 2026-09-06）
- [DJI Mic Mini 2S 常见问题](https://www.dji.com/cn/mic-mini-2s/faq)：“发射器如何与接收器、手机版接收器对频？” 方法二（CN；核验 2026-09-06）

## M2S-F038 · DJI Mic Mini 2S

状态：conflict

标准接收器充满电时间存在口径差异：参数页及FAQ给约70分钟，新手攻略给约100分钟。

待核原因：官方来源没有明确解释70/100分钟是否来自不同充电条件；待逐路径确认。
- [DJI Mic Mini 2S 技术参数](https://www.dji.com/cn/mic-mini-2s/specs)：接收器/充电时间（CN；核验 2026-09-06）
- [DJI Mic Mini 2S 常见问题](https://www.dji.com/cn/mic-mini-2s/faq)：“充电盒给发射器、接收器充满电分别需要多长时间？”（CN；核验 2026-09-06）
- [DJI Mic Mini 2S 新手快速攻略](https://repair.dji.com/help/content?customId=01700043679&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)：2.2 设备充电 提示（CN；核验 2026-09-06）

## M2S-F039 · DJI Mic Mini 2S

状态：conflict

商城“四声道输出”段将3.5毫米线也列入四路独立输出；FAQ明确3.5毫米仍为双声道，商城脚注12亦限定数字热靴或USB。

待核原因：同一商城正文与脚注及FAQ不一致，保留冲突并限制3.5毫米的四轨宣传。
- [大疆商城 DJI Mic Mini 2S（一拖二，含充电盒）](https://store.dji.com/cn/product/dji-mic-mini-2s)：“四声道输出，剪辑自如”段及脚注12（CN；核验 2026-09-06）
- [DJI Mic Mini 2S 常见问题](https://www.dji.com/cn/mic-mini-2s/faq)：“如何使用四声道模式？音频怎么分配？”（CN；核验 2026-09-06）
- [DJI Mic Mini 2S 用户手册](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/UM/DJI_MICMINI2S_um_zh-cn.pdf)：第13页四声道条件（CN；核验 2026-09-06）

## M2S-F040 · DJI Mic Mini 2S

状态：pending

四声道软件兼容表列有iOS GarageBand，但FAQ及商城脚注未给出具体iOS设备和接法，实际链路待核。

待核原因：资料覆盖范围不同不构成直接矛盾；需要iOS硬件、接口、系统及软件版本条件，才能确认完整连接方案。
- [DJI Mic Mini 2S 四声道兼容列表](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/COMPATIBILITY/DJI_Mic_Mini_2s_Quadraphonic_Computer_Software_Compatibility_List_CHS_final.pdf)：第1页 iOS/GarageBand 行（CN；核验 2026-09-06）
- [DJI Mic Mini 2S 常见问题](https://www.dji.com/cn/mic-mini-2s/faq)：“如何使用四声道模式？音频怎么分配？”（CN；核验 2026-09-06）
- [大疆商城 DJI Mic Mini 2S（一拖二，含充电盒）](https://store.dji.com/cn/product/dji-mic-mini-2s)：脚注12（CN；核验 2026-09-06）

## BASIC-C023 · DJI Mic Mini 2／DJI Mic 3

状态：conflict

Mini 2 FAQ 说两款 Mini 2 充电盒可收纳并充电 Mic 3 发射器，但配件总表对应 Mic 3 列标为不通用。

待核原因：FAQ 明确允许仅收纳及充电，而配件总表只给通用性否定标记；需核对通用性定义或官方更正。
- [DJI Mic Mini 2 常见问题](https://www.dji.com/cn/mic-mini-2/faq)：DJI Mic Mini 2 充电盒有什么功能？（中国大陆；核验 2026-09-06）
- [DJI Mic 系列配件通用性](https://repair.dji.com/help/content?customId=01700009935&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)：配件通用性表／行：DJI Mic Mini 2 充电盒、DJI Mic Mini 2 充电盒（手机版一发一收）／列：DJI Mic 3（中国大陆；核验 2026-09-06）

## BASIC-C024 · DJI Mic Mini／DJI Mic Mini 2

状态：conflict

Mini 2 FAQ 泛称与 Mini 发射器／接收器兼容，但配件总表 Mini 发射器对 Mini 2 列为不通用。

待核原因：产品组合列与具体接收器的粒度不同，且官方表述不一致；保留上下文，等待用途细化。
- [DJI Mic Mini 2 常见问题](https://www.dji.com/cn/mic-mini-2/faq)：DJI Mic Mini 2 的发射器和接收器是否兼容 DJI Mic、DJI Mic 2 、DJI Mic 3、DJI Mic Mini 的发射器和接收器？（中国大陆；核验 2026-09-06）
- [DJI Mic 系列配件通用性](https://repair.dji.com/help/content?customId=01700009935&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)：配件通用性表／行：DJI Mic Mini 发射器／列：DJI Mic Mini 2（中国大陆；核验 2026-09-06）

## MIC3-C018 · DJI Mic 3

状态：pending

官方四声道表列iOS GarageBand支持，但当前未确认具体iPhone/iPad和接线条件。

待核原因：四声道表与FAQ对宿主范围详略不同，缺少明确iOS硬件、版本与接法。
- [DJI Mic 3 四声道兼容列表](https://dl.djicdn.com/downloads/DJI%20Mic%203/202508282/DJI_Mic_3_Quadraphonic_Computer_Software_Compatibility_List_&CHS.pdf)：PDF第1页：iOS GarageBand行（中国大陆；核验 2026-09-06）
- [DJI Mic 3 常见问题](https://www.dji.com/cn/mic-3/faq)：如何使用四声道模式？音频怎么分配？（中国大陆；核验 2026-09-06）

## MIC3-C021 · DJI Mic 3

状态：pending

没有具体宿主和连接链路证据时，不判断Mic3是否兼容。

待核原因：未列宿主或未知连接方式不等同明确不支持。
- [DJI Mic 系列热靴转接件相机兼容列表](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/COMPATIBILITY/DJI_Mic_Series_Camera_Adapter_Compatibility_List_CHS_final.pdf)：PDF第1页：有限相机名单（中国大陆；核验 2026-09-06）
- [DJI Mic 系列手机兼容列表](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/COMPATIBILITY/DJI_MIC_Series_Mobile_Phone_Compatibility_List_CHS_final.pdf)：PDF第1—2页：手机名单（中国大陆；核验 2026-09-06）
- [DJI Mic 系列第三方APP兼容列表](https://dl.djicdn.com/downloads/MIC_MINI_2/20260421/compatibility/DJI_Mic_Series_ThirdParty_App_Compatibility_List_CHS.pdf)：PDF第1页：限定蓝牙App表（中国大陆；核验 2026-09-06）

## M2S-C017 · DJI Mic Mini 2S

状态：pending

未列相机的四声道支持状态尚未确认。

待核原因：缺少具体相机及其四声道规格。
- [DJI Mic 系列热靴转接件相机兼容列表](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/COMPATIBILITY/DJI_Mic_Series_Camera_Adapter_Compatibility_List_CHS_final.pdf)：第1页表头和19款型号（CN；核验 2026-09-06）
- [DJI Mic Mini 2S 常见问题](https://www.dji.com/cn/mic-mini-2s/faq)：“如何使用四声道模式？”（CN；核验 2026-09-06）

## M2S-C020 · DJI Mic Mini 2S

状态：pending

四声道软件兼容表列有iOS GarageBand，但FAQ及商城脚注未给出具体iOS设备和接法，实际链路待核。

待核原因：资料覆盖范围不同不构成直接矛盾；需要iOS硬件、接口、系统及软件版本条件，才能确认完整连接方案。
- [DJI Mic Mini 2S 四声道兼容列表](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/COMPATIBILITY/DJI_Mic_Mini_2s_Quadraphonic_Computer_Software_Compatibility_List_CHS_final.pdf)：第1页 iOS/GarageBand行（CN；核验 2026-09-06）
- [DJI Mic Mini 2S 常见问题](https://www.dji.com/cn/mic-mini-2s/faq)：“如何使用四声道模式？音频怎么分配？”（CN；核验 2026-09-06）

## M2S-C033 · DJI Mic Mini 2S

状态：pending

未提供具体手机、系统与App时，不能确认双声道录制与回放能力。

待核原因：缺少确切终端和软件版本，以及逐设备声道依据。
- [DJI Mic 系列手机兼容列表](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/COMPATIBILITY/DJI_MIC_Series_Mobile_Phone_Compatibility_List_CHS_final.pdf)：第1-2页手机型号表（CN；核验 2026-09-06）
- [DJI Mic Mini 2S 常见问题](https://www.dji.com/cn/mic-mini-2s/faq)：“通过手机连接头连接手机时，是否支持双声道模式？”（CN；核验 2026-09-06）

## 首版有意保留的边界

- 手机、App、相机及固件更新可能改变兼容；表外设备保留未确认，不由相近型号推断。
- 型号基础覆盖不等于所有旧款功能的完整手册复刻。
- 不含真实消费者语料、主观听感排行、竞品研究、实时促销或库存。
- 未做本机音频实测；官方可用能力不证明某个原帖启用了该功能。
