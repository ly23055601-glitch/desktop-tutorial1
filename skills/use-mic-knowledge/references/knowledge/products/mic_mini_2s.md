# DJI Mic Mini 2S 产品知识入口

核验日期：2026-09-06。大陆中文官方资料为主，规范型号 ID 为 `mic_mini_2s`。结构化记录保存在 [产品事实](mic_mini_2s.facts.jsonl)、[连接兼容](../compatibility/mic_mini_2s.jsonl)、[来源登记](../sources/mic_mini_2s.jsonl)。本文只提供阅读路径，事实维护以 JSONL 为准。

**先区分部件。** Mini 2S 标准接收器 DMMR03 可四发连接，DJI Mic 系列手机版接收器 DMMR02 最多两发。发射器的 32-bit 浮点内录、接收器声道输出和机身最终录音格式必须分别核对。Mic Mini 2S 充电盒 DMMC03 支持导出，手机版套装使用的 Mic Mini 2 小充电盒 DMMCS2 不支持导出（M2S-F001、F007、F012、F014、F028）。

## 主题覆盖

| 主题 | 主要事实编号 | 阅读重点 |
|---|---|---|
| 型号与组件 | M2S-F001 | 标准/手机版接收器和两种盒型 |
| 佩戴 | M2S-F002、F003 | 12克口径、磁吸固定、防风毛套 |
| 音频处理 | M2S-F004-F006、F029 | 低切、降噪、音色、自动增益与监听 |
| 内录 | M2S-F007-F010 | 位深、存储、独立录音、文件类型与循环覆盖 |
| 声道 | M2S-F011-F013、F028 | 四发、分轨、安全轨与手机版两发上限 |
| 传输 | M2S-F016 | 400/300/200米分别对应的链路和测试条件 |
| 续航与供电 | M2S-F017、F018、F030 | 单次与累计续航、功能开关、外部供电断音 |
| 连接兼容 | M2S-F019-F021、F031、F032、F034 | 手机、相机、电脑、OsmoAudio和配件 |
| 操作控制 | M2S-F008、F022、F023 | 内录、配对、拨轮、多人同时开录 |
| 文件导出 | M2S-F014、F015 | 两条电脑导出路径及密码限制 |
| 固件 | M2S-F024、F025、F033 | Mimo升级路径与已读取版本 |
| 套装 | M2S-F026、F027 | 大陆标准一拖二、一拖一、手机版一拖一 |

## 六类使用任务

以下是编辑导航，不是真实用户体验或评论草稿。

- **手机口播：** 先核手机接口和App，选标准接收器连接头或手机版接收器；蓝牙直连只接一个TX，不能直接假定原生相机收音。见 M2S-F019、F020、F027-F030；兼容 M2S-C012、C021-C024、C033。
- **相机拍摄：** 标准RX可走3.5毫米模拟音频或适配的索尼数字热靴。手机版RX没有3.5毫米相机链路。见 M2S-F021、F031；兼容 M2S-C013-C017。
- **双人采访：** 按需要选择左右独立或混合输出，确认宿主能接收双声道；安全音轨是合并输入的备份，不是第二个人单独的轨。见 M2S-F011、F013、F028。
- **多人录制：** 四人需标准RX与足量TX。四独立轨须核输出接口、软件/相机；3.5毫米仍合为左右两路。见 M2S-F011、F012、F023；兼容 M2S-C001-C003、C015、C018-C020。
- **户外收音：** 佩戴防脱、安装毛套，按现场选处理；标称传输距离来自无遮挡无干扰测试。开启内录/降噪后不能沿用关闭功能的续航测试。见 M2S-F002-F006、F016、F017。
- **录音备份：** 独立内录需确认红色录音状态灯；区分24-bit/32-bit的存储时长、实际续航和原文件/处理文件，完成导出再处理旧文件。见 M2S-F007-F010、F014、F015、F023。

## 已知缺口与来源差异

`pending` 和 `conflict` 不进入默认确定答案；下列项目保持可检索，供使用前核对。

- **M2S-F035 / pending：** 当前官方手机、热靴及第三方App表没有逐项给出系统、App和最低固件版本；未列型号与某手机是否支持双声道仍须逐机核对。 三份名单缺少版本条件与逐手机声道能力，无法形成这些组合的确定结论。
- **M2S-F036 / pending：** FAQ将自动增益调节默认状态写为关闭，2026-07-02 V30.00.03.00发布记录称防爆音功能默认开启；两者术语及版本适用范围尚未完全对应。 防爆音可能指自动增益中的模式或独立处理功能，不能仅凭默认值不同定性冲突；需结合固件实际界面核对。
- **M2S-F037 / conflict：** 清配对长按时长未统一：手册v1.0第11页写10秒，FAQ写12秒。 相同操作在两份官方资料中时长不同，尚无明确修订解释。
- **M2S-F038 / conflict：** 标准接收器充满电时间存在口径差异：参数页及FAQ给约70分钟，新手攻略给约100分钟。 官方来源没有明确解释70/100分钟是否来自不同充电条件；待逐路径确认。
- **M2S-F039 / conflict：** 商城“四声道输出”段将3.5毫米线也列入四路独立输出；FAQ明确3.5毫米仍为双声道，商城脚注12亦限定数字热靴或USB。 同一商城正文与脚注及FAQ不一致，保留冲突并限制3.5毫米的四轨宣传。
- **M2S-F040 / pending：** 四声道软件兼容表列有iOS GarageBand，但具体iOS设备、接口及软件版本待核。资料覆盖详略不同不构成直接矛盾，完整接法尚待补充。

另有 M2S-C017 未列相机四声道、M2S-C020 iOS GarageBand 链路、M2S-C033 具体手机声道的待核记录。官方热靴兼容表只列相机名称，不能把每个名称自动升级为已确认四声道；OsmoAudio表按功能列出支持状态，未给最低固件版本。

## 官方资料与复核方法

所有 PDF 链接从官方 Mini 2S FAQ 页面内嵌资料列表取得；独立 `/downloads` 页面本次只返回标题，未将空页面当作已读手册。中文FAQ与参数页通过直接读取官方HTML获取，浏览检索工具的地区重定向结果没有被冒充大陆来源。

- **M2S-S001** [DJI Mic Mini 2S 常见问题](https://www.dji.com/cn/mic-mini-2s/faq)。正文全部问题；通过官方中文 HTML 读取，另保留 HTML；下载链接来自该页内嵌官方资料数据。
- **M2S-S002** [DJI Mic Mini 2S 技术参数](https://www.dji.com/cn/mic-mini-2s/specs)。各部件和通用参数表、续航与传输脚注。
- **M2S-S003** [DJI Mic Mini 2S 用户手册](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/UM/DJI_MICMINI2S_um_zh-cn.pdf)。PDF 第1-21页；重点第5-19页操作说明。
- **M2S-S004** [DJI Mic Mini 2S 发布记录](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/RN/DJI_MIC_MINI_2S_RN_20260702_CHS.pdf)。PDF 第1页，已渲染核对中文正文。
- **M2S-S005** [大疆商城 DJI Mic Mini 2S（一拖二，含充电盒）](https://store.dji.com/cn/product/dji-mic-mini-2s)。大陆套装选择、包装清单、功能段落及脚注1-16。
- **M2S-S006** [DJI Mic 系列手机版接收器混连兼容列表](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/COMPATIBILITY/DJI_Mic_Series_MobileRX_Cross_Model_Compatibility_List_CHS4_final.pdf)。PDF 第1页全部表格，已渲染核对绿灯/蓝灯模式和最多两发射器表头。
- **M2S-S007** [DJI Mic Mini 2S OsmoAudio 兼容列表](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/COMPATIBILITY/DJI_MIC_MINI_2S_OsmoAudio_Compatibility_List_CHS_final.pdf)。PDF 第1页全部功能行与八款设备列，已渲染核对。
- **M2S-S008** [DJI Mic Mini 2S 四声道兼容列表](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/COMPATIBILITY/DJI_Mic_Mini_2s_Quadraphonic_Computer_Software_Compatibility_List_CHS_final.pdf)。PDF 第1页所有系统/软件行，已渲染核对。
- **M2S-S009** [DJI Mic 系列热靴转接件相机兼容列表](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/COMPATIBILITY/DJI_Mic_Series_Camera_Adapter_Compatibility_List_CHS_final.pdf)。PDF 第1页全部19款相机行，已渲染核对。
- **M2S-S010** [DJI Mic 系列第三方 App 兼容列表](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/COMPATIBILITY/DJI_Mic_Series_ThirdParty_App_Compatibility_List_CHS_final.pdf)。PDF 第1页完整表头、功能列和iOS/Android各行，已渲染核对。
- **M2S-S011** [DJI Mic 系列手机兼容列表](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/mic-mini-2s/20260702/COMPATIBILITY/DJI_MIC_Series_Mobile_Phone_Compatibility_List_CHS_final.pdf)。PDF 第1-2页完整型号表，已渲染核对。
- **M2S-S012** [DJI Mic Mini 2S 新手快速攻略](https://repair.dji.com/help/content?customId=01700043679&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)。正文01-05文字段；未将嵌入视频或开箱图当作已读证据。
- **M2S-S013** [大疆商城 DJI Mic Mini 2S（一拖一）](https://store.dji.com/cn/product/dji-mic-mini-2s-tx-rx?from=site-nav&set_region=CN&vid=241761)。大陆套装名称、包装清单及功能脚注。
- **M2S-S014** [大疆商城 DJI Mic Mini 2S（手机版一拖一，含充电盒）](https://store.dji.com/cn/product/dji-mic-mini-2s-1tx-1-mobile-1rx-charging-case)。大陆套装名称与包装清单。

手册为 v1.0 / 2026.07；已读取的发布记录为 2026-07-02、V30.00.03.00。其余兼容表正文未标明确文档版本；URL目录日期仅用作来源路径，不能替代发布日期。

维护时先复核被引用的当前官方页和文档版本，再更新单条记录的来源、条件、限制与实际读取日；旧的来源差异不应因检索命中或自动审计通过而消失。不得向本库写入训练人物、购买经历或假想消费者反馈。
