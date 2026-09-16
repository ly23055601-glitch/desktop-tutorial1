# 从 Mic 卖点反查详细场景

场景、用途与选材方向为编辑推演；心理为待验证假设。并非已采集原帖、实际用户经历或已验收设备组合。

从一个感兴趣的卖点找不同任务。这里的关联来自场景候选路线，不能证明原帖展示了该功能或使用者有这种心理。
阅读单卡可看适用条件；命令检索会展开准确型号的事实、限制、来源及原核验日期。更深入的用途解读见[需求与价值发散](../selling_points/value-expansion.md)。

```bash
python3 references/knowledge/scripts/mic_writing_scenarios.py --selling-point MIC3-SP003 --limit 20
python3 references/knowledge/scripts/mic_writing_scenarios.py '回听' --selling-point M2S-SP002 --model mic_mini_2s --format json
```

个人入口对应 `mic.py scenes --selling-point 编号`。卖点、问题、型号与类别同时给出时取交集；交集为空就返回空结果，不借另一型号的场景。未列场景仅表示编辑关联缺口，不表示功能不支持。

## DJI Mic

### MIC-SP001 · 24-bit 单机内录，录音文件可单独导出

- [MIC-WS004 · 已有视频补旁白：按画面空隙录短段说明](creator_learning.md#mic-ws004)
- [MIC-WS005 · 语言与面试练习：回听一轮完整回答](creator_learning.md#mic-ws005)
- [MIC-WS042 · 只用声音教一次拼搭：回听指代和顺序是否够明确](creator_learning.md#mic-ws042)
- [MIC-WS015 · 异地播客：各自存本地讲话，再交给同一位剪辑者](people_memories.md#mic-ws015)
- [MIC-WS016 · 家人口述史：顺着旧物讲，给回听留出检索位置](people_memories.md#mic-ws016)
- [MIC-WS017 · 生日或毕业声音留言：多人依次录，逐段收齐素材](people_memories.md#mic-ws017)
- [MIC-WS021 · 社团共同节目：按栏目分段录，交接麦克风和片段表](people_memories.md#mic-ws021)
- [MIC-WS023 · 方言词语对照：同一句分别说，保留自己的发音样本](people_memories.md#mic-ws023)
- [MIC-WS024 · 个人音频日记：先留下当下的想法，日后私下回听](people_memories.md#mic-ws024)
- [MIC-WS046 · 给一个熟悉的人录有声回信：语气比完整成篇更重要](people_memories.md#mic-ws046)
- [MIC-WS052 · 隔一段时间再聊同一个小问题：回听关注点怎么变](people_memories.md#mic-ws052)
- [MIC-WS034 · 现场讲解结束后单独交出录音素材](business_team.md#mic-ws034)

### MIC-SP002 · 双发射器分左右声道，便于分别处理对谈素材

- [MIC-WS008 · 双人微电影排练：回看两位角色怎样接住台词](creator_learning.md#mic-ws008)
- [MIC-WS021 · 社团共同节目：按栏目分段录，交接麦克风和片段表](people_memories.md#mic-ws021)
- [MIC-WS023 · 方言词语对照：同一句分别说，保留自己的发音样本](people_memories.md#mic-ws023)
- [MIC-WS036 · 操作培训里示范者和讲解者各守一项任务](business_team.md#mic-ws036)
- [MIC-WS058 · 镜头外留一句提示：主讲和提示者的声音用途不同](business_team.md#mic-ws058)

### MIC-SP003 · 低 6dB 安全音轨，给后期留一条较低电平输出

- [MIC-WS044 · 解谜实况突然揭晓：从平静推理转为即兴反应](creator_learning.md#mic-ws044)

## DJI Mic 2

### MIC2-SP001 · 可选 32-bit 浮点内录，按后期流程保留 WAV 素材

- [MIC-WS012 · 有声文本试读：保留轻声、重音和停顿的表演选择](creator_learning.md#mic-ws012)
- [MIC-WS013 · 面对面采访：把确认动作放在谈话自然停顿处](people_memories.md#mic-ws013)
- [MIC-WS018 · 旅行同行聊天：为两人的随口接话留一段声音](people_memories.md#mic-ws018)
- [MIC-WS019 · 婚礼关键发言：先约定要交付哪几段完整声音](people_memories.md#mic-ws019)
- [MIC-WS023 · 方言词语对照：同一句分别说，保留自己的发音样本](people_memories.md#mic-ws023)
- [MIC-WS034 · 现场讲解结束后单独交出录音素材](business_team.md#mic-ws034)

### MIC2-SP002 · 双人分声道与接收端监听，便于现场检查和后期整理

- [MIC-WS008 · 双人微电影排练：回看两位角色怎样接住台词](creator_learning.md#mic-ws008)
- [MIC-WS013 · 面对面采访：把确认动作放在谈话自然停顿处](people_memories.md#mic-ws013)
- [MIC-WS018 · 旅行同行聊天：为两人的随口接话留一段声音](people_memories.md#mic-ws018)
- [MIC-WS019 · 婚礼关键发言：先约定要交付哪几段完整声音](people_memories.md#mic-ws019)
- [MIC-WS023 · 方言词语对照：同一句分别说，保留自己的发音样本](people_memories.md#mic-ws023)
- [MIC-WS045 · 两个人一起拼东西：保留各自看到的不同细节](people_memories.md#mic-ws045)
- [MIC-WS026 · 展会短访在受访者轮换时重新确认](business_team.md#mic-ws026)
- [MIC-WS036 · 操作培训里示范者和讲解者各守一项任务](business_team.md#mic-ws036)
- [MIC-WS056 · 体验者边试边说：把第一次理解和观察者追问分别留下](business_team.md#mic-ws056)
- [MIC-WS058 · 镜头外留一句提示：主讲和提示者的声音用途不同](business_team.md#mic-ws058)

### MIC2-SP003 · 手机可选蓝牙直连，按功能需求决定是否使用接收器

- [MIC-WS003 · 线上教学离桌：在白板与实物之间继续解释](creator_learning.md#mic-ws003)
- [MIC-WS005 · 语言与面试练习：回听一轮完整回答](creator_learning.md#mic-ws005)
- [MIC-WS040 · 第一次接手机：学会分清已配对、能监听和文件里有声音](creator_learning.md#mic-ws040)

## DJI Mic 3

### MIC3-SP001 · 轻量发射器与可旋转背夹，按衣物和动作选择佩戴方式

- [MIC-WS002 · 桌面手作与维修：双手操作时解释关键动作](creator_learning.md#mic-ws002)
- [MIC-WS007 · 穿搭与妆造录制：把麦克风当作画面中的一件小物](creator_learning.md#mic-ws007)
- [MIC-WS038 · 固定全身机位：从坐着讲到站起转身](creator_learning.md#mic-ws038)
- [MIC-WS039 · 换上外套以后：单独听拉链、衣领和背带会不会碰麦](creator_learning.md#mic-ws039)
- [MIC-WS022 · 一起做饭时记录临场叮嘱：以后照做时再回听](people_memories.md#mic-ws022)
- [MIC-WS049 · 第一次给同伴戴麦：由佩戴的人试位置和说一小段](people_memories.md#mic-ws049)
- [MIC-WS025 · 带看时推门、指位置并继续讲解](business_team.md#mic-ws025)
- [MIC-WS060 · 隔天补拍一句：先重建麦位和录制条件再听能否接上](business_team.md#mic-ws060)

### MIC3-SP002 · 两种自动增益控制，分别应对突发音量与讲话响度变化

- [MIC-WS012 · 有声文本试读：保留轻声、重音和停顿的表演选择](creator_learning.md#mic-ws012)
- [MIC-WS044 · 解谜实况突然揭晓：从平静推理转为即兴反应](creator_learning.md#mic-ws044)

### MIC3-SP003 · 32-bit 浮点双文件内录，为后期保留原音与处理版的选择

- [MIC-WS001 · 独自口播：把开录检查放在第一遍表达之前](creator_learning.md#mic-ws001)
- [MIC-WS009 · 实验步骤记述：边观察边说明当时的判断](creator_learning.md#mic-ws009)
- [MIC-WS011 · 分章节录课：利用换题与休息整理文件并补电](creator_learning.md#mic-ws011)
- [MIC-WS012 · 有声文本试读：保留轻声、重音和停顿的表演选择](creator_learning.md#mic-ws012)
- [MIC-WS038 · 固定全身机位：从坐着讲到站起转身](creator_learning.md#mic-ws038)
- [MIC-WS039 · 换上外套以后：单独听拉链、衣领和背带会不会碰麦](creator_learning.md#mic-ws039)
- [MIC-WS041 · 整理作品集时口述选片理由：把还没写成文字的判断留下](creator_learning.md#mic-ws041)
- [MIC-WS043 · 同一遍讲话留两种文件：先确认比较的是同一次表达](creator_learning.md#mic-ws043)
- [MIC-WS044 · 解谜实况突然揭晓：从平静推理转为即兴反应](creator_learning.md#mic-ws044)
- [MIC-WS013 · 面对面采访：把确认动作放在谈话自然停顿处](people_memories.md#mic-ws013)
- [MIC-WS016 · 家人口述史：顺着旧物讲，给回听留出检索位置](people_memories.md#mic-ws016)
- [MIC-WS019 · 婚礼关键发言：先约定要交付哪几段完整声音](people_memories.md#mic-ws019)
- [MIC-WS020 · 生活声音小档案：先试听要留住的声源与氛围](people_memories.md#mic-ws020)
- [MIC-WS022 · 一起做饭时记录临场叮嘱：以后照做时再回听](people_memories.md#mic-ws022)
- [MIC-WS024 · 个人音频日记：先留下当下的想法，日后私下回听](people_memories.md#mic-ws024)
- [MIC-WS046 · 给一个熟悉的人录有声回信：语气比完整成篇更重要](people_memories.md#mic-ws046)
- [MIC-WS047 · 聊天只录约定的一段：开聊和开录不必同时发生](people_memories.md#mic-ws047)
- [MIC-WS049 · 第一次给同伴戴麦：由佩戴的人试位置和说一小段](people_memories.md#mic-ws049)
- [MIC-WS050 · 家庭小演出旁边：先决定想留台上声音还是身边反应](people_memories.md#mic-ws050)
- [MIC-WS051 · 一起回听再挑一段：讲述者也参与决定留下什么](people_memories.md#mic-ws051)
- [MIC-WS032 · 一段现场讲话交给两种后期版本](business_team.md#mic-ws032)
- [MIC-WS059 · 评审声音样片：先对齐文件来源再讨论喜不喜欢](business_team.md#mic-ws059)
- [MIC-WS060 · 隔天补拍一句：先重建麦位和录制条件再听能否接上](business_team.md#mic-ws060)

### MIC3-SP004 · 四发八收与有条件四声道，按人数、机位和后期分轨需要配置

- [MIC-WS013 · 面对面采访：把确认动作放在谈话自然停顿处](people_memories.md#mic-ws013)
- [MIC-WS014 · 四人读书圆桌：先决定混音成品还是逐人处理](people_memories.md#mic-ws014)
- [MIC-WS019 · 婚礼关键发言：先约定要交付哪几段完整声音](people_memories.md#mic-ws019)
- [MIC-WS048 · 两个人听同一段样片：可以喜欢不同的声音处理](people_memories.md#mic-ws048)
- [MIC-WS029 · 双人栏目增加嘉宾前盘点旧 Mini 部件](business_team.md#mic-ws029)
- [MIC-WS031 · 多机位访谈开拍前约定时间码与音轨](business_team.md#mic-ws031)
- [MIC-WS035 · 同场讲话分别送到直播台与录制机位](business_team.md#mic-ws035)
- [MIC-WS053 · 同场两位讲述者的环境不同：降噪不必整组照搬](business_team.md#mic-ws053)
- [MIC-WS057 · 多路排练先轮流说名字：确认正在听的是哪支麦](business_team.md#mic-ws057)

### MIC3-SP005 · 内置时间码，为多机位音视频素材提供同步依据

- [MIC-WS031 · 多机位访谈开拍前约定时间码与音轨](business_team.md#mic-ws031)

### MIC3-SP006 · 三挡音色与两挡降噪，提供录前声音处理选项

- [MIC-WS010 · 固定栏目试录：挑选自己愿意长期使用的人声处理](creator_learning.md#mic-ws010)
- [MIC-WS043 · 同一遍讲话留两种文件：先确认比较的是同一次表达](creator_learning.md#mic-ws043)
- [MIC-WS014 · 四人读书圆桌：先决定混音成品还是逐人处理](people_memories.md#mic-ws014)
- [MIC-WS020 · 生活声音小档案：先试听要留住的声源与氛围](people_memories.md#mic-ws020)
- [MIC-WS048 · 两个人听同一段样片：可以喜欢不同的声音处理](people_memories.md#mic-ws048)
- [MIC-WS025 · 带看时推门、指位置并继续讲解](business_team.md#mic-ws025)
- [MIC-WS032 · 一段现场讲话交给两种后期版本](business_team.md#mic-ws032)
- [MIC-WS053 · 同场两位讲述者的环境不同：降噪不必整组照搬](business_team.md#mic-ws053)
- [MIC-WS060 · 隔天补拍一句：先重建麦位和录制条件再听能否接上](business_team.md#mic-ws060)

### MIC3-SP007 · 48 kHz 24-bit 无损传输，在格式与无线距离之间作选择

- [MIC-WS054 · 先排全景机位再选传输模式：距离和格式一起定](business_team.md#mic-ws054)
- [MIC-WS059 · 评审声音样片：先对齐文件来源再讨论喜不喜欢](business_team.md#mic-ws059)

### MIC3-SP008 · 分部件续航与快充，便于安排多段拍摄补电

- [MIC-WS011 · 分章节录课：利用换题与休息整理文件并补电](creator_learning.md#mic-ws011)
- [MIC-WS033 · 分段拍摄把回盒补电排进转场](business_team.md#mic-ws033)

### MIC3-SP009 · 兼容设备可直连发射器，为轻装拍摄提供连接选择

- [MIC-WS001 · 独自口播：把开录检查放在第一遍表达之前](creator_learning.md#mic-ws001)
- [MIC-WS037 · 镜头朝向收藏物：把画外的第一反应也当作内容](creator_learning.md#mic-ws037)

## DJI Mic Mini

### MM-SP001 · 强弱两级降噪，按连接路径选择可用设置

- [MIC-WS006 · 烹饪同步讲解：说明此刻为什么翻面或收汁](creator_learning.md#mic-ws006)
- [MIC-WS018 · 旅行同行聊天：为两人的随口接话留一段声音](people_memories.md#mic-ws018)
- [MIC-WS026 · 展会短访在受访者轮换时重新确认](business_team.md#mic-ws026)
- [MIC-WS028 · 共用设备从相机任务交到手机任务](business_team.md#mic-ws028)
- [MIC-WS030 · 同一演示先拍相机版本再切手机补充](business_team.md#mic-ws030)

### MM-SP002 · 接收器、手机蓝牙与 OsmoAudio 三类连接路径

- [MIC-WS006 · 烹饪同步讲解：说明此刻为什么翻面或收汁](creator_learning.md#mic-ws006)
- [MIC-WS018 · 旅行同行聊天：为两人的随口接话留一段声音](people_memories.md#mic-ws018)
- [MIC-WS045 · 两个人一起拼东西：保留各自看到的不同细节](people_memories.md#mic-ws045)
- [MIC-WS028 · 共用设备从相机任务交到手机任务](business_team.md#mic-ws028)
- [MIC-WS030 · 同一演示先拍相机版本再切手机补充](business_team.md#mic-ws030)

### MM-SP003 · 双人分声道或低 6dB 安全轨，按后期需求选模式

- [MIC-WS018 · 旅行同行聊天：为两人的随口接话留一段声音](people_memories.md#mic-ws018)
- [MIC-WS045 · 两个人一起拼东西：保留各自看到的不同细节](people_memories.md#mic-ws045)
- [MIC-WS026 · 展会短访在受访者轮换时重新确认](business_team.md#mic-ws026)

## DJI Mic Mini 2

### MM2-SP001 · 磁吸换盖与四向背夹，兼顾入镜搭配和安装位置

- [MIC-WS007 · 穿搭与妆造录制：把麦克风当作画面中的一件小物](creator_learning.md#mic-ws007)
- [MIC-WS022 · 一起做饭时记录临场叮嘱：以后照做时再回听](people_memories.md#mic-ws022)
- [MIC-WS025 · 带看时推门、指位置并继续讲解](business_team.md#mic-ws025)
- [MIC-WS027 · 手机直播时双手展示与旁侧检查分工](business_team.md#mic-ws027)

### MM2-SP002 · 手机版接收器用 O／L／H 开关调节降噪

- [MIC-WS001 · 独自口播：把开录检查放在第一遍表达之前](creator_learning.md#mic-ws001)
- [MIC-WS021 · 社团共同节目：按栏目分段录，交接麦克风和片段表](people_memories.md#mic-ws021)
- [MIC-WS027 · 手机直播时双手展示与旁侧检查分工](business_team.md#mic-ws027)
- [MIC-WS028 · 共用设备从相机任务交到手机任务](business_team.md#mic-ws028)

### MM2-SP003 · 标准与手机版组合可选，按手机或相机接口配接收端

- [MIC-WS001 · 独自口播：把开录检查放在第一遍表达之前](creator_learning.md#mic-ws001)
- [MIC-WS007 · 穿搭与妆造录制：把麦克风当作画面中的一件小物](creator_learning.md#mic-ws007)
- [MIC-WS021 · 社团共同节目：按栏目分段录，交接麦克风和片段表](people_memories.md#mic-ws021)
- [MIC-WS022 · 一起做饭时记录临场叮嘱：以后照做时再回听](people_memories.md#mic-ws022)
- [MIC-WS025 · 带看时推门、指位置并继续讲解](business_team.md#mic-ws025)
- [MIC-WS027 · 手机直播时双手展示与旁侧检查分工](business_team.md#mic-ws027)
- [MIC-WS028 · 共用设备从相机任务交到手机任务](business_team.md#mic-ws028)

## DJI Mic Mini 2S

### M2S-SP001 · 约 12 克发射器与多位置佩戴

- [MIC-WS002 · 桌面手作与维修：双手操作时解释关键动作](creator_learning.md#mic-ws002)
- [MIC-WS003 · 线上教学离桌：在白板与实物之间继续解释](creator_learning.md#mic-ws003)
- [MIC-WS038 · 固定全身机位：从坐着讲到站起转身](creator_learning.md#mic-ws038)
- [MIC-WS039 · 换上外套以后：单独听拉链、衣领和背带会不会碰麦](creator_learning.md#mic-ws039)
- [MIC-WS049 · 第一次给同伴戴麦：由佩戴的人试位置和说一小段](people_memories.md#mic-ws049)
- [MIC-WS027 · 手机直播时双手展示与旁侧检查分工](business_team.md#mic-ws027)
- [MIC-WS060 · 隔天补拍一句：先重建麦位和录制条件再听能否接上](business_team.md#mic-ws060)

### M2S-SP002 · 发射器本地内录，并可选择原文件或处理文件

- [MIC-WS004 · 已有视频补旁白：按画面空隙录短段说明](creator_learning.md#mic-ws004)
- [MIC-WS009 · 实验步骤记述：边观察边说明当时的判断](creator_learning.md#mic-ws009)
- [MIC-WS011 · 分章节录课：利用换题与休息整理文件并补电](creator_learning.md#mic-ws011)
- [MIC-WS042 · 只用声音教一次拼搭：回听指代和顺序是否够明确](creator_learning.md#mic-ws042)
- [MIC-WS015 · 异地播客：各自存本地讲话，再交给同一位剪辑者](people_memories.md#mic-ws015)
- [MIC-WS016 · 家人口述史：顺着旧物讲，给回听留出检索位置](people_memories.md#mic-ws016)
- [MIC-WS017 · 生日或毕业声音留言：多人依次录，逐段收齐素材](people_memories.md#mic-ws017)
- [MIC-WS020 · 生活声音小档案：先试听要留住的声源与氛围](people_memories.md#mic-ws020)
- [MIC-WS047 · 聊天只录约定的一段：开聊和开录不必同时发生](people_memories.md#mic-ws047)
- [MIC-WS050 · 家庭小演出旁边：先决定想留台上声音还是身边反应](people_memories.md#mic-ws050)
- [MIC-WS051 · 一起回听再挑一段：讲述者也参与决定留下什么](people_memories.md#mic-ws051)
- [MIC-WS052 · 隔一段时间再聊同一个小问题：回听关注点怎么变](people_memories.md#mic-ws052)
- [MIC-WS032 · 一段现场讲话交给两种后期版本](business_team.md#mic-ws032)
- [MIC-WS056 · 体验者边试边说：把第一次理解和观察者追问分别留下](business_team.md#mic-ws056)
- [MIC-WS059 · 评审声音样片：先对齐文件来源再讨论喜不喜欢](business_team.md#mic-ws059)

### M2S-SP003 · 最多四发同时连接，适配链路可分别输出四路

- [MIC-WS014 · 四人读书圆桌：先决定混音成品还是逐人处理](people_memories.md#mic-ws014)
- [MIC-WS029 · 双人栏目增加嘉宾前盘点旧 Mini 部件](business_team.md#mic-ws029)

### M2S-SP004 · 两级 AI 降噪、三种音色与自动增益选项

- [MIC-WS006 · 烹饪同步讲解：说明此刻为什么翻面或收汁](creator_learning.md#mic-ws006)
- [MIC-WS010 · 固定栏目试录：挑选自己愿意长期使用的人声处理](creator_learning.md#mic-ws010)
- [MIC-WS014 · 四人读书圆桌：先决定混音成品还是逐人处理](people_memories.md#mic-ws014)
- [MIC-WS020 · 生活声音小档案：先试听要留住的声源与氛围](people_memories.md#mic-ws020)
- [MIC-WS032 · 一段现场讲话交给两种后期版本](business_team.md#mic-ws032)
- [MIC-WS060 · 隔天补拍一句：先重建麦位和录制条件再听能否接上](business_team.md#mic-ws060)

### M2S-SP005 · 标准接收器覆盖手机、相机与电脑连接

- [MIC-WS002 · 桌面手作与维修：双手操作时解释关键动作](creator_learning.md#mic-ws002)
- [MIC-WS003 · 线上教学离桌：在白板与实物之间继续解释](creator_learning.md#mic-ws003)
- [MIC-WS006 · 烹饪同步讲解：说明此刻为什么翻面或收汁](creator_learning.md#mic-ws006)
- [MIC-WS038 · 固定全身机位：从坐着讲到站起转身](creator_learning.md#mic-ws038)
- [MIC-WS039 · 换上外套以后：单独听拉链、衣领和背带会不会碰麦](creator_learning.md#mic-ws039)
- [MIC-WS041 · 整理作品集时口述选片理由：把还没写成文字的判断留下](creator_learning.md#mic-ws041)
- [MIC-WS049 · 第一次给同伴戴麦：由佩戴的人试位置和说一小段](people_memories.md#mic-ws049)
- [MIC-WS030 · 同一演示先拍相机版本再切手机补充](business_team.md#mic-ws030)
- [MIC-WS055 · 远程演示一边听一边说：把输入麦与对方声音分开安排](business_team.md#mic-ws055)
- [MIC-WS060 · 隔天补拍一句：先重建麦位和录制条件再听能否接上](business_team.md#mic-ws060)

### M2S-SP006 · 兼容 OsmoAudio 设备可直接连接发射器

- [MIC-WS037 · 镜头朝向收藏物：把画外的第一反应也当作内容](creator_learning.md#mic-ws037)

### M2S-SP007 · 手机版接收器提供实体降噪开关与条件性监听

- [MIC-WS040 · 第一次接手机：学会分清已配对、能监听和文件里有声音](creator_learning.md#mic-ws040)
- [MIC-WS027 · 手机直播时双手展示与旁侧检查分工](business_team.md#mic-ws027)

### M2S-SP008 · 标准充电盒支持多次补电，按测试条件规划拍摄

- [MIC-WS011 · 分章节录课：利用换题与休息整理文件并补电](creator_learning.md#mic-ws011)
- [MIC-WS033 · 分段拍摄把回盒补电排进转场](business_team.md#mic-ws033)

### M2S-SP009 · 已持有 Mini 系列部件可核对指定复用路径

- [MIC-WS029 · 双人栏目增加嘉宾前盘点旧 Mini 部件](business_team.md#mic-ws029)

