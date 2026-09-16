# 模块与知识路由

仓库：https://github.com/ly23055601-glitch/desktop-tutorial1

raw 根地址：`https://raw.githubusercontent.com/ly23055601-glitch/desktop-tutorial1/`

优先使用 DeepSeek++ 导入元数据中实际提供的 `Commit` 值作为 `ref`，以便规则与知识版本一致；没有该值时用 `main` 并记录本次版本未固定。读取公式是 `raw根地址 + ref + '/' + 下表路径`。只有工具返回正文才记入已读资料；不得只根据文件名描述内容。遇到超长文件，使用已授权的本地副本检索或请用户提供相关段落，不把截断输出视为全文。

## 当前阶段允许的模块

| 阶段 | 作用 | 仓库根目录相对路径 |
| --- | --- | --- |
| 1 | 完整链接集采集规则 | `skills/read-social-links-with-social-helper/MODULE.md` |
| 2 Pocket | Pocket 知识 | `skills/use-pocket-knowledge/knowledge/INDEX.md` |
| 2 Mobile/OM | 手机云台知识 | `skills/use-mobile-knowledge/knowledge/INDEX.md` |
| 2 Mic | 无线麦克风知识 | `skills/use-mic-knowledge/references/knowledge/INDEX.md` |
| 2 Nano | Nano 知识 | `skills/use-nano-knowledge/knowledge/INDEX.md` |
| 2 360 | Osmo 360 知识 | `skills/use-osmo360-knowledge/knowledge/INDEX.md` |
| 3 | 共享写手 | 本总控附带的 `references/writing.md`，不再启动一个写手 Skill |
| 4 | 全批去重质检 | 本总控附带的 `references/quality.md` |
| 5（可选） | 用户要求的每日台账 | `skills/run-daily-comment-training/MODULE.md`，只用留档与计量部分 |

知识阶段先读对应索引，再沿索引取少量与当前问题相关的事实。确需完整检索说明时读取对应 `skills/use-*-knowledge/MODULE.md`，其中转入写作、社媒和旧审查的路由不在本阶段执行。`MANIFEST.json` 列出全部 20 个内部模块，不逐一加载。

## 产品适配

- Pocket：精确区分代际，型号未知只用 Pocket/大疆Pocket；评论及回复正文不用 Osmo（来源名称不受此限）。不要把 Action、Nano、360 或 OM 的能力移植过来。适配资料为 `writer-core/products/dji/pocket/MODULE.md`。
- Mobile/OM：`product_line=osmo_mobile`；区分手机、App、云台、配件和跟随路径，能夹住不代表全兼容；保留 Osmo。适配资料为 `writer-core/products/dji/mobile/MODULE.md`。
- Mic：区分发射器、接收器、宿主连接、内录与输出，不把未知音频当已听取；适配资料为 `writer-core/products/dji/mic/MODULE.md`。
- Nano：区分主相机、图传模块、配件、固件和模式；适配资料为 `writer-core/products/dji/nano/MODULE.md`。
- Osmo 360：区分代际、全景/平面、拍摄/导出、防水/水下成像；保留 Osmo；适配资料为 `writer-core/products/dji/osmo360/MODULE.md`。

适配资料仅补约束，不把其中“先读共享写手”等旧路由执行为新任务。旧项目代码只有在当次任务明确或可核实映射时才使用，不从历史任务名称猜目标。

## 相对路径和原电脑路径

从 raw 文档打开相对链接时，以该文档所在目录为基准归一化 `../`，保留同一仓库与 ref；不能把文件路径直接当作本机已存在路径。已下载完整仓库时以实际仓库根目录解析。

旧资料中的 `/Users/...`、`.codex/skills/...`、原项目 `knowledge/...` 只是历史路径，不能访问当前设备上猜测的同名位置。本包有效路径以本表、模块自身可解析的包内链接和 MANIFEST 为准。找不到对应文件时记为缺失；禁止循环加载旧项目路由寻找另一套写法。

采集模块依赖用户已连接的社媒助手或等价、已授权的材料读取能力；普通 DeepSeek++ 导入不会自动安装这些工具。没有可用连接时用用户提供的材料，明确证据范围。
