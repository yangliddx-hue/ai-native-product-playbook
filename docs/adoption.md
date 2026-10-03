# Adoption

The initialization Skill creates only:

```text
README.md
AGENTS.md
docs/development-workflow.md
.github/pull_request_template.md
```

Use `--adopt-existing` for an existing project. Files are preserved; differences become `.playbook-proposed` files for reconciliation. An existing `docs/workflow.md` is reused instead of creating a second workflow. If both workflow paths exist, resolve which is authoritative first. Historical Intent names and documents are not renamed or deleted by the script.

Feature folders are created only when a real product requirement needs one. Maintenance stays in the PR. The Skill's three templates are optional; projects can continue without installing the Skill.

Verify each client's instruction loading separately. Structure checks do not prove approval, agent behavior or permission enforcement. Use the [behavior scenarios](../examples/README.md) for changes to these rules. No remote changes, global installation or automatic controls are performed.
