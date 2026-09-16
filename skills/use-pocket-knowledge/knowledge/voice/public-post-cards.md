# 新公共帖子表达材料

2026-09-06，从已经读过的50篇小红书train帖子中选入37条原话：16条以Pocket4为讨论主型号、19条Pocket4P、2条并列型号仍为unknown。型号沿用当前corpus/works审读，不是作者持有型号。13篇只有标签、泛教程口号或未展开导语，保留在analysis笔记中，不进入可调用记录。

记录ID为 `post:xiaohongshu:<work_id>`；`material_kind/source_kind: public_post`、`speaker_scope: work_author`、`thread_role: post`。实际正文不改字，原始XLSX行列、规范化行号、采集及发布时间均可追溯。没有图片、连续视频、音轨或评论内容；对450条主评和父句回复的新增贡献均为0。

| 卡片 | 内容 | 支持范围 |
|---|---|---|
| post_voice_001 | 认可与具体不便并存 | pattern，3作品/3账号 |
| post_voice_002 | 用具体步骤说明使用负担 | pattern，3作品/3账号 |
| post_voice_003 | 原因不确定时怎样求助 | pattern，3作品/3账号 |
| post_voice_004 | 用自己的观感标准表达偏好 | pattern，3作品/3账号 |
| post_voice_005 | 用少做哪些动作说明方便 | pattern，3作品/3账号 |
| post_voice_006 | 先说拍什么再问选择 | case，1作品/1账号 |
| post_voice_007 | 配方保留现场调整空间 | case，1作品/1账号；教程作者表达 |
| post_voice_008 | 退留犹豫与继续尝试 | case，2作品/同一账号；不推导改善因果 |

8张新卡共引用17个作品、16个导出作者账号。pattern支持来自14个独立作品和14个账号；同一账号最多使用2篇作品的限制已检查，本批实际每账号只用1篇参与pattern。一个作品可支持不同机制，但不会因此变成两个独立作品。

已知高重复作者的train input 7、17、18、52只保留原话，`pattern_support_eligible: false`，未列入任何新pattern的引用。未知账号身份仍不等于已认证真人；没有把教程清单、作者转述的投诉或参数说法当成本人已验证亲历。

调用时先确认这是一位作品作者主动发帖的语境，再读 `expression_purpose`、`need`、`mechanism`、`transferable` 与 `not_transferable`。卡片不是评论父句，不能据此生成假装已经发生的楼中楼关系。真实原话和经历保留归属，不分配给另一个真实说话者。相反色彩偏好同时保留，不提炼成Pocket4/4P用户的共同审美。

场景2、3、4、9增加了独立的 `new_public_post_support` 层。原有历史需求或编辑假设标签保持，新增作者个案不会被悄然合并成群体结论；产品功能支持仍来自官方事实。

复建原话可运行 `python3 knowledge/pocket/voice/build_public_post_records.py`；脚本先过滤train，保留其他记录，仅按ID更新本次选入帖子，不采集新链接。筛选明细见 [public-post-ingest-report.json](public-post-ingest-report.json)。表达卡是有来源的编辑归纳，不由脚本自动凑数生成。

8张新卡已由产品资料代理独立核对17个支持作品、原文归纳和作者去重，未发现阻断问题；两项收紧意见均已采用。最终有24处带字符定位的摘句。详见 [public-post-independent-review.json](public-post-independent-review.json)。本结论不覆盖旧legacy卡，不认证作者经历或产品说法，也不能表述成真实消费者身份已被验证。
