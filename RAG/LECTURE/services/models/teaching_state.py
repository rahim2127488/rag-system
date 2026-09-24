from dataclasses import dataclass, field
from typing import List, Optional

from RAG.LECTURE.services.models.concept_state import ConceptState


@dataclass
class TeachingState:
    """
    ==========================================================
                    Teaching State
    ==========================================================

    Global state of the current lecture session.

    This class remembers:

    - Current course
    - Current lesson
    - Current concept
    - Overall progress
    - Lecture status

    It DOES NOT teach.

    It ONLY stores state.
    """

    # ======================================================
    # Course
    # ======================================================

    course: str = ""

    lesson: str = ""

    # ======================================================
    # Concepts
    # ======================================================

    concepts: List[ConceptState] = field(default_factory=list)

    current_concept_index: int = 0

    # ======================================================
    # Lecture State
    # ======================================================

    lecture_started: bool = False

    lecture_finished: bool = False

    waiting_for_student: bool = True

    mode: str = "LECTURE"

    # ======================================================
    # Current Concept
    # ======================================================

    @property
    def current_concept(self) -> Optional[ConceptState]:

        if not self.concepts:
            return None

        return self.concepts[self.current_concept_index]

    # ======================================================
    # Lesson Management
    # ======================================================

    def start_lesson(self, course: str, lesson: str):

        self.course = course
        self.lesson = lesson

        self.lecture_started = False
        self.lecture_finished = False

        self.current_concept_index = 0

        self.waiting_for_student = True

    # ------------------------------------------------------

    def load_concepts(self, concepts: List[ConceptState]):

        self.concepts = concepts

    # ======================================================
    # Lecture Control
    # ======================================================

    def start_lecture(self):

        self.lecture_started = True

        if self.current_concept:
            self.current_concept.mark_visited()

    # ------------------------------------------------------

    def finish_lecture(self):

        self.lecture_finished = True

    # ======================================================
    # Navigation
    # ======================================================

    def next_concept(self):

        if self.current_concept:

            self.current_concept.mark_completed()

        if self.current_concept_index < len(self.concepts) - 1:

            self.current_concept_index += 1

            self.current_concept.mark_visited()

            return True

        self.finish_lecture()

        return False

    # ------------------------------------------------------

    def previous_concept(self):

        if self.current_concept_index > 0:

            self.current_concept_index -= 1

            return True

        return False

    # ======================================================
    # Progress
    # ======================================================

    @property
    def total_concepts(self):

        return len(self.concepts)

    # ------------------------------------------------------

    @property
    def completed_concepts(self):

        return sum(
            concept.completed
            for concept in self.concepts
        )

    # ------------------------------------------------------

    @property
    def progress_percentage(self):

        if not self.concepts:

            return 0

        return round(
            (self.completed_concepts / len(self.concepts)) * 100,
            1
        )

    # ======================================================
    # Student Waiting
    # ======================================================

    def set_waiting(self, value: bool):

        self.waiting_for_student = value

    # ======================================================
    # Export
    # ======================================================

    def to_dict(self):

        return {

            "course": self.course,

            "lesson": self.lesson,

            "lecture_started": self.lecture_started,

            "lecture_finished": self.lecture_finished,

            "mode": self.mode,

            "current_concept_index": self.current_concept_index,

            "progress_percentage": self.progress_percentage,

            "waiting_for_student": self.waiting_for_student,

            "current_concept":
                self.current_concept.to_dict()
                if self.current_concept
                else None

        }

    # ======================================================

    def __str__(self):

        return f"""
============================================================
Teaching State
============================================================

Course:
{self.course}

Lesson:
{self.lesson}

Current Concept:
{self.current_concept.title if self.current_concept else "None"}

Concept:
{self.current_concept_index + 1}/{self.total_concepts}

Progress:
{self.progress_percentage}%

Lecture Started:
{self.lecture_started}

Lecture Finished:
{self.lecture_finished}

Waiting:
{self.waiting_for_student}

============================================================
"""