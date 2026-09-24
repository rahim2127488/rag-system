from enum import Enum


class StudentAction(Enum):
    """
    ==========================================================
                    Student Actions
    ==========================================================

    Every interaction during Lecture Mode is represented
    by one of these actions.

    The frontend sends an action.

    The Lecture Engine decides what to do.
    """

    # ------------------------------------------------------
    # Lecture Control
    # ------------------------------------------------------

    START = "START"

    CONTINUE = "CONTINUE"

    PAUSE = "PAUSE"

    RESUME = "RESUME"

    FINISH = "FINISH"

    # ------------------------------------------------------
    # Learning Actions
    # ------------------------------------------------------

    EXPLAIN_AGAIN = "EXPLAIN_AGAIN"

    MORE_DETAIL = "MORE_DETAIL"

    SIMPLIFY = "SIMPLIFY"

    EXAMPLE = "EXAMPLE"

    MORE_EXAMPLES = "MORE_EXAMPLES"

    # ------------------------------------------------------
    # Navigation
    # ------------------------------------------------------

    PREVIOUS = "PREVIOUS"

    NEXT = "NEXT"

    JUMP = "JUMP"

    # ------------------------------------------------------
    # Lecture Information
    # ------------------------------------------------------

    STATUS = "STATUS"

    PROGRESS = "PROGRESS"

    # ------------------------------------------------------
    # Discussion Mode
    # ------------------------------------------------------

    DISCUSSION = "DISCUSSION"

    ASK_QUESTION = "ASK_QUESTION"

    QUIZ = "QUIZ"

    REVIEW = "REVIEW"

    # ------------------------------------------------------
    # System
    # ------------------------------------------------------

    EXIT = "EXIT"