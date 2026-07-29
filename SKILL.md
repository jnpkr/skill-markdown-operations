---
name: markdown-operations
description: Establish filesystem context and route Markdown file operations to standard or Obsidian-aware workflows. Use whenever creating, editing, renaming, moving, deleting, or reorganizing a Markdown (.md) file or note.
---

# Markdown Operations

Establish the filesystem context before operating on Markdown files.

## Workflow

1. Identify every target Markdown path. Establish the intended path before continuing when creating a new file.
2. For each target, run the detector from this skill directory:

   ```bash
   python3 scripts/detect_markdown_context.py "<target-path>"
   ```

3. Route each target from the detector output:
    - For `context=obsidian`, use `$obsidian-operations` for vault-aware operations and `$obsidian-markdown` for Obsidian-specific syntax.
    - For `context=standard-markdown`, use `$markdown-formatting`.
4. Complete the requested operation using the selected workflow. Handle targets with different contexts independently.

A successful classification returns:

```text
context=obsidian
vault_root=/absolute/vault/path
```

or:

```text
context=standard-markdown
vault_root=
```

A non-zero exit status means classification did not complete. Resolve the reported path or access error, then rerun the detector before selecting a workflow.
