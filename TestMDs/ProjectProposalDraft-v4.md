---
rapuma:
  document:
    author: Dennis Drescher
    date: '2026-03-25'
    title: PanelMaker Project Proposal - Draft v4
  latex:
    fontsize: 12pt
    mainfont: Gentium
    margin-bottom: 1 in
    margin-left: 1 in
    margin-right: 1 in
    margin-top: 1 in
    watermark: DRAFT
---
PanelMaker
===========

Insulation Panel Automation Proposal

AirPro Fan & Blower Co.  |  March 2026

---

## The Problem

Building insulation panels for a fan housing is entirely manual. For every fan that ships with insulation, a worker must physically measure each surface, sketch the panel shape by hand, cut a cardboard template, and use that template to cut the insulation and cover material to size. A single large fan housing can require 50 or more individual panels — each one measured and cut separately.

The process is slow, dependent on the skill of the individual doing it, difficult to train, and nearly impossible to repeat consistently from job to job. There is no documentation trail. If the worker who built the panels is unavailable, the next person starts from scratch. Cardboard templates are seldom saved, and if they are, they are fragile to store, often unlabeled, and tied to a specific configuration that may change between orders.

## The Opportunity

Every fan AirPro builds starts as a SolidWorks design file. That file already contains the exact geometry of the housing — every surface, radius, and edge. That data can greatly automate the panel-making process.

PanelMaker is a software tool being developed to take a fan housing dimensions from existing design files to create all the necessary insulation panel component data, both drawings and G-Code — with minimal user input and no manual measuring. The long-term result: a worker pulls up the housing drawing on a tablet, approves correctly drawn panel shapes, traces with a finger edge-case panels that need human input, and then confirms the configuration. From there the software drives production and creates all the necessary output data to drive a CNC laser or cutting table which will cut all the panel components. No cardboard. No tape measure. No hand calculations.

---

## Development Phases

Each phase begins with a statement of what problem it addresses and ends with a description of what the deliverable looks like. Each phase concludes with a code review and management sign-off before the next phase begins. No phase starts without approval.

### Phase 1 — Experimental & Exploratory  COMPLETE

Problem addressed:
Can the housing geometry be reliably extracted from a SolidWorks DXF export and used as a technical foundation for automation? What is possible, and what are the boundaries of the approach?

Work completed:

- Isolated clean housing geometry from DXF exports (Drive Side and Inlet Side views)

- Stripped all annotations, dimensions, title block, and border data automatically

- Produced scaled, print-ready PDF reference drawings from raw DXF input

- Tested against two housing drawings (HW1709M, HG1979M)

- Application runs on both Windows and Linux with a simple installer

End result:
Two clean PDF reference drawings per housing, generated automatically from the DXF file. The technical foundation is proven and the data pipeline is viable.

Code review / sign-off: Complete. Management presentation delivered.

### Phase 2 — DXF to Panel Drawings & Cardboard  NEXT

Problem addressed:
Can the software read a fan housing DXF file, extract geometry and produce accurate panel shape drawings in the form of a DFX file to create cardboard cutouts. These would be verified against the actual housing as well as used in panel production work.

Work to be done:

- Build v0.2.0 of the PanelMaker application — browser-based, accessible from any tablet or shop device over Wi-Fi, no installation required

- User can manually define simple panel shapes where needed

- Application automatically generates panel shapes from the DXF geometry — target: 75% or better automation rate

- Output: DXF files of panel shapes, ready for cutting

- Panel DXF drawings are sent out to an external service for cardboard cutting

- Cut cardboard pieces are compared against the actual housing to verify accuracy

End result:
Panel shape drawings generated from the housing DXF, outsourced to cardboard, and physically verified against the housing. Phase is considered complete when the output — drawings and cardboard cutouts — reaches the point where they can be used in actual production work.

Code review / sign-off: Cardboard cutouts physically verified against housing geometry and confirmed usable in production before Phase 3 begins.

### Phase 3 — Refinement & 3D Panel Output  FUTURE

Problem addressed:
How do we achieve 100% panel accuracy and extend the software to generate the complete three-dimensional panel components — outer cover, insulation pads, and inner cover — ready for production cutting?

Work to be done:

- Refine the user interface based on Phase 2 experience — better tools for user interaction and manual adjustment where automation falls short

- Improve automated shape generation toward 100% accuracy

- Phase 2 output (panel DFX drawings/prints) is integrated into the actual production workflow from the start of this phase

- Add automation to generate the full 3D panel component set for each panel: outer cover (with border and score lines and part numbers), insulation pads (per layer), and inner cover (with stapling flap)

- 3D panel component drawings sent to an external service for cutting

- Cut panels tested and refined iteratively until they meet production standards

End result:
The application produces complete, ready-to-cut drawings for all panel components. Outsourced cutting delivers panels that can be installed directly on the housing. Phase is complete when the panels coming back from the cutter are production-quality and the workflow is running as part of normal operations.

Code review / sign-off: Cut panels verified against housing and confirmed production-ready before Phase 4 begins.

### Phase 4 — In-House Production  FUTURE

Problem addressed:
How do we bring full panel production in-house, eliminate the outsourcing dependency, and drive the entire process from a single piece of equipment on the shop floor?

Work to be done:

- Evaluate and determine what cutting equipment is required for in-house production (CNC knife cutter, laser cutter, or both)

- Purchase, install, calibrate, and put equipment into production

- Update the PanelMaker application to generate GCode output for the installed equipment — knife cutter and laser cutter handled as interchangeable, isolated output modules

- Validate all GCode output through a CNC simulator before physical cutting

- Add in minimal nesting capability so increased material savings can be realized (more aggressive nesting could be considered in future maintenance updates)

- Run production through the new workflow and refine until stable

End result:
A complete in-house panel production workflow. A worker loads the housing drawing, traces or confirms the panels, and the shop equipment cuts every component automatically. The project is considered complete when 95% or more of panel components can be produced without manual intervention — edge cases may always exist, but they are the exception, not the rule.

Code review / sign-off: 95%+ automation rate confirmed in production before project is declared complete.

---

---

## Data Security

This is an AI agentic programming project. The agent will strictly follow all AirPro’s AI and programming policies. IP will be protected as follows: All processing runs on a dedicated device on the local shop network. No IP related data will be transmitted to the internet, sent to an external service, or stored in the cloud during any phase of the project or the finished application. Shop Wi-Fi will be the sole transport layer between the local server and shop devices — all AirPro drawings, DXF files, panel dimensions, and derived data will remain within the local network at all times. Any library or tool added to the project will be vetted to ensure it meets these requirements before use.

---

## Agentic Programming

Application Creation with AI


Agentic programming is a software development paradigm in which an AI model autonomously executes multi-step workflows — leveraging tools, external data sources, and embedded domain expertise — to accomplish complex goals with minimal human intervention at each step.

The inclusion of domain expertise is key: rather than operating as a general-purpose responder, the agent is guided by specialized knowledge baked into its context, system prompts, or tooling, allowing it to make informed, domain-appropriate decisions throughout the process.

---

## What Is Needed to Move Forward

-  Approval to continue development beyond the proof of concept

-  Survey of existing internal tools or processes related to panel work

-  Consultation with resident programmer to confirm platform and approach

-  Management approval of time estimate for Phase 2 before development begins

-  Access to additional DXF exports for testing

-  Identification of an outsourcing contact for cardboard and panel cutting (Phases 2 & 3)

- Equipment evaluation for in-house production (Phase 4)

- Ongoing access to the designer for DXF exports as needed

Prepared by Dennis Drescher  |  AirPro Fan & Blower Co.  |  March 2026
Development assisted by Claude Code (Anthropic)

