# Writing review-ready Intent, Spec and Plan

Read this before drafting or revising any of the three documents. It expands the workflow's review-ready checks with the reasons behind them and examples of failures seen in real projects. The workflow remains the rule; this guide explains how to meet it.

## Who the documents are for

The product owner approves these documents and is often not an engineer. A document the owner cannot follow gets approved without being understood, which defeats the approval. Implementers are the second audience: they need precision, but they can find it in later sections and appendices.

Write the owner summary last, after the body is stable, and check that it alone lets the owner judge whether the direction is right. Avoid jargon; when a term is unavoidable, explain it in one sentence where it first appears or in a short glossary.

## Shared failure patterns

| Pattern | What it looks like | Fix |
|---|---|---|
| Unreadable for the owner | Dense sections, undefined abbreviations, several rules per sentence | Owner summary, glossary, one idea per paragraph; move engineering depth to an appendix |
| Scattered disclaimers | “Not a commitment”, “not verified”, “we do not claim” repeated throughout | One assumptions table: assumption / how and when verified / what changes if it fails |
| Rules without reasons | Long lists of constraints with no explanation | One sentence per key choice: why, and what it gives up |
| Numbers that cannot be met | Every expensive call runs one at a time while the target demands the whole job finish quickly | Rough-calculate each time, cost or capacity target against the design; fix the design or the target |
| Two dependency models | Scheduling says two steps are independent while caching says one invalidates the other | One dependency model used by flows, scheduling, caching and task order |
| Unverified platform claims | Requiring a header that the browser never sends for that request type | Label platform, model and third-party claims as verified or inferred; verify the ones the design depends on |
| Invented external figures | Vendor prices or rate limits written from memory as if confirmed | Cite source and date, or mark as an estimate; recheck before targets depend on them |
| Duplicated decision lists | The same owner decisions listed in both Intent and Spec, drifting apart | Owner decisions live in the Intent; the Spec links to them |
| Capacity mistaken for quality | “All input fits in one request” taken as proof that nothing will be missed | Treat capacity as a precondition only; choose defaults by measuring outcomes |
| Trusting a model's self-report | “The model says it found everything” used as completeness | Compute completeness in code or confirm it with people |
| Decisions that seem to block everything | “Nothing can proceed until the vendor is chosen” when only one task needs it | For every open decision, list what it blocks and what can proceed |
| Scope creep by stage | A single-user pilot carries multi-tenant security, migration frameworks and memory watchdogs | Split protections into “must guarantee now” and “before wider release” |
| Private details in the repository | Internal endpoints, model identifiers or keys in documents or commits | Keep them in configuration outside the repository; documents name the keys. Removing them later does not remove them from Git or PR history |

## Intent

The Intent says why the product exists and how success is judged. It does not choose technology.

- State the **core value assumption**: what must be true for the product to be worth building, such as “the system can find usable segments in real long videos at acceptable cost”. The Spec and Plan must test it early.
- Make acceptance **measurable** and name who judges it. Mark criteria that need human judgment; tests and AI self-assessment cannot stand in for them.
- List the decisions only the owner can make—data permissions, budget, samples, release audience—with a default proposal and the stage each one blocks.

## Spec

The Spec says how the system behaves and how correctness is judged.

- The owner summary explains the method in plain terms: what happens, in what order, and why that order makes results trustworthy.
- Give each key choice one sentence of rationale and the alternative it rejects.
- Keep identifiers, enums and state machines consistent. Every state should have a path to cancellation or deletion where users can cancel or delete.
- Put acceptance next to the calculation that shows it is reachable.
- Collect remaining decisions and assumptions in one section, each with its blocking scope and verification plan.
- Put deep engineering detail in an appendix, split into what the current stage must guarantee and what is deferred.

## Plan

The Plan says in what order the work is done and how each step is checked.

- **Riskiest assumption first.** Early work checks the core value assumption with real data before interfaces, storage and polish are built around it. A plan that validates the product's core promise only in its last milestone is a defect.
- **Explicit gates.** A gate names exactly which tasks wait for it and which proceed in parallel, so implementers do not stop all work while one check is pending.
- **Thin end-to-end path early.** Connect the simplest version of every stage before completing any stage in depth.
- **Stage-appropriate scope.** Task completion criteria include only what the current stage must guarantee.
- **Verification mapping.** Map each acceptance criterion to a check and mark checks that need a human.
- **Parallel work.** Note which tasks can run concurrently and which files each owner may change.

## Final check before review

- Can the owner read the summary in about ten minutes and decide?
- Does every target survive a rough calculation against the design?
- Is every open decision labeled with what it blocks?
- Is every assumption in one table with a verification plan?
- Do the three documents use the same names, dependencies and scope?
- Are private access details absent from the documents, commits and PR text?
