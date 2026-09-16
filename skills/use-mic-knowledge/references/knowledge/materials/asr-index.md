# Mic 完整音轨的机器转写索引

处理日期：2026-09-08。累计 **7次完整音轨处理／4份待听音核对的中文定位线索／3份ASR异常／听音复核0**。均为 `machine_transcript_unverified`；完成执行不等于准确识别，完整输入也不等于逐字覆盖。

| 作品 | 已解码音轨 | 结果 | 回查提示 |
|---|---:|---|---|
| [P001](/Users/luocaihua/Documents/ChatGPT/op/outputs/mic-experience-20260908/asr-remaining/P001.md) | 16.068秒 | 8段，模型语言en；异常，不计有效中文转写 | 输出零散英文，不作实际语言或人声判断。设置页另见过程便笺。 |
| [P003](/Users/luocaihua/Documents/ChatGPT/op/outputs/mic-experience-20260908/asr/P003.md) | 57.051秒 | 23段，模型语言zh；中文待核时间轴 | 29–42秒：定位有麦／不用麦段落，音源切换及声音差异待核。 |
| [P004](/Users/luocaihua/Documents/ChatGPT/op/outputs/mic-experience-20260908/asr/P004.md) | 114.289秒 | 67段，模型语言zh；中文待核时间轴 | 17–23秒阶段自述；30–41秒夹位；44–63秒设置，专名和档位不能据机转修正。 |
| [P006](/Users/luocaihua/Documents/ChatGPT/op/outputs/mic-experience-20260908/asr/P006.md) | 66.270秒 | 1段，模型语言si；异常，不计有效中文转写 | 输出si单段；不能据此判断实际语言、有无人声或偏好。 |
| [P009](/Users/luocaihua/Documents/ChatGPT/op/outputs/mic-experience-20260908/asr-p009/P009.md) | 611.707秒 | 159段，模型语言zh；中文待核时间轴 | 130–164秒连接说明；344–419秒尝试连接与对照；498–544秒部件探索；565–600秒计划。只有逐帧另核的字幕可引用。 |
| [P010](/Users/luocaihua/Documents/ChatGPT/op/outputs/mic-experience-20260908/asr-remaining/P010.md) | 42.167秒 | 22段，模型语言zh；中文待核时间轴 | 0–4秒使用自述，5–11秒连接/遥控介绍；只是回查线索，所有型号、数字和宣传仍待核。 |
| [P011](/Users/luocaihua/Documents/ChatGPT/op/outputs/mic-experience-20260908/asr-remaining/P011.md) | 82.152秒 | 5段，模型语言nn；异常，不计有效中文转写 | 输出nn、重复符号与尺寸文字；不作有效中文内容或声音判断。 |

机器专名、术语、数字和宣传性说法没有静默修改为准确引语。音轨均来自平台下载视频，不是已确认的发射器原始内录。语言标签和空缺不证明原音语言、音乐或有无人声；没有拿机器转写判断音质。

本机隔离环境使用 `faster-whisper 1.2.1`、`small`、CPU/int8，无标题提示、无媒体上传。后4次直接复用缓存并设置离线；三批的来源哈希、版本、完整解码时长和逐段检查分别见：

- [首次3件运行说明](/Users/luocaihua/Documents/ChatGPT/op/outputs/mic-experience-20260908/asr/README.md)、[检查](/Users/luocaihua/Documents/ChatGPT/op/outputs/mic-experience-20260908/asr/validation.json)。
- [P009运行与字幕核对](/Users/luocaihua/Documents/ChatGPT/op/outputs/mic-experience-20260908/asr-p009/README.md)、[检查](/Users/luocaihua/Documents/ChatGPT/op/outputs/mic-experience-20260908/asr-p009/validation.json)。
- [其余3件运行说明](/Users/luocaihua/Documents/ChatGPT/op/outputs/mic-experience-20260908/asr-remaining/README.md)、[检查](/Users/luocaihua/Documents/ChatGPT/op/outputs/mic-experience-20260908/asr-remaining/validation.json)。

[候选记录](inventory.jsonl)中的7个 `machine_asr` 对象独立于 `audio_listened` 与 `audio_transcribed`，后两项仍为false。[录制过程](recording-process.md)引用的是另行目视确认的画面／烧录字幕；不能把它们称为已听音原话。

运行原始输出和大媒体保留在上述项目路径，个人包携带索引；迁移后须另外取得文件，不能假定外部路径仍可用。
