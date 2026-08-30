# Agent Trajectories

This directory contains representative execution traces for Reality Compiler agents.

Trajectories record:
- agent role
- model used
- evidence supplied to the agent
- structured output
- validation result
- deterministic solver result
- repair result

They do not contain private chain-of-thought or API secrets.

## Current agents

1. Constraint Extraction Agent
   - Converts raw organizational evidence into formal constraint candidates.
   - Output is schema validated before entering the Reality Engine.

Additional agent trajectories will be added as the architecture evolves.