# 轻量证据工具

**简体中文** | [English](en/tooling.md)

这些 Python 标准库工具检查当前使用者提供的证据，不依赖某一 Flatland 发行版，也不包含原作者的求解器、配置、轨迹或评测结果。随附数据和演示 runner 全部是**为此工具构造的合成例**。运行需要 Python 3.9 或更新版本。

在仓库根目录按需选择命令，不必全部执行：

```text
python scripts/rail_trace.py diagnose examples/synthetic_trace.json --limit 20
python scripts/rail_trace.py slice examples/synthetic_trace.json --start 1 --end 1 --context 1 --output trace-slice.json
python scripts/rail_trace.py replay examples/synthetic_replay.json --adapter scripts/synthetic_rail_runner.py --timeout 10 --trace-output replay-trace.json
python scripts/rail_trace.py reservations examples/synthetic_reservations.json
python scripts/smoke_rail_trace.py
```

四个子命令均支持 `--output PATH`，未指定时将 JSON 输出到 stdout。报告采用紧凑 JSON；回放报告不含整份轨迹，可用 `--trace-output PATH` 单独保存，供后续 `slice` 或 `diagnose` 使用。结果集合含 `items`、`total_count` 与 `truncated`；`--limit` 只限制每个集合的展示数量，不中止输入检查，也不截断保存的轨迹。

**发现异常仍返回退出码 0**，表示分析完成，不表示轨迹正确。参数、输入格式、输出、适配器失败或实际子进程超时返回 2，stderr 含 JSON `error`；`--help` 是普通命令行帮助。校验及执行成功前不会写报告/轨迹。输出不得覆盖输入、适配器或另一个输出，包括已有硬链接别名；其他已有输出文件会被替换。

## 标准化轨迹：`rail-trace/v1`

最小有用的合成结构：

```json
{
  "schema": "rail-trace/v1",
  "synthetic": true,
  "semantics": {"agent_model": "point", "vertex": "exclusive", "edge_swap": "forbidden"},
  "frames": [
    {"tick": 0, "agents": [
      {"id": "A", "position": [0, 0], "direction": 1, "occupies": true,
       "planned": {"position": [0, 0]}}
    ]}
  ]
}
```

`tick` 为严格递增的非负整数；每帧有 `agents` 数组，ID 是帧内唯一的非空字符串。整数不能用布尔值替代。提供位置时，值为两个整数组成的 `[row, column]` 或 `null`；方向为 `0..3` 或 `null`；显式 `occupies` 必须为布尔值。`occupies: true` 与 `position: null` 矛盾，会被拒绝。未知状态字段应省略；`null` 是明确记录的值，不能代替未知。

`planned` 可含 `position`、`direction` 和 `occupies`，必须描述观察记录**同一 tick** 的期望状态。仅比较双方均提供的字段；缺少计划或实际字段计入 `comparison.uncompared_fields`。`first_divergence` 是最早可比较的差异，顺序为 tick、agent ID、位置/方向/占用。先前记录不全时，它只是“首次记录到的可比较分歧”，不保证是最初起因。

可选 `blocked_by: ["B"]` 是 runner 在该时刻明确提供的等待依赖，不能根据位置不动凭空生成。可选 `release_tick` 为实际已知、且当时决策者可见的非负整数解除时刻，只作为尚需核实的提示报告。`status`、`malfunction` 及其他元数据可以保留，但工具不解释它们，也不据此推断解除条件。缺少 `blocked_by` 表示依赖证据未知；空数组表示该时刻没有列出的依赖。

`semantics` 必须声明三项：

| 字段 | 可选值 | 作用 |
| --- | --- | --- |
| `agent_model` | `point`、`unspecified` | 碰撞检查要求点状 agent 模型。 |
| `vertex` | `exclusive`、`allowed`、`unspecified` | 仅 `exclusive` 报告共享记录位置。 |
| `edge_swap` | `forbidden`、`allowed`、`unspecified` | 仅 `forbidden` 报告记录端点的对向交换。 |

`diagnose` 提供的有限观察：

- 某可比较字段首次出现计划与实际不一致。
- **同 tick 显式**等待图中的循环强连通分量、边和 `release_hints`，且 `deadlock_proven` 始终为 `false`。缺少解除提示不代表永不解除；需要回查事件、故障可见性、资源归属及未来解除条件。
- 声明独占点状占用时，依据显式 `occupies: true` 和已知位置报告共享顶点。
- 在连续整数 tick、双方前后均明确占用位置、且禁止点状交换时，报告反向端点对。这不验证轨道转移是否合法，不检查途中经过的格子、连续运动范围、分数速度、长车或全部轨道冲突。

覆盖报告指出时间缺口、上一帧出现但下一帧未记录的 agent、未记录阻挡者和未知占用。缺失 agent 只代表未记录，不推断其退出或完成；没有外部名单也不能统计从未出现的 agent。位置不变不转换成等待时长、延误、失分或吞吐损失，慢车可能仍在单元内移动。“没有发现冲突”只限于实际启用且有记录的检查。

## 切片，不是状态重建

`slice` 选择 `--start` 到 `--end` 的记录帧，包含两个端点，并在两侧各保留 `--context` 个已记录帧，默认 1。保留完整 agent 元数据与语义，区间内没有帧时拒绝。输出中的 `slice.selected_ticks` 与 `included_ticks` 区分选择范围和含上下文的范围；对该文件运行 `diagnose` 也会检查上下文帧。`--context 0` 显式省略周围证据。

切片不运行仿真。上下文本身可能稀疏，运行中途的位置和方向无法恢复完整 Flatland 检查点、运动进度、随机状态、待发生故障、出发状态或外部依赖。它只用于缩小阅读范围。

## 真正执行项目适配器

`replay` 要求通过 CLI 的 `--adapter` 显式指定当前任务获准执行的 Python 文件；不从 JSON 数据中发现或执行代码。它通过 `[sys.executable, adapter_path]`、`shell=False` 启动进程，将一个 JSON manifest 送入 stdin，捕获 stdout，并用 `subprocess.run(timeout=...)` 实际执行超时控制。这是普通本地 Python 执行，不是沙箱。适配器应同步完成，不能留下生命周期超出本次调用的后台 worker；超时终止所选进程，不保证终止任意后代进程树。诊断信息写 stderr；适配器非零退出时，不回显可能含私有数据的诊断原文。

Manifest 外层结构：

```json
{
  "schema": "rail-replay/v1",
  "synthetic": true,
  "clock": {"start_tick": 0, "action_timing": "before_step"},
  "runner_requirements": {"engine": "synthetic-line/v1"},
  "checkpoint": {"adapter_defined": "complete initial state goes here"},
  "actions": []
}
```

此块仅说明格式，占位检查点不可执行。可运行示例见 [synthetic_replay.json](../examples/synthetic_replay.json)。`clock`、`runner_requirements`、`checkpoint` 须为非空对象；起始 tick 为非负整数，`action_timing` 是非空说明，`actions` 是数组。引擎版本、检查点、动作顺序及项目字段由适配器检查；工具无法推断任意项目的状态是否充分。

适配器成功时，stdout 必须是一个 JSON 对象：

```text
{"schema":"rail-replay-result/v1","trace":<有效的 rail-trace/v1>, ...可选元数据...}
```

轨迹须在 `clock.start_tick` 包含初始检查点帧。工具校验后生成紧凑的 `rail-replay-report/v1`：实际适配器路径、执行标记、帧数、tick 范围、runner/completion 的有限标量摘要与诊断。runner 仅选取 `engine`、`version`、`name`、`is_flatland`、`synthetic`；completion 仅选取 `actions_applied`、`final_tick`、`status`。字符串最多保留 200 字符并标截断，整数含负号最多 20 位，任意嵌套元数据省略，不回显完整适配器结果或轨迹。

用 `--trace-output replay-trace.json` 保存完整、已校验的 `rail-trace/v1`（包含全部帧和轨迹元数据）；`--output replay-report.json` 单独保存报告。报告的 `trace_output` 为保存路径，未请求时为 `null`。轨迹文件可直接用于切片/诊断，报告本身不是轨迹。两个输出须与彼此、manifest、适配器区分，包括路径别名。

执行成功只证明该适配器返回了这份轨迹，不证明它忠实实现 Flatland、等价于另一 runner，或有评测收益。缺少适配器及其所需状态时，使用记录切片并说明尚缺的回放条件。

随附 [synthetic_rail_runner.py](../scripts/synthetic_rail_runner.py) 真正执行上述协议。它构造一个 `synthetic-line/v1` 水平单线世界：点状 agent 朝东（1）或西（3），显式 `go`/`hold` 动作、整数运动阶段及初始故障倒计时。一步开始时已被占用的目标会阻挡进入，即使占用者在本步离开；多个提案争用同一空格也会阻挡。所有 agent 始终保留，包括到达边界后。检查点包含运动阶段与故障倒计时。它不导入 Flatland，也不实现原作者求解器；这些局限规则演示了为何位置不变不直接等于等待。

## 预约事件检查：`rail-reservations/v1`

输入包含 `schema: "rail-reservations/v1"`、`interval: "half-open"` 与 `events` 数组。从空表开始按数组顺序执行，不推断时间推进、自动过期或项目隐藏状态。资源字符串是不透明标识，转换者须先编码当前项目真正的冲突资源。

| 操作 | 必要字段 | 含义 |
| --- | --- | --- |
| `reserve` | `owner`、`resource`、`start`、`end` | 为完全相同的键增加一个引用。 |
| `release` | 同上 | 减少一个完全相同键的引用，归零时删除。 |
| `checkpoint` | 唯一 `name` | 保存含引用计数的完整表。 |
| `rollback` | `name` | 恢复该快照及计数。 |
| `observed` | `entries` | 对比实际提供的观察快照，不改重放表。 |

每个事件含 `op`，owner/resource 为非空字符串，整数边界满足 `0 <= start < end`，区间为 `[start,end)`，所以 `[0,2)` 与 `[2,3)` 不重叠。观察项包含同样的键和正整数 `count`，不允许重复键。对比需提供被检查资源范围的完整快照；该格式不表达部分观察快照。

同一 owner/resource/interval 的重复预约采用引用计数，并列入 `duplicate_references`，不自动当作错误。释放未拥有键报告 `unowned_release`，不改状态。不同 owner 在相同资源的区间重叠会报告；重叠预约仍保留，以便审阅事件历史。同 owner 重叠不报告为跨 agent 冲突。未知回滚名报告问题但不改状态；重复检查点名被拒绝，成功的检查点在回滚后仍保留为独立快照。不会自动删除过期预约。

`observed_equivalence` 区分全部已提供快照匹配、存在不匹配，以及 `not_checked_no_observed_snapshots`。匹配也只支持当前标准化表与这些观察时刻的相等，不证明整个实际项目等价。事件检查本身不证明增量实现与全量重建一致，也不证明时刻表安全。

## 适配当前使用者工程

保持转换明确且小。先对齐决策 tick、动作提交、步后观察和计划期望 tick，再按当前拓扑规则统一行列与方向。明确离线/未出发、分数移动、故障及到达后保留/移除的 agent 如何占用资源。只有适用时才声明点状碰撞语义；更丰富的转移或占用范围检查继续放在项目适配器中。

从真实决策或仿真事件导出 `blocked_by`，区分当时可见的故障/解除信息与事后信息，不猜解除时间。回放应恢复拓扑、完整 agent 运动状态与状态类型、时钟、随机状态、故障事件源、包装层状态等实际必需项；缺少时明确失败。若重放规划决策，保持原决策者的信息边界，并说明任何刻意提供的事后信息。

预约事件与观察两侧必须使用相同区间约定和资源标识。要比较增量表与重建表，应在相关检查点/回滚边界从实际实现独立导出观察快照。示例提供协议与检查方式，项目转换、求解器改进和性能主张仍须由当前项目证据支持。

短冒烟脚本覆盖具体分歧、环的边界、稀疏记录、语义开关、坏格式、切片上下文、引用计数/半开区间冲突/无效释放/回滚/观察差异、真实 runner 的移动与故障、紧凑报告和完整轨迹保存、含硬链接的输出覆盖拒绝及实际超时。它使用合成数据和临时文件，不运行 benchmark 扫描或 A/B 套件。
