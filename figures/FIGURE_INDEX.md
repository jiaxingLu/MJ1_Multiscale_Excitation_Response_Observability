# README Figure Index

All README candidate figures are generated from the frozen English-only public tables in this repository.

## FIG01 - MERO research architecture

![MERO research architecture](../figures/fig01_mero_architecture.png)

**Key message:** MERO v0.1 connects excitation, observation, identifiability, and estimator qualification. Electrochemical interpretation is post-v0.1.

**Sources:**

- `docs/PUBLICATION_SCOPE.md`
- `docs/README_VISUAL_PLAN.md`

## FIG02 - Controlled excitation matrix

![Controlled excitation matrix](../figures/fig02_controlled_excitation_matrix.png)

**Key message:** The controlled core is a three-band by two-amplitude matrix with IDC fixed at 0.3C.

**Sources:**

- `data/mero_controlled_decision_matrix_v0_1.csv`

## FIG03 - Measured response summary

![Measured response summary](../figures/fig03_measured_response_summary.png)

**Key message:** Similar local electrical response can coexist with substantially different downstream CV memory. For F08, transfer differs by less than one percent while CV-shape RMSE differs by more than threefold.

**Sources:**

- `data/mero_controlled_decision_matrix_v0_1.csv`
- `data/mero_controlled_response_summary_v0_1.csv`

## FIG04 - Identifiability selectivity

![Identifiability selectivity](../figures/fig04_identifiability_selectivity.png)

**Key message:** Within frozen-model replay, F03 favors the slow branch, F06 is intermediate, and F08 shifts information toward the fast branch. Higher amplitude strengthens the signal without materially changing branch-selectivity ratios.

**Sources:**

- `data/mero_controlled_decision_matrix_v0_1.csv`
- `data/mero_identifiability_summary_v0_1.csv`

## FIG05 - Evidence-to-decision map

![Evidence-to-decision map](../figures/fig05_evidence_to_decision_map.png)

**Key message:** Current evidence supports different roles for F03, F06, and F08. Direct released estimator evidence exists only for the gated F08 R0 context.

**Sources:**

- `data/mero_controlled_decision_matrix_v0_1.csv`
- `data/mero_r0_estimator_evidence_v0_1.csv`
- `data/mero_claim_matrix_v0_1.csv`

## FIG06 - Evidence boundaries and roadmap

![Evidence boundaries and roadmap](../figures/fig06_evidence_boundaries_roadmap.png)

**Key message:** The major open gaps are physical causality, independent replication, cross-cell transfer, cross-temperature transfer, matched relaxation, and independent estimator validation.

**Sources:**

- `data/mero_claim_matrix_v0_1.csv`
- `data/mero_next_experiment_matrix_v0_1.csv`
- `docs/PUBLICATION_SCOPE.md`
