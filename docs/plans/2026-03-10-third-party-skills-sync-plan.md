# Third-Party Skills Sync Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a root-level registry, sync script, and documentation for tracking and updating third-party skills in this repository.

**Architecture:** Keep all management artifacts at the repository root so operational files do not mix with skill directories. Drive synchronization from an explicit registry that records ownership and upstream metadata per skill, then use a root-level Python script to validate and update only third-party entries.

**Tech Stack:** Python 3, JSON, Markdown, existing `skill-installer` helper script

---

### Task 1: Add the registry model

**Files:**
- Create: `skills-registry.json`

**Step 1: Define the registry schema**

Include top-level metadata plus a list of entries. Each entry should record:
- `name`
- `ownership`
- `source_type`
- `source_repo`
- `source_path`
- `source_url`
- `sync_method`
- `status`
- `notes`

**Step 2: Seed verified third-party entries**

Add all curated OpenAI skills installed on 2026-03-10 with `ownership=third_party` and GitHub source metadata.

**Step 3: Seed unresolved legacy entries**

Add all pre-existing local skills with `ownership=unknown` and `sync_method=manual-review`.

**Step 4: Validate completeness**

Run a verification command that compares registry names to on-disk `SKILL.md` directories.

### Task 2: Add the sync script

**Files:**
- Create: `sync-third-party-skills.py`

**Step 1: Implement registry loading and validation**

Require the registry file to exist and verify each entry has the minimum keys needed for reporting.

**Step 2: Implement reporting mode**

Print each tracked skill with ownership, source, and local presence. Report totals for `third_party`, `first_party`, and `unknown`.

**Step 3: Implement sync mode**

For `third_party` entries with `source_type=github`, install into a temporary directory using the existing helper:

```bash
python3 /Users/yepeng/.agents/skills/skill-installer/scripts/install-skill-from-github.py \
  --repo <source_repo> \
  --path <source_path> \
  --dest <tmpdir> \
  --name <name>
```

Then replace the target skill directory only after the fresh install succeeds and contains `SKILL.md`.

**Step 4: Support targeted sync**

Allow `--skill <name>` to narrow reporting or synchronization to one or more entries.

### Task 3: Add root-level documentation

**Files:**
- Create: `THIRD_PARTY_SKILLS.md`

**Step 1: Document file placement**

Explain that the registry, sync script, and documentation live at the repository root by design.

**Step 2: Document the ownership model**

Describe `first_party`, `third_party`, and `unknown`, plus how unresolved skills are handled until manually confirmed.

**Step 3: Document usage**

Include commands for:
- reporting current status
- syncing all third-party skills
- syncing a single skill

### Task 4: Verify behavior

**Files:**
- Test: `skills-registry.json`
- Test: `sync-third-party-skills.py`

**Step 1: Verify registry coverage**

Run a command that checks every local `SKILL.md` directory has a matching registry entry.

**Step 2: Verify reporting mode**

Run:

```bash
python3 /Users/yepeng/.agents/skills/sync-third-party-skills.py --check
```

Expected: summary totals plus per-skill rows without errors.

**Step 3: Verify targeted reporting**

Run:

```bash
python3 /Users/yepeng/.agents/skills/sync-third-party-skills.py --check --skill imagegen
```

Expected: only the requested skill is listed.
