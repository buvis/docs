# Agent operations components

Each component supplies a capability to the [agent operations system](index.md).
Components can serve Agents in different roles, including work outside Flights.
The [taxonomy](taxonomy.md) defines the shared terms and ownership boundaries.

Availability below is current as of 2026-11-02. An existing implementation does
not imply support for every host or deployment. Consult each product's
documentation for installation and supported configurations.

## Specflow

**Existing, unreleased.** [Specflow](https://github.com/buvis/agent-plugins/tree/master/plugins/specflow)
owns the requirements, design, and task artifacts it produces for a Flight Plan.
Autopilot consumes those artifacts and owns the Flight's execution, review,
and completion. Specflow defines the work and its acceptance criteria;
Autopilot records execution progress and checks the evidence against them.

This is the target division of responsibility. The current Specflow package
also includes implementation guidance; integration with Autopilot requires
compatible workflow consumers. Its package documentation records host support.

## Autopilot

**Migration in progress.** [Autopilot](https://github.com/buvis/agent-plugins/tree/master/plugins/autopilot)
owns one Flight's execution workflow, review policy, evidence, and outcome.
Autopilot tracks attempts and results against a Flight Plan supplied by
Specflow or another authoring workflow, including a manually written PRD.
Specflow is optional: every plan must satisfy the same input contract,
including an explicit goal, tasks, and completion criteria. Autopilot validates
the plan before execution; its source does not change review or evidence
requirements. The portable package is currently a gated foundation; host
execution, certification, and
publication remain unavailable.

Its target standalone mode uses the same workflow controller with manually
started isolated sessions. Managed execution uses OVCAQ for supervision.
Each Flight covers exactly one Project and has one authoritative workflow
writer. Coordinated work across Projects uses one Flight per Project, linked
by prerequisites; each has its own review and completion outcome.

## OVCAQ

**In development.** [OVCAQ](https://github.com/buvis/ovcaq) schedules work,
supervises Agent sessions through Drivers, records execution facts, and supplies
the operations API. State, workflow, supervision, Claude/Codex adapters, and a
terminal UI are implemented; public release is pending.

The current implementation bundles workflow state and terminal presentation.
The target integration assigns workflow authority to Autopilot and presentation
to Tower. OVCAQ owns process execution and requests workflow changes through
Autopilot's controller.

When a Flight exhausts its recovery attempts, OVCAQ requests parking through
Autopilot and notifies the Supervisor. Unrelated Flights continue; dependent
Flights wait until their prerequisites are satisfied. Parking preserves the
Flight for later resolution and does not count as successful completion.

OVCAQ's target environment interface is provider-neutral. It schedules against
capabilities and capacity, requests Seats, and uses the access supplied by the
provider. Environment location and deployment mechanics belong to the provider;
OVCAQ does not provision Kubernetes resources or configure local environments.

Each concurrently running Agent receives its own Seat. One Flight can hold
multiple Seats; successive Legs may reuse a Seat only when the next assignment's
isolation requirements are met. Review contexts and permitted inputs remain
independent even when the underlying environment is reused.

## Tower

**Planned as an independent component.** Tower provides instruments for observing
Flights and relaying operator input: Flight Board, Radar, Tower Log, and Strips.
The current terminal interface is bundled with OVCAQ.

Tower reads operational state and sends control requests through OVCAQ's API.
Closing a view must not stop execution.

## Koolna

**Existing infrastructure; Seat integration pending.**
[Koolna](https://github.com/buvis/container-images/tree/master/apps) is the
Kubernetes-focused Environment Provider. It supplies development environments
through images, a Kubernetes operator, a session manager, caches, and a web UI.

The existing repository-oriented environment model does not yet establish
Seat isolation. The Environment Provider contract and Koolna's obligations
under it are tracked as OVCAQ discovery 00067. Local execution needs a
separate provider under the same contract; none is specified yet.

## Portable messaging

**Planned; implementation not selected.** Messaging will deliver information
between Agent sessions across hosts and launchers through OVCAQ's operations
API; sessions outside OVCAQ use their host's native messaging. Its
requirements, message labels, the optional email bridge for the Supervisor,
and acceptance criteria are tracked as OVCAQ discovery 00068.

## Engram

**Existing.** [Engram](https://github.com/buvis/engram) supplies cross-project
memory and recall through a local index of project artifacts, decisions,
memory files, transcripts, review findings, and code. Hybrid search retrieves
material across registered repositories.
Most results point to source files; harvested findings retain their text.

Agents select Project scope by default for recall. Explicit portfolio
queries retrieve relevant knowledge across registered Projects while retaining
its source and Project attribution.

Its documented memory corpus reads Claude project memory files. The target
integration indexes authoritative memory files from each Project's repository;
support for that source remains to be implemented. Reusing knowledge does not
preserve an Agent's identity across sessions.

## Shared memory

**Repository-owned project memory; portable integration pending.** Shared memory
retains knowledge for reuse by Agents across sessions and roles. New memories
belong to the current Project by default, and recall defaults to that Project.
Engram provides cross-project memory and recall when a broader scope is selected.
Project scope preserves ownership and relevance; it does not prevent authorized
portfolio searches through Engram.

Authoritative project memories live in version-controlled files in the
Project's repository. All supported Agent hosts use those files as the common
source. Git records their revision history; Engram indexes them for recall
within and across Projects. An index can be rebuilt from the authoritative
files and does not become another writer of project memory. The file format,
repository path, provenance fields, and host integration are tracked as
Engram intake 00010.

| Information | Purpose | Authority |
|---|---|---|
| Session context | What an Agent sees during one run. | Local to the session and its permitted inputs. |
| Message | Information delivered to another session. | An observation or request subject to validation. |
| Project memory | Knowledge retained for later reuse. | Version-controlled files in the Project's repository, with source and author attribution. |
| Workflow state | Flight progress, review results, and outcome. | Autopilot's workflow controller. |
| Execution record | What launched, exited, or failed, and why. | OVCAQ; none in standalone mode. |

Retrieving memory does not resume the original Agent or restore its authority.
Remembered decisions must be checked against current instructions and state.
Recall must respect role-specific input limits: a blind reviewer cannot receive
excluded builder reasoning through memory.

## Agent Skills and Braid

**Existing.** [Agent Skills](https://github.com/buvis/agent-skills) supplies
reusable procedures. Braid composes source repositories into a shared discovery
view and host projections. Skills are edited in their source repositories;
generated links expose them to the supported hosts.

## Agent Plugins

**Existing foundation; component migrations in progress.**
[Agent Plugins](https://github.com/buvis/agent-plugins) packages portable workflows
and their host integrations. It contains Specflow and Autopilot, each with its
own availability and compatibility requirements.

## Warden and Aegis

**Existing Claude-specific plugins.**
[Warden](https://github.com/buvis/claude-warden) filters commands;
[Aegis](https://github.com/buvis/claude-aegis) supplies pre-action checks.
Their protections require integration with the Agent's host.

## Loupe, Strunk, and Agoge

**Existing plugins.** [Loupe](https://github.com/buvis/claude-loupe) supplies
edit feedback, [Strunk](https://github.com/buvis/claude-strunk) supplies coding
and testing guidance, and [Agoge](https://github.com/buvis/claude-agoge) exercises
products for QA. These capabilities support verification; Autopilot owns
Flight acceptance.

## Checkup and Git Ferry

**Existing plugins.** [Checkup](https://github.com/buvis/claude-checkup) audits
Agent configuration. [Git Ferry](https://github.com/buvis/claude-git-ferry)
supports repository and Git workflows. Availability depends on the installed
skills and host.

## MCP server foundation

**Existing scaffold.** [MCP Servers](https://github.com/buvis/mcp-servers)
provides shared infrastructure for exposing tools to Agent hosts, with a common
core and an example server. Messaging and shared memory require their own
implementations and are not supplied by this scaffold.
