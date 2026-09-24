from dataclasses import dataclass, field

from app.assistant.models.concept_history import ConceptHistory


@dataclass
class ConceptState:
    """
    ==========================================================
                    Concept State
    ==========================================================

    Represents one concept inside a lesson.

    It contains:

    - The concept information
    - Source metadata
    - Teaching history
    - Student progress on this concept

    The AI Professor teaches ONE ConceptState at a time.
    """

    # ======================================================
    # Concept Information
    # ======================================================

    concept_id: int

    title: str

    content: str
    # ======================================================
    # Source Information
    # ======================================================

    source_document: str = ""

    page_number: int = 0

    # ======================================================
    # Source Information
    # ======================================================

    source_document: str = ""

    page_number: int = 0

    # ======================================================
    # Teaching Progress
    # ======================================================

    visited: bool = False

    completed: bool = False

    history: ConceptHistory = field(default_factory=ConceptHistory)

    # ======================================================
    # Progress
    # ======================================================

    def mark_visited(self):
        self.visited = True

    def mark_completed(self):
        self.completed = True

    # ======================================================
    # History
    # ======================================================

    def reset_history(self):
        self.history.reset()

    def record_example(self, example: str = ""):
        self.history.record_example(example)

    def record_re_explanation(self, strategy: str = ""):
        self.history.record_re_explanation(strategy)

    def record_simplification(self):
        self.history.record_simplification()

    def increase_detail(self):
        self.history.increase_detail()

    # ======================================================
    # Helpers
    # ======================================================

    def has_examples(self):
        return self.history.has_examples()

    def has_been_simplified(self):
        return self.history.has_been_simplified()

    def progress_summary(self):
        return {
            "visited": self.visited,
            "completed": self.completed,
            "history": self.history.to_dict(),
        }

    # ======================================================
    # Export
    # ======================================================

    def to_dict(self):
        return {
            "concept_id": self.concept_id,
            "title": self.title,
            "content": self.content,
            "source_document": self.source_document,
            "page_number": self.page_number,
            "visited": self.visited,
            "completed": self.completed,
            "history": self.history.to_dict(),
        }

    # ======================================================

    def __str__(self):

        return f"""
============================================================
Concept State
============================================================

Concept ID:
{self.concept_id}

Title:
{self.title}

Source:
{self.source_document}

Page:
{self.page_number}

Visited:
{self.visited}

Completed:
{self.completed}

History:

{self.history}

============================================================
"""