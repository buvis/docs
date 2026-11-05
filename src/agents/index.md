# Agent operations

Agent operations covers how Agents receive work, execute it, communicate,
reuse knowledge, and remain observable and controlled. An Agent is the generic
actor; Pilot and Duty Controller are roles it can take on. The system includes
existing tools and components under development. It applies to both local
machines and Kubernetes environments.

- [Components](components.md): responsibilities, availability, and integration
  requirements for each part of the system.
- [Operations taxonomy](taxonomy.md): domains, terms, ownership, control,
  and execution environments.

## How the system fits together

Specflow defines requirements, design, and tasks. Autopilot accepts Flight Plans
from Specflow or other sources under the same input contract, executes them,
manages reviews, and verifies completion.
OVCAQ assigns execution to Agents acting as Pilots and supervises their sessions.
Environment Providers supply execution environments through a common contract;
Koolna provides Kubernetes environments. OVCAQ schedules work without managing
where or how those environments run. Tower presents operational state and
relays operator requests through OVCAQ. These are the intended boundaries;
the component reference distinguishes available implementations from planned
capabilities.

Skills, tools, safeguards, and quality checks support Agents in their work.
Messaging provides communication between sessions; memory and recall provide
knowledge for later reuse. Memory defaults to the current Project, with Engram
providing cross-project recall when a broader scope is selected.
These capabilities also serve Agents outside Flights and can support additional
roles as the system grows.

Hosts, model providers, and machine permission boundaries are execution
dependencies. The Supervisor is the human operator. Components can be used
independently where their contracts permit it; no single deployment must
include the entire system.
