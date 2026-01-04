from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal
import json
import os

# Define a type alias for metric direction
Direction = Literal["ascending", "descending"]

@dataclass(frozen=True, slots=True)
class BackendConfig:
    """
    Immutable configuration object controlling experiment ranking,
    Kaggle submission metadata, and final packaging behavior.

    This class is intentionally immutable to prevent accidental mutation
    during the submission pipeline.
    """

    # ------------------------------------------------------------------
    # Evaluation / Ranking
    # ------------------------------------------------------------------
    metric: str
    direction: Direction

    # ------------------------------------------------------------------
    # Weights & Biases
    # ------------------------------------------------------------------
    wandb_top_n: int = field(default=10, metadata={
        "description": "Number of top W&B runs to export"
    })
    
    wandb_output_pkl: str = field(
        default="wandb_top_runs.pkl", # If you change this, make sure to update autolab/runner.py too
        metadata={
            "description": "Serialized W&B runs for autograding"
        }
    )

    # ------------------------------------------------------------------
    # Kaggle
    # ------------------------------------------------------------------
    main_competition_name: str = field(default="", metadata={"description": "Kaggle competition name for submission"})
    slack_competition_name: str = field(default="", metadata={"description": "Kaggle competition name for Slack submission"})
    
    kaggle_output_json: str = field(
        default="kaggle_data.json", # If you change this, make sure to update autolab/runner.py too
        metadata={
        "description": "Kaggle score metadata file"
        }
    )

    # ------------------------------------------------------------------
    # Final Submission Artifact
    # ------------------------------------------------------------------
    submission_zip: str = field(
        default="handin.zip", # If you change this, update 'HANDIN_FILE' in Makefile too
        metadata={
            "description": "Final ZIP file uploaded to Autolab"
        }
    )


    def __post_init__(self) -> None:
        """
        Validation post class initialization.

        Raises:
            ValueError: if wandb_top_n is not positive
            ValueError: if metric is an empty string
        """ 
        if self.main_competition_name.strip() == "":
            raise ValueError("main_competition_name must be a non-empty string")
        
        if self.slack_competition_name.strip() == "":
            raise ValueError("slack_competition_name must be a non-empty string")
              
        if self.wandb_top_n <= 0:
            raise ValueError("wandb_top_n must be a positive integer")

        if not self.metric.strip():
            raise ValueError("metric must be a non-empty string")
        
    
    def to_dict(self) -> dict[str, object]:
        """
        Convert the BackendConfig to a dictionary.

        Returns:
            dict[str, object]: Dictionary representation of the config.
        """
        return {
            "metric": self.metric,
            "direction": self.direction,
            "wandb_top_n": self.wandb_top_n,
            "wandb_output_pkl": self.wandb_output_pkl,
            "main_competition_name": self.main_competition_name,
            "slack_competition_name": self.slack_competition_name,
            "kaggle_output_json": self.kaggle_output_json,
            "submission_zip": self.submission_zip,
        }
        
    
    @classmethod
    def from_dict(cls, data: dict[str, object]) -> BackendConfig:
        """
        Create a BackendConfig instance from a dictionary.

        Args:
            data (dict[str, object]): Dictionary containing config values.
        
        Returns:
            BackendConfig: The created BackendConfig instance.
        """
        return cls(
            metric=data["metric"],
            direction=data["direction"],
            wandb_top_n=data.get("wandb_top_n", 10),
            wandb_output_pkl=data.get("wandb_output_pkl", "wandb_top_runs.pkl"),
            main_competition_name=data["main_competition_name"],
            slack_competition_name=data["slack_competition_name"],
            kaggle_output_json=data.get("kaggle_output_json", "kaggle_data.json"),
            submission_zip=data.get("submission_zip", "handin.zip"),
        )
    

# ------------------------------------------------------------------
# Load Backend Configs for Specific Assignments
# ------------------------------------------------------------------
FILE_PATH = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(FILE_PATH, "configs/hw1p2.json"), "r", encoding="utf-8") as f:
    config_data = json.load(f)
HW1P2_BACKEND_CONFIG = BackendConfig.from_dict(config_data)

with open(os.path.join(FILE_PATH, "configs/hw2p2.json"), "r", encoding="utf-8") as f:
    config_data = json.load(f)
HW2P2_BACKEND_CONFIG = BackendConfig.from_dict(config_data)

with open(os.path.join(FILE_PATH, "configs/hw3p2.json"), "r", encoding="utf-8") as f:
    config_data = json.load(f)
HW3P2_BACKEND_CONFIG = BackendConfig.from_dict(config_data)

with open(os.path.join(FILE_PATH, "configs/hw4p2.json"), "r", encoding="utf-8") as f:
    config_data = json.load(f)
HW4P2_BACKEND_CONFIG = BackendConfig.from_dict(config_data)

