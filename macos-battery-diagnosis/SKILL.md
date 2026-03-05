---
name: macos-battery-diagnosis
description: Diagnose macOS battery drain issues and identify power-hungry processes. Use this skill when the user asks about battery draining fast, finding power-consuming apps, why their Mac didn't sleep, or identifying processes that prevent sleep. Analyzes power assertions, sleep logs, and process resource usage.
---

# macOS Battery Drain Diagnosis

Diagnose why a Mac's battery drained unexpectedly, identifying processes that consume power or prevent system sleep.

## When to Use This Skill

User asks:
- "Why is my battery draining so fast?"
- "My Mac didn't sleep last night"
- "Find power-hungry processes"
- "What's eating my battery?"
- "Why didn't my Mac go to sleep?"
- "我的电脑没电了，帮我找原因"

## Diagnosis Workflow

### Step 1: Check Current Battery Status

```bash
pmset -g batt
```

**Output analysis:**
- Current charge percentage
- Power source (AC/Battery)
- Time remaining estimate
- Battery health status

### Step 2: Check Power Assertions (Critical)

Power assertions are the MOST IMPORTANT indicator - they show which processes are actively preventing sleep.

```bash
pmset -g assertions
```

**Key assertion types:**
- `PreventSystemSleep`: Blocks system from sleeping entirely
- `PreventUserIdleSystemSleep`: Prevents idle sleep
- `NoIdleSleepAssertion`: App requests no idle sleep
- `BackgroundTask`: Background operations running

**Look for:**
- Process names holding assertions
- Duration of assertions
- Assertion reasons (e.g., "Electron", "Playing audio")

### Step 3: Check Sleep/Wake History

```bash
pmset -g log | grep -E "(Sleep|Wake|Charge|Battery|Low Power)" | tail -50
```

**Timeline analysis:**
- When did the system enter sleep?
- Was it due to "Low Power Sleep"?
- How long was the system awake?
- Any unexpected wake events?

### Step 4: Check Preventing-Sleep Assertions History

```bash
pmset -g log | grep -E "NoIdleSleepAssertion|PreventUserIdleSystemSleep|PreventSystemSleep" | tail -30
```

**Identify:**
- Which app held sleep-preventing assertions
- How long the assertions were held
- Patterns of repeated assertions

### Step 5: Check High CPU Processes

```bash
ps aux | head -20
```

**Look for:**
- Processes with high CPU percentage (>10%)
- Known power-hungry app types:
  - Electron apps (typically show "Helper (Renderer)")
  - Virtual machines (Docker, VMs)
  - Video encoding/rendering
  - Games

### Step 6: Identify the Culprit

Cross-reference findings:

| Evidence Type | What It Tells You |
|--------------|-------------------|
| Power Assertions | Which app prevented sleep |
| Assertion Duration | How long sleep was blocked |
| Sleep Log | When battery died |
| CPU Usage | Active power consumers |

## Common Culprits

### 1. Electron Apps
Electron apps frequently prevent sleep because:
- Playing audio/video in background
- Active downloads
- Notification polling
- Poor app design

**Examples:** Slack, Discord, VS Code, Notion, ChatGPT app, custom Electron apps

**Identification:**
- Assertion name often shows "Electron"
- Process names include "Helper (Renderer)"

### 2. Virtual Machines
- Docker Desktop
- Parallels
- VMware
- UTM

These always consume significant power and may prevent sleep.

### 3. Media Applications
- Spotify, Apple Music (playing audio)
- YouTube in browser
- Video players

### 4. Background Services
- Backup software (Time Machine, Carbon Copy Cloner)
- Cloud sync (Dropbox, OneDrive, iCloud)
- Download managers

## Output Format

Provide a structured diagnosis report:

```markdown
## 诊断结果

### 主要问题
<Identify the primary cause>

### 关键证据
1. **<App Name>** 阻止系统睡眠
   - 断言类型: <assertion type>
   - 持续时间: <duration>
   - 进程 ID: <PID>

### 电池耗尽时间线
- <timestamp>: <event description>

### 其他高耗能进程
| 应用 | CPU 使用 | 说明 |
|------|---------|------|
| <app> | <cpu%> | <description> |

### 建议措施
1. <Action item 1>
2. <Action item 2>
```

## Advanced Diagnostics

### Check App Nap Status
```bash
defaults read NSGlobalDomain NSAppSleepDisabled
```

### Check Power Nap Settings
```bash
pmset -g custom
```

### Check Network Activity (for network-heavy apps)
```bash
nettop -P -L 1 -n -t tcp
```

### Check GPU Usage (for graphics-heavy apps)
```bash
sudo powermetrics --samplers gpu_power -i 1000 -n 1
```

## Prevention Tips

After diagnosis, provide actionable advice:

1. **Quit problematic apps** when not in use
2. **Check app settings** for "prevent sleep" options
3. **Use Activity Monitor** before closing laptop
4. **Disable Power Nap** in System Settings > Energy
5. **Check Login Items** for background apps

## Example Diagnosis

**User**: "我的电脑昨晚上没盒盖，今天没电了"

**Diagnosis flow**:
1. `pmset -g batt` - Battery at 7%
2. `pmset -g assertions` - Found "Some.app" holding `NoIdleSleepAssertion`
3. `pmset -g log` - Shows system entered "Low Power Sleep" at 00:57:56
4. `ps aux` - Shows Some.app process running

**Finding**: Some.app (Electron-based) held a sleep-preventing assertion for ~72 hours, preventing the system from sleeping and draining the battery.