# Nano 首版验收

验收日期：2026-09-06。本轮结构检查与独立资料复核已完成。事实核验依据记录在各条目的来源中；工作问题的通过只针对有来源、保留条件的回答。
## 必须回答的工作问题

| 编号 | 问题 | 核查依据 | 实际结果 |
|---|---|---|---|
| Q01 | 整套Nano可以下水10米吗？ | [NANO-MAN-013](../products/guide.md#nano-man-013)、[NANO-MAN-014](../products/guide.md#nano-man-014)、[NANO-MAN-015](../products/guide.md#nano-man-015) | 通过 |
| Q02 | 52克的小相机能独立拍200分钟吗？ | [NANO-FORM-002](../products/guide.md#nano-form-002)、[NANO-PWR-001](../products/guide.md#nano-pwr-001)、[NANO-PWR-002](../products/guide.md#nano-pwr-002) | 通过 |
| Q03 | 4K60长续航条件是什么？ | [NANO-PWR-003](../products/guide.md#nano-pwr-003) | 通过 |
| Q04 | 插1TB卡就能直接长时间录制吗？ | [NANO-STO-002](../products/guide.md#nano-sto-002)、[NANO-STO-003](../products/guide.md#nano-sto-003)、[NANO-STO-007](../products/guide.md#nano-sto-007) | 通过 |
| Q05 | 可以用哪些DJI麦克风，接收器怎么接？ | [NANO-AUD-002](../products/guide.md#nano-aud-002)、[NANO-AUD-003](../products/guide.md#nano-aud-003)、[NANO-AUD-004](../products/guide.md#nano-aud-004)、[NANO-AUD-005](../products/guide.md#nano-aud-005) | 通过 |
| Q06 | 连接无线麦时还能分体查看画面吗？ | [NANO-AUD-007](../products/guide.md#nano-aud-007) | 通过 |
| Q07 | 骑行直接挂磁吸挂绳就行吗？ | [NANO-MAN-002](../products/guide.md#nano-man-002)、[NANO-MAN-003](../products/guide.md#nano-man-003)、[NANO-ACC-001](../products/guide.md#nano-acc-001)、[NANO-ACC-002](../products/guide.md#nano-acc-002) | 通过 |
| Q08 | 4K120慢动作有和普通视频相同的防抖吗？ | [NANO-IMG-005](../products/guide.md#nano-img-005)、[NANO-STAB-002](../products/guide.md#nano-stab-002)、[NANO-STAB-003](../products/guide.md#nano-stab-003)、[NANO-STAB-004](../products/guide.md#nano-stab-004) | 通过 |
| Q09 | 参数页只写4:3和16:9，是不支持9:16吗？ | [NANO-IMG-012](../products/guide.md#nano-img-012) | 通过 |
| Q10 | 拍孩子或宠物会自动追焦吗？ | [NANO-IMG-003](../products/guide.md#nano-img-003) | 通过 |
| Q11 | 室内开超级夜景就不会模糊吗？ | [NANO-IMG-015](../products/guide.md#nano-img-015)、[NANO-IMG-016](../products/guide.md#nano-img-016) | 通过 |
| Q12 | 任意USB-C手机都能直接导片吗？ | [NANO-STO-005](../products/guide.md#nano-sto-005)、[NANO-APP-002](../products/guide.md#nano-app-002)、[NANO-APP-003](../products/guide.md#nano-app-003) | 通过 |
| Q13 | 能用专用清洁液擦镜头吗？ | [NANO-MAN-024](../products/guide.md#nano-man-024) | 通过：明确保留待核 |
| Q14 | 长按哪个按键可以休眠？ | [NANO-MAN-023](../products/guide.md#nano-man-023) | 通过：明确保留待核 |

## 实际检查记录

- 80条事实的JSONL解析、必需字段、唯一ID、型号与状态检查通过；78条verified、2条pending。
- 7份来源文件存在且SHA256与台账一致；事实来源引用与7张场景卡的关联均有效；场景没有将pending当作肯定产品依据。
- 本轮检查152个本地文件链接与显式锚点，全部可解析。
- 项目共用写手技能的官方quick_validate校验通过；Nano索引同时接入项目AGENTS和共用写手入口，直接调用Nano技能也有本地路由。
- 独立复核逐一检查以上14个工作问题，并回查官网快照、手册、4页累计固件记录和兼容表。配件表Nano列及关键安装图经目视核对。
- 已修正两处复核发现：NANO-PWR-003补齐16:9画幅及FAQ定位；NANO-SCENE-007将镜头朝前合体条件限定到卡/电脑/手机有线导出，不再套用于Mimo无线导出。
- 休眠与清洁液仍是官方表述待核项。Q13/Q14通过说明知识库能正确指出差异，不表示取得了官方澄清。

本轮为资料、结构与问答核验，没有进行设备实拍、续航实测或社媒用户研究；七张场景卡均维持编辑假设。
