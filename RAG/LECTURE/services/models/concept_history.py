from dataclasses import dataclass, field
from typing import List


@dataclass
class ConceptHistory:
    """
    ==========================================================
                    Concept History
    ==========================================================

    Stores HOW the current concept has been taught.

    This is NOT conversation memory.

    This is pedagogical memory.

    It allows the AI Professor to remember:

    - How many examples were given
    - Whether the concept was simplified
    - Whether it was explained again
    - How much detail has already been added

    The history is reset whenever the student
    moves to a new concept.
    """

    # ======================================================
    # Teaching Counters
    # ======================================================

    examples_given: int = 0

    re_explanations: int = 0

    simplifications: int = 0

    detail_level: int = 0

    # ======================================================
    # Teaching Memory
    # ======================================================

    used_examples: List[str] = field(default_factory=list)

    used_strategies: List[str] = field(default_factory=list)

    # ======================================================
    # Recording Methods
    # ======================================================

    def record_example(self, example: str = ""):
        """
        Records that an example was given.
        """

        self.examples_given += 1

        if example:
            self.used_examples.append(example)

    # ------------------------------------------------------

    def record_re_explanation(self, strategy: str = ""):
        """
        Records another explanation.
        """

        self.re_explanations += 1

        if strategy:
            self.used_strategies.append(strategy)

    # ------------------------------------------------------

    def record_simplification(self):
        """
        Records a simplification.
        """

        self.simplifications += 1

    # ------------------------------------------------------

    def increase_detail(self):
        """
        Increases the explanation depth.
        """

        self.detail_level += 1

    # ======================================================
    # Helpers
    # ======================================================

    def has_examples(self) -> bool:
        return self.examples_given > 0

    # ------------------------------------------------------

    def has_been_simplified(self) -> bool:
        return self.simplifications > 0

    # ------------------------------------------------------

    def has_multiple_examples(self) -> bool:
        return self.examples_given > 1

    # ------------------------------------------------------

    def reset(self):
        """
        Clears the teaching history for a new concept.
        """

        self.examples_given = 0

        self.re_explanations = 0

        self.simplifications = 0

        self.detail_level = 0

        self.used_examples.clear()

        self.used_strategies.clear()

    # ======================================================

    def to_dict(self):

        return {

            "examples_given": self.examples_given,

            "re_explanations": self.re_explanations,

            "simplifications": self.simplifications,

            "detail_level": self.detail_level,

            "used_examples": self.used_examples,

            "used_strategies": self.used_strategies

        }

    # ======================================================

    def __str__(self):

        return f"""
============================================================
Concept History
============================================================

Examples Given:
{self.examples_given}

Re-explanations:
{self.re_explanations}

Simplifications:
{self.simplifications}

Detail Level:
{self.detail_level}

Used Examples:
{self.used_examples}

Teaching Strategies:
{self.used_strategies}

============================================================
"""