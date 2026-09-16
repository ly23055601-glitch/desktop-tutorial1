#!/usr/bin/env python3
"""Render Nano selling-point and training-scene reading views from JSONL."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
KB = ROOT / 'knowledge/nano'


def read_rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def bullets(label, values):
    return ['','**'+label+'**','']+['- '+value for value in values]


def fact_links(ids):
    return '、'.join(f'[{fid}](../products/guide.md#{fid.lower()})' for fid in ids)


def render_selling(rows):
    edited = max(r.get('deepened_at',r['prepared_at']) for r in rows)
    lines=['# Nano 卖点与使用价值','',f'本阅读版由 {len(rows)} 条[结构化卖点卡](cards.jsonl)生成；修改卡片后运行 `build_material_views.py` 同步。最近编辑：{edited}；事实实际核验日期见关联条目。',
           '','使用价值为编辑解释（`editorial_interpretation`），仍待用户校准。能力概述不替代完整产品条件；不证明真实用户需要或竞品不具备相同能力。选材方法见[培训专题](../TRAINING.md)。','',
           '| 卖点 | 使用价值 |','|---|---|']
    lines += [f'| [{r["id"]}｜{r["title"]}](#{r["id"].lower()}) | {r["user_value"].replace("|","／")} |' for r in rows]
    for r in rows:
        lines += ['',f'<a id="{r["id"].lower()}"></a>','',f'## {r["id"]}｜{r["title"]}','',
                  '**官方能力概述：** '+r['capability_summary'],'','**使用价值（编辑解释）：** '+r['user_value'],
                  '', '**关联事实：** '+fact_links(r['fact_ids'])]
        if r.get('value_facets'):
            lines += ['','**同一卖点下可以分开的兴趣（编辑解释）：**','',
                      '| 关注点 | 可能的使用或观看价值 | 选材线索与边界 |','|---|---|---|']
            for facet in r['value_facets']:
                lines.append('| '+' | '.join(facet[key].replace('|','／') for key in ['focus','viewer_or_user_value','material_cue'])+' |')
        for lens in r.get('decision_lenses',[]):
            lines += ['','**把价值落到具体选择（编辑解释）：**','',
                      '- 情境：'+lens['situation'],
                      '- 为什么值得在意：'+lens['why_it_matters'],
                      '- 何时价值下降：'+lens['when_value_falls'],
                      '- 需要观察：'+lens['what_to_observe']]
        for field,label in [('strong_fit_signals','适合从当前材料选用的信号'),('weak_fit_signals','不宜硬提的情况'),('possible_motives','可能动机'),('tradeoffs','取舍'),('expression_angles','可选择的表达关注点'),('conditions','使用条件'),('not_infer','不能据此推导')]:
            lines += bullets(label,r[field])
        lines += ['','**关键词：** '+'、'.join(r['keywords']),'','状态：`'+r['review_status']+'`；编写：'+r['prepared_at']]
    return '\n'.join(lines)+'\n'


def render_scenes(rows):
    labels={'training-daily':'日常与关系','training-extended':'活动与创作',
            'training-domestic-expansion':'关系与私人记忆补充','training-work-expansion':'轻型工作与创作补充',
            'training-participation-expansion':'参与与关系细节','training-practical-expansion':'设备分工与拍摄取舍'}
    source_links='、'.join(f'[{labels.get(p.stem,p.stem)}]({p.name})' for p in sorted((KB/'scenarios').glob('training-*.jsonl')))
    lines=['# Nano 细场景与培训选材','',f'共 {len(rows)} 张细场景卡，结构化数据：{source_links}。阅读版由 `build_material_views.py` 生成。',
           '','所有场景与心理均为待校准的编辑假设（`editorial_hypothesis`）。卡片提供选材，不是完整人物经历或可粘贴评论。原有[7张基础场景卡](guide.md)继续用于查基础操作边界。方法见[培训专题](../TRAINING.md)。','',
           '| 场景 | 拍摄目标 | 关联卖点 |','|---|---|---|']
    for r in rows:
        links='、'.join(f'[{sid}](../selling-points/guide.md#{sid.lower()})' for sid in r['selling_point_ids'])
        lines += [f'| [{r["id"]}｜{r["title"]}](#{r["id"].lower()}) | {r["shooting_goal"].replace("|","／")} | {links} |']
    for r in rows:
        lines += ['',f'<a id="{r["id"].lower()}"></a>','',f'## {r["id"]}｜{r["title"]}','',
                  '**类别：** '+r['group'],'','**具体片段：** '+r['moment'],'','**想留下什么：** '+r['shooting_goal'],
                  '','**拍给谁看：** '+'、'.join(r['audience_or_recipient']),'','**拍摄安排：** '+r['capture_approach'],
                  '','**关联事实：** '+fact_links(r['fact_ids'])]
        if r.get('viewer_payoff'):
            lines += ['','**拍后观看价值（编辑解释）：** '+r['viewer_payoff']]
        if r.get('usage_stage_angles'):
            lines += bullets('不同使用阶段可以关注什么（编辑假设）',r['usage_stage_angles'])
        if r.get('differentiation_note'):
            lines += ['','**本卡补充的具体区别：** '+r['differentiation_note']]
        for field,label in [('observable_details','可寻找的画面／声音细节（不是已观察事实）'),('interest_branches','不同兴趣可分别选择（编辑假设）')]:
            if r.get(field):
                lines += bullets(label,r[field])
        lines += ['','**为什么考虑这些卖点（编辑解释）：**','']
        for point in r['why_these_points']:
            sid=point['selling_point_id']
            lines.append(f'- [{sid}](../selling-points/guide.md#{sid.lower()})：'+point['value_reason'])
        for field,label in [('possible_motives','可能动机'),('frictions','可能顾虑'),('strong_fit_signals','适合选用的材料信号'),('weak_fit_signals','不宜硬提的情况'),('expression_angles','可以分别展开的表达关注点'),('variation_axes','继续发散的维度'),('conditions','使用前提'),('not_infer','不能据此推导')]:
            lines += bullets(label,r[field])
        lines += ['','**关键词：** '+'、'.join(r['keywords']),'','状态：`'+r['review_status']+'`；编写：'+r['prepared_at']]
    return '\n'.join(lines)+'\n'


def render_reverse_map(selling, scenes):
    lines=['# 从 Nano 卖点反查使用场景','',
           '由卖点和场景的现有引用生成。先按当前材料找一个有用的兴趣，再读对应卡片的条件；关联数量不是推荐强度，场景仍是编辑假设。',
           '','也可从[培训选材专题](../TRAINING.md)按生活片段进入。每个卖点下的三种兴趣可分别使用，不需写进同一条评论。','']
    for point in selling:
        sid=point['id']
        linked=[r for r in scenes if sid in r['selling_point_ids']]
        lines += [f'## {sid}｜{point["title"]}','',
                  '[完整卖点与条件](guide.md#'+sid.lower()+')；关联事实：'+fact_links(point['fact_ids']),
                  '', '**可分别选择的兴趣：** '+'；'.join(f['focus'] for f in point.get('value_facets',[])),
                  '', '| 具体场景 | 为什么在这里考虑它（编辑解释） |','|---|---|']
        for scene in linked:
            reason=next(p['value_reason'] for p in scene['why_these_points'] if p['selling_point_id']==sid)
            lines.append(f'| [{scene["id"]}｜{scene["title"]}](../scenarios/training-guide.md#{scene["id"].lower()}) | {reason.replace("|","／")} |')
        lines += ['']
    return '\n'.join(lines)+'\n'


if __name__ == '__main__':
    selling=read_rows(KB/'selling-points/cards.jsonl')
    scenes=[row for path in sorted((KB/'scenarios').glob('training-*.jsonl')) for row in read_rows(path)]
    scenes.sort(key=lambda row:row['id'])
    (KB/'selling-points/guide.md').write_text(render_selling(selling))
    (KB/'scenarios/training-guide.md').write_text(render_scenes(scenes))
    (KB/'selling-points/scenario-map.md').write_text(render_reverse_map(selling,scenes))
    print(json.dumps({'selling_points':len(selling),'training_scenarios':len(scenes),'rendered':True}))
