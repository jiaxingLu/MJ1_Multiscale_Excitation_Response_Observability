# README Visual Plan

The final README is intentionally not generated automatically at this stage.

It will be co-designed after the public numerical tables and figures are frozen.

## README questions

The README must answer five questions quickly:

1. What is MERO?
2. What was done?
3. What did the data show?
4. Where are the evidence boundaries?
5. What comes next?

## Planned figure set

### Figure 1 - MERO research architecture

Purpose:
Show the v0.1 chain:

Excite -> Observe -> Identify -> Estimate

The future Interpret layer should be shown separately as post-v0.1 work.

### Figure 2 - Controlled excitation matrix

Purpose:
Show F03/F06/F08 crossed with 0.4C/0.7C AC amplitude and the six controlled
recording groups.

### Figure 3 - Measured response summary

Purpose:
Show active fundamental transfer, phase, and downstream CV-memory behavior.

Key visual contrast:
RG_004 and RG_008 have similar local F08 transfer values but substantially
different CV-memory magnitude.

### Figure 4 - Identifiability selectivity map

Purpose:
Compare the parameter change required to generate 1 mV for:

- FAST_BRANCH;
- SLOW_BRANCH;
- R0.

The plot must make frequency selectivity and amplitude-dependent signal strength
visually obvious.

### Figure 5 - Evidence-to-decision map

Purpose:
Translate the evidence into current design roles:

- F03 -> event/batch slow-branch diagnostics;
- F06 -> mixed multiband identification support;
- F08 -> gated R0 estimation.

Each role must include an evidence-level qualifier.

### Figure 6 - Evidence boundaries and roadmap

Purpose:
Show the remaining gaps:

- independent replication;
- chamber-controlled temperature;
- cross-cell validation;
- matched post-charge relaxation;
- independent estimator holdout;
- future PyBaMM electrochemical-state bridge.

## Figure rules

- English only.
- No local absolute paths.
- Every plotted number must trace to a public CSV file.
- Figure-generation code must be included.
- Avoid causal wording unless supported by the evidence level.
- Do not label the local fundamental transfer as EIS impedance.
- Do not present F03/F06/F08 as a universal optimal-frequency ranking.
