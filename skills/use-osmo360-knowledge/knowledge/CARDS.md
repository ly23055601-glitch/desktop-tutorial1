# 知识卡目录

由 `scripts/knowledge.py build` 根据 JSONL 生成。更新应先修改事实卡，再重新生成。已核验只表示在记录日期读取了相应来源。

## Osmo 360（第一代）

### D1-001

**镜头模式与预览｜已按记录日期核验**

360°模式使用两颗镜头；单镜头模式使用一颗。全景模式中拖动屏幕调整视角仅改变预览，不改变记录的球形画面。

- 条件：视角调整仅在支持的拍摄模式可用
- 边界：单镜头与全景不能当作相同素材类型
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-04 · Osmo 360 用户手册 v1.2（2025.09）](https://dl.djicdn.com/downloads/Osmo_360/20250905/Osmo_360_User_Manual_v1.2_zh-cn.pdf)；定位：第12-13页 选择拍摄模式/调整视角

### D1-002

**全景录像｜已按记录日期核验**

普通全景视频规格：8K 7680×3840，24/25/30/48/50fps；6K 6000×3000，24/25/30/48/50/60fps；4K 3840×1920，100fps。

- 条件：8K48/50由V01.01.06.20新增
- 边界：这些是全景记录规格，不是任意平面取景后的原生分辨率
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 固件：8K48/50：V01.01.06.20新增；其他模式以当前界面为准
- 来源：[S-D1-01 · Osmo 360 - Specs](https://www.dji.com/360/specs)；定位：Camera / Panoramic Video
- 来源：[S-D1-05 · DJI Osmo 360 发布记录（2026-02-24）](https://dl.djicdn.com/downloads/Osmo_360/20260224/DJI_Osmo_360_Release_Notes_cn.pdf)；定位：第7页 V01.01.06.20

### D1-003

**单镜头录像｜已按记录日期核验**

单镜头普通视频最高5K/60fps；极广角视频最高4K/120fps。单镜头录像中可不中断切换前后镜头，切换功能限4K/60fps及以下规格。

- 条件：普通5K提供4:3与16:9；极广角4K提供4:3、16:9、9:16；9:16极广角录像由V01.03.08.60新增；单镜头录像中切换前后镜头仅支持4K/60fps及以下规格
- 边界：普通视频与极广角视频是不同模式；录像中切镜头不等于同时录制前后两路；不能外推到5K/60fps或4K/120fps
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-01 · Osmo 360 - Specs](https://www.dji.com/360/specs)；定位：Camera / Single Lens - Video / Boost Video
- 来源：[S-D1-05 · DJI Osmo 360 发布记录（2026-02-24）](https://dl.djicdn.com/downloads/Osmo_360/20260224/DJI_Osmo_360_Release_Notes_cn.pdf)；定位：第2页 V01.03.08.60
- 来源：[S-D1-02 · Osmo 360 - FAQ](https://www.dji.com/360/faq)；定位：Camera / Does Osmo 360 support switching lenses during single-lens recording?

### D1-004

**超级夜景｜已按记录日期核验**

全景超级夜景支持8K/6K的24、25、30fps；单镜头超级夜景为极广角4K或2.7K的25、30fps。

- 条件：单镜头提供4:3、16:9；单镜头超级夜景由V01.02.07.20新增
- 边界：不能将普通全景8K50写成超级夜景8K50
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-01 · Osmo 360 - Specs](https://www.dji.com/360/specs)；定位：Camera / SuperNight
- 来源：[S-D1-05 · DJI Osmo 360 发布记录（2026-02-24）](https://dl.djicdn.com/downloads/Osmo_360/20260224/DJI_Osmo_360_Release_Notes_cn.pdf)；定位：第4页 V01.02.07.20

### D1-005

**照片｜已按记录日期核验**

全景照片最高15520×7760（120MP、2:1）；单镜头照片最高6400×4800（30.72MP、4:3）。

- 边界：120MP指全景照片，不是每个裁切视角的像素数
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-01 · Osmo 360 - Specs](https://www.dji.com/360/specs)；定位：Camera / Max Photo Resolution

### D1-006

**色彩｜已按记录日期核验**

产品支持10-bit与D-Log M；D-Log M素材的饱和度和对比度较低，面向后期调色。

- 条件：使用D-Log M后需要规划色彩处理
- 边界：不以低对比预览判断成片好坏；未核验所有导出路径是否保留10-bit
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-10 · Osmo 360 - All in One](https://www.dji.com/360)；定位：10-bit & D-Log M Color Performance
- 来源：[S-D1-02 · Osmo 360 - FAQ](https://www.dji.com/360/faq)；定位：Camera / What is D-Log M color mode

### D1-007

**拼接距离｜已按记录日期核验**

官方建议相机与主体至少相距0.75米，以改善全景拼接。

- 条件：全景拍摄
- 边界：过近可能出现不自然拼接；不等于超过距离后任何场景都无接缝
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-03 · Osmo 360 新手快速攻略](https://repair.dji.com/help/content?customId=01700043553&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)；定位：3.2 拍摄与回放 / 提示
- 来源：[S-D1-02 · Osmo 360 - FAQ](https://www.dji.com/360/faq)；定位：Camera / safe Stitching Distance

### D1-008

**隐形自拍杆｜已按记录日期核验**

双鱼眼画面拼接可消除相机底部自拍杆；官方建议用隐形自拍杆并让相机与杆保持同一直线。

- 条件：全景模式；安装拧紧、保持正确对齐
- 边界：转接件折角或连接点偏移会影响隐形；单镜头模式不能照搬该效果
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-02 · Osmo 360 - FAQ](https://www.dji.com/360/faq)；定位：Camera / invisible selfie stick
- 来源：[S-D1-04 · Osmo 360 用户手册 v1.2（2025.09）](https://dl.djicdn.com/downloads/Osmo_360/20250905/Osmo_360_User_Manual_v1.2_zh-cn.pdf)；定位：第16页 搭配自拍杆

### D1-009

**硬件｜已按记录日期核验**

参数页列出重量183克；FAQ说明使用两颗1/1.1英寸方形CMOS。

- 边界：营销中的1英寸全景覆盖表述不应改写为两颗1英寸传感器
- 地区：美国/英文官方站；核验：2026-09-07
- 来源：[S-D1-01 · Osmo 360 - Specs](https://www.dji.com/360/specs)；定位：General / Weight; Camera / Sensor
- 来源：[S-D1-02 · Osmo 360 - FAQ](https://www.dji.com/360/faq)；定位：Camera / highlights

### D1-010

**防水与水下成像｜已按记录日期核验**

机身防水规格为IP68、最深10米；官方仍不建议裸机用于水下拍摄，因为折射可能造成畸变及拼接错误。

- 条件：电池仓盖、USB-C盖可靠关闭；避开高水压冲击、温泉及腐蚀性/不明液体
- 边界：防水能力不保证水下全景成像；不建议长期裸机水下使用
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-02 · Osmo 360 - FAQ](https://www.dji.com/360/faq)；定位：Other / Is Osmo 360 waterproof? / underwater precautions

### D1-011

**存储｜已按记录日期核验**

内置128GB存储，其中约105GB可用；支持microSD扩展，最大1TB。

- 条件：使用官方推荐列表中的卡型和容量进行选卡
- 边界：标称容量不等于可用容量；本卡不保证所有同等级第三方卡兼容
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-01 · Osmo 360 - Specs](https://www.dji.com/360/specs)；定位：General / Supported SD Cards; Camera / Built-in Storage Capacity
- 来源：[S-D1-02 · Osmo 360 - FAQ](https://www.dji.com/360/faq)；定位：Camera / Where is the footage saved in Osmo 360?（内置存储或插入的microSD卡）

### D1-012

**文件格式｜已按记录日期核验**

全景视频为OSV，平面视频为MP4（HEVC）；全景视频另有LRF代理文件。

- 边界：LRF代理不等于原始OSV；复制文件不等于已完成平面成片导出
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-02 · Osmo 360 - FAQ](https://www.dji.com/360/faq)；定位：Camera / video formats
- 来源：[S-D1-06 · Osmo 系列产品素材导出指南](https://repair.dji.com/help/content?customId=01700006849&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)；定位：Osmo 360 系列 / 传输到电脑 / Windows 第3项

### D1-013

**续航｜已按记录日期核验**

实验室参考：8K30全景最长100分钟，开长续航模式最长120分钟；6K24且开长续航模式最长190分钟。

- 条件：25℃、熄屏；关闭Wi-Fi、手势控制、语音控制、剪辑助手；120/190分钟需开启长续航模式
- 边界：实验室数据，不保证实际连续录制时长；欧盟和英国的运行温度法规可能导致续航不同
- 地区：英文官方站；明确含欧盟/英国差异；核验：2026-09-07
- 来源：[S-D1-01 · Osmo 360 - Specs](https://www.dji.com/360/specs)；定位：Battery / Operating Time及两条脚注

### D1-014

**温度｜已按记录日期核验**

工作温度范围-20℃至45℃；充电温度范围5℃至40℃。

- 边界：低温可工作不等于允许低温充电
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-01 · Osmo 360 - Specs](https://www.dji.com/360/specs)；定位：Battery / Operating Temperature / Charging Temperature

### D1-015

**外接收音｜已按记录日期核验**

Osmo 360可无线直连最多2个兼容DJI麦克风TX；官方列明Mic 2、Mic Mini、Mic 3、Mic Mini 2、Mic Mini 2S，不支持经RX接入。

- 条件：从相机控制中心的无线麦克风入口配对；Mic 3由V01.02.07.20新增支持
- 边界：不外推不同型号混连或第一代DJI Mic兼容；TX传入Osmo的48kHz/24-bit数据机内处理为48kHz/16-bit保存；不应称视频内录32-bit float
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-08 · DJI Mic 系列可以搭配哪些产品使用、如何使用？](https://repair.dji.com/help/content?customId=zh-cn03400006931&lang=zh-CN&re=CN&spaceId=34)；定位：搭配 Osmo 360 系列
- 来源：[S-D1-07 · DJI Mic 发射器蓝牙连接设备及数量](https://repair.dji.com/help/content?customId=01700009954&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)；定位：正文第1项及提示第2项
- 来源：[S-D1-05 · DJI Osmo 360 发布记录（2026-02-24）](https://dl.djicdn.com/downloads/Osmo_360/20260224/DJI_Osmo_360_Release_Notes_cn.pdf)；定位：第4页 V01.02.07.20

### D1-016

**机身音频备份｜已按记录日期核验**

连接无线麦克风后，可开启机身收音备份，同时把机身麦克风收音保存为单独WAV文件。

- 条件：在控制中心开启机身收音备份
- 边界：备份文件与视频音轨需分别管理
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-04 · Osmo 360 用户手册 v1.2（2025.09）](https://dl.djicdn.com/downloads/Osmo_360/20250905/Osmo_360_User_Manual_v1.2_zh-cn.pdf)；定位：第15页 控制中心 / 无线麦克风 / 机身收音备份

### D1-017

**激活与更新入口｜已按记录日期核验**

首次使用需通过DJI Mimo激活；手机开启Wi-Fi和蓝牙后连接相机并按提示完成；固件升级也由Mimo提示。

- 条件：安装兼容版本DJI Mimo并连接相机
- 边界：本库未代用户激活或更新设备
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-03 · Osmo 360 新手快速攻略](https://repair.dji.com/help/content?customId=01700043553&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)；定位：2.4 激活设备 / 2.5 升级固件

### D1-018

**固件基线｜已按记录日期核验**

本次下载入口提供的发布记录最新条目为2026-02-24、V01.03.08.70，新增智能影调。

- 条件：智能影调需要DJI Mimo V2.7.2或以上；仅全景视频中的部分规格支持，以设备界面为准
- 边界：发布记录日期不等于本地设备版本；不能把该功能扩展到所有模式
- 地区：中国大陆；核验：2026-09-06
- 固件：V01.03.08.70
- 软件：DJI Mimo ≥2.7.2（智能影调）
- 来源：[S-D1-05 · DJI Osmo 360 发布记录（2026-02-24）](https://dl.djicdn.com/downloads/Osmo_360/20260224/DJI_Osmo_360_Release_Notes_cn.pdf)；定位：第1页 V01.03.08.70

### D1-019

**素材传输｜已按记录日期核验**

手机可通过Mimo相册下载；电脑以数据线连接后在相机选文件传输：USB，再复制DCIM/DJI 001中的素材。

- 条件：相机开机；Mac若请求连接配件需允许
- 边界：此流程是素材搬运，不替代取景剪辑
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D1-06 · Osmo 系列产品素材导出指南](https://repair.dji.com/help/content?customId=01700006849&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)；定位：Osmo 360 系列 / 传输到手机 / 传输到电脑

### D1-020

**全景后期｜已按记录日期核验**

全景视频需要经后期编辑，才能作为普通平面视频分享；手册提供手机Mimo和电脑软件两条处理路径。

- 条件：先确定输出全景还是平面视频
- 边界：手册未给出所有手机/电脑的统一导出上限；不得据此承诺任意设备8K导出
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-04 · Osmo 360 用户手册 v1.2（2025.09）](https://dl.djicdn.com/downloads/Osmo_360/20250905/Osmo_360_User_Manual_v1.2_zh-cn.pdf)；定位：第17页 导出与分享 / 编辑全景视频

### D1-021

**DJI Mimo兼容｜已按记录日期核验**

核验时下载页Mimo为v2.11.9，系统门槛为iOS15或Android9及以上，并列有推荐设备。

- 条件：还需查推荐设备列表
- 边界：满足系统版本不保证所有高规格编辑功能或流畅度
- 地区：美国/英文官方下载页；核验：2026-09-07
- 软件：DJI Mimo v2.11.9（核验快照）
- 来源：[S-D1-09 · Osmo 360 - Downloads](https://www.dji.com/360/downloads)；定位：Apps / DJI Mimo

### D1-022

**DJI Studio兼容｜已按记录日期核验**

核验时Studio为v1.2.11（2026-09-02），Mac门槛为macOS11及M1或更新芯片；Windows门槛为Windows10；建议至少16GB内存。

- 条件：Windows仍需对照下载页CPU、GPU推荐配置
- 边界：最低系统门槛不是高规格素材流畅处理保证；未验证Win/Mac所有功能一致
- 地区：美国/英文官方下载页；核验：2026-09-07
- 软件：DJI Studio v1.2.11（核验快照）
- 来源：[S-D1-09 · Osmo 360 - Downloads](https://www.dji.com/360/downloads)；定位：Softwares & Drivers / DJI Studio

### D1-023

**DaVinci工作流｜已按记录日期核验**

DJI Reframe的Resolve插件要求先在Studio预处理全景素材，再选Resolve专用格式导出后取景。

- 条件：Resolve20.0.1+；macOS15+，或Windows10 64-bit 22H2+/Windows11
- 边界：不能把它描述为任意版本Resolve直接打开OSV即可完整编辑
- 地区：美国/英文官方下载页；核验：2026-09-07
- 软件：DJI Reframe for DaVinci Resolve v1.0
- 来源：[S-D1-09 · Osmo 360 - Downloads](https://www.dji.com/360/downloads)；定位：DJI Reframe - Plugin for DaVinci Resolve

### D1-024

**镜片保护｜已按记录日期核验**

透明保护镜不能用于水下；官方建议避免在水上活动或雨雪中使用，以免内部起雾。

- 条件：装镜前清洁镜头与保护镜；装后开启相机透明保护镜模式
- 边界：保护镜有明显划伤应更换；机身镜头不支持用户自行更换
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-02 · Osmo 360 - FAQ](https://www.dji.com/360/faq)；定位：Accessories / Transparent Lens Protectors; Other / change the lens
- 来源：[S-D1-04 · Osmo 360 用户手册 v1.2（2025.09）](https://dl.djicdn.com/downloads/Osmo_360/20250905/Osmo_360_User_Manual_v1.2_zh-cn.pdf)；定位：第15页 控制中心 / 保护镜模式

### D1-025

**电池与快充｜已按记录日期核验**

支持1950mAh的Osmo Action Extreme Battery Plus及1770mAh的Osmo Action Extreme Battery；FAQ建议快充使用PD3.0且最大PD输出至少30W的USB-C充电器。

- 条件：核对电池准确型号
- 边界：不外推为全部Action电池通用；不同电池不能套用同一续航结果
- 地区：美国/英文官方站；电池采用该页英文全名；核验：2026-09-07
- 来源：[S-D1-02 · Osmo 360 - FAQ](https://www.dji.com/360/faq)；定位：Battery / fast charging / Action series batteries

### D1-026

**配件安装｜已按记录日期核验**

可用Osmo Action快拆配件；底部1/4英寸螺孔及快拆转接件提供其他配件安装路径。

- 条件：逐个核对配件兼容及装配要求
- 边界：机械能装上不保证自拍杆隐形、抗振或防水；弧面胶贴不可重复使用
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-02 · Osmo 360 - FAQ](https://www.dji.com/360/faq)；定位：Accessories / compatibility / mount different accessories / Curved Adhesive Base Max

### D1-027

**增稳｜已按记录日期核验**

支持RockSteady3.0与HorizonSteady；全景视频可在Mimo导出时选择增稳。

- 条件：单镜头HorizonSteady仅限标准视野、16:9去畸变的普通平面视频，帧率≤60fps
- 边界：不能宣称所有分辨率、视野和高帧率同时支持HorizonSteady
- 地区：中国大陆；部分参数参考英文官方站；核验：2026-09-07
- 来源：[S-D1-01 · Osmo 360 - Specs](https://www.dji.com/360/specs)；定位：Camera / Stabilization及脚注

### D1-028

**慢动作｜已按记录日期核验**

官方FAQ列明：全景视频支持最高4K/100fps的4倍慢动作；单镜头支持最高4K/120fps的4倍慢动作平面视频。

- 条件：全景4K为3840×1920；单镜头4K/120fps属于极广角视频，支持4:3、16:9、9:16画幅；4倍慢动作依拍摄帧率与成片播放帧率配合；拍摄、编辑时核对实际模式
- 边界：不将单镜头4K120写成普通全景4K120；不将普通录像慢动作、Vortex特效和软件插帧混作同一能力
- 地区：美国/英文官方站；核验：2026-09-07
- 来源：[S-D1-02 · Osmo 360 - FAQ](https://www.dji.com/360/faq)；定位：Camera / Can Osmo 360 shoot slow-motion videos?
- 来源：[S-D1-01 · Osmo 360 - Specs](https://www.dji.com/360/specs)；定位：Camera / Panoramic Video / Single Lens - Boost Video

### D1-029

**全景延时与运动延时｜已按记录日期核验**

全景Timelapse与Hyperlapse均列有8K/25fps、8K/30fps规格；Hyperlapse速度选项为Auto、2、5、10、15、30倍。

- 条件：Timelapse间隔为官方列出的1秒至60分钟离散选项，非任意连续数值；时长为5/10/20/30分钟、1/2/3/5小时或无限；使用相应延时模式；录制是否持续仍受电量、存储和环境条件影响
- 边界：延时输出帧率不是普通实时全景录像帧率；无限时长选项不等于无限续航；未核验该模式的完整导出上限或新增固件版本
- 地区：美国/英文官方站；核验：2026-09-07
- 来源：[S-D1-01 · Osmo 360 - Specs](https://www.dji.com/360/specs)；定位：Camera / Panorama - Timelapse / Hyperlapse / Timelapse

### D1-030

**Vortex旋转模式｜已按记录日期核验**

参数页的Panorama - Vortex列出6K（6000×1500）100/120fps，以及4K（3840×960）240fps。

- 条件：必须选择Vortex特殊模式；记录画幅为4:1；具体旋转安装与配件使用需另按相应官方指导核对
- 边界：不同于普通2:1全景录像；不能据此声称普通全景4K240或普通6K120；本卡只确认该模式规格，不保证任意装配方式、软件路径或最终平面导出规格
- 地区：美国/英文官方站；核验：2026-09-07
- 来源：[S-D1-01 · Osmo 360 - Specs](https://www.dji.com/360/specs)；定位：Camera / Panorama - Vortex

### D1-031

**全景后期重新取景｜已按记录日期核验**

一代全景素材可以在拍摄后重新取景：DJI的一代下载页明确提供在DaVinci Resolve中自由重构全景取景（reframe）的官方插件工作流。

- 条件：本卡直接核验的路径：先使用DJI Studio预处理全景素材，导出时选择DaVinci Resolve专用格式，再在Resolve使用DJI Reframe插件取景；插件要求Resolve20.0.1或以上；macOS15或以上，或Windows10 64-bit 22H2或以上/Windows11；Studio本身还需符合D1-022的设备条件
- 边界：此卡证明一条实际支持的后期取景路径，不宣称Resolve是所有后期取景的必需软件；这些插件前处理和系统条件仅属于本卡的Resolve路径，不能套用到Mimo；未据此确认Mimo的具体取景操作；不承诺任意裁切都保留球面8K分辨率，也不能从单镜头素材恢复未拍到的方向
- 地区：美国/英文官方下载页；核验：2026-09-07
- 软件：DJI Reframe for DaVinci Resolve v1.0；DJI Studio用于预处理
- 来源：[S-D1-09 · Osmo 360 - Downloads](https://www.dji.com/360/downloads)；定位：Softwares & Drivers / DJI Reframe - Plugin for DaVinci Resolve / freely reframe panoramic footage及同段前处理、版本条件

## Osmo 360 II

### D2-001

**sensor｜已按记录日期核验**

双 1/1.1 英寸方形 CMOS，光圈 f/1.9。

- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：相机 / 影像传感器、光圈

### D2-002

**imaging_area｜已按记录日期核验**

“1 英寸全景影像”指全景拍摄的成像面积口径。

- 条件：每颗传感器在全景拍摄时的成像面积等同 4:3 的 1 英寸 CMOS
- 边界：勿把宣传口径改写为两颗物理规格为 1 英寸的矩形传感器
- 地区：中国澳门；核验：2026-09-07
- 来源：[S-D2-04 · 购买 Osmo 360 II 8K 全景导演机 — DJI 澳门商城](https://store.dji.com/mo/product/osmo-360-2?from=site-nav&set_region=MO)；定位：原生 8K/60fps 问答脚注；脚注 2

### D2-003

**panoramic_video｜已按记录日期核验**

普通全景：8K 7680×3840、6K 6000×3000，均支持 24/25/30/48/50/60fps。

- 条件：普通全景模式
- 边界：8K 指整个全景画面；不等于任意视角裁切后仍有 8K 细节
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：相机 / 全景视频

### D2-004

**supernight｜已按记录日期核验**

全景超级夜景最高 8K/60fps；8K 和 6K 均可选 24/25/30/48/50/60fps。

- 条件：全景超级夜景模式
- 边界：不能据此认定单镜头超级夜景也支持 60fps
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：相机 / 全景-超级夜景

### D2-005

**single_lens｜已按记录日期核验**

单镜头普通视频最高 4K/60fps；4K、2.7K 提供 4:3 和 16:9，帧率 25/30/50/60fps。

- 条件：单镜头普通视频
- 边界：勿沿用 Osmo 360 的 5K 单镜头参数
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：相机 / 单镜头-视频

### D2-006

**single_lens_boost｜已按记录日期核验**

单镜头极广角：4K、2.7K 的 4:3、16:9、9:16 最高 120fps；1:1 最高 60fps。

- 条件：100/120fps 仅适用于所列非 1:1 比例
- 边界：与普通单镜头视频、夜景分开查阅
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：相机 / 单镜头-极广角视频

### D2-007

**single_lens_supernight｜已按记录日期核验**

单镜头超级夜景：4K 或 2.7K、4:3 或 16:9，25/30fps。

- 条件：Single Lens - SuperNight
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：相机 / 单镜头-超级夜景

### D2-008

**slow_motion｜已按记录日期核验**

全景慢动作支持 4K 3840×1920 的 100/200/240fps。

- 条件：Panorama - Slow Motion
- 边界：普通全景 8K/60fps 与 4K/240fps 是不同规格
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：相机 / 全景-慢动作

### D2-009

**vortex｜已按记录日期核验**

时空凝固（Vortex）模式列有 8K 7680×3840@100/120fps 和 6K 6000×1500@180/200fps。

- 条件：全景-时空凝固（Panorama - Vortex）专用模式
- 边界：不可写成普通全景视频可持续拍 8K/120fps；6K 像素尺寸按该模式单独记录
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：相机 / 全景-时空凝固

### D2-010

**timelapse｜已按记录日期核验**

全景运动延时最高 8K/30fps；静止延时最高 16K/30fps，两者均有 25fps 选项。

- 条件：运动延时和静止延时分开选择
- 边界：16K 是延时输出规格，不是普通实时视频
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：相机 / 全景-延时摄影

### D2-011

**photo｜已按记录日期核验**

全景照片最高 15520×7760（120 MP）；单镜头最高 6400×4800（30.72 MP）；照片格式列有 JPEG、RAW。

- 边界：具体 RAW/HDR 组合设置需按当前相机和软件核验
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：相机 / 照片最大分辨率、图片格式

### D2-012

**color｜已按记录日期核验**

视频支持 10-bit；D-Log M 在拍照、静止延时、长续航模式不可用。

- 条件：开启 D-Log M 后，智能影调、胶片影调均不可用
- 边界：10-bit 不等于所有模式都有 D-Log M
- 地区：中国澳门；核验：2026-09-07
- 来源：[S-D2-04 · 购买 Osmo 360 II 8K 全景导演机 — DJI 澳门商城](https://store.dji.com/mo/product/osmo-360-2?from=site-nav&set_region=MO)；定位：专业色彩；脚注 3

### D2-013

**hdr_video｜已按记录日期核验**

没有独立的 HDR 视频拍摄模式；官方将原始视频描述为高动态范围，可在 Mimo 或 Studio 后期使用 HDR 功能。

- 边界：不应编造相机端“HDR 视频模式”开关
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-01 · Osmo 360 II 新手快速攻略](https://repair.dji.com/help/content?customId=01700043735&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)；定位：06 猜您想问 / 能否拍摄 HDR 视频

### D2-014

**dynamic_range｜已按记录日期核验**

官方标称全景视频动态范围最高 14.5 级。

- 条件：DJI 实验室；全景 8K/30fps；普通色彩；自动曝光；前后测光
- 边界：不是所有模式、所有场景的保证值，也不是跨品牌同条件实测
- 地区：中国澳门；核验：2026-09-07
- 来源：[S-D2-04 · 购买 Osmo 360 II 8K 全景导演机 — DJI 澳门商城](https://store.dji.com/mo/product/osmo-360-2?from=site-nav&set_region=MO)；定位：升级点 2 及其脚注 1

### D2-015

**storage｜已按记录日期核验**

标称内置 128GB，用户可用 105GB；可加 microSD。

- 边界：标称容量与可用容量应分开写
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：相机 / 内置存储容量

### D2-016

**memory_card｜已按记录日期核验**

microSD 最高 1TB；官方推荐包含 Kingston CANVAS Go! Plus 与 Lexar Professional SILVER PLUS 的 U3 A2 V30 型号。

- 条件：按官方完整推荐型号和容量选卡
- 边界：速度等级相同不代表所有品牌卡均已验证
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：通用 / 支持存储卡类型、推荐 microSD 卡列表

### D2-017

**stitching｜已按记录日期核验**

常规全景拍摄建议主体距离相机至少 0.75m；全隐形防水壳水下为 1m。

- 条件：全景拼接
- 边界：近于安全距离可能出现接缝异常；距离合格也不是所有复杂场景的完美保证
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-11 · Osmo 360 II — 常见问题（中国大陆）](https://www.dji.com/cn/360-2/faq)；定位：相机 / 安全拼接距离

### D2-018

**invisible_selfie_stick｜已按记录日期核验**

隐形自拍杆依赖双鱼眼重叠区域和拼接处理；相机与杆应保持直线。

- 条件：建议使用官方隐形自拍杆；安装连接处保持在相机前后平面
- 边界：转接件折出角度或偏离平面可破坏隐形效果
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-11 · Osmo 360 II — 常见问题（中国大陆）](https://www.dji.com/cn/360-2/faq)；定位：相机 / 自拍杆隐形原理及使用注意

### D2-019

**stabilization｜已按记录日期核验**

全景防抖在 DJI Mimo 或 DJI Studio 导出时选择；单镜头 HorizonSteady 有规格限制。

- 条件：普通单镜头：标准视角、16:9、畸变校正、≤60fps；极广角单镜头：≤60fps
- 边界：不可宣称任意单镜头比例和高帧率均支持 HorizonSteady
- 地区：中国大陆；核验：2026-09-07
- 软件：DJI Mimo / DJI Studio（页面未标最低版本）
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：相机 / 增稳及脚注

### D2-020

**activation｜已按记录日期核验**

首次使用需通过 DJI Mimo 激活；手机开启 Wi-Fi、蓝牙并登录 DJI 账号后按连接提示完成。

- 条件：首次激活
- 地区：中国大陆；核验：2026-09-07
- 软件：DJI Mimo（未标最低版本）
- 来源：[S-D2-01 · Osmo 360 II 新手快速攻略](https://repair.dji.com/help/content?customId=01700043735&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)；定位：2.4 激活设备

### D2-021

**firmware_update｜已按记录日期核验**

相机连接 DJI Mimo 后按推送升级，升级前电量应大于 15%。

- 条件：有新固件提示时
- 边界：本页没有提供截至核验日的最新固件版本号
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-01 · Osmo 360 II 新手快速攻略](https://repair.dji.com/help/content?customId=01700043735&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)；定位：2.5 固件升级

### D2-022

**nfc｜已按记录日期核验**

NFC 碰一碰可打开 Mimo 并连接；相机回放页先选素材再碰，可下载所选素材。

- 条件：手机解锁并在主屏幕；蓝牙和 NFC 开启；已安装 DJI Mimo
- 边界：全景视频进入 Mimo 相册，其他素材进入手机相册；不是所有手机都有 NFC
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-01 · Osmo 360 II 新手快速攻略](https://repair.dji.com/help/content?customId=01700043735&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)；定位：3.4 素材传输 / NFC 碰一碰

### D2-023

**file_transfer｜已按记录日期核验**

素材可经 Mimo、microSD 读卡器或 USB-C 文件传输读取。

- 条件：USB 路径需在相机选择文件传输/USB 模式
- 边界：传输原素材不等于已经拼接、取景并导出最终平面成片
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-01 · Osmo 360 II 新手快速攻略](https://repair.dji.com/help/content?customId=01700043735&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)；定位：3.4 素材传输
- 来源：[S-D2-11 · Osmo 360 II — 常见问题（中国大陆）](https://www.dji.com/cn/360-2/faq)；定位：相机 / 如何导出已拍摄好的照片和视频

### D2-024

**spotlight_follow｜已按记录日期核验**

主角跟随可检测相机周围 2m 内的人脸，锁定后记录主角及视角信息；可用 Mimo 或 Studio 输出跟随主角的平面视频，最高 4K/30fps。

- 条件：主角跟随模式
- 边界：不能将该输出上限写成 8K/60fps
- 地区：中国大陆及中国澳门；核验：2026-09-07
- 来源：[S-D2-01 · Osmo 360 II 新手快速攻略](https://repair.dji.com/help/content?customId=01700043735&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)；定位：3.3 主角跟随
- 来源：[S-D2-04 · 购买 Osmo 360 II 8K 全景导演机 — DJI 澳门商城](https://store.dji.com/mo/product/osmo-360-2?from=site-nav&set_region=MO)；定位：升级点 5；脚注 3
- 来源：[S-D2-11 · Osmo 360 II — 常见问题（中国大陆）](https://www.dji.com/cn/360-2/faq)；定位：相机 / 主角跟随怎么使用（主角与视角信息、免后期手动二次构图、4K/30fps 脚注）

### D2-025

**tracking_loss｜已按记录日期核验**

主角丢失超过 5 秒会提示；再次入画不会自动恢复，需手动重新锁定。

- 条件：主角跟随
- 边界：不要承诺遮挡后始终自动续跟
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-11 · Osmo 360 II — 常见问题（中国大陆）](https://www.dji.com/cn/360-2/faq)；定位：相机 / 主角跟随怎么使用

### D2-026

**ai_slow_motion｜已按记录日期核验**

64 倍慢动作依靠 4K/240fps 全景素材与 DJI Studio 的 8 倍后期插帧处理。

- 条件：仅 Apple M 系列芯片 Mac 支持该功能
- 边界：不是相机原生录制 1920fps；最终平面输出须经过裁切
- 地区：中国大陆；核验：2026-09-07
- 软件：DJI Studio；Apple silicon Mac
- 来源：[S-D2-11 · Osmo 360 II — 常见问题（中国大陆）](https://www.dji.com/cn/360-2/faq)；定位：操控 / 如何实现 64 倍超级慢动作；相机 / 对比 Osmo 360 有哪些更新点及脚注

### D2-027

**ai_8k480｜已按记录日期核验**

“等效 8K/480fps”是用原生 8K/60fps 全景素材做 AI 插帧后的时间流畅度描述。

- 条件：DJI Studio AI 插帧，最高 8 倍慢放
- 边界：不是原生 8K/480fps；平面输出分辨率取决于裁切与软件设置
- 地区：中国澳门；核验：2026-09-07
- 来源：[S-D2-04 · 购买 Osmo 360 II 8K 全景导演机 — DJI 澳门商城](https://store.dji.com/mo/product/osmo-360-2?from=site-nav&set_region=MO)；定位：升级点 6；脚注 4

### D2-028

**davinci_workflow｜已按记录日期核验**

官方发布稿支持将 DJI Studio 导出的全景视频通过插件导入 DaVinci Resolve。

- 条件：先经 DJI Studio 导出，再用插件导入
- 边界：插件名称、版本和系统兼容矩阵本次未核验
- 地区：全球/其他地区；核验：2026-09-07
- 来源：[S-D2-05 · DJI Launches Osmo 360 II at IFA 2026](https://www.dji.com/media-center/announcements/dji-release-osmo-360-2)；定位：Improved Workflows with Spotlight Follow and One-Tap NFC Connections

### D2-029

**audio_builtin｜已按记录日期核验**

机身有 4 个麦克风；录音参数为 48kHz、16-bit、AAC。

- 条件：机身录音规格
- 边界：不等于连接无线麦克风后相机音轨变成 32-bit float
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：通用 / 麦克风；相机 / 音频录制

### D2-030

**audio_wireless｜已按记录日期核验**

可无线直连 DJI Mic 2、Mic Mini、Mic 3、Mic Mini 2、Mic Mini 2S 的发射器；不支持通过接收器连接。

- 条件：相机麦克风菜单选择 TX1/TX2；发射器进入蓝牙配对
- 边界：勿套用其他 Osmo 相机的 USB 接收器方案
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-06 · DJI Mic 系列可以搭配哪些产品使用、如何使用？](https://repair.dji.com/help/content?customId=zh-cn03400006931&lang=zh-CN&re=CN&spaceId=34)；定位：搭配 Osmo 360 系列

### D2-031

**audio_two_tx｜已按记录日期核验**

支持同时连接两台 DJI 无线麦克风发射器。

- 条件：使用支持的 DJI Mic 发射器
- 边界：不自动保证不同代发射器任意混搭或所有降噪、内录功能一致
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-01 · Osmo 360 II 新手快速攻略](https://repair.dji.com/help/content?customId=01700043735&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)；定位：4.1 连接收音设备

### D2-032

**battery｜已按记录日期核验**

标准参数所列电池容量为 2150mAh、8.3Wh。

- 边界：兼容旧电池不代表旧电池容量与此一致
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：电池 / 容量、能量

### D2-033

**runtime｜已按记录日期核验**

官方 8K/30fps 全景续航为最长 100 分钟，长续航模式最长 120 分钟。

- 条件：25℃ 实验室；Wi-Fi、手势控制、语音控制、快剪助手关闭；屏幕关闭
- 边界：实验室参考值；不用于保证 8K/60fps、夜景或冬季实拍时长；欧盟/英国因温度法规可能不同
- 地区：中国澳门；核验：2026-09-07
- 来源：[S-D2-04 · 购买 Osmo 360 II 8K 全景导演机 — DJI 澳门商城](https://store.dji.com/mo/product/osmo-360-2?from=site-nav&set_region=MO)；定位：续航问答及脚注

### D2-034

**battery_compatibility｜已按记录日期核验**

支持 Osmo Action 1950mAh 耐低温增强续航电池和 1770mAh 耐低温长续航电池。

- 边界：不可沿用 2150mAh 电池的续航数值
- 地区：中国澳门；核验：2026-09-07
- 来源：[S-D2-04 · 购买 Osmo 360 II 8K 全景导演机 — DJI 澳门商城](https://store.dji.com/mo/product/osmo-360-2?from=site-nav&set_region=MO)；定位：Osmo Action 系列电池兼容问答

### D2-035

**temperature｜已按记录日期核验**

工作温度 -20～45℃；充电温度 5～40℃。

- 边界：可低温工作不等于可在 -20℃ 充电
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：电池 / 使用环境温度、充电环境温度

### D2-036

**waterproof_body｜已按记录日期核验**

裸机防水标称 10m，IP68；水下折射仍可能导致失真和拼接错误。

- 条件：电池仓和 USB-C 保护盖关紧；受控水压测试
- 边界：不建议裸机水下拍摄；避开温泉、腐蚀/不明液体、极端涉水及长时间高冲击水流
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：通用 / 防水及脚注
- 来源：[S-D2-11 · Osmo 360 II — 常见问题（中国大陆）](https://www.dji.com/cn/360-2/faq)；定位：其他 / 具备防水能力吗（长时间水下或水流冲击压力大时不建议裸机下水）

### D2-037

**waterproof_case｜已按记录日期核验**

另购 Osmo 360 全隐形防水壳后标称可达 50m；水下安全拼接距离 1m。

- 条件：按防水壳操作规范正确安装；DJI 实验室受控水压测试
- 边界：防水表现受潜水环境与产品状态影响
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-01 · Osmo 360 II 新手快速攻略](https://repair.dji.com/help/content?customId=01700043735&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)；定位：4.5 Osmo 360 全隐形防水壳
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：通用 / 防水及脚注

### D2-038

**lens_replacement｜已按记录日期核验**

外层镜片意外刮伤或受损后，可用 Osmo 360 II 镜片更换套件自行更换。

- 条件：对应 II 型号更换套件，需另购
- 边界：指外层镜片；不代表镜头模组或传感器可自行更换
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-01 · Osmo 360 II 新手快速攻略](https://repair.dji.com/help/content?customId=01700043735&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)；定位：4.4 Osmo 360 II 镜片更换套件
- 来源：[S-D2-11 · Osmo 360 II — 常见问题（中国大陆）](https://www.dji.com/cn/360-2/faq)；定位：相机 / 如何保护镜头；其他 / 能否更换镜片

### D2-039

**mounting｜已按记录日期核验**

采用双向磁吸快拆和底部 1/4 英寸螺纹；双向底座支持 Osmo Nano、Osmo Action 6。

- 条件：具体配件核对型号
- 边界：FAQ 不建议用于其他相机：即使物理可插入，也可能磁力较弱
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-11 · Osmo 360 II — 常见问题（中国大陆）](https://www.dji.com/cn/360-2/faq)；定位：配件 / 快拆接口兼容、如何安装配件

### D2-040

**selfie_stick_accessory｜已按记录日期核验**

大陆官方 1.2 米双向磁吸隐形自拍杆套件列明适配 Osmo 360 II。

- 条件：核验日页面价格 229 元人民币；对应单独套件
- 边界：价格会变化；不据此推断其他杆款或一代的兼容
- 地区：中国大陆；核验：2026-09-06
- 来源：[S-D2-07 · Osmo 1.2 米双向磁吸隐形自拍杆套件](https://store.dji.com/cn/product/osmo-120-cm-dual-direction-quick-release-invisible-selfie-stick-kit?from=site-nav&set_region=CN&vid=261771)；定位：产品名、适配 Osmo 360 II、价格

### D2-041

**controls｜已按记录日期核验**

语音建议安静环境内 1m；手势建议 2m；扭转开拍需连续转杆两次、每次超过 45°。

- 条件：分别先开启对应控制功能
- 边界：手势有效距离可能随固件改变；不保证风噪、遮挡或高速运动时成功
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-11 · Osmo 360 II — 常见问题（中国大陆）](https://www.dji.com/cn/360-2/faq)；定位：操控 / 语音控制、手势控制、扭转开拍

### D2-042

**snapshot｜已按记录日期核验**

关机时短按拍摄键可用 SnapShot 迅速开录；停拍后 3 秒无操作则自动关机。

- 条件：SnapShot 预设可在设置中调整
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-01 · Osmo 360 II 新手快速攻略](https://repair.dji.com/help/content?customId=01700043735&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)；定位：3.3 SnapShot 快速启动

### D2-043

**charging｜已按记录日期核验**

支持 PD 3.0 快充，FAQ 建议 USB-C 充电器最大 PD 输出达到 30W 或以上；支持边充边用。

- 条件：干燥环境，符合充电温度范围
- 边界：这是充电器建议，不是相机任何时候都以 30W 充电
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-11 · Osmo 360 II — 常见问题（中国大陆）](https://www.dji.com/cn/360-2/faq)；定位：电池 / 是否支持快充、是否支持插电时使用
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：电池 / 充电环境温度；通用 / 防水脚注（接口盖需闭紧）

### D2-044

**battery_storage｜已按记录日期核验**

超过 10 天不用时，官方建议电量 40%～65% 储存，约每 3 个月充放电维护。

- 条件：长期储存
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-01 · Osmo 360 II 新手快速攻略](https://repair.dji.com/help/content?customId=01700043735&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)；定位：2.2 设备充电 / 提示

### D2-045

**lens_protectors｜已按记录日期核验**

透明保护镜只能防泼溅，不能水下使用；官方建议避免在雨雪及水上活动中使用，以免起雾。

- 条件：安装前清理镜片、卡槽与保护镜内外表面
- 边界：保护镜不是全隐形防水壳；出现明显刮伤应更换
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-11 · Osmo 360 II — 常见问题（中国大陆）](https://www.dji.com/cn/360-2/faq)；定位：配件 / 透明镜头保护镜防刮伤能力、可以下水使用吗

### D2-046

**motion_blur｜已按记录日期核验**

软件运动模糊/ND 效果当前支持 Apple M 系列 Mac 的 DJI Studio，以及 iPhone 14 及后续机型的 DJI Mimo。

- 条件：将软件更新至最新版本
- 边界：这是后期效果，不等同安装物理 ND 镜
- 地区：中国大陆；核验：2026-09-07
- 软件：DJI Studio / DJI Mimo（页面未列最低版本）
- 来源：[S-D2-11 · Osmo 360 II — 常见问题（中国大陆）](https://www.dji.com/cn/360-2/faq)；定位：APP / 如何使用 ND 滤镜特效

### D2-047

**file_format｜已按记录日期核验**

全景视频为 OSV；平面视频为 MP4（HEVC）。

- 边界：文件传输完成后仍需选择全景输出或平面重构工作流
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-11 · Osmo 360 II — 常见问题（中国大陆）](https://www.dji.com/cn/360-2/faq)；定位：相机 / 可拍摄什么格式的视频

### D2-048

**dimensions｜已按记录日期核验**

机身 61×36.3×81mm，重量 183g。

- 条件：官方参数口径
- 边界：配件、电池组合或安装总重量需另算，不作为整套装备重量
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-10 · Osmo 360 II — 技术参数（中国大陆）](https://www.dji.com/cn/360-2/specs)；定位：通用 / 尺寸、重量

### D2-049

**thermal_management｜已按记录日期核验**

高规格和长时间拍摄会增加发热；官方建议降分辨率/帧率、关屏、停用不必要 Wi-Fi 并保持通风。

- 条件：已出现明显发热时可按此排查
- 边界：不形成“永不热停”或固定热停分钟数结论
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-11 · Osmo 360 II — 常见问题（中国大陆）](https://www.dji.com/cn/360-2/faq)；定位：其他 / 使用过程中为什么发热、如何缓解发热

### D2-050

**firmware_release_record｜已按记录日期核验**

2026-08-13 官方日文发布记录列明固件 V01.01.02.10，配套 DJI Mimo iOS/Android 均为 V2.11.4；记录包含全景/夜景影像、全景照片和主角跟随稳定性优化及已知问题修复。

- 条件：适用于该份 2026-08-13 发布记录
- 边界：未取得完整更新历史，不能声称这是 2026-09-06 最新版本；Mimo V2.11.4 是记录列示版本，不等同所有功能的最低兼容版本
- 地区：日本语言版；核验：2026-09-06
- 固件：V01.01.02.10
- 软件：DJI Mimo iOS/Android V2.11.4（该记录列示版本）
- 来源：[S-D2-09 · DJI Osmo 360 II リリースノート（2026-08-13）](https://terra-1-g.djicdn.com/6189933d30024fc1b331bffe4fe41837/360-2/20260806/DJI_Osmo_360_II_Release_Notes_ja.pdf)；定位：第 1 页：版本栏及最新情報

### D2-051

**export_matrix_gap｜待核验**

待核验：完整的 Mimo/Studio 全景与平面导出矩阵、16K 导出设备条件和插件版本兼容。

- 边界：已验证的主角跟随和 AI 慢动作条件可查对应卡；其余上限暂不推断；补核验 global/cn 下载页仅返回标题页面壳；已读发布记录只给 Mimo 对应版本，未给导出矩阵或插件兼容表；2026-09-07 再次读取已知下载地址仍为 534 字节标题页面壳；大陆 Specs/FAQ 的个别功能条件不等于完整导出矩阵
- 地区：全球/其他地区；核验：2026-09-06

### D2-052

**post_reframing｜已按记录日期核验**

全景素材可在后期选择构图；转为平面视频时需要视角裁切。

- 条件：最终导出分辨率按实际软件设置
- 边界：不等于任意裁切后仍保留整幅全景的 8K 分辨率；完整设备和导出矩阵仍待核
- 地区：中国澳门；核验：2026-09-07
- 来源：[S-D2-04 · 购买 Osmo 360 II 8K 全景导演机 — DJI 澳门商城](https://store.dji.com/mo/product/osmo-360-2?from=site-nav&set_region=MO)；定位：专业色彩（后制构图）；升级点 6 的脚注 4（平面裁切与实际导出）

### D2-053

**smart_tone｜已按记录日期核验**

智能影调可调节画面对比度并提亮人脸，效果需将素材导入 DJI Mimo 后查看。

- 条件：智能影调开启；D-Log M 关闭
- 边界：不把效果写为所有人脸、光线下的保证；D-Log M 开启后智能影调与胶片影调均不可用
- 地区：中国大陆及中国澳门；核验：2026-09-07
- 软件：DJI Mimo（来源未标最低版本）
- 来源：[S-D2-01 · Osmo 360 II 新手快速攻略](https://repair.dji.com/help/content?customId=01700043735&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)；定位：3.2 图像与音频
- 来源：[S-D2-04 · 购买 Osmo 360 II 8K 全景导演机 — DJI 澳门商城](https://store.dji.com/mo/product/osmo-360-2?from=site-nav&set_region=MO)；定位：脚注 3 / D-Log M 与影调互斥

### D2-054

**single_lens_switch｜已按记录日期核验**

单镜头录制中可不中断录像切换前后镜头，最高 4K/60fps 及以下规格。

- 条件：单镜头录制；≤4K/60fps
- 边界：不等于同一模式同时录下前后两路；不外推至 4K/120fps
- 地区：中国大陆；核验：2026-09-07
- 来源：[S-D2-11 · Osmo 360 II — 常见问题（中国大陆）](https://www.dji.com/cn/360-2/faq)；定位：相机 / 是否支持单镜头录制过程中切换镜头

## Insta360 X6

### IX6-001

**全景拍摄｜已按记录日期核验**

全景视频支持7680×3840最高50fps、6016×3008最高60fps；PureVideo全景8K最高30fps。

- 条件：按对应360 Video或PureVideo模式选择
- 边界：球面文件规格不等于重取景后的平面成片规格
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX6-01 · Insta360 X6 产品页与规格](https://www.insta360.com/product/insta360-x6)；定位：Specs / Video Resolution (360 Mode)

### IX6-002

**平面拍摄｜已按记录日期核验**

平面视频最高5K60或4K120；170°视场对应5K30，5K60最大视场为132°。

- 条件：5K60采用支持60fps的横向比例
- 边界：不能把170°、5K、60fps拼成同一档位
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX6-01 · Insta360 X6 产品页与规格](https://www.insta360.com/product/insta360-x6)；定位：Flat Video / Specs / 脚注2

### IX6-003

**色彩｜已按记录日期核验**

产品页列出10-bit及Standard、Dolby Vision、I-Log色彩选项。

- 条件：按拍摄菜单可选模式使用
- 边界：未核验各模式组合及输出端Dolby Vision兼容清单
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX6-01 · Insta360 X6 产品页与规格](https://www.insta360.com/product/insta360-x6)；定位：10-Bit Color / Color Preset
- 来源：[S-IX-10 · X Series: Color Bit Depth and Chroma Subsampling](https://onlinemanual.insta360.com/x6/en-us/specs/color-chroma)；定位：Color bit depth / X6 Video；Color gamut / X6；FAQ 1 / I-Log

### IX6-004

**传感器命名｜已按记录日期核验**

实际传感器规格为双1/1.1英寸；“1英寸全景成像”是官方对全景成像面积的等效描述。

- 条件：官方等效解释以4:3和360内容为条件
- 边界：不得改写为两颗物理1英寸传感器
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX-02 · X Series: Hardware Specifications](https://onlinemanual.insta360.com/x5/en-us/specs/hardware)；定位：Sensor Size / X6列
- 来源：[S-IX6-01 · Insta360 X6 产品页与规格](https://www.insta360.com/product/insta360-x6)；定位：脚注1

### IX6-005

**存储｜已按记录日期核验**

内置64GB，其中可用47GB；可扩展microSD，硬件表列上限1TB。

- 条件：microSD需UHS-I V30或更高速度等级
- 边界：系统与缓存占用的空间不能计入素材可用容量
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX-02 · X Series: Hardware Specifications](https://onlinemanual.insta360.com/x5/en-us/specs/hardware)；定位：Memory / X6列
- 来源：[S-IX6-01 · Insta360 X6 产品页与规格](https://www.insta360.com/product/insta360-x6)；定位：Memory

### IX6-006

**续航｜已按记录日期核验**

Xtreme电池在官方指定条件下，全景8K30约140分钟；8K50约79分钟。

- 条件：25°C实验室；开机息屏；Wi-Fi开启；标准码率；标准色彩；360镜头模式；Xtreme电池
- 边界：实际续航受温度、参数和设备状态影响；不同品牌测试条件不一致
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX-03 · X Series: Battery Level & Battery Life](https://onlinemanual.insta360.com/x6/en-us/operating-tutorials/duration/battery-duration)；定位：Recording with screen off / X6 + Standard Battery / Xtreme Battery

### IX6-007

**直出与跟随｜已按记录日期核验**

InstaFrame 2.0可同时保存4K30平面视频与8K30全景备份；关闭备份后仅保留平面视频。

- 条件：需要在拍摄前开启360 Video Backup以保留球面素材
- 边界：不能在只保存平面视频后恢复未保存的其他方向
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX6-04 · X6: InstaFrame 2.0](https://onlinemanual.insta360.com/x6/en-us/operating-tutorials/capture-preview/shooting-mode/instaframe)；定位：How to enable 360 Video Backup / Feature Comparison

### IX6-008

**素材传输｜已按记录日期核验**

可用USB连接并选择File Transfer导出INSV/INSP；也可关机取卡后用读卡器复制。

- 条件：连接电脑使用相应USB数据线；取卡前关机
- 边界：复制原始文件不等于已经重取景和导出平面成片
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX6-05 · Connecting to Studio and Transferring Files](https://onlinemanual.insta360.com/x6/en-us/camera/file-transfer-footage-management/connecting-to-studio-and-transferring-files)；定位：U-Disk Transfer Mode / High-Speed Card Reader Transfer

### IX6-009

**外置音频｜已按记录日期核验**

X6产品页明示可同时连接两只Mic Air或Mic Pro发射器，直接进行双人无线收音。

- 条件：使用明示兼容的发射器并核对当前固件
- 边界：未核验不同型号发射器混用及双轨交付细节；不类推至其他蓝牙麦克风
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX6-01 · Insta360 X6 产品页与规格](https://www.insta360.com/product/insta360-x6)；定位：Pro-Grade Audio / Insta360 Direct Connect

### IX6-010

**防水与水下成像｜已按记录日期核验**

裸机防水深度为20米；水下折射会影响对焦和拼接，官方建议采用适配潜水壳。

- 条件：电池盖、USB盖完整闭合且橙色标记不可见；密封无损无砂尘；潜水壳与防雾片按对应说明使用
- 边界：防水深度不代表裸机水下拼接质量；镜头保护镜不能与潜水壳同时使用
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX-06 · X Series: Dustproofing & Waterproofing Related FAQ](https://onlinemanual.insta360.com/x6/en-us/operating-tutorials/protection/waterproof)；定位：Waterproof Performance / FAQ 1、2

### IX6-011

**镜片维护｜已按记录日期核验**

X6有专用可更换镜头套件；商城要求在清洁、少尘、湿度低于70%的环境操作。

- 条件：只用X6兼容套件并先读随附操作说明
- 边界：换镜并非任何损坏均能自修；不直接套用X5教程的工具和步骤
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX6-07 · X6 Replacement Lens Kit 官方商城](https://store.insta360.com/product/x6-replacement-lens-kit?i_campaign=x6-replacement-lens-kit&i_medium=product_page_button&i_source=website)；定位：X6 Replacement Lens Kit / 使用条件

### IX6-012

**费用｜已按记录日期核验**

2026-09-06所见美国商城X6标准套装为699.99美元，黑色且不含microSD卡。

- 条件：标准套装含相机、Xtreme电池、USB-C线及保护袋；页面所示地区美国，币种USD
- 边界：动态页面会变；非大陆报价，不包含额外配件和可能税费
- 地区：美国；价格观察日2026-09-06；核验：2026-09-06
- 来源：[S-IX6-08 · Insta360 X6 官方商城](https://store.insta360.com/product/x6?i_campaign=x6-comparison&i_medium=product_page_button&i_source=website)；定位：United States / Standard Bundle / No microSD Card

### IX6-013

**云服务费用｜已按记录日期核验**

产品页注明Moments Pro需订阅，具体方案需在Insta360 App查看。

- 条件：以用户所在地区App可见方案为准
- 边界：本次未读取大陆订阅金额，不计入统一总价
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX6-01 · Insta360 X6 产品页与规格](https://www.insta360.com/product/insta360-x6)；定位：脚注12

### IX6-014

**安装｜已按记录日期核验**

X6支持1/4英寸螺纹与磁吸安装；官方列其磁吸接口兼容X5、X4 Air和Ace系列安装配件。

- 条件：限明示安装接口与对应配件
- 边界：接口兼容不等于电池、潜水壳、镜头套件全部通用
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX6-01 · Insta360 X6 产品页与规格](https://www.insta360.com/product/insta360-x6)；定位：Magnetic Mounting Ecosystem / Interface

### IX6-015

**后期软件｜已按记录日期核验**

官方提供手机Insta360 App与Mac/Windows版Insta360 Studio用于全景内容处理。

- 条件：拍摄球面素材后选择角度再输出
- 边界：本次未核验当前App和Studio每种导出档位及最低系统组合
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX6-01 · Insta360 X6 产品页与规格](https://www.insta360.com/product/insta360-x6)；定位：Shoot First, Frame Later / Insta360 Studio

## Insta360 X5

### IX5-001

**全景拍摄｜已按记录日期核验**

全景视频最高8K30；另有5.7K60和全景4K120，PureVideo全景8K最高30fps。

- 条件：按Video或PureVideo对应模式选择
- 边界：全景规格不能用作任意角度平面成片分辨率
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX5-01 · Insta360 X5 产品页与规格](https://www.insta360.com/product/insta360-x5)；定位：Specs / 360 Video Resolution

### IX5-002

**单镜头拍摄｜已按记录日期核验**

单镜头视频最高4K60；170° MaxView对应FreeFrame 4K30。

- 条件：单镜头Video与FreeFrame为不同模式
- 边界：不能写成170°的4K60
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX5-01 · Insta360 X5 产品页与规格](https://www.insta360.com/product/insta360-x5)；定位：4K60FPS SINGLE-LENS MODE / Single-Lens Video Resolution

### IX5-003

**硬件与存储｜已按记录日期核验**

X5采用双1/1.28英寸传感器；存储使用microSD，要求UHS-I V30或更高速度等级。

- 条件：先确认存储卡型号和速度等级
- 边界：不把同表X6的内置64GB或可用47GB写到X5
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX5-01 · Insta360 X5 产品页与规格](https://www.insta360.com/product/insta360-x5)；定位：Sensor Size
- 来源：[S-IX-02 · X Series: Hardware Specifications](https://onlinemanual.insta360.com/x5/en-us/specs/hardware)；定位：Memory / Sensor Size / X5列

### IX5-004

**机身音频｜已按记录日期核验**

X5音频模式列有自动风噪抑制、人声增强、立体声和360°音频。

- 条件：按环境选择音频模式
- 边界：存在降噪功能不等于任何风速下均能完全消除风噪
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX5-01 · Insta360 X5 产品页与规格](https://www.insta360.com/product/insta360-x5)；定位：Audio Modes

### IX5-005

**续航冲突｜来源冲突**

电池FAQ在指定条件下记X5标准电池8K30约93分钟；产品页比较区另记100分钟，差异未解决。

- 条件：FAQ：25°C实验室；开机息屏；Wi-Fi设Auto；标准码率；AdaptiveTone关闭；AI Highlights Assistant关闭；标准电池
- 边界：产品页Specs也为93分钟，Comparison的100分钟未给出足以解释差异的独立完整条件；培训不挑选其中一个数值做无条件续航结论
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX-03 · X Series: Battery Level & Battery Life](https://onlinemanual.insta360.com/x6/en-us/operating-tutorials/duration/battery-duration)；定位：X5 + Standard Battery / 8K30fps
- 来源：[S-IX5-01 · Insta360 X5 产品页与规格](https://www.insta360.com/product/insta360-x5)；定位：Comparison / Max. Run Time；Specs / Run Time

### IX5-006

**节能续航｜已按记录日期核验**

标准电池在官方指定节能条件下，5.7K24约208分钟。

- 条件：25°C实验室；Endurance Mode开启；开机息屏；Wi-Fi设Auto；标准码率；AdaptiveTone关闭；AI Highlights Assistant关闭；固件v1.3.0或以上
- 边界：不等于8K续航；Ultra电池235分钟是另一个电池组合
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 固件：v1.3.0或以上
- 来源：[S-IX-03 · X Series: Battery Level & Battery Life](https://onlinemanual.insta360.com/x6/en-us/operating-tutorials/duration/battery-duration)；定位：X5 + Standard Battery / 5.7K24fps
- 来源：[S-IX5-01 · Insta360 X5 产品页与规格](https://www.insta360.com/product/insta360-x5)；定位：脚注1

### IX5-007

**直出与版本｜已按记录日期核验**

InstaFrame 2.0关闭360备份可输出4K30平面；开启备份则保存5.7K+30全景与1080p30平面。

- 条件：X5固件v1.7.43或以上；Insta360 App v2.14.0或以上
- 边界：该模式的人物跟踪不含动物或物体；关闭备份后不能恢复其他方向素材
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 固件：v1.7.43或以上
- 软件：Insta360 App v2.14.0或以上
- 来源：[S-IX5-02 · X Series: InstaFrame Mode](https://onlinemanual.insta360.com/x5/en-us/operating_tutorials/capture-preview/shooting-mode/instaframe)；定位：InstaFrame 2.0 / Comparison / FAQ 1

### IX5-008

**外置音频｜已按记录日期核验**

兼容表X5行支持Mic Air与Mic Pro蓝牙直连，也列出接收器连接方式。

- 条件：相机及麦克风更新至对应支持固件；按所选发射器/接收器套装连接
- 边界：本卡未验证多发射器同时连接；不可从X6的双人直连能力类推
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX5-03 · Mic Series: Compatibility List](https://onlinemanual.insta360.com/micair/en-us/specs/compatibility)；定位：Compatibility / X5行

### IX5-009

**防水与水下成像｜已按记录日期核验**

X5裸机防水15米，但水下360拍摄可能因折射出现拼接问题，官方推荐隐形潜水壳。

- 条件：入水前取下镜头保护镜；电池和USB盖密封完整闭合；海水使用后清水冲洗并浸泡5至10分钟，完全干燥再开盖
- 边界：避免高速入水；防水等级不保证水下拼接效果
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX5-04 · X5 Waterproofing](https://onlinemanual.insta360.com/x5/en-us/camera/maintenance/waterproof)；定位：Waterproofing 1-5

### IX5-010

**镜片维护｜已按记录日期核验**

X5可用专用镜头套件更换；安装后需执行Stitching Calibration。

- 条件：在少尘室内操作；湿度超过60%时按指南先除湿；使用适配工具
- 边界：镜环变形、磨损、裂镜等超出该指南适用状况时停止自换并联系售后
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX5-05 · X Series: Replacement Lens Kit](https://onlinemanual.insta360.com/x4air/en-us/faq/accessories/lens_kit)；定位：How to install/remove the lens / 步骤5；Lens Replacement Precautions

### IX5-011

**素材文件｜已按记录日期核验**

X5全景素材含一个保存双镜头数据的高分辨率VID原始文件，以及LRV代理文件。

- 条件：按原始素材与代理文件用途归档
- 边界：不要把LRV预览文件当作高画质交付源
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX-09 · X Series: File Formats](https://onlinemanual.insta360.com/x6/en-us/operating-tutorials/storage/flieformat)；定位：Video Formats Supported / FAQ 1

### IX5-012

**费用｜已按记录日期核验**

2026-09-06所见美国商城X5黑色标准套装促销价464.99美元，划线价549.99美元，不含microSD卡。

- 条件：页面套装说明包含相机及一块电池；币种USD
- 边界：这是地区与日期限定的促销观察，非大陆价格；不能据此给出统一成本胜负
- 地区：美国；价格观察日2026-09-06；核验：2026-09-06
- 来源：[S-IX5-06 · Insta360 X5 官方商城](https://store.insta360.com/product/x5?i_campaign=x5-comparison&i_medium=product_page_button&i_source=website)；定位：United States / Standard Bundle / No microSD Card

### IX5-013

**后期软件｜已按记录日期核验**

X5全景视频采用INSV，普通单镜头视频为MP4；官方支持Insta360 App及Studio处理全景内容。

- 条件：此格式说明针对对应模式，FreeFrame等专门模式另查
- 边界：手机可控制相机不代表必能流畅处理最高规格素材
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX5-01 · Insta360 X5 产品页与规格](https://www.insta360.com/product/insta360-x5)；定位：Video Format / Insta360 Studio
- 来源：[S-IX5-02 · X Series: InstaFrame Mode](https://onlinemanual.insta360.com/x5/en-us/operating_tutorials/capture-preview/shooting-mode/instaframe)；定位：InstaFrame 1.0 / Retention of 360 video

### IX5-014

**安装｜已按记录日期核验**

X5硬件列有1/4英寸安装点及快拆安装点。

- 条件：使用相应接口配件
- 边界：接口相同不表示所有外形套件或电池跨代通用
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-IX-02 · X Series: Hardware Specifications](https://onlinemanual.insta360.com/x5/en-us/specs/hardware)；定位：Mounting Point / X5列

### IX5-015

**视频位深与Log｜已按记录日期核验**

官方色彩表列X5视频为8-bit，并支持Flat及I-Log；支持Log不等于视频是10-bit。

- 条件：按X5列读取Video行与Log行
- 边界：DNG照片的16-bit与视频位深属于不同对象；不能据此写成16-bit视频
- 地区：全球英文资料；核验：2026-09-06
- 来源：[S-IX-10 · X Series: Color Bit Depth and Chroma Subsampling](https://onlinemanual.insta360.com/x6/en-us/specs/color-chroma)；定位：Color bit depth / X5列；FAQ 1 / Flat、Log

## GoPro MAX2

### GM2-001

**全景拍摄｜已按记录日期核验**

MAX2支持8K30全景视频；官方当前产品页另列5.6K60及4K100球面视频。

- 条件：8K30来源为公司2025年年报产品披露；高帧率档按当前相机地区/防闪烁设置复核
- 边界：球面视频与重取景平面分辨率不可混用
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-GM2-07 · GoPro 2025 Form 10-K 产品介绍](https://www.sec.gov/Archives/edgar/data/1500435/000150043526000006/gpro-20251231.htm)；定位：Our Products / MAX2 / 8K at 30 FPS
- 来源：[S-GM2-01 · GoPro MAX2 产品页](https://gopro.com/en/us/shop/cameras/learn/max2/CHDHZ-311-master.html)；定位：SUPER SLO-MO IN 360

### GM2-002

**单镜头拍摄｜已按记录日期核验**

MAX2单镜头支持4K60，Max HyperView数字镜头可提供180°视场。

- 条件：使用Single Lens模式及Max HyperView
- 边界：数字镜头选择影响画面视场和形变
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-GM2-01 · GoPro MAX2 产品页](https://gopro.com/en/us/shop/cameras/learn/max2/CHDHZ-311-master.html)；定位：180° IN 4K60

### GM2-003

**色彩与码率｜已按记录日期核验**

MAX2支持8K 10-bit及GP-Log；v1.30增加200Mbps最大码率选项，300Mbps需可选GoPro Labs固件。

- 条件：200Mbps要求v1.30或以上支持版本；300Mbps须GoPro Labs而非默认固件设置
- 边界：码率不是综合画质排名；Log素材需后期处理
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 固件：v1.30增加200Mbps；300Mbps另需GoPro Labs
- 来源：[S-GM2-03 · MAX2 Firmware Update](https://gopro.com/en/us/update/max2)；定位：MAX2 v1.30 / NEW FEATURES
- 来源：[S-GM2-04 · GoPro 2025年9月23日新品发布公告](https://investor.gopro.com/press-releases/press-release-details/2025/GoPro-Announces-Three-New-Products---MAX2-360-Camera-with-True-8K-Resolution-and-Twist-and-Go-Replaceable-Lenses-LIT-HERO-Miniature-4K-Lifestyle-Camera-with-Built-In-Light-for-Whatever-Whenever-Capture-and-Fluid-Pro-AI-Gimbal-for-Stabilizing-GoPros-P/default.aspx)；定位：10-Bit Color / Enhanced Capability with GoPro Labs

### GM2-004

**机身音频｜已按记录日期核验**

MAX2有六麦克风阵列；单镜头可设置Front、Back或Match Lens等收音方向。

- 条件：全景和单镜头音频控制不同
- 边界：麦克风数量不能直接证明收音胜过竞品
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-GM2-01 · GoPro MAX2 产品页](https://gopro.com/en/us/shop/cameras/learn/max2/CHDHZ-311-master.html)；定位：IMMERSIVE AUDIO + PRECISE CONTROL

### GM2-005

**外置音频｜已按记录日期核验**

MAX2支持蓝牙音频，可用兼容AirPods、蓝牙耳机或无线麦克风录音。

- 条件：逐型号确认兼容设备
- 边界：本次未读取完整蓝牙兼容列表，不承诺所有第三方麦克风
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-GM2-01 · GoPro MAX2 产品页](https://gopro.com/en/us/shop/cameras/learn/max2/CHDHZ-311-master.html)；定位：BLUETOOTH AUDIO + VOICE CONTROL

### GM2-006

**电池｜已按记录日期核验**

MAX2配套Cold-Weather Enduro电池容量为1960mAh。

- 条件：型号为MAX2对应电池
- 边界：本次未验证与其他GoPro型号电池互换；容量不能代替实测续航
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-GM2-04 · GoPro 2025年9月23日新品发布公告](https://investor.gopro.com/press-releases/press-release-details/2025/GoPro-Announces-Three-New-Products---MAX2-360-Camera-with-True-8K-Resolution-and-Twist-and-Go-Replaceable-Lenses-LIT-HERO-Miniature-4K-Lifestyle-Camera-with-Built-In-Light-for-Whatever-Whenever-Capture-and-Fluid-Pro-AI-Gimbal-for-Stabilizing-GoPros-P/default.aspx)；定位：1960mAh Cold-Weather Enduro Battery

### GM2-007

**续航待核｜待核验**

尚未取得可读取的MAX2官方续航时长及完整实验条件。

- 条件：需补读官方续航表并确认分辨率、帧率、温度、无线、屏幕及电池
- 边界：不得填入测评时长冒充官方值，也不得据此推断续航差
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-GM2-06 · GoPro Camera Battery Life 支持页](https://community.gopro.com/s/article/gopro-camera-battery-life?language=en_US)；定位：页面读取失败：Loading / CSS Error

### GM2-008

**存储｜已按记录日期核验**

MAX2需另购microSD；手册要求A2与V30或更高等级，容量最高1TB。

- 条件：使用官方推荐品牌型号并先备份再格式化
- 边界：不要因相机支持8K就省略存储卡等级核对
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-GM2-02 · MAX2 User Manual REVA](https://static.gopro.com/assets/blta2b8522e5372af40/blte32e2783ff44e36a/68c27e50d9e51a0e3481b803/MAX2_UM_en-US_REVA.pdf)；定位：印刷页8 SD CARDS

### GM2-009

**防水与水下成像｜已按记录日期核验**

MAX2锁紧舱门时防水5米；手册明确因图像畸变不适合水下使用。

- 条件：密封干净且舱门锁紧
- 边界：可在水面场景使用不等于可获得合格的水下全景成像
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-GM2-02 · MAX2 User Manual REVA](https://static.gopro.com/assets/blta2b8522e5372af40/blte32e2783ff44e36a/68c27e50d9e51a0e3481b803/MAX2_UM_en-US_REVA.pdf)；定位：印刷页45 Using Your GoPro Around Water

### GM2-010

**镜片维护与安装｜已按记录日期核验**

MAX2镜头可手动旋转更换，无需工具或校准；安装方式包括1/4-20螺纹、GoPro折叠接头和兼容磁吸附件。

- 条件：购买MAX2适配镜片和对应安装附件
- 边界：可换镜不代表机身所有损伤可自行修复
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-GM2-04 · GoPro 2025年9月23日新品发布公告](https://investor.gopro.com/press-releases/press-release-details/2025/GoPro-Announces-Three-New-Products---MAX2-360-Camera-with-True-8K-Resolution-and-Twist-and-Go-Replaceable-Lenses-LIT-HERO-Miniature-4K-Lifestyle-Camera-with-Built-In-Light-for-Whatever-Whenever-Capture-and-Fluid-Pro-AI-Gimbal-for-Stabilizing-GoPros-P/default.aspx)；定位：Twist-and-Go Replaceable Lenses
- 来源：[S-GM2-01 · GoPro MAX2 产品页](https://gopro.com/en/us/shop/cameras/learn/max2/CHDHZ-311-master.html)；定位：FAQs / Why is MAX2 the best 360 camera for action

### GM2-011

**手机后期｜已按记录日期核验**

Quik支持关键帧重取景、对象跟踪和MotionFrame；订阅用户可使用云端素材编辑。

- 条件：关键帧设定时间点的视场，软件生成中间过渡；云端功能受订阅及地区可用性约束
- 边界：拍摄POV/Selfie模式仍保留全景角度，不能混同单镜头拍摄
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-GM2-01 · GoPro MAX2 产品页](https://gopro.com/en/us/shop/cameras/learn/max2/CHDHZ-311-master.html)；定位：KEYFRAMES / OBJECT TRACKING / FREESTYLE YOUR EDITS
- 来源：[S-GM2-04 · GoPro 2025年9月23日新品发布公告](https://investor.gopro.com/press-releases/press-release-details/2025/GoPro-Announces-Three-New-Products---MAX2-360-Camera-with-True-8K-Resolution-and-Twist-and-Go-Replaceable-Lenses-LIT-HERO-Miniature-4K-Lifestyle-Camera-with-Built-In-Light-for-Whatever-Whenever-Capture-and-Fluid-Pro-AI-Gimbal-for-Stabilizing-GoPros-P/default.aspx)；定位：Cloud-Based Editing

### GM2-012

**电脑后期｜已按记录日期核验**

GoPro Player可重取景、修剪和批量导出全景内容；MAX2手册将其列为电脑播放工具。

- 条件：电脑需满足HEVC解码和所用软件系统要求
- 边界：本次未验证所有MAX2输出格式的逐档上限；不把第三方插件旧发布计划当作已上线
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-GM2-05 · GoPro Player](https://gopro.com/en/us/info/gopro-player)；定位：Turn 360 Footage Into Cinematic Gold / Batch Export / Technical Specs
- 来源：[S-GM2-02 · MAX2 User Manual REVA](https://static.gopro.com/assets/blta2b8522e5372af40/blte32e2783ff44e36a/68c27e50d9e51a0e3481b803/MAX2_UM_en-US_REVA.pdf)；定位：印刷页82 Troubleshooting

### GM2-013

**历史费用｜已按记录日期核验**

2025-09-23美国官方公告列MAX2相机预售价499.99美元，2025-09-30起发货。

- 条件：历史单相机报价，USD；未包含另售场景套装、存储卡或订阅
- 边界：非2026-09-06当前成交价，非大陆价格；不能与竞品现价直接作价格优劣结论
- 地区：美国；历史报价日2025-09-23；核验：2026-09-06
- 来源：[S-GM2-04 · GoPro 2025年9月23日新品发布公告](https://investor.gopro.com/press-releases/press-release-details/2025/GoPro-Announces-Three-New-Products---MAX2-360-Camera-with-True-8K-Resolution-and-Twist-and-Go-Replaceable-Lenses-LIT-HERO-Miniature-4K-Lifestyle-Camera-with-Built-In-Light-for-Whatever-Whenever-Capture-and-Fluid-Pro-AI-Gimbal-for-Stabilizing-GoPros-P/default.aspx)；定位：MAX2 preorder price

### GM2-014

**外接供电｜已按记录日期核验**

MAX2可通过USB-C外接电源录制，但录制时电池不充电；普通舱门打开时不防水。

- 条件：使用适配外接电源和线缆
- 边界：专用USB直通门仅描述为weather resistant，不等于恢复5米潜水能力
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-GM2-02 · MAX2 User Manual REVA](https://static.gopro.com/assets/blta2b8522e5372af40/blte32e2783ff44e36a/68c27e50d9e51a0e3481b803/MAX2_UM_en-US_REVA.pdf)；定位：印刷页76 Recording When Plugged Into a Power Source

### GM2-015

**隐形自拍杆｜已按记录日期核验**

MAX2隐形杆拍摄要求兼容延长杆经底部1/4-20安装，长度至少36厘米并从相机底部直线伸出。

- 条件：使用360拍摄模式；杆与相机底部轴线保持直线
- 边界：单镜头模式或弯折偏轴安装不能套用隐形效果承诺
- 地区：全球英文资料；大陆地区服务/销售条件另核；核验：2026-09-06
- 来源：[S-GM2-02 · MAX2 User Manual REVA](https://static.gopro.com/assets/blta2b8522e5372af40/blte32e2783ff44e36a/68c27e50d9e51a0e3481b803/MAX2_UM_en-US_REVA.pdf)；定位：印刷页19 INVISIBLE 360 POLE SHOTS
