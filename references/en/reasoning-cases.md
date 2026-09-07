[简体中文](../reasoning-cases.md)

# Anonymized Reasoning Cases: How Evidence Changed Judgments

These cases are distilled from a Flatland research experience. They retain qualitative observations and ways of reasoning while omitting algorithm configurations, code, parameters, and experimental details that could identify or reconstruct the final solution. They are organized by research difficulty, not by the original solution's module order or a required sequence of steps. Later success cannot validate an explanation that was still untested at the time.

These materials do not include raw experiments that can be independently checked, so they are not evidence for public performance comparisons or optimality. They are intended to suggest hypotheses. Users should design experiments in their own environments to test whether the judgments hold. There is a tradeoff between protecting implementation details and fully reproducing the original experiments. This skill preserves teaching value without claiming to provide both.

## A promising new method added little value

**Observation.** Some candidates substantially improved weaker initial results and passed local correctness checks. When added after a system that was already extensively optimized, however, they produced little additional gain.

**Explanations that needed to be distinguished.** A candidate might not have supplied a capability missing from the original system, instead repeating work the system could already do. Alternatively, its placement or the experimental resources might have been unsuitable. The results did not distinguish these possibilities, much less establish that the method was generally useless.

**How to test them.** Start the added process from the same complete baseline result and observe what it actually contributes. Separate its value for early convergence from its incremental value later on. If it might be suitable for replacing earlier work, formulate a separate replacement hypothesis. A gain from a weak starting point cannot be counted directly as a gain from appending the method at the end.

**The limited judgment reached.** Under the starting points, resources, and scope of observation used at the time, the evidence did not support further investment in those candidates as additional stages. This was a research tradeoff, not a theoretical rejection.

**When to reconsider.** A user with a different baseline, different resource constraints, or evidence that the method supplies a capability missing from the current system can test it again.

**Ask the user.** “Is your candidate repairing a weak starting point, or adding a capability the complete system does not yet have? What comparison could distinguish these two kinds of value?”

## Why did a better internal metric not lead to a better actual evaluation?

**Observation.** In historical comparisons, the ordering given by an internal aggregate measure did not always agree with the ordering given by actual scores.

**Explanations that needed to be distinguished.** Possible causes included aggregation or normalization, the distribution of cases, differences between execution and scoring, or records from different versions being mixed together. Observing a disagreement in rankings did not establish the specific scoring formula.

**How to test them.** Bind each result to its version and evaluation conditions, and inspect changes by instance and the conditions under which scores are assigned. Record internal plans, complete execution, and actual evaluations separately. Verify rules directly where possible and leave unknown rules unresolved.

**The limited judgment reached.** The final version could not be selected solely by an internal measure that was convenient to aggregate. The observed disagreements supported this judgment, but did not establish any unverified mechanism as the sole cause.

**Scope.** If the user's actual objective is that aggregate measure and scoring is consistent with execution, the measure can of course serve as the primary metric. The experience does not imply that all proxies are unreliable.

**Ask the user.** “In the relationship between the quantity you compare and the quantity the task actually evaluates, which links have been verified, and which are still assumptions?”

## If the program became faster, can all the final improvement be credited to the new idea?

**Observation.** Implementation changes for performance could preserve results and relevant state while reducing runtime in the tested comparisons with a fixed workload. In complete runs with a time limit, workload and final results could then change as well.

**Explanations that needed to be distinguished.** The final improvement might have come from completing more work in the same time, changes in decision behavior, or variations in machine state. Unchanged code in one part of the system does not guarantee that different runs with time limits follow exactly the same process.

**How to test them.** Use a fixed workload to check behavior and throughput, then use comparable resource conditions to check the actual task benefit. Record results before and after the added process within the same run, so differences across runs are not all attributed to one change.

**The limited judgment reached.** The tested comparisons could support an efficiency claim within a specific scope. A local runtime change could not be converted directly into a change in total runtime or score. Agreement in a limited set of tests was also not a formal proof of equivalence for every input.

**Scope.** A user with a verifiable proof of strict equivalence may draw a stronger conclusion than these tests support. If their system does not use a wall-clock time limit, the main confounding factors may also differ.

**Ask the user.** “Do you want to show that the same work requires less computation, or that the same resources produce a better result? Which question do your existing experiments actually answer?”

## What has been established after the target is met?

**Observation.** The research eventually produced a result accepted by the target evaluation. It did not exhaust all algorithms, configurations, or environments, and it did not provide a proof of global optimality.

**Leaps to avoid.** Reaching a defined goal does not mean that every decision along the way was necessary. Lacking an optimality proof does not mean that all observations and experiments were worthless.

**A reasonable conclusion.** Make bounded claims about the successful version and verified conditions, while retaining failed attempts, alternatives that were not compared, and unresolved questions. The user's goals and tradeoffs in effort can justify stopping optimization without pretending that a theoretical limit has been reached.

**Ask the user.** “Which of your conclusions are already supported by evidence? Which assumptions would need to be checked again in another Flatland environment? What additional evidence would let you generalize one of those conclusions?”

## Using the cases appropriately in teaching

Each case helps users see how an observation changes a judgment and where that judgment may fail. Do not turn the absence of an observed gain into a claim that gains are impossible. Do not turn the order of the narrative into a recommended architecture.

When users propose different explanations, help design experiments that compare them. Update conclusions when contrary evidence appears; do not ignore evidence to defend the original author's method. Additional teaching cases should also retain observations, competing explanations, experiments that distinguish them, limited conclusions, and conditions for revisiting the judgment. Check whether multiple cases, taken together, could expose the original solution's distinctive combination of components.
