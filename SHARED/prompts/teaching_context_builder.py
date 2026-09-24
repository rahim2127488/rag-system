"""
==============================================================
NPU AI Professor
Teaching Context Builder
==============================================================

Builds a rich runtime teaching context for the AI Professor.

This class converts the current learning state into natural
language that is easy for an LLM to understand.

It does NOT communicate with the LLM.
It does NOT build prompts.
It only prepares teaching context.
"""


class TeachingContextBuilder:

    @staticmethod
    def build(concept, teaching_state, student_action) -> str:

        history = concept.history

        return f"""
==================================================
LESSON STATE
==================================================

Course:
{teaching_state.course}

Lesson:
{teaching_state.lesson}

Current Concept

Title:
{concept.title}

Concept Position:
{teaching_state.current_concept_index + 1} / {teaching_state.total_concepts}

Lesson Progress:
{teaching_state.progress_percentage}%
==================================================
CURRENT STUDENT REQUEST
==================================================

{TeachingContextBuilder._action_description(student_action)}

==================================================
LEARNING HISTORY
==================================================

This concept has already been taught.

Examples Given:
{history.examples_given}

Re-Explanations:
{history.re_explanations}

Simplifications:
{history.simplifications}

Current Detail Level:
{TeachingContextBuilder._detail_name(history.detail_level)}

==================================================
PROFESSOR OBJECTIVE
==================================================

{TeachingContextBuilder._objective(student_action)}

==================================================
GUIDANCE
==================================================

{TeachingContextBuilder._guidance(history)}

==================================================
IMPORTANT
==================================================

Remain on the current concept.

Do not introduce a new concept.

Do not restart the lesson.

Stop after completing the requested action.
"""

    # ======================================================
    # Detail Level
    # ======================================================

    @staticmethod
    def _detail_name(level: int) -> str:

        if level <= 0:
            return "Beginner"

        if level == 1:
            return "Basic"

        if level == 2:
            return "Intermediate"

        if level == 3:
            return "Advanced"

        return "Expert"

    # ======================================================
    # Student Action
    # ======================================================

    @staticmethod
    def _action_description(action) -> str:

        return action.name.replace("_", " ").title()

    # ======================================================
    # Professor Objective
    # ======================================================

    @staticmethod
    def _objective(action) -> str:

        objectives = {

            "START":
                "Introduce the current concept and build intuition.",

            "CONTINUE":
                "Teach the next concept supplied by the system.",

            "EXPLAIN_AGAIN":
                "Explain the same concept using a different approach.",

            "SIMPLIFY":
                "Explain the same concept using simpler language and analogies.",

            "MORE_DETAIL":
                "Increase the technical depth without restarting.",

            "EXAMPLE":
                "Provide one worked example immediately.",

            "MORE_EXAMPLES":
                "Provide a completely different worked example.",

            "STATUS":
                "Summarize the student's current learning progress.",

            "FINISH":
                "Politely conclude the lesson."
        }

        return objectives.get(
            action.name,
            "Respond appropriately."
        )

    # ======================================================
    # Guidance
    # ======================================================

    @staticmethod
    def _guidance(history) -> str:

        guidance = []

        if history.examples_given == 0:
            guidance.append(
                "- No examples have been given yet."
            )

        elif history.examples_given == 1:
            guidance.append(
                "- One example has already been shown. Use a different scenario."
            )

        else:
            guidance.append(
                "- Several examples have already been used. Avoid repetition."
            )

        if history.re_explanations > 0:
            guidance.append(
                "- Use a different mental model than previous explanations."
            )

        if history.simplifications > 0:
            guidance.append(
                "- The student benefits from simpler explanations."
            )

        if history.detail_level >= 2:
            guidance.append(
                "- Assume the student understands the fundamentals."
            )

        guidance.append(
            "- Keep the response focused on one concept."
        )

        guidance.append(
            "- Do not ask whether the student wants to continue."
        )

        return "\n".join(guidance)