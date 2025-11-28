---
type: dashboard
tags:
  - dataview
  - keybindings
---

# Unified Keybindings Dashboard

This dashboard lists all config-docs, workflows, motion grammar files, and related neuroprofile notes used in the unified keybinding system.

---

## Config Docs

```dataview
TABLE file.name AS "Config File", tool
FROM ""
WHERE type = "config-doc"
SORT file.name ASC
```

---

## Motion / Search Models

```dataview
TABLE file.name AS "Model", type
FROM ""
WHERE contains(tags, "motion") OR contains(tags, "search")
SORT file.name ASC
```

---

## Workflows

```dataview
TABLE file.name AS "Workflow"
FROM ""
WHERE contains(file.folder, "dev-environment/workflows")
SORT file.name ASC
```

---

## Neuroprofile Connections

```dataview
LIST file.name
FROM ""
WHERE contains(file.folder, "neuroprofile-toolkit/11.2.3-meta-cognitive-strategies")
SORT file.name
```
