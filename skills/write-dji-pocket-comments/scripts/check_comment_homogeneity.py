#!/usr/bin/env python3
"""Audit DJI Pocket comments for structure, repetition, and LH5–LH12 evidence."""

from __future__ import annotations

import argparse
import difflib
import html
import json
import math
import re
import statistics
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit


SECTION_RE = re.compile(r"^##\s+(?:(?:小红书|抖音|B站|哔哩哔哩|微博)\s*)?(?:链接\s*)?(\d+)(?:\s*[｜|]\s*(\S+))?\s*$", re.IGNORECASE)
CONTENT_ID_RE = re.compile(r"/(?:video|item|explore|detail|status)/([^/?#]+)", re.IGNORECASE)
MAIN_RE = re.compile(r"^\s*主评论(?:\s*[（(](?P<label>[^)）]*)[)）])?\s*[：:]\s*(?P<body>.+?)\s*$")
REPLY_RE = re.compile(r"^\s*↳\s*回复\s*(?P<number>\d+)?(?:\s*[（(](?P<label>[^)）]*)[)）])?\s*[：:]\s*(?P<body>.+?)\s*$")
NUMBERED_MAIN_RE = re.compile(r"^(?P<number>\d+)\.[ \t]+(?P<body>\S.*?)\s*$")
INDENTED_REPLY_RE = re.compile(r"^(?P<indent>[ \t]+)-[ \t]+(?P<body>\S.*?)\s*$")

MODEL_TOKEN = r"(?:[1-9]\d*\s*(?:Pro|P)?|4P)"
FULL_PRODUCT_RE = re.compile(
    rf"(?:(?:大疆|DJI)\s*(?:Osmo\s*)?|Osmo\s*)Pocket\s*{MODEL_TOKEN}(?![A-Za-z0-9])",
    re.IGNORECASE,
)
ANY_PRODUCT_RE = re.compile(
    rf"(?:(?:大疆|DJI)\s*(?:Osmo\s*)?|Osmo\s*)Pocket(?:\s*{MODEL_TOKEN})?|"
    rf"Pocket(?:\s*{MODEL_TOKEN})?|(?<![A-Za-z0-9])4P(?![A-Za-z0-9])",
    re.IGNORECASE,
)
PRODUCT_CUE_RE = re.compile(
    r"Pocket|4P|大疆|云台|跟随|焦段|1\s*[×x]|3\s*[×x]|直出|慢动作|变焦|"
    r"中焦|双镜头|双摄|防抖|收音|续航|防水|D-?Log|帧率",
    re.IGNORECASE,
)
NON_DJI_POCKET_PREFIX_RE = re.compile(
    r"(?:飞宇|Feiyu|影石|Insta360|飞米|FIMI|浩瀚|Hohem|奥川|AOCHUAN)\s*$",
    re.IGNORECASE,
)
LH7_PRODUCT_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:(?:大疆|DJI)\s*)?(?:Osmo\s*)?Pocket"
    r"(?:\s*[1-9]\d*(?:\s*(?:Pro|P))?)?(?![A-Za-z0-9])|"
    r"(?<![A-Za-z0-9])(?:(?:大疆|DJI)\s*)?(?:p\s*[1-4]|4\s*P)(?![A-Za-z0-9])",
    re.IGNORECASE,
)
LH7_OTHER_DEVICE_PREFIX_RE = re.compile(
    r"(?:飞宇|Feiyu|影石|Insta360|飞米|FIMI|浩瀚|Hohem|奥川|AOCHUAN|"
    r"华为|Huawei|荣耀|Honor|小米|Xiaomi|红米|Redmi|苹果|Apple|iPhone|"
    r"OPPO|vivo|三星|Samsung|手机|竞品)(?:的|款)?\s*$",
    re.IGNORECASE,
)
LH7_OTHER_DEVICE_SUFFIX_RE = re.compile(r"\s*(?:手机|电话|平板)")
COPY_URL_RE = re.compile(r"https?://[^\s<>\u4e00-\u9fff，。！？；：、\"“”]+", re.IGNORECASE)
LH7_OTHER_PRODUCT_RE = re.compile(
    r"(?:Insta\s*360(?:\s*(?:GO|X|Ace)(?:\s*\d+)?(?:\s*(?:Pro|Ultra))?)?|"
    r"Go\s*Pro(?:\s*HERO)?(?:\s*\d+)?|HERO\s*\d+|"
    r"iPhone\s*\d+(?:\s*(?:Pro|Max|Plus|Air))*|"
    r"(?:(?:DJI|Osmo)\s*)?(?:Action|Mobile|Mic)\s*(?:\d+|Mini)(?:\s*Pro)?|"
    r"(?:DJI\s*)?Osmo\s*Nano(?:\s*\d+)?|"
    r"ZV\s*-?\s*E\s*\d+)", re.IGNORECASE,
)

BANNED = (
    "本质上",
    "这说明",
    "产品价值",
    "核心优势",
    "适合哪类人",
    "适合谁",
    "真正需要的是",
    "行程闭环",
    "分水岭",
)

FIXED_PATTERNS = {
    "mouth_vs_action": re.compile(r"嘴上.{0,18}(?:手上|行动|身体)"),
    "what_is_this": re.compile(r"这哪是.{0,18}(?:分明|明明|简直是)"),
    "not_but": re.compile(r"不是.{0,22}(?:而是|只是)"),
    "while_while": re.compile(r"一边.{0,18}一边"),
    "expect_twist": re.compile(r"(?:本来|刚想|正准备|以为).{0,24}(?:结果|没想到|却)"),
    "until_then": re.compile(r"直到.{0,20}才"),
    "role_colon": re.compile(r"^[\u4e00-\u9fffA-Za-z]{1,8}[：:]"),
    "stock_slang": re.compile(r"我宣布|谁懂|直接封神|DNA动了", re.IGNORECASE),
}
ARTIFICIAL_JOKE_IDS = {"mouth_vs_action", "what_is_this", "role_colon"}
MOMENT_RE = re.compile(r"(?:这|那)(?:一下|一秒|一张|张|一段|段|一格|格|一帧|帧)|最后")
REACTION_RE = re.compile(r"我(?:的)?第一反应|我下意识|我暂停|我反而|我偏偏|比.{0,12}更抢眼")
SHORT_REPLY_EXEMPT = {"哈哈", "哈哈哈", "同问", "蹲一个", "我也是", "真的", "笑死", "+1", "＋1"}

# Evidence-aware seeding diagnostics use reviewable text proxies; the state is
# still the source of truth for factual grades. LH6 structural red lines are
# hard failures, while style warnings still require human rereading.
BENEFIT_PROXY_RE = re.compile(
    r"不用|不必|省得|免得|省事|省力|省心|少(?:靠近|走|跑|错过|返工|试错|折腾|带|剪|等|占)|"
    r"更(?:容易|方便|轻松|稳|自然|省事|好拍|好剪|好带|清楚|安全)|"
    r"(?:一|单)个人也能|自己也能|腾出手|解放双手|带得动|愿意带|不占手|"
    r"不用挤前排|不用走近|不怕错过|不容易错过|安全距离|不打扰|"
    r"拍得到|拍得清|拍得稳|拍得进|跟得住|框得住|收得进|塞得下|"
    r"一遍成|少废片|好出片|方便剪|好导出|省后期|少后期|随手就能|抬手就能"
)
QUESTION_RE = re.compile(
    r"[?？]|是否|能不能|可不可以|会不会|有没有|是不是|到底|"
    r"想知道|求问|请问|怎么|哪个|哪台|哪颗|多少|几倍|直出还是|后期还是|"
    r"(?:吗|么|嘛)(?:[，。！？?!\s]|$)"
)
UNRESOLVED_RE = re.compile(
    r"没写|没说|没标|没提|没看到|看不出|不清楚|不知道|不确定|"
    r"未说明|未标注|先别|别先|别猜|不好猜|不一定|未必|等作者|蹲作者|想看作者回|蹲一个"
)
DIRECT_ANSWER_RE = re.compile(
    r"(?:官方|正文|作者|原帖|参数|页面|标题).{0,12}(?:写|说|标|叫|显示|支持|提到)|"
    r"用的是|用的就是|官方叫|明确是|确定是|"
    r"(?:Pocket|4P|这台|这个模式|该机).{0,12}(?:是|有|支持|可以|能|需要|只能|不能|没有)|"
    r"(?:支持|可以|需要|只能|不能|没有|并不是|取决于).{1,18}",
    re.IGNORECASE,
)
CAVEAT_RE = re.compile(
    r"不过|但是|但(?=[^a-zA-Z]|$)|只是|也可能|不一定|未必|并非|不全是|不等于|"
    r"没写|没说|没标|没提|没看到|看不出|不清楚|不知道|不确定|"
    r"先别|别先|别把|别默认|别只凭|不能只|不能默认|要看|取决于|限制|裸机不防水"
)
HARD_PUSH_RE = re.compile(
    r"闭眼入|必买|必入|无脑冲|无脑入|吊打|必须买|"
    r"赶紧(?:买|冲)|直接(?:买|冲|下单)|立刻下单|马上下单|冲就完了|"
    r"买它|不买(?:就|会)?后悔|早买早享受|全款拿下"
)
SOFT_PURCHASE_RE = re.compile(
    r"有点想要|开始想要|想买|想入|想换|想升级|心动|种草|"
    r"会偏(?:4P|Pocket|大疆)|更想选|更想买|升级理由|值得关注|"
    r"考虑(?:买|入|换)|放进购物车|加入购物车|下单|入手"
)
FEATURE_PATTERNS = {
    "stabilization": re.compile(r"三轴|云台|防抖|增稳"),
    "tracking": re.compile(r"跟随|追踪|跟拍|人物跟踪|人脸跟踪"),
    "focal_length": re.compile(r"焦段|中焦|长焦|广角|变焦|1\s*[×x]|3\s*[×x]|双镜头|双摄|20\s*mm|60\s*mm", re.IGNORECASE),
    "slow_motion": re.compile(r"慢动作|升格|帧率|\d{2,3}\s*fps", re.IGNORECASE),
    "image_quality": re.compile(r"画质|动态范围|高光|暗部|低光|夜景|HDR|4K|10\s*bit|D-?Log|色彩", re.IGNORECASE),
    "audio": re.compile(r"收音|麦克风|音质|音轨"),
    "battery": re.compile(r"续航|电池|充电"),
    "waterproofing": re.compile(r"防水|潜水|防水壳"),
    "portability": re.compile(r"便携|口袋|体积|重量|长时间手持|轻装"),
    "workflow": re.compile(r"直出|导出|剪辑|后期|快传|调色|素材"),
    "exposure": re.compile(r"快门|ISO|曝光|光圈", re.IGNORECASE),
    "focus": re.compile(r"对焦|自动对焦|合焦"),
}

MODEL_PATTERNS = (
    ("pocket_4p", re.compile(r"(?:Osmo\s*)?Pocket\s*4P|(?<![A-Za-z0-9])4P(?![A-Za-z0-9])", re.IGNORECASE)),
    ("pocket_4", re.compile(r"(?:Osmo\s*)?Pocket\s*4(?!\s*P)", re.IGNORECASE)),
    ("pocket_3", re.compile(r"(?:Osmo\s*)?Pocket\s*3(?![A-Za-z0-9])", re.IGNORECASE)),
)
CONDITIONAL_RE = re.compile(r"如果|要是|假如|经常|常拍|主要拍|这类|这种场景|的话|会(?:先)?看|会选|会偏|才(?:会|更)|更适合|先看")
BOUNDARY_LANGUAGE_RE = re.compile(r"不过|但是|但(?=[^A-Za-z]|$)|不是|并非|不支持|不能|只有|仅限|前提|取决于|用不到|没必要")
OPTICAL_2X_RE = re.compile(r"(?:2|二)\s*(?:倍|[x×])\s*(?:纯)?光学|光学\s*(?:2|二)\s*(?:倍|[x×])", re.IGNORECASE)
WATERMARK_RE = re.compile(r"水印")
WORKFLOW_VISUAL_RE = re.compile(r"转场|调色|构图|固定机位|留空景|后期同框|混拍|剪(?:辑|起来|片|素材)?|卡点|运镜")
POCKET4_FALSE_60MM_RE = re.compile(
    r"(?:Pocket\s*4(?!\s*P)\s*(?:也)?(?:有|支持|带有|配有|的)\s*(?:60\s*mm|实体中焦)|"
    r"(?:60\s*mm|实体中焦)\s*(?:是|属于|来自|给)\s*Pocket\s*4(?!\s*P)|"
    r"Pocket\s*4(?!\s*P).{0,12}(?:和|与|、).{0,4}4P.{0,8}(?:都|均)(?:有|支持).{0,6}(?:60\s*mm|实体中焦))",
    re.IGNORECASE,
)
EVIDENCE_SOURCE_RE = re.compile(
    r"^(operation|setting|control|ui|author_demo|result|output|frame|same_condition|comparison):"
    r"([^:\s|]+):(.+)$",
    re.IGNORECASE,
)
SHOT_MAPPING_EVIDENCE_RE = re.compile(
    r"^shot:([^:\s|]+):(pocket_4p|pocket_4|pocket_3):(.+)$",
    re.IGNORECASE,
)
FACT_NEGATION_RE = re.compile(r"不是|并非|不能|不支持|没有|并没有|别写成|不要写成|不能说")
CURRENT_MODEL_ASSERTION_RE = re.compile(
    r"(?:(?:这(?:段|条|格|个画面)?|原片|画面).{0,12}(?:就是|是|用的是|来自).{0,12}"
    r"(?:(?:Osmo\s*)?Pocket\s*(?:4P|4|3)|4P).{0,12}(?:拍|直出)|"
    r"(?:(?:拍摄)?(?:设备|机型|机器|相机)).{0,6}(?:就是|是|为|用的是|型号是).{0,8}"
    r"(?:(?:Osmo\s*)?Pocket\s*(?:4P|4|3)|4P)|"
    r"(?:(?:Osmo\s*)?Pocket\s*(?:4P|4|3)|4P).{0,8}(?:拍的|拍出来|拍成|直出))",
    re.IGNORECASE,
)
LH7_CURRENT_MODEL_ASSERTION_RE = re.compile(
    CURRENT_MODEL_ASSERTION_RE.pattern.replace("(?:4P|4|3)", "(?:4P|4|3|2|1)"),
    re.IGNORECASE,
)
LH7_SHOT_MAPPING_EVIDENCE_RE = re.compile(
    SHOT_MAPPING_EVIDENCE_RE.pattern.replace("pocket_4|pocket_3", "pocket_4|pocket_3|pocket_2|pocket_1"),
    re.IGNORECASE,
)
AUTHOR_ATTRIBUTION_RE = re.compile(r"(?:作者|博主|正文|标题|口播).{0,10}(?:说|写|标|提到|自称)")
CURRENT_RESULT_CAUSAL_RE = re.compile(
    r"(?:(?:这(?:段|条|格|个画面)?|当前画面|眼前这格|原片).{0,24}"
    r"(?:靠|因为|归功于|由|就是).{0,16}(?:拍成|带来|变近|变稳|清楚|原因)|"
    r"(?:就是|正是|靠|归功于).{0,28}(?:这(?:段|条|格|个画面)?|当前画面|眼前这格|原片).{0,16}"
    r"(?:拍成|带来|变近|变稳|清楚|原因)|"
    r"(?:(?:Pocket|4P|中焦|长焦|跟随|云台|D-?Log).{0,18}(?:让|把|使).{0,12}"
    r"(?:这(?:段|条|格|个画面)?|当前画面|原片|人脸|主体).{0,12}(?:变近|变稳|清楚)))",
    re.IGNORECASE,
)
CONTRAST_BOUNDARY_TERM_RE = re.compile(
    r"没有|不支持|不是|并非|不同|更(?:重|轻|适合|需要)|用不到|不需要|没必要|无需|只有|仅有|少了|多了"
)
SHARED_CLAIM_MODEL_EDGE_RE = re.compile(
    r"(?:比.{0,12}更(?:稳|好|强|清楚|值得)|更(?:稳|好|强|清楚|值得).{0,12}(?:比|相比)|优于|胜过|不如|吊打)"
)

LH5_RULE_VERSION = "2026-09-02-LH5"
LH6_RULE_VERSION = "2026-09-03-LH6"
LH7_RULE_VERSION = "2026-09-05-LH7"
LH8_RULE_VERSION = "2026-09-05-LH8"
LH9_RULE_VERSION = "2026-09-05-LH9"
LH10_RULE_VERSION = "2026-09-05-LH10"
LH11_RULE_VERSION = "2026-09-05-LH11"
LH12_RULE_VERSION = "2026-09-05-LH12"
LH11_PLUS_RULE_VERSIONS = {LH11_RULE_VERSION, LH12_RULE_VERSION}
LH10_PLUS_RULE_VERSIONS = {LH10_RULE_VERSION, *LH11_PLUS_RULE_VERSIONS}
LH9_PLUS_RULE_VERSIONS = {LH9_RULE_VERSION, *LH10_PLUS_RULE_VERSIONS}
LH8_PLUS_RULE_VERSIONS = {LH8_RULE_VERSION, *LH9_PLUS_RULE_VERSIONS}
SUPPORTED_RULE_VERSIONS = {LH5_RULE_VERSION, LH6_RULE_VERSION, LH7_RULE_VERSION, *LH8_PLUS_RULE_VERSIONS}
LH7_PLUS_RULE_VERSIONS = {LH7_RULE_VERSION, *LH8_PLUS_RULE_VERSIONS}
LH6_PLUS_RULE_VERSIONS = {LH6_RULE_VERSION, *LH7_PLUS_RULE_VERSIONS}
LH10_CURRENT_RESULT_CAUSAL_RE = re.compile(
    CURRENT_RESULT_CAUSAL_RE.pattern + r"|(?:这(?:段|条|格|个画面)?|当前画面|原片)"
    r"[^，,。！？!?；;\n]{0,18}(?:稳|清楚|清晰|干净|流畅|变近)"
    r"[^，,。！？!?；;\n]{0,8}(?:全靠|靠|归功于|因为|多亏)"
    r"[^，,。！？!?；;\n]{1,24}",
    re.IGNORECASE,
)
LH11_DEVICE_REFERENCE_RE = re.compile(
    r"(?:这|那|该)(?:台(?:机器|设备|相机|摄像机|摄影机)?|部(?:相机|摄像机|摄影机))|"
    r"(?:这个|那个|这|那|该)?(?:相机|摄像机|摄影机|拍摄设备)|"
    r"(?:这个|那个|该)(?:机器|设备)"
)
LH11_DEVICE_OWNER_PREDICATE_RE = re.compile(
    r"\s*(?:(?:是|就是)(?:她|他|博主(?:本人)?|作者)(?:的|用的|在用的)|"
    r"(?:属于|归)(?:她|他|博主(?:本人)?|作者))\s*[，,。！？!?；;]?\s*"
)
LH11_EXPLICIT_SPEC_RE = re.compile(
    r"\d+(?:\.\d+)?\s*(?:K|fps|mm|bit)|三轴(?:机械)?云台|双摄|光学变焦|"
    r"(?:续航|能录).{0,8}\d+(?:\.\d+)?\s*(?:分钟|小时)", re.IGNORECASE,
)
LH12_IMPLIED_STABILITY_ASSERTION_RE = re.compile(
    r"\s*(?:那|所以)(?:它|这台(?:机器|设备|相机)?)?(?:肯定|一定|必然)"
    r"(?:就)?(?:很|更|特别)?稳(?:了)?\s*[，,。！？!?；;]?\s*"
)
LH8_OSMO_RE = re.compile(r"Osmo", re.IGNORECASE)
LH8_CURRENT_MODEL_ASSERTION_RE = re.compile(
    r"(?:(?:这(?:段|条|格|个画面)?|原片|画面)[^，,。！？!?；;\n]{0,12}(?:就是|是|用的是|来自)"
    r"[^，,。！？!?；;\n]{0,8}Pocket(?:4P|4|3|2|1)[^，,。！？!?；;\n]{0,6}(?:拍的|拍出来|拍成|拍摄|直出)|"
    r"(?:拍摄设备|设备|机型|机器|相机).{0,6}(?:就是|是|为|用的是|型号是).{0,8}Pocket(?:4P|4|3|2|1)|"
    r"Pocket(?:4P|4|3|2|1)[^，,。！？!?；;\n]{0,6}(?:拍的|拍出来|拍成|直出))",
    re.IGNORECASE,
)
LH8_PERSONAL_HISTORY_RE = re.compile(
    r"我(?:刚刚|刚|已经|之前|去年|上次|前几天)?.{0,8}(?:入手了?|买了|下单了|用了|用过|拍过|带过)|"
    r"(?:刚刚|刚|已经|去年|上次|前几天)(?:才)?(?:入手|买|下单)|"
    r"我家|我(?:爸|妈|对象|老公|老婆|闺蜜)|用了(?:几|[一二三四五六七八九十\d]+)(?:年|个月|天)|"
    r"我(?:也|还)?(?:的|手里(?:的)?|有(?:一台)?)(?:大疆|DJI)?(?:Pocket\d*|p[1-4]|4p)|"
    r"我(?:上次|之前|去年|那次|昨天).{0,10}(?:拍的|录的|用的)", re.IGNORECASE,
)
LH8_HARDWARE_TERM_RE = re.compile(
    r"防抖|三轴|云台|跟随|追踪|变焦|中焦|双镜头|双摄|帧率|收音|续航|防水|"
    r"对焦|光圈|画质|低光|动态范围|HDR|D-?Log|\d+(?:\.\d+)?\s*(?:K|fps|mm|bit|分钟|小时)",
    re.IGNORECASE,
)
LH8_CAPABILITY_ASSERTION_RE = re.compile(
    r"支持|具备|配有|带有|能够|能(?:拍|录|跟|收|让|把|省|\d)|可以(?:拍|录|跟|收)|"
    r"(?:自带|拥有)|(?:防抖|收音|画质|对焦|跟随|低光).{0,6}(?:很|更|特别|真)(?:稳|好|强|清楚|准)|"
    r"有.{0,6}(?:云台|跟随|双摄|中焦|变焦|防抖|追踪)|"
    r"(?:云台|跟随|双摄|中焦|变焦|防抖|追踪|收音|对焦).{0,6}(?:让|可以|能|省|不用|不必)|"
    r"(?:有|是).{0,8}\d+(?:\.\d+)?\s*(?:K|fps|mm|bit)|"
    r"(?:续航|能录).{0,8}\d+(?:\.\d+)?\s*(?:分钟|小时)",
    re.IGNORECASE,
)
LH6_MAIN_MOVES = {
    "observation",
    "reaction",
    "preference",
    "question",
    "disagreement",
    "joke",
    "need",
    "product",
    "benefit",
    "boundary",
}
LH6_SEED_LAYERS = {"need", "question", "product", "benefit", "boundary"}
LH6_GROUP_SCHEMA_CONTRACT = {
    "main_anchor_ids": {
        "type": "array",
        "min_items": 1,
        "max_items": 1,
        "items": "non_empty_string",
    },
    "main_moves": {
        "type": "array",
        "min_items": 1,
        "max_items": 2,
        "unique_items": True,
        "allowed_values": [
            "observation",
            "reaction",
            "preference",
            "question",
            "disagreement",
            "joke",
            "need",
            "product",
            "benefit",
            "boundary",
        ],
    },
    "seed_layers": {
        "type": "object",
        "required_keys": ["main", "replies"],
        "allowed_values": ["need", "question", "product", "benefit", "boundary"],
        "main_max_items": 2,
        "replies_max_items": 5,
        "unique_items_per_scope": True,
    },
    "light_meme_anchor": {
        "type": "string",
        "empty_or_main_anchor": True,
        "required_when_main_moves_contains": "joke",
    },
}
LH6_INTERNAL_AUDIT_RE = re.compile(
    r"本地(?:只有|只(?:有|看到|拿到)|没有)|证据(?:还|也)?接不上|作者口径|"
    r"不替(?:设备|产品|机器|它|这台(?:设备|机器)?).{0,6}(?:认功|背书|下结论)|因果边界"
)
LH6_ENUM_LIST_RE = re.compile(
    r"[^，,。！？!?；;：:\n、]{1,16}、[^，,。！？!?；;：:\n、]{1,16}、[^，,。！？!?；;：:\n、]{1,16}"
)
LH6_ENUM_CONJ_DUNHAO_RE = re.compile(
    r"[^，,。！？!?；;：:\n、]{1,16}、[^，,。！？!?；;：:\n、]{1,16}"
    r"(?:和|与|及|以及|还有|再加上)[^，,。！？!?；;：:\n、]{1,16}"
)
LH6_ENUM_CONJ_COMMA_RE = re.compile(
    r"(?P<first>[^，,。！？!?；;：:\n、]{1,12})[，,]"
    r"(?P<second>[^，,。！？!?；;：:\n、]{1,12})"
    r"(?:和|与|及|以及|还有|再加上)(?P<third>[^，,。！？!?；;：:\n、]{1,16})"
)
LH6_ENUM_COMMA_CONTEXT_RE = re.compile(
    r"^(?:在)?(?:开头|结尾|前面|后面|这里|那里|外面|里面|画面里|镜头里|视频里|正文里|标题里|评论区)"
    r"(?:这段|这一段|那段)?$"
)
LH6_ENUM_COMMA_NEW_CLAUSE_RE = re.compile(
    r"^(?:(?:我|你|他|她|它)(?:们)?(?:$|也|都|会|要|想|和|与|觉得|感觉|一起)|"
    r"觉得|感觉|进去|出来|走进|走出|这时|此时)"
)
LH6_ENUM_COMMA_THIRD_CLAUSE_RE = re.compile(
    r"^(?:我|你|他|她|它)(?:们)?(?:$|也|都|会|要|想|更|和|与|觉得|感觉|一起)"
)
LH6_ENUM_COMMA_CLAUSE_ENDINGS = (
    "停住",
    "入画",
    "出画",
    "转身",
    "回头",
    "推近",
    "拉远",
    "切走",
    "过去",
    "进来",
    "出来",
    "出现",
    "消失",
    "开始",
    "结束",
    "亮",
    "暗",
    "开",
    "关",
    "停",
    "动",
    "晃",
    "笑",
    "哭",
)
LH6_ENUM_COMMA_ACTION_MODIFIER_RE = re.compile(r"^(?:(?:先|再|快速|慢慢|直接|接着|然后)\s*)+")
LH6_THREE_STEP_RE = re.compile(
    r"(?:先|开头|一开始|前一秒).{0,36}(?:再|然后|接着|随后|后面|下一段).{0,36}(?:最后|收尾|末尾)",
    re.DOTALL,
)
LH6_CLOSED_SUMMARY_RE = re.compile(
    r"原路退回|(?:这|那)(?:才|就是).{0,10}(?:重点|关键|答案|感觉|氛围|价值)|"
    r"(?:所以|说明|证明|原来|难怪).{0,18}|(?:一下子|瞬间|直接).{0,12}(?:有了|拉满|成立|明白)|"
    r"(?:负责|替).{0,12}(?:托住|收尾|兜底)|(?:担心|顾虑).{0,12}(?:退回|打消)|"
    r"(?:像|成了).{0,12}(?:电影|故事|答案|证明)|(?:最后|收尾).{0,16}(?:能|会|才|更|不用|少)"
)
LH6_FORMULA_RE = re.compile(
    r"(?:如果|要是)[^。！？!?]{0,24}(?:经常拍|常拍)[^。！？!?]{0,48}"
    r"(?:(?:Osmo\s*)?Pocket(?:\s*(?:4P|4|3))?|(?<![A-Za-z0-9])4P(?![A-Za-z0-9]))"
    r"[^。！？!?]{0,40}(?:能|会|更|少)",
    re.IGNORECASE,
)

S_RANK = {"S0": 0, "S1": 1, "S2": 2, "S3": 3}
M_RANK = {"M0": 0, "M1": 1, "M2": 2}
N_RANK = {"N0": 0, "N1": 1, "N2": 2}
F_RANK = {"F0": 0, "F1": 1, "F2": 2, "F3": 3}
P_RANK = {"P0": 0, "P1": 1, "P2": 2}
VALID_CLAIM_MODES = {"observed", "attributed", "scenario_fit", "causal", "comparative"}
VALID_BENEFIT_BASES = {"product", "workflow", "visual"}
VALID_MODELS = {"pocket_4p", "pocket_4", "pocket_3", "unknown"}
# Older Pocket posts can be discussed from their own evidence without adding
# unsupported models to the versioned official-claim registry.
LH7_CONTEXT_MODELS = VALID_MODELS | {"pocket_1", "pocket_2"}
VALID_MODEL_EVIDENCE_TYPES = {
    "unknown",
    "author_claim",
    "author_statement",
    "body_confirmed",
    "body_ui_confirmed",
    "ui_confirmed",
    "mixed_unmapped",
    "mixed_devices_unmapped",
    "mixed_mapped",
    "watermark_only",
}
WORKFLOW_BENEFIT_ALLOWED_CLAIMS = {
    "4p_dlog2_17stop_1x",
    "4p_physical_60mm",
    "4p_dual_20_60",
    "p4_2x_lossless",
    "p4_internal_107gb",
    "shared_internal_storage",
}
DEFAULT_CLAIM_REGISTRY = Path(__file__).resolve().parents[1] / "references" / "product-claims.json"


@dataclass
class Item:
    file: str
    line: int
    section: str
    url: str
    group: int
    role: str
    text: str
    reply_no: int | None = None
    lh7: bool = False
    speaker: str | None = None
    reply_target: str | None = None


@dataclass
class Group:
    main: Item
    replies: list[Item] = field(default_factory=list)


@dataclass
class Section:
    file: str
    line: int
    number: str
    url: str
    groups: list[Group] = field(default_factory=list)


def clean_raw(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", html.unescape(text))).strip()


def keep_word_chars(text: str) -> str:
    kept: list[str] = []
    for char in text:
        category = unicodedata.category(char)
        if category[0] in {"L", "N"} or "\u4e00" <= char <= "\u9fff":
            kept.append(char)
    return "".join(kept)


def canonical(text: str, *, lh7: bool = False) -> str:
    value = clean_raw(text).lower()
    if lh7:
        for match in reversed(lh7_product_matches(value)):
            value = value[: match.start()] + "产品词" + value[match.end() :]
    else:
        value = ANY_PRODUCT_RE.sub("产品词", value)
    value = re.sub(r"\d+(?:\.\d+)?", "数字", value)
    return keep_word_chars(value)


def scaffold(text: str, *, lh7: bool = False) -> str:
    return canonical(text, lh7=lh7).replace("产品词", "")


def valid_len(text: str) -> int:
    return len(keep_word_chars(clean_raw(text)))


def lh7_product_matches(text: str) -> list[re.Match[str]]:
    """Recognize Pocket names, excluding explicitly named phones/competitors."""
    matches = []
    url_spans = [match.span() for match in COPY_URL_RE.finditer(text)]
    for match in LH7_PRODUCT_RE.finditer(text):
        if any(start <= match.start() < end for start, end in url_spans):
            continue
        prefix = text[max(0, match.start() - 24) : match.start()]
        suffix = text[match.end() : match.end() + 12]
        if LH7_OTHER_DEVICE_PREFIX_RE.search(prefix) or LH7_OTHER_DEVICE_SUFFIX_RE.match(suffix):
            continue
        matches.append(match)
    return matches


def lh7_model_for_label(label: str) -> str:
    value = re.sub(r"\s+", "", clean_raw(label)).lower()
    value = re.sub(r"^(?:大疆|dji)", "", value)
    value = re.sub(r"^(?:osmo)?pocket", "", value)
    return {"1": "pocket_1", "p1": "pocket_1", "2": "pocket_2", "p2": "pocket_2", "3": "pocket_3", "p3": "pocket_3", "4": "pocket_4", "p4": "pocket_4", "4p": "pocket_4p", "": "unknown"}.get(value, "unsupported")


def lh7_fact_text(text: str) -> str:
    """Expand accepted aliases for existing fact regexes without changing copy."""
    accepted = {match.span() for match in lh7_product_matches(text)}
    labels = {"pocket_1": "Pocket1", "pocket_2": "Pocket2", "pocket_3": "Pocket3", "pocket_4": "Pocket4", "pocket_4p": "Pocket4P", "unknown": "Pocket"}
    for match in reversed(list(LH7_PRODUCT_RE.finditer(text))):
        replacement = labels.get(lh7_model_for_label(match.group(0)), match.group(0)) if match.span() in accepted else "其他设备"
        text = text[: match.start()] + replacement + text[match.end() :]
    return text


def find_product_match(text: str, *, lh7: bool = False) -> re.Match[str] | None:
    """Find a Pocket-family mention while ignoring another brand's Pocket name."""
    if lh7:
        return next(iter(lh7_product_matches(text)), None)
    for match in ANY_PRODUCT_RE.finditer(text):
        prefix = text[max(0, match.start() - 16) : match.start()]
        if NON_DJI_POCKET_PREFIX_RE.search(prefix):
            continue
        return match
    return None


def shingles(text: str, size: int) -> set[str]:
    if len(text) < size:
        return set()
    return {text[index : index + size] for index in range(len(text) - size + 1)}


def dice(left: str, right: str, size: int = 3) -> float:
    a, b = shingles(left, size), shingles(right, size)
    if not a or not b:
        return 0.0
    return 2 * len(a & b) / (len(a) + len(b))


def coefficient_of_variation(values: list[int]) -> float:
    mean = statistics.mean(values) if values else 0
    if not mean:
        return 0.0
    return statistics.pstdev(values) / mean


def percentile(values: list[int], q: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def product_class(text: str, *, lh7: bool = False) -> str:
    if FULL_PRODUCT_RE.search(text):
        return "FULL"
    if find_product_match(text, lh7=lh7):
        return "SHORT"
    return "NONE"


def product_position(text: str, *, lh7: bool = False) -> str:
    match = find_product_match(text, lh7=lh7)
    if not match:
        return "none"
    before = valid_len(text[: match.start()])
    total = max(valid_len(text), 1)
    if before <= 1:
        return "start"
    ratio = before / total
    if ratio <= 0.25:
        return "early"
    if ratio <= 0.75:
        return "middle"
    return "late"


def product_in_first_six(text: str, *, lh7: bool = False) -> bool:
    match = find_product_match(text, lh7=lh7)
    return bool(match and valid_len(text[: match.start()]) < 6)


def punctuation_signature(text: str) -> str:
    return "".join(char for char in text if unicodedata.category(char).startswith("P"))


def collect_paths(inputs: list[str]) -> list[Path]:
    found: set[Path] = set()
    for raw in inputs:
        path = Path(raw).expanduser()
        if path.is_dir():
            found.update(item.resolve() for item in path.rglob("*.md") if item.is_file())
        elif path.is_file():
            found.add(path.resolve())
        else:
            raise FileNotFoundError(raw)
    return sorted(found)


def parse_file(path: Path, *, lh12: bool = False) -> tuple[list[Section], list[dict]]:
    diagnostics: list[dict] = []
    sections: list[Section] = []
    current: Section | None = None
    current_group: Group | None = None
    in_fence = False
    seen_sections: set[str] = set()
    reply_indent: str | None = None

    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as exc:
        raise RuntimeError(f"cannot read {path}: {exc}") from exc

    for line_no, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            if lh12 and current is not None:
                diagnostics.append(diag("error", "E_DELIVERY_LINE_INVALID", "最终评论正文不使用代码块，避免可见正文被跳过", path, line_no, current.number))
            in_fence = not in_fence
            continue
        if in_fence or not stripped or (stripped.startswith("# ") and (not lh12 or current is None)):
            continue

        section_match = SECTION_RE.match(line)
        if section_match:
            number, url = section_match.group(1), section_match.group(2) or ""
            if number in seen_sections:
                diagnostics.append(diag("error", "E_DUP_SECTION", f"章节 {number} 重复", path, line_no, number))
            seen_sections.add(number)
            current = Section(str(path), line_no, number, url)
            current_group = None
            reply_indent = None
            sections.append(current)
            continue

        numbered_main = NUMBERED_MAIN_RE.match(line) if lh12 else None
        main_match = MAIN_RE.match(line) or numbered_main
        if main_match:
            if current is None:
                diagnostics.append(diag("error", "E_ORPHAN_MAIN", "主评论位于任何章节之外", path, line_no))
                continue
            group_no = len(current.groups) + 1
            if numbered_main is not None and int(numbered_main.group("number")) != group_no:
                diagnostics.append(diag("error", "E_MAIN_SEQUENCE", f"每帖主评编号应从1连续递增，当前应为{group_no}", path, line_no, current.number, group_no))
            item = Item(str(path), line_no, current.number, current.url, group_no, "main", main_match.group("body"), speaker=None if numbered_main is not None else main_match.group("label"))
            current_group = Group(item)
            current.groups.append(current_group)
            reply_indent = None
            continue

        indented_reply = INDENTED_REPLY_RE.match(line) if lh12 else None
        reply_match = REPLY_RE.match(line) or indented_reply
        if reply_match:
            if current is None or current_group is None:
                diagnostics.append(diag("error", "E_ORPHAN_REPLY", "回复没有对应的主评论", path, line_no, current.number if current else ""))
                continue
            if indented_reply is not None:
                reply_no = len(current_group.replies) + 1
                indent = indented_reply.group("indent").expandtabs(4)
                if reply_indent is not None and indent != reply_indent:
                    diagnostics.append(diag("error", "E_REPLY_INDENT", "回复只使用同一层缩进；实际回复对象保存在 dialogue.reply_to", path, line_no, current.number, current_group.main.group))
                reply_indent = indent if reply_indent is None else reply_indent
                label = None
            else:
                reply_no = int(reply_match.group("number")) if reply_match.group("number") else None
                label = reply_match.group("label")
            label_parts = label.split("→") if label is not None else []
            speaker = label_parts[0].strip() if label_parts else None
            target = label_parts[1].strip() if len(label_parts) == 2 else None
            item = Item(str(path), line_no, current.number, current.url, current_group.main.group, "reply", reply_match.group("body"), reply_no, speaker=speaker, reply_target=target)
            current_group.replies.append(item)
            continue

        if current is not None:
            diagnostics.append(diag("error" if lh12 else "warning", "E_DELIVERY_LINE_INVALID" if lh12 else "W_UNPARSED_LINE", "章节内存在未识别的非空行；LH12使用编号主评及单层缩进回复，或原有主评论/回复格式" if lh12 else "章节内存在未识别的非空行", path, line_no, current.number, text=stripped[:120]))

    return sections, diagnostics


def loc(item: Item) -> dict:
    return {
        "file": item.file,
        "line": item.line,
        "section": item.section,
        "group": item.group,
    }


def diag(
    severity: str,
    code: str,
    message: str,
    file: Path | str | None = None,
    line: int | None = None,
    section: str = "",
    group: int | None = None,
    **extra,
) -> dict:
    locations = []
    if file is not None:
        locations.append({"file": str(file), "line": line or 0, "section": section, "group": group})
    result = {"severity": severity, "code": code, "message": message, "locations": locations}
    result.update(extra)
    return result


def add_pair_diag(diagnostics: list[dict], severity: str, code: str, message: str, left: Item, right: Item, **extra) -> None:
    result = {"severity": severity, "code": code, "message": message, "locations": [loc(left), loc(right)]}
    result.update(extra)
    diagnostics.append(result)


def seed_severity(policy: str, hard: bool = False) -> str:
    return "error" if hard or policy == "strict" else "warning"


def seed_code(policy: str, stem: str, hard: bool = False) -> str:
    return ("E_" if hard or policy == "strict" else "W_") + stem


def add_seed_diag(
    diagnostics: list[dict],
    policy: str,
    stem: str,
    message: str,
    section: Section | None = None,
    group: Group | None = None,
    *,
    hard: bool = False,
    file: Path | str | None = None,
    metrics: dict[str, Any] | None = None,
) -> None:
    target_file = group.main.file if group else section.file if section else file
    target_line = group.main.line if group else section.line if section else 1
    section_number = group.main.section if group else section.number if section else ""
    group_number = group.main.group if group else None
    diagnostics.append(
        diag(
            seed_severity(policy, hard),
            seed_code(policy, stem, hard),
            message,
            target_file,
            target_line,
            section_number,
            group_number,
            metrics=metrics or {},
        )
    )


def load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot read {label} {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} must contain a JSON object: {path}")
    return value


def load_seed_state(
    state_path: Path | None,
    policy: str,
    diagnostics: list[dict],
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    if state_path is None:
        add_seed_diag(
            diagnostics,
            policy,
            "SEED_STATE_MISSING",
            "LH5/LH6/LH7/LH8/LH9/LH10/LH11/LH12 种草检查缺少 --state；未执行逐链接证据映射",
        )
        return {}, {}

    try:
        state = load_json_object(state_path, "state")
    except RuntimeError as exc:
        add_seed_diag(diagnostics, policy, "SEED_STATE_INVALID", str(exc), file=state_path, hard=True)
        return {}, {}

    contexts: dict[str, list[dict[str, Any]]] = defaultdict(list)
    blocks = state.get("block_allocations", [])
    if not isinstance(blocks, list):
        add_seed_diag(diagnostics, policy, "SEED_STATE_INVALID", "state.block_allocations 必须是数组", file=state_path, hard=True)
        return {}, state

    for block in blocks:
        if not isinstance(block, dict):
            continue
        block_draft_path = block.get("draft_path", "")
        allocations = block.get("persuasion_allocations", [])
        if not isinstance(allocations, list):
            continue
        for allocation in allocations:
            if not isinstance(allocation, dict):
                continue
            number = str(allocation.get("section_number", "")).strip()
            if not number:
                continue
            copied = dict(allocation)
            copied["_resolved_draft_path"] = resolve_state_draft_path(
                allocation.get("draft_path") or block_draft_path,
                state_path,
            )
            contexts[number].append(copied)

    return dict(contexts), state


def load_claim_registry(
    registry_path: Path,
    policy: str,
    diagnostics: list[dict],
) -> dict[str, Any]:
    try:
        registry = load_json_object(registry_path, "claim registry")
    except RuntimeError as exc:
        add_seed_diag(diagnostics, policy, "CLAIM_REGISTRY_INVALID", str(exc), file=registry_path, hard=True)
        return {}
    claims = registry.get("claims")
    if not isinstance(claims, dict):
        add_seed_diag(
            diagnostics,
            policy,
            "CLAIM_REGISTRY_INVALID",
            "claim registry 的 claims 必须是对象",
            file=registry_path,
            hard=True,
        )
        return {}
    if str(registry.get("schema_version", "")) != "1.0.0":
        add_seed_diag(
            diagnostics,
            policy,
            "CLAIM_REGISTRY_INVALID",
            "claim registry schema_version 必须为 1.0.0",
            file=registry_path,
            hard=True,
            metrics={"actual": registry.get("schema_version", "")},
        )
    if str(registry.get("registry_version", "")) != "2026-09-02-LH5":
        add_seed_diag(
            diagnostics,
            policy,
            "CLAIM_REGISTRY_INVALID",
            "claim registry registry_version 必须为 2026-09-02-LH5",
            file=registry_path,
            hard=True,
        )
    try:
        date.fromisoformat(str(registry.get("verified_at", "")))
    except (TypeError, ValueError):
        add_seed_diag(
            diagnostics,
            policy,
            "CLAIM_REGISTRY_INVALID",
            "claim registry verified_at 必须是 YYYY-MM-DD",
            file=registry_path,
            hard=True,
        )
    fact_levels = registry.get("fact_levels")
    if not isinstance(fact_levels, dict) or set(fact_levels) != set(P_RANK):
        add_seed_diag(
            diagnostics,
            policy,
            "CLAIM_REGISTRY_INVALID",
            "claim registry fact_levels 必须完整定义 P0/P1/P2",
            file=registry_path,
            hard=True,
        )
    registry_models = string_list(registry.get("model_ids", []))
    if registry_models is None or set(registry_models) != VALID_MODELS:
        add_seed_diag(
            diagnostics,
            policy,
            "CLAIM_REGISTRY_INVALID",
            "claim registry model_ids 与检查器支持型号不一致",
            file=registry_path,
            hard=True,
            metrics={"actual": registry_models or [], "expected": sorted(VALID_MODELS)},
        )
    known_false_assertions = registry.get("known_false_assertions")
    known_false_issues: list[str] = []
    if not isinstance(known_false_assertions, list):
        known_false_issues.append("not_array")
    else:
        seen_known_false_ids: set[str] = set()
        for index, assertion in enumerate(known_false_assertions):
            prefix = f"[{index}]"
            if not isinstance(assertion, dict):
                known_false_issues.append(f"{prefix}:not_object")
                continue
            assertion_id = assertion.get("id")
            models = string_list(assertion.get("models"))
            pattern = assertion.get("pattern")
            message = assertion.get("message")
            if not isinstance(assertion_id, str) or not assertion_id.strip() or assertion_id in seen_known_false_ids:
                known_false_issues.append(f"{prefix}:id")
            else:
                seen_known_false_ids.add(assertion_id)
            if not models or any(model not in VALID_MODELS - {"unknown"} for model in models):
                known_false_issues.append(f"{prefix}:models")
            if not isinstance(pattern, str) or not pattern.strip():
                known_false_issues.append(f"{prefix}:pattern")
            else:
                try:
                    re.compile(pattern, re.IGNORECASE)
                except re.error:
                    known_false_issues.append(f"{prefix}:pattern")
            if not isinstance(message, str) or not message.strip():
                known_false_issues.append(f"{prefix}:message")
    if known_false_issues:
        add_seed_diag(
            diagnostics,
            policy,
            "CLAIM_REGISTRY_INVALID",
            "claim registry 的 known_false_assertions 类型或正则无效",
            file=registry_path,
            hard=True,
            metrics={"issues": known_false_issues[:30], "issue_count": len(known_false_issues)},
        )
    invariants = registry.get("global_invariants")
    required_invariants = {
        "watermark_counts_as_evidence": False,
        "product_name_only_has_s_level": False,
        "current_post_model_assertion_min_m": "M2",
        "causal_attribution_min_f": "F2",
        "comparative_result_min_f": "F3",
        "scenario_fit_min_n": "N1",
        "scenario_fit_requires_conditional_language": True,
        "p0_claims_forbidden_above_s1": True,
    }
    if not isinstance(invariants, dict) or any(invariants.get(key) != value for key, value in required_invariants.items()):
        add_seed_diag(
            diagnostics,
            policy,
            "CLAIM_REGISTRY_INVALID",
            "claim registry global_invariants 与 LH5 门禁不一致",
            file=registry_path,
            hard=True,
        )
    claim_schema_issues: list[str] = []
    for claim_id, claim in claims.items():
        if not isinstance(claim, dict):
            claim_schema_issues.append(f"{claim_id}:not_object")
            continue
        required_fields = {
            "label",
            "models",
            "scope",
            "fact_status_required",
            "causal_min_feature_use",
            "scene_need_tags",
            "text_terms",
            "boundaries",
            "official_sources",
        }
        missing = sorted(required_fields - set(claim))
        if missing:
            claim_schema_issues.append(f"{claim_id}:missing={','.join(missing)}")
            continue
        if not isinstance(claim.get("label"), str) or not str(claim.get("label", "")).strip():
            claim_schema_issues.append(f"{claim_id}:label")
        models = string_list(claim.get("models"))
        scene_tags = string_list(claim.get("scene_need_tags"))
        text_terms = string_list(claim.get("text_terms"))
        boundaries = string_list(claim.get("boundaries"))
        sources = string_list(claim.get("official_sources"))
        if not models or any(model not in VALID_MODELS - {"unknown"} for model in models):
            claim_schema_issues.append(f"{claim_id}:models")
        if not scene_tags:
            claim_schema_issues.append(f"{claim_id}:scene_need_tags")
        if not text_terms:
            claim_schema_issues.append(f"{claim_id}:text_terms")
        if not boundaries:
            claim_schema_issues.append(f"{claim_id}:boundaries")
        if not sources or any(
            not normalized_source_url(source).startswith(("store.dji.com/", "www.dji.com/", "dji.com/"))
            for source in sources
        ):
            claim_schema_issues.append(f"{claim_id}:official_sources")
        if claim.get("scope") not in {"shared", "differentiator"}:
            claim_schema_issues.append(f"{claim_id}:scope")
        if str(claim.get("fact_status_required", "")).upper() not in {"P1", "P2"}:
            claim_schema_issues.append(f"{claim_id}:fact_status_required")
        if str(claim.get("causal_min_feature_use", "")).upper() not in {"F2", "F3"}:
            claim_schema_issues.append(f"{claim_id}:causal_min_feature_use")
        if claim.get("scope") == "differentiator" and not string_list(claim.get("s3_boundary_terms", [])):
            claim_schema_issues.append(f"{claim_id}:s3_boundary_terms")
        for field_name in ("required_text_groups",):
            groups = claim.get(field_name, [])
            if not isinstance(groups, list) or any(not string_list(group) for group in groups):
                claim_schema_issues.append(f"{claim_id}:{field_name}")
        if "benefit_required_terms" in claim and not string_list(claim.get("benefit_required_terms")):
            claim_schema_issues.append(f"{claim_id}:benefit_required_terms")
        patterns = claim.get("forbidden_text_patterns", [])
        if not isinstance(patterns, list):
            claim_schema_issues.append(f"{claim_id}:forbidden_text_patterns")
        else:
            for pattern in patterns:
                if not isinstance(pattern, str) or not pattern.strip():
                    claim_schema_issues.append(f"{claim_id}:forbidden_text_patterns")
                    break
                try:
                    re.compile(pattern, re.IGNORECASE)
                except re.error:
                    claim_schema_issues.append(f"{claim_id}:forbidden_text_patterns")
                    break
        more_specific = claim.get("more_specific_claim")
        if more_specific is not None:
            if not isinstance(more_specific, dict):
                claim_schema_issues.append(f"{claim_id}:more_specific_claim")
            else:
                specific_id = str(more_specific.get("claim_id", "")).strip()
                trigger_groups = more_specific.get("when_all_text_groups")
                if specific_id not in claims or not isinstance(trigger_groups, list) or not trigger_groups or any(
                    not string_list(group) for group in trigger_groups
                ):
                    claim_schema_issues.append(f"{claim_id}:more_specific_claim")
    if claim_schema_issues:
        add_seed_diag(
            diagnostics,
            policy,
            "CLAIM_REGISTRY_INVALID",
            "claim registry 含不完整或类型错误的卖点定义",
            file=registry_path,
            hard=True,
            metrics={"issues": claim_schema_issues[:30], "issue_count": len(claim_schema_issues)},
        )
    return registry


def audit_structure(sections: list[Section], diagnostics: list[dict], *, lh7: bool = False, lh12: bool = False, delivery_mode: str = "with_replies") -> None:
    for section in sections:
        valid_count = 2 <= len(section.groups) <= 4 if lh12 else 1 <= len(section.groups) <= 3 if lh7 else len(section.groups) == 3
        if not valid_count:
            expected_groups = "2–4组" if lh12 else "1–3组" if lh7 else "3组"
            diagnostics.append(diag("error", "E_GROUP_COUNT", f"章节应有{expected_groups}，实际为{len(section.groups)}组", section.file, section.line, section.number))
        for group in section.groups:
            count = len(group.replies)
            main_only = lh7 and delivery_mode == "main_only"
            if (count != 0 if main_only else not (0 if lh12 else 2) <= count <= 4):
                expected_replies = "0条回复（main_only）" if main_only else "0–4条回复" if lh12 else "2–4条回复"
                diagnostics.append(diag("error", "E_REPLY_COUNT", f"每组应有{expected_replies}，实际为{count}条", group.main.file, group.main.line, group.main.section, group.main.group))
            expected = list(range(1, count + 1))
            actual = [item.reply_no for item in group.replies]
            if any(value is None for value in actual) or actual != expected:
                diagnostics.append(diag("error", "E_REPLY_SEQUENCE", f"回复编号应连续为{expected}，实际为{actual}", group.main.file, group.main.line, group.main.section, group.main.group))


def lh7_has_sentence_period(text: str) -> bool:
    # Preserve URL punctuation, decimal points and both ellipsis spellings.
    if "。" in text:
        return True
    value = clean_raw(text)
    for match in reversed(list(COPY_URL_RE.finditer(value))):
        url = match.group(0).rstrip(".,!?;:)]}")
        value = value[: match.start()] + " " * len(url) + value[match.start() + len(url) :]
    value = re.sub(r"\.{2,}|…+|(?<=\d)\.(?=\d)", "", value)
    # A remaining period before a non-ASCII-word character is a sentence
    # stop, including stops followed by emoji or another punctuation mark.
    return bool(re.search(r"\.(?=$|[^A-Za-z0-9_])", value))


def lh8_personal_context(group_context: dict[str, Any]) -> tuple[set[str], list[str]]:
    """Validate source metadata, never infer post evidence from a personal model.

    A valid source reference is an auditable user-material locator, not proof
    of truth by itself. The writing workflow must inspect that material.
    """
    context = group_context.get("personal_context")
    if context is None:
        return set(), []
    if not isinstance(context, dict):
        return set(), ["personal_context"]
    issues = []
    source = context.get("source_ref")
    facts = context.get("facts")
    models = context.get("models")
    if not isinstance(source, str) or not source.strip():
        issues.append("personal_context.source_ref")
    if not isinstance(facts, list) or not facts or any(not isinstance(fact, str) or not fact.strip() for fact in facts):
        issues.append("personal_context.facts")
    if not isinstance(models, list) or any(not isinstance(model, str) or model not in LH7_CONTEXT_MODELS - {"unknown"} for model in models):
        issues.append("personal_context.models")
    return (set(models) if not issues else set()), issues


def audit_lh9_reply_sources(group: Group, context: dict[str, Any], turns: dict[int, dict[str, Any]], diagnostics: list[dict]) -> None:
    """Bind personal sources to speakers, not reply positions or interlocutors.

    Facts are human-reviewed evidence fragments. This function checks source
    ownership and model coverage; it cannot prove that prose follows from facts.
    """
    def issue(code: str, message: str, item: Item, **metrics: Any) -> None:
        diagnostics.append(diag("error", code, message, item.file, item.line, item.section, item.group, metrics=metrics))

    speaker_sources: dict[str, dict[str, Any]] = {}
    source_owners: dict[str, str] = {}
    main_source = context.get("personal_context")
    _, main_issues = lh8_personal_context(context)
    if isinstance(main_source, dict) and not main_issues:
        speaker_sources["A"] = dict(main_source)
        source_owners[clean_raw(main_source["source_ref"])] = "A"
    reply_contexts = context.get("reply_personal_contexts", {})
    if not isinstance(reply_contexts, dict):
        issue("E_REPLY_PERSONAL_CONTEXT_INVALID", "reply_personal_contexts 必须按实际回复序号映射说话者的真实材料", group.main)
        reply_contexts = {}
    actual_numbers = {str(reply.reply_no) for reply in group.replies}
    extra_keys = [str(key) for key in reply_contexts if not isinstance(key, str) or key not in actual_numbers]
    if extra_keys:
        issue("E_REPLY_PERSONAL_CONTEXT_INVALID", "个人材料序号必须对应实际交付的回复", group.main, keys=extra_keys)
    for reply in group.replies:
        turn = turns.get(reply.reply_no, {})
        speaker = turn.get("speaker")
        if not isinstance(speaker, str) or speaker not in {"A", "B", "C", "D", "E"}:
            continue  # Invalid turn metadata cannot authorize source inheritance.
        key = str(reply.reply_no)
        source = reply_contexts.get(key)
        _, source_issues = lh8_personal_context({"personal_context": source})
        invalid_explicit = key in reply_contexts and (not isinstance(source, dict) or bool(source_issues))
        if invalid_explicit:
            issue("E_REPLY_PERSONAL_CONTEXT_INVALID", "回复材料必须有非空 source_ref、facts 和合法 models", reply, fields=source_issues)
        elif source is not None:
            source_ref = clean_raw(source["source_ref"])
            prior = speaker_sources.get(speaker)
            if prior is not None and clean_raw(prior["source_ref"]) != source_ref:
                issue("E_DIALOGUE_SOURCE_CONFLICT", "同一说话者不能拼接不同 source_ref 冒充同一个人，请使用原来源补充事实", reply, speaker=speaker)
                invalid_explicit = True
            elif source_ref in source_owners and source_owners[source_ref] != speaker:
                issue("E_DIALOGUE_SOURCE_BORROWED", "不同说话者不能借用同一份个人材料，需分别定位各自来源", reply, speaker=speaker, source_owner=source_owners[source_ref])
                invalid_explicit = True
            else:
                merged = dict(source)
                if prior is not None:
                    merged["facts"] = list(dict.fromkeys([*prior["facts"], *source["facts"]]))
                    merged["models"] = list(dict.fromkeys([*prior["models"], *source["models"]]))
                speaker_sources[speaker] = merged
                source_owners[source_ref] = speaker
        effective = None if invalid_explicit else speaker_sources.get(speaker)
        if lh8_has_personal_history(reply.text):
            if effective is None:
                issue("E_REPLY_PERSONAL_CONTEXT_MISSING", "回复含明确本人经历，需该说话者自己的真实材料；A 可复用主评来源，其他人只能复用本人此前来源", reply, speaker=speaker)
            else:
                models = lh8_personal_history_models(reply.text)
                if models - set(effective["models"]):
                    issue("E_REPLY_PERSONAL_MODEL_UNGROUNDED", "回复中的本人型号未被该说话者来源支持；新增事实需在同来源补充并审稿", reply, speaker=speaker, models=sorted(models), personal_models=effective["models"])


def audit_lh9_dialogue(group: Group, context: dict[str, Any], diagnostics: list[dict], *, lh12: bool = False) -> None:
    def issue(code: str, message: str, item: Item | None = None, **metrics: Any) -> None:
        item = item or group.main
        diagnostics.append(diag("error", code, message, item.file, item.line, item.section, item.group, metrics=metrics))

    dialogue = context.get("dialogue")
    if lh12 and not group.replies and dialogue is None:
        if group.main.speaker is not None and group.main.speaker != "A":
            issue("E_DIALOGUE_LABEL_MISMATCH", "显式主评角色标签须与内部主评者A一致")
        audit_lh9_reply_sources(group, context, {}, diagnostics)
        return
    if not isinstance(dialogue, dict):
        issue("E_DIALOGUE_CONTEXT_MISSING", "LH9 有回复的评论组必须填写 dialogue.main_speaker 和逐条 replies 映射")
        return
    if dialogue.get("main_speaker") != "A":
        issue("E_DIALOGUE_MAIN_SPEAKER", "dialogue.main_speaker 必须为 A")
    if (not lh12 or group.main.speaker is not None) and group.main.speaker != "A":
        issue("E_DIALOGUE_LABEL_MISMATCH", "LH9 主评须标注主评论（A），并与 dialogue 一致")
    raw_turns = dialogue.get("replies")
    if not isinstance(raw_turns, list):
        issue("E_DIALOGUE_REPLY_MAPPING", "dialogue.replies 必须是按交付顺序排列的回复映射数组")
        return
    actual = {item.reply_no: item for item in group.replies}
    turns: dict[int, dict[str, Any]] = {}
    for entry in raw_turns:
        if not isinstance(entry, dict) or type(entry.get("reply")) is not int or entry.get("reply") not in actual:
            issue("E_DIALOGUE_REPLY_MAPPING", "每个 dialogue reply 必须用整数序号恰好映射一条实际回复")
            continue
        number = entry["reply"]
        if number in turns:
            issue("E_DIALOGUE_REPLY_MAPPING", "dialogue 中同一回复不能重复映射", actual[number], reply=number)
            continue
        turns[number] = entry
    if set(turns) != set(actual) or [entry.get("reply") if isinstance(entry, dict) else None for entry in raw_turns] != [item.reply_no for item in group.replies]:
        issue("E_DIALOGUE_REPLY_MAPPING", "dialogue 必须按顺序完整映射每条实际回复，不能遗漏、重复或换序")
    has_reply_exchange = False
    for reply in group.replies:
        entry = turns.get(reply.reply_no)
        if entry is None:
            continue
        speaker = entry.get("speaker")
        if not isinstance(speaker, str) or speaker not in {"A", "B", "C", "D", "E"}:
            issue("E_DIALOGUE_SPEAKER", "回复 speaker 必须是 A、B、C、D 或 E，不用博主身份", reply)
        move = entry.get("response_move")
        if not isinstance(move, str) or not move.strip():
            issue("E_DIALOGUE_RESPONSE_MOVE", "response_move 应简短写明这句如何回应父句，不限定固定套路", reply)
        parent_ref = entry.get("reply_to")
        parent = None
        parent_speaker = None
        if parent_ref == "main":
            parent, parent_speaker = group.main, "A"
        elif isinstance(parent_ref, str) and re.fullmatch(r"reply:[1-4]", parent_ref):
            parent_number = int(parent_ref.split(":")[1])
            if type(reply.reply_no) is int and parent_number < reply.reply_no and parent_number in actual and parent_number in turns:
                parent = actual[parent_number]
                parent_speaker = turns[parent_number].get("speaker")
                has_reply_exchange = True
        if parent is None or (reply.reply_no == 1 and parent_ref != "main"):
            issue("E_DIALOGUE_PARENT", "reply_to 只能指向本组 main 或更早存在的 reply:n，第一条必须回 main", reply)
            continue
        if speaker == parent_speaker:
            issue("E_DIALOGUE_SELF_REPLY", "同一说话者不能回复自己，请检查话轮和被回复对象", reply)
        if (not lh12 or reply.speaker is not None or reply.reply_target is not None) and (reply.speaker != speaker or reply.reply_target != parent_speaker):
            issue("E_DIALOGUE_LABEL_MISMATCH", "回复标签须为（说话者→被回复者），且与 dialogue 中实际父句一致", reply, expected=f"{speaker}→{parent_speaker}")
        quote = entry.get("anchor_quote")
        if not isinstance(quote, str) or not clean_raw(quote) or clean_raw(quote) not in clean_raw(parent.text):
            issue("E_DIALOGUE_ANCHOR_QUOTE", "anchor_quote 必须是被回复正文中非空的实际片段，不能引用别句或仅填主题标签", reply)
    if not lh12 and not has_reply_exchange:
        issue("E_DIALOGUE_NO_EXCHANGE", "至少一条回复须接住前面的回复，不能所有人只分别回复主评")
    audit_lh9_reply_sources(group, context, turns, diagnostics)


def audit_lh9_dialogues(sections: list[Section], contexts: dict[str, list[dict[str, Any]]], state: dict[str, Any], diagnostics: list[dict]) -> dict[str, Any]:
    """Run structural gates even with seeding checks off; no semantic certification."""
    checked = 0
    lh12 = state.get("rule_version") == LH12_RULE_VERSION
    section_counts = Counter(section.number for section in sections)
    for section in sections:
        path = str(Path(section.file).resolve())
        candidates = contexts.get(section.number, [])
        if len(candidates) == 1 and section_counts[section.number] == 1:
            matches = candidates if candidates[0].get("_resolved_draft_path") in {None, "", path} else []
        else:
            matches = [context for context in candidates if context.get("_resolved_draft_path") == path]
        allocation = matches[0] if len(matches) == 1 else {}
        raw_groups = allocation.get("groups", [])
        for group in section.groups:
            if not group.replies and not lh12:
                continue  # main_only has no dialogue requirement; counts are checked separately.
            checked += 1
            group_contexts = [entry for entry in raw_groups if isinstance(entry, dict) and entry.get("group") == group.main.group] if isinstance(raw_groups, list) else []
            audit_lh9_dialogue(group, group_contexts[0] if len(group_contexts) == 1 else {}, diagnostics, lh12=lh12)
    for finding in diagnostics:
        if finding["code"] == "W_UNPARSED_LINE" and re.match(r"(?:主评论|↳\s*回复)", finding.get("text", "")):
            finding.update(severity="error", code="E_DIALOGUE_LABEL_INVALID", message="LH9 评论行未解析，使用主评论（A）：或 ↳ 回复1（B→A）：格式")
    return {"groups_checked": checked, "semantic_review_required": True, "note": "仅验证话轮、父句引用和来源归属，互动自然度、新增事实覆盖和说话者一致性仍须人工或模型逐句审稿"}


def audit_lh10_diversity(
    sections: list[Section], contexts: dict[str, list[dict[str, Any]]],
    state: dict[str, Any], diagnostics: list[dict],
) -> tuple[dict[str, Any], set[str]]:
    """Require recorded semantic comparison; identical wording is only a hard floor.

    Free-form descriptions are intentionally not style enums. A passed record is
    a reviewer declaration, not this checker's proof of distinct meaning.
    """
    qa = state.get("qa")
    semantic = qa.get("semantic_review") if isinstance(qa, dict) else None
    reviews = semantic.get("diversity_review") if isinstance(semantic, dict) else None
    records: dict[str, list[dict[str, Any]]] = defaultdict(list)
    if not isinstance(reviews, list):
        diagnostics.append(diag("error", "E_DIVERSITY_REVIEW_MISSING", "LH10/LH11 缺少 qa.semantic_review.diversity_review 逐帖并排复核记录"))
        reviews = []
    for record in reviews:
        if not isinstance(record, dict) or not isinstance(record.get("id"), str) or not record["id"].strip():
            diagnostics.append(diag("error", "E_DIVERSITY_REVIEW_INVALID", "diversity_review 每项须有非空 allocation.id"))
            continue
        records[record["id"].strip()].append(record)
    known_ids = {str(allocation.get("id", "")).strip() for candidates in contexts.values() for allocation in candidates}
    for allocation_id in records.keys() - known_ids:
        diagnostics.append(diag("error", "E_DIVERSITY_REVIEW_ORPHAN", "diversity_review.id 未对应 state 中的链接", metrics={"id": allocation_id}))
    section_counts = Counter(section.number for section in sections)
    passed_ids: set[str] = set()
    for section in sections:
        path = str(Path(section.file).resolve())
        candidates = contexts.get(section.number, [])
        if len(candidates) == 1 and section_counts[section.number] == 1:
            matches = candidates if candidates[0].get("_resolved_draft_path") in {None, "", path} else []
        else:
            matches = [candidate for candidate in candidates if candidate.get("_resolved_draft_path") == path]
        allocation = matches[0] if len(matches) == 1 else {}
        allocation_id = str(allocation.get("id", "")).strip()
        valid = True

        def issue(code: str, message: str, group: Group | None = None, **metrics: Any) -> None:
            nonlocal valid
            valid = False
            item = group.main if group else section
            diagnostics.append(diag("error", code, message, item.file, item.line, section.number, group.main.group if group else None, metrics=metrics or None))

        matched_reviews = records.get(allocation_id, [])
        if len(matched_reviews) != 1:
            issue("E_DIVERSITY_REVIEW_MISSING" if not matched_reviews else "E_DIVERSITY_REVIEW_DUPLICATE", "每个交付链接须恰好一条 diversity_review 记录", id=allocation_id)
        else:
            record = matched_reviews[0]
            if record.get("verdict") == "revise":
                issue("E_DIVERSITY_REVIEW_REVISE", "并排语义复核仍为 revise，修改并重审后才可交付", id=allocation_id)
            elif record.get("verdict") != "passed":
                issue("E_DIVERSITY_REVIEW_INVALID", "diversity_review.verdict 只能为 passed 或 revise，空值表示尚未验收", id=allocation_id)
            reason = record.get("comparison_reason")
            if not isinstance(reason, str) or not keep_word_chars(clean_raw(reason)):
                issue("E_DIVERSITY_REVIEW_REASON_MISSING", "comparison_reason 须说明各组主导表达并排比较后的实义差异", id=allocation_id)
        raw_groups = allocation.get("groups", [])
        expressions: dict[str, int] = {}
        for group in section.groups:
            mapped = [entry for entry in raw_groups if isinstance(entry, dict) and entry.get("group") == group.main.group] if isinstance(raw_groups, list) else []
            group_context = mapped[0] if len(mapped) == 1 else {}
            for field in ("dominant_expression", "product_connection"):
                if (field == "product_connection" and state.get("rule_version") in LH11_PLUS_RULE_VERSIONS
                        and lh11_visual_only_group(group, group_context, lh12=state.get("rule_version") == LH12_RULE_VERSION)):
                    continue
                value = group_context.get(field)
                normalized = keep_word_chars(clean_raw(value)).lower() if isinstance(value, str) else ""
                if not normalized:
                    issue("E_LH10_" + field.upper() + "_MISSING", f"每组必须用自由短句填写 {field}，并对照实际正文验收", group)
                elif field == "dominant_expression":
                    if normalized in expressions:
                        issue("E_DOMINANT_EXPRESSION_DUPLICATE", "同帖主导表达描述明确重复；只换标点或措辞标签不能证明实际说了不同内容", group, other_group=expressions[normalized])
                    expressions[normalized] = group.main.group
        if valid:
            passed_ids.add(allocation_id)
    return ({"sections_checked": len(sections), "records_passed": len(passed_ids), "semantic_review_required": True,
             "note": "仅核验复核记录、必要描述和明确重复；不同描述、不同模式或 passed 标签不自动证明三条实义不同，须逐帖并排审稿"}, passed_ids)


def lh8_current_model_assertions(text: str, *, lh12: bool = False) -> list[re.Match[str]]:
    matches = []
    for match in LH8_CURRENT_MODEL_ASSERTION_RE.finditer(text):
        # Personal recollections do not identify the original post's camera.
        # Missing personal sources have their own diagnostic instead.
        clause_start = max(text.rfind(mark, 0, match.start()) for mark in "，,。！？!?；;\n") + 1
        prefix = text[clause_start:match.start()]
        clause_end = next((index for index in range(match.end(), len(text)) if text[index] in "，,。！？!?；;\n"), len(text))
        if lh12:
            clause = text[clause_start:clause_end + 1]
            # A question protects only its own clause, not another claim in
            # the same turn. Explicit rhetorical assertions stay reviewable.
            rhetorical = re.search(r"难道|难不成|不就是|不正是|岂不是|肯定|一定|当然|明明|显然|毫无疑问", clause)
            crosses_clause = re.search(r"[，,。！？!?；;\n]", match.group(0))
            if QUESTION_RE.search(clause.rstrip("，,。；;\n")) and not rhetorical and not crosses_clause:
                continue
        personal_recollection = (
            re.search(r"我(?:的|上次|之前|去年|刚|那次|昨天|用|拿|带)|(?:上次|去年|之前)(?:用|拿|带)", prefix)
            and not re.search(r"原片|博主|作者|你|当前画面", text[clause_start:clause_end])
        )
        if not personal_recollection:
            matches.append(match)
    return matches


def lh8_personal_hardware_assertions(text: str) -> list[str]:
    """Find explicit product capability claims, not tutorial/user relief words."""
    claims = []
    previous_product_reference = False
    for clause in re.split(r"[，,。！？!?；;\n]", text):
        named_product = bool(find_product_match(clause))
        device_pronoun = bool(previous_product_reference and re.match(r"\s*(?:(?:而且|听说|据说|然后|另外|但是|不过)\s*)?(?:它|这台(?:机器|设备|相机)?|这个(?:机器|设备|相机))", clause))
        previous_product_reference = named_product or device_pronoun
        if not (previous_product_reference and LH8_HARDWARE_TERM_RE.search(clause)):
            continue
        assertion = LH8_CAPABILITY_ASSERTION_RE.search(clause)
        if assertion and not match_is_negated(clause, assertion) and not QUESTION_RE.search(clause):
            claims.append(clause)
    return claims


def lh10_group_product_facts(group: Group, context: dict[str, Any], *, lh11: bool = False, lh12: bool = False) -> tuple[list[str], list[str]]:
    """Find assertions per turn using its actual dialogue parent's referent.

    Neutral acknowledgements preserve device references; named non-devices
    break them. Questions and negation are checked within the asserted clause.
    This is a conservative text gate, not semantic certification.
    """
    dialogue = context.get("dialogue")
    raw_turns = dialogue.get("replies", []) if isinstance(dialogue, dict) else []
    turns = {entry.get("reply"): entry for entry in raw_turns if isinstance(entry, dict) and type(entry.get("reply")) is int} if isinstance(raw_turns, list) else {}
    device_contexts: dict[str, bool] = {}
    non_device_contexts: dict[str, bool] = {}
    capabilities: list[str] = []
    causes: list[str] = []
    non_device = re.compile(r"猫|狗|杯子|纸箱|箱子|小孩|宝宝|博主本人|手机|其他设备")
    lh11_non_device = re.compile(non_device.pattern + r"|(?:博主|姐姐|妹妹|哥哥|弟弟|男生|女生|人物|她|他)(?!台)")
    pronoun = re.compile(r"它|这台(?:机器|设备|相机)?|这个(?:机器|设备|相机)")
    neutral = re.compile(r"\s*(?:确实|对|对啊|是啊|是的|嗯|嗯嗯|哦|噢|哈哈|哈哈哈|好像是|听说|据说|而且|然后|另外|不过|但是)\s*[，,。！？!?；;]?\s*")
    implicit = re.compile(r"\s*(?:支持|具备|配有|带有|能够|自带|拥有|能(?:拍|录|跟|收)|可以(?:拍|录|跟|收))")
    for item in [group.main, *group.replies]:
        reference = "main" if item is group.main else f"reply:{item.reply_no}"
        parent = turns.get(item.reply_no, {}).get("reply_to") if item is not group.main else None
        device_context = device_contexts.get(parent, False) if isinstance(parent, str) else False
        non_device_context = non_device_contexts.get(parent, False) if isinstance(parent, str) else False
        for piece in re.finditer(r"[^，,。！？!?；;\n]+[，,。！？!?；;\n]?", lh7_fact_text(item.text)):
            clause = piece.group(0)
            if neutral.fullmatch(clause):
                continue
            product_match = find_product_match(clause)
            named_product = bool(product_match)
            assertion = LH8_CAPABILITY_ASSERTION_RE.search(clause)
            # An animal after the capability verb is the filming object, not
            # a replacement subject: "Pocket能拍4K视频给小孩留念" stays factual.
            subject_prefix = clause[:assertion.start()] if assertion else clause
            other_subjects = list((lh11_non_device if lh11 else non_device).finditer(subject_prefix))
            explicit_non_device = bool(other_subjects and (product_match is None or other_subjects[-1].start() > product_match.start()))
            refers_to_device = not explicit_non_device and (named_product or (device_context and bool(pronoun.search(clause) or implicit.match(clause))))
            if lh11:
                device_match = LH11_DEVICE_REFERENCE_RE.search(subject_prefix)
                explicit_device = bool(device_match and (not other_subjects or device_match.start() > other_subjects[-1].start()))
                device_reference = product_match or device_match
                if device_reference and LH11_DEVICE_OWNER_PREDICATE_RE.fullmatch(clause[device_reference.end():]):
                    # "这台相机是她的" identifies the device's owner; 她 is
                    # not a new subject for the next clause's capability.
                    explicit_device = True
                    explicit_non_device = False
                # A visual parent need not name a camera. An explicit device or
                # unambiguous specification still starts a factual discussion;
                # an animal/person antecedent does not become a camera via 它.
                spec_subject = bool(assertion and LH11_EXPLICIT_SPEC_RE.search(clause)
                                    and (pronoun.search(subject_prefix) or implicit.match(clause))
                                    and not non_device_context and not explicit_non_device)
                refers_to_device = explicit_device or refers_to_device or spec_subject
                if explicit_device:
                    explicit_non_device = False
            if (lh12 and device_context and not explicit_non_device
                    and LH12_IMPLIED_STABILITY_ASSERTION_RE.fullmatch(clause)
                    and not QUESTION_RE.search(clause)):
                # "这台支持4K？那肯定很稳" still makes a performance
                # inference after the question, even with an omitted subject.
                capabilities.append(clause)
                refers_to_device = True
            if refers_to_device and LH8_HARDWARE_TERM_RE.search(clause):
                if assertion and not match_is_negated(clause, assertion) and not QUESTION_RE.search(clause):
                    capabilities.append(clause)
            for causal_match in LH10_CURRENT_RESULT_CAUSAL_RE.finditer(clause):
                causal_words = causal_match.group(0)
                product_cause = bool(find_product_match(causal_words) or LH8_HARDWARE_TERM_RE.search(causal_words) or (refers_to_device and pronoun.search(causal_words))
                                     or (lh11 and LH11_DEVICE_REFERENCE_RE.search(causal_words)))
                tutorial_clarity = re.search(r"(?:讲|说|解释|分析)(?:得|的|得很|得挺)?清楚", causal_words)
                if product_cause and not explicit_non_device and not tutorial_clarity and not match_is_negated(clause, causal_match) and not QUESTION_RE.search(clause):
                    causes.append(clause)
            device_context = refers_to_device
            non_device_context = explicit_non_device or (non_device_context and not refers_to_device and bool(pronoun.search(clause)))
        device_contexts[reference] = device_context
        non_device_contexts[reference] = non_device_context
    return capabilities, causes


def lh11_visual_only_group(group: Group, context: dict[str, Any], *, lh12: bool = False) -> bool:
    """Only a whole observed/S0 group can omit its product connection.

    Grounding and distinct meaning remain separate anchor and reviewer gates.
    Sibling comments never participate in this group's product/fact decision.
    """
    if (context.get("claim_mode") != "observed" or context.get("target_s_level") != "S0"
            or context.get("actual_s_level") != "S0" or context.get("benefit_basis") != "visual"):
        return False
    if any(lh7_product_matches(item.text) for item in [group.main, *group.replies]):
        return False
    capabilities, causes = lh10_group_product_facts(group, context, lh11=True, lh12=lh12)
    return not (capabilities or causes)


def lh8_other_person_models(text: str) -> set[str]:
    """A personal model source cannot name the creator's unidentified camera."""
    result: set[str] = set()
    for clause in re.split(r"[，,。！？!?；;\n]", lh7_fact_text(text)):
        for match in re.finditer(r"(?:你|博主|作者|原片)(?:的|用的|手里(?:的)?|手中(?:的)?|拿着的|这台|那台|拍的|那个|这个|是|就是){0,3}Pocket(?:4P|4|3|2|1)", clause, re.IGNORECASE):
            result.update(extract_models(match.group(0), lh7=True))
    return result


def lh8_soft_purchase_terms(text: str) -> list[str]:
    terms = []
    for match in SOFT_PURCHASE_RE.finditer(text):
        if match.group(0) in {"入手", "下单"}:
            prefix = text[max(0, match.start() - 12):match.start()]
            suffix = text[match.end():match.end() + 2]
            if re.search(r"(?:刚刚|刚|已经|已|去年|上次|之前|前几天|昨天)(?:才)?$", prefix) or suffix.startswith("了"):
                continue
        terms.append(match.group(0))
    return terms


def lh8_has_personal_history(text: str) -> bool:
    # Quoted creator speech is not the commenting person's biography.
    value = re.sub(r"[“\"「『][^”\"」』]*[”\"」』]", "", text)
    value = re.sub(r"(?:博主|作者|你)(?:说|写|提到|刚说)[^，,。！？!?；;\n]*", "", value)
    return bool(LH8_PERSONAL_HISTORY_RE.search(value))


def lh8_personal_history_models(text: str) -> set[str]:
    """Limit biography-model checks to recollections, not a desired upgrade."""
    models = set()
    for clause in re.split(r"[，,。！？!?；;\n]", text):
        if not lh8_has_personal_history(clause):
            continue
        for match in lh7_product_matches(clause):
            prefix = clause[max(0, match.start() - 12):match.start()]
            if re.search(r"(?:想|考虑|准备|打算|计划)(?:买|入手?|换|升级(?:到)?|试)(?:一台)?$|(?:换成|升级到)$", prefix):
                continue
            model = lh7_model_for_label(match.group(0))
            if model != "unknown":
                models.add(model)
    return models


def audit_lh7_copy(sections: list[Section], state: dict[str, Any], diagnostics: list[dict]) -> None:
    """Check only deliverable bodies; headings, URLs and audit notes stay untouched."""
    delivery_mode = state.get("delivery_mode", "with_replies")
    if not isinstance(delivery_mode, str) or delivery_mode not in {"with_replies", "main_only"}:
        diagnostics.append(diag("error", "E_LH7_DELIVERY_MODE", "delivery_mode 必须是 with_replies 或 main_only"))
    for section in sections:
        label_groups: dict[str, list[Item]] = defaultdict(list)
        for group in section.groups:
            matches = lh7_product_matches(group.main.text)
            if not matches and state.get("rule_version") not in LH11_PLUS_RULE_VERSIONS:
                diagnostics.append(diag("error", "E_MAIN_PRODUCT_NAME_MISSING", "每条主评必须明确点名 Pocket 产品；代词、仅品牌名或竞品名不能替代", group.main.file, group.main.line, group.main.section, group.main.group))
            for label in {re.sub(r"\s+", "", clean_raw(match.group(0))).lower() for match in matches}:
                label_groups[label].append(group.main)
            for item in [group.main, *group.replies]:
                if state.get("rule_version") in LH8_PLUS_RULE_VERSIONS and LH8_OSMO_RE.search(item.text):
                    diagnostics.append(diag("error", "E_COPY_OSMO_NAME", "LH8/LH9/LH10/LH11 评论正文不使用 Osmo，改用 Pocket 或已确认的型号称呼", item.file, item.line, item.section, item.group))
                product_matches = [*LH7_PRODUCT_RE.finditer(item.text), *LH7_OTHER_PRODUCT_RE.finditer(item.text)]
                spaced = sorted({match.group(0) for match in product_matches if re.search(r"\s", match.group(0))})
                if spaced:
                    diagnostics.append(diag("error", "E_PRODUCT_INTERNAL_SPACE", "评论正文中的英文产品名与型号必须连写", item.file, item.line, item.section, item.group, metrics={"names": spaced}))
                if lh7_has_sentence_period(item.text):
                    diagnostics.append(diag("error", "E_COPY_SENTENCE_PERIOD", "主评和回复正文不使用中文句号或句末英文句点", item.file, item.line, item.section, item.group))
        for label, items in label_groups.items():
            if len(items) > 1:
                add_pair_diag(diagnostics, "error", "E_MAIN_PRODUCT_NAME_REPEAT", f"同一帖子多条主评重复产品称呼“{label}”，请使用同型号的不同清晰称呼", items[0], items[1])


def audit_lh7_allocation(section: Section, context: dict[str, Any], diagnostics: list[dict], *, lh8: bool = False, lh11: bool = False, lh12: bool = False) -> None:
    """Bind reduced delivery and named main models to the resolved post evidence."""
    reason = context.get("reduced_output_reason", "")
    if not lh12 and len(section.groups) in {1, 2} and (not isinstance(reason, str) or not reason.strip()):
        diagnostics.append(diag("error", "E_REDUCED_OUTPUT_REASON", "素材不足交付1–2条主评时，allocation.reduced_output_reason 必须说明减量依据", section.file, section.line, section.number))
    raw_groups = context.get("groups", [])
    actual_numbers = {group.main.group for group in section.groups}
    context_numbers = [candidate.get("group") for candidate in raw_groups if isinstance(candidate, dict)] if isinstance(raw_groups, list) else []
    try:
        context_numbers = [int(number) for number in context_numbers]
    except (ValueError, TypeError):
        context_numbers = []
    if set(context_numbers) != actual_numbers or len(context_numbers) != len(actual_numbers):
        diagnostics.append(diag("error", "E_LH7_GROUP_CONTEXT_COUNT", "allocation.groups 必须与实际交付的评论组一一对应", section.file, section.line, section.number, metrics={"actual_groups": sorted(actual_numbers), "state_groups": context_numbers}))
    model_status = context.get("model_status", {})
    if not isinstance(model_status, dict):
        return  # The evidence validator reports malformed model_status.
    level = str(model_status.get("level", "")).upper()
    known = set()
    if level == "M2":
        known.add(normalize_model(model_status.get("confirmed_model")))
    if level in {"M1", "M2"}:
        known.add(normalize_model(model_status.get("claimed_model")))
        mixed = model_status.get("mixed_models", [])
        if isinstance(mixed, list):
            known.update(normalize_model(value) for value in mixed)
    known.discard("unknown")
    for group in section.groups:
        group_context = next((candidate for candidate in raw_groups if isinstance(candidate, dict) and str(candidate.get("group")) == str(group.main.group)), {}) if isinstance(raw_groups, list) else {}
        personal_models, _ = lh8_personal_context(group_context) if lh8 else (set(), [])
        models = {lh7_model_for_label(match.group(0)) for match in lh7_product_matches(group.main.text)} - {"unknown"}
        unsupported = (models - known - personal_models) | ((lh8_other_person_models(group.main.text) - known) if lh8 else set())
        if unsupported:
            message = "主评型号必须来自原帖证据或本组真实个人材料；未知时使用 Pocket 产品线称呼" if lh8 else "主评型号必须来自原帖型号证据，未知时使用 Pocket 产品线称呼；不能为换称呼猜代际"
            diagnostics.append(diag("error", "E_MAIN_MODEL_UNGROUNDED", message, group.main.file, group.main.line, group.main.section, group.main.group, metrics={"models": sorted(models), "evidenced_models": sorted(known), "personal_models": sorted(personal_models), "model_level": level}))
        if lh11:
            # Once mains may stay visual, product discussion can begin in a
            # reply. Bind those labels to this post or this speaker's source,
            # never a sibling group's named main or another speaker's source.
            speaker_models = {"A": set(personal_models)}
            dialogue = group_context.get("dialogue", {})
            turns = dialogue.get("replies", []) if isinstance(dialogue, dict) else []
            turn_map = {turn.get("reply"): turn for turn in turns if isinstance(turn, dict)} if isinstance(turns, list) else {}
            reply_sources = group_context.get("reply_personal_contexts", {})
            for reply in group.replies:
                speaker = turn_map.get(reply.reply_no, {}).get("speaker")
                if not isinstance(speaker, str) or speaker not in {"A", "B", "C", "D", "E"}:
                    continue  # Invalid identities are already rejected by dialogue validation.
                source = reply_sources.get(str(reply.reply_no)) if isinstance(reply_sources, dict) else None
                source_models, issues = lh8_personal_context({"personal_context": source})
                if source is not None and not issues and speaker in {"A", "B", "C", "D", "E"}:
                    speaker_models.setdefault(speaker, set()).update(source_models)
                own_models = speaker_models.get(speaker, set())
                reply_models = {lh7_model_for_label(match.group(0)) for match in lh7_product_matches(reply.text)} - {"unknown"}
                ungrounded = (reply_models - known - own_models) | (lh8_other_person_models(reply.text) - known)
                if ungrounded:
                    diagnostics.append(diag("error", "E_REPLY_MODEL_UNGROUNDED", "回复点名型号须来自本帖证据或该说话者自己的真实材料，不能借同帖其他组补证", reply.file, reply.line, reply.section, reply.group, metrics={"models": sorted(ungrounded), "evidenced_models": sorted(known), "personal_models": sorted(own_models)}))


def audit_duplicates(items: list[Item], diagnostics: list[dict], role: str) -> None:
    exact: dict[str, list[Item]] = defaultdict(list)
    canon: dict[str, list[Item]] = defaultdict(list)
    for item in items:
        exact[clean_raw(item.text)].append(item)
        canon[canonical(item.text, lh7=item.lh7)].append(item)

    for value, matches in exact.items():
        if len(matches) < 2:
            continue
        if role == "reply" and (valid_len(value) <= 6 or value in SHORT_REPLY_EXEMPT):
            same_group = defaultdict(list)
            for item in matches:
                same_group[(item.file, item.section, item.group)].append(item)
            for group_matches in same_group.values():
                if len(group_matches) >= 2:
                    add_pair_diag(diagnostics, "error", "E_EXACT_REPLY_LOCAL", "同一楼中楼出现重复回复", group_matches[0], group_matches[1])
            if len(matches) > 3:
                add_pair_diag(
                    diagnostics,
                    "warning",
                    "W_SHORT_REPLY_REPEAT",
                    "同一条短回复在批次中出现超过3次",
                    matches[0],
                    matches[-1],
                    metrics={"count": len(matches), "text": value},
                )
            continue
        code = "E_EXACT_MAIN" if role == "main" else "W_EXACT_REPLY"
        severity = "error" if role == "main" else "warning"
        add_pair_diag(diagnostics, severity, code, "出现完全相同的主评论" if role == "main" else "不同评论组出现相同回复", matches[0], matches[1], metrics={"count": len(matches)})

    if role == "main":
        for value, matches in canon.items():
            if len(value) < 8 or len(matches) < 2:
                continue
            raw_values = {clean_raw(item.text) for item in matches}
            if len(raw_values) == 1:
                continue
            add_pair_diag(diagnostics, "error", "E_CANON_MAIN", "主评论只更换了型号、数字、标点或空格", matches[0], matches[1], metrics={"count": len(matches)})


def audit_near_duplicates(items: list[Item], diagnostics: list[dict], role: str) -> None:
    prepared = [(item, scaffold(item.text, lh7=item.lh7)) for item in items]
    for index, (left_item, left) in enumerate(prepared):
        min_length = 12 if role == "main" else 14
        if len(left) < min_length:
            continue
        for right_item, right in prepared[index + 1 :]:
            if len(right) < min_length:
                continue
            if role == "reply" and (left_item.file, left_item.section, left_item.group) == (right_item.file, right_item.section, right_item.group):
                continue
            ratio = min(len(left), len(right)) / max(len(left), len(right))
            if ratio < 0.72:
                continue
            dice_score = dice(left, right, 3)
            sequence_score = difflib.SequenceMatcher(None, left, right, autojunk=False).ratio()
            if role == "main":
                threshold_dice, threshold_sequence = ((0.78, 0.90) if max(len(left), len(right)) <= 23 else (0.70, 0.84))
            else:
                threshold_dice, threshold_sequence = 0.82, 0.92
            if dice_score >= threshold_dice and sequence_score >= threshold_sequence:
                add_pair_diag(
                    diagnostics,
                    "warning",
                    "W_NEAR_MAIN" if role == "main" else "W_NEAR_REPLY",
                    "主评论骨架高度相似" if role == "main" else "回复骨架高度相似",
                    left_item,
                    right_item,
                    metrics={"dice": round(dice_score, 3), "sequence": round(sequence_score, 3)},
                )


def audit_against_baseline(current: list[Item], baseline: list[Item], diagnostics: list[dict], role: str) -> None:
    """Compare new copy with history without auditing historical files as deliverables."""
    if not current or not baseline:
        return
    exact_index: dict[str, Item] = {}
    canonical_index: dict[str, Item] = {}
    for item in baseline:
        exact_index.setdefault(clean_raw(item.text), item)
        canonical_index.setdefault(canonical(item.text, lh7=item.lh7), item)

    for item in current:
        raw = clean_raw(item.text)
        if raw in exact_index:
            if role == "reply" and (valid_len(raw) <= 6 or raw in SHORT_REPLY_EXEMPT):
                continue
            add_pair_diag(
                diagnostics,
                "error" if role == "main" else "warning",
                "E_BASELINE_EXACT_MAIN" if role == "main" else "W_BASELINE_EXACT_REPLY",
                "主评论与历史成品完全相同" if role == "main" else "回复与历史成品完全相同",
                item,
                exact_index[raw],
            )
            continue

        normalized = canonical(item.text, lh7=item.lh7)
        if role == "main" and len(normalized) >= 8 and normalized in canonical_index:
            add_pair_diag(
                diagnostics,
                "error",
                "E_BASELINE_CANON_MAIN",
                "主评论与历史成品相比只更换了型号、数字、标点或空格",
                item,
                canonical_index[normalized],
            )
            continue

        left = scaffold(item.text, lh7=item.lh7)
        minimum = 12 if role == "main" else 14
        if len(left) < minimum:
            continue
        best: tuple[float, float, Item] | None = None
        for old in baseline:
            right = scaffold(old.text, lh7=old.lh7)
            if len(right) < minimum:
                continue
            length_ratio = min(len(left), len(right)) / max(len(left), len(right))
            if length_ratio < 0.72:
                continue
            dice_score = dice(left, right, 3)
            sequence_score = difflib.SequenceMatcher(None, left, right, autojunk=False).ratio()
            if role == "main":
                threshold_dice, threshold_sequence = ((0.78, 0.90) if max(len(left), len(right)) <= 23 else (0.70, 0.84))
            else:
                threshold_dice, threshold_sequence = 0.82, 0.92
            if dice_score >= threshold_dice and sequence_score >= threshold_sequence:
                score = (dice_score, sequence_score, old)
                if best is None or score[:2] > best[:2]:
                    best = score
        if best is not None:
            add_pair_diag(
                diagnostics,
                "warning",
                "W_BASELINE_NEAR_MAIN" if role == "main" else "W_BASELINE_NEAR_REPLY",
                "主评论与历史成品骨架高度相似" if role == "main" else "回复与历史成品骨架高度相似",
                item,
                best[2],
                metrics={"dice": round(best[0], 3), "sequence": round(best[1], 3)},
            )


def audit_baseline_openings(current: list[Item], baseline: list[Item], diagnostics: list[dict]) -> None:
    if not current or not baseline:
        return
    old_prefixes: dict[str, list[Item]] = defaultdict(list)
    new_prefixes: dict[str, list[Item]] = defaultdict(list)
    for item in baseline:
        prefix = scaffold(item.text, lh7=item.lh7)[:6]
        if len(prefix) >= 4:
            old_prefixes[prefix].append(item)
    for item in current:
        prefix = scaffold(item.text, lh7=item.lh7)[:6]
        if len(prefix) >= 4:
            new_prefixes[prefix].append(item)
    for prefix, new_matches in new_prefixes.items():
        old_matches = old_prefixes.get(prefix, [])
        section_ids = {(item.file, item.section) for item in old_matches + new_matches}
        if old_matches and len(section_ids) >= 3 and len(old_matches) + len(new_matches) >= 3:
            diagnostics.append(
                {
                    "severity": "warning",
                    "code": "W_BASELINE_OPENING",
                    "message": f"去产品名后前6字“{prefix}”与历史成品重复过密",
                    "locations": [loc(item) for item in new_matches + old_matches[:2]],
                    "metrics": {"new": len(new_matches), "historical": len(old_matches)},
                }
            )


def audit_openings_and_patterns(sections: list[Section], mains: list[Item], diagnostics: list[dict]) -> None:
    prefix_map: dict[str, list[Item]] = defaultdict(list)
    pattern_map: dict[str, list[Item]] = defaultdict(list)
    for item in mains:
        value = scaffold(item.text, lh7=item.lh7)
        prefix = value[:6]
        if len(prefix) >= 4:
            prefix_map[prefix].append(item)
        for pattern_id, pattern in FIXED_PATTERNS.items():
            if pattern.search(item.text):
                pattern_map[pattern_id].append(item)
        for phrase in BANNED:
            if phrase in item.text:
                diagnostics.append(diag("error", "E_BANNED_STYLE", f"主评论包含总结腔：{phrase}", item.file, item.line, item.section, item.group))

    for prefix, matches in prefix_map.items():
        section_ids = {(item.file, item.section) for item in matches}
        if len(section_ids) >= 3 and len(matches) >= 3:
            result = {"severity": "warning", "code": "W_SAME_OPENING", "message": f"去产品名后前6字“{prefix}”跨多个链接重复", "locations": [loc(item) for item in matches], "metrics": {"count": len(matches), "sections": len(section_ids)}}
            diagnostics.append(result)

    for section in sections:
        local_prefixes: dict[str, list[Item]] = defaultdict(list)
        artificial = []
        for group in section.groups:
            item = group.main
            prefix = scaffold(item.text, lh7=item.lh7)[:6]
            if len(prefix) >= 4:
                local_prefixes[prefix].append(item)
            artificial.extend(pattern_id for pattern_id in ARTIFICIAL_JOKE_IDS if FIXED_PATTERNS[pattern_id].search(item.text))
        for prefix, matches in local_prefixes.items():
            if len(matches) >= 2:
                add_pair_diag(diagnostics, "warning", "W_SAME_OPENING_LOCAL", f"同一链接两条主评以“{prefix}”开头", matches[0], matches[1])
        if len(artificial) > 1:
            diagnostics.append(diag("error", "E_ARTIFICIAL_JOKE_LOCAL", "同一链接使用了超过一次人工造梗结构", section.file, section.line, section.number, metrics={"patterns": artificial}))

    for pattern_id, matches in pattern_map.items():
        section_ids = {(item.file, item.section) for item in matches}
        if len(section_ids) >= 3 and len(matches) >= 3:
            diagnostics.append({"severity": "warning", "code": "W_FIXED_PATTERN", "message": f"固定句型 {pattern_id} 跨多个链接重复", "locations": [loc(item) for item in matches], "metrics": {"count": len(matches)}})


def section_platform(section: Section) -> str:
    source = f"{section.url} {section.file}".lower()
    if "xiaohongshu" in source or "xhs" in source:
        return "xhs"
    if "douyin" in source or "iesdouyin" in source:
        return "douyin"
    if "bilibili" in source or "b23.tv" in source:
        return "bilibili"
    if "weibo" in source:
        return "weibo"
    return "unknown"


def feature_categories(text: str) -> set[str]:
    return {name for name, pattern in FEATURE_PATTERNS.items() if pattern.search(text)}


def group_copy(group: Group) -> str:
    return clean_raw(" ".join(item.text for item in [group.main, *group.replies]))


def lh6_string_list(value: Any) -> list[str] | None:
    """Validate an LH6 list without silently discarding blank elements."""
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        return None
    return [item.strip() for item in value]


def lh6_has_triple_enum(text: str) -> bool:
    """Detect a three-item list or an explicit three-step retelling in a main."""
    value = clean_raw(text)
    if (
        LH6_ENUM_LIST_RE.search(value)
        or LH6_ENUM_CONJ_DUNHAO_RE.search(value)
        or LH6_THREE_STEP_RE.search(value)
    ):
        return True
    for match in LH6_ENUM_CONJ_COMMA_RE.finditer(value):
        first = match.group("first").strip()
        second = match.group("second").strip()
        third = match.group("third").strip()
        if LH6_ENUM_COMMA_CONTEXT_RE.search(first):
            continue
        if first.endswith(("了", "着", "过")):
            continue
        action_without_modifier = LH6_ENUM_COMMA_ACTION_MODIFIER_RE.sub("", first)
        if any(
            first != ending
            and first.endswith(ending)
            and action_without_modifier != ending
            for ending in LH6_ENUM_COMMA_CLAUSE_ENDINGS
        ):
            continue
        if LH6_ENUM_COMMA_NEW_CLAUSE_RE.search(second):
            continue
        if LH6_ENUM_COMMA_THIRD_CLAUSE_RE.search(third):
            continue
        return True
    return False


def lh6_is_closed_copy(text: str) -> bool:
    """Detect a three-clause mini-essay that closes with an interpretive flourish."""
    clauses = [part.strip() for part in re.split(r"[，,；;。！？!?：:]", clean_raw(text)) if part.strip()]
    return len(clauses) >= 3 and bool(LH6_CLOSED_SUMMARY_RE.search(clauses[-1]))


def lh6_has_linked_operation_result(allocation: dict[str, Any], group_context: dict[str, Any]) -> bool:
    """Return true only for a recorded F2/F3 operation-to-result evidence chain."""
    m_level = context_level(allocation, "model_status", M_RANK)
    f_level = context_level(allocation, "feature_use", F_RANK)
    p_level = context_level(allocation, "fact_status", P_RANK)
    claim_mode = str(group_context.get("claim_mode", "")).strip()
    required_f = "F3" if claim_mode == "comparative" else "F2"
    if (
        not m_level
        or M_RANK[m_level] < M_RANK["M2"]
        or not f_level
        or F_RANK[f_level] < F_RANK[required_f]
        or not p_level
        or P_RANK[p_level] < P_RANK["P1"]
    ):
        return False
    if claim_mode not in {"causal", "comparative"}:
        return False
    claim_id = str(group_context.get("claim_id", "")).strip()
    feature_use = allocation.get("feature_use", {})
    fact_status = allocation.get("fact_status", {})
    feature_claims = string_list(feature_use.get("claim_ids", [])) if isinstance(feature_use, dict) else None
    verified_claims = (
        string_list(fact_status.get("verified_claim_ids", [])) if isinstance(fact_status, dict) else None
    )
    if (
        not claim_id
        or feature_claims is None
        or verified_claims is None
        or claim_id not in feature_claims
        or claim_id not in verified_claims
    ):
        return False
    source_values = string_list(group_context.get("evidence_sources", []))
    if source_values is None:
        return False
    parsed, invalid = parse_evidence_sources({value.lower() for value in source_values})
    if invalid:
        return False
    operation_anchors = set().union(
        *(parsed.get(kind, set()) for kind in ("operation", "setting", "control", "ui", "author_demo"))
    )
    result_anchors = set().union(*(parsed.get(kind, set()) for kind in ("result", "output", "frame")))
    linked_anchors = operation_anchors & result_anchors
    if claim_mode == "comparative":
        comparison_anchors = parsed.get("same_condition", set()) | parsed.get("comparison", set())
        return bool(linked_anchors & comparison_anchors)
    return bool(linked_anchors)


def lh6_seed_chain_layers(main_text: str, group_context: dict[str, Any]) -> set[str]:
    """Infer only high-signal main-comment seed layers for overload detection."""
    value = clean_raw(main_text)
    layers: set[str] = set()
    seed_layers = group_context.get("seed_layers")
    if isinstance(seed_layers, dict):
        declared = string_list(seed_layers.get("main", []))
        if declared is not None:
            layers.update(item for item in declared if item in LH6_SEED_LAYERS)

    usage_condition = str(group_context.get("usage_condition", "")).strip()
    user_benefit = str(group_context.get("user_benefit", "")).strip()
    boundary = str(group_context.get("boundary", "")).strip()
    if usage_condition and phrase_in_text(value, usage_condition):
        layers.add("need")
    elif find_product_match(value) and CONDITIONAL_RE.search(value):
        layers.add("need")
    if QUESTION_RE.search(value):
        layers.add("question")
    if find_product_match(value):
        layers.add("product")
    if feature_categories(value):
        layers.add("feature")
    if (user_benefit and phrase_in_text(value, user_benefit)) or BENEFIT_PROXY_RE.search(value):
        layers.add("benefit")
    if (boundary and phrase_in_text(value, boundary)) or BOUNDARY_LANGUAGE_RE.search(value):
        layers.add("boundary")
    return layers


def audit_lh6_contract(
    sections: list[Section],
    resolved_contexts: dict[tuple[str, str], dict[str, Any]],
    diagnostics: list[dict],
    *, lh8: bool = False, lh12: bool = False,
) -> None:
    """Apply the LH6 state and copy contract retained by LH7 to current drafts."""
    mains: list[Item] = []
    for section in sections:
        context = resolved_contexts.get((str(Path(section.file).resolve()), section.number))
        raw_groups = context.get("groups", []) if isinstance(context, dict) else []
        group_contexts: dict[int, dict[str, Any]] = {}
        if isinstance(raw_groups, list):
            for candidate in raw_groups:
                if not isinstance(candidate, dict):
                    continue
                try:
                    number = int(candidate.get("group"))
                except (TypeError, ValueError):
                    continue
                if number in ({1, 2, 3, 4} if lh12 else {1, 2, 3}) and number not in group_contexts:
                    group_contexts[number] = candidate

        for group in section.groups:
            mains.append(group.main)
            group_context = group_contexts.get(group.main.group)

            if group_context is not None:
                schema_issues: list[str] = []
                anchors = lh6_string_list(group_context.get("main_anchor_ids"))
                if anchors is None or len(anchors) != 1:
                    schema_issues.append("main_anchor_ids")

                moves = lh6_string_list(group_context.get("main_moves"))
                if (
                    moves is None
                    or not 1 <= len(moves) <= 2
                    or len(set(moves)) != len(moves)
                    or any(move not in LH6_MAIN_MOVES for move in moves)
                ):
                    schema_issues.append("main_moves")

                seed_layers = group_context.get("seed_layers")
                main_layers: list[str] | None = None
                reply_layers: list[str] | None = None
                if not isinstance(seed_layers, dict) or not {"main", "replies"}.issubset(seed_layers):
                    schema_issues.append("seed_layers")
                else:
                    main_layers = lh6_string_list(seed_layers.get("main"))
                    reply_layers = lh6_string_list(seed_layers.get("replies"))
                    if (
                        main_layers is None
                        or len(main_layers) > 2
                        or len(set(main_layers)) != len(main_layers)
                        or any(layer not in LH6_SEED_LAYERS for layer in main_layers)
                    ):
                        schema_issues.append("seed_layers.main")
                    if (
                        reply_layers is None
                        or len(reply_layers) > 5
                        or len(set(reply_layers)) != len(reply_layers)
                        or any(layer not in LH6_SEED_LAYERS for layer in reply_layers)
                    ):
                        schema_issues.append("seed_layers.replies")

                meme_value = group_context.get("light_meme_anchor")
                anchor = anchors[0] if anchors and len(anchors) == 1 else ""
                if not isinstance(meme_value, str):
                    schema_issues.append("light_meme_anchor")
                    meme_anchor = ""
                else:
                    meme_anchor = meme_value.strip()
                    if meme_anchor and meme_anchor != anchor:
                        schema_issues.append("light_meme_anchor")
                if moves is not None and "joke" in moves and (not anchor or meme_anchor != anchor):
                    schema_issues.append("light_meme_anchor_for_joke")

                if schema_issues:
                    diagnostics.append(
                        diag(
                            "error",
                            "E_LH6_GROUP_SCHEMA",
                            "LH6 评论组缺少合法的单锚点、表达动作、种草层或轻梗锚点",
                            group.main.file,
                            group.main.line,
                            group.main.section,
                            group.main.group,
                            metrics={"fields": sorted(set(schema_issues))},
                        )
                    )

            if lh6_has_triple_enum(group.main.text):
                diagnostics.append(
                    diag(
                        "error",
                        "E_MAIN_TRIPLE_ENUM",
                        "主评论连续枚举了三个对象或复述了三步画面，请只保留一个锚点",
                        group.main.file,
                        group.main.line,
                        group.main.section,
                        group.main.group,
                    )
                )

            closed_exception = bool(
                context
                and group_context
                and lh6_has_linked_operation_result(context, group_context)
            )
            if lh6_is_closed_copy(group.main.text) and not closed_exception:
                diagnostics.append(
                    diag(
                        "warning",
                        "W_CLOSED_COPY",
                        "主评论形成了三段以上分句加总结升华的小作文闭环",
                        group.main.file,
                        group.main.line,
                        group.main.section,
                        group.main.group,
                    )
                )

            if group_context is not None and not (lh8 and group_context.get("claim_mode") == "personal_need"):
                overload_layers = lh6_seed_chain_layers(lh7_fact_text(group.main.text) if group.main.lh7 else group.main.text, group_context)
                if len(overload_layers) >= 4:
                    diagnostics.append(
                        diag(
                            "error",
                            "E_SEED_CHAIN_OVERLOAD",
                            "主评论同时承担了四层以上种草信息，请把卖点、收益或边界拆到楼中楼",
                            group.main.file,
                            group.main.line,
                            group.main.section,
                            group.main.group,
                            metrics={"layers": sorted(overload_layers)},
                        )
                    )

            for item in [group.main, *group.replies]:
                match = LH6_INTERNAL_AUDIT_RE.search(item.text)
                if match:
                    diagnostics.append(
                        diag(
                            "error",
                            "E_INTERNAL_AUDIT_VOICE",
                            "评论出现内部取证或审稿口吻，请改成普通用户会说的话",
                            item.file,
                            item.line,
                            item.section,
                            item.group,
                            metrics={"matched": match.group(0)},
                        )
                    )

    formula_indices = [index for index, item in enumerate(mains) if LH6_FORMULA_RE.search(lh7_fact_text(item.text) if item.lh7 else item.text)]
    for formula_no, index in enumerate(formula_indices):
        recent = [candidate for candidate in formula_indices[: formula_no + 1] if index - candidate < 30]
        if len(recent) < 3:
            continue
        item = mains[index]
        diagnostics.append(
            diag(
                "error",
                "E_SEED_FORMULA_REPEAT",
                "滚动30条主评论内第三次出现“如果/要是常拍＋产品＋收益”同骨架",
                item.file,
                item.line,
                item.section,
                item.group,
                metrics={"matches_in_window": len(recent), "window_start": max(0, index - 29), "window_end": index},
            )
        )


def extract_content_id(url: str) -> str:
    match = CONTENT_ID_RE.search(str(url or ""))
    return match.group(1) if match else ""


def extract_models(text: str, *, lh7: bool = False) -> set[str]:
    if lh7:
        return {lh7_model_for_label(match.group(0)) for match in lh7_product_matches(text)} - {"unknown", "unsupported"}
    return {model for model, pattern in MODEL_PATTERNS if pattern.search(text)}


def model_has_nearby_boundary(text: str, model: str, *, lh7: bool = False) -> bool:
    pattern = next((pattern for candidate, pattern in MODEL_PATTERNS if candidate == model), None)
    if lh7:
        matches = [match for match in lh7_product_matches(text) if lh7_model_for_label(match.group(0)) == model]
    elif pattern is None:
        return False
    else:
        matches = list(pattern.finditer(text))
    for match in matches:
        before = text[max(0, match.start() - 24) : match.start()]
        after = text[match.end() : match.end() + 24]
        if CONTRAST_BOUNDARY_TERM_RE.search(before) or CONTRAST_BOUNDARY_TERM_RE.search(after):
            return True
    return False


def normalize_model(value: Any) -> str:
    raw = re.sub(r"[^a-z0-9]", "", str(value or "").lower())
    aliases = {
        "pocket1": "pocket_1",
        "osmopocket1": "pocket_1",
        "pocket2": "pocket_2",
        "osmopocket2": "pocket_2",
        "pocket4p": "pocket_4p",
        "osmopocket4p": "pocket_4p",
        "op4p": "pocket_4p",
        "4p": "pocket_4p",
        "pocket4": "pocket_4",
        "osmopocket4": "pocket_4",
        "op4": "pocket_4",
        "4": "pocket_4",
        "pocket3": "pocket_3",
        "osmopocket3": "pocket_3",
        "op3": "pocket_3",
        "3": "pocket_3",
        "unknown": "unknown",
        "": "unknown",
    }
    return aliases.get(raw, str(value or "unknown").strip().lower())


def context_level(container: dict[str, Any], key: str, valid: dict[str, int]) -> str:
    value = container.get(key, {})
    if isinstance(value, dict):
        level = str(value.get("level", "")).upper()
    else:
        level = str(value or "").upper()
    return level if level in valid else ""


def normalized_contains(text: str, terms: list[Any]) -> bool:
    normalized = re.sub(r"\s+", "", clean_raw(text)).lower()
    return any(re.sub(r"\s+", "", str(term)).lower() in normalized for term in terms if str(term).strip())


def phrase_in_text(text: str, phrase: str) -> bool:
    normalized_text = keep_word_chars(clean_raw(text)).lower()
    normalized_phrase = keep_word_chars(clean_raw(phrase)).lower()
    return bool(normalized_phrase and normalized_phrase in normalized_text)


def match_is_negated(text: str, match: re.Match[str]) -> bool:
    prefix = text[max(0, match.start() - 12) : match.start()]
    if re.search(r"(?:不是|并非|不算|不能算|不能说|不要说|别说|别写成|不要写成)\s*$", prefix):
        return True
    return bool(FACT_NEGATION_RE.search(match.group(0)))


def author_attribution_binds_assertion(text: str, match: re.Match[str]) -> bool:
    """Require an M1 author cue in the same clause as the model assertion."""
    clause_start = max(
        text.rfind(mark, 0, match.start()) for mark in ("。", "！", "？", "；", ";", "\n")
    ) + 1
    clause = text[clause_start : match.end()]
    return bool(AUTHOR_ATTRIBUTION_RE.search(clause))


def string_list(value: Any) -> list[str] | None:
    """Return a normalized string list, or None when the JSON type is invalid."""
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        return None
    return [item.strip() for item in value if item.strip()]


def url_platform(value: Any) -> str:
    """Identify a supported social host without using filenames as a fallback."""
    try:
        hostname = (urlsplit(str(value or "").strip()).hostname or "").lower()
    except ValueError:
        return "unknown"
    if hostname == "xiaohongshu.com" or hostname.endswith(".xiaohongshu.com") or hostname == "xhslink.com" or hostname.endswith(".xhslink.com"):
        return "xhs"
    if hostname == "douyin.com" or hostname.endswith(".douyin.com") or hostname == "iesdouyin.com" or hostname.endswith(".iesdouyin.com"):
        return "douyin"
    if hostname == "bilibili.com" or hostname.endswith(".bilibili.com") or hostname == "b23.tv" or hostname.endswith(".b23.tv"):
        return "bilibili"
    if hostname == "weibo.com" or hostname.endswith(".weibo.com") or hostname == "weibo.cn" or hostname.endswith(".weibo.cn"):
        return "weibo"
    return "unknown"


def normalized_source_url(value: Any) -> str:
    """Compare official sources by host and path, ignoring query/fragment/slash."""
    try:
        parts = urlsplit(str(value).strip())
    except ValueError:
        return ""
    if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
        return ""
    path = re.sub(r"/+", "/", parts.path or "/").rstrip("/") or "/"
    return f"{parts.hostname.lower()}{path.lower()}"


def canonical_post_url(value: Any) -> str:
    """Return a credential-free host/path identity for a social post URL."""
    raw = str(value or "").strip()
    if not raw:
        return ""
    try:
        parts = urlsplit(raw)
    except ValueError:
        return ""
    if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
        return ""
    path = re.sub(r"/+", "/", parts.path or "/").rstrip("/") or "/"
    return f"https://{parts.hostname.lower()}{path}"


def parse_evidence_sources(values: set[str]) -> tuple[dict[str, set[str]], list[str]]:
    """Parse `kind:anchor:detail` evidence records used by F2/F3 claims."""
    parsed: dict[str, set[str]] = defaultdict(set)
    invalid: list[str] = []
    for value in values:
        match = EVIDENCE_SOURCE_RE.match(value)
        if not match or not match.group(3).strip():
            invalid.append(value)
            continue
        parsed[match.group(1).lower()].add(match.group(2).lower())
    return parsed, invalid


def resolve_state_draft_path(value: Any, state_path: Path) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = state_path.parent / path
    return str(path.resolve())


def audit_seed_semantics(
    sections: list[Section],
    contexts: dict[str, list[dict[str, Any]]],
    state: dict[str, Any],
    registry: dict[str, Any],
    diagnostics: list[dict],
    policy: str,
    *, personal_need_groups: set[tuple[str, str, int]] | None = None,
    observed_s0_groups: set[tuple[str, str, int]] | None = None,
    diversity_reviewed_ids: set[str] | None = None,
) -> dict[str, Any]:
    """Audit LH5/LH6/LH7/LH8/LH9/LH10/LH11/LH12 evidence contracts without pretending regex can assign S grades.

    The state file is the explicit semantic review contract. Text checks only
    verify that the registered claim and its required boundaries actually appear
    in the corresponding comment group.
    """
    start_index = len(diagnostics)
    claims = registry.get("claims", {}) if isinstance(registry, dict) else {}
    expected_registry_version = str(registry.get("registry_version", "")) if registry else ""
    sections_checked = 0
    groups_checked = 0
    strong_sections = 0
    missing_context_sections = 0
    resolved_contexts: dict[tuple[str, str], dict[str, Any]] = {}

    if not state:
        add_seed_diag(
            diagnostics,
            policy,
            "SEED_STATE_INVALID",
            "--state 文件为空或缺少 LH5/LH6/LH7/LH8/LH9/LH10/LH11/LH12 顶层结构",
            hard=True,
        )
        return {
            "status": "invalid_state",
            "sections_checked": 0,
            "groups_checked": 0,
            "strong_seed_sections": 0,
            "missing_context_sections": len(sections),
            "findings_by_code": {},
        }

    rule_version = str(state.get("rule_version", ""))
    lh7 = rule_version in LH7_PLUS_RULE_VERSIONS
    lh8 = rule_version in LH8_PLUS_RULE_VERSIONS
    lh10 = rule_version in LH10_PLUS_RULE_VERSIONS
    lh11 = rule_version in LH11_PLUS_RULE_VERSIONS
    lh12 = rule_version == LH12_RULE_VERSION
    allowed_group_numbers = {1, 2, 3, 4} if lh12 else {1, 2, 3}
    valid_context_models = LH7_CONTEXT_MODELS if lh7 else VALID_MODELS
    shot_mapping_pattern = LH7_SHOT_MAPPING_EVIDENCE_RE if lh7 else SHOT_MAPPING_EVIDENCE_RE
    if rule_version not in SUPPORTED_RULE_VERSIONS:
        add_seed_diag(
            diagnostics,
            policy,
            "SEED_RULE_VERSION",
            "state.rule_version 必须为受支持的 LH5、LH6、LH7、LH8、LH9、LH10、LH11 或 LH12 版本",
            file=state.get("output_path") or None,
            metrics={"actual": rule_version, "supported": sorted(SUPPORTED_RULE_VERSIONS)},
        )
    if expected_registry_version and str(state.get("claim_registry_version", "")) != expected_registry_version:
        add_seed_diag(
            diagnostics,
            policy,
            "CLAIM_REGISTRY_VERSION",
            "state 与卖点注册表版本不一致",
            metrics={
                "state": state.get("claim_registry_version", ""),
                "registry": expected_registry_version,
            },
        )

    semantic_policy = state.get("semantic_policy")
    required_semantic_policy = {
        "evidence_source_format": "kind:shared_anchor:detail",
        "shot_mapping_format": "shot:anchor:model:source",
        "user_benefit_must_quote_copy": True,
        "s3_usage_condition_and_boundary_must_quote_copy": True,
        "actual_s_level_required": True,
    }
    if not isinstance(semantic_policy, dict) or any(
        semantic_policy.get(key) != value for key, value in required_semantic_policy.items()
    ):
        add_seed_diag(
            diagnostics,
            policy,
            "SEED_STATE_INCOMPLETE",
            "state.semantic_policy 与 LH5/LH6/LH7/LH8/LH9/LH10/LH11/LH12 检查协议不一致",
            file=state.get("output_path") or None,
            metrics={"required": required_semantic_policy},
        )
    if (
        rule_version in LH6_PLUS_RULE_VERSIONS
        and (
            not isinstance(semantic_policy, dict)
            or semantic_policy.get("lh6_group_schema") != LH6_GROUP_SCHEMA_CONTRACT
        )
    ):
        add_seed_diag(
            diagnostics,
            policy,
            "LH6_GROUP_SCHEMA",
            "LH6 state.semantic_policy.lh6_group_schema 与当前契约不一致",
            file=state.get("output_path") or None,
            hard=True,
            metrics={"required": LH6_GROUP_SCHEMA_CONTRACT},
        )

    if "evidence_stop_ids" not in state:
        add_seed_diag(
            diagnostics,
            policy,
            "SEED_STATE_INCOMPLETE",
            "LH5/LH6/LH7/LH8/LH9/LH10/LH11/LH12 state 缺少 evidence_stop_ids",
            file=state.get("output_path") or None,
        )
    raw_evidence_stop_ids = state.get("evidence_stop_ids", [])
    evidence_stop_values = string_list(raw_evidence_stop_ids)
    if evidence_stop_values is None:
        add_seed_diag(
            diagnostics,
            policy,
            "SEED_STATE_INVALID",
            "state.evidence_stop_ids 必须是数组",
            file=state.get("output_path") or None,
            hard=True,
        )
        evidence_stop_ids: set[str] = set()
    else:
        evidence_stop_ids = set(evidence_stop_values)
    allocation_ids = [
        str(allocation.get("id", "")).strip()
        for candidates in contexts.values()
        for allocation in candidates
        if str(allocation.get("id", "")).strip()
    ]
    orphan_stop_ids = sorted(evidence_stop_ids - set(allocation_ids))
    if orphan_stop_ids:
        add_seed_diag(
            diagnostics,
            policy,
            "EVIDENCE_STOP_ORPHAN",
            "evidence_stop_ids 含未对应任何 allocation 的 ID",
            file=state.get("output_path") or None,
            metrics={"orphan_ids": orphan_stop_ids},
        )
    duplicate_allocation_ids = sorted(
        allocation_id for allocation_id, count in Counter(allocation_ids).items() if count > 1
    )
    if duplicate_allocation_ids:
        add_seed_diag(
            diagnostics,
            policy,
            "SEED_ALLOCATION_ID_DUPLICATE",
            "state 中 allocation.id 重复，无法稳定绑定链接证据",
            file=state.get("output_path") or None,
            hard=True,
            metrics={"duplicate_ids": duplicate_allocation_ids},
        )

    required_section_fields = {
        "id",
        "canonical_url",
        "model_status",
        "watermark_hint",
        "scene_need",
        "feature_use",
        "fact_status",
        "clip_causality_cap",
        "scenario_fit_cap",
        "strong_seed_group",
        "groups",
    }
    section_number_counts = Counter(section.number for section in sections)

    for section in sections:
        candidates = contexts.get(section.number, [])
        if not candidates:
            missing_context_sections += 1
            add_seed_diag(
                diagnostics,
                policy,
                "SEED_CONTEXT_MISSING",
                f"章节 {section.number} 缺少 LH5/LH6/LH7/LH8/LH9/LH10/LH11/LH12 证据映射",
                section,
            )
            continue

        section_path = str(Path(section.file).resolve())
        if len(candidates) == 1 and section_number_counts[section.number] == 1:
            candidate_path = str(candidates[0].get("_resolved_draft_path", ""))
            if candidate_path and candidate_path != section_path:
                missing_context_sections += 1
                add_seed_diag(
                    diagnostics,
                    policy,
                    "SEED_CONTEXT_PATH_MISMATCH",
                    f"章节 {section.number} 的 state.draft_path 指向另一份草稿",
                    section,
                    hard=True,
                    metrics={"state_draft_path": candidate_path, "actual_draft_path": section_path},
                )
                continue
            context = candidates[0]
        else:
            matching = [item for item in candidates if item.get("_resolved_draft_path") == section_path]
            if len(matching) != 1:
                missing_context_sections += 1
                add_seed_diag(
                    diagnostics,
                    policy,
                    "SEED_CONTEXT_AMBIGUOUS",
                    f"章节 {section.number} 在多个草稿中重复，state 必须用 draft_path 唯一定位",
                    section,
                    hard=True,
                    metrics={
                        "candidate_count": len(candidates),
                        "matching_count": len(matching),
                        "draft_path": section_path,
                    },
                )
                continue
            context = matching[0]

        resolved_contexts[(section_path, section.number)] = context
        if rule_version in LH7_PLUS_RULE_VERSIONS:
            audit_lh7_allocation(section, context, diagnostics, lh8=lh8, lh11=lh11, lh12=lh12)

        section_content_id = extract_content_id(section.url)
        allocation_content_id = str(context.get("id", "")).strip()
        state_canonical_url = canonical_post_url(context.get("canonical_url", ""))
        actual_canonical_url = canonical_post_url(section.url)
        actual_platform = url_platform(section.url)
        state_platform = url_platform(context.get("canonical_url", ""))
        if not actual_canonical_url or actual_platform == "unknown":
            missing_context_sections += 1
            add_seed_diag(
                diagnostics,
                policy,
                "SEED_CONTEXT_LINK_INVALID",
                "草稿章节必须使用受支持平台的 HTTP(S) 原帖或已解析规范链接",
                section,
                hard=True,
                metrics={"draft_url": section.url},
            )
            continue
        if not context.get("canonical_url") or not state_canonical_url or state_platform == "unknown":
            missing_context_sections += 1
            short_host = (urlsplit(str(section.url)).hostname or "").lower()
            is_short_link = short_host in {"v.douyin.com", "b23.tv", "xhslink.com", "www.xhslink.com"}
            add_seed_diag(
                diagnostics,
                policy,
                "SEED_CONTEXT_LINK_UNBOUND" if is_short_link else "SEED_CONTEXT_LINK_INVALID",
                (
                    "短链接章节必须用 allocation.canonical_url 绑定解析后的规范原帖"
                    if is_short_link
                    else "allocation.canonical_url 必须填写受支持平台的 HTTP(S) 去参数规范链接"
                ),
                section,
                hard=True,
            )
            continue
        if state_canonical_url != actual_canonical_url or state_platform != actual_platform:
            missing_context_sections += 1
            add_seed_diag(
                diagnostics,
                policy,
                "SEED_CONTEXT_LINK_MISMATCH",
                "allocation.canonical_url 与当前草稿的规范链接或平台不一致",
                section,
                hard=True,
                metrics={
                    "state_url": state_canonical_url,
                    "draft_url": actual_canonical_url,
                    "state_platform": state_platform,
                    "draft_platform": actual_platform,
                },
            )
            continue
        if section_content_id and allocation_content_id != section_content_id:
            missing_context_sections += 1
            add_seed_diag(
                diagnostics,
                policy,
                "SEED_CONTEXT_ID_MISMATCH",
                "allocation.id 与草稿链接中的作品 ID 不一致",
                section,
                hard=True,
                metrics={"state_id": allocation_content_id, "link_id": section_content_id},
            )
            continue
        missing = sorted(required_section_fields - set(context))
        if missing:
            missing_context_sections += 1
            add_seed_diag(
                diagnostics,
                policy,
                "SEED_CONTEXT_INCOMPLETE",
                f"章节 {section.number} 的 LH5/LH6/LH7/LH8/LH9/LH10/LH11/LH12 证据字段不完整",
                section,
                metrics={"missing_fields": missing},
            )
            continue

        model_status = context.get("model_status")
        watermark_hint = context.get("watermark_hint")
        scene_need = context.get("scene_need")
        feature_use = context.get("feature_use")
        fact_status = context.get("fact_status")
        raw_group_contexts = context.get("groups")
        if not all(isinstance(value, dict) for value in [model_status, watermark_hint, scene_need, feature_use, fact_status]) or not isinstance(raw_group_contexts, list):
            missing_context_sections += 1
            add_seed_diag(
                diagnostics,
                policy,
                "SEED_CONTEXT_INVALID",
                f"章节 {section.number} 的 M/N/F/P 或 groups 类型无效",
                section,
            )
            continue

        raw_lists = {
            "model_status.mixed_models": model_status.get("mixed_models", []),
            "model_status.shot_mapping_evidence": model_status.get("shot_mapping_evidence", []),
            "scene_need.tags": scene_need.get("tags", []),
            "feature_use.claim_ids": feature_use.get("claim_ids", []),
            "fact_status.verified_claim_ids": fact_status.get("verified_claim_ids", []),
            "fact_status.source_urls": fact_status.get("source_urls", []),
        }
        invalid_list_fields = sorted(name for name, value in raw_lists.items() if string_list(value) is None)
        if invalid_list_fields:
            missing_context_sections += 1
            add_seed_diag(
                diagnostics,
                policy,
                "SEED_CONTEXT_INVALID",
                f"章节 {section.number} 的数组字段类型无效",
                section,
                metrics={"invalid_fields": invalid_list_fields},
            )
            continue

        m_level = context_level(context, "model_status", M_RANK)
        n_level = context_level(context, "scene_need", N_RANK)
        f_level = context_level(context, "feature_use", F_RANK)
        p_level = context_level(context, "fact_status", P_RANK)
        causal_cap = str(context.get("clip_causality_cap", "")).upper()
        scenario_cap = str(context.get("scenario_fit_cap", "")).upper()
        invalid_levels = {
            "model_status": m_level,
            "scene_need": n_level,
            "feature_use": f_level,
            "fact_status": p_level,
            "clip_causality_cap": causal_cap if causal_cap in S_RANK else "",
            "scenario_fit_cap": scenario_cap if scenario_cap in S_RANK else "",
        }
        if any(not value for value in invalid_levels.values()):
            missing_context_sections += 1
            add_seed_diag(
                diagnostics,
                policy,
                "SEED_CONTEXT_INVALID",
                f"章节 {section.number} 的证据等级或 S 级上限无效",
                section,
                metrics=invalid_levels,
            )
            continue

        derived_scenario_cap = "S3" if N_RANK[n_level] >= 1 and P_RANK[p_level] >= 1 else "S1" if N_RANK[n_level] >= 1 else "S0"
        if M_RANK[m_level] >= 2 and F_RANK[f_level] >= 2 and P_RANK[p_level] >= 1:
            derived_causal_cap = "S3"
        elif M_RANK[m_level] >= 1 or F_RANK[f_level] >= 1:
            derived_causal_cap = "S1"
        else:
            derived_causal_cap = "S0"
        if S_RANK[scenario_cap] > S_RANK[derived_scenario_cap] or S_RANK[causal_cap] > S_RANK[derived_causal_cap]:
            add_seed_diag(
                diagnostics,
                policy,
                "DECLARED_CAP_EXCEEDS_EVIDENCE",
                f"章节 {section.number} 声明的 S 级上限超过 M/N/F/P 可支持范围",
                section,
                metrics={
                    "declared_clip_causality_cap": causal_cap,
                    "derived_clip_causality_cap": derived_causal_cap,
                    "declared_scenario_fit_cap": scenario_cap,
                    "derived_scenario_fit_cap": derived_scenario_cap,
                },
            )

        sections_checked += 1
        confirmed_model = normalize_model(model_status.get("confirmed_model"))
        claimed_model = normalize_model(model_status.get("claimed_model"))
        model_evidence_type = str(model_status.get("evidence_type", "")).strip().lower()
        mixed_models = [
            normalize_model(value)
            for value in (string_list(model_status.get("mixed_models", [])) or [])
            if normalize_model(value) != "unknown"
        ]
        shot_mapping = str(model_status.get("shot_mapping", "not_applicable")).strip().lower()
        shot_mapping_evidence = string_list(model_status.get("shot_mapping_evidence", [])) or []
        valid_shot_mapping_evidence = [
            value for value in shot_mapping_evidence if shot_mapping_pattern.match(value)
        ]
        invalid_shot_mapping_evidence = [
            value for value in shot_mapping_evidence if not shot_mapping_pattern.match(value)
        ]
        shot_models_by_anchor: dict[str, set[str]] = defaultdict(set)
        for value in valid_shot_mapping_evidence:
            match = shot_mapping_pattern.match(value)
            if match:
                shot_models_by_anchor[match.group(1).lower()].add(normalize_model(match.group(2)))
        mixed_is_present = len(set(mixed_models)) > 1 or model_evidence_type in {
            "mixed_unmapped",
            "mixed_devices_unmapped",
            "mixed_mapped",
        }
        mixed_unmapped = mixed_is_present and (shot_mapping != "mapped" or not valid_shot_mapping_evidence)
        scene_tags = set(string_list(scene_need.get("tags", [])) or [])
        feature_claim_ids = set(string_list(feature_use.get("claim_ids", [])) or [])
        verified_claim_ids = set(string_list(fact_status.get("verified_claim_ids", [])) or [])
        source_urls = string_list(fact_status.get("source_urls", [])) or []
        fact_checked_at = str(fact_status.get("checked_at", "")).strip()
        watermark_present = bool(watermark_hint.get("present"))
        watermark_model = normalize_model(watermark_hint.get("model"))
        watermark_used = bool(watermark_hint.get("used_as_evidence"))
        watermark_declared_in_copy = bool(watermark_hint.get("mentioned_in_copy"))
        watermark_actual_in_copy = any(WATERMARK_RE.search(group_copy(group)) for group in section.groups)
        axis_inconsistencies: list[str] = []
        if (n_level == "N0" and scene_tags) or (N_RANK[n_level] >= 1 and not scene_tags):
            axis_inconsistencies.append("scene_need.level/tags")
        if (f_level == "F0" and feature_claim_ids) or (F_RANK[f_level] >= 1 and not feature_claim_ids):
            axis_inconsistencies.append("feature_use.level/claim_ids")
        if feature_claim_ids - set(claims):
            axis_inconsistencies.append("feature_use.unknown_claim_ids")
        if p_level == "P0" and (verified_claim_ids or source_urls):
            axis_inconsistencies.append("fact_status.P0_payload")
        if P_RANK[p_level] >= 1 and (not verified_claim_ids or not source_urls):
            axis_inconsistencies.append("fact_status.verified_claim_ids/source_urls")
        if verified_claim_ids - set(claims):
            axis_inconsistencies.append("fact_status.unknown_claim_ids")
        supplied_source_keys = {
            normalized_source_url(source) for source in source_urls if normalized_source_url(source)
        }
        for verified_claim_id in verified_claim_ids & set(claims):
            verified_claim = claims.get(verified_claim_id, {})
            required_p = str(verified_claim.get("fact_status_required", "P0")).upper()
            expected_source_keys = {
                normalized_source_url(source)
                for source in (string_list(verified_claim.get("official_sources", [])) or [])
                if normalized_source_url(source)
            }
            if P_RANK[p_level] < P_RANK.get(required_p, 99):
                axis_inconsistencies.append(f"fact_status.level<{verified_claim_id}:{required_p}")
            if expected_source_keys and not (expected_source_keys & supplied_source_keys):
                axis_inconsistencies.append(f"fact_status.source_urls:{verified_claim_id}")
        if P_RANK[p_level] >= 1:
            try:
                date.fromisoformat(fact_checked_at)
            except ValueError:
                axis_inconsistencies.append("fact_status.checked_at")
        if axis_inconsistencies:
            add_seed_diag(
                diagnostics,
                policy,
                "EVIDENCE_AXIS_INCONSISTENT",
                "M/N/F/P 轴的等级与明细字段不一致",
                section,
                metrics={"fields": sorted(set(axis_inconsistencies))},
            )
        invalid_models = sorted(
            model
            for model in {confirmed_model, claimed_model, *mixed_models}
            if model not in valid_context_models
        )
        if invalid_models:
            add_seed_diag(
                diagnostics,
                policy,
                "MODEL_STATUS_INVALID",
                "model_status 含未登记型号",
                section,
                metrics={"invalid_models": invalid_models},
            )
        if model_evidence_type not in VALID_MODEL_EVIDENCE_TYPES:
            add_seed_diag(
                diagnostics,
                policy,
                "MODEL_EVIDENCE_TYPE_INVALID",
                    "model_status.evidence_type 不是 LH5/LH6/LH7/LH8/LH9/LH10/LH11/LH12 允许值",
                section,
                metrics={"evidence_type": model_evidence_type},
            )
        if watermark_model not in valid_context_models:
            add_seed_diag(
                diagnostics,
                policy,
                "WATERMARK_STATE_INCONSISTENT",
                "watermark_hint.model 不是已登记型号或 unknown",
                section,
                metrics={"model": watermark_model},
            )
        if not watermark_present and watermark_model != "unknown":
            add_seed_diag(
                diagnostics,
                policy,
                "WATERMARK_STATE_INCONSISTENT",
                "watermark_hint.present=false 时 model 必须为 unknown",
                section,
                metrics={"model": watermark_model},
            )
        if model_evidence_type == "watermark_only" and not watermark_present:
            add_seed_diag(
                diagnostics,
                policy,
                "WATERMARK_STATE_INCONSISTENT",
                "evidence_type=watermark_only 时必须如实记录 watermark_hint.present=true",
                section,
            )
        if mixed_is_present and shot_mapping == "mapped" and not valid_shot_mapping_evidence:
            add_seed_diag(
                diagnostics,
                policy,
                "SHOT_MAPPING_EVIDENCE_INVALID",
                "混拍逐镜映射必须填写 shot:<anchor>:<model>:<source> 明细",
                section,
                metrics={"shot_mapping_evidence": shot_mapping_evidence},
            )
        if invalid_shot_mapping_evidence:
            add_seed_diag(
                diagnostics,
                policy,
                "SHOT_MAPPING_EVIDENCE_INVALID",
                "shot_mapping_evidence 含不符合 shot:<anchor>:<model>:<source> 的条目",
                section,
                metrics={"invalid_entries": invalid_shot_mapping_evidence},
            )
        ambiguous_shot_anchors = sorted(
            anchor for anchor, models in shot_models_by_anchor.items() if len(models) != 1
        )
        if ambiguous_shot_anchors:
            add_seed_diag(
                diagnostics,
                policy,
                "SHOT_MAPPING_AMBIGUOUS",
                "同一 shot anchor 只能映射到一个型号；当前逐镜归属存在歧义",
                section,
                metrics={
                    "anchors": ambiguous_shot_anchors,
                    "models_by_anchor": {
                        anchor: sorted(shot_models_by_anchor[anchor]) for anchor in ambiguous_shot_anchors
                    },
                },
            )
        if (
            (m_level == "M0" and (claimed_model != "unknown" or confirmed_model != "unknown"))
            or (m_level == "M1" and (claimed_model == "unknown" or confirmed_model != "unknown"))
            or (m_level == "M2" and confirmed_model == "unknown")
        ):
            add_seed_diag(
                diagnostics,
                policy,
                "MODEL_STATUS_INCONSISTENT",
                "model_status 等级与 claimed_model/confirmed_model 不一致",
                section,
                metrics={"level": m_level, "claimed_model": claimed_model, "confirmed_model": confirmed_model},
            )
        if m_level == "M0" and model_evidence_type not in {
            "unknown",
            "watermark_only",
            "mixed_unmapped",
            "mixed_devices_unmapped",
        }:
            add_seed_diag(
                diagnostics,
                policy,
                "MODEL_STATUS_INCONSISTENT",
                "M0 不得使用 UI/机身确认类 evidence_type",
                section,
                metrics={"evidence_type": model_evidence_type},
            )
        if m_level == "M1" and model_evidence_type not in {"author_claim", "author_statement"}:
            add_seed_diag(
                diagnostics,
                policy,
                "MODEL_STATUS_INCONSISTENT",
                "M1 必须来自作者声明，evidence_type 应为 author_claim/author_statement",
                section,
                metrics={"evidence_type": model_evidence_type},
            )
        if m_level == "M2" and model_evidence_type not in {
            "body_confirmed",
            "body_ui_confirmed",
            "ui_confirmed",
            "mixed_mapped",
        }:
            add_seed_diag(
                diagnostics,
                policy,
                "MODEL_STATUS_INCONSISTENT",
                "M2 必须来自正文可确认机身、型号标签、UI 或有效逐镜映射",
                section,
                metrics={"evidence_type": model_evidence_type},
            )
        if model_evidence_type == "watermark_only" and m_level != "M0":
            add_seed_diag(
                diagnostics,
                policy,
                "WATERMARK_MODEL_INFLATION",
                "水印不能把 model_status 从 M0 提高到 M1/M2",
                section,
                metrics={"level": m_level},
            )
        if watermark_present and m_level == "M0" and model_evidence_type == "unknown":
            add_seed_diag(
                diagnostics,
                policy,
                "WATERMARK_STATE_INCONSISTENT",
                "M0 且仅记录到水印提示时，evidence_type 必须明确写 watermark_only 或混拍状态",
                section,
            )
        if watermark_declared_in_copy != watermark_actual_in_copy:
            add_seed_diag(
                diagnostics,
                policy,
                "WATERMARK_STATE_INCONSISTENT",
                "watermark_hint.mentioned_in_copy 与评论正文不一致",
                section,
                metrics={
                    "declared": watermark_declared_in_copy,
                    "actual": watermark_actual_in_copy,
                },
            )
        required_evidence_fields = []
        if M_RANK[m_level] >= 1 and not str(model_status.get("evidence", "")).strip():
            required_evidence_fields.append("model_status.evidence")
        if N_RANK[n_level] >= 1 and not str(scene_need.get("evidence", "")).strip():
            required_evidence_fields.append("scene_need.evidence")
        if F_RANK[f_level] >= 1 and not str(feature_use.get("evidence", "")).strip():
            required_evidence_fields.append("feature_use.evidence")
        if required_evidence_fields:
            add_seed_diag(
                diagnostics,
                policy,
                "EVIDENCE_DESCRIPTION_MISSING",
                "提升 M/N/F 等级时必须填写对应证据说明",
                section,
                metrics={"missing_fields": required_evidence_fields},
            )
        declared_strong = context.get("strong_seed_group")
        try:
            strong_group_no = int(declared_strong) if declared_strong is not None else None
        except (TypeError, ValueError):
            strong_group_no = -1
            add_seed_diag(
                diagnostics,
                policy,
                "STRONG_SEED_GROUP_INVALID",
                "strong_seed_group 必须是 1–4 或 null" if lh12 else "strong_seed_group 必须是 1–3 或 null",
                section,
            )
        if strong_group_no is not None and strong_group_no not in allowed_group_numbers:
            add_seed_diag(
                diagnostics,
                policy,
                "STRONG_SEED_GROUP_INVALID",
                "strong_seed_group 必须是 1–4 或 null" if lh12 else "strong_seed_group 必须是 1–3 或 null",
                section,
                metrics={"actual": strong_group_no},
            )

        group_contexts: dict[int, dict[str, Any]] = {}
        for raw_group in raw_group_contexts:
            if not isinstance(raw_group, dict):
                add_seed_diag(diagnostics, policy, "SEED_GROUP_CONTEXT_INVALID", "groups 中存在非对象条目", section)
                continue
            try:
                number = int(raw_group.get("group"))
            except (TypeError, ValueError):
                add_seed_diag(diagnostics, policy, "SEED_GROUP_CONTEXT_INVALID", "评论组 group 必须是 1–4" if lh12 else "评论组 group 必须是 1–3", section)
                continue
            if number not in allowed_group_numbers:
                add_seed_diag(
                    diagnostics,
                    policy,
                    "SEED_GROUP_CONTEXT_INVALID",
                    "评论组 group 必须是 1–4" if lh12 else "评论组 group 必须是 1–3",
                    section,
                    metrics={"actual": number},
                )
                continue
            if number in group_contexts:
                add_seed_diag(
                    diagnostics,
                    policy,
                    "SEED_GROUP_CONTEXT_DUPLICATE",
                    f"评论组 {number} 的证据映射重复",
                    section,
                    hard=True,
                )
                continue
            group_contexts[number] = raw_group

        valid_strong_groups: set[int] = set()
        valid_personal_groups: set[int] = set()
        valid_observed_groups: set[int] = set()
        any_product_mention = any(find_product_match(group_copy(group)) for group in section.groups)

        if watermark_used:
            add_seed_diag(
                diagnostics,
                policy,
                "WATERMARK_AS_SEED",
                "watermark_hint 被标记为种草证据；水印只能作为采集提示",
                section,
            )

        for group in section.groups:
            group_context = group_contexts.get(group.main.group)
            if group_context is None:
                add_seed_diag(
                    diagnostics,
                    policy,
                    "SEED_GROUP_CONTEXT_MISSING",
                    "评论组缺少 claim_mode、claim_id 与 S 级映射",
                    section,
                    group,
                )
                continue

            groups_checked += 1
            text = group_copy(group)
            if rule_version in LH7_PLUS_RULE_VERSIONS:
                text = lh7_fact_text(text)
            mode = str(group_context.get("claim_mode", "")).strip()
            claim_id_value = group_context.get("claim_id", "")
            claim_id = str(claim_id_value).strip() if isinstance(claim_id_value, str) else ""
            target_model = normalize_model(group_context.get("target_model"))
            benefit_basis = str(group_context.get("benefit_basis", "")).strip()
            user_benefit = str(group_context.get("user_benefit", "")).strip()
            usage_condition = str(group_context.get("usage_condition", "")).strip()
            boundary = str(group_context.get("boundary", "")).strip()
            if rule_version in LH7_PLUS_RULE_VERSIONS:
                user_benefit = lh7_fact_text(user_benefit)
                usage_condition = lh7_fact_text(usage_condition)
                boundary = lh7_fact_text(boundary)
            raw_evidence_sources = group_context.get("evidence_sources", [])
            evidence_source_values = string_list(raw_evidence_sources)
            evidence_sources = {value.lower() for value in (evidence_source_values or [])}
            raw_contrast_models = group_context.get("contrast_models", [])
            contrast_model_values = string_list(raw_contrast_models)
            contrast_models = {
                normalize_model(value)
                for value in (contrast_model_values or [])
                if normalize_model(value) != "unknown"
            }
            target_s = str(group_context.get("target_s_level", "")).upper()
            actual_s_value = group_context.get("actual_s_level")
            actual_s_missing = actual_s_value is None or not str(actual_s_value).strip()
            actual_s = target_s if actual_s_missing else str(actual_s_value).upper()
            group_valid = True

            def group_issue(stem: str, message: str, *, hard: bool = False, metrics: dict[str, Any] | None = None) -> None:
                nonlocal group_valid
                group_valid = False
                add_seed_diag(diagnostics, policy, stem, message, section, group, hard=hard, metrics=metrics)

            invalid_group_lists = []
            if evidence_source_values is None:
                invalid_group_lists.append("evidence_sources")
            if contrast_model_values is None:
                invalid_group_lists.append("contrast_models")
            if invalid_group_lists:
                group_issue(
                    "SEED_GROUP_CONTEXT_INVALID",
                    "评论组的数组字段类型无效",
                    metrics={"invalid_fields": invalid_group_lists},
                )
            invalid_group_models = sorted(
                model for model in {target_model, *contrast_models} if model not in valid_context_models
            )
            if invalid_group_models:
                group_issue(
                    "SEED_GROUP_CONTEXT_INVALID",
                    "target_model/contrast_models 含未登记型号",
                    metrics={"invalid_models": invalid_group_models},
                )
            if actual_s_missing:
                group_issue(
                    "ACTUAL_S_LEVEL_MISSING",
                    "LH5/LH6/LH7/LH8/LH9/LH10/LH11/LH12 严格检查要求显式填写 actual_s_level",
                    metrics={"target_s": target_s},
                )

            valid_modes = VALID_CLAIM_MODES | ({"personal_need"} if lh8 else set())
            if mode not in valid_modes or benefit_basis not in VALID_BENEFIT_BASES or target_s not in S_RANK or actual_s not in S_RANK:
                group_issue(
                    "SEED_GROUP_CONTEXT_INVALID",
                    "评论组的 claim_mode、benefit_basis 或 S 级无效",
                    metrics={"claim_mode": mode, "benefit_basis": benefit_basis, "target_s": target_s, "actual_s": actual_s},
                )
                continue
            if S_RANK[actual_s] > S_RANK[target_s]:
                group_issue(
                    "S_LEVEL_STATE_INVALID",
                    "actual_s_level 不得高于 target_s_level",
                    metrics={"target_s": target_s, "actual_s": actual_s},
                )

            high_seed = S_RANK[actual_s] >= 2
            lh10_capabilities, lh10_causes = lh10_group_product_facts(group, group_context, lh11=lh11, lh12=lh12) if lh10 else ([], [])
            lh10_product_assertion = bool(lh10_capabilities or lh10_causes)
            fact_evidence_required = high_seed or lh10_product_assertion
            text_models_for_facts = extract_models(text, lh7=lh7)
            personal_models, personal_context_issues = lh8_personal_context(group_context) if lh8 else (set(), [])
            personal_context_valid = lh8 and group_context.get("personal_context") is not None and not personal_context_issues
            if personal_context_issues:
                group_issue("PERSONAL_CONTEXT_INVALID", "personal_context 必须提供用户材料定位、非空真实片段和合法型号数组", hard=True, metrics={"fields": personal_context_issues})
            if lh8 and lh8_has_personal_history(group.main.text) and not personal_context_valid:
                group_issue("PERSONAL_CONTEXT_MISSING", "主评含明确的本人经历，请提供本组 personal_context 对应的真实用户材料", hard=True)
            if lh8 and rule_version not in LH9_PLUS_RULE_VERSIONS:
                reply_contexts = group_context.get("reply_personal_contexts", {})
                actual_reply_numbers = {str(reply.reply_no) for reply in group.replies}
                if not isinstance(reply_contexts, dict):
                    group_issue("REPLY_PERSONAL_CONTEXT_INVALID", "reply_personal_contexts 必须以字符串回复序号映射各回复作者自己的真实材料", hard=True)
                    reply_contexts = {}
                extra_reply_keys = [key for key in reply_contexts if not isinstance(key, str) or key not in actual_reply_numbers]
                if extra_reply_keys:
                    group_issue("REPLY_PERSONAL_CONTEXT_INVALID", "reply_personal_contexts 的序号必须对应实际交付的回复", hard=True, metrics={"keys": [str(key) for key in extra_reply_keys]})
                for reply in group.replies:
                    reply_context = reply_contexts.get(str(reply.reply_no))
                    reply_models, reply_issues = lh8_personal_context({"personal_context": reply_context})
                    reply_context_present = str(reply.reply_no) in reply_contexts
                    reply_context_valid = isinstance(reply_context, dict) and not reply_issues
                    if reply_context_present and not reply_context_valid:
                        group_issue("REPLY_PERSONAL_CONTEXT_INVALID", "回复个人材料必须有 source_ref、facts 和 models，不能继承主评作者材料", hard=True, metrics={"reply": reply.reply_no, "fields": reply_issues or ["personal_context"]})
                    if lh8_has_personal_history(reply.text):
                        if not reply_context_valid:
                            group_issue("REPLY_PERSONAL_CONTEXT_MISSING", "回复含明确的本人经历，请在 reply_personal_contexts 中提供该回复作者自己的真实材料", hard=True, metrics={"reply": reply.reply_no})
                        else:
                            reply_text_models = lh8_personal_history_models(reply.text)
                            if reply_text_models - reply_models:
                                group_issue("REPLY_PERSONAL_MODEL_UNGROUNDED", "回复的本人型号必须由该回复自己的个人材料支持", hard=True, metrics={"reply": reply.reply_no, "models": sorted(reply_text_models), "personal_models": sorted(reply_models)})
            if lh8 and mode == "personal_need":
                if claim_id_value != "" or benefit_basis not in {"workflow", "visual"} or max(S_RANK[target_s], S_RANK[actual_s]) > 1:
                    group_issue("PERSONAL_NEED_CONTRACT", "personal_need 上限 S1，claim_id 必须为空且 benefit_basis 只能是 workflow 或 visual", hard=True)
                connection = group_context.get("need_connection")
                if not isinstance(connection, str) or not connection.strip():
                    group_issue("PERSONAL_NEED_CONNECTION_MISSING", "personal_need 必须填写 need_connection，说明主锚点如何触发本人的使用需求", hard=True)
            if (lh8 and mode == "personal_need") or (lh10 and mode == "observed"):
                # A question in another speaker's turn cannot turn this reply's
                # factual assertion into a question. Preserve legacy LH8 behavior.
                capability_claims = lh10_capabilities if lh10 else ([claim for item in [group.main, *group.replies] for claim in lh8_personal_hardware_assertions(lh7_fact_text(item.text))]
                                     if rule_version in LH9_PLUS_RULE_VERSIONS else lh8_personal_hardware_assertions(text))
                mode_code = "PERSONAL_NEED" if mode == "personal_need" else "OBSERVED"
                if capability_claims:
                    group_issue(mode_code + "_PRODUCT_ASSERTION", f"{mode} 不能代替硬件功能核验，含产品能力断言时应改用对应的产品证据模式", hard=True, metrics={"claims": capability_claims})
                if lh10:
                    for causal_text in lh10_causes:
                        group_issue(mode_code + "_CURRENT_CAUSALITY", f"{mode} 不能把当前画面结果归因于产品功能", hard=True, metrics={"matched": causal_text})
                    causal_pairs = []
                else:
                    causal_claim = CURRENT_RESULT_CAUSAL_RE.search(text)
                    causal_pairs = [(text, causal_claim)] if causal_claim else []
                for causal_text, causal_claim in causal_pairs:
                    causal_is_product_claim = bool((LH8_HARDWARE_TERM_RE.search(causal_claim.group(0)) or find_product_match(causal_claim.group(0))) and not re.search(r"(?:讲|说|解释|分析)(?:得|的|得很|得挺)?清楚", causal_claim.group(0)))
                    if causal_is_product_claim and not match_is_negated(causal_text, causal_claim):
                        group_issue(mode_code + "_CURRENT_CAUSALITY", f"{mode} 不能把当前画面结果归因于产品功能", hard=True, metrics={"matched": causal_claim.group(0)})
            if lh10_causes and mode not in {"observed", "personal_need", "causal", "comparative"}:
                group_issue("PRODUCT_CAUSALITY_MODE_INVALID", "正文已把当前画面归因于产品，不能以其他模式或低S级绕过因果证据核验", hard=True, metrics={"claim_mode": mode, "claims": lh10_causes})
            if lh8:
                current_assertions = [(item_text, match) for item in [group.main, *group.replies] for item_text in [clean_raw(lh7_fact_text(item.text))] for match in lh8_current_model_assertions(item_text, lh12=lh12)]
            else:
                assertion = (LH7_CURRENT_MODEL_ASSERTION_RE if lh7 else CURRENT_MODEL_ASSERTION_RE).search(text)
                current_assertions = [(text, assertion)] if assertion else []
            for assertion_text, current_model_assertion in current_assertions:
                if match_is_negated(assertion_text, current_model_assertion):
                    continue
                asserted_models = extract_models(current_model_assertion.group(0), lh7=lh7)
                if M_RANK[m_level] < 1:
                    group_issue(
                        "CURRENT_MODEL_BELOW_M2",
                        "正文直接断言当前画面由某型号拍摄，但 M0 没有型号证据",
                        metrics={"actual_m": m_level},
                    )
                elif M_RANK[m_level] == 1 and (
                    mode != "attributed" or not author_attribution_binds_assertion(assertion_text, current_model_assertion)
                ):
                    group_issue(
                        "CURRENT_MODEL_BELOW_M2",
                        "M1 只能明确转述作者的型号声明，不能写成自行确认",
                        metrics={"actual_m": m_level, "claim_mode": mode},
                    )
                elif M_RANK[m_level] >= 2 and (
                    confirmed_model == "unknown" or confirmed_model not in asserted_models
                ):
                    group_issue(
                        "MODEL_FEATURE_MISMATCH",
                        "正文断言的当前拍摄型号与 model_status.confirmed_model 不一致",
                        hard=True,
                        metrics={
                            "confirmed_model": confirmed_model,
                            "asserted_models": sorted(asserted_models),
                        },
                    )
                if M_RANK[m_level] == 1 and claimed_model not in asserted_models:
                    group_issue(
                        "MODEL_FEATURE_MISMATCH",
                        "正文转述的作者型号与 model_status.claimed_model 不一致",
                        hard=True,
                        metrics={
                            "claimed_model": claimed_model,
                            "asserted_models": sorted(asserted_models),
                        },
                    )
            if POCKET4_FALSE_60MM_RE.search(text):
                group_issue(
                    "MODEL_FEATURE_MISMATCH",
                    "Pocket 4 被错误写成具备 60 mm 实体中焦；该卖点仅属于 4P",
                    hard=True,
                )
            optical_2x_match = OPTICAL_2X_RE.search(text)
            if (
                "pocket_4" in text_models_for_facts
                and optical_2x_match
                and not match_is_negated(text, optical_2x_match)
            ):
                group_issue(
                    "DIGITAL_ZOOM_WRITTEN_AS_OPTICAL",
                    "Pocket 4 的 2 倍无损变焦被写成光学变焦",
                    hard=True,
                )
            seen_forbidden_patterns: set[tuple[str, str]] = set()
            known_false_assertions = registry.get("known_false_assertions", [])
            fact_context_models = set(text_models_for_facts)
            if target_model != "unknown":
                fact_context_models.add(target_model)
            if M_RANK[m_level] >= 2 and confirmed_model != "unknown":
                fact_context_models.add(confirmed_model)
            if isinstance(known_false_assertions, list):
                for assertion in known_false_assertions:
                    if not isinstance(assertion, dict):
                        continue
                    assertion_models = {
                        normalize_model(value)
                        for value in (string_list(assertion.get("models", [])) or [])
                    }
                    if not (fact_context_models & assertion_models):
                        continue
                    pattern = assertion.get("pattern")
                    if not isinstance(pattern, str):
                        continue
                    try:
                        false_match = re.search(pattern, text, re.IGNORECASE)
                    except re.error:
                        continue
                    if not false_match or match_is_negated(text, false_match):
                        continue
                    fingerprint = (str(assertion.get("id", "known_false")), false_match.group(0).lower())
                    if fingerprint in seen_forbidden_patterns:
                        continue
                    seen_forbidden_patterns.add(fingerprint)
                    group_issue(
                        "FORBIDDEN_PRODUCT_CLAIM",
                        str(assertion.get("message") or "评论含已登记的错误产品事实"),
                        hard=True,
                        metrics={
                            "assertion_id": assertion.get("id", ""),
                            "matched": false_match.group(0),
                        },
                    )
            for registered_claim_id, registered_claim in claims.items():
                if not isinstance(registered_claim, dict):
                    continue
                registered_models = {
                    normalize_model(value)
                    for value in (string_list(registered_claim.get("models", [])) or [])
                }
                if not (text_models_for_facts & registered_models):
                    continue
                raw_patterns = registered_claim.get("forbidden_text_patterns", [])
                if not isinstance(raw_patterns, list):
                    continue
                for pattern in raw_patterns:
                    try:
                        match = re.search(str(pattern), text, re.IGNORECASE)
                    except re.error:
                        continue
                    if not match or match_is_negated(text, match):
                        continue
                    fingerprint = (str(registered_claim_id), match.group(0).lower())
                    if fingerprint in seen_forbidden_patterns:
                        continue
                    seen_forbidden_patterns.add(fingerprint)
                    group_issue(
                        "FORBIDDEN_PRODUCT_CLAIM",
                        "评论含已登记的明确禁写产品事实，即使降为 S0/S1 也不能放行",
                        hard=True,
                        metrics={"claim_id": registered_claim_id, "matched": match.group(0)},
                    )
            for registered_claim_id, registered_claim in claims.items():
                if registered_claim_id == claim_id or not isinstance(registered_claim, dict):
                    continue
                required_groups = registered_claim.get("required_text_groups", [])
                registered_text_terms = string_list(registered_claim.get("text_terms", []))
                registered_models = {
                    normalize_model(value)
                    for value in (string_list(registered_claim.get("models", [])) or [])
                }
                if (
                    isinstance(required_groups, list)
                    and required_groups
                    and registered_text_terms
                    and normalized_contains(text, registered_text_terms)
                    and fact_context_models & registered_models
                    and all(isinstance(terms, list) and normalized_contains(text, terms) for terms in required_groups)
                    and registered_claim_id not in verified_claim_ids
                ):
                    group_issue(
                        "ADDITIONAL_PRODUCT_FACT_UNVERIFIED",
                        "评论还写入了另一项可明确识别的产品事实，但 state 未记录该 claim 的官方核验",
                        metrics={"claim_id": registered_claim_id},
                    )
            if (
                claim_id == "p4_2x_lossless"
                and optical_2x_match
                and not match_is_negated(text, optical_2x_match)
            ):
                group_issue(
                    "DIGITAL_ZOOM_WRITTEN_AS_OPTICAL",
                    "Pocket 4 的 2 倍无损变焦被写成光学变焦",
                    hard=True,
                    metrics={"claim_id": claim_id},
                )

            if high_seed and (
                watermark_used
                or "watermark" in evidence_sources
                or "水印" in evidence_sources
                or WATERMARK_RE.search(text)
            ):
                group_issue(
                    "WATERMARK_AS_SEED",
                    "S2/S3 使用了水印作为型号、功能或收益依据",
                    metrics={"claim_id": claim_id, "evidence_sources": sorted(evidence_sources)},
                )
            if high_seed and benefit_basis != "product":
                group_issue(
                    "GENERIC_SCENE_AS_PRODUCT_BENEFIT",
                    "visual/workflow 收益不能替 Pocket 获得 S2/S3",
                    metrics={"benefit_basis": benefit_basis, "claim_id": claim_id},
                )
            if high_seed and not user_benefit:
                group_issue("USER_BENEFIT_MISSING", "S2/S3 缺少明确的用户实际收益", metrics={"claim_id": claim_id})
            elif high_seed and not phrase_in_text(text, user_benefit):
                group_issue(
                    "USER_BENEFIT_NOT_IN_COPY",
                    "state.user_benefit 必须引用该评论组中实际出现的收益短语",
                    metrics={"claim_id": claim_id, "user_benefit": user_benefit},
                )
            if fact_evidence_required and not claim_id:
                group_issue("SEED_CLAIM_MISSING", "S2/S3 或 LH10/LH11 正文产品事实断言缺少有效 claim_id", hard=lh10_product_assertion)

            claim = claims.get(claim_id) if claim_id else None
            if claim_id and not isinstance(claim, dict):
                group_issue("SEED_CLAIM_UNKNOWN", f"claim_id 未在卖点注册表中登记：{claim_id}", hard=True)
                claim = None

            claim_text_present = False
            if claim is not None:
                claim_models = string_list(claim.get("models", []))
                allowed_models = {normalize_model(value) for value in (claim_models or [])}
                text_models = extract_models(text, lh7=lh7)
                if claim_models is None or not allowed_models:
                    group_issue(
                        "CLAIM_REGISTRY_INVALID",
                        f"claim {claim_id} 的 models 无效",
                        hard=True,
                    )
                if target_model != "unknown" and target_model not in allowed_models:
                    group_issue(
                        "MODEL_FEATURE_MISMATCH",
                        "目标型号与 claim_id 支持的型号不匹配",
                        hard=True,
                        metrics={"target_model": target_model, "claim_id": claim_id, "allowed_models": sorted(allowed_models)},
                    )
                unsupported_text_models = text_models - allowed_models
                non_target_text_models = (
                    text_models - {target_model} if target_model != "unknown" else set(text_models)
                )
                permitted_contrast = (
                    bool(non_target_text_models)
                    and mode in {"scenario_fit", "comparative"}
                    and non_target_text_models.issubset(contrast_models)
                    and bool(usage_condition)
                    and bool(boundary)
                    and bool(CONDITIONAL_RE.search(text))
                    and bool(BOUNDARY_LANGUAGE_RE.search(text))
                    and all(model_has_nearby_boundary(text, model, lh7=lh7) for model in non_target_text_models)
                )
                if fact_evidence_required and claim.get("scope") == "shared" and (
                    mode == "comparative"
                    or (len(text_models) > 1 and SHARED_CLAIM_MODEL_EDGE_RE.search(text))
                ):
                    group_issue(
                        "SHARED_CLAIM_MODEL_COMPARISON",
                        "共享卖点不能被写成 4P、Pocket 4 或其他代际之间的能力胜负",
                        metrics={"claim_id": claim_id, "text_models": sorted(text_models)},
                    )
                if (unsupported_text_models or non_target_text_models) and not permitted_contrast:
                    group_issue(
                        "MODEL_FEATURE_MISMATCH",
                        "评论正文含 target_model 之外的型号；只有显式 contrast_models 与真实条件/边界才可比较",
                        hard=True,
                        metrics={
                            "text_models": sorted(text_models),
                            "unsupported_models": sorted(unsupported_text_models),
                            "non_target_models": sorted(non_target_text_models),
                            "contrast_models": sorted(contrast_models),
                            "claim_id": claim_id,
                            "allowed_models": sorted(allowed_models),
                        },
                    )
                if contrast_models and not contrast_models.issubset(text_models):
                    group_issue(
                        "CONTRAST_MODEL_NOT_IN_COPY",
                        "contrast_models 中声明的对比型号没有出现在评论正文",
                        metrics={"contrast_models": sorted(contrast_models), "text_models": sorted(text_models)},
                    )
                if fact_evidence_required and target_model == "unknown" and (
                    len(allowed_models) == 1 or mode in {"causal", "comparative"}
                ):
                    group_issue(
                        "TARGET_MODEL_MISSING",
                        "型号专属或当前成片归因的 S2/S3 必须填写 target_model",
                        metrics={"claim_id": claim_id},
                    )
                if fact_evidence_required and text_models and target_model not in text_models:
                    group_issue(
                        "TARGET_PRODUCT_NOT_IN_COPY",
                        "评论组既然点名型号，就必须包含 target_model；其他型号只能作为显式对比",
                        metrics={"claim_id": claim_id, "target_model": target_model, "text_models": sorted(text_models)},
                    )
                if fact_evidence_required and len(allowed_models) == 1 and not text_models:
                    group_issue(
                        "TARGET_PRODUCT_NOT_IN_COPY",
                        "型号专属 S2/S3 必须在评论组正文点明 target_model，不能只写泛 60 mm 等规格",
                        metrics={"claim_id": claim_id, "target_model": target_model},
                    )
                if fact_evidence_required and len(allowed_models) > 1 and not find_product_match(text):
                    group_issue(
                        "TARGET_PRODUCT_NOT_IN_COPY",
                        "共享能力的 S2/S3 也必须在评论组中自然连接 Pocket 产品",
                        metrics={"claim_id": claim_id},
                    )

                if fact_evidence_required:
                    text_terms = string_list(claim.get("text_terms", []))
                    if text_terms is None:
                        group_issue("CLAIM_REGISTRY_INVALID", f"claim {claim_id} 的 text_terms 无效", hard=True)
                        text_terms = []
                    claim_text_present = bool(text_terms and normalized_contains(text, text_terms))
                    if text_terms and not claim_text_present:
                        group_issue(
                            "CLAIM_NOT_IN_COPY",
                            "状态中的卖点没有出现在对应评论组正文",
                            metrics={"claim_id": claim_id, "text_terms": text_terms},
                        )
                    if lh10_product_assertion and text_terms:
                        unmapped_assertions = [assertion for assertion in lh10_capabilities if not normalized_contains(assertion, text_terms)]
                        if unmapped_assertions:
                            group_issue("PRODUCT_ASSERTION_CLAIM_MISMATCH", "逐句产品断言未对应所登记的 claim，不能借另一处卖点词补齐核验", hard=True, metrics={"claim_id": claim_id, "assertions": unmapped_assertions})
                    benefit_required_terms = string_list(claim.get("benefit_required_terms", []))
                    if benefit_required_terms is None:
                        group_issue(
                            "CLAIM_REGISTRY_INVALID",
                            f"claim {claim_id} 的 benefit_required_terms 无效",
                            hard=True,
                        )
                    elif high_seed and benefit_required_terms and not normalized_contains(user_benefit, benefit_required_terms):
                        group_issue(
                            "CLAIM_BENEFIT_MISMATCH",
                            "该精确卖点必须转化为与其差异本身对应的用户收益，不能借用共享能力的收益",
                            metrics={
                                "claim_id": claim_id,
                                "required_any_of": benefit_required_terms,
                                "user_benefit": user_benefit,
                            },
                        )
                    required_p = str(claim.get("fact_status_required", "P0")).upper()
                    if P_RANK[p_level] < P_RANK.get(required_p, 99) or claim_id not in verified_claim_ids:
                        group_issue(
                            "PRODUCT_FACT_UNVERIFIED",
                            "产品事实的 claim_id 未达到注册表要求的 P 级或未列入 verified_claim_ids",
                            hard=lh10_product_assertion,
                            metrics={"claim_id": claim_id, "actual_p": p_level, "required_p": required_p},
                        )
                    official_sources = string_list(claim.get("official_sources", []))
                    expected_sources = {
                        normalized_source_url(source)
                        for source in (official_sources or [])
                        if normalized_source_url(source)
                    }
                    supplied_sources = {
                        normalized_source_url(source)
                        for source in source_urls
                        if normalized_source_url(source)
                    }
                    if official_sources is None or not expected_sources:
                        group_issue(
                            "CLAIM_REGISTRY_INVALID",
                            f"claim {claim_id} 缺少有效 official_sources",
                            hard=True,
                        )
                    elif not (expected_sources & supplied_sources):
                        group_issue(
                            "PRODUCT_FACT_SOURCE_MISSING",
                            "产品事实的来源未匹配该 claim 登记的 DJI 官方页面",
                            hard=lh10_product_assertion,
                            metrics={
                                "claim_id": claim_id,
                                "expected_sources": sorted(expected_sources),
                                "supplied_sources": sorted(supplied_sources),
                            },
                        )
                    if required_p == "P2" and fact_checked_at != date.today().isoformat():
                        group_issue(
                            "PRODUCT_FACT_STALE",
                            "P2 高风险卖点必须在运行当日复核",
                            metrics={"claim_id": claim_id, "checked_at": fact_checked_at, "required": date.today().isoformat()},
                        )

                    required_groups = claim.get("required_text_groups", [])
                    if not isinstance(required_groups, list):
                        group_issue("CLAIM_REGISTRY_INVALID", f"claim {claim_id} 的 required_text_groups 无效", hard=True)
                        required_groups = []
                    for index, terms in enumerate(required_groups):
                        if not isinstance(terms, list):
                            group_issue(
                                "CLAIM_REGISTRY_INVALID",
                                f"claim {claim_id} 的 required_text_groups[{index}] 无效",
                                hard=True,
                            )
                            continue
                        if normalized_contains(text, terms):
                            continue
                        stem = "HIGH_RISK_MODE_CONDITION_MISSING"
                        if claim_id == "p4_2x_lossless" and index == 0:
                            stem = "DIGITAL_ZOOM_BOUNDARY_MISSING"
                        group_issue(
                            stem,
                            "高风险卖点缺少注册表要求的模式或事实边界",
                            metrics={"claim_id": claim_id, "missing_any_of": terms},
                        )

                    forbidden_patterns = claim.get("forbidden_text_patterns", [])
                    if not isinstance(forbidden_patterns, list):
                        group_issue("CLAIM_REGISTRY_INVALID", f"claim {claim_id} 的 forbidden_text_patterns 无效", hard=True)
                        forbidden_patterns = []
                    for pattern in forbidden_patterns:
                        try:
                            forbidden_match = re.search(str(pattern), text, re.IGNORECASE)
                        except re.error:
                            group_issue(
                                "CLAIM_REGISTRY_INVALID",
                                f"claim {claim_id} 含无效 forbidden_text_patterns 正则",
                                hard=True,
                                metrics={"pattern": pattern},
                            )
                            continue
                        fingerprint = (claim_id, forbidden_match.group(0).lower()) if forbidden_match else None
                        if (
                            forbidden_match
                            and not match_is_negated(text, forbidden_match)
                            and fingerprint not in seen_forbidden_patterns
                        ):
                            seen_forbidden_patterns.add(fingerprint)
                            group_issue(
                                "FORBIDDEN_PRODUCT_CLAIM",
                                "评论触发该卖点注册表的明确禁写事实",
                                hard=True,
                                metrics={"claim_id": claim_id, "matched": forbidden_match.group(0)},
                            )

                    more_specific_claim = claim.get("more_specific_claim")
                    if more_specific_claim is not None:
                        if not isinstance(more_specific_claim, dict):
                            group_issue(
                                "CLAIM_REGISTRY_INVALID",
                                f"claim {claim_id} 的 more_specific_claim 无效",
                                hard=True,
                            )
                        else:
                            specific_id = str(more_specific_claim.get("claim_id", "")).strip()
                            trigger_groups = more_specific_claim.get("when_all_text_groups", [])
                            if not isinstance(trigger_groups, list) or any(
                                not isinstance(terms, list) for terms in trigger_groups
                            ):
                                group_issue(
                                    "CLAIM_REGISTRY_INVALID",
                                    f"claim {claim_id} 的 more_specific_claim 触发条件无效",
                                    hard=True,
                                )
                            elif (
                                mode in {"causal", "comparative"}
                                and trigger_groups
                                and all(normalized_contains(text, terms) for terms in trigger_groups)
                                and specific_id
                                and specific_id != claim_id
                            ):
                                group_issue(
                                    "MORE_SPECIFIC_CLAIM_REQUIRED",
                                    "正文展示了更具体的操作，应绑定最具体 claim_id",
                                    metrics={"current_claim_id": claim_id, "required_claim_id": specific_id},
                                )

            workflow_without_product_mechanism = (
                bool(WORKFLOW_VISUAL_RE.search(text)) and not claim_text_present
            ) or (
                bool(WORKFLOW_VISUAL_RE.search(user_benefit))
                and claim_id not in WORKFLOW_BENEFIT_ALLOWED_CLAIMS
            )
            if high_seed and workflow_without_product_mechanism:
                group_issue(
                    "WORKFLOW_ONLY_ABOVE_S1",
                    "构图、剪辑或混拍等工作流价值没有被有效产品机制转换为用户收益",
                    metrics={"claim_id": claim_id, "benefit_basis": benefit_basis},
                )

            if fact_evidence_required:
                if mode == "scenario_fit":
                    current_result_causal = CURRENT_RESULT_CAUSAL_RE.search(text)
                    if current_result_causal and not match_is_negated(text, current_result_causal):
                        group_issue(
                            "SCENARIO_FIT_CURRENT_CAUSALITY",
                            "scenario_fit 只能写未来场景适配，不能把卖点说成当前画面结果的原因",
                            metrics={"claim_id": claim_id, "matched": current_result_causal.group(0)},
                        )
                    if N_RANK[n_level] < 1:
                        group_issue("SCENARIO_NEED_MISSING", "scenario_fit 的链接缺少 N1/N2 场景需求", metrics={"claim_id": claim_id})
                    if not usage_condition or not CONDITIONAL_RE.search(text):
                        group_issue(
                            "SCENARIO_FIT_MISSING_CONDITIONAL",
                            "未直接演示功能时，S2/S3 必须使用明确的场景条件表达",
                            metrics={"claim_id": claim_id},
                        )
                    if claim is not None:
                        allowed_tag_values = string_list(claim.get("scene_need_tags", []))
                        if allowed_tag_values is None:
                            group_issue(
                                "CLAIM_REGISTRY_INVALID",
                                f"claim {claim_id} 的 scene_need_tags 无效",
                                hard=True,
                            )
                            allowed_tag_values = []
                        allowed_tags = set(allowed_tag_values)
                        if allowed_tags and not (scene_tags & allowed_tags):
                            group_issue(
                                "SCENE_CLAIM_MISMATCH",
                                "scene_need 与所选 claim_id 的适用场景不匹配",
                                metrics={"scene_tags": sorted(scene_tags), "claim_tags": sorted(allowed_tags), "claim_id": claim_id},
                            )
                    if S_RANK[actual_s] > S_RANK[scenario_cap]:
                        group_issue(
                            "SCENARIO_FIT_CAP_EXCEEDED",
                            "评论的 S 级超过未来场景适配上限",
                            metrics={"actual_s": actual_s, "scenario_fit_cap": scenario_cap},
                        )
                elif mode in {"causal", "comparative"}:
                    if mixed_unmapped:
                        group_issue(
                            "MIXED_SHOT_MAPPING_MISSING",
                            "混拍内容未逐镜映射，不能把当前画面归因给单一设备卖点",
                            metrics={"claim_id": claim_id},
                        )
                    required_f = "F3" if mode == "comparative" else str((claim or {}).get("causal_min_feature_use", "F2")).upper()
                    if F_RANK[f_level] < F_RANK.get(required_f, 99) or claim_id not in feature_claim_ids:
                        group_issue(
                            "CAUSAL_CLAIM_BELOW_F2" if mode == "causal" else "COMPARATIVE_CLAIM_BELOW_F3",
                            "当前成片因果超过功能使用证据上限",
                            metrics={"claim_id": claim_id, "actual_f": f_level, "required_f": required_f},
                        )
                    parsed_sources, invalid_sources = parse_evidence_sources(evidence_sources)
                    if invalid_sources:
                        group_issue(
                            "FEATURE_EVIDENCE_SOURCE_INVALID",
                            "F2/F3 evidence_sources 必须使用 kind:anchor:detail 格式",
                            metrics={"claim_id": claim_id, "invalid_sources": sorted(invalid_sources)},
                        )
                    operation_anchors = set().union(
                        *(parsed_sources.get(kind, set()) for kind in ("operation", "setting", "control", "ui", "author_demo"))
                    )
                    result_anchors = set().union(
                        *(parsed_sources.get(kind, set()) for kind in ("result", "output", "frame"))
                    )
                    linked_anchors = operation_anchors & result_anchors
                    if not linked_anchors:
                        group_issue(
                            "FEATURE_EVIDENCE_LINK_MISSING",
                            "F2/F3 因果必须用同一 anchor 记录操作或 UI 证据及对应结果证据",
                            metrics={
                                "claim_id": claim_id,
                                "operation_anchors": sorted(operation_anchors),
                                "result_anchors": sorted(result_anchors),
                            },
                        )
                    if mixed_is_present:
                        attribution_model = target_model if target_model != "unknown" else confirmed_model
                        mapped_linked_anchors = {
                            anchor
                            for anchor in linked_anchors
                            if shot_models_by_anchor.get(anchor, set()) == {attribution_model}
                        }
                        if not mapped_linked_anchors:
                            group_issue(
                                "MIXED_SHOT_MAPPING_MISSING",
                                "混拍的逐镜型号映射必须与因果证据共用 anchor，并指向当前 claim 的目标型号",
                                metrics={
                                    "claim_id": claim_id,
                                    "target_model": attribution_model,
                                    "linked_anchors": sorted(linked_anchors),
                                    "shot_mapping_anchors": sorted(shot_models_by_anchor),
                                },
                            )
                    comparison_anchors = parsed_sources.get("same_condition", set()) | parsed_sources.get("comparison", set())
                    if mode == "comparative" and not (comparison_anchors & linked_anchors):
                        group_issue(
                            "COMPARISON_EVIDENCE_MISSING",
                            "comparative 必须用同一 anchor 记录同条件测试或比较证据",
                            metrics={
                                "claim_id": claim_id,
                                "linked_anchors": sorted(linked_anchors),
                                "comparison_anchors": sorted(comparison_anchors),
                            },
                        )
                    if M_RANK[m_level] < 2:
                        group_issue("CURRENT_MODEL_BELOW_M2", "当前成片因果必须有 M2 型号确认", metrics={"actual_m": m_level})
                    if target_model == "unknown":
                        group_issue(
                            "TARGET_MODEL_MISSING",
                            "causal/comparative 必须填写本组归因的 target_model",
                            metrics={"claim_id": claim_id},
                        )
                    elif confirmed_model != "unknown" and target_model != confirmed_model:
                        group_issue(
                            "MODEL_FEATURE_MISMATCH",
                            "causal/comparative 的 target_model 与 confirmed_model 不一致",
                            hard=True,
                            metrics={"target_model": target_model, "confirmed_model": confirmed_model},
                        )
                    causal_text_models = extract_models(text, lh7=lh7)
                    if causal_text_models and target_model not in causal_text_models:
                        group_issue(
                            "MODEL_FEATURE_MISMATCH",
                            "causal/comparative 正文点名的型号不包含 target_model",
                            hard=True,
                            metrics={"target_model": target_model, "text_models": sorted(causal_text_models)},
                        )
                    if claim is not None and confirmed_model not in {"unknown", *{normalize_model(value) for value in claim.get("models", [])}}:
                        group_issue(
                            "MODEL_FEATURE_MISMATCH",
                            "已确认的原帖型号与因果卖点不匹配",
                            hard=True,
                            metrics={"confirmed_model": confirmed_model, "claim_id": claim_id},
                        )
                    if confirmed_model == "unknown":
                        group_issue("CONFIRMED_MODEL_MISSING", "当前成片因果缺少 confirmed_model")
                    if S_RANK[actual_s] > S_RANK[causal_cap]:
                        group_issue(
                            "CLIP_CAUSALITY_CAP_EXCEEDED",
                            "评论的 S 级超过当前成片因果上限",
                            metrics={"actual_s": actual_s, "clip_causality_cap": causal_cap},
                        )
                elif lh10_product_assertion and not high_seed and mode == "attributed":
                    assertion_clauses = [*lh10_capabilities, *lh10_causes]
                    if any(not AUTHOR_ATTRIBUTION_RE.search(clause) for clause in assertion_clauses):
                        group_issue("PRODUCT_ATTRIBUTION_MISSING", "attributed 的每个产品断言须保留作者声明来源，不能只改模式标签", hard=True)
                    if F_RANK[f_level] < F_RANK["F1"] or claim_id not in feature_claim_ids:
                        group_issue("PRODUCT_ATTRIBUTION_UNGROUNDED", "attributed 产品断言须有原帖作者的 F1 以上声明并映射该 claim", hard=True)
                elif mode not in {"observed", "personal_need"} or high_seed:
                    group_issue(
                        "CLAIM_MODE_TOO_WEAK",
                        "S2/S3 必须使用 scenario_fit、causal 或具备 F3 的 comparative",
                        metrics={"claim_mode": mode, "claim_id": claim_id},
                    )

                if actual_s == "S3":
                    if claim is not None and claim.get("scope") != "differentiator":
                        group_issue(
                            "S3_REQUIRES_DIFFERENTIATOR",
                            "共享卖点不能单独支撑 4P/4 的 S3 型号选择",
                            metrics={"claim_id": claim_id, "scope": claim.get("scope")},
                        )
                    if not usage_condition or not CONDITIONAL_RE.search(text):
                        group_issue("S3_USAGE_CONDITION_MISSING", "S3 缺少使用频率或场景条件", metrics={"claim_id": claim_id})
                    elif not phrase_in_text(text, usage_condition):
                        group_issue(
                            "S3_USAGE_CONDITION_NOT_IN_COPY",
                            "state.usage_condition 必须引用该评论组中实际出现的条件短语",
                            metrics={"claim_id": claim_id, "usage_condition": usage_condition},
                        )
                    if not boundary or not BOUNDARY_LANGUAGE_RE.search(text):
                        group_issue("S3_BOUNDARY_MISSING", "S3 缺少真实选择边界", metrics={"claim_id": claim_id})
                    elif not phrase_in_text(text, boundary):
                        group_issue(
                            "S3_BOUNDARY_NOT_IN_COPY",
                            "state.boundary 必须引用该评论组中实际出现的边界短语",
                            metrics={"claim_id": claim_id, "boundary": boundary},
                        )
                    if claim is not None:
                        s3_boundary_terms = string_list(claim.get("s3_boundary_terms", []))
                        if s3_boundary_terms is None:
                            group_issue(
                                "CLAIM_REGISTRY_INVALID",
                                f"claim {claim_id} 的 s3_boundary_terms 无效",
                                hard=True,
                            )
                        elif claim.get("scope") == "differentiator" and (
                            not s3_boundary_terms or not normalized_contains(text, s3_boundary_terms)
                        ):
                            group_issue(
                                "S3_CLAIM_BOUNDARY_MISSING",
                                "S3 的边界与该差异卖点无关，不能只写预算等通用保留项",
                                metrics={"claim_id": claim_id, "required_any_of": s3_boundary_terms or []},
                            )

            if high_seed and group_valid:
                valid_strong_groups.add(group.main.group)
            if lh8 and mode == "personal_need" and group_valid:
                valid_personal_groups.add(group.main.group)
                if personal_need_groups is not None:
                    personal_need_groups.add((group.main.file, group.main.section, group.main.group))
            if lh10 and mode == "observed" and target_s == actual_s == "S0" and group_valid:
                anchors = lh6_string_list(group_context.get("main_anchor_ids"))
                connection = group_context.get("product_connection")
                group_has_error = any(
                    finding["severity"] == "error" and any(
                        location.get("file") == group.main.file and location.get("section") == group.main.section
                        and location.get("group") in {None, group.main.group}
                        for location in finding.get("locations", [])
                    ) for finding in diagnostics
                )
                # This permits content interaction after semantic review, never
                # a product name alone or an unreviewed/invalid group.
                if (claim_id_value == "" and benefit_basis in {"workflow", "visual"}
                        and anchors is not None and len(anchors) == 1
                        and ((isinstance(connection, str) and connection.strip())
                             or (lh11 and lh11_visual_only_group(group, group_context, lh12=lh12)))
                        and str(context.get("id", "")).strip() in (diversity_reviewed_ids or set())
                        and not group_has_error):
                    valid_observed_groups.add(group.main.group)
                    if observed_s0_groups is not None:
                        observed_s0_groups.add((group.main.file, group.main.section, group.main.group))

        allocation_id = str(context.get("id", "")).strip()
        under_target_reason = str(context.get("under_target_reason", "")).strip()
        scene_is_valid = N_RANK[n_level] >= 1 or F_RANK[f_level] >= 2
        if lh8:
            # A useful personal association can remain S1 even when the post
            # has no feature evidence. This never raises the original caps.
            if strong_group_no is not None and strong_group_no not in valid_strong_groups:
                add_seed_diag(diagnostics, policy, "STRONG_SEED_GROUP_INVALID", "strong_seed_group 未指向通过证据门禁的真实 S2/S3", section, metrics={"declared": strong_group_no, "valid_groups": sorted(valid_strong_groups)})
            if (strong_group_no is not None or valid_strong_groups) and not scene_is_valid:
                add_seed_diag(diagnostics, policy, "STRONG_SEED_WITHOUT_NEED", "无有效场景需求或功能演示时不得硬设强种草组", section)
            if valid_strong_groups:
                strong_sections += 1
            valid_content_groups = valid_personal_groups | valid_observed_groups
            if allocation_id in evidence_stop_ids and (scene_is_valid or valid_content_groups):
                add_seed_diag(diagnostics, policy, "EVIDENCE_STOP_CONFLICT", "已有可用需求关联的链接不应仅因缺少强种草而登记 evidence_stop_ids", section)
            elif not scene_is_valid and not valid_content_groups and not (allocation_id in evidence_stop_ids and under_target_reason):
                add_seed_diag(diagnostics, policy, "EVIDENCE_STOP_MISSING", "无有效原帖需求且没有可用 personal_need 或 LH10/LH11 已复核的 observed/S0 时，仍需登记 evidence_stop_ids 并说明依据", section)
        elif scene_is_valid:
            if allocation_id and allocation_id in evidence_stop_ids:
                add_seed_diag(
                    diagnostics,
                    policy,
                    "EVIDENCE_STOP_CONFLICT",
                    "已有有效场景需求或功能演示的链接不应列入 evidence_stop_ids",
                    section,
                    metrics={"id": allocation_id},
                )
            if strong_group_no is None:
                add_seed_diag(
                    diagnostics,
                    policy,
                    "STRONG_SEED_GROUP_UNSET",
                    "有效场景链接必须指定一组 strong_seed_group",
                    section,
                )
            elif strong_group_no not in valid_strong_groups:
                add_seed_diag(
                    diagnostics,
                    policy,
                    "STRONG_SEED_GROUP_INVALID",
                    "strong_seed_group 未指向通过证据门禁的真实 S2/S3",
                    section,
                    metrics={"declared": strong_group_no, "valid_groups": sorted(valid_strong_groups)},
                )
            if not valid_strong_groups:
                add_seed_diag(
                    diagnostics,
                    policy,
                    "STRONG_SEED_MISSING",
                    "有效场景链接没有任何通过证据门禁的产品 S2/S3",
                    section,
                )
            else:
                strong_sections += 1
        elif strong_group_no is not None or valid_strong_groups:
            add_seed_diag(
                diagnostics,
                policy,
                "STRONG_SEED_WITHOUT_NEED",
                "无有效场景需求或功能演示时不得为完成配额硬设强种草组",
                section,
            )
        elif not allocation_id or allocation_id not in evidence_stop_ids or not under_target_reason:
            add_seed_diag(
                diagnostics,
                policy,
                "EVIDENCE_STOP_MISSING",
                "N0 且无 F2/F3 演示时，必须在 evidence_stop_ids 登记并填写 under_target_reason",
                section,
                metrics={
                    "id": allocation_id,
                    "listed": bool(allocation_id and allocation_id in evidence_stop_ids),
                    "has_reason": bool(under_target_reason),
                },
            )

        if watermark_present and m_level == "M0" and any_product_mention and not valid_strong_groups and not lh8:
            add_seed_diag(
                diagnostics,
                policy,
                "WATERMARK_ONLY_NAMING",
                "链接仅有水印型号提示，却在评论中点名产品且没有有效卖点链路",
                section,
            )
        watermark_mentions = [group for group in section.groups if WATERMARK_RE.search(group_copy(group))]
        if len(watermark_mentions) > 1:
            add_seed_diag(
                diagnostics,
                policy,
                "WATERMARK_MENTION_EXCESS",
                "同一链接最多一组可为混拍归属冲突提到水印",
                section,
                watermark_mentions[1],
            )
        for watermark_group in watermark_mentions:
            watermark_context = group_contexts.get(watermark_group.main.group, {})
            watermark_actual_s = str(watermark_context.get("actual_s_level", "")).upper()
            watermark_mode = str(watermark_context.get("claim_mode", "")).strip()
            allowed_watermark_mention = (
                mixed_unmapped
                and watermark_actual_s == "S0"
                and watermark_mode == "observed"
                and watermark_group.main.group != strong_group_no
            )
            if not allowed_watermark_mention:
                add_seed_diag(
                    diagnostics,
                    policy,
                    "WATERMARK_MENTION",
                    "评论默认不写水印；仅混拍归属冲突的单个 observed/S0 非种草组可例外",
                    section,
                    watermark_group,
                )

    if rule_version in LH6_PLUS_RULE_VERSIONS:
        audit_lh6_contract(sections, resolved_contexts, diagnostics, lh8=lh8, lh12=lh12)

    new_findings = diagnostics[start_index:]
    return {
        "status": "checked",
        "sections_checked": sections_checked,
        "groups_checked": groups_checked,
        "strong_seed_sections": strong_sections,
        "missing_context_sections": missing_context_sections,
        "findings_by_code": dict(Counter(item["code"] for item in new_findings)),
    }


def is_product_question(item: Item) -> bool:
    return bool(PRODUCT_CUE_RE.search(item.text) and QUESTION_RE.search(item.text))


def is_answer_proxy(text: str) -> bool:
    """Return whether a later reply appears to advance a product question.

    This intentionally stays conservative. An explicit "the post did not say"
    response is useful caveat copy, but it does not resolve the purchase question.
    """
    if QUESTION_RE.search(text) or UNRESOLVED_RE.search(text):
        return False
    if DIRECT_ANSWER_RE.search(text):
        return True
    return bool(feature_categories(text) or BENEFIT_PROXY_RE.search(text))


def audit_seed_proxies(sections: list[Section], diagnostics: list[dict], *, lh7: bool = False, lh8: bool = False, personal_need_groups: set[tuple[str, str, int]] | None = None, observed_s0_groups: set[tuple[str, str, int]] | None = None) -> dict:
    """Add advisory proxies for product-persuasion gaps.

    These checks deliberately emit warnings only. They expose likely weak spots
    for semantic review; they do not calculate or enforce an S0–S3 grade.
    """
    sections_with_benefit = 0
    zero_proxy_sections = 0
    product_question_sections = 0
    question_only_sections = 0
    caveat_dominance_sections = 0
    feature_stack_groups = 0
    push_density_sections = 0

    for section in sections:
        all_items = [item for group in section.groups for item in [group.main, *group.replies]]
        zero_proxy_exempt = (personal_need_groups or set()) | (observed_s0_groups or set())
        product_items = [item for item in all_items if PRODUCT_CUE_RE.search(item.text) and (item.file, item.section, item.group) not in zero_proxy_exempt]
        benefit_items = [item for item in all_items if BENEFIT_PROXY_RE.search(item.text)]

        if benefit_items:
            sections_with_benefit += 1
        elif product_items:
            zero_proxy_sections += 1
            diagnostics.append(
                {
                    "severity": "warning",
                    "code": "W_SEED_ZERO_PROXY",
                    "message": "链接已有产品或功能露出，但未发现面向用户的可感收益线索；请人工复核种草链路",
                    "locations": [loc(product_items[0])],
                    "metrics": {"product_cue_lines": len(product_items), "benefit_proxy_lines": 0},
                }
            )

        product_questions: list[Item] = []
        resolved_questions = 0
        for group in section.groups:
            ordered = [group.main, *group.replies]
            for index, item in enumerate(ordered):
                if not is_product_question(item):
                    continue
                product_questions.append(item)
                if any(is_answer_proxy(later.text) for later in ordered[index + 1 :]):
                    resolved_questions += 1
        if product_questions:
            product_question_sections += 1
        if product_questions and resolved_questions == 0 and not lh7:
            question_only_sections += 1
            diagnostics.append(
                {
                    "severity": "warning",
                    "code": "W_SEED_QUESTION_ONLY",
                    "message": "链接中的产品问题均未在后续回复得到收益或条件层面的推进",
                    "locations": [loc(item) for item in product_questions],
                    "metrics": {"product_questions": len(product_questions), "resolved_proxy": 0},
                }
            )

        caveat_items = [item for item in all_items if CAVEAT_RE.search(item.text)]
        if len(caveat_items) >= 3 and len(caveat_items) > max(1, len(benefit_items)) * 1.5:
            caveat_dominance_sections += 1
            diagnostics.append(
                {
                    "severity": "warning",
                    "code": "W_CAVEAT_DOMINANCE",
                    "message": "限制和不确定性表达明显多于收益表达，可能把前面的产品价值抵消掉",
                    "locations": [loc(item) for item in caveat_items],
                    "metrics": {
                        "caveat_lines": len(caveat_items),
                        "benefit_proxy_lines": len(benefit_items),
                        "ratio": round(len(caveat_items) / max(len(benefit_items), 1), 2),
                    },
                }
            )

        for group in section.groups:
            group_items = [group.main, *group.replies]
            categories: dict[str, list[Item]] = defaultdict(list)
            for item in group_items:
                for name in feature_categories(item.text):
                    categories[name].append(item)
            if len(categories) >= 3:
                feature_stack_groups += 1
                diagnostics.append(
                    {
                        "severity": "warning",
                        "code": "W_FEATURE_STACK",
                        "message": "单组评论出现三个以上产品功能类别，可能从真人讨论滑向功能清单",
                        "locations": [loc(group.main)],
                        "metrics": {
                            "feature_count": len(categories),
                            "features": sorted(categories),
                            "feature_line_counts": {name: len(items) for name, items in sorted(categories.items())},
                        },
                    }
                )

        hard_matches: list[tuple[Item, str]] = []
        soft_matches: list[tuple[Item, str]] = []
        soft_groups: set[int] = set()
        for group in section.groups:
            for item in [group.main, *group.replies]:
                item_hard = [match.group(0) for match in HARD_PUSH_RE.finditer(item.text)]
                item_soft = lh8_soft_purchase_terms(item.text) if lh8 else [match.group(0) for match in SOFT_PURCHASE_RE.finditer(item.text)]
                hard_matches.extend((item, value) for value in item_hard)
                soft_matches.extend((item, value) for value in item_soft)
                if item_soft:
                    soft_groups.add(group.main.group)
        if hard_matches or len(soft_groups) > 1 or len(soft_matches) > 2:
            push_density_sections += 1
            push_items: list[Item] = []
            seen_locations: set[tuple[str, int]] = set()
            for item, _ in [*hard_matches, *soft_matches]:
                key = (item.file, item.line)
                if key not in seen_locations:
                    seen_locations.add(key)
                    push_items.append(item)
            diagnostics.append(
                {
                    "severity": "warning",
                    "code": "W_PUSH_WORD_DENSITY",
                    "message": "强推词或显性购买倾向出现过密；每个链接最多保留一组克制的购买联想",
                    "locations": [loc(item) for item in push_items],
                    "metrics": {
                        "hard_terms": [value for _, value in hard_matches],
                        "soft_terms": [value for _, value in soft_matches],
                        "purchase_tendency_groups": sorted(soft_groups),
                    },
                }
            )

    return {
        "sections_with_benefit_proxy": sections_with_benefit,
        "sections_without_benefit_proxy": zero_proxy_sections,
        "product_question_sections": product_question_sections,
        "question_only_sections": question_only_sections,
        "caveat_dominance_sections": caveat_dominance_sections,
        "feature_stack_groups": feature_stack_groups,
        "push_density_sections": push_density_sections,
        "note": "proxy warnings require semantic review and do not assign S0-S3 grades",
    }


def audit_length_and_punctuation(sections: list[Section], mains: list[Item], diagnostics: list[dict]) -> dict:
    lengths = [valid_len(item.text) for item in mains]
    platform_items: dict[str, list[Item]] = defaultdict(list)
    for section in sections:
        platform = section_platform(section)
        platform_items[platform].extend(group.main for group in section.groups)
        local = [valid_len(group.main.text) for group in section.groups]
        suggested_gap = 8 if platform == "xhs" else 6
        if len(local) == 3 and (max(local) - min(local) < suggested_gap or (statistics.mean(local) >= 10 and coefficient_of_variation(local) <= 0.08)):
            diagnostics.append(diag("warning", "W_UNIFORM_LENGTH_LOCAL", f"同一链接三条主评长度过齐：{local}", section.file, section.line, section.number))
        if section.groups and all("，" in group.main.text or "," in group.main.text for group in section.groups):
            diagnostics.append(diag("warning", "W_ALL_COMMA_LOCAL", "同一链接三条主评都使用逗号骨架", section.file, section.line, section.number))

    band_metrics: dict[str, dict] = {}
    for platform, items in platform_items.items():
        if not items:
            continue
        platform_lengths = [valid_len(item.text) for item in items]
        if platform == "xhs":
            short_limit, long_limit = 17, 32
        elif platform == "douyin":
            short_limit, long_limit = 13, 24
        else:
            short_limit, long_limit = 18, 35
        short_ratio = sum(length <= short_limit for length in platform_lengths) / len(platform_lengths)
        long_ratio = sum(length >= long_limit for length in platform_lengths) / len(platform_lengths)
        band_metrics[platform] = {
            "count": len(platform_lengths),
            "short_limit": short_limit,
            "long_limit": long_limit,
            "short_ratio": round(short_ratio, 3),
            "long_ratio": round(long_ratio, 3),
        }
        if len(platform_lengths) < 15:
            continue
        cv = coefficient_of_variation(platform_lengths)
        iqr = percentile(platform_lengths, 0.75) - percentile(platform_lengths, 0.25)
        if cv < 0.20 and iqr <= 8:
            diagnostics.append({"severity": "warning", "code": f"W_UNIFORM_LENGTH_{platform.upper()}", "message": f"{platform} 主评长度分布过窄", "locations": [], "metrics": {"cv": round(cv, 3), "iqr": round(iqr, 2)}})
        if short_ratio < 0.20 or long_ratio < 0.15:
            diagnostics.append({"severity": "warning", "code": f"W_LENGTH_BANDS_{platform.upper()}", "message": f"{platform} 短句或长句比例不足，主评可能集中在同一长度档", "locations": [], "metrics": band_metrics[platform]})

    one_comma = sum(item.text.count("，") + item.text.count(",") == 1 for item in mains)
    any_comma = sum("，" in item.text or "," in item.text for item in mains)
    if len(mains) >= 15 and (one_comma / len(mains) > 0.40 or any_comma / len(mains) > 0.75):
        diagnostics.append({"severity": "warning", "code": "W_COMMA_PATTERN", "message": "“画面＋逗号＋判断”句形占比过高", "locations": [], "metrics": {"one_comma": round(one_comma / len(mains), 3), "any_comma": round(any_comma / len(mains), 3)}})

    moment_items = [item for item in mains if MOMENT_RE.search(item.text)]
    reaction_items = [item for item in mains if REACTION_RE.search(item.text)]
    if len(mains) >= 15 and len(moment_items) / len(mains) > 0.20:
        diagnostics.append({"severity": "warning", "code": "W_MOMENT_PHRASES", "message": "“这段/那一下/最后”等瞬间指示词使用过密", "locations": [loc(item) for item in moment_items], "metrics": {"ratio": round(len(moment_items) / len(mains), 3)}})
    if len(mains) >= 15 and len(reaction_items) / len(mains) > 0.10:
        diagnostics.append({"severity": "warning", "code": "W_REACTION_PHRASES", "message": "观看反应套语使用过密", "locations": [loc(item) for item in reaction_items], "metrics": {"ratio": round(len(reaction_items) / len(mains), 3)}})

    return {
        "min": min(lengths) if lengths else 0,
        "median": statistics.median(lengths) if lengths else 0,
        "max": max(lengths) if lengths else 0,
        "short_le_18": sum(length <= 18 for length in lengths),
        "long_ge_35": sum(length >= 35 for length in lengths),
        "by_platform": band_metrics,
    }


def audit_replies(sections: list[Section], diagnostics: list[dict], *, lh7: bool = False) -> Counter:
    if lh7:
        # Two replies are the default; repeated counts alone are not copy similarity.
        return Counter(len(group.replies) for section in sections for group in section.groups)
    counts: list[int] = []
    combos: list[tuple[int, ...]] = []
    combo_sections: list[Section] = []
    combo_locations: dict[tuple[int, ...], list[Section]] = defaultdict(list)
    for section in sections:
        combo = tuple(len(group.replies) for group in section.groups)
        if combo:
            combos.append(combo)
            combo_sections.append(section)
            combo_locations[combo].append(section)
            counts.extend(combo)
        if len(combo) == 3 and len(set(combo)) == 1:
            diagnostics.append(diag("warning", "W_REPLY_COUNT_LOCAL", f"同一链接三组回复数完全一致：{combo}", section.file, section.line, section.number))

    distribution = Counter(counts)
    if counts:
        value, count = distribution.most_common(1)[0]
        if count / len(counts) >= 0.65:
            diagnostics.append({"severity": "warning", "code": "W_REPLY_COUNT_BATCH", "message": f"回复数 {value} 在全批占比过高", "locations": [], "metrics": {"ratio": round(count / len(counts), 3)}})

    for combo, matches in combo_locations.items():
        if len(matches) >= 10 and len(matches) / max(len(sections), 1) >= 0.30:
            diagnostics.append({"severity": "warning", "code": "W_REPLY_COMBO", "message": f"回复数组合 {combo} 重复过密", "locations": [{"file": section.file, "line": section.line, "section": section.number, "group": None} for section in matches], "metrics": {"ratio": round(len(matches) / len(sections), 3)}})

    all_distinct = [section for section in sections if len(section.groups) == 3 and sorted(len(group.replies) for group in section.groups) == [2, 3, 4]]
    if len(sections) >= 8 and len(all_distinct) / len(sections) > 0.50:
        diagnostics.append({"severity": "warning", "code": "W_REPLY_PERMUTATION", "message": "过多链接刻意凑成2/3/4条回复各一次", "locations": [{"file": section.file, "line": section.line, "section": section.number, "group": None} for section in all_distinct], "metrics": {"ratio": round(len(all_distinct) / len(sections), 3)}})

    for index in range(len(combos) - 2):
        if combos[index] == combos[index + 1] == combos[index + 2]:
            section = combo_sections[index]
            diagnostics.append(diag("warning", "W_REPLY_COMBO_RUN", f"连续3个链接使用相同回复数组合 {combos[index]}", section.file, section.line, section.number))
            break

    for index in range(max(len(combos) - 14, 0)):
        window = combos[index : index + 15]
        repeated = Counter(window).most_common(1)[0]
        if repeated[1] > 3:
            section = combo_sections[index + 14]
            diagnostics.append(
                diag(
                    "warning",
                    "W_REPLY_COMBO_ROLLING",
                    f"连续15个链接内回复数组合 {repeated[0]} 出现{repeated[1]}次",
                    section.file,
                    section.line,
                    section.number,
                    metrics={"window_start": combo_sections[index].number, "ratio": round(repeated[1] / 15, 3)},
                )
            )
            break
    return distribution


def audit_product_patterns(
    sections: list[Section],
    mains: list[Item],
    diagnostics: list[dict],
    product_policy: str = "off",
    *,
    lh7: bool = False,
) -> dict:
    arrangements: Counter = Counter()
    full_slots: Counter = Counter()
    short_slots: Counter = Counter()
    arrangement_sections: dict[tuple[str, ...], list[Section]] = defaultdict(list)
    full_start_sections = 0

    for section in sections:
        classes = tuple(product_class(group.main.text, lh7=group.main.lh7) for group in section.groups)
        arrangements[classes] += 1
        arrangement_sections[classes].append(section)
        named = sum(value != "NONE" for value in classes)
        full_labels = []
        for group in section.groups:
            match = FULL_PRODUCT_RE.search(group.main.text)
            if match:
                full_labels.append(re.sub(r"\s+", "", match.group(0).lower()))
        if len(classes) == 3 and named != 2 and product_policy != "off":
            severity = "error" if product_policy == "strict" else "warning"
            code = "E_TWO_CLEAR_ONE_HIDDEN" if severity == "error" else "W_TWO_CLEAR_ONE_HIDDEN"
            diagnostics.append(diag(severity, code, f"默认两明一隐；当前产品分类为 {classes}", section.file, section.line, section.number))
        repeated_full = [label for label, count in Counter(full_labels).items() if count > 1]
        if repeated_full and product_policy != "off":
            severity = "error" if product_policy == "strict" else "warning"
            code = "E_FULL_PRODUCT_REPEAT" if severity == "error" else "W_FULL_PRODUCT_REPEAT"
            diagnostics.append(diag(severity, code, f"同一链接重复完整型号：{repeated_full[0]}", section.file, section.line, section.number))
        for slot, value in enumerate(classes, 1):
            if value == "FULL":
                full_slots[slot] += 1
                if product_position(section.groups[slot - 1].main.text, lh7=section.groups[slot - 1].main.lh7) == "start":
                    full_start_sections += 1
            elif value == "SHORT":
                short_slots[slot] += 1
        product_starts = [group.main for group in section.groups if product_in_first_six(group.main.text, lh7=group.main.lh7)]
        if len(product_starts) > 1:
            diagnostics.append({"severity": "warning", "code": "W_PRODUCT_START_LOCAL", "message": "同一链接超过一条主评在前6字出现产品词", "locations": [loc(item) for item in product_starts]})
        for group, value in zip(section.groups, classes):
            if product_policy != "off" and value == "NONE" and not any(PRODUCT_CUE_RE.search(reply.text) for reply in group.replies):
                diagnostics.append(diag("warning", "W_HIDDEN_PRODUCT_CUE", "隐性组楼中楼未发现明显产品线索，请人工确认画面是否已完成关联", group.main.file, group.main.line, group.main.section, group.main.group))

    starts = [item for item in mains if product_in_first_six(item.text, lh7=item.lh7)]
    positions = Counter(product_position(item.text, lh7=item.lh7) for item in mains)
    if len(mains) >= 12 and len(starts) / len(mains) > 0.30:
        diagnostics.append({"severity": "warning", "code": "W_PRODUCT_START_BATCH", "message": "产品词位于主评前6字的比例过高", "locations": [loc(item) for item in starts], "metrics": {"ratio": round(len(starts) / len(mains), 3)}})

    for index in range(max(len(mains) - 11, 0)):
        window = mains[index : index + 12]
        window_starts = [item for item in window if product_in_first_six(item.text, lh7=item.lh7)]
        if len(window_starts) > 3:
            diagnostics.append(
                {
                    "severity": "warning",
                    "code": "W_PRODUCT_START_ROLLING",
                    "message": f"连续12条主评中有{len(window_starts)}条在前6字出现产品词",
                    "locations": [loc(item) for item in window_starts],
                    "metrics": {"window_start": loc(window[0]), "window_end": loc(window[-1])},
                }
            )
            break

    for label, slots in (() if lh7 else (("完整型号", full_slots), ("简称", short_slots))):
        total = sum(slots.values())
        if total >= 8:
            slot, count = slots.most_common(1)[0]
            if count / total >= 0.70:
                diagnostics.append({"severity": "warning", "code": "W_PRODUCT_SLOT", "message": f"{label}长期固定在第{slot}组", "locations": [], "metrics": {"ratio": round(count / total, 3), "slot": slot}})

    for arrangement, matches in arrangement_sections.items():
        if not lh7 and len(matches) >= 10 and len(matches) / max(len(sections), 1) >= 0.50:
            diagnostics.append({"severity": "warning", "code": "W_PRODUCT_ARRANGEMENT", "message": f"产品露出排列 {arrangement} 占比过高", "locations": [{"file": section.file, "line": section.line, "section": section.number, "group": None} for section in matches], "metrics": {"ratio": round(len(matches) / len(sections), 3)}})

    sequence = [tuple(product_class(group.main.text, lh7=group.main.lh7) for group in section.groups) for section in sections]
    for index in range(len(sequence) - 2):
        if not lh7 and len(set(sequence[index : index + 3])) == 1:
            section = sections[index]
            diagnostics.append(diag("warning", "W_PRODUCT_ARRANGEMENT_RUN", f"连续3个链接使用相同产品露出排列 {sequence[index]}", section.file, section.line, section.number))
            break

    full_presence = [any(product_class(group.main.text, lh7=group.main.lh7) == "FULL" for group in section.groups) for section in sections]
    for index in range(max(len(full_presence) - 9, 0)):
        count = sum(full_presence[index : index + 10])
        if not lh7 and count > 7:
            section = sections[index + 9]
            diagnostics.append(
                diag(
                    "warning",
                    "W_FULL_PRODUCT_ROLLING",
                    f"连续10个链接中有{count}个使用完整型号，露出可能过整齐",
                    section.file,
                    section.line,
                    section.number,
                    metrics={"window_start": sections[index].number, "ratio": round(count / 10, 3)},
                )
            )
            break

    exposure_sets: list[set[tuple[str, int, str]]] = []
    for section in sections:
        entries: set[tuple[str, int, str]] = set()
        for slot, group in enumerate(section.groups, 1):
            match = find_product_match(group.main.text, lh7=group.main.lh7)
            if match:
                label = re.sub(r"\s+", "", match.group(0).lower())
                entries.add((label, slot, product_position(group.main.text, lh7=group.main.lh7)))
        exposure_sets.append(entries)
    for index in range(len(exposure_sets) - 2):
        repeated = exposure_sets[index] & exposure_sets[index + 1] & exposure_sets[index + 2]
        if repeated:
            label, slot, position = sorted(repeated)[0]
            section = sections[index]
            diagnostics.append(
                diag(
                    "warning",
                    "W_PRODUCT_LABEL_POSITION_RUN",
                    f"连续3个链接把“{label}”放在第{slot}组的{position}位置",
                    section.file,
                    section.line,
                    section.number,
                )
            )
            break

    return {
        "classes": dict(Counter(product_class(item.text, lh7=item.lh7) for item in mains)),
        "positions": dict(positions),
        "arrangements": {"/".join(key): value for key, value in arrangements.items()},
        "full_start_sections": full_start_sections,
    }


def audit(
    paths: list[Path],
    baseline_paths: list[Path] | None = None,
    product_policy: str = "off",
    *,
    state_path: Path | None = None,
    seeding_policy: str = "advisory",
    claim_registry_path: Path | None = None,
) -> dict:
    baseline_paths = baseline_paths or []
    sections: list[Section] = []
    baseline_sections: list[Section] = []
    diagnostics: list[dict] = []
    contexts: dict[str, list[dict[str, Any]]] = {}
    state: dict[str, Any] = {}
    if state_path is not None or seeding_policy != "off":
        state_diagnostics: list[dict] = []
        contexts, state = load_seed_state(state_path, seeding_policy, state_diagnostics)
        if seeding_policy != "off" or state.get("rule_version") in LH7_PLUS_RULE_VERSIONS:
            diagnostics.extend(state_diagnostics)
    lh12 = state.get("rule_version") == LH12_RULE_VERSION
    for path in paths:
        parsed, parse_diagnostics = parse_file(path, lh12=lh12)
        sections.extend(parsed)
        diagnostics.extend(parse_diagnostics)
    for path in baseline_paths:
        parsed, _ = parse_file(path, lh12=lh12)
        baseline_sections.extend(parsed)
        if not parsed:
            diagnostics.append(diag("warning", "W_BASELINE_EMPTY", "历史基线未解析出任何链接章节，请检查批量标题格式", path, 1))

    if not sections:
        diagnostics.append(diag("error", "E_NO_SECTIONS", "当前草稿未解析出任何链接章节；批量标题应包含平台（可选）、原序号和链接", paths[0] if paths else None, 1))

    mains = [group.main for section in sections for group in section.groups]
    replies = [reply for section in sections for group in section.groups for reply in group.replies]
    baseline_mains = [group.main for section in baseline_sections for group in section.groups]
    baseline_replies = [reply for section in baseline_sections for group in section.groups for reply in group.replies]

    lh7 = state.get("rule_version") in LH7_PLUS_RULE_VERSIONS
    if lh7:
        # History participates in alias-aware comparison, never new copy gates.
        for item in [*mains, *replies, *baseline_mains, *baseline_replies]:
            item.lh7 = True
    audit_structure(sections, diagnostics, lh7=lh7, lh12=lh12, delivery_mode=state.get("delivery_mode", "with_replies"))
    if lh7:
        audit_lh7_copy(sections, state, diagnostics)
    dialogue_stats = audit_lh9_dialogues(sections, contexts, state, diagnostics) if state.get("rule_version") in LH9_PLUS_RULE_VERSIONS else None
    diversity_stats = None
    diversity_reviewed_ids: set[str] = set()
    if state.get("rule_version") in LH10_PLUS_RULE_VERSIONS:
        diversity_stats, diversity_reviewed_ids = audit_lh10_diversity(sections, contexts, state, diagnostics)
    audit_duplicates(mains, diagnostics, "main")
    audit_duplicates(replies, diagnostics, "reply")
    audit_near_duplicates(mains, diagnostics, "main")
    audit_near_duplicates(replies, diagnostics, "reply")
    audit_against_baseline(mains, baseline_mains, diagnostics, "main")
    audit_against_baseline(replies, baseline_replies, diagnostics, "reply")
    audit_baseline_openings(mains, baseline_mains, diagnostics)
    audit_openings_and_patterns(sections, mains, diagnostics)
    length_stats = audit_length_and_punctuation(sections, mains, diagnostics)
    reply_distribution = audit_replies(sections, diagnostics, lh7=lh7)
    product_stats = audit_product_patterns(sections, mains, diagnostics, "off" if lh7 else product_policy, lh7=lh7)
    if seeding_policy == "off":
        seed_stats: dict[str, Any] = {"status": "off", "note": "LH5/LH6/LH7/LH8/LH9/LH10/LH11/LH12 seeding checks disabled"}
    else:
        personal_need_groups: set[tuple[str, str, int]] = set()
        observed_s0_groups: set[tuple[str, str, int]] = set()
        seed_stats = {}
        registry = load_claim_registry(claim_registry_path or DEFAULT_CLAIM_REGISTRY, seeding_policy, diagnostics)
        if registry and state_path is not None and state:
            seed_stats["semantic"] = audit_seed_semantics(
                sections,
                contexts,
                state,
                registry,
                diagnostics,
                seeding_policy,
                personal_need_groups=personal_need_groups,
                observed_s0_groups=observed_s0_groups,
                diversity_reviewed_ids=diversity_reviewed_ids,
            )
        elif not registry:
            seed_stats["semantic"] = {
                "status": "invalid_registry",
                "sections_checked": 0,
                "groups_checked": 0,
                "strong_seed_sections": 0,
                "missing_context_sections": len(sections),
                "findings_by_code": {},
            }
        elif state_path is not None:
            if not any(item["code"].endswith("SEED_STATE_INVALID") for item in diagnostics):
                add_seed_diag(
                    diagnostics,
                    seeding_policy,
                    "SEED_STATE_INVALID",
                    "--state 文件为空或缺少 LH5/LH6/LH7/LH8/LH9/LH10/LH11/LH12 顶层结构",
                    hard=True,
                    file=state_path,
                )
            seed_stats["semantic"] = {
                "status": "invalid_state",
                "sections_checked": 0,
                "groups_checked": 0,
                "strong_seed_sections": 0,
                "missing_context_sections": len(sections),
                "findings_by_code": {},
            }
        else:
            seed_stats["semantic"] = {
                "status": "missing_state",
                "sections_checked": 0,
                "groups_checked": 0,
                "strong_seed_sections": 0,
                "missing_context_sections": len(sections),
                "findings_by_code": {},
            }
        seed_stats.update(audit_seed_proxies(sections, diagnostics, lh7=lh7, lh8=state.get("rule_version") in LH8_PLUS_RULE_VERSIONS, personal_need_groups=personal_need_groups, observed_s0_groups=observed_s0_groups))

    diagnostics.sort(key=lambda item: (0 if item["severity"] == "error" else 1, item["code"], item.get("locations", [{}])[0].get("file", "") if item.get("locations") else "", item.get("locations", [{}])[0].get("line", 0) if item.get("locations") else 0))
    errors = sum(item["severity"] == "error" for item in diagnostics)
    warnings = sum(item["severity"] == "warning" for item in diagnostics)

    return {
        "dialogue": dialogue_stats,
        **({"diversity": diversity_stats} if diversity_stats is not None else {}),
        "summary": {
            "files": len(paths),
            "baseline_files": len(baseline_paths),
            "sections": len(sections),
            "baseline_sections": len(baseline_sections),
            "groups": len(mains),
            "mains": len(mains),
            "baseline_mains": len(baseline_mains),
            "replies": len(replies),
            "errors": errors,
            "warnings": warnings,
        },
        "distributions": {
            "main_length": length_stats,
            "reply_counts": dict(sorted(reply_distribution.items())),
            "product": product_stats,
            "seeding": seed_stats,
        },
        "diagnostics": diagnostics,
    }


def render_text(result: dict, max_examples: int, verbose: bool = False) -> str:
    summary = result["summary"]
    lines = [
        "DJI Pocket 评论同质化检查",
        f"files={summary['files']} baseline_files={summary['baseline_files']} sections={summary['sections']} baseline_sections={summary['baseline_sections']} groups={summary['groups']} mains={summary['mains']} baseline_mains={summary['baseline_mains']} replies={summary['replies']}",
        f"errors={summary['errors']} warnings={summary['warnings']}",
    ]
    if verbose:
        diagnostic_groups = [[item] for item in result["diagnostics"]]
    else:
        grouped: dict[tuple[str, str], list[dict]] = {}
        for item in result["diagnostics"]:
            grouped.setdefault((item["severity"], item["code"]), []).append(item)
        diagnostic_groups = list(grouped.values())

    for matches in diagnostic_groups:
        item = matches[0]
        count_suffix = f" ({len(matches)} events)" if len(matches) > 1 else ""
        lines.append(f"[{item['severity'].upper()}] {item['code']}{count_suffix}: {item['message']}")
        locations: list[dict] = []
        for match in matches:
            locations.extend(match.get("locations", []))
        for location in locations[:max_examples]:
            group = f" group={location.get('group')}" if location.get("group") else ""
            lines.append(f"  - {location.get('file')}:{location.get('line')} section={location.get('section')}{group}")
        if len(locations) > max_examples:
            lines.append(f"  - ... and {len(locations) - max_examples} more locations")
        if len(matches) == 1 and item.get("metrics"):
            lines.append(f"  metrics={json.dumps(item['metrics'], ensure_ascii=False, sort_keys=True)}")
    lines.append("distributions=" + json.dumps(result["distributions"], ensure_ascii=False, sort_keys=True))
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="Current draft Markdown files or directories")
    parser.add_argument("--baseline", nargs="+", default=[], help="Historical Markdown used only for cross-batch similarity checks")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--strict", action="store_true", help="Return 1 when warnings exist")
    parser.add_argument("--verbose", action="store_true", help="Print every diagnostic event instead of grouping by code")
    parser.add_argument(
        "--product-policy",
        choices=("advisory", "strict", "off"),
        default="off",
        help="Legacy two-clear-one-hidden policy; use off for LH5/LH6; ignored by LH7/LH8/LH9/LH10/LH11/LH12",
    )
    parser.add_argument("--state", type=Path, help="LH5/LH6/LH7/LH8/LH9/LH10/LH11/LH12 pocket_comment_state.json with per-section M/N/F/P evidence")
    parser.add_argument(
        "--seeding-policy",
        choices=("advisory", "strict", "off"),
        default="advisory",
        help="How to enforce LH5/LH6/LH7/LH8/LH9/LH10/LH11/LH12 evidence-aware product seeding checks",
    )
    parser.add_argument(
        "--claim-registry",
        type=Path,
        default=DEFAULT_CLAIM_REGISTRY,
        help="Versioned Pocket claim registry (defaults to references/product-claims.json)",
    )
    parser.add_argument("--max-examples", type=int, default=4)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.max_examples < 1:
        print("--max-examples must be >= 1", file=sys.stderr)
        return 2
    try:
        paths = collect_paths(args.inputs)
        if not paths:
            raise FileNotFoundError("no Markdown files found")
        baseline_paths = collect_paths(args.baseline) if args.baseline else []
        candidate_set = set(paths)
        baseline_paths = [path for path in baseline_paths if path not in candidate_set]
        state_path = args.state.expanduser().resolve() if args.state else None
        claim_registry_path = args.claim_registry.expanduser().resolve()
        result = audit(
            paths,
            baseline_paths,
            args.product_policy,
            state_path=state_path,
            seeding_policy=args.seeding_policy,
            claim_registry_path=claim_registry_path,
        )
    except (FileNotFoundError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text(result, args.max_examples, args.verbose))
    if result["summary"]["errors"]:
        return 1
    if args.strict and result["summary"]["warnings"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
