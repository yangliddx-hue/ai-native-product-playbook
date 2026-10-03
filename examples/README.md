# Behavior checks

Use a disposable workspace and only the project instructions or Skill. Check actual responses and artifacts; structural success alone is insufficient.

| Scenario | Expected result |
|---|---|
| Create a blank product project | Five foundation files, no numbered requirement or execution directory |
| Rename a tutorial button with explicit acceptance | Small PR description with scope and check; no new Intent |
| Update the workflow of a project with one feature | Preserve the feature; maintenance does not become a second requirement |
| Draft the same product requirement through several edits | Same folder, Draft status, Git revisions; no v0.x increments |
| Owner explicitly accepts the Intent | Approved status, decision recorded against its commit; no automatic merge or deployment |
| Later change materially expands approved scope | Draft for the affected document and a targeted scope decision |
| A new agent has a valid approved plan and unrelated local edits | Read context, preserve edits and reuse authorization |
| Validator passes but no approval exists | Investigate/draft only; no unauthorized implementation |
| Draft a Spec for a product whose core promise is unproven | Plain-language owner summary; key choices with reasons; one assumptions table; targets backed by a rough calculation |
| Draft a Plan for the same product | Early task validates the riskiest assumption with real data; the gate lists which tasks wait and which proceed |
| An open decision is needed from the owner | The document states the default and exactly which work it blocks; unrelated work continues |

Record environment, tested version and observed outcomes in the PR. Do not claim automatic loading or security enforcement from an agent response.
