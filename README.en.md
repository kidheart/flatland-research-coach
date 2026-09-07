[简体中文](README.md) | **English**

![Flatland Research Coach: from observations to testable judgments](assets/cover.svg)

# Flatland Research Coach

**Develop your own research judgment from your own evidence.**

An **agent-agnostic Markdown coaching skill** for experiments in **Flatland and railway multi-agent planning**. Through a few questions at a time, it helps you explain observations, form testable hypotheses, design controlled experiments, and state the conditions under which your conclusions hold. It includes anonymized reasoning cases, a question and hint bank, and an experiment card to use when helpful.

The general way to use it is to give an agent the Markdown instructions to read. You can use local files with an agent that supports file access, or upload or paste the text into a chat tool. Automatic discovery, installation, and persistence depend on the host platform; this repository does not assume every agent recognizes a skill format automatically.

This is a portable way to provide guidance, not a claim that every model or agent product has been tested. Actual behavior also depends on the host's context limits, file access, and available tools.

## When to use it

- You have results but cannot explain what caused an improvement.
- A plan looks reasonable, yet execution stalls, arrives late, or needs repeated repairs.
- A new method helps from a simple starting point but adds little to the complete system.
- Internal metrics, full execution results, and the final evaluation do not agree.
- You want to review a research effort: which judgments have evidence, which remain hypotheses, and whether another experiment is worth the investment.

Bring your own code, logs, evaluation rules, or a specific question. If you have no experiment materials yet, you can start with a clearly labeled fictional example. The coach uses the information you have already provided before asking one or two questions that matter most for the next step.

## How a round of reasoning works

**Observe → Distinguish explanations → Design an experiment → Interpret results → Update your judgment**

| Stage | What to clarify |
| --- | --- |
| Observe | What actually happened? Where did it first depart from your expectations? |
| Distinguish explanations | What different causes could produce this observation? What evidence would distinguish them? |
| Design an experiment | What will you change and hold fixed? What does each explanation predict? |
| Interpret results | Which claim does the evidence support? What remains possible? What did the change cost? |
| Update your judgment | Should you keep, revise, or abandon the explanation? Why is the next step worth taking? |

A round of discussion usually leaves you with an evidence-backed judgment, an open question, and an experiment whose purpose you can explain. Reuse existing records; a short experiment may need only a few lines. There is no need to complete a full form every time.

The depth of help adapts to your needs. When you are stuck, the coach narrows the question and offers progressive hints. If you ask for a direct explanation, analysis of your own code, or an authorized experiment, it can proceed directly.

### A fictional exchange

> **This is a fictional teaching example. It does not describe real experiment results or recommend parameter values.**
>
> **Learner:** I added a step and the plan cost went down, so the final evaluation should improve too.
>
> **Coach:** Was that cost recorded after planning or after full execution? Does your evaluation rule use it directly?
>
> **Learner:** Just after planning. Execution still has disruptions, and I have not checked the scoring rule yet.
>
> **Coach:** So far, the evidence supports an improvement at the planning stage. How would you test whether that benefit survives through execution?
>
> **Learner:** I would run a controlled comparison from the same inputs through to completion, recording the plans, execution results, and actual resource use separately. Then I would compare them using the verified evaluation rules.
>
> **Coach:** That helps separate the different stages. What result would make you revise your original judgment?

## Getting the files and loading the guidance

Chinese and English are two editions of the same skill. **Load the edition you prefer; no separate installation is needed for each language.** The repository includes both, and you can ask the coach to respond in the language you use in conversation.

### 1. Download to an ordinary folder

Choose a folder you can give your agent access to. This PowerShell example requires Git and downloads the repository into your home directory without changing any agent's global configuration. It stops if the destination already exists:

```powershell
$coachPath = Join-Path $HOME 'flatland-research-coach'

if (Test-Path -LiteralPath $coachPath) {
    throw 'The destination already exists. Check the existing folder before making changes; do not overwrite it.'
}

git clone https://github.com/kidheart/flatland-research-coach.git "$coachPath"

if ($LASTEXITCODE -ne 0) {
    throw 'Cloning did not complete. Check the Git output and destination directory before proceeding.'
}
```

You can also download the repository files from [GitHub](https://github.com/kidheart/flatland-research-coach) and keep them in an ordinary folder of your choice.

### 2. Give an agent the instructions

For an agent that can read local files, replace `<path-to-repository>` with the full path to your downloaded folder, then enter:

```text
Read <path-to-repository>/SKILL.en.md and follow its coaching guidance
for this conversation. Read relevant files under
<path-to-repository>/references/en/ when the current question calls for them.
Use the environment description and experiment records I provide,
then help me identify the most important uncertainty to investigate.
Respond in English.
```

If your chat tool cannot read local files, upload or paste the contents of `SKILL.en.md` and ask it to follow those instructions. Provide the relevant reference files as the discussion needs them. A filename or link inside pasted text does not mean the tool has read the linked document; supply its contents if the tool cannot retrieve it.

An agent needs access to the actual guidance to use it. Whether that guidance is automatically loaded again in another conversation depends on your platform.

<details>
<summary>Optional Codex integration</summary>

Codex users can install this same repository as a discoverable skill. This is an optional host-specific integration; the general file-reading workflow above also applies.

Ask Codex to install it:

```text
Use $skill-installer to install the skill at the root of
https://github.com/kidheart/flatland-research-coach
with the name flatland-research-coach.
If an installation directory with that name already exists,
explain the situation before proceeding and do not overwrite it.
```

Alternatively, with Git installed, clone it into Codex's user-level skill directory using PowerShell. These commands stop if the destination already exists:

```powershell
$skillPath = Join-Path $HOME '.agents/skills/flatland-research-coach'

if (Test-Path -LiteralPath $skillPath) {
    throw 'The destination already exists. Check the current installation before making changes; do not overwrite it.'
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $skillPath) | Out-Null
git clone https://github.com/kidheart/flatland-research-coach.git "$skillPath"

if ($LASTEXITCODE -ne 0) {
    throw 'Cloning did not complete. Check the Git output and destination directory before proceeding.'
}
```

After installation, start a new conversation; restart Codex if it has not discovered the skill. You can then begin with:

```text
Use $flatland-research-coach and respond in English.
First read the environment description and experiment records I provide,
then help me investigate my current research question.
```

See [OpenAI's skills documentation](https://learn.chatgpt.com/docs/build-skills) for skill directories and installation guidance. The `agents/openai.yaml` file supplies optional Codex UI metadata and is not required for reading or using the Markdown guidance.

</details>

## Get started

Choose a prompt that fits your current question and attach relevant materials you have permission to use. In the examples below, `SKILL.en.md` means the file you have made available by giving its full path, uploading it, or pasting its contents.

**Start with a research question**

```text
Read SKILL.en.md and follow its coaching guidance.
First read the environment description and experiment records I provide,
then restate the facts you already know.
Ask one or two questions at a time about the most important uncertainty.
Help me form a hypothesis that could be disproved and design the next experiment together.
```

**Trace a mismatch between planning and execution**

```text
Read SKILL.en.md and follow its coaching guidance.
I have provided my planned trajectory, actual trajectory, and action interface description.
First identify the earliest divergence and separate known facts from possible explanations.
Then help me design a small check to locate the cause.
```

**Assess what an improvement actually shows**

```text
Read SKILL.en.md and follow its coaching guidance.
Review the before-and-after experiments I provide.
Did they start from comparable conditions? What resources did they use?
How much work actually finished? Were failures and timeouts included in the statistics?
Help me distinguish efficiency changes, strategy changes, and gains in full execution,
and state the limits of the evidence.
```

**Explore an idea before running experiments**

```text
Read SKILL.en.md and follow its coaching guidance.
I do not have run data yet. Use a small railway example clearly labeled as fictional
to help me practice separating observations from explanations
and designing an experiment that can distinguish two explanations.
Let me state my judgment first; give progressive hints when I get stuck.
```

## Contents

| File | Purpose |
| --- | --- |
| [SKILL.en.md](SKILL.en.md) | English coach instructions: the dialogue process, depth of help, judgment standards, and material boundaries. |
| [Question and hint bank](references/en/question-bank.md) | Choose questions about objectives, interfaces, experiments, generalization, and interpreting results. |
| [Experiment card](references/en/experiment-card.md) | Record predictions, actual results, conditions that would challenge a hypothesis, and next steps. |
| [Anonymized reasoning cases](references/en/reasoning-cases.md) | Explore how qualitative observations change judgments and what new evidence could overturn them. |
| [agents/openai.yaml](agents/openai.yaml) | Optional Codex-specific UI metadata: display name, description, and default prompt. Not a requirement for using the Markdown guidance. |
| [LICENSE](LICENSE) | The repository's license terms. |

## Limits of the research conclusions

Flatland environments can differ in version, transition rules, speeds, malfunction visibility, goal handling, evaluation rules, and resource limits. Each discussion should begin with the conditions in your environment that matter to the question.

The anonymized cases preserve qualitative observations and reasoning. The underlying experiment materials have not been published for independent verification. These cases help generate hypotheses; they do not provide evidence for public performance comparisons or optimality claims. Their order does not prescribe an architecture or a research path to retrace.

Feasibility, meeting a defined objective, achieving a favorable evaluation, and theoretical optimality each require appropriate evidence. Local checks, local results, and full evaluations also support conclusions of different scope. This project does not promise a particular score, a perfect score, or optimality across all environments.

The repository does not include the source project's code, exact configurations, parameters, per-case scores, or implementation details that could reconstruct its solution. The coach uses materials that the current user provides or authorizes it to access, together with public sources. It does not proactively recover the source solution from past conversations or private projects.

If your explanation has stronger evidence, the judgments in the cases should be revised or overturned. Once you have verified the objective you defined, you can record the applicable conditions and remaining unknowns, then conclude that round of research.

## Contributing

Discuss improvements in an [Issue](https://github.com/kidheart/flatland-research-coach/issues), or submit a [Pull Request](https://github.com/kidheart/flatland-research-coach/pulls) with:

- Questions that distinguish explanations, and useful progressive hints for learners who are stuck.
- Clearly labeled fictional teaching examples, or sufficiently anonymized qualitative reasoning cases that you have permission to publish.
- Clearer experiment records, wording improvements, and translations.

For a new case, describe the observation, possible explanations, a distinguishing experiment, a bounded conclusion, and the conditions for reconsidering it. Check whether several cases together could reveal a distinctive combination from the source solution.

Do not submit private solutions, code, parameters, configurations, scores, logs, or commit identifiers from the source project or other people's work. Before contributing, confirm that you have the right to publish the material and are willing to release your contribution under the repository's license.

## License

© kidheart. This repository is licensed under [Creative Commons Attribution–NonCommercial 4.0 International (CC BY-NC 4.0)](LICENSE). You may share and adapt the material for noncommercial purposes under the license, provided you give appropriate credit, link to the license, indicate changes, and comply with its other terms. Commercial use requires separate permission.

Suggested attribution:

> Based on [Flatland Research Coach](https://github.com/kidheart/flatland-research-coach) by kidheart, licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Describe any changes here.
