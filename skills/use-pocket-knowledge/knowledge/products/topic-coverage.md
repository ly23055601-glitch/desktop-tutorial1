# Pocket4 / Pocket4P 使用过程主题覆盖表

核对日期：2026-09-06。原流程基线依据[事实库](facts.jsonl)和[来源台账](../sources/official.jsonl)整理，机器可读版本见[topic-coverage.json](topic-coverage.json)。本次补核实际读取了4P中国攻略3.1两张静态操作图。

当前事实表（2026-09-14）为 **129条事实：127已核、2待核，24个官方来源**。主库4/4P共**82条唯一事实：80已核、2待核**；Pocket4适用39条，Pocket4P适用57条，两者共享14条，所以39+57−14=82。此前2026-09-06基线118条（116已核、2待核）仅作历史对照。

**已覆盖**只表示下面这个限定问题可依据所列事实回答；**部分**表示流程主题仍有重要空缺；**缺口**表示尚未有入库证据，不能反写成产品不支持。本轮12个流程主题在两款机型上均为“部分”，没有把零散功能条目算成整章完成。

引用前读取事实的`conditions`和来源的地区/语言。英国FAQ没有给出可比较的固件版本，不自动代表中国大陆目标设备。待核事实只能提示冲突，不能作为肯定能力；同一事实可在多个流程入口出现，但只计算一次。

## 覆盖概览

| 型号 | 已核 / 待核 | 已覆盖的限定问题 | 尚待回答的具体问题 | 流程主题 |
|---|---:|---:|---:|---|
| Pocket4 | 39 / 0 | 30 | 37 | 12项均部分覆盖 |
| Pocket4P | 55 / 2 | 43 | 44 | 12项均部分覆盖 |

问题数只是索引入口，不表示相互独立事实数或完成率。当前82条主款唯一事实均已挂到至少一个主题；2026-09-07及2026-09-10新增事实与现行计数见下文补充及JSON索引。

## Pocket4

### 1. 准备｜部分

- **已覆盖**：机身可用存储多少，能否扩展？ → `PKF-P4-005`
- **已覆盖**：旧代手机转接头能否沿用，标准套装是否包含补光灯？ → `PKF-S-002`、`PKF-P4-006`
- **待核事实**：无已登记条目。
- **缺口问题**：首次激活的手机要求、完整步骤和无网限制是什么？；充电器协议、充电时长及测试条件是什么，拍摄时如何供电？；按目标码率怎样选卡，推荐卡型号与格式化前检查是什么？
- **对应来源**：[DJI-P4-GUIDE](https://repair.dji.com/help/content?customId=01700043653&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-S-CONNECT](https://repair.dji.com/help/content?customId=01700009275&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)

### 2. 开关及按键｜部分

- **已覆盖**：取出后怎样开机，旋屏即拍需要什么设置？ → `PKF-P4-001`、`PKF-P4-017`
- **已覆盖**：变焦键单击、双击、再次按下有什么区别？ → `PKF-P4-007`
- **待核事实**：无已登记条目。
- **缺口问题**：拍摄中和非拍摄中如何关机，旋屏方向与横竖锁定怎样影响停录？；5D摇杆与自定义键各按法、默认动作、重新映射的完整操作是什么？
- **对应来源**：[DJI-P4-GUIDE](https://repair.dji.com/help/content?customId=01700043653&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-P4-MANUAL](https://dl.djicdn.com/downloads/DJI_Osmo_Pocket_4/UM/v1.0/Osmo_Pocket_4_User_Manual_en.pdf)

### 3. 架设和构图｜部分

- **已覆盖**：竖拍裁切与横向握持拍4K竖屏如何区别？ → `PKF-S-016`
- **已覆盖**：旋转运镜可做什么，为什么不能和跟随同时用？ → `PKF-P4-002`、`PKF-P4-008`
- **已覆盖**：近物展示对焦和轨迹延时对焦有什么模式边界？ → `PKF-S-012`、`PKF-S-013`
- **待核事实**：无已登记条目。
- **缺口问题**：三脚架、拓展件和续航手柄如何安装并检查机位？；跟随、俯仰锁定、FPV等云台模式的完整选择路径和适用动作是什么？；曝光、白平衡、对焦和构图参考线怎样按场景设置？
- **对应来源**：[DJI-S-VERTICAL](https://repair.dji.com/help/content?customId=01700007470&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-P4-GUIDE](https://repair.dji.com/help/content?customId=01700043653&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-P4-MANUAL](https://dl.djicdn.com/downloads/DJI_Osmo_Pocket_4/UM/v1.0/Osmo_Pocket_4_User_Manual_en.pdf)、[DJI-S-FOCUS](https://repair.dji.com/help/content?customId=01700009262&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)

### 4. 跟随｜部分

- **已覆盖**：人脸追焦与云台跟随有什么区别，黄框消失代表失焦吗？ → `PKF-S-010`、`PKF-S-011`
- **已覆盖**：哪些模式不支持基础跟随？ → `PKF-P4-008`
- **已覆盖**：手势控制怎样保持有效操作距离？ → `PKF-P4-016`
- **待核事实**：无已登记条目。
- **缺口问题**：基础跟随如何选目标、退出、重新选取，支持对象与遮挡恢复规则是什么？；主角登记、优先跟随、多人跟随的设置与上限分别是什么？；不同倍率、距离、光照下的跟随限制和固件差异是什么？
- **对应来源**：[DJI-S-FOCUS](https://repair.dji.com/help/content?customId=01700009262&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-P4-MANUAL](https://dl.djicdn.com/downloads/DJI_Osmo_Pocket_4/UM/v1.0/Osmo_Pocket_4_User_Manual_en.pdf)

### 5. 视频、照片、慢动作与夜间｜部分

- **已覆盖**：Live Photo与视频自动低光增强对应哪条已读版本记录？ → `PKF-P4-014`、`PKF-P4-015`
- **已覆盖**：哪些风格功能互斥，竖拍和轨迹延时有哪些已知边界？ → `PKF-P4-003`、`PKF-S-012`、`PKF-S-016`
- **待核事实**：无已登记条目。
- **缺口问题**：照片、普通视频、慢动作、低光和延时各自的分辨率、帧率、倍率完整矩阵是什么？；低光模式与自动低光增强有什么操作区别，何时开启/关闭？；夜景运动模糊、降噪和曝光取舍如何通过实际设置与测试回答？；Live Photo捕捉前后时长、导出限制与当前固件支持范围是什么？
- **对应来源**：[DJI-P4-RN](https://dl.djicdn.com/downloads/DJI_Osmo_Pocket_4/RN/DJI_Osmo_Pocket_4_Release_Notes_en.pdf)、[DJI-P4-GUIDE](https://repair.dji.com/help/content?customId=01700043653&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-S-FOCUS](https://repair.dji.com/help/content?customId=01700009262&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-S-VERTICAL](https://repair.dji.com/help/content?customId=01700007470&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)

### 6. 收音｜部分

- **已覆盖**：相机可同时接几台兼容无线发射器？ → `PKF-P4-004`
- **已覆盖**：音频备份保存在哪里，哪些输出/拍摄模式不支持？ → `PKF-P4-009`
- **已覆盖**：网络摄像头下怎样用Mic2蓝牙收音？ → `PKF-S-017`
- **待核事实**：无已登记条目。
- **缺口问题**：当前具体发射器兼容表、对频步骤、断连提示与重连方法是什么？；内置麦指向、增益、风噪处理、声道分配如何设置？；有线外接麦、无线双发与发射器自身内录的限制怎样分别确认？
- **对应来源**：[DJI-P4-GUIDE](https://repair.dji.com/help/content?customId=01700043653&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-P4-MANUAL](https://dl.djicdn.com/downloads/DJI_Osmo_Pocket_4/UM/v1.0/Osmo_Pocket_4_User_Manual_en.pdf)、[DJI-S-WEBCAM](https://repair.dji.com/help/content?customId=zh-cn03400006962&lang=zh-CN&re=CN&spaceId=34)

### 7. 配件｜部分

- **已覆盖**：补光灯套装边界、增广镜全景限制和旧转接头兼容边界是什么？ → `PKF-P4-006`、`PKF-P4-012`、`PKF-S-002`
- **已覆盖**：续航手柄随相机升级时有什么操作限制？ → `PKF-P4-013`
- **待核事实**：无已登记条目。
- **缺口问题**：补光灯亮度/色温、滤镜与增广镜安装拆卸步骤是什么？；续航手柄的供电优先级、增时测试条件与热插拔限制是什么？；FrameTap是否兼容Pocket4，以及各遥控功能是否可用？；不同支架、保护件与云台活动范围如何核对？
- **对应来源**：[DJI-P4-GUIDE](https://repair.dji.com/help/content?customId=01700043653&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-P4-MANUAL](https://dl.djicdn.com/downloads/DJI_Osmo_Pocket_4/UM/v1.0/Osmo_Pocket_4_User_Manual_en.pdf)、[DJI-S-CONNECT](https://repair.dji.com/help/content?customId=01700009275&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)

### 8. 传输｜部分

- **已覆盖**：手机转存有哪些路径，OTG依赖哪些手机与线材条件？ → `PKF-P4-010`、`PKF-S-005`、`PKF-S-006`
- **已覆盖**：电脑文件传输与继续拍摄能否同时进行？ → `PKF-P4-011`
- **已覆盖**：连接失败、退出OTG或出现格式化提示，先查什么？ → `PKF-S-003`、`PKF-S-007`、`PKF-S-008`
- **待核事实**：无已登记条目。
- **缺口问题**：Mimo无线传输速率、机身有线速率及实际测试条件是什么？；素材分段、单文件限制、批量下载和断点恢复规则是什么？；剪辑前如何核对原始文件、备份完整性及安全拔线？
- **对应来源**：[DJI-P4-MANUAL](https://dl.djicdn.com/downloads/DJI_Osmo_Pocket_4/UM/v1.0/Osmo_Pocket_4_User_Manual_en.pdf)、[DJI-S-OTG](https://repair.dji.com/help/content?customId=zh-cn03400007307&lang=zh-CN&re=CN&spaceId=34)、[DJI-S-GIMBAL](https://repair.dji.com/help/content?customId=01700011802&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-S-EXPORT](https://repair.dji.com/help/content?customId=01700009294&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)

### 9. 剪辑色彩｜部分

- **已覆盖**：Pocket4的D-Log需要哪一型号和配置的还原LUT？ → `PKF-S-014`
- **已覆盖**：机内美肤与胶片影调能否叠加，Live Photo按已读版本如何导出？ → `PKF-P4-003`、`PKF-P4-014`
- **待核事实**：无已登记条目。
- **缺口问题**：LUT在Mimo/剪辑软件怎样导入、预览和导出，适用版本是什么？；D-Log各拍摄规格的支持矩阵、监看还原与文件实际色彩有何区别？；手机剪辑高规格素材的兼容、代理、导出色彩和HDR/SDR转换如何验证？
- **对应来源**：[DJI-S-LUT](https://repair.dji.com/help/content?customId=01700007105&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-P4-GUIDE](https://repair.dji.com/help/content?customId=01700043653&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-P4-RN](https://dl.djicdn.com/downloads/DJI_Osmo_Pocket_4/RN/DJI_Osmo_Pocket_4_Release_Notes_en.pdf)

### 10. 收纳维护｜部分

- **已覆盖**：云台有阻挡或受损迹象时，检查与清理有什么前提？ → `PKF-S-004`
- **已覆盖**：设备要求格式化但仍能回放时，素材应怎样先保全？ → `PKF-S-008`
- **待核事实**：无已登记条目。
- **缺口问题**：关机、取下灯/镜片、安装云台夹和装袋的完整顺序是什么？；镜片/触点/卡槽怎样清洁，防水防尘和温度范围是什么？；长期存放电量、充放电维护和运输保护要求是什么？
- **对应来源**：[DJI-S-GIMBAL](https://repair.dji.com/help/content?customId=01700011802&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-S-EXPORT](https://repair.dji.com/help/content?customId=01700009294&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)

### 11. 故障｜部分

- **已覆盖**：云台保护或退出OTG后不动，按什么线索排查？ → `PKF-S-003`、`PKF-S-004`
- **已覆盖**：iPhone15提示耗电大、电脑不识别、要求格式化时如何区分？ → `PKF-S-006`、`PKF-S-007`、`PKF-S-008`
- **已覆盖**：登记主角黄框消失是否意味着追焦停止？ → `PKF-S-011`
- **待核事实**：无已登记条目。
- **缺口问题**：黑屏、卡顿、发热停录、无法开机和充电异常分别如何排查？；无线连接、麦克风、录音缺失和录像中断怎样交叉定位？；哪些情况应停用送检，需要收集什么日志和版本证据？
- **对应来源**：[DJI-S-GIMBAL](https://repair.dji.com/help/content?customId=01700011802&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-S-OTG](https://repair.dji.com/help/content?customId=zh-cn03400007307&lang=zh-CN&re=CN&spaceId=34)、[DJI-S-EXPORT](https://repair.dji.com/help/content?customId=01700009294&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-S-FOCUS](https://repair.dji.com/help/content?customId=01700009262&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)

### 12. 固件｜部分

- **已覆盖**：通过什么应用升级，开始前电量条件是什么？ → `PKF-S-009`
- **已覆盖**：已装续航手柄升级时能否拆下？ → `PKF-P4-013`
- **已覆盖**：已读v01.01.32.02版本增加了哪些已入库功能？ → `PKF-P4-014`、`PKF-P4-015`
- **待核事实**：无已登记条目。
- **缺口问题**：本地区当前最新相机/Mimo版本及版本历史是什么？；升级失败、升级中断、手柄单独失败的恢复步骤是什么？；新旧版本中菜单与功能限制的变化如何追踪？
- **对应来源**：[DJI-S-FIRMWARE](https://repair.dji.com/help/content?customId=01700006836&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-P4-MANUAL](https://dl.djicdn.com/downloads/DJI_Osmo_Pocket_4/UM/v1.0/Osmo_Pocket_4_User_Manual_en.pdf)、[DJI-P4-RN](https://dl.djicdn.com/downloads/DJI_Osmo_Pocket_4/RN/DJI_Osmo_Pocket_4_Release_Notes_en.pdf)

## Pocket4P

### 1. 准备｜部分

- **已覆盖**：内置存储多少，容量时长和电池续航为何要分开看？ → `PKF-P4P-003`、`PKF-P4P-012`
- **已覆盖**：准备连接手机时哪些旧配件和并行连接不可沿用？ → `PKF-S-002`、`PKF-P4P-014`
- **已覆盖**：首次激活怎样进入Mimo连接流程，FrameTap应先怎样处理？ → `PKF-P4P-036`
- **待核事实**：`PKF-P4P-015`（续航手柄延长分钟数待核）
- **缺口问题**：首次激活支持哪些手机和Mimo版本，联网要求、未激活限制与失败恢复规则是什么？；充电/边拍边供电、标准与Vlog套装的本地区清单及测试条件是什么？；拍摄目标对应的推荐存储卡、预留空间和准备检查是什么？
- **对应来源**：[DJI-P4P-GUIDE](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)、[DJI-S-CONNECT](https://repair.dji.com/help/content?customId=01700009275&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)

### 2. 开关及按键｜部分

- **已覆盖**：左实体键在不同当前倍率下怎样单击、双击与长按？ → `PKF-P4P-020`
- **已覆盖**：右自定义键长按和快捷映射分别做什么？ → `PKF-P4P-021`
- **已覆盖**：遥控器屏幕如何切换摇杆用途和回放？ → `PKF-P4P-027`
- **已覆盖**：拍摄键如何开机、开拍停录和在非拍摄状态关机？ → `PKF-P4P-031`
- **已覆盖**：机身摇杆如何回中和翻转朝向，C键默认动作怎样查？ → `PKF-P4P-035`、`PKF-P4P-021`
- **待核事实**：无已登记条目。
- **缺口问题**：不同固件的可选改键动作、变焦速度菜单和按键组合限制如何确认？；旋屏即拍、录像中旋屏和长按摇杆的两种锁定方式如何配置，分别怎样影响当前拍摄？；FrameTap实体键、摇杆单击/双击/三击及快捷键如何操作？
- **对应来源**：[DJI-P4P-STORE-GB](https://store.dji.com/uk/product/osmo-pocket-4p-vlog-combo?set_region=GB&vid=241311)、[DJI-P4P-GUIDE](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)

### 3. 架设和构图｜部分

- **已覆盖**：两颗镜头的焦段与工作关系是什么，近拍对焦距离有何差别？ → `PKF-P4P-001`、`PKF-P4P-002`、`PKF-P4P-025`
- **已覆盖**：竖拍裁切和横向握持4K竖屏怎样区别？ → `PKF-S-016`
- **已覆盖**：机身怎样进入对焦设置，展示与轨迹延时如何区分？ → `PKF-P4P-016`、`PKF-S-012`、`PKF-S-013`
- **已覆盖**：离开机位时FrameTap怎样配对和调画面？ → `PKF-P4P-010`、`PKF-P4P-026`、`PKF-P4P-027`
- **已覆盖**：摇杆上下为什么有时调俯仰、有时变焦，怎样切换？ → `PKF-P4P-034`
- **待核事实**：无已登记条目。
- **缺口问题**：三脚架、扩展转接件、续航手柄的安装与站位检查是什么？；云台各模式、曝光/白平衡/对焦、构图辅助的完整操作是什么？；镜头切换边界、过渡效果与不同拍摄规格的关系是什么？
- **对应来源**：[DJI-P4P-GUIDE](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)、[DJI-P4P-STORE-GB](https://store.dji.com/uk/product/osmo-pocket-4p-vlog-combo?set_region=GB&vid=241311)、[DJI-S-VERTICAL](https://repair.dji.com/help/content?customId=01700007470&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-S-FOCUS](https://repair.dji.com/help/content?customId=01700009262&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)

### 4. 跟随｜部分

- **已覆盖**：主角跟随、多人居中、人脸追焦分别控制什么？ → `PKF-P4P-004`、`PKF-P4P-019`、`PKF-S-010`、`PKF-S-011`
- **已覆盖**：怎样用手势或FrameTap启动目标跟随？ → `PKF-P4P-005`、`PKF-P4P-010`
- **已覆盖**：可跟随哪些非人主体，哪些模式与倍率不能直接套用？ → `PKF-P4P-030`、`PKF-P4P-028`、`PKF-P4P-024`
- **已覆盖**：在屏幕上怎样选择智能跟随对象，怎样退出？ → `PKF-P4P-033`
- **待核事实**：无已登记条目。
- **缺口问题**：中国大陆目标固件的多人跟随上限与禁用变焦条件如何复核？；基础跟随在遮挡后怎样恢复，目标切换、登记主角与不同模式下的操作怎样衔接？；不同倍率、光照、距离的有效范围与宠物快速运动限制是什么？
- **对应来源**：[DJI-P4P-GUIDE](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)、[DJI-P4P-STORE-GB](https://store.dji.com/uk/product/osmo-pocket-4p-vlog-combo?set_region=GB&vid=241311)、[DJI-S-FOCUS](https://repair.dji.com/help/content?customId=01700009262&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)

### 5. 视频、照片、慢动作与夜间｜部分

- **已覆盖**：双镜头慢动作上限和12x禁用模式分别是什么？ → `PKF-P4P-023`、`PKF-P4P-024`
- **已覆盖**：D-Log2倍率与竖拍分辨率有哪些已知限制？ → `PKF-P4P-022`、`PKF-S-016`
- **已覆盖**：App美颜预览、补光灯和展示对焦有哪些使用前提？ → `PKF-P4P-006`、`PKF-P4P-017`、`PKF-S-013`
- **已覆盖**：录制前怎样选择模式并进入拍摄参数？ → `PKF-P4P-032`
- **待核事实**：`PKF-P4P-007`（胶片影调慢动作支持范围存在地区来源冲突）
- **缺口问题**：各镜头在照片/视频/慢动作/低光/延时下的分辨率、帧率、色彩、倍率完整矩阵是什么？；低光模式与自动低光增强的实际入口、自动切换和禁用组合是什么？；Live Photo的拍摄、回放、导出限制与固件条件是什么？；胶片影调慢动作支持范围的CN/GB差异对应什么固件？；开始录制后，1x与3x互切在各分辨率、帧率、色彩和拍摄模式下分别是否可用，是否需要先停录？英国FAQ的一般录制说明未提供完整组合矩阵。；正在录制时能否由普通视频切入慢动作、或由慢动作切回普通视频？已读慢动作操作指南只给出录制前选模式和参数的顺序，尚不能回答录制中切换规则。
- **对应来源**：[DJI-P4P-STORE-GB](https://store.dji.com/uk/product/osmo-pocket-4p-vlog-combo?set_region=GB&vid=241311)、[DJI-S-VERTICAL](https://repair.dji.com/help/content?customId=01700007470&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-P4P-GUIDE](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)、[DJI-S-FOCUS](https://repair.dji.com/help/content?customId=01700009262&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)

### 6. 收音｜部分

- **已覆盖**：哪些兼容发射器可以双发直连，怎样配对和确认连接？ → `PKF-P4P-009`
- **已覆盖**：网络摄像头如何使用Mic2蓝牙收音？ → `PKF-S-017`
- **待核事实**：无已登记条目。
- **缺口问题**：4P内置麦音频备份的AAC/附加音轨、开启路径与禁用模式是什么？；双发、四声道、内置环境声和播放默认音轨如何分配？；内置麦指向、增益、风噪、降噪和有线外接的操作与限制是什么？；发射器自身内录、相机备份、掉线后重连的功能条件怎样分别确认？
- **对应来源**：[DJI-P4P-GUIDE](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)、[DJI-S-WEBCAM](https://repair.dji.com/help/content?customId=zh-cn03400006962&lang=zh-CN&re=CN&spaceId=34)

### 7. 配件｜部分

- **已覆盖**：滤镜怎样旋转锁紧，补光灯怎样安装并调挡？ → `PKF-P4P-011`、`PKF-P4P-017`
- **已覆盖**：FrameTap怎样配对、监看、回放并安排遥控距离？ → `PKF-P4P-010`、`PKF-P4P-026`、`PKF-P4P-027`
- **已覆盖**：网络摄像头时FrameTap能否控制云台，Mimo能否同时连？ → `PKF-P4P-029`、`PKF-P4P-014`
- **已覆盖**：旧代手机转接头和当前兼容无线麦应怎样分别判断？ → `PKF-S-002`、`PKF-P4P-009`
- **待核事实**：`PKF-P4P-015`（续航手柄延长分钟数待核）
- **缺口问题**：续航手柄增时为什么有两个数字，完整测试和热插拔条件是什么？；FrameTap实体键、升级、续航、充电和文件传输能力如何确认？；配件叠加、非官方支架、保护件与云台活动范围有什么限制？
- **对应来源**：[DJI-P4P-GUIDE](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)、[DJI-P4P-STORE-GB](https://store.dji.com/uk/product/osmo-pocket-4p-vlog-combo?set_region=GB&vid=241311)、[DJI-S-WEBCAM](https://repair.dji.com/help/content?customId=zh-cn03400006962&lang=zh-CN&re=CN&spaceId=34)、[DJI-S-CONNECT](https://repair.dji.com/help/content?customId=01700009275&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)

### 8. 传输｜部分

- **已覆盖**：OTG连接手机依赖哪些设备、线材和连接顺序条件？ → `PKF-S-005`、`PKF-S-006`
- **已覆盖**：电脑不识别或出现格式化提示时，先检查和保存什么？ → `PKF-S-007`、`PKF-S-008`
- **已覆盖**：FrameTap回放、Mimo连接和OTG退出后的状态怎样区分？ → `PKF-P4P-027`、`PKF-P4P-014`、`PKF-S-003`
- **已覆盖**：拍完怎样在机身查看照片和视频？ → `PKF-P4P-037`
- **已覆盖**：导出到手机或电脑有哪些已核基本路径？ → `PKF-P4P-038`
- **待核事实**：无已登记条目。
- **缺口问题**：4P到Mimo、手机文件管理及电脑的完整导出/重连/安全移除步骤是什么？基本路径和机身回放已核，异常与批量操作尚未完整覆盖。；800MB/s和90MB/s各自测试条件、线材接口及手机要求是什么？；录制中是否能传输、单文件分段、批量下载和断点恢复规则是什么？；FrameTap监看是否占用哪些无线资源，是否支持其他传输路径并行？
- **对应来源**：[DJI-S-OTG](https://repair.dji.com/help/content?customId=zh-cn03400007307&lang=zh-CN&re=CN&spaceId=34)、[DJI-S-EXPORT](https://repair.dji.com/help/content?customId=01700009294&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-P4P-STORE-GB](https://store.dji.com/uk/product/osmo-pocket-4p-vlog-combo?set_region=GB&vid=241311)、[DJI-S-CONNECT](https://repair.dji.com/help/content?customId=01700009275&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-S-GIMBAL](https://repair.dji.com/help/content?customId=01700011802&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-P4P-GUIDE](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)

### 9. 剪辑色彩｜部分

- **已覆盖**：机身哪里设D-Log2，它有哪些已核倍率条件？ → `PKF-P4P-018`、`PKF-P4P-022`
- **已覆盖**：D-Log和D-Log2对应哪些本型号LUT？ → `PKF-S-015`
- **已覆盖**：App美颜怎样预览，机内美肤和胶片影调能否并用？ → `PKF-P4P-006`、`PKF-P4P-008`
- **待核事实**：`PKF-P4P-007`（胶片影调慢动作支持范围存在地区来源冲突）
- **缺口问题**：两种Log的完整帧率/镜头/模式矩阵及监看还原开关是什么？；LUT在Mimo与其他软件如何导入、管理和正确导出？；胶片影调在慢动作的本地区固件支持范围是什么？；手机剪辑高规格、音轨选择、色彩和HDR/SDR转换有哪些兼容限制？；Pocket4P素材添加产品型号水印需要哪个Mimo版本、手机系统和机身固件？已读水印攻略图片的机型说明截至2025-09-05，未列Pocket4P，不能据此确认现版本兼容性。；部分素材不能加水印时，原始相机视频、已剪辑再导出视频、照片/截图/Live Photo及第三方导入素材各有什么限制？需区分“水印设置/截图”和“贴纸”入口，再用原文件及当前App版本核对。
- **对应来源**：[DJI-P4P-GUIDE](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)、[DJI-P4P-STORE-GB](https://store.dji.com/uk/product/osmo-pocket-4p-vlog-combo?set_region=GB&vid=241311)、[DJI-S-LUT](https://repair.dji.com/help/content?customId=01700007105&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)

### 10. 收纳维护｜部分

- **已覆盖**：关机收纳前要先取下哪些配件？ → `PKF-P4P-013`
- **已覆盖**：镜片、云台清理和受损检查有什么前提？ → `PKF-P4P-011`、`PKF-S-004`
- **已覆盖**：存储异常时为何应先保全可回放素材？ → `PKF-S-008`
- **待核事实**：无已登记条目。
- **缺口问题**：保护夹/包袋的正确安装、长期存放电量和运输要求是什么？；防水防尘、温度、湿气与高频振动的实际限制是什么？；机身、镜头、触点和卡槽完整维护方法是什么？
- **对应来源**：[DJI-P4P-GUIDE](https://repair.dji.com/help/content?customId=01700043704&lang=zh-CN&paperDocType=FAQ&re=CN&spaceId=17)、[DJI-S-GIMBAL](https://repair.dji.com/help/content?customId=01700011802&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-S-EXPORT](https://repair.dji.com/help/content?customId=01700009294&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)

### 11. 故障｜部分

- **已覆盖**：Mimo搜不到相机时，FrameTap的状态应怎样处理？ → `PKF-P4P-014`
- **已覆盖**：云台保护、OTG退出和黄框消失应怎样分别判断？ → `PKF-S-003`、`PKF-S-004`、`PKF-S-011`
- **已覆盖**：iPhone15、电脑不识别和存储格式化提示有何已核排查项？ → `PKF-S-006`、`PKF-S-007`、`PKF-S-008`
- **待核事实**：无已登记条目。
- **缺口问题**：黑屏、发热停录、自动关机、充电和存储卡异常完整排查流程是什么？；双镜头切换/合焦异常、跟随丢失、FrameTap断连怎样定位？；音轨缺失、麦克风无声、升级失败需要哪些交叉测试和日志？
- **对应来源**：[DJI-S-CONNECT](https://repair.dji.com/help/content?customId=01700009275&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-S-GIMBAL](https://repair.dji.com/help/content?customId=01700011802&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-S-FOCUS](https://repair.dji.com/help/content?customId=01700009262&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-S-OTG](https://repair.dji.com/help/content?customId=zh-cn03400007307&lang=zh-CN&re=CN&spaceId=34)、[DJI-S-EXPORT](https://repair.dji.com/help/content?customId=01700009294&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)

### 12. 固件｜部分

- **已覆盖**：相机通过什么应用升级，升级前电量要求是什么？ → `PKF-S-009`
- **已覆盖**：连接Mimo升级前应怎样处理FrameTap连接？ → `PKF-P4P-014`
- **待核事实**：无已登记条目。
- **缺口问题**：4P完整用户手册、当前固件号和可读版本历史在哪里？；CN/GB页面差异是否来自地区、固件或文档更新时间？；FrameTap、相机、无线麦各自的升级顺序、版本匹配和失败恢复是什么？
- **对应来源**：[DJI-S-FIRMWARE](https://repair.dji.com/help/content?customId=01700006836&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)、[DJI-S-CONNECT](https://repair.dji.com/help/content?customId=01700009275&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)

## 数量与最后新增条目核对

- `PKF-P4P-031`至`038`补入首次激活、机身按键、选模式、跟随进入退出、摇杆构图、回放及导出路径；`020/021`补入CN实体按键图依据。
- 主库唯一82条、Pocket4适用39条、Pocket4P适用57条，与当前JSONL逐条计数一致。
- `PKF-P4P-007`（胶片影调慢动作范围）和`PKF-P4P-015`（手柄增时数字）仍是仅有的两条pending。
- 旧代事实不纳入本表。共享培训写作使用前复核当前官方来源，将证据登记为`product`来源并绑定`product_fact`断言；只有LH13真实材料专项核验或旧稿复核，才按注册表登记claim并绑定`product_facts`原句。不能把LH13的claim门槛套到一般共享培训。

## 两项具体问题的有限补核（2026-09-06）

**录制中切镜头或切普通/慢动作。** `PKF-P4P-002/019/020/022/023/024`已有镜头选择、变焦键和若干模式限制。实际读到的[英国商品FAQ](https://store.dji.com/uk/product/osmo-pocket-4p-vlog-combo?set_region=GB&vid=241311)描述录制时按倍率选择对应镜头，但没有给各分辨率、帧率、色彩和模式的完整允许矩阵，也没有可比较的固件版本。[中国慢动作操作指南](https://repair.dji.com/help/content?customId=01700006756&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)的4P段落只交代先选模式和参数、再开始录制；这不足以回答正在录制时能否切换普通视频与慢动作。两项均保留为上述精确缺口。

**Mimo部分素材不能加水印。** 已实际读取[官方水印攻略](https://repair.dji.com/help/content?customId=01700043604&documentType=&lang=zh-CN&paperDocType=ARTICLE&re=CN&spaceId=17)及两张操作图。图片区分“水印设置/截图”和“贴纸”入口，但适用机型和发布范围注明截至2025-09-05，未列4P，不能直接解释4P当前个案。待核时应保留原素材与是否二次导出、视频/照片/Live类型、使用入口、手机系统、Mimo和固件版本。没有把作者的问题升级为产品事实。

这两项补读本身只记录问题边界，未新增确定事实；后续中国攻略静态图操作补核另见下节，当前计数以页首为准。补读页面与图片定位见JSON的`bounded_followup_checks`，与支持已核事实的`source_reference_index`分开。

## 中国攻略静态操作图补核（2026-09-06）

本次实际读到3.1实体按键与拍摄界面两图，图文件、原始CDN地址和SHA-256保存在来源`DJI-P4P-GUIDE.image_evidence`。新增事实没有把其他未看的视频或动图算作已读，也没有把其他官方指引中的Pocket2段落挪到4P。

仍保留4P音频备份、完整模式兼容矩阵、录制中切模式、水印个案、FrameTap全部按键与传输并行规则等缺口。回放不等于导出；手机或电脑传输的基本路径不等于已掌握完整剪辑教程。

## 2026-09-07卖点学习补充

2026-09-07基线79条主款已核事实、2条待核事实；官方来源24个。新增10条事实已进入JSON的对应流程主题。此前问题清单是基线，不能用旧问题的“待核”覆盖下面已经明确的部分，也不能由单项补核认定整章完成。

- `PKF-P4-018`：一英寸成像与14挡动态范围条件，对应capture_modes；完整条件见[事实表](facts.jsonl)。
- `PKF-P4-019`：4K高帧率属于慢动作，对应capture_modes；完整条件见[事实表](facts.jsonl)。
- `PKF-P4-020`：普通视频D-Log及监看还原，对应editing_color；完整条件见[事实表](facts.jsonl)。
- `PKF-P4-021`：手势分别控制跟随和拍摄，对应tracking；完整条件见[事实表](facts.jsonl)。
- `PKF-P4-022`：选定主体后让云台跟随，对应tracking；完整条件见[事实表](facts.jsonl)。
- `PKF-P4P-039`：双镜头的成像基础各不相同，对应capture_modes；完整条件见[事实表](facts.jsonl)。
- `PKF-S-018`：三轴机械增稳减轻拍摄抖动，对应setup_framing；完整条件见[事实表](facts.jsonl)。
- `PKF-S-019`：普通视频可在机内调整美肤，对应editing_color；完整条件见[事实表](facts.jsonl)。
- `PKF-P4P-040`：三轴机械增稳减轻拍摄抖动，对应setup_framing；完整条件见[事实表](facts.jsonl)。
- `PKF-P4P-041`：普通视频可在机内调整美肤，对应editing_color；完整条件见[事实表](facts.jsonl)。

本轮产品来源重读范围和地区差异见[官方复核记录](../selling_points/current-official-review.json)，可用场景见[详细场景库](../use_cases/guide.md)。

## 2026-09-10研究触发复核

新增`PKF-P4P-042`：内置103GB按官方标准码率估算的存储时长与续航分开；不能替代128GB卡实测。另复核9条相关事实，只更新实际核验条目的日期。当前总数见[动态覆盖](../COVERAGE.md)，网友最新固件HDR说法仍待对应版本说明；详见[本批产品问题](../_provenance/project/outputs/social-comment-research/2026-09-10/op-pocket-7d-01/product-questions.jsonl)。
