from RAG.LECTURE.prompts.answer_review_prompt import AnswerReviewPrompt
from RAG.LECTURE.prompts.teaching_context_builder import TeachingContextBuilder


class AnswerReviewer:
    """
    AI Professor - Lecture Mode

    Responsibility:
    - Build runtime teaching context.
    - Build the final teaching prompt.
    - Send the prompt to the LLM.
    - Return only the professor response.

    It does NOT:
    - Control lesson navigation.
    - Decide when to continue.
    - Modify teaching state.
    - Retrieve course material.
    """

    def __init__(self, client, model):
        self.client = client
        self.model = model

    # ==========================================================
    # Lesson Introduction
    # ==========================================================

    def introduce_lesson(self, course, lesson):

        prompt = f"""
You are an excellent university professor.

Course:
{course}

Lesson:
{lesson}

Welcome the student.

Briefly explain today's lesson.

Tell the student:

- You will teach ONE concept at a time.
- They may interrupt whenever they want.
- The lesson only advances when they press CONTINUE.

Do NOT begin teaching.

Finish by asking the student to press START.

Return only your response.
"""

        return self._generate(prompt)

    # ==========================================================
    # Teaching
    # ==========================================================

    def teach(
        self,
        student_action,
        current_concept,
        teaching_state
    ):

        context = TeachingContextBuilder.build(
            concept=current_concept,
            teaching_state=teaching_state,
            student_action=student_action
        )

        prompt = AnswerReviewPrompt.build(
            concept=current_concept,
            context=context
        )

        # ------------------------------------------------------
        # Lecture grounding policy
        # ------------------------------------------------------

        grounding_rules = f"""
==================================================
LECTURE GROUNDING POLICY
==================================================

You are teaching an official university lecture.

The CURRENT CONCEPT below is the authoritative source
for what you teach.

CURRENT CONCEPT:
{current_concept.title}

OFFICIAL COURSE CONTENT:
{current_concept.content}

STRICT RULES:

1. Teach ONLY the current concept.

2. The official course content above determines WHAT
   information is allowed to be taught.

3. Do NOT introduce new concepts that are not present
   in the official course content.

4. Do NOT introduce additional APIs, classes, methods,
   interfaces, algorithms, data structures, performance
   claims, terminology, hierarchy information, or other
   technical facts unless they are supported by the
   official course content.

5. You may rewrite, reorganize, simplify, or clarify
   information from the official course content.

6. You may use a simple analogy only when it explains
   information already present in the official course
   content.

7. For EXAMPLE or MORE_EXAMPLES:
   create an example that demonstrates ONLY information
   already present in the official course content.
   Do not use the example as an excuse to introduce
   unrelated Java knowledge.

8. For MORE_DETAIL:
   add DEPTH to the CURRENT CONCEPT using details that
   are already present in the official course content.
   Do not expand into later concepts or general textbook
   knowledge.

9. If the official course content does not contain enough
   information to satisfy the requested action, say so
   briefly rather than inventing or importing new material.

10. NEVER teach the next concept.

11. NEVER restart the lesson.

12. NEVER decide lesson progression.

13. Return ONLY the professor's teaching response.

==================================================
END LECTURE GROUNDING POLICY
==================================================
"""

        final_prompt = f"""
{prompt}

{grounding_rules}
"""

        return self._generate(final_prompt)

    # ==========================================================
    # Lesson End
    # ==========================================================

    def end_lesson(
        self,
        course,
        lesson
    ):

        prompt = f"""
Today's lecture has finished.

Course:
{course}

Lesson:
{lesson}

Congratulate the student.

Briefly summarize the lesson that was completed.

Invite the student into Discussion Mode.

Return only your response.
"""

        return self._generate(prompt)

    # ==========================================================
    # LLM
    # ==========================================================

    def _generate(self, prompt):

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": prompt
                }
            ]
        )

        return completion.choices[0].message.content.strip()