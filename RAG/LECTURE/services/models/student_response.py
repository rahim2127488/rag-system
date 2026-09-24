from dataclasses import dataclass, field
from typing import List


# ==========================================================
# Lecture Progress
# ==========================================================

@dataclass
class LectureProgress:

    current_concept: int

    total_concepts: int

    percentage: float


# ==========================================================
# Lecture Response
# ==========================================================

@dataclass
class LectureResponse:
    """
    Complete response returned by LectureEngine.

    This object contains EVERYTHING the frontend needs.
    """

    # ------------------------------------------------------
    # Professor
    # ------------------------------------------------------

    message: str

    # ------------------------------------------------------
    # Course
    # ------------------------------------------------------

    course: str

    lesson: str

    # ------------------------------------------------------
    # Current Concept
    # ------------------------------------------------------

    current_concept: str

    source_document: str

    page_number: int

    # ------------------------------------------------------
    # Mode
    # ------------------------------------------------------

    mode: str

    # ------------------------------------------------------
    # Progress
    # ------------------------------------------------------

    progress: LectureProgress

    # ------------------------------------------------------
    # UI
    # ------------------------------------------------------

    available_actions: List[str] = field(default_factory=list)

    waiting_for_student: bool = True

    lecture_finished: bool = False

    error: str | None = None

    # ======================================================

    def to_dict(self):

        return {

            "message": self.message,

            "course": self.course,

            "lesson": self.lesson,

            "current_concept": self.current_concept,

            "source_document": self.source_document,

            "page_number": self.page_number,

            "mode": self.mode,

            "progress": {

                "current_concept":
                    self.progress.current_concept,

                "total_concepts":
                    self.progress.total_concepts,

                "percentage":
                    self.progress.percentage

            },

            "available_actions":
                self.available_actions,

            "waiting_for_student":
                self.waiting_for_student,

            "lecture_finished":
                self.lecture_finished,

            "error":
                self.error

        }

    # ======================================================

    def __str__(self):

        return f"""
============================================================
Lecture Response
============================================================

Course:
{self.course}

Lesson:
{self.lesson}

Current Concept:
{self.current_concept}

Source:
{self.source_document}

Page:
{self.page_number}

Mode:
{self.mode}

Progress:
{self.progress.percentage:.1f}%

Professor:

{self.message}

Available Actions:
{", ".join(self.available_actions)}

============================================================
"""