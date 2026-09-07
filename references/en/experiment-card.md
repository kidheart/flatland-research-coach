[简体中文](../experiment-card.md)

# The User's Own Experiment Card

Reuse an existing tracking system rather than creating extra forms. Default small changes and short smoke checks need only the brief record below. Use the longer card that follows as needed for mechanism or performance research with a testable hypothesis; neither the long card nor a full evaluation is required each round. In autonomous mode, the agent fills in and updates the card. In interactive mode, invite the user to explain first. First-person statements refer to the person or agent making the judgment; do not attribute agent-generated opinions to the user.

## Default short record

```text
Change and actual version:
Relevant checks / reused evidence → actual results, including failures or timeouts:
Acceptance decision; best-version location; key claims still unconfirmed:
```

Passing a smoke check does not establish a performance gain; performance claims require relevant, comparable measurements. When retaining a candidate, also preserve the previously verified best version. A candidate with insufficient evidence does not automatically become the new best version. A budget is a ceiling, not a spending target. Expand checks or use the longer card only for a specific unresolved question whose result would change the next decision.

## Before the experiment: define the hypothesis and comparison

```text
The phenomenon I want to explain:
Conditions in my environment and evaluation relevant to this question:
Relevant case, if any; similar conditions, differences, and signs it does not apply:
Locations and evidence for the baseline and best verified version:
My current explanation:
Another possible cause of the same phenomenon:
What I will change and what I will hold fixed:
What I expect to observe if each explanation is correct:
Results that would make me abandon or revise my current explanation:
Candidate acceptance criteria and hard constraints that must not regress:
This round's budget and remaining total budget; stopping conditions:
```

In interactive mode, add only omissions that affect the conclusion. In autonomous mode, the agent proposes testable hypotheses and review findings. Neither mode may fabricate data, results, or statements by the user. If a causal hypothesis does not yet yield predictions that distinguish it from alternatives, narrow the question before an expensive experiment. For fact checks or interface verification, state what the check can answer without manufacturing another explanation.

## After the experiment: separate facts from judgments

```text
Identifiers for the code/configuration and data actually tested:
Expected samples and samples actually completed; failures/timeouts:
Changes before and after the new step within the same run, if applicable:
Results and resource use within the scope actually run:
Changes in key constraints and secondary metrics:
Actual evaluation results (write "not obtained" if unavailable):
What the observations support and what they cannot prove:
Assumptions behind the conclusion; new evidence that would make me reconsider:
Accept, reject, or pending confirmation; location of the retained best version:
My choice of next step and the reason for it:
```

Keep conclusions within the scope actually checked: local checks do not establish gains in full execution, and local results cannot automatically be converted into server scores. A gain close to observed variation may be marked "unconfirmed" without mandatory repetition. Choose a paired or repeated experiment only if resolving that uncertainty would change the next decision. In autonomous mode, run necessary experiments within the budget; in interactive mode, guide the user's choice. Reuse valid evidence when there are no new concerns; do not default to experiment matrices, full A/B evaluations, random-seed sweeps, or repeated baselines.

## A short feedback structure for interactive mode

“You observed …, which supports …; at present, we still cannot rule out …. What do you plan to observe to distinguish these explanations?”

When the evidence is sufficient, acknowledge the scope of the conclusion directly and move forward. Do not create an endless series of counterquestions. When the user requests a direct explanation, give a clear account, then invite them to apply the judgment to their own problem.

## When concluding a piece of research

Summarize why the method may work, its assumptions, environments still lacking evidence, and ways to recognize failure. In autonomous mode, the agent delivers this summary from the records; in interactive mode, invite the user to explain first. Save the user's own reproducible version and results. Reaching the defined goal does not establish a generally optimal solution for every Flatland task.

When sharing research experience, use only material the user has explicitly permitted to be shared. Fictional examples are sufficient to explain a method; there is no need for the source project's parameters, code, commit identifiers, or winning configuration.
