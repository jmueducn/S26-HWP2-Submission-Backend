from __future__ import annotations

import logging
from typing import Any, Dict, List
import wandb
from wandb import Run
from wandb.errors import AuthenticationError, CommError

log = logging.getLogger(__name__)


###############################################################################
# Errors
###############################################################################

class WandBExportError(RuntimeError):
    """Raised when exporting Weights & Biases runs fails."""


###############################################################################
# Public API
###############################################################################

def export_top_wandb_runs(
    *,
    api_key: str,
    entity: str,
    project: str,
    acknowledged: bool,
    top_n: int,
) -> List[Dict[str, Any]]:
    """
    Export the top-N W&B runs sorted by a given metric.

    Guarantees:
      • W&B authentication succeeds
      • Runs exist for the project

    Returns:
        A list of fully-serializable dictionaries.
    """

    if not acknowledged:
        raise WandBExportError(
            "Acknowledgement not accepted.\n"
            "👉 You must accept the acknowledgement before exporting W&B runs."
        )

    if top_n <= 0:
        raise WandBExportError(
            "Invalid configuration: top_n must be a positive integer."
        )

    log.info("Authenticating with Weights & Biases…")

    try:
        wandb.login(key=api_key)
    except AuthenticationError as exc:
        raise WandBExportError(
            "Failed to authenticate with Weights & Biases.\n"
            "👉 Check that your API key is correct and active."
        ) from exc

    api = wandb.Api()
    project_path = f"{entity}/{project}"
    log.info("Fetching runs for project %s", project_path)

    try:
        runs = api.runs(project_path, order="+created_at")
    except CommError as exc:
        raise WandBExportError(
            f"Unable to access W&B project '{project_path}'.\n"
            "👉 Check that the entity and project names are correct."
        ) from exc

    if not runs:
        raise WandBExportError(
            f"No runs found for project '{project_path}'.\n"
            "👉 Ensure that at least one run has been logged."
        )

    selected = runs[: min(top_n, len(runs))]

    records: List[Dict[str, Any]] = []
    for run in selected:
        record = _serialize_run(run)
        records.append(record)
    log.info("✓ Exported %d W&B run(s)", len(records))
    return records


###############################################################################
# Helpers
###############################################################################

def _serialize_run(run: Run) -> Dict[str, Any]:
    """
    Serialize a W&B run into a fully JSON-serializable dictionary.
    """
    record: Dict[str, Any] = {
        "id": run.id,
        "name": run.name,
        "state": run.state,
        "created_at": str(run.created_at),
        "config": dict(run.config),
        "tags": list(run.tags),
    }

    try:
        record["history"] = (
            run.history(samples=1000, pandas=True)
            .to_dict(orient="records")
        )
    except Exception as exc:
        record["history"] = {
            "error": str(exc),
            "message": "History could not be retrieved for this run.",
        }

    return record
