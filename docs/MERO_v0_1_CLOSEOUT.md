# MERO v0.1 Closeout

## Project

**MJ1 Multiscale Excitation-Response Observability (MERO)**

MERO links multiscale current excitation to measured battery response, parameter identifiability, and estimator qualification.

Core research chain:

```text
Excite -> Observe -> Identify -> Estimate
```

Electrochemical mechanism interpretation is intentionally outside the frozen v0.1 scope and is reserved for the next PyBaMM bridge.

## Controlled matrix

| Group | Band | AC | Transfer (mOhm) | CV shape RMSE (mA) | Fast branch 1 mV (%) | Slow branch 1 mV (%) | R0 1 mV (%) |
|---|---:|---:|---:|---:|---:|---:|---:|
| RG_002 | F03 | 0.4C | 68.152 | 0.579 | 1290.481 | 15.583 | 2.580 |
| RG_003 | F06 | 0.4C | 46.741 | 0.629 | 139.592 | 21.488 | 2.580 |
| RG_004 | F08 | 0.4C | 41.027 | 0.552 | 111.348 | 193.330 | 2.580 |
| RG_005 | F03 | 0.7C | 61.506 | 2.058 | 737.379 | 8.904 | 1.474 |
| RG_006 | F06 | 0.7C | 45.670 | 0.539 | 79.767 | 12.279 | 1.474 |
| RG_008 | F08 | 0.7C | 40.665 | 1.796 | 63.623 | 110.475 | 1.474 |

## Main findings

1. Active fundamental transfer magnitude follows F03 > F06 > F08 at both controlled AC amplitudes.
2. Frequency primarily determines branch-selectivity geometry in the frozen 2RC model replay.
3. Increasing AC amplitude from 0.4C to 0.7C increases practical signal strength while leaving branch-selectivity ratios nearly unchanged.
4. F03 provides the strongest slow-branch information, F06 is an intermediate mixed region, and F08 shifts information toward the fast branch.
5. R0 remains easier to observe than either dynamic RC branch in all six controlled protocol-family conditions.
6. At fixed amplitude, R0 model-replay voltage sensitivity is approximately frequency-independent across F03, F06, and F08.
7. F08 is the currently qualified excitation context for gated R0 adaptation because of the released fast-excitation gate and estimator evidence, not because R0 sensitivity is uniquely higher at F08.
8. Useful identifiability does not imply transferable continuous online adaptation. Continuous R2/tau2 adaptation remains closed.
9. The only current post-charge relaxation bridge is protocol-level evidence for the F03 0.3C+0.4C condition.

## Evidence boundaries

- No independent replication.
- No strict physical frequency causality has been established.
- No strict physical amplitude causality has been established.
- No cross-cell generalization.
- No cross-temperature generalization.
- Same protocol does not establish same physical-run identity.
- The apparent local fundamental transfer is not small-signal EIS impedance.
- The 12-hour relaxation point is a descriptive long-rest reference, not an equilibrium OCV claim.
- F01 remains exploratory and is not part of the primary controlled matrix.

## Current design interpretation

- F03: event-based or batch slow-branch diagnostics.
- F06: mixed multiband identification support.
- F08: gated R0 online-estimation support within the released v1.0 scope.

This is an evidence-graded design aid, not a universal optimal-frequency map.

## Next research phase

The next extension will add an electrochemical interpretation layer using PyBaMM, beginning with the F08 0.4C versus 0.7C contrast where the local active response is similar but downstream CV memory differs strongly.
