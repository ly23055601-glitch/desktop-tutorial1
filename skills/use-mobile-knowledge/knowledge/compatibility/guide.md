# 兼容与连接路径

按具体云台型号阅读。安装、蓝牙连接、快门控制、取景和跟随分别核对；未列出的组合不代表不支持。

## Osmo Mobile 8P

<a id="mobile-c8p-001"></a>
### MOBILE-C8P-001｜8P可通过Apple DockKit在iPhone原生相机和兼容第三方App中进行人物跟拍。

- 型号：Osmo Mobile 8P；组件：Apple DockKit原生人物跟拍
- 状态：`verified`；实际核验：2026-09-06
- 条件：iOS18.5及以上；以官方兼容表逐机型核对；排除iPhone SE第三代；iPhone16e单列冲突。；首次按NFC提示配对，取下追踪模块并关闭DJI Mimo App。
- 限制与不可推论：不能推导原生猫狗或物体跟随；不与模块/Mimo跟随同时使用。
- 设备：iPhone 12系列及后续兼容机型；路径：Apple DockKit原生人物跟拍
- 支持结论：`conditional`；功能：人物跟拍；原生相机
- 依据：[SRC-MOBILE-8P-003](../sources/README.md#src-mobile-8p-003)｜物理页31-32／Apple DockKit；[SRC-MOBILE-8P-002](../sources/README.md#src-mobile-8p-002)｜DockKit追踪功能／使用Apple DockKit需要什么设备？

<a id="mobile-c8p-002"></a>
### MOBILE-C8P-002｜iPhone16e的DockKit支持存在官方文档冲突。

- 型号：Osmo Mobile 8P；组件：Apple DockKit
- 状态：`conflict`；实际核验：2026-09-06
- 条件：兼容表DockKit列写支持，8P FAQ与手册31页明确排除。
- 限制与不可推论：冲突未解，不能作为支持或不支持的确定选购结论。
- 设备：iPhone 16e；路径：Apple DockKit
- 支持结论：`unconfirmed`；功能：DockKit；冲突
- 待核／冲突原因：当前兼容表与FAQ/手册对同一型号结论相反。
- 依据：[SRC-MOBILE-8P-005](../sources/README.md#src-mobile-8p-005)｜物理页1／iOS表iPhone16e行Apple DockKit列；[SRC-MOBILE-8P-003](../sources/README.md#src-mobile-8p-003)｜物理页31／设备要求；[SRC-MOBILE-8P-002](../sources/README.md#src-mobile-8p-002)｜DockKit追踪功能／使用Apple DockKit需要什么设备？

<a id="mobile-c8p-003"></a>
### MOBILE-C8P-003｜FAQ列出的华为机型可通过蓝牙或NFC配对8P，使用原生相机或兼容鸿蒙App人物跟拍。

- 型号：Osmo Mobile 8P；组件：鸿蒙智能追焦
- 状态：`verified`；实际核验：2026-09-06
- 条件：手机HarmonyOS6及以上；取下追踪模块；具体App按官方支持范围。
- 限制与不可推论：“系列”表述保留原来源范围，不推定所有其他华为手机或全部App支持。
- 设备：HUAWEI Mate 80系列；HUAWEI Mate X7系列；HUAWEI Mate 70系列；HUAWEI Mate X6系列；HUAWEI Mate 60系列；HUAWEI Mate X5系列；HUAWEI Pura 80系列；HUAWEI Pura 70系列；HUAWEI Pocket 2系列；路径：鸿蒙智能追焦
- 支持结论：`conditional`；功能：人物跟拍；原生相机；NFC
- 依据：[SRC-MOBILE-8P-002](../sources/README.md#src-mobile-8p-002)｜鸿蒙智能追焦／如何使用鸿蒙智能追焦？适配设备；[SRC-MOBILE-8P-003](../sources/README.md#src-mobile-8p-003)｜物理页32-33／鸿蒙智能追焦

<a id="mobile-c8p-004"></a>
### MOBILE-C8P-004｜已配对兼容华为手机时，手表原相机可遥控跟随和拍摄。

- 型号：Osmo Mobile 8P；组件：鸿蒙手表原相机遥控
- 状态：`verified`；实际核验：2026-09-06
- 条件：手机和手表均HarmonyOS6及以上；手机已与8P建立鸿蒙智能追焦连接。
- 限制与不可推论：不是手表DJI Mimo路径。
- 设备：HUAWEI WATCH 5及后续机型；路径：鸿蒙手表原相机遥控
- 支持结论：`conditional`；功能：手表遥控
- 依据：[SRC-MOBILE-8P-003](../sources/README.md#src-mobile-8p-003)｜物理页33／鸿蒙智能追焦；[SRC-MOBILE-8P-002](../sources/README.md#src-mobile-8p-002)｜鸿蒙智能追焦／适配设备

<a id="mobile-c8p-005"></a>
### MOBILE-C8P-005｜FAQ列出的Apple Watch可通过Mimo预览、拍录、云台摇杆和智能跟随。

- 型号：Osmo Mobile 8P；组件：Apple Watch上的DJI Mimo
- 状态：`verified`；实际核验：2026-09-06
- 条件：手表系统9.0以上；iPhone iOS16及以上；Mimo2.0.4及以上，两端安装并打开；无遮挡空旷一般8米以内。
- 限制与不可推论：预览清晰度受手表带宽影响，不等于原片分辨率；不建议同时蓝牙连接DJI麦克风。
- 设备：Apple Watch Series 7/8/9/10/11；Apple Watch SE 2/3；Apple Watch Ultra 1/2；路径：Apple Watch上的DJI Mimo
- 支持结论：`conditional`；功能：Mimo；预览；遥控；智能跟随
- 依据：[SRC-MOBILE-8P-002](../sources/README.md#src-mobile-8p-002)｜手表遥控／兼容型号、使用步骤、距离、蓝牙设备同时使用

<a id="mobile-c8p-006"></a>
### MOBILE-C8P-006｜手机与8P通过DockKit连接后，可打开手表相机遥控器控制跟随与拍摄。

- 型号：Osmo Mobile 8P；组件：Apple DockKit已连接后的原生相机遥控
- 状态：`verified`；实际核验：2026-09-06
- 条件：手表watchOS11或以上；手机满足DockKit机型及iOS要求。
- 限制与不可推论：不同于Mimo手表路径的系统要求；不能混用其全部兼容列表。
- 设备：Apple Watch；路径：Apple DockKit已连接后的原生相机遥控
- 支持结论：`conditional`；功能：DockKit；手表原生相机
- 依据：[SRC-MOBILE-8P-003](../sources/README.md#src-mobile-8p-003)｜物理页32／跟随与拍摄；[SRC-MOBILE-8P-002](../sources/README.md#src-mobile-8p-002)｜DockKit追踪功能／Apple DockKit如何通过Apple Watch远程遥控？

<a id="mobile-c8p-007"></a>
### MOBILE-C8P-007｜8P兼容一代模块，但该模块不支持向FrameTap投屏。

- 型号：Osmo Mobile 8P；组件：一代模块装到8P
- 状态：`verified`；实际核验：2026-09-06
- 条件：来源未另列；不作额外推断
- 限制与不可推论：不因8P有遥控器就产生一代模块视频输出；各代模块功能另核。
- 设备：DJI OM多功能追踪模块；路径：一代模块装到8P
- 支持结论：`supported`；功能：模块一代；兼容；无模块投屏
- 依据：[SRC-MOBILE-8P-002](../sources/README.md#src-mobile-8p-002)｜通用／可以搭配DJI OM7系列磁吸手机夹及DJI OM多功能追踪模块使用吗？

<a id="mobile-c8p-008"></a>
### MOBILE-C8P-008｜模块2可向FrameTap提供追踪预览，并在屏幕上选择跟随目标。

- 型号：Osmo Mobile 8P；组件：模块2镜头投屏到FrameTap
- 状态：`verified`；实际核验：2026-09-06
- 条件：模块镜头与手机摄像头方向一致；按对象类型使用点选或手动框选。
- 限制与不可推论：预览来自模块2而非手机；需时做画面校准。
- 设备：DJI OM多功能追踪模块2；Osmo FrameTap取景遥控器；路径：模块2镜头投屏到FrameTap
- 支持结论：`supported`；功能：模块投屏；触屏框选；物体跟随
- 依据：[SRC-MOBILE-8P-003](../sources/README.md#src-mobile-8p-003)｜物理页26-27、30／跟随与拍摄、画面校准

<a id="mobile-c8p-009"></a>
### MOBILE-C8P-009｜iPhone可搭配DJI Mimo把手机屏幕画面投到FrameTap。

- 型号：Osmo Mobile 8P；组件：手机经DJI Mimo向FrameTap投屏
- 状态：`verified`；实际核验：2026-09-06
- 条件：按兼容表手机行确认；V01.02.01.01增加iOS投屏；按遥控器左滑的苹果指引连接。
- 限制与不可推论：不是模块投屏；退出时iOS还需在手机结束录屏；投屏不能证明全部App远程按键可控。
- 设备：iPhone兼容机型；路径：手机经DJI Mimo向FrameTap投屏
- 支持结论：`conditional`；功能：手机投屏；iOS；Mimo
- 依据：[SRC-MOBILE-8P-002](../sources/README.md#src-mobile-8p-002)｜通用／相比Osmo Mobile8有哪些提升？；取景遥控器／如何进行手机投屏？；[SRC-MOBILE-8P-003](../sources/README.md#src-mobile-8p-003)｜物理页17-18／手机投屏；[SRC-MOBILE-8P-004](../sources/README.md#src-mobile-8p-004)｜物理页2／新增iOS投屏；[SRC-MOBILE-8P-005](../sources/README.md#src-mobile-8p-005)｜物理页1／iOS遥控器投屏列和脚注4

<a id="mobile-c8p-010"></a>
### MOBILE-C8P-010｜兼容Android/鸿蒙手机可按系统投屏方式向FrameTap显示手机画面。

- 型号：Osmo Mobile 8P；组件：手机系统投屏到FrameTap
- 状态：`verified`；实际核验：2026-09-06
- 条件：在遥控器左滑选择对应手机系统；手机兼容表中逐行确认遥控器投屏列，不能只按操作系统判断。
- 限制与不可推论：当前表如Google Pixel系列列不支持遥控器投屏；功能不因能蓝牙连云台而自动成立。
- 设备：Android兼容机型；HarmonyOS兼容机型；路径：手机系统投屏到FrameTap
- 支持结论：`conditional`；功能：手机投屏；安卓；鸿蒙
- 依据：[SRC-MOBILE-8P-002](../sources/README.md#src-mobile-8p-002)｜通用／相比Osmo Mobile8有哪些提升？；取景遥控器／如何进行手机投屏？；[SRC-MOBILE-8P-005](../sources/README.md#src-mobile-8p-005)｜物理页1／Android表遥控器投屏列及脚注7

<a id="mobile-c8p-011"></a>
### MOBILE-C8P-011｜8P可搭配DJI OM7系列磁吸手机夹。

- 型号：Osmo Mobile 8P；组件：磁吸装夹
- 状态：`verified`；实际核验：2026-09-06
- 条件：手机及附件仍需满足相应装夹和平衡要求。
- 限制与不可推论：只证明此手机夹可用，不证明所有旧代手机夹均兼容。
- 设备：DJI OM7系列磁吸手机夹；路径：磁吸装夹
- 支持结论：`supported`；功能：旧手机夹；装夹
- 依据：[SRC-MOBILE-8P-002](../sources/README.md#src-mobile-8p-002)｜通用／可以搭配DJI OM7系列磁吸手机夹及DJI OM多功能追踪模块使用吗？

<a id="mobile-c8p-012"></a>
### MOBILE-C8P-012｜在8P拍摄组合中，手机端接收器可承接最多2台发射器的音频。

- 型号：Osmo Mobile 8P；组件：接收器连接手机后安装8P
- 状态：`verified`；实际核验：2026-09-06
- 条件：接收器接手机；具体TX型号、手机接口和线材按接收器资料另核。
- 限制与不可推论：不表明模块2能直接连接2台TX；不直接把手机端接收器插入云台充电口。
- 设备：DJI Mic系列手机版接收器；路径：接收器连接手机后安装8P
- 支持结论：`conditional`；功能：音频；双人；手机接收器
- 依据：[SRC-MOBILE-8P-003](../sources/README.md#src-mobile-8p-003)｜物理页31／连接无线麦克风

## Osmo Mobile 8

<a id="mobile-c8-001"></a>
### MOBILE-C8-001｜符合170–300克、宽67–84毫米、厚6.9–10毫米的手机属于官方推荐机械安装范围。

- 型号：Osmo Mobile 8；组件：手机夹
- 状态：`verified`；实际核验：2026-09-06
- 条件：手机加保护壳厚度不超过10毫米；配重与镜头遮挡需实际检查
- 限制与不可推论：不是全部手机App、跟随或分辨率兼容保证。
- 设备：Osmo Mobile 8 磁吸手机夹；手机及保护壳；路径：磁吸手机夹机械安装
- 支持结论：`conditional`；功能：夹持；增稳
- 依据：[SRC-MOBILE-8-001](../sources/README.md#src-mobile-8-001)｜通用／适用手机范围；[SRC-MOBILE-8-002](../sources/README.md#src-mobile-8-002)｜通用／保护壳

<a id="mobile-c8-002"></a>
### MOBILE-C8-002｜外接镜头后的手机组合建议总重不超过300克并三轴配平。

- 型号：Osmo Mobile 8；组件：外接镜头
- 状态：`verified`；实际核验：2026-09-06
- 条件：避免过大/过重镜头；偏重时可用横滚轴配重孔
- 限制与不可推论：机械可用不代表图像不遮挡或全部模式可用。
- 设备：手机；手机外接镜头；横滚轴配重块；路径：装配后机械配平
- 支持结论：`conditional`；功能：增稳
- 依据：[SRC-MOBILE-8-002](../sources/README.md#src-mobile-8-002)｜通用／外接镜头、是否需要调平

<a id="mobile-c8-003"></a>
### MOBILE-C8-003｜iPhone13、iPhone13 Pro、iPhone13 Pro Max可按DockKit路径进行人物跟拍。

- 型号：Osmo Mobile 8；组件：iPhone DockKit
- 状态：`verified`；实际核验：2026-09-06
- 条件：iOS18.5+；关闭Mimo、取下模块；启用手机网络、蓝牙及NFC
- 限制与不可推论：此路径不意味着Mimo已连接；第三方App需兼容DockKit。
- 设备：iPhone 13；iPhone 13 Pro；iPhone 13 Pro Max；路径：手机NFC配对云台 → Apple DockKit → 系统相机或兼容App
- 支持结论：`conditional`；功能：人物跟随；原生相机跟拍
- 依据：[SRC-MOBILE-8-004](../sources/README.md#src-mobile-8-004)｜第28–29页；[SRC-MOBILE-8-008](../sources/README.md#src-mobile-8-008)｜第1页iOS对应行及脚注3

<a id="mobile-c8-004"></a>
### MOBILE-C8-004｜iPhone16e是否支持Mobile8 DockKit存在官方资料冲突。

- 型号：Osmo Mobile 8；组件：iPhone 16e DockKit
- 状态：`conflict`；实际核验：2026-09-06
- 条件：兼容PDF标支持，8 FAQ和手册明确排除
- 限制与不可推论：不得按iPhone12以后统括回答支持，也不得仅据旧FAQ最终判不支持。
- 设备：iPhone 16e；路径：Apple DockKit
- 支持结论：`unconfirmed`；功能：人物跟随
- 待核／冲突原因：同一组合的官方资料不一致，未获得解决该差异的正式说明。
- 依据：[SRC-MOBILE-8-008](../sources/README.md#src-mobile-8-008)｜第1页iPhone16e行Apple DockKit列；[SRC-MOBILE-8-002](../sources/README.md#src-mobile-8-002)｜DockKit／使用Apple DockKit需要什么设备；[SRC-MOBILE-8-004](../sources/README.md#src-mobile-8-004)｜第28页

<a id="mobile-c8-005"></a>
### MOBILE-C8-005｜iPhone12、12 Pro、12 Pro Max的Mimo智能跟随版本在兼容表为7.0。

- 型号：Osmo Mobile 8；组件：iPhone 12 Mimo
- 状态：`verified`；实际核验：2026-09-06
- 条件：使用兼容Mimo和手机系统；最低安装要求iOS15
- 限制与不可推论：不因Mobile8型号数字认定手机有跟随8.0；这些机型不支持双摄增强。
- 设备：iPhone 12；iPhone 12 Pro；iPhone 12 Pro Max；路径：手机 → DJI Mimo → 云台
- 支持结论：`conditional`；功能：Mimo跟随7.0
- 依据：[SRC-MOBILE-8-008](../sources/README.md#src-mobile-8-008)｜第1页iOS相应行；[SRC-MOBILE-8-003](../sources/README.md#src-mobile-8-003)｜Mimo系统要求

<a id="mobile-c8-006"></a>
### MOBILE-C8-006｜iPhone13 Pro、13 Pro Max兼容表列出Mimo智能跟随8.0和双摄增强。

- 型号：Osmo Mobile 8；组件：iPhone 13 Pro Mimo
- 状态：`verified`；实际核验：2026-09-06
- 条件：按当前Mimo和兼容表使用
- 限制与不可推论：普通iPhone13不能继承双摄增强；不保证遮挡后永不跟丢。
- 设备：iPhone 13 Pro；iPhone 13 Pro Max；路径：手机 → DJI Mimo → 云台
- 支持结论：`conditional`；功能：Mimo跟随8.0；双摄增强
- 依据：[SRC-MOBILE-8-008](../sources/README.md#src-mobile-8-008)｜第1页iOS相应行；[SRC-MOBILE-8-002](../sources/README.md#src-mobile-8-002)｜DJI Mimo／双摄增强适用机型

<a id="mobile-c8-007"></a>
### MOBILE-C8-007｜兼容表中Galaxy S26、S26+的系统相机按键功能为拍照录像；S26 Ultra另外列前后镜头切换和变焦。

- 型号：Osmo Mobile 8；组件：三星系统相机
- 状态：`verified`；实际核验：2026-09-06
- 条件：按兼容表逐机与系统版本核查
- 限制与不可推论：支持快门不代表具备无需模块的原生人物跟随；也不能把Ultra功能推给S26/S26+。
- 设备：Samsung Galaxy S26；Samsung Galaxy S26+；Samsung Galaxy S26 Ultra；路径：系统蓝牙配对云台 → 手机系统相机
- 支持结论：`conditional`；功能：系统相机快门控制
- 依据：[SRC-MOBILE-8-008](../sources/README.md#src-mobile-8-008)｜第1页Android三星对应行、脚注3

<a id="mobile-c8-008"></a>
### MOBILE-C8-008｜已核HUAWEI Mate60、Mate60 Pro、Mate70、Mate70 Pro、Pura70、Pura70 Pro和Pura70 Ultra可按鸿蒙智能追焦路径使用。

- 型号：Osmo Mobile 8；组件：鸿蒙智能追焦
- 状态：`verified`；实际核验：2026-09-06
- 条件：HarmonyOS6+；取下模块；不与Mimo跟随同时使用；逐机查当前FAQ
- 限制与不可推论：不泛化所有华为手机、折叠状态或所有第三方鸿蒙应用。
- 设备：HUAWEI Mate 60；HUAWEI Mate 60 Pro；HUAWEI Mate 70；HUAWEI Mate 70 Pro；HUAWEI Pura 70；HUAWEI Pura 70 Pro；HUAWEI Pura 70 Ultra；路径：系统蓝牙或NFC配对云台 → 鸿蒙系统相机/适配应用
- 支持结论：`conditional`；功能：人物跟随；原生相机拍摄
- 依据：[SRC-MOBILE-8-004](../sources/README.md#src-mobile-8-004)｜第31页；[SRC-MOBILE-8-002](../sources/README.md#src-mobile-8-002)｜鸿蒙智能追焦／适配设备；[SRC-MOBILE-8-008](../sources/README.md#src-mobile-8-008)｜第1页Android华为行、脚注6

<a id="mobile-c8-009"></a>
### MOBILE-C8-009｜Mobile8可使用DJI OM多功能追踪模块，也可使用FAQ所指7P同款模块。

- 型号：Osmo Mobile 8；组件：一代追踪模块
- 状态：`verified`；实际核验：2026-09-06
- 条件：云台与模块正确安装、更新固件；人物0.5–8米，手势0.5–3米；猫狗推荐单只
- 限制与不可推论：不同代际固件的具体能力需复核；这里不确认7P使用8模块后必有完全相同能力。
- 设备：DJI OM 多功能追踪模块（Osmo Mobile 8/7P）；路径：模块磁吸到手机夹 → 模块镜头识别 → 云台跟随
- 支持结论：`conditional`；功能：人物跟随；猫狗跟随；补光
- 依据：[SRC-MOBILE-8-002](../sources/README.md#src-mobile-8-002)｜模块8与7P是否通用；跟随提升；[SRC-MOBILE-8-005](../sources/README.md#src-mobile-8-005)｜第6–9页

<a id="mobile-c8-010"></a>
### MOBILE-C8-010｜Mobile8配合模块2支持人物、猫狗、车辆跟随及拨轮调补光。

- 型号：Osmo Mobile 8；组件：模块2
- 状态：`verified`；实际核验：2026-09-06
- 条件：云台V01.02.02.02及以后适配固件；模块镜头与手机同向；人物0.5–8米、非人物占画面10%以上；避免逆光暗光
- 限制与不可推论：8不支持模块2的触屏控制、智能跟随设置及其他物体手动框选；麦克风接收另待核。
- 设备：DJI OM 多功能追踪模块 2；路径：模块磁吸到手机夹 → 识别目标 → 云台扳机/人物手势控制
- 支持结论：`conditional`；功能：人物跟随；猫狗跟随；车辆跟随；补光
- 依据：[SRC-MOBILE-8-007](../sources/README.md#src-mobile-8-007)｜第1页；[SRC-MOBILE-8-006](../sources/README.md#src-mobile-8-006)｜第6–8、11–12页

<a id="mobile-c8-011"></a>
### MOBILE-C8-011｜模块2触屏控制、智能跟随设置以及其他物体的手动框选在手册中限定仅Osmo Mobile8P支持。

- 型号：Osmo Mobile 8；组件：模块2的8P专属功能
- 状态：`verified`；实际核验：2026-09-06
- 条件：当前组合云台为Osmo Mobile8
- 限制与不可推论：此限制只覆盖所列高级功能，不能推成8不支持模块2。
- 设备：DJI OM 多功能追踪模块 2；路径：模块2高级触屏操作
- 支持结论：`not_supported`；功能：触屏选目标；智能跟随设置；任意物体手动框选
- 依据：[SRC-MOBILE-8-006](../sources/README.md#src-mobile-8-006)｜第6–8、10页8P专属说明及表格脚注

<a id="mobile-c8-012"></a>
### MOBILE-C8-012｜Mobile8一代模块可接收1台或最多2台同款Mic Mini/Mic3/Mic2发射器并有线送入手机。

- 型号：Osmo Mobile 8；组件：一代模块音频
- 状态：`verified`；实际核验：2026-09-06
- 条件：双发射器必须同款；Mic Mini/Mic3接收器配对模式，Mic2蓝牙配对模式；Mic3支持更新见V01.01.02.09
- 限制与不可推论：不是三种发射器混搭；50厘米充电线不能代替音频线；App要实际选择/接收输入。
- 设备：DJI OM 多功能追踪模块；DJI Mic Mini 发射器；DJI Mic 3 发射器；DJI Mic 2 发射器；手机充电/录音连接线（15 cm）；路径：发射器 → 一代模块接收 → 专用音频线 → 手机
- 支持结论：`conditional`；功能：无线收音
- 依据：[SRC-MOBILE-8-004](../sources/README.md#src-mobile-8-004)｜第25–28页；[SRC-MOBILE-8-007](../sources/README.md#src-mobile-8-007)｜第2页Mic3更新

<a id="mobile-c8-013"></a>
### MOBILE-C8-013｜Lightning口iPhone经一代模块收音时需另购专用USB-C转Lightning充电/录音线。

- 型号：Osmo Mobile 8；组件：Lightning音频
- 状态：`verified`；实际核验：2026-09-06
- 条件：按模块音频配对；供电可双击M键单独开关
- 限制与不可推论：不把任意USB-C转Lightning充电线视为等效音频线。
- 设备：Lightning接口iPhone；DJI OM 多功能追踪模块；手机充电/录音连接线（USB-C 转 Lightning）；路径：发射器 → 模块 → USB-C转Lightning音频线 → iPhone
- 支持结论：`conditional`；功能：外接收音；手机供电
- 依据：[SRC-MOBILE-8-002](../sources/README.md#src-mobile-8-002)｜多功能追踪模块／配合手机录音；[SRC-MOBILE-8-004](../sources/README.md#src-mobile-8-004)｜第26–27页

<a id="mobile-c8-014"></a>
### MOBILE-C8-014｜已列Apple Watch可通过Mimo控制Mobile8并预览取景。

- 型号：Osmo Mobile 8；组件：Apple Watch Mimo
- 状态：`verified`；实际核验：2026-09-06
- 条件：watchOS9+；iPhone iOS16+；Mimo2.0.4+；两端打开Mimo；空旷无遮挡一般8米内
- 限制与不可推论：预览不等于原片分辨率；不建议同时连接DJI麦克风或其他蓝牙设备。
- 设备：Apple Watch Series 7/8/9/10；Apple Watch SE 2；Apple Watch Ultra 1/2；iPhone；路径：Apple Watch Mimo ↔ iPhone Mimo ↔ Mobile8
- 支持结论：`conditional`；功能：实时预览；拍照录像；摇杆；智能跟随；横竖拍；回中
- 依据：[SRC-MOBILE-8-002](../sources/README.md#src-mobile-8-002)｜手表遥控全部相关问答；[SRC-MOBILE-8-004](../sources/README.md#src-mobile-8-004)｜第30页

<a id="mobile-c8-015"></a>
### MOBILE-C8-015｜DockKit连接下可用Apple Watch系统相机遥控器控制跟随与拍摄。

- 型号：Osmo Mobile 8；组件：Apple Watch DockKit
- 状态：`verified`；实际核验：2026-09-06
- 条件：watchOS11+；手机iOS18.5+且满足DockKit型号要求；关闭Mimo，取下模块
- 限制与不可推论：与Mimo手表路径分开，不能把watchOS9门槛用在此路径。
- 设备：Apple Watch；兼容DockKit的iPhone；路径：Apple Watch系统相机遥控器 ↔ iPhone DockKit ↔ Mobile8
- 支持结论：`conditional`；功能：跟随控制；拍照录像
- 依据：[SRC-MOBILE-8-004](../sources/README.md#src-mobile-8-004)｜第28–29页

<a id="mobile-c8-016"></a>
### MOBILE-C8-016｜当前FAQ列出HUAWEI WATCH5及后续机型可配合适配华为手机的原相机控制Mobile8转动、跟随、拍照录像。

- 型号：Osmo Mobile 8；组件：华为手表鸿蒙追焦
- 状态：`verified`；实际核验：2026-09-06
- 条件：手表系统HarmonyOS6+；手机满足鸿蒙智能追焦条件；后续型号使用前再核
- 限制与不可推论：不是在华为手表运行Apple Watch版Mimo；FAQ未给统一遥控距离。
- 设备：HUAWEI WATCH 5；鸿蒙智能追焦兼容华为手机；路径：华为手表原相机 ↔ 华为手机鸿蒙智能追焦 ↔ Mobile8
- 支持结论：`conditional`；功能：云台转动；人物跟随；拍照录像
- 依据：[SRC-MOBILE-8-002](../sources/README.md#src-mobile-8-002)｜鸿蒙智能追焦／使用步骤3及适配设备；[SRC-MOBILE-8-004](../sources/README.md#src-mobile-8-004)｜第31页

<a id="mobile-c8-017"></a>
### MOBILE-C8-017｜手机功能表的FrameTap投屏支持尚不足以确认Mobile8全部云台联控功能。

- 型号：Osmo Mobile 8；组件：FrameTap
- 状态：`pending`；实际核验：2026-09-06
- 条件：需补充FrameTap官方适配云台与固件说明
- 限制与不可推论：手机投屏列不能代表8具有8P的模块2触屏框选。
- 设备：Osmo FrameTap 取景遥控器；手机；路径：手机投屏至FrameTap；Mobile8联控待核
- 支持结论：`unconfirmed`；功能：取景；云台遥控
- 待核／冲突原因：缺少明确Mobile8与FrameTap整套联控的官方依据。
- 依据：[SRC-MOBILE-8-008](../sources/README.md#src-mobile-8-008)｜第1页iOS脚注4、Android脚注7；[SRC-MOBILE-8-006](../sources/README.md#src-mobile-8-006)｜第6–8页

## Osmo Mobile 7P

<a id="mobile-cl-001"></a>
### MOBILE-CL-001｜本型号手机夹的机械范围为宽67至84毫米、厚6.9至10毫米、重170至300克。

- 型号：Osmo Mobile 7P；组件：手机夹/手机
- 状态：`verified`；实际核验：2026-09-06
- 条件：手机及保护壳合计尺寸须在夹持范围内；外接镜头后保持平衡且总重不超过对应上限。
- 限制与不可推论：仅作机械适配筛选，不承诺手机全部App、镜头、录像规格、快门或跟随功能。
- 设备：符合所列机械范围的智能手机；磁吸手机夹；路径：手机夹机械安装
- 支持结论：`conditional`；功能：机械安装；云台承载
- 依据：[SRC-MOBILE-LEGACY-001](../sources/README.md#src-mobile-legacy-001)｜技术参数/适用手机范围；[SRC-MOBILE-LEGACY-002](../sources/README.md#src-mobile-legacy-002)｜保护壳与外接镜头问答

<a id="mobile-cl-006"></a>
### MOBILE-CL-006｜DJI OM 多功能追踪模块（一代）经DJI OM 7系列磁吸手机夹安装，可在Mimo以外的相机/直播App跟随人物。

- 型号：Osmo Mobile 7P；组件：一代追踪模块/手机夹
- 状态：`verified`；实际核验：2026-09-06
- 条件：7P原标准套装附带模块和对应夹；7需另购追踪套件。；模块镜头朝向主体；拍照录像控制还需手机/App兼容。
- 限制与不可推论：一代模块的人物跟随不能推为7系列支持猫狗或任意物体；不能推模块2可用。
- 设备：DJI OM 多功能追踪模块；DJI OM 7 系列磁吸手机夹；路径：模块视觉跟随→云台；手机原生/第三方App拍摄
- 支持结论：`conditional`；功能：人物跟随；模块补光
- 依据：[SRC-MOBILE-LEGACY-002](../sources/README.md#src-mobile-legacy-002)｜如何使用云台智能跟随功能？；模块智能跟随和Mimo有什么区别？；[SRC-MOBILE-LEGACY-009](../sources/README.md#src-mobile-legacy-009)｜PDF物理第6、7、19、20页

<a id="mobile-cl-008"></a>
### MOBILE-CL-008｜一代模块可接DJI Mic Mini或DJI Mic 2发射器，并用手机录音线将音频送至手机。

- 型号：Osmo Mobile 7P；组件：一代追踪模块/DJI Mic Mini或Mic2/录音线
- 状态：`verified`；实际核验：2026-09-06
- 条件：Mic2新增于固件V01.02.00.01；当次Mimo版本iOS2.2.5/Android2.2.4。；模块经15厘米手机录音线接手机；Lightning手机另购专用USB-C转Lightning录音线。；手册最多2个同款发射器；MicMini进入接收器配对模式，Mic2进入蓝牙配对模式。
- 限制与不可推论：50厘米云台充电线不能替代录音线；Mimo模块音频调参仅明确支持MicMini。；不把这两款的2发同款规则自动扩推到Mic3。
- 设备：DJI OM 多功能追踪模块；DJI Mic Mini 发射器；DJI Mic 2 发射器；手机录音连接线（USB-C转USB-C，15cm）；路径：TX无线→一代模块→手机录音线→手机
- 支持结论：`conditional`；功能：无线收音；音频传输
- 依据：[SRC-MOBILE-LEGACY-009](../sources/README.md#src-mobile-legacy-009)｜PDF物理第24页；[SRC-MOBILE-LEGACY-002](../sources/README.md#src-mobile-legacy-002)｜云台充电线和手机录音连接线是否通用？；[SRC-MOBILE-LEGACY-010](../sources/README.md#src-mobile-legacy-010)｜PDF物理第5页 2025.04.09

<a id="mobile-cl-010"></a>
### MOBILE-CL-010｜7系列固件新增鸿蒙智能追焦，可搭配官方列出的HarmonyOS 6华为手机系列使用。

- 型号：Osmo Mobile 7P；组件：手机系统/云台
- 状态：`verified`；实际核验：2026-09-06
- 条件：云台固件含V01.05.00.01新增能力；手机系统HarmonyOS 6及以上。；本记录设备清单来自读取日中文FAQ；具体手机仍需满足安装条件。
- 限制与不可推论：本记录只肯定有依据的蓝牙配对及系统追焦；NFC配对和横滚轴盖灯交互另列待核。；不由华为系列名推出所有系统版本或所有第三方App均支持。
- 设备：HUAWEI Mate 80 系列；HUAWEI Mate X7 系列；HUAWEI Mate 70 系列；HUAWEI Mate X6 系列；HUAWEI Mate 60 系列；HUAWEI Mate X5 系列；HUAWEI Pura 80 系列；HUAWEI Pura 70 系列；HUAWEI Pocket 2 系列；路径：华为手机系统蓝牙→云台；鸿蒙原生智能追焦
- 支持结论：`conditional`；功能：系统原生智能跟随
- 依据：[SRC-MOBILE-LEGACY-010](../sources/README.md#src-mobile-legacy-010)｜PDF物理第2页；[SRC-MOBILE-LEGACY-002](../sources/README.md#src-mobile-legacy-002)｜鸿蒙智能追焦/如何使用鸿蒙智能追焦？ 适配设备

<a id="mobile-cl-012"></a>
### MOBILE-CL-012｜7系列、6及SE在官方列出的Apple Watch上可用Mimo遥控云台并查看拍摄画面。

- 型号：Osmo Mobile 7P；组件：Apple Watch/iPhone/DJI Mimo
- 状态：`verified`；实际核验：2026-09-06
- 条件：手表watchOS 9及以上；iPhone iOS16及以上；iPhone上Mimo2.0.4及以上。；手表与iPhone先配对，两端打开Mimo，iPhone连接云台进入拍摄界面。；当前7系列FAQ明确列7系列、6及SE；清单外新手表不由本条推断兼容。
- 限制与不可推论：手表实时预览带宽不等于成片分辨率；不是FrameTap硬件遥控器。；Apple蓝牙同时使用麦克风不推荐，可另走有线接收器路径。
- 设备：Apple Watch Series 7；Apple Watch Series 8；Apple Watch Series 9；Apple Watch Series 10；Apple Watch SE 2；Apple Watch Ultra 1；Apple Watch Ultra 2；iPhone；路径：手表Mimo→配对iPhone Mimo→蓝牙云台
- 支持结论：`conditional`；功能：预览；拍照录像；虚拟摇杆；智能跟随；横竖切换；回中
- 依据：[SRC-MOBILE-LEGACY-002](../sources/README.md#src-mobile-legacy-002)｜手表遥控/兼容型号、如何使用、有哪些功能、清晰度、麦克风同时使用

<a id="mobile-cl-016"></a>
### MOBILE-CL-016｜尚无本次已读取资料直接确认该旧型号与模块2的完整兼容结论。

- 型号：Osmo Mobile 7P；组件：DJI OM 多功能追踪模块 2
- 状态：`pending`；实际核验：2026-09-06
- 条件：必须找到对应云台固件记录或型号明确的模块兼容依据后再使用肯定答案。
- 限制与不可推论：旧支持页只列8P已过时；当前8模块2手册没有给出本型号的明确支持或不支持结论。；未列不等于不支持；不能从磁吸可装、其他型号可用推兼容。
- 设备：DJI OM 多功能追踪模块 2；路径：模块2→该云台的跟随/供电/控制兼容待核
- 支持结论：`unconfirmed`；功能：来源未另列；不作额外推断
- 待核／冲突原因：目前仅取得明确8/8P使用依据，未取得本型号模块2支持或排除证据。
- 依据：[SRC-MOBILE-LEGACY-008](../sources/README.md#src-mobile-legacy-008)｜适用产品（已知列表不完整）；[SRC-MOBILE-8-006](../sources/README.md#src-mobile-8-006)｜PDF物理第6页 产品使用及后续操作；未给出本型号兼容结论

<a id="mobile-cl-021"></a>
### MOBILE-CL-021｜Mic3基本连接的固件新增已有依据，但7系列组合的路数、混用规则与Mimo音频调参仍待核。

- 型号：Osmo Mobile 7P；组件：一代追踪模块/DJI Mic 3 TX
- 状态：`pending`；实际核验：2026-09-06
- 条件：先区分固件新增连接能力与具体音频功能。
- 限制与不可推论：不能从手册对MicMini/Mic2的最多2台同款规则扩推Mic3；未核参数不进入确定答复。
- 设备：DJI OM 多功能追踪模块；DJI Mic 3 发射器；路径：Mic3→一代模块→手机音频细项待核
- 支持结论：`unconfirmed`；功能：来源未另列；不作额外推断
- 待核／冲突原因：固件明确新增连接，但已读手册与FAQ尚未补充Mic3专属连接步骤、路数及设置范围。
- 依据：[SRC-MOBILE-LEGACY-010](../sources/README.md#src-mobile-legacy-010)｜PDF物理第2页 2025.10.22；[SRC-MOBILE-LEGACY-009](../sources/README.md#src-mobile-legacy-009)｜PDF物理第24页仅列MicMini/Mic2及相应参数设置范围

## Osmo Mobile 7

<a id="mobile-cl-002"></a>
### MOBILE-CL-002｜本型号手机夹的机械范围为宽67至84毫米、厚6.9至10毫米、重170至300克。

- 型号：Osmo Mobile 7；组件：手机夹/手机
- 状态：`verified`；实际核验：2026-09-06
- 条件：手机及保护壳合计尺寸须在夹持范围内；外接镜头后保持平衡且总重不超过对应上限。
- 限制与不可推论：仅作机械适配筛选，不承诺手机全部App、镜头、录像规格、快门或跟随功能。
- 设备：符合所列机械范围的智能手机；磁吸手机夹；路径：手机夹机械安装
- 支持结论：`conditional`；功能：机械安装；云台承载
- 依据：[SRC-MOBILE-LEGACY-001](../sources/README.md#src-mobile-legacy-001)｜技术参数/适用手机范围；[SRC-MOBILE-LEGACY-002](../sources/README.md#src-mobile-legacy-002)｜保护壳与外接镜头问答

<a id="mobile-cl-007"></a>
### MOBILE-CL-007｜DJI OM 多功能追踪模块（一代）经DJI OM 7系列磁吸手机夹安装，可在Mimo以外的相机/直播App跟随人物。

- 型号：Osmo Mobile 7；组件：一代追踪模块/手机夹
- 状态：`verified`；实际核验：2026-09-06
- 条件：7P原标准套装附带模块和对应夹；7需另购追踪套件。；模块镜头朝向主体；拍照录像控制还需手机/App兼容。
- 限制与不可推论：一代模块的人物跟随不能推为7系列支持猫狗或任意物体；不能推模块2可用。
- 设备：DJI OM 多功能追踪模块；DJI OM 7 系列磁吸手机夹；路径：模块视觉跟随→云台；手机原生/第三方App拍摄
- 支持结论：`conditional`；功能：人物跟随；模块补光
- 依据：[SRC-MOBILE-LEGACY-002](../sources/README.md#src-mobile-legacy-002)｜如何使用云台智能跟随功能？；模块智能跟随和Mimo有什么区别？；[SRC-MOBILE-LEGACY-009](../sources/README.md#src-mobile-legacy-009)｜PDF物理第6、7、19、20页

<a id="mobile-cl-009"></a>
### MOBILE-CL-009｜一代模块可接DJI Mic Mini或DJI Mic 2发射器，并用手机录音线将音频送至手机。

- 型号：Osmo Mobile 7；组件：一代追踪模块/DJI Mic Mini或Mic2/录音线
- 状态：`verified`；实际核验：2026-09-06
- 条件：Mic2新增于固件V01.02.00.01；当次Mimo版本iOS2.2.5/Android2.2.4。；模块经15厘米手机录音线接手机；Lightning手机另购专用USB-C转Lightning录音线。；手册最多2个同款发射器；MicMini进入接收器配对模式，Mic2进入蓝牙配对模式。
- 限制与不可推论：50厘米云台充电线不能替代录音线；Mimo模块音频调参仅明确支持MicMini。；不把这两款的2发同款规则自动扩推到Mic3。
- 设备：DJI OM 多功能追踪模块；DJI Mic Mini 发射器；DJI Mic 2 发射器；手机录音连接线（USB-C转USB-C，15cm）；路径：TX无线→一代模块→手机录音线→手机
- 支持结论：`conditional`；功能：无线收音；音频传输
- 依据：[SRC-MOBILE-LEGACY-009](../sources/README.md#src-mobile-legacy-009)｜PDF物理第24页；[SRC-MOBILE-LEGACY-002](../sources/README.md#src-mobile-legacy-002)｜云台充电线和手机录音连接线是否通用？；[SRC-MOBILE-LEGACY-010](../sources/README.md#src-mobile-legacy-010)｜PDF物理第5页 2025.04.09

<a id="mobile-cl-011"></a>
### MOBILE-CL-011｜7系列固件新增鸿蒙智能追焦，可搭配官方列出的HarmonyOS 6华为手机系列使用。

- 型号：Osmo Mobile 7；组件：手机系统/云台
- 状态：`verified`；实际核验：2026-09-06
- 条件：云台固件含V01.05.00.01新增能力；手机系统HarmonyOS 6及以上。；本记录设备清单来自读取日中文FAQ；具体手机仍需满足安装条件。
- 限制与不可推论：本记录只肯定有依据的蓝牙配对及系统追焦；NFC配对和横滚轴盖灯交互另列待核。；不由华为系列名推出所有系统版本或所有第三方App均支持。
- 设备：HUAWEI Mate 80 系列；HUAWEI Mate X7 系列；HUAWEI Mate 70 系列；HUAWEI Mate X6 系列；HUAWEI Mate 60 系列；HUAWEI Mate X5 系列；HUAWEI Pura 80 系列；HUAWEI Pura 70 系列；HUAWEI Pocket 2 系列；路径：华为手机系统蓝牙→云台；鸿蒙原生智能追焦
- 支持结论：`conditional`；功能：系统原生智能跟随
- 依据：[SRC-MOBILE-LEGACY-010](../sources/README.md#src-mobile-legacy-010)｜PDF物理第2页；[SRC-MOBILE-LEGACY-002](../sources/README.md#src-mobile-legacy-002)｜鸿蒙智能追焦/如何使用鸿蒙智能追焦？ 适配设备

<a id="mobile-cl-013"></a>
### MOBILE-CL-013｜7系列、6及SE在官方列出的Apple Watch上可用Mimo遥控云台并查看拍摄画面。

- 型号：Osmo Mobile 7；组件：Apple Watch/iPhone/DJI Mimo
- 状态：`verified`；实际核验：2026-09-06
- 条件：手表watchOS 9及以上；iPhone iOS16及以上；iPhone上Mimo2.0.4及以上。；手表与iPhone先配对，两端打开Mimo，iPhone连接云台进入拍摄界面。；当前7系列FAQ明确列7系列、6及SE；清单外新手表不由本条推断兼容。
- 限制与不可推论：手表实时预览带宽不等于成片分辨率；不是FrameTap硬件遥控器。；Apple蓝牙同时使用麦克风不推荐，可另走有线接收器路径。
- 设备：Apple Watch Series 7；Apple Watch Series 8；Apple Watch Series 9；Apple Watch Series 10；Apple Watch SE 2；Apple Watch Ultra 1；Apple Watch Ultra 2；iPhone；路径：手表Mimo→配对iPhone Mimo→蓝牙云台
- 支持结论：`conditional`；功能：预览；拍照录像；虚拟摇杆；智能跟随；横竖切换；回中
- 依据：[SRC-MOBILE-LEGACY-002](../sources/README.md#src-mobile-legacy-002)｜手表遥控/兼容型号、如何使用、有哪些功能、清晰度、麦克风同时使用

<a id="mobile-cl-017"></a>
### MOBILE-CL-017｜尚无本次已读取资料直接确认该旧型号与模块2的完整兼容结论。

- 型号：Osmo Mobile 7；组件：DJI OM 多功能追踪模块 2
- 状态：`pending`；实际核验：2026-09-06
- 条件：必须找到对应云台固件记录或型号明确的模块兼容依据后再使用肯定答案。
- 限制与不可推论：旧支持页只列8P已过时；当前8模块2手册没有给出本型号的明确支持或不支持结论。；未列不等于不支持；不能从磁吸可装、其他型号可用推兼容。
- 设备：DJI OM 多功能追踪模块 2；路径：模块2→该云台的跟随/供电/控制兼容待核
- 支持结论：`unconfirmed`；功能：来源未另列；不作额外推断
- 待核／冲突原因：目前仅取得明确8/8P使用依据，未取得本型号模块2支持或排除证据。
- 依据：[SRC-MOBILE-LEGACY-008](../sources/README.md#src-mobile-legacy-008)｜适用产品（已知列表不完整）；[SRC-MOBILE-8-006](../sources/README.md#src-mobile-8-006)｜PDF物理第6页 产品使用及后续操作；未给出本型号兼容结论

<a id="mobile-cl-022"></a>
### MOBILE-CL-022｜Mic3基本连接的固件新增已有依据，但7系列组合的路数、混用规则与Mimo音频调参仍待核。

- 型号：Osmo Mobile 7；组件：一代追踪模块/DJI Mic 3 TX
- 状态：`pending`；实际核验：2026-09-06
- 条件：先区分固件新增连接能力与具体音频功能。
- 限制与不可推论：不能从手册对MicMini/Mic2的最多2台同款规则扩推Mic3；未核参数不进入确定答复。
- 设备：DJI OM 多功能追踪模块；DJI Mic 3 发射器；路径：Mic3→一代模块→手机音频细项待核
- 支持结论：`unconfirmed`；功能：来源未另列；不作额外推断
- 待核／冲突原因：固件明确新增连接，但已读手册与FAQ尚未补充Mic3专属连接步骤、路数及设置范围。
- 依据：[SRC-MOBILE-LEGACY-010](../sources/README.md#src-mobile-legacy-010)｜PDF物理第2页 2025.10.22；[SRC-MOBILE-LEGACY-009](../sources/README.md#src-mobile-legacy-009)｜PDF物理第24页仅列MicMini/Mic2及相应参数设置范围

## Osmo Mobile 6

<a id="mobile-cl-003"></a>
### MOBILE-CL-003｜本型号手机夹的机械范围为宽67至84毫米、厚6.9至10毫米、重170至290克。

- 型号：Osmo Mobile 6；组件：手机夹/手机
- 状态：`verified`；实际核验：2026-09-06
- 条件：手机及保护壳合计尺寸须在夹持范围内；外接镜头后保持平衡且总重不超过对应上限。
- 限制与不可推论：仅作机械适配筛选，不承诺手机全部App、镜头、录像规格、快门或跟随功能。
- 设备：符合所列机械范围的智能手机；磁吸手机夹；路径：手机夹机械安装
- 支持结论：`conditional`；功能：机械安装；云台承载
- 依据：[SRC-MOBILE-LEGACY-004](../sources/README.md#src-mobile-legacy-004)｜技术参数/适用手机范围；[SRC-MOBILE-LEGACY-004](../sources/README.md#src-mobile-legacy-004)｜保护壳与外接镜头问答

<a id="mobile-cl-014"></a>
### MOBILE-CL-014｜7系列、6及SE在官方列出的Apple Watch上可用Mimo遥控云台并查看拍摄画面。

- 型号：Osmo Mobile 6；组件：Apple Watch/iPhone/DJI Mimo
- 状态：`verified`；实际核验：2026-09-06
- 条件：手表watchOS 9及以上；iPhone iOS16及以上；iPhone上Mimo2.0.4及以上。；手表与iPhone先配对，两端打开Mimo，iPhone连接云台进入拍摄界面。；当前7系列FAQ明确列7系列、6及SE；清单外新手表不由本条推断兼容。
- 限制与不可推论：手表实时预览带宽不等于成片分辨率；不是FrameTap硬件遥控器。；Apple蓝牙同时使用麦克风不推荐，可另走有线接收器路径。
- 设备：Apple Watch Series 7；Apple Watch Series 8；Apple Watch Series 9；Apple Watch Series 10；Apple Watch SE 2；Apple Watch Ultra 1；Apple Watch Ultra 2；iPhone；路径：手表Mimo→配对iPhone Mimo→蓝牙云台
- 支持结论：`conditional`；功能：预览；拍照录像；虚拟摇杆；智能跟随；横竖切换；回中
- 依据：[SRC-MOBILE-LEGACY-002](../sources/README.md#src-mobile-legacy-002)｜手表遥控/兼容型号、如何使用、有哪些功能、清晰度、麦克风同时使用

<a id="mobile-cl-018"></a>
### MOBILE-CL-018｜尚无本次已读取资料直接确认该旧型号与模块2的完整兼容结论。

- 型号：Osmo Mobile 6；组件：DJI OM 多功能追踪模块 2
- 状态：`pending`；实际核验：2026-09-06
- 条件：必须找到对应云台固件记录或型号明确的模块兼容依据后再使用肯定答案。
- 限制与不可推论：旧支持页只列8P已过时；当前8模块2手册没有给出本型号的明确支持或不支持结论。；未列不等于不支持；不能从磁吸可装、其他型号可用推兼容。
- 设备：DJI OM 多功能追踪模块 2；路径：模块2→该云台的跟随/供电/控制兼容待核
- 支持结论：`unconfirmed`；功能：来源未另列；不作额外推断
- 待核／冲突原因：目前仅取得明确8/8P使用依据，未取得本型号模块2支持或排除证据。
- 依据：[SRC-MOBILE-LEGACY-008](../sources/README.md#src-mobile-legacy-008)｜适用产品（已知列表不完整）；[SRC-MOBILE-8-006](../sources/README.md#src-mobile-8-006)｜PDF物理第6页 产品使用及后续操作；未给出本型号兼容结论

## Osmo Mobile SE

<a id="mobile-cl-004"></a>
### MOBILE-CL-004｜本型号手机夹的机械范围为宽67至84毫米、厚6.9至10毫米、重170至290克。

- 型号：Osmo Mobile SE；组件：手机夹/手机
- 状态：`verified`；实际核验：2026-09-06
- 条件：手机及保护壳合计尺寸须在夹持范围内；外接镜头后保持平衡且总重不超过对应上限。
- 限制与不可推论：仅作机械适配筛选，不承诺手机全部App、镜头、录像规格、快门或跟随功能。
- 设备：符合所列机械范围的智能手机；磁吸手机夹；路径：手机夹机械安装
- 支持结论：`conditional`；功能：机械安装；云台承载
- 依据：[SRC-MOBILE-LEGACY-005](../sources/README.md#src-mobile-legacy-005)｜技术参数/适用手机范围；[SRC-MOBILE-LEGACY-006](../sources/README.md#src-mobile-legacy-006)｜保护壳与外接镜头问答

<a id="mobile-cl-015"></a>
### MOBILE-CL-015｜7系列、6及SE在官方列出的Apple Watch上可用Mimo遥控云台并查看拍摄画面。

- 型号：Osmo Mobile SE；组件：Apple Watch/iPhone/DJI Mimo
- 状态：`verified`；实际核验：2026-09-06
- 条件：手表watchOS 9及以上；iPhone iOS16及以上；iPhone上Mimo2.0.4及以上。；手表与iPhone先配对，两端打开Mimo，iPhone连接云台进入拍摄界面。；当前7系列FAQ明确列7系列、6及SE；清单外新手表不由本条推断兼容。
- 限制与不可推论：手表实时预览带宽不等于成片分辨率；不是FrameTap硬件遥控器。；Apple蓝牙同时使用麦克风不推荐，可另走有线接收器路径。
- 设备：Apple Watch Series 7；Apple Watch Series 8；Apple Watch Series 9；Apple Watch Series 10；Apple Watch SE 2；Apple Watch Ultra 1；Apple Watch Ultra 2；iPhone；路径：手表Mimo→配对iPhone Mimo→蓝牙云台
- 支持结论：`conditional`；功能：预览；拍照录像；虚拟摇杆；智能跟随；横竖切换；回中
- 依据：[SRC-MOBILE-LEGACY-002](../sources/README.md#src-mobile-legacy-002)｜手表遥控/兼容型号、如何使用、有哪些功能、清晰度、麦克风同时使用

<a id="mobile-cl-019"></a>
### MOBILE-CL-019｜尚无本次已读取资料直接确认该旧型号与模块2的完整兼容结论。

- 型号：Osmo Mobile SE；组件：DJI OM 多功能追踪模块 2
- 状态：`pending`；实际核验：2026-09-06
- 条件：必须找到对应云台固件记录或型号明确的模块兼容依据后再使用肯定答案。
- 限制与不可推论：旧支持页只列8P已过时；当前8模块2手册没有给出本型号的明确支持或不支持结论。；未列不等于不支持；不能从磁吸可装、其他型号可用推兼容。
- 设备：DJI OM 多功能追踪模块 2；路径：模块2→该云台的跟随/供电/控制兼容待核
- 支持结论：`unconfirmed`；功能：来源未另列；不作额外推断
- 待核／冲突原因：目前仅取得明确8/8P使用依据，未取得本型号模块2支持或排除证据。
- 依据：[SRC-MOBILE-LEGACY-008](../sources/README.md#src-mobile-legacy-008)｜适用产品（已知列表不完整）；[SRC-MOBILE-8-006](../sources/README.md#src-mobile-8-006)｜PDF物理第6页 产品使用及后续操作；未给出本型号兼容结论

## DJI OM 5

<a id="mobile-cl-005"></a>
### MOBILE-CL-005｜本型号手机夹的机械范围为宽67至84毫米、厚6.9至10毫米、重170至290克。

- 型号：DJI OM 5；组件：手机夹/手机
- 状态：`verified`；实际核验：2026-09-06
- 条件：手机及保护壳合计尺寸须在夹持范围内；外接镜头后保持平衡且总重不超过对应上限。
- 限制与不可推论：仅作机械适配筛选，不承诺手机全部App、镜头、录像规格、快门或跟随功能。
- 设备：符合所列机械范围的智能手机；磁吸手机夹；路径：手机夹机械安装
- 支持结论：`conditional`；功能：机械安装；云台承载
- 依据：[SRC-MOBILE-LEGACY-007](../sources/README.md#src-mobile-legacy-007)｜技术参数/适用手机范围；[SRC-MOBILE-LEGACY-007](../sources/README.md#src-mobile-legacy-007)｜保护壳与外接镜头问答

<a id="mobile-cl-020"></a>
### MOBILE-CL-020｜尚无本次已读取资料直接确认该旧型号与模块2的完整兼容结论。

- 型号：DJI OM 5；组件：DJI OM 多功能追踪模块 2
- 状态：`pending`；实际核验：2026-09-06
- 条件：必须找到对应云台固件记录或型号明确的模块兼容依据后再使用肯定答案。
- 限制与不可推论：旧支持页只列8P已过时；当前8模块2手册没有给出本型号的明确支持或不支持结论。；未列不等于不支持；不能从磁吸可装、其他型号可用推兼容。
- 设备：DJI OM 多功能追踪模块 2；路径：模块2→该云台的跟随/供电/控制兼容待核
- 支持结论：`unconfirmed`；功能：来源未另列；不作额外推断
- 待核／冲突原因：目前仅取得明确8/8P使用依据，未取得本型号模块2支持或排除证据。
- 依据：[SRC-MOBILE-LEGACY-008](../sources/README.md#src-mobile-legacy-008)｜适用产品（已知列表不完整）；[SRC-MOBILE-8-006](../sources/README.md#src-mobile-8-006)｜PDF物理第6页 产品使用及后续操作；未给出本型号兼容结论
