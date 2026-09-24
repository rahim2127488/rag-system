"""
==========================================================
Lecture Engine
Version 3
==========================================================

Controller responsible for lecture flow.

It controls:

- lesson progression
- student actions
- concept navigation
- lecture responses

It NEVER teaches.

Teaching is delegated to AnswerReviewer.
"""
from RAG.LECTURE.services.models.student_action import StudentAction
from RAG.LECTURE.services.models.student_response import (
    LectureResponse,
    LectureProgress,
)


class LectureEngine:

    def __init__(
        self,
        professor,
        lecture_retriever,
        lesson_parser,
        teaching_state
    ):

        self.professor = professor
        self.lecture_retriever = lecture_retriever
        self.lesson_parser = lesson_parser
        self.state = teaching_state

    # ======================================================
    # Lesson
    # ======================================================

    def start_lesson(self, course, lesson):

        self.state.start_lesson(course, lesson)

        chunks = self.lecture_retriever.get_lesson_material(
            course,
            lesson
        )
        
       # print("\n========== RAW RETRIEVED CHUNK ==========")
        #print(chunks[0])
        #print("=========================================\n")
        concepts = self.lesson_parser.parse(chunks)

        self.state.load_concepts(concepts)

        return self._build_response(

            self.professor.introduce_lesson(
                course,
                lesson
            )

        )

    # ======================================================
    # Student Actions
    # ======================================================

    def handle_action(self, action):

        if isinstance(action, str):

            action = StudentAction[action]

        if action == StudentAction.START:

            self.state.start_lecture()

            return self._teach(action)

        if action == StudentAction.CONTINUE:

            return self._continue()

        if action == StudentAction.EXPLAIN_AGAIN:

            self.state.current_concept.record_re_explanation()

            return self._teach(action)

        if action == StudentAction.SIMPLIFY:

            self.state.current_concept.record_simplification()

            return self._teach(action)

        if action == StudentAction.MORE_DETAIL:

            self.state.current_concept.increase_detail()

            return self._teach(action)

        if action == StudentAction.EXAMPLE:

            self.state.current_concept.record_example()

            return self._teach(action)

        if action == StudentAction.MORE_EXAMPLES:

            self.state.current_concept.record_example()

            return self._teach(action)

        if action == StudentAction.STATUS:

            return self._build_response(

                "Lecture status updated."

            )

        if action == StudentAction.FINISH:

            return self._finish()

        return self._build_response(

            "Unsupported action.",

            error="Unsupported action"

        )

    # ======================================================
    # Teaching
    # ======================================================

    def _teach(self, action):

        concept = self.state.current_concept

        message = self.professor.teach(

            student_action=action,

            current_concept=concept,

            teaching_state=self.state

        )

        self.state.set_waiting(True)

        return self._build_response(message)

    # ======================================================
    # Continue
    # ======================================================

    def _continue(self):

        if not self.state.next_concept():

            return self._finish()

        return self._teach(

            StudentAction.CONTINUE

        )

    # ======================================================
    # Finish
    # ======================================================

    def _finish(self):

        self.state.finish_lecture()

        message = self.professor.end_lesson(

            self.state.course,

            self.state.lesson

        )

        return self._build_response(

            message,

            finished=True

        )

    # ======================================================
    # UI
    # ======================================================

    def _available_actions(self):

        history = self.state.current_concept.history

        actions = [

            "CONTINUE",

            "EXPLAIN_AGAIN",

            "SIMPLIFY"

        ]

        if history.examples_given == 0:

            actions.append(

                "EXAMPLE"

            )

        else:

            actions.append(

                "MORE_EXAMPLES"

            )

        actions.append(

            "MORE_DETAIL"

        )

        return actions

    # ======================================================
    # Response
    # ======================================================

    def _build_response(

        self,

        message,

        finished=False,

        error=None

    ):

        progress = LectureProgress(

            current_concept=self.state.current_concept_index + 1,

            total_concepts=self.state.total_concepts,

            percentage=self.state.progress_percentage

        )

        concept = self.state.current_concept

        return LectureResponse(

    message=message,

    course=self.state.course,

    lesson=self.state.lesson,

    current_concept=concept.title if concept else "",

    source_document=(
        concept.source_document if concept else ""
    ),

    page_number=(
        concept.page_number if concept else 0
    ),

    mode=self.state.mode,

    progress=progress,

    available_actions=(
        ["DISCUSSION", "QUIZ", "REVIEW"]
        if finished
        else self._available_actions()
    ),

    waiting_for_student=self.state.waiting_for_student,

    lecture_finished=finished,

    error=error

)