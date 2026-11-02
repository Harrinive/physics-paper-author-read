---
name: physics-paper-author-read
description: >-
  Responds to a physics author's own edits and margin comments: reads each change
  in its story, treats its guessed purpose as a ruling, accepts silently, and
  brings back only the decisions the author must make. Sweeps a recurring pattern
  across the paper with a verdict for every occurrence. Use when an author has
  edited a paper or left comments in it and asks for a review of those changes.
  Language goes through physics-paper-editing or physics-paper-editing-section.
---

# Physics paper author read

Use when the author changes the text themselves: edits, or comments in the text.
The other editing skills start from text that an agent changes. Here the author's
changes are the input and the output is a short list of decisions. Canon is
**`physics-paper-principles`**. Every sentence the agent adds or changes goes through
**`physics-paper-editing`** (a passage of at most 12 sentences) or
**`physics-paper-editing-section`** (a longer passage or a section).

Project files override this skill where they differ: a workflow file, a rulings
file, a writing guide, a vocabulary registry.

## Input

The author's change as a diff: a commit the author made, or any other diff the author
points to. Review what the author marked as ready, not work in progress. The
project says how the author marks a comment in the text.

Before the first change, read the project's rulings file and writing guide.

**Uncommitted work of the author is not touched.** Look at the state of the files
first. Uncommitted changes that were there when the work started are the author's;
an edit that must reach such a file waits until the author has committed it.

## For each change

1. **Read the story first.** Read the whole paragraph, its neighbours, and every
   place that makes the same point: other sections, captions, and appendices.
2. **Guess the purpose and treat it as a ruling.** Infer what each edit or comment
   is for. Ask only when two readings lead to different edits and the difference
   matters. Take the spirit of the author's words, not only the letter.
3. **Accept silently.** An accepted change is not reported. A minor language repair
   that leaves the meaning, the flow, and the level of detail as they are is applied
   after review, without comment.
4. **Report only what needs the author.** A change is reported when:
   - it has to be reverted, or extended because the claim is not accurate without
     another clause;
   - it contradicts another place, a locked name, or a standing ruling;
   - it disrupts the story around it;
   - the agent disagrees, with its reason and one recommendation.
5. **Generalize a pattern.** When a change hints at an issue that may recur, sweep
   the paper (below).
6. **Review the language.** Every added or changed sentence, the author's included,
   takes the reviewed path. Before showing a reviewer's fix, reread it in its
   paragraph and drop it if the text already covers the point. A change to the
   author's wording in meaning, flow, or level of detail is shown before and after.

## Pattern sweep

An agent's "all clear" is not evidence. A sweep ends with a verdict for every
occurrence.

1. State the pattern as guessed.
2. List every occurrence with an identifier:
   `python3 scripts/check_sweep.py extract --pattern REGEX --out occurrences.tsv FILE...`.
3. Give every occurrence a verdict in a table with the columns `id`, `verdict`
   (`fix` or `keep`), and `reason`.
4. Check the table: `python3 scripts/check_sweep.py check occurrences.tsv verdicts.tsv`.
   It fails on a missing, unknown, or repeated identifier. A subagent's table goes
   through the same check.
5. For each `fix`, check that the change does not disrupt the story. Change it to
   `keep` where the fix would over-correct: the text or a caption already makes the
   point; the fix breaks a parallel, a topic chain, or an order chosen on purpose; it
   adds weight for a nit; the context differs.
6. Present what remains, each with its before and after. Nothing is applied before the
   author rules. Proposed wording is reviewed before it is shown; a long proposal is
   reviewed on a scratch copy of the file.

## The reply

- **One status line:** how many changes were accepted, and the files that hold the
  silent repairs.
- **A one-line list of the decisions,** then one decision per turn
  ([user-communication.md](../physics-paper-editing/user-communication.md)). Each
  gives the place, the author's text, the problem, and the proposed wording, already
  reviewed. A pattern adds its instances with before and after, and a count of the
  skipped instances, each with a one-line reason.
- Nothing else, beyond what a section round requires in a report. The accepted
  changes are not listed.

## After the rulings

- Apply wording as the author ruled it, review only what changed beyond that, then
  run the project's checks.
- **Do not commit or push** unless the author asks. Name the ruling behind each
  edited file in the reply.
- **Record what was ruled.** A decision about one object or claim goes into the
  project's rulings file, following
  [rulings-file.md](../physics-paper-editing-section/rulings-file.md). A general rule
  goes into the writing guide, and the places written under the old rule are
  audited.

## Related skills

- **physics-paper-principles** — drafting and review canon
- **physics-paper-editing** — reviewed language for a short passage
- **physics-paper-editing-section** — reviewed language for a long passage or a
  section

## Out of scope

- Editing text the author did not touch, beyond a ruled sweep
- Deciding science for the author
- Committing, pushing, or syncing the author's work unasked
