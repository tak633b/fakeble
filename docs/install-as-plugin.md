# Install Fakeble as a Claude Code plugin

This is an alternative to `./install.sh`. The plugin path installs the **seven skills**
and keeps them updatable through the marketplace mechanism, without copying files into
`~/.claude/skills/` by hand. The CLAUDE.md fragment and the anti-drift hook stay opt-in
(see below) — installing the plugin does **not** touch your `CLAUDE.md`.

## What the plugin ships

`.claude-plugin/plugin.json` exposes the seven skills that already live at the repo root:

| Skill | Purpose |
|---|---|
| `companion-state` | Maintain a curated state file so any future session catches up in one read |
| `catchup` | Low-token catch-up: state file first, primary sources only for the named gap |
| `hypothesis-ledger` | Keep evidence attributed to hypotheses during long investigations |
| `framing-library` | Bank named structural insights; re-apply deep judgments by classification |
| `self-calibration` | Counterfactual salience checks, variance probes, a mistake log |
| `bootstrap` | Day-zero interview that generates your first state file and framings |
| `escalation-queue` | Bank frontier-depth questions; distill answered ones into framings |

Nothing else in the repo (`claude-md/`, `hooks/`, `templates/`, `experiments/`, `docs/`)
is claimed by the plugin loader — those directories are not plugin-reserved names, so they
are ignored when the plugin is enabled.

## Install from a local clone

```bash
git clone https://github.com/tak633b/fakeble
```

Then, in Claude Code, add the clone as a local marketplace/plugin and enable it:

```
/plugin marketplace add /absolute/path/to/fakeble
/plugin install fakeble
```

(Or point `/plugin marketplace add` at the GitHub repo directly once it is published as a
marketplace.) Enabling the plugin registers the seven skills; disabling it removes them.
Skills are invoked the same way as any other Claude Code skill — by name, when their
`description` matches what you are doing.

## What the plugin deliberately does NOT do

- **It does not append `claude-md/fakeble.md` to your `CLAUDE.md`.** That fragment is the
  behavioral core (pre-response check, silence rule, same-turn state upsert). It changes
  global behavior on every turn, so it stays a *consented* append. Run `./install.sh` (it
  asks before touching `CLAUDE.md` and writes a `.bak-fakeble` backup) or paste it in
  yourself. Plugins have no mechanism to inject into `CLAUDE.md`, so this separation is
  enforced by the format, not just by convention.

- **It does not enable the anti-drift reinjection hook.** A Claude Code plugin is
  enabled or disabled as a whole — there is no per-hook toggle inside an enabled plugin.
  If the hook were bundled into the plugin's `hooks/hooks.json`, it would fire on *every*
  user prompt whenever the plugin (and thus the skills) is enabled. That contradicts the
  hook's design: it is off by default, because frontier models rarely need it and only
  benefit in very long sessions where the pre-response behavior starts to fade. So the
  hook stays an explicit, manual opt-in. To enable it, merge
  `hooks/reinjection/settings-snippet.json` into your `~/.claude/settings.json` and place
  the reminder text at `~/.claude/fakeble-reminder.md` (the snippet's `cat` command reads
  that path). This keeps "install the skills" and "turn on always-on reinjection" as two
  independent decisions.

## Schema source

The `.claude-plugin/plugin.json` schema was verified against the official Claude Code
plugins reference (https://code.claude.com/docs/en/plugins-reference) and cross-checked
against working local plugins under `~/.claude/plugins/marketplaces/` (`oh-my-claudecode`,
`andrej-karpathy-skills`, `agent-skills`, `context-mode`). Confirmed points: only
`plugin.json` lives inside `.claude-plugin/`; all component directories (`skills/`,
`hooks/`, `commands/`, `agents/`) live at the plugin root; skills are `<name>/SKILL.md`
directories; the `skills` field may be an explicit array of paths (used here) or omitted
to rely on auto-discovery of the root `skills/` directory.
