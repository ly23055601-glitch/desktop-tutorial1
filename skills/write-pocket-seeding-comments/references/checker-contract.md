# LH13项目验收引擎契约

本项目新稿使用 `2026-09-05-LH13`，入口是 `scripts/check_comment_homogeneity.py`，新状态从 `assets/pocket_comment_state.lh13.template.json` 复制。原 `pocket_comment_state.template.json` 保留为LH12兼容模板，旧版状态不启用本页的新行为。注册表主版本仍是 `2026-09-02-LH5`，新增内容放在 `product-claims.json` 的 `lh13.claims`，仅LH13合并读取

知识库接入后，`lh13.model_ids`补全`pocket_1`、`pocket_2`，基础LH5型号表保持兼容；旧型号可按已确认代际填写，不自动继承新代际claim。知识卡ID与`claim_id`分开：只有知识卡映射到已登记且适用型号的claim，才可在复核当前官方页面后填入`product_facts`；未映射项先补登记。知识库检索、语料规律与产品卡均不改变LH13正文、M/F/S等级、用户经历或审稿接口

## 最终稿与种草审稿

直接读取最终编号稿，每帖2–4条主评，每条0–4条缩进回复，不维护另一份正文。单文件状态顶层填写 `draft_sha256`，值为最终Markdown原始字节的SHA256。多文件使用 `draft_hashes` 对象，以各稿绝对路径为键；仅审稿引用未变而正文变了，也必须重新验稿并更新hash

原 `qa.semantic_review.diversity_review` 和说话者、来源、父句等检查继续生效。新增 `qa.semantic_review.seeding_review` 数组，每个实际交付的 `allocation.id` 恰好一项：

```json
{
  "id": "与allocation.id完全一致",
  "verdict": "passed",
  "reason": "说明本帖如何让观看者产生具体Pocket兴趣，以及产品不是装饰性点名的依据",
  "interest_entries": [
    {
      "group": 1,
      "exact_copy_quote": "对应主评的实际原文片段",
      "interest": "观看者从这句话获得的具体Pocket兴趣"
    }
  ]
}
```

`verdict` 允许 `passed` 或 `revise`，未通过或未填写不能交付。至少引用一条实际主评，引用不能只有型号，组号不得重复或越界。被引用组须有实际 `product_connection`，不能把未记录产品关联的纯画面辅条当作整帖种草依据。无需规定参数数量、点名比例或种草类型；纯画面组可保留，但每帖必须经审稿确认有具体产品兴趣。检查器仅验证审稿记录、引用和稿件绑定，不能自动判断心动程度、活人感或“产品名是否真的只是装饰”

## 独立官网事实

写作表达仍沿用既有 `observed`、`personal_need` 等 `claim_mode`，不为加入普通产品事实而改写主导表达。每组可新增 `product_facts`，纯画面、纯感受和真实疑问可为空：

```json
{
  "product_facts": [
    {
      "claim_id": "4p_3x_physical_lens",
      "target_model": "pocket_4p",
      "source_urls": ["https://store.dji.com/cn/product/osmo-pocket-4p-vlog-combo?set_region=CN"],
      "checked_at": "2026-09-05",
      "exact_copy_quote": "4p那个3倍镜头"
    }
  ]
}
```

- 引用必须来自本组单条主评或回复的实际正文，可仅引用最小事实片段，不必包含“想试试”等情绪前缀；需覆盖事实内容，不能引用型号后借同组另一句补证
- 每项校验注册claim、明确型号、引用匹配、官方页面、日期及该claim不可省略的限定。同句中不同事实需分别映射；新事实先扩展注册表，不能换成低S级、标成疑问或用P0跳过
- `personal_need` 仍为S0/S1、`claim_id`为空，独立事实放入 `product_facts`。`observed` 可以保留原S级和既有claim字段；语义类型不提高事实等级
- `product_facts` 不提高原帖M/F，不表示原片启用某功能，不证明产品造成了当前画面。原片型号、功能演示、因果及比较仍走既有证据门禁
- 组内独立记录按自身来源核验；既有section `fact_status` 若声明某claim，仍必须满足它的P级和来源。P0不能用于掩盖未登记的断言
- P1须为有效且非未来的核验日期；P2模式受限事实须当日重新核验。日期不会自动延用为“已核验”

本轮新增或补充的claim：`4p_3x_physical_lens`、`4p_zoom_button`、`p4_spinshot_auto`，以及双镜头1倍/3倍称呼和 `shared_intelligent_tracking` 的当前官网来源。实体变焦键与自动旋转已加入事实检测；明确支持语句需要证据，正常倍率和跟随问句不因关键词命中而误判。旋转不能同时开启跟随的禁写组合单独拦截

官方来源只接受HTTPS的 `store.dji.com`、`www.dji.com`、`dji.com`、`repair.dji.com`。比较商城页面时忽略推广/地区/变体查询参数；帮助页必须是 `/help/content` 且匹配 `customId`，不能用同域另一个帮助文章补证

## 新批次填表顺序

1. 复制LH13模板，只保留真实输入对应的allocation；每帖先写成立的正文，再按实际主评数量复制唯一的group结构并连续编号。不要复制accepted-state的passed结论或个人材料
2. `allocation.draft_path` 优先于 `block.draft_path`；相对路径均相对state JSON所在目录解析。`draft_paths` 是交付台账，不能覆盖前述绑定。`input_path`、`evidence_path`、`capture_policy.batch_ledger_path`记录实际文件；来源文件不等于正文文件
3. 为每条保留一个真实 `main_anchor_ids`，填写自由短句 `dominant_expression` 和 `product_connection`；只有整组纯画面且无产品事实时关联可为空。`personal_need`另填 `need_connection`
4. 初始清空旧 `product_facts`、个人来源、dialogue.replies、reply_personal_contexts、两类审稿数组、hash与旧QA结果。按本轮原文逐项重建；零回复不留旧回复，别把旧真实经历转给新角色
5. 完成事实及独立语义审稿后填review，再计算最终MD原始字节SHA256并跑检查。`accepted-state.json`仅作填表结构示意，不能直接替代新批次证据

| 字段 | 填写约束 |
|---|---|
| `scene_need.tags` | 字符串数组；N0为空，N1/N2须有精确标签及evidence。普通观察/需求可自由命名；`scenario_fit`须与对应claim的 `scene_need_tags` 至少一项匹配，可在注册表选择实际适用的键，不能靠换标签制造证据 |
| `seeding_mechanism`、`purchase_stage`、`audience_perspective` | 自由短句，写实际动机、阶段和关注视角；没有硬性枚举，不用中文硬凑同一个模板 |
| `main_moves` | 1–2项枚举：`observation/reaction/preference/question/disagreement/joke/need/product/benefit/boundary` |
| `seed_layers.main/replies` | 枚举 `need/question/product/benefit/boundary`；main最多2项，replies最多5项，描述实际正文而非预填数量；零回复保持replies为空 |
| `claim_mode` | `observed/personal_need/attributed/scenario_fit/causal/comparative`；真实疑问通常仍是observed，question只属于main_moves，不能把claim_mode改成不存在的question来逃过事实检查 |
| `benefit_basis` | `visual/workflow/product`；personal_need仅visual或workflow |
| `model_status` | 未知为M0；仅标题/作者声明为M1、evidence_type=`author_claim`、claimed_model填真实型号、confirmed_model=`unknown`；M2需要机身或UI等确认，水印不能升级 |
| `feature_use/fact_status` | 没有功能材料F0、claim_ids空；未核验官网P0、verified_claim_ids/source_urls空；不因为想使用某功能而提升F。P1/P2声明的每个claim须有对应官网来源与日期 |
| `target_s_level/actual_s_level` | 明确填写且actual不高于target；S0可以承载贴帖互动，personal_need上限S1。`strong_seed_group`无真实S2/S3时为null，不能用强种草等级替代本帖兴趣审稿 |
| `personal_context` | 只放该说话者真实用户材料的source_ref/facts/models；“拥有Pocket”不等于已确认具体型号。回复中的其他说话者不得借主评来源 |

### 只有用户材料，没有平台链接

只有用户已经提供充分文本/截图等材料、无需实时读取时使用。材料保存为真实本地 `.md` 或 `.txt` 文件，以 `## T1`、`## T2` 分节；合成验收输入必须明确标为合成材料，不能标为平台采集成果

正文标题写 `## 1｜user-material:T1`，allocation的 `id` 为 `T1`、`canonical_url` 为 `user-material:T1`，`capture_policy.primary_surface` 为 `user_supplied_evidence`，再填：

```json
{"user_material":{"path":"input-evidence.md","anchor":"T1","exact_quote":"该标题下实际存在的用户材料原文片段"}}
```

ID限英文字母开头及字母、数字、下划线、短横线，最长64字符。`path`相对state目录解析；检查器会实际读取文件、核对 `## ID` 锚点与该节原文，不能借另一帖的片段。失败/暂停ID不得改成该定位绕过停项；已知平台来源仍用原URL，不在user_material中用origin_url/source_url等重映射。此入口不授权重新获取任何被限制的远程材料，也不证明本地文件内容一定来自用户，来源真实性仍需审稿

## 运行与边界

在项目根目录运行：

```sh
python3 .agents/skills/write-pocket-seeding-comments/scripts/check_comment_homogeneity.py .agents/skills/write-pocket-seeding-comments/assets/accepted-comments.md --state .agents/skills/write-pocket-seeding-comments/assets/accepted-state.json --seeding-policy strict --format json
python3 -m unittest discover -s .agents/skills/write-pocket-seeding-comments/tests -p 'test*.py'
```

`--seeding-policy strict` 是事实验收入口；`--seeding-policy off` 只供格式诊断，不能作为整体通过。单独的 `--strict` 会把全部风格提示变成非零退出，不应用它设置字数、逗号或点名比例配额。所有提示仍须逐项语义审稿，不能为消掉提示而删除有效种草

新增测试覆盖：2/3/4主评与0–4回复混排、纯画面辅条、独立事实与表达模式并存、普通疑问/反问/后续断言、变焦键/旋转、第四组及无名主评下回复事实、P0不绕过、来源与帮助文章身份、日期/型号/原文片段、原片因果隔离、禁写组合及正向事实被反向否定句借证、审稿引用/稿件hash、真实本地用户材料定位、模板与旧版兼容。原206条回归保持未改

这些规则以显式关键词和已登记指纹定位风险，不能识别所有自然语言事实、影射或复合断言，也不能证明官方链接的实际内容为真。每条新增产品事实与个人经历仍须人工或模型逐句核验；新增产品事实先完成官网读取和注册，再写入验收状态。通过测试、补填passed或重新算hash均不能代替语义审稿
