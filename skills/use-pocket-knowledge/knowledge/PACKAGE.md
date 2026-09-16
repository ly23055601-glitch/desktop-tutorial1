# 封装与维护

这是显式生成的个人资料快照，不是指向op项目的软链接。产品与表达查询仅依赖本包和Python 3.9+标准库；原始xlsx用于追溯，正常检索不依赖openpyxl。写评论另依赖同机的write-consumer-comments及write-dji-pocket-comments，真实链接读取另依赖统一社媒技能。

## 来源保真

产品、语料、原始导出、normalized文件、学习/留出分组及核验日期按原字节保存。JSON中的绝对路径是采集时记录，不能从当前工作目录直接打开；用检索结果的resolved_source_path或resolve-source命令定位包内相同来源。package-map.json提供旧路径别名，缺项时不退回原项目。个别Markdown只调整导航链接，manifest.json分别记录源文件与封装后哈希。

_provenance中是旧记录引用的归档材料，不是当前写作指令。历史model_source_sha256和反馈索引中的旧SKILL哈希对应当时索引，不代表现在源文件同版；不改写成当前哈希冒称复现。原始/normalized正文来源与封装快照哈希分别核验。封装时间不刷新产品核验日、不增加样本、不放行pending。

## 明确刷新

维护源：`/Users/luocaihua/Documents/ChatGPT/op/knowledge/pocket/`。修改维护源并验收后，在该项目执行：

```bash
python3 knowledge/pocket/packaging/build_package.py
```

该命令只刷新个人技能的knowledge目录和manifest，不采集、不调用模型，不修改原语料或其他个人技能。已有快照移到非扫描的backups目录，避免重复发现同名技能。MODULE.md、agents元数据和共享写法由各自维护入口更新。没有自动同步或后台续采。

原资料中的构建命令、采集队列和大规模验收设计仅是历史工程说明；当前查询按本包INDEX使用。迁移设备时复制完整use-pocket-knowledge文件夹；若要生成正式评论，还需安装上述共享写作依赖，不能从归档旧规则拼出替代流程。
