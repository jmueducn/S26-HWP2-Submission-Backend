from __future__ import annotations

import torch
from torch import nn
from typing import Dict, Any
import logging

log = logging.getLogger(__name__)


###############################################################################
# Errors
###############################################################################

class ModelMetadataError(RuntimeError):
    """Raised when model metadata cannot be constructed."""


###############################################################################
# Public API
###############################################################################

def build_model_metadata(model: nn.Module, param_limit: int) -> Dict[str, Any]:
    """
    Build a deterministic, serializable metadata dictionary for a PyTorch model.

    This metadata is used for submission auditing and grading and must:
      • Be side-effect free
      • Be JSON-serializable
      • Fail early on invalid models

    Args:
        model (nn.Module): The model to inspect
        param_limit (int): Maximum allowed number of trainable parameters   
    Returns:
        Dict[str, Any]: Model metadata
    """

    if not isinstance(model, nn.Module):
        raise ModelMetadataError(
            "Invalid model object.\n"
            "👉 Expected a torch.nn.Module instance."
        )

    try:
        parameters = list(model.parameters())
    except Exception as exc:
        raise ModelMetadataError(
            "Failed to access model parameters.\n"
            "👉 Ensure your model is a valid nn.Module."
        ) from exc

    if not parameters:
        raise ModelMetadataError(
            "Model contains no parameters.\n"
            "👉 Ensure your model defines trainable layers."
        )

    trainable_params = [
        p for p in parameters if p.requires_grad
    ]

    if sum(p.numel() for p in trainable_params) > param_limit:
        raise ModelMetadataError(
            f"Model exceeds parameter limit of {param_limit}.\n"
            "👉 Reduce model size or complexity."
        )

    metadata: Dict[str, Any] = {
        "schema_version": "1.0",

        "model": {
            "class_name": model.__class__.__name__,
            "module": model.__class__.__module__,
            "repr": repr(model),
            "trainable_parameters": sum(p.numel() for p in trainable_params),
            "total_parameters": sum(p.numel() for p in parameters),
        },

        "framework": {
            "torch_version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "cuda_version": torch.version.cuda,
        },
    }

    log.info(
        "Model metadata built: %d trainable parameters",
        metadata["model"]["trainable_parameters"],
    )

    return metadata
