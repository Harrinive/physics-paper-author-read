# Physics paper author read skill

Responds to a physics author's own edits and margin comments. It reads each change
in its story, treats its guessed purpose as a ruling, accepts silently, and brings
back only the decisions the author must make, one at a time. A recurring pattern is
swept across the paper with a verdict for every occurrence, checked by
`scripts/check_sweep.py`. Start with [SKILL.md](SKILL.md).

## Install

Clone it next to its siblings, under `~/.agents/skills/` or the matching folder of
your host:

```bash
git clone https://github.com/Harrinive/physics-paper-author-read.git ~/.agents/skills/physics-paper-author-read
```

It needs [physics-paper-principles](https://github.com/Harrinive/physics-paper-principles),
[physics-paper-editing](https://github.com/Harrinive/physics-paper-editing), and
[physics-paper-editing-section](https://github.com/Harrinive/physics-paper-editing-section)
as sibling folders. The script needs only `python3`.

## Supported hosts

The skill follows the [Agent Skills specification](https://agentskills.io/specification)
and is designed for Cursor, OpenAI Codex, and Claude Code. It contains no
host-specific instructions.
