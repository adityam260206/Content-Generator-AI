"""Base strategy class for educational quiz generation."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseQuizStrategy(ABC):
    """Abstract base class for quiz generation strategies."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generate_quiz(self, context_text: str, num_questions: int = 5) -> List[Dict[str, Any]]:
        """Generate quiz questions given input context."""
        pass
