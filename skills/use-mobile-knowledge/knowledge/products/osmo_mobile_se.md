# Osmo Mobile SE 产品事实

本页由结构化记录生成；引用前读取完整条件和官方依据。`verified` 只表示按记录日期核验，不表示实机测试。

## 身份与组件

<a id="mobile-se-identity-001"></a>
### MOBILE-SE-identity-001｜Osmo Mobile SE 是与DJI OM 4 SE不同的型号；相对后者增加状态显示面板、M键切换云台模式，并更新摇杆和手机夹。

- 型号：Osmo Mobile SE；组件：云台/状态显示面板
- 状态：`verified`；实际核验：2026-09-06
- 条件：官方准确名称为Osmo Mobile SE。
- 限制与不可推论：不能简写为OM4 SE或把二者视为同一固件产品。
- 依据：[SRC-MOBILE-LEGACY-006](../sources/README.md#src-mobile-legacy-006)｜相比 DJI OM 4 SE，Osmo Mobile SE 有哪些提升？

## 安装与操作

<a id="mobile-se-controls-001"></a>
### MOBILE-SE-controls-001｜Osmo Mobile SE 通过手柄左侧变焦滑杆上下推动控制变焦。

- 型号：Osmo Mobile SE；组件：变焦滑杆
- 状态：`verified`；实际核验：2026-09-06
- 条件：相机功能需结合手机和App兼容情况。
- 限制与不可推论：该滑杆不是6/7P的变焦对焦拨轮；变焦画质取决于手机镜头。
- 依据：[SRC-MOBILE-LEGACY-006](../sources/README.md#src-mobile-legacy-006)｜如何使用 Osmo Mobile SE 手柄控制手机相机变焦？

<a id="mobile-se-controls-002"></a>
### MOBILE-SE-controls-002｜Osmo Mobile SE 双击切换键切横竖拍；可通过M键切至旋转拍摄模式，再左右拨摇杆使用旋转拍摄。

- 型号：Osmo Mobile SE；组件：M按键/切换键
- 状态：`verified`；实际核验：2026-09-06
- 条件：开机状态；也可在Mimo对应拍摄模式的云台设置内选旋转拍摄。
- 限制与不可推论：SpinShot是拍摄模式，不能据此写水平无限位；规格平移结构范围为-161.2°至171.95°。
- 依据：[SRC-MOBILE-LEGACY-006](../sources/README.md#src-mobile-legacy-006)｜如何切换 Osmo Mobile SE 的横竖方向？；如何使用 Osmo Mobile SE 进行旋转拍摄？；[SRC-MOBILE-LEGACY-005](../sources/README.md#src-mobile-legacy-005)｜云台/结构转动范围

## 跟随与遥控

<a id="mobile-se-tracking-001"></a>
### MOBILE-SE-tracking-001｜Osmo Mobile SE 可在Mimo通过扳机、手动画框、开启后的手势启动智能跟随。

- 型号：Osmo Mobile SE；组件：DJI Mimo
- 状态：`verified`；实际核验：2026-09-06
- 条件：连接云台并进入Mimo拍摄界面。
- 限制与不可推论：蓝牙控制原生快门不等于原生App可做Mimo主体跟随。
- 依据：[SRC-MOBILE-LEGACY-006](../sources/README.md#src-mobile-legacy-006)｜如何使用 Osmo Mobile SE 的云台智能跟随功能？

## 手机与配件兼容

<a id="mobile-legacy-013"></a>
### MOBILE-LEGACY-013｜6、SE、DJI OM 5 的官方手机机械范围为170至290克、宽67至84毫米、厚6.9至10毫米。

- 型号：Osmo Mobile 6, Osmo Mobile SE, DJI OM 5；组件：手机夹/手机
- 状态：`verified`；实际核验：2026-09-06
- 条件：OM5规格原文为230±60克，即170至290克；手机加壳须仍满足可夹持尺寸，外接镜头后总重不超过290克。
- 限制与不可推论：夹持能力不代表手机所有镜头、帧率、分辨率、蓝牙控制与App功能均适配；不把新款300克上限套入这三款。
- 依据：[SRC-MOBILE-LEGACY-004](../sources/README.md#src-mobile-legacy-004)｜技术参数/适用手机范围；配件/外接镜头；[SRC-MOBILE-LEGACY-005](../sources/README.md#src-mobile-legacy-005)｜通用/适用手机范围；[SRC-MOBILE-LEGACY-006](../sources/README.md#src-mobile-legacy-006)｜手机保护壳；配件/外接镜头；[SRC-MOBILE-LEGACY-007](../sources/README.md#src-mobile-legacy-007)｜技术参数/适用手机范围；手机壳与外接镜头问答

## 续航与供电

<a id="mobile-se-power-001"></a>
### MOBILE-SE-power-001｜Osmo Mobile SE 工作时间约8小时，使用10瓦充电器测试充满约2小时12分钟。

- 型号：Osmo Mobile SE；组件：电池
- 状态：`verified`；实际核验：2026-09-06
- 条件：工作时间为调平衡工况下测试参考值。
- 限制与不可推论：不应替换为6的续航或7系列的10小时；不能承诺全天实际拍摄。
- 依据：[SRC-MOBILE-LEGACY-005](../sources/README.md#src-mobile-legacy-005)｜电池/工作时间、充电时间

<a id="mobile-se-power-002"></a>
### MOBILE-SE-power-002｜Osmo Mobile SE 可边充边用，但不能在使用时给其他设备供电；电池不能更换。

- 型号：Osmo Mobile SE；组件：USB-C/电池
- 状态：`verified`；实际核验：2026-09-06
- 条件：推荐充电5伏2安。
- 限制与不可推论：给云台输入电力和给手机输出电力是不同能力。
- 依据：[SRC-MOBILE-LEGACY-006](../sources/README.md#src-mobile-legacy-006)｜电池/能否边充电边使用？；能否在使用时对其他设备供电？；电池能否更换？

## 套装

<a id="mobile-se-kits-001"></a>
### MOBILE-SE-kits-001｜Osmo Mobile SE 机身不内置延长杆或三脚架；固定放置使用底部螺纹孔安装的外接三脚架。

- 型号：Osmo Mobile SE；组件：云台结构/延长杆/三脚架
- 状态：`verified`；实际核验：2026-09-06
- 条件：本条区分机身结构和外接配件；三脚架使用底部1/4"-20 UNC接口。
- 限制与不可推论：机身结构不代表所有在售SKU均附送三脚架；具体包装另核。；不能套用7/7P内置三脚架描述。
- 依据：[SRC-MOBILE-LEGACY-011](../sources/README.md#src-mobile-legacy-011)｜PDF物理第4页机身结构图（已目视）及第8页 1/4"-20 UNC螺纹孔；[SRC-MOBILE-LEGACY-006](../sources/README.md#src-mobile-legacy-006)｜配件/底部螺口是什么型号？

## 维护与限制

<a id="mobile-se-maintenance-001"></a>
### MOBILE-SE-maintenance-001｜Osmo Mobile SE与DJI OM 4 SE固件不通用；Mimo按所连接型号推送固件。

- 型号：Osmo Mobile SE；组件：云台固件
- 状态：`verified`；实际核验：2026-09-06
- 条件：连接前核对型号。
- 限制与不可推论：不能因为都带SE而套用相同固件。
- 依据：[SRC-MOBILE-LEGACY-006](../sources/README.md#src-mobile-legacy-006)｜Osmo Mobile SE 和 DJI OM 4 SE 固件是否通用？

## 软件与固件

<a id="mobile-legacy-012"></a>
### MOBILE-LEGACY-012｜当前7系列、6和SE中文官方FAQ均已介绍智能跟随8.0，不能只按上市时的跟随版本描述现状。

- 型号：Osmo Mobile 7P, Osmo Mobile 7, Osmo Mobile 6, Osmo Mobile SE；组件：DJI Mimo 智能跟随
- 状态：`verified`；实际核验：2026-09-06
- 条件：能力处于DJI Mimo路径，使用当前兼容的App与对应云台固件。
- 限制与不可推论：不从App算法名称推断模块代际、无限位、电机硬件或所有旧机型均有新款功能；具体版本最低门槛仍须当前发布记录。；官网FAQ介绍8.0不等于所有手机均获8.0；必须按兼容表的具体手机行确认算法版本和功能。
- 依据：[SRC-MOBILE-LEGACY-002](../sources/README.md#src-mobile-legacy-002)｜DJI Mimo App/智能跟随8.0有哪些提升？；[SRC-MOBILE-LEGACY-004](../sources/README.md#src-mobile-legacy-004)｜DJI Mimo App/智能跟随8.0有哪些提升？；[SRC-MOBILE-LEGACY-006](../sources/README.md#src-mobile-legacy-006)｜DJI Mimo App/智能跟随8.0有哪些提升？
