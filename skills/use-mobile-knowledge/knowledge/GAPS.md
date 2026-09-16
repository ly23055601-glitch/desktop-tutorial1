# 缺口与资料冲突

这些条目只提示需要核实的问题，不作为肯定能力依据。无命中不等于明确不支持。

## MOBILE-LEGACY-010

- 型号：Osmo Mobile 7P, Osmo Mobile 7
- 问题：7系列中文FAQ描述了NFC碰一碰配对和横滚轴后盖灯交互，型号级硬件与操作适用性尚未核实。
- 状态：`pending`
- 原因：FAQ描述NFC和轴盖灯，7系列手册部件图未列这些标记；缺少明确型号级操作依据。未列本身不是不支持证据。
- 现有依据：[SRC-MOBILE-LEGACY-002](sources/README.md#src-mobile-legacy-002)｜鸿蒙智能追焦/配对、智能灯光交互与显示；[SRC-MOBILE-LEGACY-009](sources/README.md#src-mobile-legacy-009)｜PDF物理第6、7页 部件示意（未列NFC感应区）

## MOBILE-8-COMPATIBILITY-005

- 型号：Osmo Mobile 8
- 问题：iPhone 16e 的 Mobile 8 DockKit 支持状态存在官方来源冲突，暂不作支持或不支持的肯定答复。
- 状态：`conflict`
- 原因：官方兼容表与型号FAQ/手册结论相反，未找到明确纠正声明或可核实机结果；需DJI按手机系统及云台固件确认。
- 现有依据：[SRC-MOBILE-8-008](sources/README.md#src-mobile-8-008)｜第1页iOS iPhone16e行Apple DockKit列，已目视；[SRC-MOBILE-8-002](sources/README.md#src-mobile-8-002)｜DockKit／使用Apple DockKit需要什么设备；[SRC-MOBILE-8-004](sources/README.md#src-mobile-8-004)｜第28页设备要求

## MOBILE-8-AUDIO-004

- 型号：Osmo Mobile 8
- 问题：现已读取的Mobile 8模块2手册只说明跟随、补光、给手机充电；其作为无线麦克风接收端的能力尚未在本组资料中核实。
- 状态：`pending`
- 原因：模块2手册未列音频接收或配对步骤，需要直接型号适配说明补足。
- 现有依据：[SRC-MOBILE-8-006](sources/README.md#src-mobile-8-006)｜第4–5、11–12页目录、组件与功能

## MOBILE-8-SOFTWARE-006

- 型号：Osmo Mobile 8
- 问题：兼容表的遥控器投屏列描述手机到Osmo FrameTap的投屏能力，尚不能据此确认Mobile8与FrameTap的整套云台联控。
- 状态：`pending`
- 原因：Mobile8 FAQ/手册未找到FrameTap整套控制的明确适配说明，需遥控器兼容资料确认。
- 现有依据：[SRC-MOBILE-8-008](sources/README.md#src-mobile-8-008)｜第1页iOS脚注4、Android脚注7；[SRC-MOBILE-8-006](sources/README.md#src-mobile-8-006)｜第6–8页仅8P支持触屏

## MOBILE-8P-TRACKING-007

- 型号：Osmo Mobile 8P
- 问题：手机投屏说明未明确界定Mimo拍摄与模块2跟随的并用范围。
- 状态：`pending`
- 原因：FAQ在同一回答中概述手机投屏和模块跟随，未说明是否指同一前台相机路径；手册明确模块跟随和拍摄不在Mimo内使用。现有表述不构成可肯定并用的依据，也不认定为直接互斥的官方结论。
- 现有依据：[SRC-MOBILE-8P-002](sources/README.md#src-mobile-8p-002)｜通用／多功能追踪模块图传和手机投屏图传的区别是什么？；[SRC-MOBILE-8P-003](sources/README.md#src-mobile-8p-003)｜物理页26／跟随与拍摄末尾提示

## MOBILE-8P-AUDIO-003

- 型号：Osmo Mobile 8P
- 问题：尚未取得足以确认模块2本身能作为DJI Mic无线接收器的官方具体连接说明。
- 状态：`pending`
- 原因：模块2手册/规格与商城一代模块支持表述不能独立确认二代收音路径。
- 现有依据：[SRC-MOBILE-8P-003](sources/README.md#src-mobile-8p-003)｜物理页25／模块组件；页31／连接无线麦克风；[SRC-MOBILE-8P-006](sources/README.md#src-mobile-8p-006)｜比较表／DJI OsmoAudio麦克风直连提示

## MOBILE-C8-004

- 型号：Osmo Mobile 8
- 问题：iPhone16e是否支持Mobile8 DockKit存在官方资料冲突。
- 状态：`conflict`
- 原因：同一组合的官方资料不一致，未获得解决该差异的正式说明。
- 现有依据：[SRC-MOBILE-8-008](sources/README.md#src-mobile-8-008)｜第1页iPhone16e行Apple DockKit列；[SRC-MOBILE-8-002](sources/README.md#src-mobile-8-002)｜DockKit／使用Apple DockKit需要什么设备；[SRC-MOBILE-8-004](sources/README.md#src-mobile-8-004)｜第28页

## MOBILE-C8-017

- 型号：Osmo Mobile 8
- 问题：手机功能表的FrameTap投屏支持尚不足以确认Mobile8全部云台联控功能。
- 状态：`pending`
- 原因：缺少明确Mobile8与FrameTap整套联控的官方依据。
- 现有依据：[SRC-MOBILE-8-008](sources/README.md#src-mobile-8-008)｜第1页iOS脚注4、Android脚注7；[SRC-MOBILE-8-006](sources/README.md#src-mobile-8-006)｜第6–8页

## MOBILE-C8P-002

- 型号：Osmo Mobile 8P
- 问题：iPhone16e的DockKit支持存在官方文档冲突。
- 状态：`conflict`
- 原因：当前兼容表与FAQ/手册对同一型号结论相反。
- 现有依据：[SRC-MOBILE-8P-005](sources/README.md#src-mobile-8p-005)｜物理页1／iOS表iPhone16e行Apple DockKit列；[SRC-MOBILE-8P-003](sources/README.md#src-mobile-8p-003)｜物理页31／设备要求；[SRC-MOBILE-8P-002](sources/README.md#src-mobile-8p-002)｜DockKit追踪功能／使用Apple DockKit需要什么设备？

## MOBILE-CL-016

- 型号：Osmo Mobile 7P
- 问题：尚无本次已读取资料直接确认该旧型号与模块2的完整兼容结论。
- 状态：`pending`
- 原因：目前仅取得明确8/8P使用依据，未取得本型号模块2支持或排除证据。
- 现有依据：[SRC-MOBILE-LEGACY-008](sources/README.md#src-mobile-legacy-008)｜适用产品（已知列表不完整）；[SRC-MOBILE-8-006](sources/README.md#src-mobile-8-006)｜PDF物理第6页 产品使用及后续操作；未给出本型号兼容结论

## MOBILE-CL-017

- 型号：Osmo Mobile 7
- 问题：尚无本次已读取资料直接确认该旧型号与模块2的完整兼容结论。
- 状态：`pending`
- 原因：目前仅取得明确8/8P使用依据，未取得本型号模块2支持或排除证据。
- 现有依据：[SRC-MOBILE-LEGACY-008](sources/README.md#src-mobile-legacy-008)｜适用产品（已知列表不完整）；[SRC-MOBILE-8-006](sources/README.md#src-mobile-8-006)｜PDF物理第6页 产品使用及后续操作；未给出本型号兼容结论

## MOBILE-CL-018

- 型号：Osmo Mobile 6
- 问题：尚无本次已读取资料直接确认该旧型号与模块2的完整兼容结论。
- 状态：`pending`
- 原因：目前仅取得明确8/8P使用依据，未取得本型号模块2支持或排除证据。
- 现有依据：[SRC-MOBILE-LEGACY-008](sources/README.md#src-mobile-legacy-008)｜适用产品（已知列表不完整）；[SRC-MOBILE-8-006](sources/README.md#src-mobile-8-006)｜PDF物理第6页 产品使用及后续操作；未给出本型号兼容结论

## MOBILE-CL-019

- 型号：Osmo Mobile SE
- 问题：尚无本次已读取资料直接确认该旧型号与模块2的完整兼容结论。
- 状态：`pending`
- 原因：目前仅取得明确8/8P使用依据，未取得本型号模块2支持或排除证据。
- 现有依据：[SRC-MOBILE-LEGACY-008](sources/README.md#src-mobile-legacy-008)｜适用产品（已知列表不完整）；[SRC-MOBILE-8-006](sources/README.md#src-mobile-8-006)｜PDF物理第6页 产品使用及后续操作；未给出本型号兼容结论

## MOBILE-CL-020

- 型号：DJI OM 5
- 问题：尚无本次已读取资料直接确认该旧型号与模块2的完整兼容结论。
- 状态：`pending`
- 原因：目前仅取得明确8/8P使用依据，未取得本型号模块2支持或排除证据。
- 现有依据：[SRC-MOBILE-LEGACY-008](sources/README.md#src-mobile-legacy-008)｜适用产品（已知列表不完整）；[SRC-MOBILE-8-006](sources/README.md#src-mobile-8-006)｜PDF物理第6页 产品使用及后续操作；未给出本型号兼容结论

## MOBILE-CL-021

- 型号：Osmo Mobile 7P
- 问题：Mic3基本连接的固件新增已有依据，但7系列组合的路数、混用规则与Mimo音频调参仍待核。
- 状态：`pending`
- 原因：固件明确新增连接，但已读手册与FAQ尚未补充Mic3专属连接步骤、路数及设置范围。
- 现有依据：[SRC-MOBILE-LEGACY-010](sources/README.md#src-mobile-legacy-010)｜PDF物理第2页 2025.10.22；[SRC-MOBILE-LEGACY-009](sources/README.md#src-mobile-legacy-009)｜PDF物理第24页仅列MicMini/Mic2及相应参数设置范围

## MOBILE-CL-022

- 型号：Osmo Mobile 7
- 问题：Mic3基本连接的固件新增已有依据，但7系列组合的路数、混用规则与Mimo音频调参仍待核。
- 状态：`pending`
- 原因：固件明确新增连接，但已读手册与FAQ尚未补充Mic3专属连接步骤、路数及设置范围。
- 现有依据：[SRC-MOBILE-LEGACY-010](sources/README.md#src-mobile-legacy-010)｜PDF物理第2页 2025.10.22；[SRC-MOBILE-LEGACY-009](sources/README.md#src-mobile-legacy-009)｜PDF物理第24页仅列MicMini/Mic2及相应参数设置范围

## 首版资料边界

本库没有设备实测、真实消费者语料或竞品横评。手机兼容表的全部机型未逐项转写；具体手机仍须读取对应原表的型号列、系统条件及脚注。当前保存版本之外的后续固件、App、价格和套装变化需要重新核验。
