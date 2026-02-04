from __future__ import annotations

import os
import logging
from typing import Dict, List, Any
from wandb import api


log = logging.getLogger(__name__)


###############################################################################
# Errors
###############################################################################

class KaggleValidationError(RuntimeError):
    """Raised when Kaggle validation fails."""


###############################################################################
# Helpers
###############################################################################

def kaggle_login(username: str, api_key: str) -> Any:
    """
    Authenticate with Kaggle and return an API client.

    Note:
        Kaggle's API requires credentials via environment variables.
    """
    os.environ["KAGGLE_USERNAME"] = username
    os.environ["KAGGLE_API_KEY"] = api_key

    import kaggle
    api = kaggle.api  # Already authenticated on import
    return api


def _submissions_for_user(
    api: Any,
    competition: str,
    username: str,
) -> List:
    """
    Fetch submissions for a given user in a competition.
    """
    try:
        submissions = api.competition_submissions(competition)
    except Exception as exc:
        raise KaggleValidationError(
            f"Unable to access competition '{competition}'.\n"
            f"👉 Have you joined the competition?"
        ) from exc

    return [
        s for s in submissions
        if getattr(s, "_submitted_by", None) == username
    ]


###############################################################################
# Public API
###############################################################################

def export_kaggle_metadata(
    *,
    username: str,
    api_key: str,
    acknowledged: bool,
    main_competition_name: str,
    slack_competition_name: str,
) -> Dict[str, object]:
    """
    Validate Kaggle user registration and export minimal metadata.

    Validation guarantees:
      • Username exists
      • User is registered for at least one competition
      • User has submitted at least once

    Returns:
        A serializable dictionary for inclusion in submission ZIP.
    """

    if not acknowledged:
        raise KaggleValidationError(
            "Acknowledgement not accepted.\n"
            "👉 You must accept the acknowledgement before submitting."
        )

    log.info("Validating Kaggle user '%s'...", username)

    api = kaggle_login(username, api_key)

    competitions = {
        "main": main_competition_name,
        "slack": slack_competition_name,
    }

    results: Dict[str, int] = {}
    total_submissions = 0

    for label, competition in competitions.items():
        try:
            subs = _submissions_for_user(api, competition, username)
            results[label] = len(subs)
            total_submissions += len(subs)

            log.info(
                "✓ %s competition '%s': %d submission(s)",
                label.capitalize(),
                competition,
                len(subs),
            )
        except Exception:
            results[label] = 0
            pass

    if total_submissions == 0:
        raise KaggleValidationError(
            f"No Kaggle submissions found for user '{username}'.\n\n"
            "Common causes:\n"
            "• You have not joined the competition\n"
            "• You submitted under a different Kaggle account\n"
            "• Your username is misspelled (case-sensitive)\n"
            "• You have not submitted yet"
        )

    return {
        "kaggle_username": username,
        "competitions": {
            main_competition_name: results["main"],
            slack_competition_name: results["slack"],
        },
        "total_submissions": total_submissions,
    }
