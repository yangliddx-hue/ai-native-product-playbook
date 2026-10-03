---
name: initialize-ai-native-project
description: Initialize or adopt a minimal product workflow, or prepare a product Intent and optional design/plan. Preserve existing project rules and keep routine maintenance in the PR.
---

# Initialize an AI-native product project

Read existing project instructions, product documents and relevant PR first. Collect known facts; leave missing facts as `Unknown`.

```bash
python3 scripts/initialize_project.py TARGET --project-name "NAME" --owner "OWNER" --project-type "TYPE"
```

Use `--adopt-existing` for an existing project. The initializer preserves files and generates `.playbook-proposed` differences; reconcile them before continuing. It creates four foundation files, no feature folders or execution logs. It performs no remote actions.

Read the generated `docs/development-workflow.md` (or preserved `docs/workflow.md`). Follow its rules for naming, approval and handoff. New independent product requirements use descriptive folders such as `docs/intent/video-clipping/`; existing names stay stable. Workflow updates, document edits and ordinary fixes belong in the PR, not a newly numbered Intent.

Product positioning, users, value and scope belong in Intent; do not create a separate product.md. Carry relevant user-provided initialization details into Intent when drafting it.

Use `assets/project-starter/change/intent.md` when a requirement needs a document. Add `spec.md` and `plan.md` only when needed. Templates are optional. Every document must stand alone as the current result. Intent defines the product; Spec defines behavior and design; Plan defines execution; workflow and Skills define rules. Preserve useful rationale and unknowns, but keep chat history, revision narratives and superseded proposals out of these documents. Do not invent users, restrict a product to a sample domain, or expand scope from research suggestions.

Draft edits use Git, not `v0.x`. Explicit owner acceptance changes the document to Approved; record the decision and fixed commit in the PR, without implying merge or deployment authorization. Keep progress and evidence there as well.

Before drafting or revising an Intent, Spec or Plan, read `references/document-guide.md`. Before submitting documents, apply the adopted workflow’s review-ready document checks to the entire document, not only the edited paragraphs.

Run `python3 scripts/validate_project.py TARGET`. It checks structure only. Verify the actual changed behavior separately, then report changes, remaining proposals/unknowns and the next action. Do not install global Skills, overwrite local decisions or publish remotely unless authorized.
