# fzf Socket Listener: Real-World Use Cases (TWO-Oriented)

## 1. Global “Search Palette”
Run a persistent fzf daemon and send lists from any shell.
- Zero startup overhead.
- Behaves like a global command/search launcher.

## 2. Zellij: Shared Picker Across Panes
Multiple panes feed lists to one fzf viewer.
- Consistent UI across panes.
- Reduced cognitive switching and setup duplication.

## 3. Picker-as-a-Service for Scripts
Scripts outsource user-choice steps to the same fzf instance.
- Branch checkout, project opener, deployment helpers.

## 4. Global Quick-Switcher
Use persistent fzf state for switching sessions, windows, or contexts.
- Unifies Zellij sessions, Kitty windows, projects.

## 5. Continuous Feeds (Event Viewer)
Pipe live output streams into fzf.
- TODO scanners.
- journalctl viewers.
- Live ripgrep matches.

## 6. IDE-Like “Quick Open Everything”
Unify:
- Files.
- Symbols.
- ripgrep matches.
- Git grep results.
- Commit messages.

fzf becomes a terminal-native “Search Everywhere” interface.

## 7. Workflow Orchestration (TWO Input Layer)
fzf listener acts as the selector primitive.
- Producers: fd, rg, git, systemd, zoxide.
- TWO resolves selection and dispatches handlers.

## 8. Shared Preview Engine
One persistent fzf with unified preview config.
- Stable previews.
- No config drift.
- Reduced parameter switching.

## 9. Cross-Shell / Cross-TTY Picker
fzf instance is TTY-independent.
- Works across Kitty, Zellij, SSH.
- Functions as a system-level selector.

## 10. Low-Overhead Automation UI
fzf listener powers tiny UI layers for:
- systemd units
- Docker containers
- Git branches/tags/stashes
- Python venvs / Rust crates
- Kubernetes pods or Helm charts

## Strategic Note
Once search tools become cognition-native, upgrading to a structured `fzf-service` (persistent daemon + standard producers + TWO schema integration) becomes natural.

