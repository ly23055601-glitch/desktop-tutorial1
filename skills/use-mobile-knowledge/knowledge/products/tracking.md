# 跟随与遥控：按路径选择资料

手机云台的机械跟随模式、画面主体跟随、蓝牙快门和遥控取景分别核对。下面列出可用路径；具体条件请打开编号记录与相关缺口。

| 路径 | 核对重点 | 事实入口 |
|---|---|---|
| DJI Mimo 内跟随 | 在Mimo内拍摄，算法、镜头和拍摄规格受手机支持表影响；不把软件版本当某代硬件独占 | [MOBILE-8-TRACKING-001](osmo_mobile_8.md#mobile-8-tracking-001)、[MOBILE-8-TRACKING-002](osmo_mobile_8.md#mobile-8-tracking-002)、[MOBILE-8P-TRACKING-006](osmo_mobile_8p.md#mobile-8p-tracking-006) |
| 一代追踪模块 | 系统相机／第三方拍摄App中的硬件跟随；7/7P的人物与8的猫狗能力分别核对；8P使用一代模块不能向FrameTap投屏 | [MOBILE-LEGACY-003](osmo_mobile_7p.md#mobile-legacy-003)、[MOBILE-8-TRACKING-003](osmo_mobile_8.md#mobile-8-tracking-003)、[MOBILE-C8P-007](../compatibility/guide.md#mobile-c8p-007) |
| 第二代追踪模块 | 8更新指定固件后可用；触屏、高级设置和其他物体手动框选是手册限定的8P能力。非人物主体保留占画面超过10%条件 | [MOBILE-8-TRACKING-007](osmo_mobile_8.md#mobile-8-tracking-007)、[MOBILE-C8-011](../compatibility/guide.md#mobile-c8-011)、[MOBILE-8P-TRACKING-003](osmo_mobile_8p.md#mobile-8p-tracking-003)、[MOBILE-8P-TRACKING-004](osmo_mobile_8p.md#mobile-8p-tracking-004) |
| Apple DockKit | 适配iPhone、iOS和应用；原生人物跟拍与蓝牙快门不同。iPhone16e单独存在支持冲突 | [MOBILE-8-TRACKING-004](osmo_mobile_8.md#mobile-8-tracking-004)、[MOBILE-C8P-001](../compatibility/guide.md#mobile-c8p-001)、[MOBILE-C8-004](../compatibility/guide.md#mobile-c8-004)、[MOBILE-C8P-002](../compatibility/guide.md#mobile-c8p-002) |
| 鸿蒙智能追焦 | 逐机核对HarmonyOS版本、适配App、云台固件；7系列新增支持但部分FAQ配对描述仍待确认 | [MOBILE-8-TRACKING-006](osmo_mobile_8.md#mobile-8-tracking-006)、[MOBILE-C8P-003](../compatibility/guide.md#mobile-c8p-003)、[MOBILE-LEGACY-009](osmo_mobile_7p.md#mobile-legacy-009)、[MOBILE-LEGACY-010](osmo_mobile_7p.md#mobile-legacy-010) |

## FrameTap的两种画面来源

**手机投屏**显示手机屏幕内容，连接方式和兼容表按手机系统分别核对。**模块2投屏**显示追踪模块自身镜头画面，可在追踪预览中选择目标。两种画面不能当成同一镜头、同一画质或同一条拍摄流程。[MOBILE-8P-CONTROLS-004](osmo_mobile_8p.md#mobile-8p-controls-004)、[MOBILE-8P-CONTROLS-005](osmo_mobile_8p.md#mobile-8p-controls-005)、[MOBILE-C8P-009](../compatibility/guide.md#mobile-c8p-009)、[MOBILE-C8P-010](../compatibility/guide.md#mobile-c8p-010)

8P的“10米范围遥控”和规格“25米Wi-Fi图传”具有不同对象、测试环境及连接路径，不能合写成“25米稳定控制”。8的完整FrameTap云台联控仍未核定，不由手机支持表中的投屏列推断。[MOBILE-8P-CONTROLS-003](osmo_mobile_8p.md#mobile-8p-controls-003)、[MOBILE-8P-CONTROLS-004](osmo_mobile_8p.md#mobile-8p-controls-004)、[MOBILE-C8-017](../compatibility/guide.md#mobile-c8-017)

手机投屏说明中涉及Mimo与模块并用的范围尚待确认。默认按手册使用系统相机或第三方拍摄App配合模块；不要拼出“Mimo智能跟随和模块跟随同时开启”的功能。[MOBILE-8P-TRACKING-007](osmo_mobile_8p.md#mobile-8p-tracking-007)

## 手表遥控也有不同路径

Mimo手表App与系统相机遥控器的设备、系统和操作条件分别保存。预览不等于原片分辨率，能够预览也不意味着所有第三方App都能遥控。Mimo手表与其他蓝牙设备并用时，保留对应官方限制。[MOBILE-C8-014](../compatibility/guide.md#mobile-c8-014)、[MOBILE-C8-015](../compatibility/guide.md#mobile-c8-015)、[MOBILE-C8P-005](../compatibility/guide.md#mobile-c8p-005)、[MOBILE-C8P-006](../compatibility/guide.md#mobile-c8p-006)、[MOBILE-8-SOFTWARE-005](osmo_mobile_8.md#mobile-8-software-005)

## 软件更新怎样改变答案

8的2026-06-16发布记录新增模块2和iOS原生相机控制；7/7P的2025-10-22发布记录新增鸿蒙智能追焦和模块连接Mic3。问旧款时也应查后续更新。专门的新增支持记录与旧清单漏列要分开处理；明确互相排斥的文档结论则单列冲突。[MOBILE-8-TRACKING-007](osmo_mobile_8.md#mobile-8-tracking-007)、[MOBILE-8-CONTROLS-005](osmo_mobile_8.md#mobile-8-controls-005)、[MOBILE-LEGACY-009](osmo_mobile_7p.md#mobile-legacy-009)、[MOBILE-LEGACY-011](osmo_mobile_7p.md#mobile-legacy-011)
