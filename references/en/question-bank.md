[简体中文](../question-bank.md)

# Question and Hint Bank

Read code and available material first; there is no fixed questionnaire or hidden “full-score answer.” **If current scores, detailed results, or rules are missing, actually send the intake question to the user** rather than keeping it as an internal prompt. Continue independent source inspection and evaluation preparation while awaiting the answer. Other research questions are internal prompts in autonomous mode: the agent investigates, implements, and evaluates instead of waiting for user answers each round. The guidance for stuck learners, progressive hints, and waiting below applies only to explicitly selected interactive mode; choose the one or two most informative questions there.

## Information to obtain at takeover

First read the actual solver, latest and historical best results with corresponding versions, component/per-case scores, and the current benchmark's rules and runtime limits. If the material is complete, assess the current solver and proceed to the next optimization without asking the user to repeat it.

Ask directly for only the missing parts of this request:

> Please provide the actual scores and versions for the current and historical best solver, component or per-case results, and this benchmark's scoring rules and runtime limits. Existing evaluation files or reports are welcome.

Unless the user specifies another objective, state “I will continue toward 100% / full marks on this benchmark.” **Do not ask which target they want or whether pursuing full marks is worthwhile.** If the rules define no full score, ask only how the evaluation defines the best result; do not silently turn completion rate into a scoring percentage. Respect requests limited to a specific repair or learning task.

The internal takeover assessment should answer what planning and coordination capabilities the code actually has, where the gap lies, and whether it calls for an architecture upgrade or improvement of an existing strong solver. For example, a simple implementation lacking joint coordination with many mutually blocked agents warrants a substantially stronger combined candidate; a mature near-full-score solver warrants targeted trials on the remaining loss. Neither algorithm names nor the total score alone establish this judgment.

## Goals and benchmarks

**Use when:** Checking the scoring meaning of the default full-marks objective, explaining “Why did I not get a full score when everything finished?”, or examining someone else's results. These are rule-inspection or optional teaching prompts, not a request to choose the goal again.

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

If the user is stuck: For suspected execution errors, align planned positions, actual positions, available actions, and external events in a small example of their own. If execution is correct but quality is poor, inspect ordering, coordination, and candidate selection directly. Do not require a trace divergence before allowing an algorithmic upgrade.

## The interface between planning and execution

**Use when:** A plan appears conflict-free, but the actual run stops, misses scheduled times, or repeatedly needs repair.

Possible questions:

- “Do you return positions, actions, or a schedule? How does the executor consume them?”
- “Can the current interface actually express the waiting or departure behavior you assume?”
- “After a train reaches its target or a malfunction occurs, who updates the state next, and who replans?”

If the user is stuck: Choose a very short trajectory they create themselves, and ask them to explain each step: ‘current state → returned value → actual action → new state.’ Obtain answers from the interface and execution results of their version. Do not extrapolate from the behavior of another course or public repository.

## Experiments that distinguish explanations

**Use when:** Choosing parameter, algorithm-combination, or architecture-upgrade candidates and using bounded evaluation to determine the next step.

Possible questions:

- “Which genuinely different choices does this trial compare, and which scoring components could benefit or suffer?”
- “How can you change only the parts relevant to your hypothesis? If parts must change together, how will you interpret their interaction?”
- “What result would make you retain, revise, or reject this candidate, and which decision level could you explore next?”

If the user is stuck: Turn “I want to improve it” into a comparable choice, such as ordering diversity or joint-replanning scope, then select representative evaluation that can expose actual quality differences. A complete causal explanation may follow the results; bounded trial and error on the current benchmark is legitimate. Allow cooperating modules to be upgraded together without mandatory single-variable experiments or complete ablations. Do not default to a full parameter sweep.

## Starting points and scope of applicability

**Use when:** A new method works only on a weak initial solution, tuning always uses the same few maps, or a user wants to copy someone else's configuration directly.

Possible questions:

- “From what starting point was this gain obtained? Could the original system already produce this part of the improvement?”
- “Which cases influenced your choices? What independent samples could test this explanation?”
- “If the map distribution, speeds, malfunction mechanism, or information visible at decision time changed, which parts of your reasoning would still hold?”

If the user is stuck: Ask them to state the method's assumptions, then test benefits on current-benchmark cases withheld from selection or through available authoritative evaluation. Optimizing this benchmark is a valid goal; promotion does not require demonstrating generalization to other benchmarks. Bound conclusions to the evidence. When screening cases are reused for stability checks, label that purpose accurately.

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

Agent: “Was that cost recorded after generating the plan or after complete execution? Do your scoring rules use it directly?”

User: “Only after plan generation. Malfunctions can still occur during execution.”

Agent: “Then the evidence currently supports an improvement in the planning stage. How would you design a comparison to distinguish a benefit that survives execution from one canceled out by later disturbances?”

User: “Start from the same input, run to completion, and record both the results before and after the new step and the final result.”

Agent: “That separates several levels of the result. If both runs are time-limited, what else would you need to record to avoid attributing a difference in workload to the new step?”

This dialogue illustrates how to proceed gradually in response to the user's answers. It does not require the user to guess a designated algorithm, and it does not provide the source project's implementation.
