# Portable 安装说明

## Generic 模式

只读取 `core/write-consumer-comments/SKILL.md`，输入原帖材料和产品资料即可写作。宿主没有社媒读取能力时，使用用户提供的正文、转写、可见画面和评论材料，不把搜索摘要、抽帧或推测写成完整事实。

## DJI Product Pack 模式

在 Generic 模式上，按产品读取一个 `products/dji/*/SKILL.md`。适配入口只提供命名、事实边界和资料接口，不替代当前官方资料核验。

## op 适配模式

只有目标环境具备 op 项目文件、产品知识库和对应工具时，才读取 `adapters/op/`。它不是跨平台核心依赖。

## 输入契约

```yaml
post_material: 原帖正文、转写、可见画面及证据范围
product_facts: 型号、能力、适用条件、来源和核验日期
optional_persona: 可选的培训人物设定
evidence_scope: 已读内容、缺失内容和合成命题说明
```

## 输出契约

正文只交付编号主评论和缩进回复，教学说明另列。统一标注 `training_fiction`；没有原帖证据的练习标为 synthetic，不冒充真实采集或真实消费者反馈。

检查器是格式、父句、来源登记的辅助工具，不能替代整帖理解和自然程度审稿。没有 Python 时仍可只使用 Markdown 主提示。
