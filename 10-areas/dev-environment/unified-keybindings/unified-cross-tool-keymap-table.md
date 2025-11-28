---
type: reference
tool: unified-keybindings
tags:
  - keybindings
  - cross-tool
---

# Cross-Tool Equivalence Table

This reference aligns common actions across Helix, Zellij, Yazi, and Kitty.

## Movement and Focus

| Action       | Helix  | Zellij      | Yazi | Kitty |
|-------------|--------|-------------|------|-------|
| Up          | `k`    | `Alt-k`(*)  | `k`  | n/a   |
| Down        | `j`    | `Alt-j`(*)  | `j`  | n/a   |
| Left        | `h`    | `Alt-h`(*)  | `h`  | n/a   |
| Right       | `l`    | `Alt-l`(*)  | `l`  | n/a   |

(*) Once configured in your Zellij keymap.

## Search

| Action                | Helix | Zellij | Yazi  | Kitty           |
|-----------------------|-------|--------|-------|------------------|
| In-tool search        | `/`   | `/`    | `/`   | `Ctrl+Shift+F`   |
| External `rg` search  | cmd   | n/a    | `?`   | n/a              |

## Editor Integration from Yazi

| Action              | Yazi key | Effect                        |
|---------------------|----------|-------------------------------|
| Edit in Helix       | `e`      | `hx "$@"`                     |
| Edit in HX floating | `Ctrl-e` | Zellij floating pane with HX  |

## System Helpers

| Action        | Tool  | Binding / Description                 |
|--------------|-------|----------------------------------------|
| Copy paths   | Yazi  | `y` → `xclip` integration              |
| Open shell   | Yazi  | `!`                                   |
| LazyGit pane | Yazi  | `Ctrl-g` → Zellij floating LazyGit     |

---
