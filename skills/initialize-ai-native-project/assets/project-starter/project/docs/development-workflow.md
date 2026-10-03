# AI-native product workflow

## Core documents

- `docs/intent/<feature-name>/intent.md`: standalone product definition—positioning, users, problem, outcome, scope, non-goals, the core value assumption, measurable acceptance and open questions.
- `spec.md` in that folder: add only when behavior, data or acceptance need more design.
- `plan.md` in that folder: add only when implementation needs coordinated steps, dependencies, verification and recovery. It validates the riskiest assumption before building around it.

Use a descriptive feature name, such as `video-clipping`. One product requirement keeps one folder. Documentation edits, workflow maintenance and ordinary fixes do not create new requirements: describe them in a PR. Preserve existing names during adoption; do not renumber historical work.

Do not pre-create feature folders or separate execution, approval, verification or initialization logs. Write every document as a standalone current result: product scope, design, implementation steps or operating rules. Retain decision rationale, constraints and open questions; keep conversation history, revision narratives and superseded proposals out of the document. Git preserves revisions; the PR carries progress and evidence. Research is supporting evidence, not approved scope. Templates are optional; write directly from these minimum contents when the Skill is unavailable.

### Review-ready documents

All documents, including intent.md, spec.md and plan.md, must present a complete current design that a reader can understand and review without knowing the conversation.

Integrate decisions into the relevant sections and rewrite affected content coherently. Do not append conversation summaries, revision narratives, intermediate experiments, discarded designs, temporary drafting notes or execution logs. Retain only the goals, scope, behavior, necessary boundaries and rationale that explain the current proposal. Clearly separate unresolved decisions without inventing approval.

Before submission, reread the whole document: does it present one consistent design without requiring the reader to assemble scattered amendments? For example, write “The product supports automatic discovery and request-based selection,” not “We initially considered automatic discovery, then added request-based selection after discussion.” Keep history and execution evidence in Git and the PR.

Every Intent, Spec and Plan also passes these checks. The owner approves these documents, so an owner who cannot follow them cannot meaningfully approve them.

1. **Owner summary first.** Open with a short plain-language summary a non-technical owner can read in about ten minutes: the approach, the user-visible result, key trade-offs and the biggest unknown. Explain unavoidable terms where they first appear or in a short glossary.
2. **Reasons, not only rules.** State why each key choice was made and what it gives up, in a sentence.
3. **One assumptions table.** The Intent names the core value assumption; the Spec (or the Intent when there is no Spec) collects unverified assumptions in one table: assumption / how and when it is verified / what changes if it fails; the Plan schedules those checks. Do not scatter disclaimers through the text or repeat the table in each document.
4. **Decisions say what they block.** For each open decision, state which work it blocks and which work can proceed without it. Owner decisions (permissions, budget, samples, audience) live in the Intent; the Spec lists only open design decisions and links to the Intent instead of repeating it.
5. **Numbers must agree.** Check targets such as time, cost and capacity against the design with a rough calculation; a target the design cannot reach is a defect.
6. **One vocabulary, one dependency model.** Use one name and one set of values per concept; keep flows, dependencies and state models consistent within and across the three documents.
7. **Mark verified versus inferred.** Claims about external platforms, models or third-party behavior, and external figures such as prices or limits, end with “(verified: source, date)” or “(estimate)”. Never present an invented figure as fact. Capacity or a model's self-report is not evidence of quality; decide important defaults by measurement.
8. **Depth matches the stage.** Keep what the current stage must guarantee in the main text; move deeper engineering detail to an appendix and mark protections deferred to later stages.
9. **No private access details.** Endpoints, credentials and internal identifiers live in configuration outside the repository; documents name the configuration keys.

See the Skill's `references/document-guide.md` for fuller guidance and examples when it is available.

## Revisions and approval

Use Git commits for revisions, not manually incremented draft versions. A feature name identifies the requirement; a commit identifies its exact contents.

Put `Status: Draft` or `Status: Approved` at the top of Intent and Spec. Mark Approved only after the responsible person explicitly accepts that document in chat or a review. Record the person, date, decision summary, scope and approved commit in the PR. Approval can precede merge. Tests, AI review and silence do not confer approval.

Approved Intent may leave explicit design parameters for the Spec. It does not mean implemented, merged or deployed. Wording-only edits retain approval; changed scope, acceptance, data permissions or material risk return the affected document to Draft and require a decision on that change. Reuse all unaffected authorization.

## Work and handoff

Read this workflow, relevant Intent/Spec/Plan documents and PR, then inspect the actual checkout and outstanding edits. Do not guess missing facts or approvals. Preserve unknowns and other people's changes.

Proceed from accepted Intent to any necessary Spec and Plan, then implement within authorized scope. Before implementation, have sufficient design, acceptance, steps and authorization; a small PR may contain them together. Merge, deployment, spending, external publication and production-data changes require applicable authorization.

Maintain one current progress record in the PR description: decisions and input commits; done/remaining work; checkout and uncommitted changes; checks and tested version; blockers and next step. Before a PR exists, use an existing Plan's task list or the existing task/issue record; do not create a Markdown execution log or a PR without authorization just to satisfy a template.

For delegation, pass the relevant paths, fixed baseline, assigned files, dependencies, authorization and acceptance. One coordinator integrates results. The receiver checks those inputs against the checkout; handoff does not require a new feature or repeated approval. If a PR or required context is inaccessible, continue only work independent of the missing information.

## Verification

Use checks appropriate to the change and record actual results against the tested commit. After relevant changes, rerun affected checks. Report implementation, verification and delivery separately. Do not claim unrun tests, deployed controls or released products.

The structural validator checks files and proposals, not approval, completeness or evidence truth. Instructions do not themselves enforce permissions.

## Sources

Inspired by Claude Academy's AI-Native SDLC Playbook. File layout, Git-based revisions and PR handoff are local conventions.
