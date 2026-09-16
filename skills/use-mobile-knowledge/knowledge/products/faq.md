# 常见问题

这些答案是带编号依据的阅读摘要；引用时核对完整条件、相关缺口和当前官方资料。

<a id="q01"></a>
## Q01｜8不装模块还能跟随吗？

可以选择Mimo内跟随，适配手机还可走DockKit或鸿蒙原生跟拍。先确认手机、系统、App及固件；原生路径不能直接泛化所有手机。

依据：[MOBILE-8-TRACKING-001](osmo_mobile_8.md#mobile-8-tracking-001)、[MOBILE-8-TRACKING-004](osmo_mobile_8.md#mobile-8-tracking-004)、[MOBILE-8-TRACKING-006](osmo_mobile_8.md#mobile-8-tracking-006)

<a id="q02"></a>
## Q02｜蓝牙能按快门，就能在任何原生相机里自动跟人吗？

不能这样推断。快门是相机控制，主体跟随需满足Mimo、硬件模块或系统跟拍路径各自的条件；具体手机支持表中的“系统相机”按键列也不是DockKit列。

依据：[MOBILE-8-CONTROLS-005](osmo_mobile_8.md#mobile-8-controls-005)、[MOBILE-C8-007](../compatibility/guide.md#mobile-c8-007)、[MOBILE-8-TRACKING-004](osmo_mobile_8.md#mobile-8-tracking-004)

<a id="q03"></a>
## Q03｜8装模块2后能和8P一样框选任意物品吗？

8在V01.02.02.02更新后支持模块2的人物、猫狗和车辆跟随；触屏、智能跟随设置及其他物体手动框选在模块2手册中限定8P。支持同一个配件不代表全部操作相同。

依据：[MOBILE-8-TRACKING-007](osmo_mobile_8.md#mobile-8-tracking-007)、[MOBILE-C8-011](../compatibility/guide.md#mobile-c8-011)、[MOBILE-8P-TRACKING-004](osmo_mobile_8p.md#mobile-8p-tracking-004)

<a id="q04"></a>
## Q04｜8P装一代模块，FrameTap能看到模块画面吗？

一代模块不能向FrameTap投屏。模块2追踪预览来自模块镜头；手机投屏来自手机屏幕，另按手机和系统连接，不能把两者混写。

依据：[MOBILE-C8P-007](../compatibility/guide.md#mobile-c8p-007)、[MOBILE-8P-CONTROLS-004](osmo_mobile_8p.md#mobile-8p-controls-004)、[MOBILE-8P-CONTROLS-005](osmo_mobile_8p.md#mobile-8p-controls-005)

<a id="q05"></a>
## Q05｜FrameTap的25米图传就是25米稳定遥控吗？

不是同一口径。遥控记录为距离云台10米范围；25米Wi-Fi图传来自特定手机和空旷、无干扰、无遮挡测试。实际范围按对应路径及环境判断。

依据：[MOBILE-8P-CONTROLS-003](osmo_mobile_8p.md#mobile-8p-controls-003)、[MOBILE-8P-CONTROLS-004](osmo_mobile_8p.md#mobile-8p-controls-004)

<a id="q06"></a>
## Q06｜8P开跟随和补光也能10小时吗？

10小时测试仅配FrameTap且云台调平静置：分体蓝牙无操作4小时、合体6小时。模块2跟随关灯约5小时，跟随且最亮补光约4小时；一代模块对应约4.5和3小时。给手机充电还会缩短续航。

依据：[MOBILE-8P-POWER-001](osmo_mobile_8p.md#mobile-8p-power-001)、[MOBILE-8P-POWER-002](osmo_mobile_8p.md#mobile-8p-power-002)、[MOBILE-8P-POWER-003](osmo_mobile_8p.md#mobile-8p-power-003)、[MOBILE-8P-POWER-004](osmo_mobile_8p.md#mobile-8p-power-004)

<a id="q07"></a>
## Q07｜8与8P的10小时能直接横比吗？

应先读测试组合：8为无额外配件、调平静置，8P包含遥控器的分体与合体阶段。开启模块、补光或手机供电后的工况另算，不能当同一种持续拍摄实测。

依据：[MOBILE-8-POWER-002](osmo_mobile_8.md#mobile-8-power-002)、[MOBILE-8-POWER-003](osmo_mobile_8.md#mobile-8-power-003)、[MOBILE-8P-POWER-001](osmo_mobile_8p.md#mobile-8p-power-001)

<a id="q08"></a>
## Q08｜总重300克以内，带厚壳和外接镜头就一定兼容吗？

还要看宽度、手机连壳厚度、镜头遮挡与配平。8P适用厚度6.9–11毫米，8为6.9–10毫米；两款推荐宽度67–84毫米、重量170–300克。外接镜头按整个手机组合核对，软件功能再查兼容表。

依据：[MOBILE-8P-COMPATIBILITY-001](osmo_mobile_8p.md#mobile-8p-compatibility-001)、[MOBILE-8P-COMPATIBILITY-002](osmo_mobile_8p.md#mobile-8p-compatibility-002)、[MOBILE-8P-COMPATIBILITY-003](osmo_mobile_8p.md#mobile-8p-compatibility-003)、[MOBILE-8-COMPATIBILITY-001](osmo_mobile_8.md#mobile-8-compatibility-001)、[MOBILE-8-COMPATIBILITY-002](osmo_mobile_8.md#mobile-8-compatibility-002)

<a id="q09"></a>
## Q09｜iPhone16e能用8或8P的DockKit吗？

当前官方材料不一致：手机功能表列支持，FAQ／手册又明确排除iPhone16e。本库保留双方依据，在官方澄清前不作支持或不支持的肯定答复；不把这一冲突扩展到所有iPhone。

依据：[MOBILE-C8-004](../compatibility/guide.md#mobile-c8-004)、[MOBILE-C8P-002](../compatibility/guide.md#mobile-c8p-002)

<a id="q10"></a>
## Q10｜7与7P也能360°水平无限位吗？

7/7P的平移控制范围为−99°至210°，结构范围−109°至222°；不能继承8和8P的平移轴无限位能力，也不能用旋转拍摄模式代替该硬件判断。

依据：[MOBILE-LEGACY-001](osmo_mobile_7p.md#mobile-legacy-001)、[MOBILE-8-STABILIZATION-001](osmo_mobile_8.md#mobile-8-stabilization-001)、[MOBILE-8P-STABILIZATION-002](osmo_mobile_8p.md#mobile-8p-stabilization-002)

<a id="q11"></a>
## Q11｜旧款自拍杆、三脚架与拨轮怎样区分？

7P有内置延长杆、三脚架和拨轮；7有内置三脚架、无内置延长杆，使用变焦滑杆。6有内置延长杆和侧拨轮；OM5有内置延长杆及变焦滑杆；SE的变焦滑杆与M键模式控制另见对应档案。6与OM5的三脚架为外接；SE没有内置延长杆或三脚架。[结构补充](differences.md#旧款机身结构补充)有手册图文定位。

依据：[MOBILE-7P-identity-001](osmo_mobile_7p.md#mobile-7p-identity-001)、[MOBILE-7-identity-001](osmo_mobile_7.md#mobile-7-identity-001)、[MOBILE-7P-controls-001](osmo_mobile_7p.md#mobile-7p-controls-001)、[MOBILE-7-controls-001](osmo_mobile_7.md#mobile-7-controls-001)、[MOBILE-6-controls-001](osmo_mobile_6.md#mobile-6-controls-001)、[MOBILE-6-controls-002](osmo_mobile_6.md#mobile-6-controls-002)、[MOBILE-6-kits-001](osmo_mobile_6.md#mobile-6-kits-001)、[MOBILE-OM5-identity-001](dji_om_5.md#mobile-om5-identity-001)、[MOBILE-OM5-controls-001](dji_om_5.md#mobile-om5-controls-001)、[MOBILE-SE-controls-001](osmo_mobile_se.md#mobile-se-controls-001)

<a id="q12"></a>
## Q12｜7系列能用鸿蒙智能追焦吗？

其2025-10-22 V01.05.00.01发布记录明确新增该功能，仍需HarmonyOS 6及以上系统和官方适配的华为机型，按兼容记录逐项核对。当前7系列FAQ中的NFC和轴盖灯描述未核清型号适用范围，不把8系列操作直接套入7。

依据：[MOBILE-LEGACY-009](osmo_mobile_7p.md#mobile-legacy-009)、[MOBILE-LEGACY-010](osmo_mobile_7p.md#mobile-legacy-010)

<a id="q13"></a>
## Q13｜7P的一代模块能连接Mic3吗？

官方V01.05.00.01发布记录明确新增DJI Mic3发射器支持。当前FAQ／手册部分列表未同步列出，不由遗漏认定不支持；Mic3的双发射器路数、混连和App设置不能从MicMini/Mic2说明直接扩推。

依据：[MOBILE-LEGACY-011](osmo_mobile_7p.md#mobile-legacy-011)

<a id="q14"></a>
## Q14｜所有手机在Mimo里都是相同分辨率与跟随版本吗？

不同手机的接口开放和软件适配不同。当前兼容表中iPhone12系列对应跟随7.0，部分后续iPhone为8.0；镜头、慢动作、双摄增强等项目逐行核对，不能把手机系统相机规格原样搬到Mimo。

依据：[MOBILE-8-TRACKING-002](osmo_mobile_8.md#mobile-8-tracking-002)、[MOBILE-C8-005](../compatibility/guide.md#mobile-c8-005)、[MOBILE-C8-006](../compatibility/guide.md#mobile-c8-006)、[MOBILE-8P-SOFTWARE-004](osmo_mobile_8p.md#mobile-8p-software-004)

<a id="q15"></a>
## Q15｜标准套装默认含追踪模块和麦克风吗？

已核8与8P中国大陆标准套装清单都没有列追踪模块或麦克风。8的AI套装列一代模块，8P的AI套装含模块2，8P全能Vlog套装还包含Mic Mini 2发射器及手机版接收器；购买前还需核对当前SKU，不从产品页展示配件推定随箱附送。

依据：[MOBILE-8-KITS-001](osmo_mobile_8.md#mobile-8-kits-001)、[MOBILE-8-KITS-002](osmo_mobile_8.md#mobile-8-kits-002)、[MOBILE-8P-KITS-001](osmo_mobile_8p.md#mobile-8p-kits-001)、[MOBILE-8P-KITS-002](osmo_mobile_8p.md#mobile-8p-kits-002)、[MOBILE-8P-KITS-004](osmo_mobile_8p.md#mobile-8p-kits-004)

<a id="q16"></a>
## Q16｜内置三脚架在户外有风的桌上也适用吗？

官方限定为无风、稳定、水平表面；其他环境应核对另接三脚架及具体摆放条件。云台的防抖能力不替代机位支撑条件。

依据：[MOBILE-8-STABILIZATION-005](osmo_mobile_8.md#mobile-8-stabilization-005)、[MOBILE-8P-MAINTENANCE-002](osmo_mobile_8p.md#mobile-8p-maintenance-002)、[MOBILE-LEGACY-006](osmo_mobile_7p.md#mobile-legacy-006)

<a id="q17"></a>
## Q17｜旅行自拍场景是来自真实消费者吗？

七类场景均为编辑推演，只解释任务与产品条件之间的关系，不能当真实评价或实拍效果。训练中的购买、持有与感受保存于独立人物状态，不进入本库。

依据：[场景性质与写作调用](../INDEX.md#资料性质)、[场景卡](../scenarios/guide.md)

<a id="q18"></a>
## Q18｜只写“大疆OM”时默认用8P吗？

先确定具体代际。型号未明只能讨论产品线层面的明确问题，不替原帖确定设备，也不自动取最新款的功能。

依据：[型号目录](models.jsonl)、[检索说明](../INDEX.md#本地检索)

<a id="q19"></a>
## Q19｜查不到某手机或配件，是不是不兼容？

无命中只说明本库没有找到已核依据。查对应官方兼容表、具体连接路径与脚注；来源未明确的组合登记为待核，不改写成不支持。

依据：[兼容与连接记录](../compatibility/guide.md)、[缺口清单](../GAPS.md)

<a id="q20"></a>
## Q20｜在op里直接调用Mobile评论技能会使用本库吗？

项目AGENTS和项目写手入口都已加入本库路由。先按型号查事实与场景，再进入共享写法；新稿仍为training_fiction，已读索引不重复加载，真实资料核验与旧稿审查保持原分支。

依据：[写作调用](../INDEX.md#在写手能力库中使用)、[跨项目 Mobile 能力入口](../../MODULE.md)
