# Osmo Mobile 8P 卖点

由 cards.jsonl 生成。角色匹配与价值均为编辑推演；来源核验日期见各事实，卡片编辑日期不等于官网核验日期。

## 选取目录

- [MOBILE-SELL-001｜站到画面里后查看手机取景并调整构图](#mobile-sell-001)
- [MOBILE-SELL-002｜在模块预览里指定要跟随的物品](#mobile-sell-002)
- [MOBILE-SELL-003｜人物站在镜头前时用手势启停跟随与拍摄](#mobile-sell-003)
- [MOBILE-SELL-004｜把预想的起止构图设成A/B运镜](#mobile-sell-004)
- [MOBILE-SELL-005｜兼容手机可保留原生相机的人物跟拍路径](#mobile-sell-005)
- [MOBILE-SELL-006｜用机械增稳承接手持移动镜头](#mobile-sell-006)
- [MOBILE-SELL-015｜水平连续转动，给环绕构图留出空间](#mobile-sell-015)
- [MOBILE-SELL-016｜内置延长杆与独立支腿，兼顾手持和固定取景](#mobile-sell-016)
- [MOBILE-SELL-017｜第五代手机夹的装夹与遮挡优化](#mobile-sell-017)
- [MOBILE-SELL-018｜按拍摄组合安排续航，并可给手机供电](#mobile-sell-018)

## 相关待核与冲突

下列项目不能被卖点中的通用说法覆盖；按实际手机、配件与软件检查是否相关。

- [MOBILE-8P-TRACKING-007](../products/osmo_mobile_8p.md#mobile-8p-tracking-007)｜`pending`｜FAQ在同一回答中概述手机投屏和模块跟随，未说明是否指同一前台相机路径；手册明确模块跟随和拍摄不在Mimo内使用。现有表述不构成可肯定并用的依据，也不认定为直接互斥的官方结论。
- [MOBILE-8P-AUDIO-003](../products/osmo_mobile_8p.md#mobile-8p-audio-003)｜`pending`｜模块2手册/规格与商城一代模块支持表述不能独立确认二代收音路径。
- [MOBILE-C8P-002](../compatibility/guide.md#mobile-c8p-002)｜`conflict`｜当前兼容表与FAQ/手册对同一型号结论相反。

<a id="mobile-sell-001"></a>
## MOBILE-SELL-001｜站到画面里后查看手机取景并调整构图

**能力概括**：FrameTap可遥控8P拍照录像、横竖屏切换及构图调整；兼容手机可按对应系统路径把手机屏幕画面投到FrameTap。

**具体用途**：先摆好自拍或口播机位，进入画面后用遥控器检查人物和背景的位置，再按这次需要调整；这里使用手机投屏画面，不借用模块预览来证明手机构图。

**可能价值（编辑推演）**：对经常为了确认站位而走回手机的人，可能减少来回检查、让开始讲述或自拍的动作更连贯；实际节省多少步骤未经测量。

**可匹配角色**：[独自旅行／看展者](../audiences/guide.md#mobile-aud-001)、[独自口播／课程录制者](../audiences/guide.md#mobile-aud-006)、[想拍自己、但不想在公共场合久架手机的人](../audiences/guide.md#mobile-aud-012)

**型号与路径**：8P的FrameTap整套遥控已核；不将手机投屏兼容列外推成Mobile 8整套联控。

**不应扩写为**：25米内所有手机都能稳定遥控拍摄。；模块预览就是手机最终构图。；任何App的变焦、快门和跟随均可远程操作。；手机投屏、Mimo拍摄和模块2跟随已经确认可以同时组合。；有遥控就不必确认摆放、校准或场地。

**事实及完整条件入口**（命中后须一并读取条件、限制、官方定位与日期）：

- [MOBILE-8P-CONTROLS-003](../products/osmo_mobile_8p.md#mobile-8p-controls-003)｜FrameTap远程控制｜`verified`｜核验 2026-09-06
- [MOBILE-8P-CONTROLS-004](../products/osmo_mobile_8p.md#mobile-8p-controls-004)｜FrameTap手机投屏｜`verified`｜核验 2026-09-06
- [MOBILE-8P-SOFTWARE-002](../products/osmo_mobile_8p.md#mobile-8p-software-002)｜V01.02.01.01固件｜`verified`｜核验 2026-09-06
- [MOBILE-8P-MAINTENANCE-002](../products/osmo_mobile_8p.md#mobile-8p-maintenance-002)｜内置三脚架｜`verified`｜核验 2026-09-06
- [MOBILE-C8P-009](../compatibility/guide.md#mobile-c8p-009)｜手机经DJI Mimo向FrameTap投屏｜`verified`｜核验 2026-09-06
- [MOBILE-C8P-010](../compatibility/guide.md#mobile-c8p-010)｜手机系统投屏到FrameTap｜`verified`｜核验 2026-09-06

<a id="mobile-sell-002"></a>
## MOBILE-SELL-002｜在模块预览里指定要跟随的物品

**能力概括**：模块2可将自身镜头画面传到FrameTap用于选目标；人物、猫狗、车辆以外的物体，须在追踪预览中手动框选触发跟随。

**具体用途**：展示一个轮廓清晰、会移动的物件时，先确认模块和手机都朝向它，再手动框选这个物件，让取景围绕这次要展示的对象展开。

**可能价值（编辑推演）**：当讲解重点是物件而非人脸时，可能更贴合展示对象的选择；效果取决于识别条件，不能据此证明手部和完整工序都会入镜。

**可匹配角色**：[小店店主／经营者](../audiences/guide.md#mobile-aud-008)、[手工／烹饪／维修过程记录者](../audiences/guide.md#mobile-aud-015)、[手机影像爱好者](../audiences/guide.md#mobile-aud-011)

**型号与路径**：8P模块2高级操作：触屏选目标和其他物体手动框选；与8更新后的人物、猫狗、车辆跟随分开。

**不应扩写为**：所有物品都会被自动识别。；对物品做人物手势即可触发跟随。；Mobile 8装上模块2就能获得相同触屏框物功能。；跟物品就一定能拍全双手、工具和操作步骤。；模块2的智能跟随设置可自动达到本库未记录的具体效果。

**事实及完整条件入口**（命中后须一并读取条件、限制、官方定位与日期）：

- [MOBILE-8P-CONTROLS-005](../products/osmo_mobile_8p.md#mobile-8p-controls-005)｜FrameTap模块投屏｜`verified`｜核验 2026-09-06
- [MOBILE-8P-TRACKING-002](../products/osmo_mobile_8p.md#mobile-8p-tracking-002)｜多功能追踪模块2｜`verified`｜核验 2026-09-06
- [MOBILE-8P-TRACKING-003](../products/osmo_mobile_8p.md#mobile-8p-tracking-003)｜多功能追踪模块2｜`verified`｜核验 2026-09-06
- [MOBILE-8P-TRACKING-004](../products/osmo_mobile_8p.md#mobile-8p-tracking-004)｜多功能追踪模块2物体跟随｜`verified`｜核验 2026-09-06
- [MOBILE-C8P-008](../compatibility/guide.md#mobile-c8p-008)｜模块2镜头投屏到FrameTap｜`verified`｜核验 2026-09-06

<a id="mobile-sell-003"></a>
## MOBILE-SELL-003｜人物站在镜头前时用手势启停跟随与拍摄

**能力概括**：模块2人物手势可用于启停跟随、调整构图及触发拍照录像，手势功能可自定义。

**具体用途**：独自录一段练习或讲解时，先摆好机位并检查活动范围，再在镜头前用已设置的手势开始或结束需要的动作。

**可能价值（编辑推演）**：对愿意先熟悉少量手势的人，可能把部分操作留在出镜位置完成；这是一种控制选择，不代表所有动作记录都需要跟随。

**可匹配角色**：[亲子日常记录者](../audiences/guide.md#mobile-aud-004)、[舞蹈／健身／技能练习者](../audiences/guide.md#mobile-aud-007)、[直播／远程教学演示者](../audiences/guide.md#mobile-aud-010)

**型号与路径**：8P模块2已核使用路径，不宣称手势为8P独有；不把人物手势推广给猫狗、车辆和其他物体。

**不应扩写为**：8米范围内随便做手势都有效。；做手势后必定完整保持全身入镜。；不配对手机也已保证能手势拍录。；人物手势可以控制宠物或车辆。

**事实及完整条件入口**（命中后须一并读取条件、限制、官方定位与日期）：

- [MOBILE-8P-TRACKING-002](../products/osmo_mobile_8p.md#mobile-8p-tracking-002)｜多功能追踪模块2｜`verified`｜核验 2026-09-06
- [MOBILE-8P-TRACKING-003](../products/osmo_mobile_8p.md#mobile-8p-tracking-003)｜多功能追踪模块2｜`verified`｜核验 2026-09-06
- [MOBILE-8P-TRACKING-005](../products/osmo_mobile_8p.md#mobile-8p-tracking-005)｜多功能追踪模块2手势｜`verified`｜核验 2026-09-06
- [MOBILE-8P-MAINTENANCE-002](../products/osmo_mobile_8p.md#mobile-8p-maintenance-002)｜内置三脚架｜`verified`｜核验 2026-09-06

<a id="mobile-sell-004"></a>
## MOBILE-SELL-004｜把预想的起止构图设成A/B运镜

**能力概括**：FrameTap创意拍摄可设置旋转、环绕和A/B轨迹；A/B模式在预设的两个位置之间移动。

**具体用途**：想把取景从陈列的一侧转到另一侧时，先设置起止位置及时间，再试拍比较这段转动是否符合表达节奏。

**可能价值（编辑推演）**：对喜欢主动试运镜的人，可能把注意力集中在起止构图和时长的调整上，也保留反复尝试的空间；不保证一次就得到理想镜头。

**可匹配角色**：[日常Vlog初学者](../audiences/guide.md#mobile-aud-002)、[手机影像爱好者](../audiences/guide.md#mobile-aud-011)

**型号与路径**：8P遥控器创意拍摄的已核操作；不能改写成Mobile 8已有同一套FrameTap A/B控制。

**不应扩写为**：A/B会让设备自己从房间一端走到另一端。；横滚、俯仰和平移都能无限旋转。；设好A/B就能复现任何空间路径或一次出片。；Mobile 8现已获得同一套FrameTap A/B能力。

**事实及完整条件入口**（命中后须一并读取条件、限制、官方定位与日期）：

- [MOBILE-8P-STABILIZATION-004](../products/osmo_mobile_8p.md#mobile-8p-stabilization-004)｜云台自动运镜｜`verified`｜核验 2026-09-06
- [MOBILE-8P-SOFTWARE-002](../products/osmo_mobile_8p.md#mobile-8p-software-002)｜V01.02.01.01固件｜`verified`｜核验 2026-09-06

<a id="mobile-sell-005"></a>
## MOBILE-SELL-005｜兼容手机可保留原生相机的人物跟拍路径

**能力概括**：8P可通过Apple DockKit或适配鸿蒙智能追焦，让兼容手机在原生相机及相应兼容App中进行人物跟拍。

**具体用途**：已经习惯某款受支持的原生相机或App时，按手机所属路径完成连接，用于人物在预定范围内走动的短段落。

**可能价值（编辑推演）**：对希望沿用熟悉拍摄界面的人，可能少一次更换拍摄App的适应过程；是否适合仍取决于需要的拍摄功能和具体手机。

**可匹配角色**：[亲子日常记录者](../audiences/guide.md#mobile-aud-004)、[独自口播／课程录制者](../audiences/guide.md#mobile-aud-006)、[总替家人朋友拍照的人](../audiences/guide.md#mobile-aud-003)

**型号与路径**：8P已核的共有方向；与8分别保留各自手机范围及配对条件，不作8P独占卖点。

**不应扩写为**：所有iPhone或华为手机都支持。；NFC连上就证明原生跟拍兼容。；原生人物跟拍还包括猫狗、车辆和任意物体。；iPhone16e已确定支持或已确定不支持。

**事实及完整条件入口**（命中后须一并读取条件、限制、官方定位与日期）：

- [MOBILE-8P-TRACKING-001](../products/osmo_mobile_8p.md#mobile-8p-tracking-001)｜手机原生跟拍｜`verified`｜核验 2026-09-06
- [MOBILE-C8P-001](../compatibility/guide.md#mobile-c8p-001)｜Apple DockKit原生人物跟拍｜`verified`｜核验 2026-09-06
- [MOBILE-C8P-003](../compatibility/guide.md#mobile-c8p-003)｜鸿蒙智能追焦｜`verified`｜核验 2026-09-06

<a id="mobile-sell-006"></a>
## MOBILE-SELL-006｜用机械增稳承接手持移动镜头

**能力概括**：8P通过三轴机械云台承托手机增稳，平移轴支持360°无限位旋转；普通手机装夹通常无需精确调平，但须检查对位与居中。

**具体用途**：拍从门口到窗边的空间介绍时，先规划移动方向、检查装夹，再让手机随手柄完成所需转向，并在重要细节前停下。

**可能价值（编辑推演）**：对于用连续镜头交代位置关系的人，机械增稳可能帮助管理手持转向；画面是否易理解还取决于路线、速度和讲解设计。

**可匹配角色**：[房产／装修现场讲解者](../audiences/guide.md#mobile-aud-009)、[日常Vlog初学者](../audiences/guide.md#mobile-aud-002)、[手机影像爱好者](../audiences/guide.md#mobile-aud-011)

**型号与路径**：8P的基础手机云台能力；8亦为三轴机械云台，本卡不建立8P独占或画质优于其他型号的结论。

**不应扩写为**：消除所有走路起伏。；装上就让手机拥有更高分辨率或夜景画质。；三轴都能无限旋转。；具备测距、空间测量或自动生成房屋平面图的能力。

**事实及完整条件入口**（命中后须一并读取条件、限制、官方定位与日期）：

- [MOBILE-8P-STABILIZATION-001](../products/osmo_mobile_8p.md#mobile-8p-stabilization-001)｜三轴电机｜`verified`｜核验 2026-09-06
- [MOBILE-8P-STABILIZATION-002](../products/osmo_mobile_8p.md#mobile-8p-stabilization-002)｜平移轴｜`verified`｜核验 2026-09-06
- [MOBILE-8P-STABILIZATION-005](../products/osmo_mobile_8p.md#mobile-8p-stabilization-005)｜手机夹及配重孔｜`verified`｜核验 2026-09-06
- [MOBILE-8P-COMPATIBILITY-001](../products/osmo_mobile_8p.md#mobile-8p-compatibility-001)｜磁吸手机夹5｜`verified`｜核验 2026-09-06

<a id="mobile-sell-015"></a>
## MOBILE-SELL-015｜水平连续转动，给环绕构图留出空间

**能力概括**：平移轴支持360°无限位旋转；不同跟随模式决定手机朝向如何响应手柄。

**具体用途**：围绕桌面物品、人物或展陈安排连续的水平运镜。

**可能价值（编辑推演）**：对想亲自掌握运镜节奏的人，可能减少在水平转动过程中处理结构限位的中断。

**可匹配角色**：[日常Vlog初学者](../audiences/guide.md#mobile-aud-002)、[房产／装修现场讲解者](../audiences/guide.md#mobile-aud-009)、[手机影像爱好者](../audiences/guide.md#mobile-aud-011)

**型号与路径**：8P机械平移范围；不是全轴无限位或全景相机功能。

**不应扩写为**：三轴都能无限转动。；转一圈就是360全景视频。；跟随主体永不丢失。

**事实及完整条件入口**（命中后须一并读取条件、限制、官方定位与日期）：

- [MOBILE-8P-STABILIZATION-002](../products/osmo_mobile_8p.md#mobile-8p-stabilization-002)｜平移轴｜`verified`｜核验 2026-09-06
- [MOBILE-8P-STABILIZATION-003](../products/osmo_mobile_8p.md#mobile-8p-stabilization-003)｜云台跟随模式｜`verified`｜核验 2026-09-06

<a id="mobile-sell-016"></a>
## MOBILE-SELL-016｜内置延长杆与独立支腿，兼顾手持和固定取景

**能力概括**：内置延长杆；内置三脚架的三个支腿可独立展开。

**具体用途**：需要拉开自拍取景距离时用延长杆；回到适合的桌面可安排固定构图。

**可能价值（编辑推演）**：对常在手持自拍与桌面口播之间切换的人，机位准备可能更集中在同一设备上。

**可匹配角色**：[独自旅行／看展者](../audiences/guide.md#mobile-aud-001)、[总替家人朋友拍照的人](../audiences/guide.md#mobile-aud-003)、[独自口播／课程录制者](../audiences/guide.md#mobile-aud-006)、[手工／烹饪／维修过程记录者](../audiences/guide.md#mobile-aud-015)

**型号与路径**：独立展开是支腿结构；仍需符合原记录的摆放条件。

**不应扩写为**：支腿能任意调高或自动调平。；任何户外地面和有风环境都稳。；不必安装、配平或确认构图。

**事实及完整条件入口**（命中后须一并读取条件、限制、官方定位与日期）：

- [MOBILE-8P-IDENTITY-003](../products/osmo_mobile_8p.md#mobile-8p-identity-003)｜内置延长杆｜`verified`｜核验 2026-09-06
- [MOBILE-8P-MAINTENANCE-002](../products/osmo_mobile_8p.md#mobile-8p-maintenance-002)｜内置三脚架｜`verified`｜核验 2026-09-06
- [MOBILE-8P-MAINTENANCE-005](../products/osmo_mobile_8p.md#mobile-8p-maintenance-005)｜内置三脚架｜`verified`｜核验 2026-09-07

<a id="mobile-sell-017"></a>
## MOBILE-SELL-017｜第五代手机夹的装夹与遮挡优化

**能力概括**：官方将手机夹尺寸、重量与软胶厚度列为优化项，并说明屏幕遮挡更小；日常装夹通常无需精准调平。

**具体用途**：装好常用手机后继续操作屏幕和取景；带壳或加镜头时重新检查完整组合。

**可能价值（编辑推演）**：对频繁装取手机的人，可围绕夹持和屏幕操作的便利解释这项设计；实际手感和遮挡仍取决于手机。

**可匹配角色**：[独自旅行／看展者](../audiences/guide.md#mobile-aud-001)、[日常Vlog初学者](../audiences/guide.md#mobile-aud-002)、[小店店主／经营者](../audiences/guide.md#mobile-aud-008)、[想拍自己、但不想在公共场合久架手机的人](../audiences/guide.md#mobile-aud-012)

**型号与路径**：优化是官方定性描述；不虚构减重、夹持力或安装速度对比。

**不应扩写为**：任何手机都零遮挡。；磁吸永不掉落。；手机能夹住就完整兼容。；随便加重镜头也不用配平。

**事实及完整条件入口**（命中后须一并读取条件、限制、官方定位与日期）：

- [MOBILE-8P-IDENTITY-005](../products/osmo_mobile_8p.md#mobile-8p-identity-005)｜DJI OM 磁吸手机夹 5｜`verified`｜核验 2026-09-07
- [MOBILE-8P-STABILIZATION-005](../products/osmo_mobile_8p.md#mobile-8p-stabilization-005)｜手机夹及配重孔｜`verified`｜核验 2026-09-06
- [MOBILE-8P-COMPATIBILITY-002](../products/osmo_mobile_8p.md#mobile-8p-compatibility-002)｜磁吸手机夹及手机壳｜`verified`｜核验 2026-09-06
- [MOBILE-8P-COMPATIBILITY-003](../products/osmo_mobile_8p.md#mobile-8p-compatibility-003)｜手机与外接镜头｜`verified`｜核验 2026-09-06

<a id="mobile-sell-018"></a>
## MOBILE-SELL-018｜按拍摄组合安排续航，并可给手机供电

**能力概括**：云台可经指定输出接口给手机供电；云台与FrameTap、两代模块的续航测试分别有独立工况。

**具体用途**：先确定拍摄时是否开跟随、补光和手机供电，再据此准备电量与充电机会。

**可能价值（编辑推演）**：对分段拍摄口播、旅行短片的人，可多一种应急供电安排；可用时长须按当次组合估计。

**可匹配角色**：[独自旅行／看展者](../audiences/guide.md#mobile-aud-001)、[独自口播／课程录制者](../audiences/guide.md#mobile-aud-006)、[小店店主／经营者](../audiences/guide.md#mobile-aud-008)、[直播／远程教学演示者](../audiences/guide.md#mobile-aud-010)

**型号与路径**：供电会消耗云台电池；10小时口径不能与开启模块、补光混写。

**不应扩写为**：所有功能全开也有10小时。；FrameTap独立使用能持续10小时。；手机和云台永远不用补电。；可以替换电池继续拍。

**事实及完整条件入口**（命中后须一并读取条件、限制、官方定位与日期）：

- [MOBILE-8P-POWER-001](../products/osmo_mobile_8p.md#mobile-8p-power-001)｜云台与FrameTap｜`verified`｜核验 2026-09-06
- [MOBILE-8P-POWER-002](../products/osmo_mobile_8p.md#mobile-8p-power-002)｜云台与多功能追踪模块2｜`verified`｜核验 2026-09-06
- [MOBILE-8P-POWER-003](../products/osmo_mobile_8p.md#mobile-8p-power-003)｜云台与一代多功能追踪模块｜`verified`｜核验 2026-09-06
- [MOBILE-8P-POWER-004](../products/osmo_mobile_8p.md#mobile-8p-power-004)｜云台USB-C输出｜`verified`｜核验 2026-09-06
- [MOBILE-8P-POWER-005](../products/osmo_mobile_8p.md#mobile-8p-power-005)｜云台内置电池｜`verified`｜核验 2026-09-06
- [MOBILE-8P-POWER-006](../products/osmo_mobile_8p.md#mobile-8p-power-006)｜FrameTap内置电池｜`verified`｜核验 2026-09-06
