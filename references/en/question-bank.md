[简体中文](../question-bank.md)

# Question and Hint Bank

Select this coaching material according to the problem. It is not a fixed questionnaire, and there is no hidden “full-score answer.” Choose only the one or two questions that best distinguish the possibilities in the current round. First reduce the questions using information the user has already provided, then consider what to ask next.

## Goals and benchmarks

**Use when:** A user says “I want 100%,” asks “Why did I not get a full score when everything finished?”, or directly applies someone else's results.

Possible questions:

- “Which quantity does ‘100%’ refer to? How does it relate to all trains arriving, all trains arriving on time, and theoretical optimality?”
- “Can you find the part of your own evaluation rules that supports this interpretation?”
- “If one strategy runs faster but produces more late arrivals, how would you choose? Would the evaluator make the same choice?”

If the user is stuck: First ask them to separate the primary metric from conditions that must not be violated. If needed, use a fictional example: all three trains arrive, but one is late. Which facts does this directly establish? Do not insert a scoring formula from the source project.

## Observations and mechanisms

**Use when:** The only evidence is an overall score, a screenshot of one failure, or a broad judgment such as “I think it is congestion.”

Possible questions:

- “At what point did the actual behavior first differ from your expectation?”
- “What else could produce the same observation? What would you need to record to distinguish the explanations?”
- “If your proposed cause were absent, where should this trajectory differ?”

If the user is stuck: Suggest aligning planned positions, actual positions, available actions, and external events in a small example of their own. Locate the first divergence before suggesting a replacement for the overall algorithm.

## The interface between planning and execution

**Use when:** A plan appears conflict-free, but the actual run stops, misses scheduled times, or repeatedly needs repair.

Possible questions:

- “Do you return positions, actions, or a schedule? How does the executor consume them?”
- “Can the current interface actually express the waiting or departure behavior you assume?”
- “After a train reaches its target or a malfunction occurs, who updates the state next, and who replans?”

If the user is stuck: Choose a very short trajectory they create themselves, and ask them to explain each step: ‘current state → returned value → actual action → new state.’ Obtain answers from the interface and execution results of their version. Do not extrapolate from the behavior of another course or public repository.

## Experiments that distinguish explanations

**Use when:** A user plans to change several parameters or replace multiple modules at once, or keeps adding random attempts.

Possible questions:

- “What question should this experiment answer? What result does each of two reasonable explanations predict?”
- “How can you change only the parts relevant to your hypothesis? If parts must change together, how will you interpret their interaction?”
- “What result would make you stop pursuing this approach?”

If the user is stuck: First rewrite “I want to improve it” as a specific causal claim, then choose a small experiment capable of refuting it. Allow justified combined experiments; do not turn the advice to change one variable at a time into an absolute prohibition.

## Starting points and generalization

**Use when:** A new method works only on a weak initial solution, tuning always uses the same few maps, or a user wants to copy someone else's configuration directly.

Possible questions:

- “From what starting point was this gain obtained? Could the original system already produce this part of the improvement?”
- “Which cases influenced your choices? What independent samples could test this explanation?”
- “If the map distribution, speeds, malfunction mechanism, or information visible at decision time changed, which parts of your reasoning would still hold?”

If the user is stuck: Ask them to write down the method's assumptions, then choose a small, controllable change that tests one of them. Define the scope of the conclusion first. Do not treat success on a few cases as applicable to all Flatland environments.

## Time and workload

**Use when:** “It is faster” conflicts with total runtime, a larger budget brings no benefit, or two runs disagree.

Possible questions:

- “Are you comparing runtime for the same workload, or result quality under the same time budget?”
- “Which stage takes most of the time? Does the configured budget match the work actually completed?”
- “How did resources, caches, or random states differ between the runs? How could you control the most suspicious difference?”

If the user is stuck: First suggest recording stage start and end times, actual workload, and exit reasons. Ask them to predict whether a controlled change will affect time, quality, or both, instead of giving budget values directly.

## Interpreting results and choosing the next step

**Use when:** A user has experimental results but is unsure whether to retain an approach, reject it, or continue.

Possible questions:

- “Which statement of yours does this evidence support? Which statement remains untested?”
- “Were any failed or timed-out samples excluded from the summary? Does the improvement come with a significant cost?”
- “How could the next experiment reduce uncertainty more than simply repeating this round?”

If the user is stuck: Put changes within a stage of one run, differences across runs, complete execution results, and actual scores in separate columns. If needed, use the entirely fictional dialogue below to help explain. Do not treat any numbers as suggested parameters.

## A fictional example of follow-up questions

User: “I added a step that lowers the plan cost, so the final score must be higher.”

Coach: “Was that cost recorded after generating the plan or after complete execution? Do your scoring rules use it directly?”

User: “Only after plan generation. Malfunctions can still occur during execution.”

Coach: “Then the evidence currently supports an improvement in the planning stage. How would you design a comparison to distinguish a benefit that survives execution from one canceled out by later disturbances?”

User: “Start from the same input, run to completion, and record both the results before and after the new step and the final result.”

Coach: “That separates several levels of the result. If both runs are time-limited, what else would you need to record to avoid attributing a difference in workload to the new step?”

This dialogue illustrates how to proceed gradually in response to the user's answers. It does not require the user to guess a designated algorithm, and it does not provide the source project's implementation.
