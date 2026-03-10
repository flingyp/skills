# Third-Party Skills Management

This repository keeps skill management artifacts at the root so operational files do not mix with the skill directories themselves.

## Files

- `skills-registry.json`: the source-of-truth registry for every skill in this repository
- `sync-third-party-skills.py`: report and sync tool for third-party skills
- `THIRD_PARTY_SKILLS.md`: usage and ownership notes

## Ownership Model

- `third_party`: a skill with a verified upstream source. These entries can be synced automatically.
- `first_party`: a locally authored skill maintained in this repository. These entries are reported but never overwritten by the sync script.
- `unknown`: a skill that already exists locally but whose upstream source is not yet verified. These entries are reported and skipped during sync until you confirm their origin.

## Current Source Rules

- All skills imported from `openai/skills` curated catalog on 2026-03-10 are tracked as `third_party`.
- Their source is recorded as `https://github.com/openai/skills/tree/main/skills/.curated/<skill-name>`.
- Skills matched to `antfu/skills`, `obra/superpowers`, `anthropics/skills`, `anthropics/claude-code`, `evgyur/find-skills`, `aiskillstore/marketplace`, `browser-use/browser-use`, `coreyhaines31/marketingskills`, `vercel-labs/agent-browser`, `coleam00/excalidraw-diagram-skill`, and `remotion-dev/skills` are tracked as `third_party` with their confirmed source recorded in the registry.
- Repository-local custom skills confirmed by the user are tracked as `first_party`.

## Current Totals

- `third_party`: 77
- `first_party`: 10
- `unknown`: 0

## Current First-Party Skills

- `codebase-explorer`
- `copy-optimizer`
- `create-nano-banana`
- `dev-log`
- `excalidraw-animated-video`
- `fund-portfolio-analyzer`
- `git-commit`
- `macos-battery-diagnosis`
- `tech-plan`
- `viral-tech-copywriter`

## Syncability Notes

- Entries with `sync_method=github-path` can be updated directly by the root sync script.
- The sync script also respects an optional `source_ref` field in the registry for repositories that do not use `main` as their default branch, such as `evgyur/find-skills` on `master`.
- `first_party` entries are always reported and never overwritten.

## Usage

Report current status:

```bash
python3 /Users/yepeng/.agents/skills/sync-third-party-skills.py --check
```

Report one skill:

```bash
python3 /Users/yepeng/.agents/skills/sync-third-party-skills.py --check --skill imagegen
```

Sync all verified third-party skills:

```bash
python3 /Users/yepeng/.agents/skills/sync-third-party-skills.py --sync
```

Sync one verified third-party skill:

```bash
python3 /Users/yepeng/.agents/skills/sync-third-party-skills.py --sync --skill imagegen
```

## Sync Behavior

When `--sync` is used, the script:

1. reads `skills-registry.json`
2. selects entries marked `third_party`
3. downloads a fresh copy into a temporary directory with the existing `skill-installer` helper
4. verifies the staged skill contains `SKILL.md`
5. replaces the on-disk skill directory with the staged copy

`unknown` and `first_party` entries are intentionally skipped to avoid overwriting local or unresolved skills.
