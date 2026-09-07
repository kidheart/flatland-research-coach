[简体中文](../experiment-card.md)

# The User's Own Experiment Card

Use this only once the conversation has produced a testable hypothesis. Reuse an existing experiment tracking system if one is available; do not require an extra form. A short experiment may need only a few lines.

## Before the experiment: let the user explain first

```text
The phenomenon I want to explain:
Conditions in my environment and evaluation relevant to this question:
My current explanation:
Another possible cause of the same phenomenon:
What I will change and what I will hold fixed:
What I expect to observe if each explanation is correct:
Results that would make me abandon or revise my current explanation:
The time and computing cost I can afford:
```

The coach should add only omissions that affect the conclusion. Do not invent data, hypotheses, or implementation results for the user. If a causal hypothesis does not yet yield predictions that distinguish it from alternatives, narrow the question before running an expensive experiment. For fact checks or interface verification, simply state what the check can answer; there is no need to manufacture another explanation.

## After the experiment: separate facts from judgments

```text
Identifiers for the code/configuration and data actually tested:
Expected samples and samples actually completed; failures/timeouts:
Changes before and after the new step within the same run, if applicable:
Complete results and resource use across runs:
Changes in key constraints and secondary metrics:
Actual evaluation results (write "not obtained" if unavailable):
What the observations support and what they cannot prove:
Assumptions behind the conclusion; new evidence that would make me reconsider:
My choice of next step and the reason for it:
```

Do not substitute local checks for complete execution or automatically convert local results into server scores. When a gain is close to the observed variation, let the user choose a paired or repeated experiment that controls the main uncertainty. Reuse existing valid evidence when there are no new concerns.

## A short structure for the coach's feedback

“You observed …, which supports …; at present, we still cannot rule out …. What do you plan to observe to distinguish these explanations?”

When the evidence is sufficient, acknowledge the scope of the conclusion directly and move forward. Do not create an endless series of counterquestions. When the user requests a direct explanation, give a clear account, then invite them to apply the judgment to their own problem.

## When concluding a piece of research

Ask users to explain in their own words why the method works, which assumptions it depends on, which environments still lack evidence, and how they would recognize failure. Save their own reproducible version and results. Reaching the currently defined goal does not automatically establish a generally optimal solution for every Flatland task.

When sharing research experience, use only material the user has explicitly permitted to be shared. Fictional examples are sufficient to explain a method; there is no need for the source project's parameters, code, commit identifiers, or winning configuration.
