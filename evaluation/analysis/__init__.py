"""Evaluation analysis and follow-up experiment proposals."""

from .study_analysis import generate_study_summary, get_confounding_factors
from .followup_experiment import get_experimental_protocol

__all__ = ["generate_study_summary", "get_confounding_factors", "get_experimental_protocol"]
