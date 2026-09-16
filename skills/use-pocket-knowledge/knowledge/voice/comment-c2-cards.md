# C2评论：补单句证据，不补线程

实际读取14篇合格train作品的119条C2评论：Pocket4为7篇65条，Pocket4P为7篇54条。input21没有评论导出，input22型号未明，均不作为本次支持；holdout正文未参与分析。导出全部缺少根/引用关系字段，`thread_role=unknown`，不能称为已证主评或楼中楼，也不能据语义和昵称补父句。

本次优先延伸已有机制，给3张C1卡补证据，另新增2张有边界的case。共引用12条C2评论、7个独立作品/7个发布账号，其中8条来自Pocket4P讨论作品、4条来自Pocket4讨论作品。评论仍只保存在`corpus/comments.jsonl`；没有复制原记录或增加主评、父句讨论计数。

| 卡片 | 当前范围 | C2补充了什么 |
|---|---|---|
| comment_c1_001 | pattern，5作品 | input23/24的参数适用拍照吗、是否视频截取、App传到手机疑问；不新增承接证据 |
| comment_c1_003 | case，2作品 | input23只支持重复调参顾虑；听说能保存后仍需步骤的对话仍仅由C1实际父链支持 |
| comment_c1_004 | 从case扩为pattern，4作品/4发布账号 | input31/34/38将4/4P选择连到旅行、自述新手、排除价格后关注发热或人像；不凭昵称合并发言者 |
| comment_c2_001 | case，2篇Pocket4P讨论作品 | input38/40把建议具体到先熟悉基础、镜头切换或吃饭散步通勤；不证明这些建议已被采用或有效 |
| comment_c2_002 | case，1篇Pocket4P讨论作品 | input37同一句交代只有机器，再问配件需要；未提供用途，不能据此列必买配件或假定腾手场景 |

`evidence_batches`区分C1/C2；`evidence_extensions`写明新句能支持到哪里。C2摘句的角色始终unknown，`thread_links`没有新增一条。C1的原父句关系仍仅对原记录成立；新增独立问题不证明它是旧句的回复。作品作者去重不等于评论者认证，更不表示人口比例、商业独立性或真实使用效果。

场景002、003、005、009增加独立的C2文字支持层。原evidence/editorial_hypothesis依据、产品事实条件和公共帖子层不变；关于配件的单句没有强接到腾手/固定场景。所有硬件、参数、发热、色彩、传输和效果说法仍保留说话者归属，写产品事实时另查官方来源。

本次未采用纯推广、无具体观点的短句、未读媒体占位或需要推测画面的描述作为机制证据。已读不等于已验证：例如评论中的`[视频] 19s`只说明导出带有媒体占位，不能据此评价画面。

构建与来源核对见[build_comment_c2_cards.py](build_comment_c2_cards.py)和[comment-c2-build-report.json](comment-c2-build-report.json)。C1已审版本存于`revisions/comment-c1-before-c2.jsonl`作为变更基线，不计原话或作品数量。C2重建会恢复本次变更卡为待审；C1构建器在存在C2扩展时拒绝覆盖，避免丢掉新证据。

本次5张变化卡和4处场景支持已通过独立模型审读，原句、定位、父句隔离与归纳范围均无阻断问题；两处措辞建议已落实。详见[comment-c2-independent-review.json](comment-c2-independent-review.json)。本轮按用户要求以现有材料收尾，不再扩量或等待额外批次。
