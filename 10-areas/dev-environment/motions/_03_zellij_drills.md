# Zellij Mode and Motion Drills

Concise drills targeting the core interaction flows across **normal**, **pane**, **resize**, **tab**, **scroll**, and **search** modes. Aligned with the unified motion grammar.

---

## 1. Normal Mode Drills
Focus: navigation, switching panes, switching tabs.

### N1 — Pane Focus with Alt-h/j/k/l
1. Enter normal mode (Esc if needed).
2. Press Alt-h → move focus left.
3. Press Alt-l → move focus right.
4. Press Alt-j / Alt-k → move focus down/up.
5. Repeat in a grid layout until reflexive.

### N2 — Tab Switching via Alt-1..9
1. Open at least 3 tabs.
2. Normal mode.
3. Press Alt-1, Alt-2, Alt-3 in sequence.
4. Repeat backwards.

### N3 — Quick Exit from Any Mode
Drill: from any Zellij mode you are in, press Esc.
Goal: build muscle memory for mode-reset before acting.

---

## 2. Pane Mode Drills (Alt-p)
Focus: creating and manipulating panes.

### P1 — Create Panes in Four Directions
1. Enter pane mode: Alt-p.
2. Press h → new pane left.
3. Press l → new pane right.
4. Press j → new pane down.
5. Press k → new pane up.
6. Esc → return to normal.

### P2 — Split + Navigate
1. Alt-p → l (create pane right).
2. Esc.
3. Alt-h/l → move between panes.
4. Repeat with vertical splits.

---

## 3. Resize Mode Drills (Alt-r)
Focus: resizing panes with directional keystrokes.

### R1 — Resize Cycle
1. Enter resize mode: Alt-r.
2. Press h h h → shrink right pane.
3. Press l l l → expand right pane.
4. Press j / k to tune vertical sizes.
5. Esc → return to normal.

### R2 — Resize + Navigate
1. Alt-r → adjust pane.
2. Esc → Alt-h/l to check your spacing.
3. Repeat until spatial intuition is consistent.

---

## 4. Tab Mode Drills (Alt-t)
Focus: create, rename, close, reorder.

### T1 — Create + Navigate
1. Alt-t → n → new tab.
2. Alt-t → h/l → switch between tabs.
3. Esc.

### T2 — Close Tabs
1. Alt-t → x → close current.
2. Verify fallback to previous tab.

### T3 — Numeric Tab Access
1. Create 3 tabs.
2. Normal mode: Alt-1, Alt-2, Alt-3.
3. Build numeric recall.

---

## 5. Scroll Mode Drills (Alt-s)
Focus: scrollback exploration.

### S1 — Basic Scroll
1. Alt-s → enter scroll mode.
2. Use j / k → scroll lines.
3. Use u / d → half-page.
4. Use Alt-b / Alt-f → page up/down.
5. Esc → exit.

### S2 — Scroll + Context Check
1. Run a command producing long output.
2. Alt-s → navigate.
3. Esc → back to normal.

---

## 6. Search Mode Drills (inside Scroll)
Focus: searching terminal scrollback.

### H1 — Search Next/Prev
1. Alt-s → s → begin search.
2. Type term → Enter.
3. n → next match.
4. p → previous match.
5. Esc.

### H2 — Combined Flow
1. Alt-s → s → query.
2. n n n.
3. Alt-f → jump forward page.
4. Esc.

---

## 7. Autolock / Editor Integration Drills
Focus: switching between Zellij-managed and editor-managed modes.

### A1 — Enter Locked State
1. Open hx or nvim inside Zellij.
2. If autolock enabled, Zellij locks automatically.
3. Check: Alt-h/j/k/l should NOT move focus.

### A2 — Temporary Unlock
1. Press Alt-z.
2. Now Alt-h/j/k/l move focus again.

### A3 — Re-enable Autolock
1. Press Alt-Shift-z.
2. Confirm editor takes focus control again.

---

# Quick Motion Reference Table

## Pane Focus
| Action      | Keys        |
|-------------|-------------|
| Focus left  | Alt-h       |
| Focus right | Alt-l       |
| Focus down  | Alt-j       |
| Focus up    | Alt-k       |

---

## Pane Management
| Action              | Keys                |
|---------------------|----------------------|
| Enter pane mode     | Alt-p               |
| New pane left       | Alt-p → h           |
| New pane right      | Alt-p → l           |
| New pane down       | Alt-p → j           |
| New pane up         | Alt-p → k           |

---

## Resize
| Action       | Keys        |
|--------------|-------------|
| Enter resize | Alt-r       |
| Resize       | h/j/k/l     |

---

## Tabs
| Action               | Keys                  |
|----------------------|------------------------|
| Enter tab mode       | Alt-t                 |
| New tab              | Alt-t → n             |
| Close tab            | Alt-t → x             |
| Tab left/right       | Alt-t → h / Alt-t → l |
| Go to tab N          | Alt-1..9              |

---

## Scroll + Search
| Action                 | Keys                     |
|------------------------|---------------------------|
| Enter scroll mode      | Alt-s                    |
| Line scroll            | j / k                    |
| Half page              | u / d                    |
| Page up/down           | Alt-b / Alt-f            |
| Enter search           | s (inside scroll mode)   |
| Next / prev match      | n / p                    |

---

## Autolock / Editor Switching
| Action                   | Keys           |
|--------------------------|----------------|
| Temporary unlock         | Alt-z          |
| Enable autolock          | Alt-Shift-z    |
| Detect locked state      | Editor owns keys |

---

Daily use: run each section twice. Focus on reducing cognitive transitions between Zellij and editor modes.

