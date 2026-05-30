"""
AGENTS.md loader plugin - 在 agent_before 时注入 AGENTS.md 到 system prompt
"""
import os
from plugins import hooks

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_AGENTS_PATH = os.path.join(_PROJECT_ROOT, 'AGENTS.md')

# 加载 AGENTS.md 内容
_AGENTS_CONTENT = None
if os.path.exists(_AGENTS_PATH):
    with open(_AGENTS_PATH, 'r', encoding='utf-8') as f:
        _AGENTS_CONTENT = f.read()

@hooks.register('agent_before')
def inject_agents_md(ctx):
    """在 agent 启动前注入 AGENTS.md 到 system prompt"""
    if _AGENTS_CONTENT and 'system_prompt' in ctx:
        # 在 system prompt 后面追加 AGENTS.md 内容
        ctx['system_prompt'] += f'\n\n[Project Constraints] (../AGENTS.md)\n{_AGENTS_CONTENT}\n'
        return ctx
    return ctx
