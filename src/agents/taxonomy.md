# Agent operations taxonomy

This document defines the shared vocabulary for every project that builds,
runs, or supports autonomous agent work,
including Autopilot, OVCAQ, Tower, Koolna, messaging, and memory.
A project may keep its own internal names, but its docs, UI, and contracts
with other projects use these terms.

The names describe responsibilities, not service boundaries, databases,
deployment units, or a requirement to build every named feature. Ownership is
logical: one standalone process may fulfill several responsibilities.

OVCAQ names the shepherd role: the orchestrator that manages Flights. Tower
names the infrastructure used to watch over those Flights and relay operator
input through instruments such as Radar and the Flight Board.

## The four execution domains

These domains organize Flight execution. They are part of the wider
[agent operations system](index.md), which also includes specification,
skills, safeguards, quality tools, messaging, and memory. A component need
not belong to a Flight or become another execution domain.

Ownership below describes the target architecture. The [component reference](components.md)
records current availability and integration limits.

| Domain | Metaphor | Owns | Project today |
|---|---|---|---|
| **Autopilot** | on board the aircraft | One Flight's execution against its Flight Plan: phases, task attempts, review cycles, and outcome | `agent-plugins/plugins/autopilot` |
| **OVCAQ** | the shepherd, an orchestration role | Scheduling and execution of the Flights it manages, execution records, the operations API | `ovcaq` |
| **Tower** | infrastructure for watching over Flights | Instruments that show operational state and relay the operator's input | planned |
| **Environment provision** | the workshop | Ponks, Seats, Toolsets, and Seat isolation through a provider-neutral contract | Koolna for Kubernetes; local provider not yet specified |

With all four domains in use:

> Environment Providers keep the Ponks. OVCAQ assigns work to Seats and sends
> Pilots to fly it. Autopilot flies the Flight Plan. Tower shows it all.

Koolna is the Kubernetes Environment Provider. Other providers can supply
environments through the same contract.

In the target architecture, Autopilot runs standalone without OVCAQ, Tower,
or Koolna: the operator starts isolated sessions in an available workspace
against the same workflow controller. OVCAQ uses the Environment Provider
contract for execution and runs headless without Tower. Closing or crashing a
Tower view never stops a Flight. These are intended operating modes,
not a stack in which every domain must be deployed.

## Glossary

### Work

| Term | Meaning |
|---|---|
| **Project** | A codebase being developed. |
| **Flight Plan** | The goal, tasks, completion criteria, and any prerequisite Flights for one Flight. Produced by Specflow or another authoring workflow, including a manually written PRD, and validated against Autopilot's input contract. Defined before execution and revised explicitly when scope changes. |
| **Flight** | An effort by one or more Pilots to achieve one Flight Plan in exactly one Project. It may take one or many sessions and has its own review and completion outcome. |
| **Leg** | One agent session within a Flight. A long Flight is flown in many Legs. |
| **Crew change** | A handoff between Legs: a fresh session continues from the Flight's state, not from the last session's memory. |

Work spanning Projects uses a Flight for each Project. A Flight Plan may list
other Flights as prerequisites; OVCAQ schedules the Flight after they complete.
For example, matching API changes in OVCAQ and Tower use two Flights.
Completion of one does not imply completion of the other.

### Agents and people

| Term | Meaning |
|---|---|
| **Agent** | The generic software actor that performs work and can take on different roles. Its identity is scoped to one session: a fresh session creates a new Agent. Independent of its host, selected model, and any particular Flight. |
| **Session** | One bounded run in a host, defining an Agent's lifetime, context, and runtime identity. Roles, work, and shared knowledge can outlive the session. |
| **Role** | An Agent's assigned responsibility in a particular context. It defines the work expected of that Agent; a role name alone grants no permissions. |
| **Pilot** | An Agent acting in the role that flies a Leg of a Flight. Implementor, reviewer, and doubt pass are Pilot assignments. Every Pilot is an Agent; not every Agent is a Pilot. |
| **Duty Controller** | The role of an agent that works for OVCAQ: it judges Squawks that OVCAQ's rules cannot classify. It flies nothing. |
| **Driver** | The technical adapter for an agent host: launches sessions and translates its input and output. A host may support several model providers. Not a role. |
| **Supervisor** | The human operator. May intervene at any time; required when no authorized automated action remains. |

Agent is the actor; Pilot or Duty Controller is its role; Leg is its session
within a Flight. OVCAQ names the orchestration responsibility and the system
that fulfills it through rules and, when needed, Agents such as the Duty
Controller. OVCAQ need not be one Agent.

Pilot and Duty Controller are the currently named operational roles, not a
closed list. Agents can exchange messages or use memory without being Pilots
or belonging to Flights. Messaging services, memory stores, and tools can
support Agents without themselves being Agents.

Role assignments may change where policy permits. A role change does not
erase context, create a fresh session, or satisfy reviewer isolation. Required
crew changes and independent reviews still use separate contexts. A fresh
session creates a new Agent even when it uses the same role, model, or shared
memory. Handoffs transfer work and permitted context, never Agent identity.
Records retain the originating Agent's identity for attribution after its
session ends.

### Control

| Term | Meaning |
|---|---|
| **Dispatch** | OVCAQ's choice of which Pilot flies which Leg, from which Seat. |
| **Squawk** | A signal from a Flight that it needs help: blocked, out of options, or waiting for a decision. |
| **Clearance** | A request to control a Flight's lifecycle: pause, resume, park, retry, abort. A retry starts a fresh Leg; Dispatch chooses its Pilot. Accepting a review finding as it stands is a Waiver, not a Clearance. Autopilot validates each Clearance and records whether it was applied. |
| **Waiver** | An explicit, scoped exception issued by the Supervisor to a rule that policy permits the Supervisor to waive. It cannot bypass an external permission or security control. |

### Environment

| Term | Meaning |
|---|---|
| **Environment Provider** | Supplies and maintains execution environments through a common contract for capacity, Toolsets, Seat allocation, access, and isolation guarantees. Owns the deployment-specific implementation. Koolna provides Kubernetes environments. |
| **Toolset** | A versioned definition of tools, runtimes, and configuration. It may be supplied by an image or a local tool manager. |
| **Ponk** | A maintained execution environment that supplies a Toolset and capacity for Seats. Its deployment and update mechanism are implementation choices. |
| **Seat** | An isolated place at a Ponk for one active Agent, holding its Workspace and Execution Boundary. A Flight may allocate several Seats for concurrent Agents. |
| **Workspace** | The files an Agent works on in its Seat, normally a dedicated Git worktree for its assignment. A worktree alone is not a security boundary. |
| **Execution Boundary** | The enforced permissions and limits of a Seat, including filesystem, credentials, HOME, processes, network, and resources. Its guarantees must be stated and verified. |

### Views

| Term | Meaning |
|---|---|
| **Flight Board** | A Tower instrument showing current status across Flights, including queued, running, parked, and blocked work: the queue and status table. |
| **Radar** | A Tower instrument showing what is moving now: active Legs and their Pilots, allocated Seats, open Squawks, and the live event stream. The Flight Board is the table; Radar is the live picture. |
| **Tower Log** | A Tower view of recorded events: what happened, when, why, and who decided it. Records persist independently of the view. |
| **Strip** | The compact picture of one Flight: its plan, active Legs and Pilots, allocated Seats, state, and any Squawk. A view element, not a domain entity. |

## Ownership

| Concern | Owner |
|---|---|
| Requirements, design, and task artifacts defining the Flight Plan | Specflow or the plan's authoring workflow |
| Flight Plan input contract and validation | Autopilot |
| Flight execution state, phases, task attempts, review cycles, outcome | Autopilot |
| Dispatch, session/process lifecycle, execution records | OVCAQ when managed; the Supervisor starts each session by hand when standalone, with no execution record |
| Squawk triage and Clearances across Flights | OVCAQ |
| Instruments, keyboard and touch input, view preferences | Tower |
| Toolsets, Ponks, Seats, and Seat isolation | The Environment Provider; Koolna for Kubernetes |
| Authoritative project memory and its revision history | Version-controlled files in the Project's repository |
| Cross-project memory indexing and recall | Engram |
| Project identity and source code | the Project's own repository |

The plan's authoring workflow owns its specification artifacts. Specflow is
optional; plans from every source meet the same input and acceptance requirements.
Autopilot is the one writer of Flight execution state: the plan revision being
executed, phases, task attempts,
review results, and outcome. A scope change requires an explicit update to the
Flight Plan; execution progress does not silently change its requirements.
OVCAQ records execution facts such as process exits; those facts are not
a second copy of workflow state. Autopilot reconciles them when
it resumes. A standalone Flight has no execution record: the Supervisor
starts each session and Autopilot resumes from workflow state alone.
Concurrent Legs submit results through Autopilot's state writer.

OVCAQ requests workflow changes through Clearances. Tower keeps its own
view preferences but changes operational state only through OVCAQ's API;
it never signals a process directly. Environment Providers supply execution
environments and report capabilities and capacity. OVCAQ decides what work to
schedule through that contract without managing Kubernetes resources or local
environment setup. Provider-specific placement and access belong to the provider.

## Escalation: management by exception

The goal is automated operations within existing authorization. Standing
authorization remains valid; routine retries and reversible work need no new
approval merely because they cross a domain boundary.

| Tier | Who | Handles |
|---|---|---|
| 1 | **Autopilot** | Workflow decisions inside one Flight: phases, rework, retry policy, and when a fresh Leg is required. OVCAQ performs session changes when managed; the Supervisor starts the next session when standalone. |
| 2 | **OVCAQ** | Execution decisions for managed Flights: scheduling, stuck processes, available hosts/models, and capacity. Rules first; an optional Duty Controller handles unresolved judgment. |
| 3 | **Supervisor** | Waivers, indispensable missing input, and actions requiring authorization that has not already been granted. |

A Squawk climbs only as far as it must. Standalone Autopilot escalates directly
to the Supervisor when needed. Track avoidable interventions alongside failed
outcomes and policy violations; fewer interventions alone does not mean health.

When a Flight exhausts its recovery attempts, park it and notify the Supervisor
with the blocker, attempted recovery, and available next actions. For managed
Flights, OVCAQ requests parking through a Clearance; Autopilot records the
workflow transition. Unrelated Flights continue. Flights whose prerequisites
are unmet wait. A parked Flight is incomplete; recovery exhaustion does not
waive acceptance criteria.

### Duty Controller limits

- It sees only what the rules could not classify.
- It may request Clearances within its authorization. It may not grant itself
  permission, issue a Waiver, or perform an unauthorized tier 3 action.
- It escalates to the Supervisor with a prepared decision: evidence, options,
  and a recommendation.
- It gets a fresh, isolated context for each Squawk, and where possible a
  different model family from the Pilot it judges.
- Bound recovery attempts per unresolved Squawk. At the cap, request parking
  of the affected Flight and notify the Supervisor. Do not start another
  recovery loop or invent a new approval requirement for already authorized work.
- OVCAQ records every decision and its reason, available through the Tower
  Log even if no view was attached when it happened. Repeated decisions are
  candidates for tested rules, not automatic policy changes.

## Clearances and Waivers

Autopilot owns workflow transitions within policy and permission controls.
OVCAQ owns the lifecycle of processes it launches. Stopping a process does
not establish a successful, aborted, or otherwise completed workflow outcome.

- Autopilot checks authenticity, authorization, applicable policy, and current
  state before applying a Clearance. A Supervisor request is not a bypass of
  non-waivable controls. Completion requires the Flight Plan's evidence;
  requirements may be waived only where policy explicitly permits it.
- Every Clearance records who issued it: the Supervisor, OVCAQ's rules, or the
  Duty Controller.
- A Clearance has an identifier and a recorded result: pending, applied, or
  rejected with a reason. Re-delivery must not repeat its effect.
- Only the Supervisor may issue a Waiver.
- A Waiver applies to one Flight. Changing a rule for every Flight is a policy
  change, not a Clearance.
- A Waiver never looks clean. The Flight lands as "done, waived: review", with
  the waiver, its reason, and its issuer in the Flight record, so merges,
  releases, audits, and Strips can see it.
- When OVCAQ cannot reach Autopilot, it may stop Legs, but it must not rewrite
  Flight state to make up for the lost link.

## Ponks and Seats

A Ponk is the environment you maintain; a Seat provides an isolated place for
one active Agent. A Flight can allocate multiple Seats for concurrent Legs.

OVCAQ requests suitable Seats through the Environment Provider contract.
Providers expose the capabilities needed for scheduling and enforce their
advertised isolation guarantees. The same scheduling logic applies regardless
of where an environment runs. Koolna implements the Kubernetes side; local
execution requires a separate provider implementation.

The contract's requirements, including Seat reuse, parking, shared repository
storage, and Toolset revision tracking, are tracked as OVCAQ discovery 00067.

## Shared agent capabilities

Messaging serves Agents across hosts and launchers through OVCAQ's operations
API; sessions outside OVCAQ use their host's native messaging. Memory serves
Agents in every role, inside or outside a Flight. Memory and recall default to
the current Project; Engram provides cross-project recall through explicit
portfolio queries. Messages deliver information, memory retains knowledge, and workflow
state records authoritative progress. None substitutes for another. The
[component reference](components.md) records each capability's status and
where its requirements are tracked.

## Tower

Tower provides the infrastructure and instruments for watching Flights and
accepting operator input. It presents OVCAQ's operational state; orchestration
decisions remain with OVCAQ.

- Tower reads state and sends Clearances only through OVCAQ's operations API.
  OVCAQ does not need to know which Tower views are attached.
- A Clearance sent from a view is a request. Accepted is not applied; the view
  shows what Autopilot actually did.

## Words to use

| Say | Not |
|---|---|
| Autopilot owns the Flight | OVCAQ owns the Flight |
| OVCAQ sends a Clearance | OVCAQ sets the Flight's state |
| OVCAQ orchestrates; Tower provides instruments | Tower dispatches Pilots |
| Dispatch assigns work to a provider-supplied Seat | Koolna dispatches a Flight |
| The Pilot flies a Leg from the Seat | The Pilot is provisioned from a Ponk |
| The Environment Provider maintains the Ponk | OVCAQ installs tools |
| A Strip shows a Flight | A Strip shows a Pilot |
| Pilot (a role) | Pilot (a kind of agent, or a provider) |
| An Agent acts as a Pilot | Agent and Pilot mean the same thing |
