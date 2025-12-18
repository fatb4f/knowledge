# Fish vi-mode Drills

Concise drills covering the highest-frequency flows in insert, normal, and visual modes. Designed for daily practice.

---

## 1. Insert Mode Drills
Focus: typing, quick correction, stack actions.

### I1 — Typing + Fixing Errors
1. Type: `echo Hellp world` (don’t press Enter).
2. Use Left/Right to reach the typo and correct to `Hello`.
3. Press Enter.
4. Repeat with misspellings of `Documents`.

### I2 — Stack Chords: Ctrl-f / Ctrl-r / Ctrl-p
1. Start typing any partial command (don’t run).
2. Press Ctrl-f → directory search (fzf UI).
3. Press Ctrl-r → history search.
4. Press Ctrl-p → zoxide project jump.
5. Repeat until all three are reflexes.

---

## 2. Normal (Default) Mode Drills
Enter with Esc. Focus: history, movement, edits.

### N1 — History with j/k
1. Press Esc.
2. Press j repeatedly → older history.
3. Press k → newer history.
4. Press Enter to run the chosen entry.

### N2 — Movement: 0, $, w, b, dw
1. Recall a long command via Esc → j.
2. Practice:
   - 0 → start of line.
   - $ → end of line.
   - w / b → move word-wise.
3. Delete a word:
   - Move to target.
   - dw → delete word.
   - Press Enter.

### N3 — Stack Actions in Normal Mode
1. Ensure normal mode (Esc).
2. Ctrl-f → directory search.
3. Ctrl-r → history search.
4. Ctrl-p → project jump.
5. Drill until mode is irrelevant: same muscle memory in insert + normal.

---

## 3. Visual Mode Drills
Useful for correcting long commands or reorganizing paths.

### V1 — Select + Replace
1. Recall a sentence-like command: `echo "The quick brown fox jumps..."`.
2. Esc, navigate with 0 + w to the word brown.
3. Press v → start selection.
4. Use w w to select `brown fox`.
5. Press c → change selection.
6. Type replacement, e.g. `red cat`.
7. Enter.

### V2 — Yank + Paste
1. Recall a long path command.
2. Esc, move to the segment you want.
3. v then w w to enlarge selection.
4. Press y → yank.
5. Move to another location ($, b, etc.).
6. Press p → paste.
7. Edit and run.

---

## Summary Table

| Mode   | Primary Actions                | Key Skills                  |
|--------|---------------------------------|------------------------------|
| Insert | Typing, corrections, stack use | Ctrl-f, Ctrl-r, Ctrl-p       |
| Normal | History, movement, edits       | j/k, 0/$, w/b, dw            |
| Visual | Select + modify                | v, w, y, p, c                |

