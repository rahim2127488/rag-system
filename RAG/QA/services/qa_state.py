class QAState:
    """
    Runtime state for a Question & Answer session.

    Responsibilities:
    - Store the current course and lesson.
    - Optionally store the concept the student is focusing on.
    - Keep the QA conversation history.
    - Track the number of questions asked.

    It does NOT:
    - Retrieve course material.
    - Generate answers.
    - Store embeddings.
    - Control lecture progression.
    - Store long-term learning progress.
    """

    def __init__(self):
        self.course = None
        self.lesson = None
        self.selected_concept = None
        self.conversation_history = []
        self.question_count = 0

    def start_session(
        self,
        course,
        lesson,
        selected_concept=None
    ):
        """
        Start a new QA session and clear previous conversation state.
        """
        self.course = course
        self.lesson = lesson
        self.selected_concept = selected_concept
        self.conversation_history = []
        self.question_count = 0

    def set_concept(self, concept):
        """
        Set or change the optional concept context for the session.
        """
        self.selected_concept = concept

    def add_message(self, role, content):
        """
        Add one message to the QA conversation history.
        """
        if not content:
            return

        self.conversation_history.append(
            {
                "role": role,
                "content": content,
            }
        )

    def add_question(self, question):
        """
        Record a student question.
        """
        self.add_message("student", question)
        self.question_count += 1

    def add_answer(self, answer):
        """
        Record the professor's answer.
        """
        self.add_message("professor", answer)

    def get_history(self):
        """
        Return the full QA conversation history.
        """
        return list(self.conversation_history)

    def clear(self):
        """
        Clear the current QA conversation while keeping the
        selected course and lesson.
        """
        self.conversation_history = []
        self.question_count = 0

    def get_state(self):
        """
        Return a serializable snapshot of the current QA state.
        """
        return {
            "course": self.course,
            "lesson": self.lesson,
            "selected_concept": self.selected_concept,
            "conversation_history": self.get_history(),
            "question_count": self.question_count,
        }
