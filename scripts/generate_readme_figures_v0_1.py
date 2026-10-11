from __future__ import annotations

import csv
import hashlib
import math
import re
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# =============================================================================
# Repository layout
# =============================================================================

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"
FIGURES_DIR = ROOT / "figures"
PROVENANCE_DIR = ROOT / "provenance"

DECISION_CSV = (
    DATA_DIR
    / "mero_controlled_decision_matrix_v0_1.csv"
)

RESPONSE_CSV = (
    DATA_DIR
    / "mero_controlled_response_summary_v0_1.csv"
)

IDENTIFIABILITY_CSV = (
    DATA_DIR
    / "mero_identifiability_summary_v0_1.csv"
)

R0_ESTIMATOR_CSV = (
    DATA_DIR
    / "mero_r0_estimator_evidence_v0_1.csv"
)

RELAXATION_CSV = (
    DATA_DIR
    / "mero_relaxation_bridge_v0_1.csv"
)

CLAIM_CSV = (
    DATA_DIR
    / "mero_claim_matrix_v0_1.csv"
)

NEXT_EXPERIMENT_CSV = (
    DATA_DIR
    / "mero_next_experiment_matrix_v0_1.csv"
)

PUBLICATION_SCOPE = (
    DOCS_DIR
    / "PUBLICATION_SCOPE.md"
)

README_VISUAL_PLAN = (
    DOCS_DIR
    / "README_VISUAL_PLAN.md"
)

FIGURE_INDEX = (
    FIGURES_DIR
    / "FIGURE_INDEX.md"
)

FIGURE_MANIFEST = (
    PROVENANCE_DIR
    / "readme_figure_manifest_v0_1.csv"
)

REQUIREMENTS = (
    ROOT
    / "requirements.txt"
)


# =============================================================================
# Required decision-matrix schema
# =============================================================================

DECISION_REQUIRED_FIELDS = {
    "recording_group_id",
    "frequency_cluster_id",
    "frequency_hz",
    "dc_c",
    "ac_pk_c",
    "hppc_omega_tau1_median",
    "hppc_omega_tau2_median",
    "ekf_omega_tau1_median",
    "ekf_omega_tau2_median",
    "active_transfer_mohm",
    "active_phase_deg",
    "cv_duration_shift_pct",
    "cv_shape_rmse_ma",
    "cv_memory_morphology",
    "temperature_status",
    "relaxation_evidence_available",
    "fast_branch_1mv_requirement_pct",
    "slow_branch_1mv_requirement_pct",
    "r0_1mv_requirement_pct",
    "fast_to_slow_requirement_ratio",
    "best_dynamic_to_r0_requirement_ratio",
    "estimator_evidence_available",
    "matched_estimator_case_id",
    "final_alpha_r0",
    "estimator_rmse_change_pct",
    "primary_dynamic_role",
    "amplitude_information_status",
    "memory_amplitude_warning",
    "r0_estimator_design_role",
    "recommended_current_use",
    "independent_replication",
    "causal_status",
    "small_signal_impedance_claim",
    "cross_temperature_generalization",
    "cross_cell_generalization",
}


# =============================================================================
# Publication-language gate
# =============================================================================

CJK_PATTERN = re.compile(
    r"[\u3400-\u4DBF"
    r"\u4E00-\u9FFF"
    r"\uF900-\uFAFF"
    r"\u3040-\u309F"
    r"\u30A0-\u30FF"
    r"\uAC00-\uD7AF"
    r"\uFF0C"
    r"\u3002"
    r"\uFF01"
    r"\uFF1F"
    r"\uFF1B"
    r"\uFF1A"
    r"\u3001"
    r"\uFF08"
    r"\uFF09"
    r"\u3010"
    r"\u3011"
    r"\u300A"
    r"\u300B"
    r"\u201C"
    r"\u201D"
    r"\u2018"
    r"\u2019"
    r"\uFF05"
    r"]"
)

LOCAL_PATH_PATTERN = re.compile(
    r"(?:[A-Za-z]:[\\/](?:Users|Documents and Settings)[\\/]"
    r"|/(?:Users|home)/)",
    flags=re.I,
)


# =============================================================================
# Global plot settings
# =============================================================================

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 16,
        "axes.labelsize": 12,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "legend.fontsize": 10,
        "figure.titlesize": 19,
    }
)


# =============================================================================
# Generic helpers
# =============================================================================

def read_csv(
    path: Path,
) -> Tuple[List[str], List[Dict[str, str]]]:

    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:

        reader = csv.DictReader(
            handle
        )

        rows = list(
            reader
        )

        fields = list(
            reader.fieldnames
            or []
        )

    return fields, rows


def write_csv(
    path: Path,
    fieldnames: List[str],
    rows: List[Dict[str, object]],
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(
            rows
        )


def sha256_file(
    path: Path,
) -> str:

    digest = hashlib.sha256()

    with path.open(
        "rb"
    ) as handle:

        for block in iter(
            lambda:
                handle.read(
                    1024 * 1024
                ),
            b"",
        ):

            digest.update(
                block
            )

    return digest.hexdigest()


def as_float(
    value,
) -> float:

    return float(
        str(
            value
        ).strip()
    )


def as_optional_float(
    value,
):

    if value is None:
        return None

    text = str(
        value
    ).strip()

    if text == "":
        return None

    return float(
        text
    )


def as_bool(
    value,
) -> bool:

    return (
        str(
            value
        )
        .strip()
        .lower()
        in {
            "true",
            "1",
            "yes",
        }
    )


def relative_path(
    path: Path,
) -> str:

    return (
        path
        .relative_to(
            ROOT
        )
        .as_posix()
    )


def save_figure(
    fig,
    stem: str,
) -> Tuple[Path, Path]:

    FIGURES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    png_path = (
        FIGURES_DIR
        / f"{stem}.png"
    )

    svg_path = (
        FIGURES_DIR
        / f"{stem}.svg"
    )

    fig.savefig(
        png_path,
        dpi=220,
        bbox_inches="tight",
        facecolor="white",
    )

    fig.savefig(
        svg_path,
        bbox_inches="tight",
        facecolor="white",
    )

    plt.close(
        fig
    )

    return (
        png_path,
        svg_path,
    )


def annotate_positive_bars(
    ax,
    bars,
    digits: int,
) -> None:

    ymin, ymax = (
        ax.get_ylim()
    )

    span = (
        ymax
        - ymin
    )

    for bar in bars:

        value = (
            bar.get_height()
        )

        ax.text(
            bar.get_x()
            + bar.get_width()
            / 2,
            value
            + span * 0.015,
            f"{value:.{digits}f}",
            ha="center",
            va="bottom",
            fontsize=9.5,
        )


def annotate_negative_bars(
    ax,
    bars,
    digits: int,
) -> None:

    ymin, ymax = (
        ax.get_ylim()
    )

    span = (
        ymax
        - ymin
    )

    for bar in bars:

        value = (
            bar.get_height()
        )

        ax.text(
            bar.get_x()
            + bar.get_width()
            / 2,
            value
            + span * 0.018,
            f"{value:.{digits}f}",
            ha="center",
            va="bottom",
            fontsize=9.5,
        )


def add_card(
    ax,
    x: float,
    y: float,
    width: float,
    height: float,
    title: str,
    body: str,
    dashed: bool = False,
) -> None:

    rectangle = Rectangle(
        (
            x,
            y,
        ),
        width,
        height,
        fill=False,
        linewidth=1.8,
        linestyle=(
            "--"
            if dashed
            else "-"
        ),
        edgecolor="black",
    )

    ax.add_patch(
        rectangle
    )

    ax.text(
        x
        + width / 2,
        y
        + height * 0.78,
        title,
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
    )

    ax.text(
        x
        + width / 2,
        y
        + height * 0.42,
        body,
        ha="center",
        va="center",
        fontsize=11,
        linespacing=1.35,
    )


# =============================================================================
# Source loading
# =============================================================================

def source_check() -> None:

    sources = [
        DECISION_CSV,
        RESPONSE_CSV,
        IDENTIFIABILITY_CSV,
        R0_ESTIMATOR_CSV,
        RELAXATION_CSV,
        CLAIM_CSV,
        NEXT_EXPERIMENT_CSV,
        PUBLICATION_SCOPE,
        README_VISUAL_PLAN,
    ]

    print("")
    print(
        "SOURCE CHECK"
    )

    for path in sources:

        exists = (
            path.exists()
        )

        print(
            f"{path.name:55s} "
            f"{'FOUND' if exists else 'MISSING'}"
        )

        if not exists:

            raise FileNotFoundError(
                path
            )


def load_decision_matrix():

    fields, rows = read_csv(
        DECISION_CSV
    )

    missing = (
        DECISION_REQUIRED_FIELDS
        -
        set(
            fields
        )
    )

    if missing:

        raise RuntimeError(
            "Decision matrix missing required fields: "
            + ", ".join(
                sorted(
                    missing
                )
            )
        )

    if len(
        rows
    ) != 6:

        raise RuntimeError(
            "Expected exactly six controlled decision rows."
        )

    expected_groups = {
        "RG_002",
        "RG_003",
        "RG_004",
        "RG_005",
        "RG_006",
        "RG_008",
    }

    actual_groups = {
        row[
            "recording_group_id"
        ]
        for row in rows
    }

    if (
        actual_groups
        != expected_groups
    ):

        raise RuntimeError(
            "Controlled recording-group set mismatch."
        )

    return rows


def build_decision_index(
    rows,
):

    output = {}

    for row in rows:

        band = str(
            row[
                "frequency_cluster_id"
            ]
        ).strip()

        ac_value = (
            f"{as_float(row['ac_pk_c']):.1f}"
        )

        key = (
            band,
            ac_value,
        )

        if key in output:

            raise RuntimeError(
                f"Duplicate controlled condition: {key}"
            )

        output[
            key
        ] = row

    required_keys = {
        (
            "F03",
            "0.4",
        ),
        (
            "F06",
            "0.4",
        ),
        (
            "F08",
            "0.4",
        ),
        (
            "F03",
            "0.7",
        ),
        (
            "F06",
            "0.7",
        ),
        (
            "F08",
            "0.7",
        ),
    }

    if (
        set(
            output
        )
        != required_keys
    ):

        raise RuntimeError(
            "Controlled condition index mismatch."
        )

    return output


# =============================================================================
# Figure 1
# =============================================================================

def build_figure_01():

    fig, ax = plt.subplots(
        figsize=(
            14.5,
            5.2,
        )
    )

    ax.set_xlim(
        0,
        1,
    )

    ax.set_ylim(
        0,
        1,
    )

    ax.axis(
        "off"
    )

    fig.suptitle(
        "MERO: from excitation to qualified information",
        fontsize=22,
        y=0.97,
    )

    ax.text(
        0.46,
        0.82,
        "MERO v0.1 scope",
        ha="center",
        va="center",
        fontsize=17,
        fontweight="bold",
    )

    ax.text(
        0.91,
        0.82,
        "Post-v0.1",
        ha="center",
        va="center",
        fontsize=15,
    )

    cards = [
        (
            0.03,
            0.25,
            0.17,
            0.40,
            "EXCITE",
            "Current excitation\n\nFrequency\nAmplitude",
        ),
        (
            0.25,
            0.25,
            0.18,
            0.40,
            "OBSERVE",
            "Voltage response\n\nCV memory\n\nRelaxation",
        ),
        (
            0.48,
            0.25,
            0.18,
            0.40,
            "IDENTIFY",
            "R0\n\nFast branch\n\nSlow branch",
        ),
        (
            0.71,
            0.25,
            0.17,
            0.40,
            "ESTIMATE",
            "Qualified gated\n\nR0 adaptation",
        ),
    ]

    for (
        x,
        y,
        width,
        height,
        title,
        body,
    ) in cards:

        add_card(
            ax,
            x,
            y,
            width,
            height,
            title,
            body,
        )

    arrow_pairs = [
        (
            0.205,
            0.245,
        ),
        (
            0.435,
            0.475,
        ),
        (
            0.665,
            0.705,
        ),
    ]

    for (
        x_start,
        x_end,
    ) in arrow_pairs:

        ax.annotate(
            "",
            xy=(
                x_end,
                0.45,
            ),
            xytext=(
                x_start,
                0.45,
            ),
            arrowprops={
                "arrowstyle":
                    "->",

                "linewidth":
                    1.8,
            },
        )

    add_card(
        ax,
        0.91,
        0.25,
        0.08,
        0.40,
        "INTERPRET",
        "PyBaMM\n\nstate bridge",
        dashed=True,
    )

    ax.annotate(
        "",
        xy=(
            0.905,
            0.45,
        ),
        xytext=(
            0.885,
            0.45,
        ),
        arrowprops={
            "arrowstyle":
                "->",

            "linewidth":
                1.8,

            "linestyle":
                "--",
        },
    )

    fig.subplots_adjust(
        left=0.02,
        right=0.99,
        top=0.90,
        bottom=0.06,
    )

    return save_figure(
        fig,
        "fig01_mero_architecture",
    )


# =============================================================================
# Figure 2
# =============================================================================

def build_figure_02(
    decision_index,
):

    bands = [
        "F03",
        "F06",
        "F08",
    ]

    amplitudes = [
        "0.4",
        "0.7",
    ]

    band_frequencies = {}

    for band in bands:

        frequencies = [
            as_float(
                decision_index[
                    (
                        band,
                        amplitude,
                    )
                ][
                    "frequency_hz"
                ]
            )
            for amplitude
            in amplitudes
        ]

        band_frequencies[
            band
        ] = (
            sum(
                frequencies
            )
            / len(
                frequencies
            )
        )

    fig, ax = plt.subplots(
        figsize=(
            11.5,
            7.6,
        )
    )

    ax.set_xlim(
        0,
        3,
    )

    ax.set_ylim(
        0,
        2,
    )

    ax.set_xticks(
        [
            0.5,
            1.5,
            2.5,
        ]
    )

    ax.set_xticklabels(
        [
            (
                f"{band}\n"
                f"{band_frequencies[band]:.6f} Hz"
            )
            for band
            in bands
        ],
        fontsize=13,
    )

    ax.set_yticks(
        [
            0.5,
            1.5,
        ]
    )

    ax.set_yticklabels(
        [
            "0.4C",
            "0.7C",
        ],
        fontsize=13,
    )

    ax.set_xlabel(
        "Frequency band",
        fontsize=14,
        labelpad=12,
    )

    ax.set_ylabel(
        "AC peak amplitude",
        fontsize=14,
        labelpad=12,
    )

    fig.suptitle(
        "Controlled excitation matrix",
        fontsize=20,
        y=0.96,
    )

    fig.text(
        0.5,
        0.905,
        "IDC = 0.3C fixed",
        ha="center",
        va="center",
        fontsize=13,
    )

    for value in [
        0,
        1,
        2,
        3,
    ]:

        ax.plot(
            [
                value,
                value,
            ],
            [
                0,
                2,
            ],
            linewidth=1.7,
            color="black",
        )

    for value in [
        0,
        1,
        2,
    ]:

        ax.plot(
            [
                0,
                3,
            ],
            [
                value,
                value,
            ],
            linewidth=1.7,
            color="black",
        )

    for band_index, band in enumerate(
        bands
    ):

        for amplitude_index, amplitude in enumerate(
            amplitudes
        ):

            row = (
                decision_index[
                    (
                        band,
                        amplitude,
                    )
                ]
            )

            x = (
                band_index
                + 0.5
            )

            y = (
                amplitude_index
                + 0.5
            )

            ax.text(
                x,
                y
                + 0.10,
                row[
                    "recording_group_id"
                ],
                ha="center",
                va="center",
                fontsize=17,
                fontweight="bold",
            )

            ax.text(
                x,
                y
                - 0.08,
                (
                    f"IACpk = "
                    f"{as_float(row['ac_pk_c']):.1f}C"
                ),
                ha="center",
                va="center",
                fontsize=13,
            )

    ax.tick_params(
        length=0
    )

    for spine in (
        ax.spines.values()
    ):

        spine.set_visible(
            False
        )

    fig.subplots_adjust(
        left=0.12,
        right=0.98,
        top=0.84,
        bottom=0.16,
    )

    return save_figure(
        fig,
        "fig02_controlled_excitation_matrix",
    )


# =============================================================================
# Figure 3
# =============================================================================

def build_figure_03(
    decision_index,
):

    bands = [
        "F03",
        "F06",
        "F08",
    ]

    x_positions = [
        0,
        1,
        2,
    ]

    width = 0.34

    cycle_colors = (
        plt.rcParams[
            "axes.prop_cycle"
        ]
        .by_key()[
            "color"
        ]
    )

    color_04 = (
        cycle_colors[
            0
        ]
    )

    color_07 = (
        cycle_colors[
            1
        ]
    )

    metric_specs = [
        (
            "active_transfer_mohm",
            "Local fundamental transfer (mOhm)",
            3,
        ),
        (
            "active_phase_deg",
            "Voltage-current phase (deg)",
            2,
        ),
        (
            "cv_shape_rmse_ma",
            "CV shape RMSE (mA)",
            3,
        ),
    ]

    fig = plt.figure(
        figsize=(
            14.5,
            10.5,
        )
    )

    grid = (
        fig.add_gridspec(
            3,
            4,
            width_ratios=[
                1,
                1,
                1,
                0.95,
            ],
            hspace=0.30,
            wspace=0.45,
        )
    )

    axes = [
        fig.add_subplot(
            grid[
                row_index,
                0:3,
            ]
        )
        for row_index
        in range(
            3
        )
    ]

    callout_ax = fig.add_subplot(
        grid[
            :,
            3,
        ]
    )

    callout_ax.axis(
        "off"
    )

    fig.suptitle(
        "Measured local response and downstream CV memory",
        fontsize=20,
        y=0.98,
    )

    for ax_index, (
        ax,
        (
            field,
            ylabel,
            digits,
        ),
    ) in enumerate(
        zip(
            axes,
            metric_specs,
        )
    ):

        values_04 = [
            as_float(
                decision_index[
                    (
                        band,
                        "0.4",
                    )
                ][
                    field
                ]
            )
            for band
            in bands
        ]

        values_07 = [
            as_float(
                decision_index[
                    (
                        band,
                        "0.7",
                    )
                ][
                    field
                ]
            )
            for band
            in bands
        ]

        bars_04 = ax.bar(
            [
                x
                - width / 2
                for x in x_positions
            ],
            values_04,
            width,
            label="0.4C AC",
            color=color_04,
        )

        bars_07 = ax.bar(
            [
                x
                + width / 2
                for x in x_positions
            ],
            values_07,
            width,
            label="0.7C AC",
            color=color_07,
        )

        ax.set_ylabel(
            ylabel,
            fontsize=12,
        )

        ax.grid(
            axis="y",
            alpha=0.20,
        )

        if field == "active_phase_deg":

            ymin = (
                min(
                    values_04
                    + values_07
                )
                * 1.12
            )

            ax.set_ylim(
                ymin,
                1.2,
            )

            annotate_negative_bars(
                ax,
                bars_04,
                digits,
            )

            annotate_negative_bars(
                ax,
                bars_07,
                digits,
            )

        else:

            ymax = (
                max(
                    values_04
                    + values_07
                )
                * 1.16
            )

            ax.set_ylim(
                0,
                ymax,
            )

            annotate_positive_bars(
                ax,
                bars_04,
                digits,
            )

            annotate_positive_bars(
                ax,
                bars_07,
                digits,
            )

        if ax_index == 0:

            ax.legend(
                loc="upper right",
                ncol=2,
                frameon=True,
            )

        if ax_index < 2:

            ax.set_xticks(
                x_positions
            )

            ax.set_xticklabels(
                []
            )

        else:

            ax.set_xticks(
                x_positions,
                bands,
            )

            ax.set_xlabel(
                "Frequency band",
                fontsize=12,
            )

    f08_04 = (
        decision_index[
            (
                "F08",
                "0.4",
            )
        ]
    )

    f08_07 = (
        decision_index[
            (
                "F08",
                "0.7",
            )
        ]
    )

    transfer_04 = as_float(
        f08_04[
            "active_transfer_mohm"
        ]
    )

    transfer_07 = as_float(
        f08_07[
            "active_transfer_mohm"
        ]
    )

    cv_04 = as_float(
        f08_04[
            "cv_shape_rmse_ma"
        ]
    )

    cv_07 = as_float(
        f08_07[
            "cv_shape_rmse_ma"
        ]
    )

    transfer_difference_pct = (
        (
            transfer_07
            - transfer_04
        )
        / transfer_04
        * 100.0
    )

    cv_ratio = (
        cv_07
        / cv_04
    )

    callout_ax.text(
        0.5,
        0.90,
        "F08 key contrast",
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
    )

    callout_ax.text(
        0.5,
        0.72,
        (
            "Local transfer\n\n"
            f"{transfer_04:.3f} vs "
            f"{transfer_07:.3f} mOhm\n\n"
            f"Difference: "
            f"{transfer_difference_pct:+.2f}%"
        ),
        ha="center",
        va="center",
        fontsize=13,
        bbox={
            "boxstyle":
                "round,pad=0.5",

            "facecolor":
                "white",

            "edgecolor":
                "black",
        },
    )

    callout_ax.text(
        0.5,
        0.43,
        (
            "CV-memory magnitude\n\n"
            f"{cv_04:.3f} vs "
            f"{cv_07:.3f} mA\n\n"
            f"Ratio: "
            f"{cv_ratio:.2f}x"
        ),
        ha="center",
        va="center",
        fontsize=13,
        bbox={
            "boxstyle":
                "round,pad=0.5",

            "facecolor":
                "white",

            "edgecolor":
                "black",
        },
    )

    callout_ax.text(
        0.5,
        0.14,
        (
            "Similar local electrical response\n"
            "does not imply similar downstream\n"
            "CV memory."
        ),
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
        linespacing=1.35,
    )

    fig.subplots_adjust(
        left=0.07,
        right=0.98,
        top=0.93,
        bottom=0.07,
    )

    return save_figure(
        fig,
        "fig03_measured_response_summary",
    )


# =============================================================================
# Figure 4
# =============================================================================

def build_figure_04(
    decision_index,
):

    bands = [
        "F03",
        "F06",
        "F08",
    ]

    x_positions = [
        0,
        1,
        2,
    ]

    cycle_colors = (
        plt.rcParams[
            "axes.prop_cycle"
        ]
        .by_key()[
            "color"
        ]
    )

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(
            14.5,
            7.1,
        ),
        sharey=True,
    )

    fig.suptitle(
        (
            "Model replay: branch selectivity varies across "
            "frequency bands; amplitude scales sensitivity"
        ),
        fontsize=18,
        y=0.97,
    )

    for (
        ax,
        amplitude,
    ) in zip(
        axes,
        [
            "0.4",
            "0.7",
        ],
    ):

        fast_values = [
            as_float(
                decision_index[
                    (
                        band,
                        amplitude,
                    )
                ][
                    "fast_branch_1mv_requirement_pct"
                ]
            )
            for band
            in bands
        ]

        slow_values = [
            as_float(
                decision_index[
                    (
                        band,
                        amplitude,
                    )
                ][
                    "slow_branch_1mv_requirement_pct"
                ]
            )
            for band
            in bands
        ]

        r0_values = [
            as_float(
                decision_index[
                    (
                        band,
                        amplitude,
                    )
                ][
                    "r0_1mv_requirement_pct"
                ]
            )
            for band
            in bands
        ]

        ratios = [
            as_float(
                decision_index[
                    (
                        band,
                        amplitude,
                    )
                ][
                    "fast_to_slow_requirement_ratio"
                ]
            )
            for band
            in bands
        ]

        all_values = (
            fast_values
            + slow_values
            + r0_values
        )

        plot_min = (
            min(
                all_values
            )
            / 1.45
        )

        plot_max = (
            max(
                all_values
            )
            * 2.3
        )

        ax.plot(
            x_positions,
            fast_values,
            marker="o",
            linewidth=2,
            label="Fast branch (R1, tau1)",
            color=cycle_colors[
                0
            ],
        )

        ax.plot(
            x_positions,
            slow_values,
            marker="o",
            linewidth=2,
            label="Slow branch (R2, tau2)",
            color=cycle_colors[
                1
            ],
        )

        ax.plot(
            x_positions,
            r0_values,
            marker="o",
            linewidth=2,
            label="R0",
            color=cycle_colors[
                2
            ],
        )

        ax.set_yscale(
            "log"
        )

        ax.set_ylim(
            plot_min,
            plot_max,
        )

        ax.set_xticks(
            x_positions,
            bands,
        )

        ax.set_xlabel(
            "Frequency band"
        )

        ax.set_title(
            f"AC amplitude = {amplitude}C",
            pad=12,
        )

        ax.grid(
            axis="y",
            alpha=0.22,
        )

        for index, ratio in enumerate(
            ratios
        ):

            ax.text(
                x_positions[
                    index
                ],
                0.88,
                f"F/S = {ratio:.3g}",
                transform=ax.get_xaxis_transform(),
                ha="center",
                va="center",
                fontsize=10,
                bbox={
                    "boxstyle":
                        "round,pad=0.18",

                    "facecolor":
                        "white",

                    "edgecolor":
                        "none",

                    "alpha":
                        0.88,
                },
            )

        ax.text(
            0.03,
            0.035,
            (
                "Lower values = stronger "
                "voltage sensitivity"
            ),
            transform=ax.transAxes,
            ha="left",
            va="bottom",
            fontsize=10.3,
            bbox={
                "boxstyle":
                    "round,pad=0.20",

                "facecolor":
                    "white",

                "edgecolor":
                    "none",

                "alpha":
                    0.90,
            },
        )

    axes[
        0
    ].set_ylabel(
        (
            "Parameter change required "
            "for 1 mV (%)"
        )
    )

    handles, labels = (
        axes[
            0
        ].get_legend_handles_labels()
    )

    fig.legend(
        handles,
        labels,
        loc="lower center",
        bbox_to_anchor=(
            0.5,
            0.025,
        ),
        ncol=3,
        frameon=True,
    )

    fig.subplots_adjust(
        left=0.075,
        right=0.985,
        top=0.84,
        bottom=0.22,
        wspace=0.12,
    )

    return save_figure(
        fig,
        "fig04_identifiability_selectivity",
    )


# =============================================================================
# Figure 5
# =============================================================================

def build_figure_05(
    decision_index,
):

    bands = [
        "F03",
        "F06",
        "F08",
    ]

    fig, ax = plt.subplots(
        figsize=(
            13.5,
            6.4,
        )
    )

    ax.set_xlim(
        0,
        1,
    )

    ax.set_ylim(
        0,
        1,
    )

    ax.axis(
        "off"
    )

    fig.suptitle(
        "Evidence-to-decision map",
        fontsize=21,
        y=0.96,
    )

    band_cards = []

    for band in bands:

        row_04 = (
            decision_index[
                (
                    band,
                    "0.4",
                )
            ]
        )

        row_07 = (
            decision_index[
                (
                    band,
                    "0.7",
                )
            ]
        )

        ratios = [
            as_float(
                row_04[
                    "fast_to_slow_requirement_ratio"
                ]
            ),
            as_float(
                row_07[
                    "fast_to_slow_requirement_ratio"
                ]
            ),
        ]

        ratio_mean = (
            sum(
                ratios
            )
            / len(
                ratios
            )
        )

        fast_range = sorted(
            [
                as_float(
                    row_04[
                        "fast_branch_1mv_requirement_pct"
                    ]
                ),
                as_float(
                    row_07[
                        "fast_branch_1mv_requirement_pct"
                    ]
                ),
            ]
        )

        slow_range = sorted(
            [
                as_float(
                    row_04[
                        "slow_branch_1mv_requirement_pct"
                    ]
                ),
                as_float(
                    row_07[
                        "slow_branch_1mv_requirement_pct"
                    ]
                ),
            ]
        )

        if band == "F03":

            body = (
                "Event/batch\n"
                "slow-branch diagnostics\n\n"
                "Model-replay evidence\n\n"
                f"F/S requirement ratio: "
                f"{ratio_mean:.2f}\n"
                f"Slow 1 mV: "
                f"{slow_range[0]:.1f}-"
                f"{slow_range[1]:.1f}%"
            )

        elif band == "F06":

            body = (
                "Mixed multiband\n"
                "identification support\n\n"
                "Model-replay evidence\n\n"
                f"F/S requirement ratio: "
                f"{ratio_mean:.2f}\n"
                f"Fast 1 mV: "
                f"{fast_range[0]:.1f}-"
                f"{fast_range[1]:.1f}%\n"
                f"Slow 1 mV: "
                f"{slow_range[0]:.1f}-"
                f"{slow_range[1]:.1f}%"
            )

        else:

            alpha_values = [
                value
                for value in [
                    as_optional_float(
                        row_04[
                            "final_alpha_r0"
                        ]
                    ),
                    as_optional_float(
                        row_07[
                            "final_alpha_r0"
                        ]
                    ),
                ]
                if value is not None
            ]

            rmse_values = [
                value
                for value in [
                    as_optional_float(
                        row_04[
                            "estimator_rmse_change_pct"
                        ]
                    ),
                    as_optional_float(
                        row_07[
                            "estimator_rmse_change_pct"
                        ]
                    ),
                ]
                if value is not None
            ]

            alpha_text = (
                "NA"
                if not alpha_values
                else
                (
                    f"{min(alpha_values):.4f}-"
                    f"{max(alpha_values):.4f}"
                )
            )

            rmse_text = (
                "NA"
                if not rmse_values
                else
                (
                    f"{min(rmse_values):.2f}% to "
                    f"{max(rmse_values):.2f}%"
                )
            )

            body = (
                "Gated R0\n"
                "online estimation\n\n"
                "Released estimator evidence\n\n"
                f"F/S requirement ratio: "
                f"{ratio_mean:.3f}\n"
                f"alpha_R0: "
                f"{alpha_text}\n"
                f"RMSE change: "
                f"{rmse_text}"
            )

        band_cards.append(
            (
                band,
                body,
            )
        )

    x_positions = [
        0.04,
        0.36,
        0.68,
    ]

    for (
        x,
        (
            band,
            body,
        ),
    ) in zip(
        x_positions,
        band_cards,
    ):

        add_card(
            ax,
            x,
            0.18,
            0.27,
            0.62,
            band,
            body,
        )

    ax.text(
        0.5,
        0.07,
        (
            "These are current evidence-graded roles, "
            "not universal optimal-frequency claims."
        ),
        ha="center",
        va="center",
        fontsize=12.5,
    )

    fig.subplots_adjust(
        left=0.02,
        right=0.98,
        top=0.90,
        bottom=0.05,
    )

    return save_figure(
        fig,
        "fig05_evidence_to_decision_map",
    )


# =============================================================================
# Figure 6
# =============================================================================

def build_figure_06():

    claim_fields, claim_rows = read_csv(
        CLAIM_CSV
    )

    experiment_fields, experiment_rows = read_csv(
        NEXT_EXPERIMENT_CSV
    )

    required_claim_fields = {
        "claim_id",
        "claim",
        "status",
        "evidence_scope",
        "boundary",
    }

    required_experiment_fields = {
        "experiment_id",
        "priority",
        "experiment_name",
        "decision_use",
    }

    if not required_claim_fields.issubset(
        set(
            claim_fields
        )
    ):

        raise RuntimeError(
            "Claim matrix schema mismatch."
        )

    if not required_experiment_fields.issubset(
        set(
            experiment_fields
        )
    ):

        raise RuntimeError(
            "Next-experiment matrix schema mismatch."
        )

    claim_map = {
        row[
            "claim_id"
        ]:
            row
        for row in claim_rows
    }

    boundary_specs = [
        (
            "C16",
            "Frequency / amplitude causality",
        ),
        (
            "C17",
            "Cross-temperature generalization",
        ),
        (
            "C18",
            "Cross-cell generalization",
        ),
        (
            "C15",
            "12 h = equilibrium OCV",
        ),
        (
            "C19",
            "Local transfer = small-signal EIS",
        ),
    ]

    fig, ax = plt.subplots(
        figsize=(
            15.0,
            9.2,
        )
    )

    ax.set_xlim(
        0,
        1,
    )

    ax.set_ylim(
        0,
        1,
    )

    ax.axis(
        "off"
    )

    fig.suptitle(
        (
            "What v0.1 does not establish, "
            "and what must come next"
        ),
        fontsize=21,
        y=0.97,
    )

    ax.text(
        0.245,
        0.885,
        "Current evidence boundaries",
        ha="center",
        va="center",
        fontsize=17,
        fontweight="bold",
    )

    ax.text(
        0.75,
        0.885,
        "Next experimental roadmap",
        ha="center",
        va="center",
        fontsize=17,
        fontweight="bold",
    )

    left_x = 0.03
    left_width = 0.43
    left_height = 0.125
    left_top = 0.70
    left_gap = 0.025

    for index, (
        claim_id,
        label,
    ) in enumerate(
        boundary_specs
    ):

        row = (
            claim_map[
                claim_id
            ]
        )

        y = (
            left_top
            - index
            * (
                left_height
                + left_gap
            )
        )

        rectangle = Rectangle(
            (
                left_x,
                y,
            ),
            left_width,
            left_height,
            fill=False,
            linewidth=1.7,
            edgecolor="black",
        )

        ax.add_patch(
            rectangle
        )

        ax.text(
            left_x
            + left_width / 2,
            y
            + left_height * 0.76,
            label,
            ha="center",
            va="center",
            fontsize=12.5,
            fontweight="bold",
        )

        ax.text(
            left_x
            + left_width / 2,
            y
            + left_height * 0.50,
            row[
                "status"
            ].replace(
                "_",
                " ",
            ),
            ha="center",
            va="center",
            fontsize=11.3,
        )

        boundary_text = (
            row[
                "boundary"
            ]
        )

        boundary_text = (
            boundary_text
            .replace(
                (
                    "Causality is not established because "
                    "independent replication and full confound "
                    "control are absent."
                ),
                (
                    "Causality is not established because "
                    "independent replication\n"
                    "and full confound control are absent."
                ),
            )
            .replace(
                (
                    "This terminology is not allowed; "
                    "the result is reported as a local "
                    "fundamental transfer quantity."
                ),
                (
                    "This terminology is not allowed; "
                    "the result is reported as a local\n"
                    "fundamental transfer quantity."
                ),
            )
        )

        ax.text(
            left_x
            + left_width / 2,
            y
            + left_height * 0.20,
            boundary_text,
            ha="center",
            va="center",
            fontsize=9.1,
            linespacing=1.20,
        )

    experiments_sorted = sorted(
        experiment_rows,
        key=lambda row: (
            row[
                "priority"
            ],
            row[
                "experiment_id"
            ],
        ),
    )

    right_x = 0.53
    right_width = 0.44
    right_height = 0.118
    right_top = 0.70
    right_gap = 0.025

    for index, row in enumerate(
        experiments_sorted
    ):

        y = (
            right_top
            - index
            * (
                right_height
                + right_gap
            )
        )

        rectangle = Rectangle(
            (
                right_x,
                y,
            ),
            right_width,
            right_height,
            fill=False,
            linewidth=1.7,
            edgecolor="black",
        )

        ax.add_patch(
            rectangle
        )

        ax.text(
            right_x
            + right_width / 2,
            y
            + right_height * 0.66,
            (
                f"{row['priority']} | "
                f"{row['experiment_name']}"
            ),
            ha="center",
            va="center",
            fontsize=10.7,
            fontweight="bold",
            wrap=True,
        )

        ax.text(
            right_x
            + right_width / 2,
            y
            + right_height * 0.26,
            row[
                "decision_use"
            ],
            ha="center",
            va="center",
            fontsize=9.4,
            wrap=True,
        )

    pybamm_rectangle = Rectangle(
        (
            right_x,
            0.025,
        ),
        right_width,
        0.080,
        fill=False,
        linewidth=1.8,
        linestyle="--",
        edgecolor="black",
    )

    ax.add_patch(
        pybamm_rectangle
    )

    ax.text(
        right_x
        + right_width / 2,
        0.065,
        (
            "Post-v0.1 extension\n"
            "PyBaMM electrochemical-state bridge"
        ),
        ha="center",
        va="center",
        fontsize=11.2,
        fontweight="bold",
    )

    fig.subplots_adjust(
        left=0.02,
        right=0.99,
        top=0.90,
        bottom=0.025,
    )

    return save_figure(
        fig,
        "fig06_evidence_boundaries_roadmap",
    )


# =============================================================================
# Figure index and provenance
# =============================================================================

def write_figure_index(
    figure_rows,
) -> None:

    lines = [
        "# README Figure Index",
        "",
        (
            "All README candidate figures are generated from "
            "the frozen English-only public tables in this repository."
        ),
        "",
    ]

    for row in figure_rows:

        png_relative = relative_path(
            row[
                "png"
            ]
        )

        lines.extend(
            [
                (
                    f"## {row['figure_id']} - "
                    f"{row['title']}"
                ),
                "",
                (
                    f"![{row['title']}]"
                    f"(../{png_relative})"
                ),
                "",
                (
                    f"**Key message:** "
                    f"{row['key_message']}"
                ),
                "",
                "**Sources:**",
                "",
            ]
        )

        for source in row[
            "sources"
        ]:

            lines.append(
                f"- `{relative_path(source)}`"
            )

        lines.append(
            ""
        )

    FIGURE_INDEX.write_text(
        "\n".join(
            lines
        ),
        encoding="utf-8",
    )


def write_figure_manifest(
    figure_rows,
) -> None:

    output_rows = []

    for row in figure_rows:

        source_files = [
            relative_path(
                source
            )
            for source
            in row[
                "sources"
            ]
        ]

        source_hashes = [
            (
                f"{relative_path(source)}:"
                f"{sha256_file(source)}"
            )
            for source
            in row[
                "sources"
            ]
        ]

        output_rows.append(
            {
                "figure_id":
                    row[
                        "figure_id"
                    ],

                "title":
                    row[
                        "title"
                    ],

                "png_path":
                    relative_path(
                        row[
                            "png"
                        ]
                    ),

                "png_sha256":
                    sha256_file(
                        row[
                            "png"
                        ]
                    ),

                "svg_path":
                    relative_path(
                        row[
                            "svg"
                        ]
                    ),

                "svg_sha256":
                    sha256_file(
                        row[
                            "svg"
                        ]
                    ),

                "source_files":
                    ";".join(
                        source_files
                    ),

                "source_signatures":
                    ";".join(
                        source_hashes
                    ),

                "key_message":
                    row[
                        "key_message"
                    ],

                "publication_status":
                    "README_CANDIDATE",
            }
        )

    write_csv(
        FIGURE_MANIFEST,
        [
            "figure_id",
            "title",
            "png_path",
            "png_sha256",
            "svg_path",
            "svg_sha256",
            "source_files",
            "source_signatures",
            "key_message",
            "publication_status",
        ],
        output_rows,
    )


def write_requirements() -> None:

    REQUIREMENTS.write_text(
        (
            f"matplotlib=="
            f"{matplotlib.__version__}\n"
        ),
        encoding="utf-8",
    )


# =============================================================================
# Publication gate
# =============================================================================

def run_publication_gate():

    text_suffixes = {
        ".py",
        ".md",
        ".csv",
        ".svg",
        ".txt",
        ".yml",
        ".yaml",
        ".toml",
        ".cff",
    }

    excluded_directories = {
        ".git",
        ".venv",
        "__pycache__",
    }

    rows = []

    for path in sorted(
        ROOT.rglob(
            "*"
        ),
        key=lambda item:
            str(
                item
            ).lower(),
    ):

        if not path.is_file():

            continue

        relative = (
            path.relative_to(
                ROOT
            )
        )

        if any(
            part
            in excluded_directories
            for part
            in relative.parts
        ):

            continue

        path_text = (
            relative.as_posix()
        )

        path_cjk_count = len(
            CJK_PATTERN.findall(
                path_text
            )
        )

        content_cjk_count = 0
        local_path_count = 0

        if (
            path.suffix.lower()
            in text_suffixes
            or path.name
            in {
                ".gitignore",
                ".gitattributes",
                "requirements.txt",
            }
        ):

            text = path.read_text(
                encoding="utf-8",
                errors="replace",
            )

            content_cjk_count = len(
                CJK_PATTERN.findall(
                    text
                )
            )

            local_path_count = len(
                LOCAL_PATH_PATTERN.findall(
                    text
                )
            )

        status = (
            "PASS"
            if (
                path_cjk_count == 0
                and
                content_cjk_count == 0
                and
                local_path_count == 0
            )
            else
            "FAIL"
        )

        rows.append(
            {
                "relative_path":
                    path_text,

                "path_cjk_count":
                    path_cjk_count,

                "content_cjk_count":
                    content_cjk_count,

                "local_absolute_path_count":
                    local_path_count,

                "status":
                    status,
            }
        )

    return rows


# =============================================================================
# Main
# =============================================================================

def main() -> None:

    print(
        "=" * 120
    )

    print(
        "MERO v0.1 | README FIGURE GENERATION"
    )

    print(
        "=" * 120
    )

    source_check()

    decision_rows = (
        load_decision_matrix()
    )

    decision_index = (
        build_decision_index(
            decision_rows
        )
    )

    print("")
    print(
        "CONTROLLED CONDITION INDEX"
    )

    for key in sorted(
        decision_index
    ):

        print(
            f"{key[0]} / AC={key[1]}C -> "
            f"{decision_index[key]['recording_group_id']}"
        )

    print("")
    print(
        "GENERATE FIGURES"
    )

    figure_rows = []

    png, svg = (
        build_figure_01()
    )

    figure_rows.append(
        {
            "figure_id":
                "FIG01",

            "title":
                "MERO research architecture",

            "png":
                png,

            "svg":
                svg,

            "sources":
                [
                    PUBLICATION_SCOPE,
                    README_VISUAL_PLAN,
                ],

            "key_message":
                (
                    "MERO v0.1 connects excitation, observation, "
                    "identifiability, and estimator qualification. "
                    "Electrochemical interpretation is post-v0.1."
                ),
        }
    )

    print(
        "FIG01: PASS"
    )

    png, svg = (
        build_figure_02(
            decision_index
        )
    )

    figure_rows.append(
        {
            "figure_id":
                "FIG02",

            "title":
                "Controlled excitation matrix",

            "png":
                png,

            "svg":
                svg,

            "sources":
                [
                    DECISION_CSV,
                ],

            "key_message":
                (
                    "The controlled core is a three-band by "
                    "two-amplitude matrix with IDC fixed at 0.3C."
                ),
        }
    )

    print(
        "FIG02: PASS"
    )

    png, svg = (
        build_figure_03(
            decision_index
        )
    )

    figure_rows.append(
        {
            "figure_id":
                "FIG03",

            "title":
                "Measured response summary",

            "png":
                png,

            "svg":
                svg,

            "sources":
                [
                    DECISION_CSV,
                    RESPONSE_CSV,
                ],

            "key_message":
                (
                    "Similar local electrical response can coexist "
                    "with substantially different downstream CV memory. "
                    "For F08, transfer differs by less than one percent "
                    "while CV-shape RMSE differs by more than threefold."
                ),
        }
    )

    print(
        "FIG03: PASS"
    )

    png, svg = (
        build_figure_04(
            decision_index
        )
    )

    figure_rows.append(
        {
            "figure_id":
                "FIG04",

            "title":
                "Identifiability selectivity",

            "png":
                png,

            "svg":
                svg,

            "sources":
                [
                    DECISION_CSV,
                    IDENTIFIABILITY_CSV,
                ],

            "key_message":
                (
                    "Within frozen-model replay, F03 favors the slow branch, "
                    "F06 is intermediate, and F08 shifts information toward "
                    "the fast branch. Higher amplitude strengthens the signal "
                    "without materially changing branch-selectivity ratios."
                ),
        }
    )

    print(
        "FIG04: PASS"
    )

    png, svg = (
        build_figure_05(
            decision_index
        )
    )

    figure_rows.append(
        {
            "figure_id":
                "FIG05",

            "title":
                "Evidence-to-decision map",

            "png":
                png,

            "svg":
                svg,

            "sources":
                [
                    DECISION_CSV,
                    R0_ESTIMATOR_CSV,
                    CLAIM_CSV,
                ],

            "key_message":
                (
                    "Current evidence supports different roles for "
                    "F03, F06, and F08. Direct released estimator evidence "
                    "exists only for the gated F08 R0 context."
                ),
        }
    )

    print(
        "FIG05: PASS"
    )

    png, svg = (
        build_figure_06()
    )

    figure_rows.append(
        {
            "figure_id":
                "FIG06",

            "title":
                "Evidence boundaries and roadmap",

            "png":
                png,

            "svg":
                svg,

            "sources":
                [
                    CLAIM_CSV,
                    NEXT_EXPERIMENT_CSV,
                    PUBLICATION_SCOPE,
                ],

            "key_message":
                (
                    "The major open gaps are physical causality, "
                    "independent replication, cross-cell transfer, "
                    "cross-temperature transfer, matched relaxation, "
                    "and independent estimator validation."
                ),
        }
    )

    print(
        "FIG06: PASS"
    )

    write_figure_index(
        figure_rows
    )

    write_figure_manifest(
        figure_rows
    )

    write_requirements()

    print("")
    print(
        "FIGURE OUTPUTS"
    )

    for row in figure_rows:

        print(
            relative_path(
                row[
                    "png"
                ]
            )
        )

        print(
            relative_path(
                row[
                    "svg"
                ]
            )
        )

    print("")
    print(
        "TRACEABILITY OUTPUTS"
    )

    print(
        relative_path(
            FIGURE_INDEX
        )
    )

    print(
        relative_path(
            FIGURE_MANIFEST
        )
    )

    print(
        relative_path(
            REQUIREMENTS
        )
    )

    print("")
    print(
        "RUN FIGURE PUBLICATION GATE"
    )

    gate_rows = (
        run_publication_gate()
    )

    failures = [
        row
        for row in gate_rows
        if row[
            "status"
        ]
        == "FAIL"
    ]

    total_path_cjk = sum(
        int(
            row[
                "path_cjk_count"
            ]
        )
        for row in gate_rows
    )

    total_content_cjk = sum(
        int(
            row[
                "content_cjk_count"
            ]
        )
        for row in gate_rows
    )

    total_local_paths = sum(
        int(
            row[
                "local_absolute_path_count"
            ]
        )
        for row in gate_rows
    )

    print(
        f"Files checked: "
        f"{len(gate_rows)}"
    )

    print(
        f"Path CJK count: "
        f"{total_path_cjk}"
    )

    print(
        f"Content CJK count: "
        f"{total_content_cjk}"
    )

    print(
        f"Local absolute path count: "
        f"{total_local_paths}"
    )

    print(
        f"Failed files: "
        f"{len(failures)}"
    )

    if failures:

        print("")

        for row in failures:

            print(
                f"FAIL | "
                f"{row['relative_path']} | "
                f"path_cjk="
                f"{row['path_cjk_count']} | "
                f"content_cjk="
                f"{row['content_cjk_count']} | "
                f"local_paths="
                f"{row['local_absolute_path_count']}"
            )

    print("")

    if failures:

        print(
            "FINAL README FIGURE BUILD STATUS: FAIL"
        )

        print(
            "README design: BLOCKED"
        )

    else:

        print(
            "FINAL README FIGURE BUILD STATUS: PASS"
        )

        print(
            "English-only figure gate: PASS"
        )

        print(
            "Local-path privacy gate: PASS"
        )

        print(
            "Figure traceability: PASS"
        )

        print(
            "Final README.md: STILL PENDING MANUAL REVIEW"
        )

        print("")

        print(
            "Next stage: review the final six figures "
            "before composing README.md."
        )

        print(
            "Git initialization remains blocked "
            "until README approval."
        )

    print(
        "=" * 120
    )


if __name__ == "__main__":
    main()