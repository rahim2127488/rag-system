import json

from app.assistant.llm.llm_client import llm_client
from app.assistant.prompts.memory_prompt import MemoryPrompt


class MemoryUpdater:
    """
    Uses the LLM to update the student's Learning State.

    This class does NOT modify the LearningState directly.

    It only asks the LLM to produce a JSON update and
    returns the parsed dictionary.
    """

    def __init__(self, model_name: str):

        self.client = llm_client.client
        self.model_name = model_name

    def update(self, learning_state, question, answer):
        """
        Ask the LLM to generate a Learning State update.

        Parameters:
            learning_state (dict): Current learning state.
            question (str): Latest student question.
            answer (str): Latest AI answer.

        Returns:
            dict
        """

        system_prompt = MemoryPrompt.build_prompt()

        user_prompt = f"""
Current Learning State:

{json.dumps(learning_state, indent=4)}

------------------------------------------------------------

Student Question:

{question}

------------------------------------------------------------

AI Answer:

{answer}

------------------------------------------------------------

Update the Learning State.

Return ONLY valid JSON.
"""

        response = self.client.chat.completions.create(

            model=self.model_name,

            messages=[

                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": user_prompt
                }

            ],

            temperature=0

        )

        result = response.choices[0].message.content.strip()

        try:

            return json.loads(result)

        except json.JSONDecodeError:

            print("\nMemory Updater Error")
            print("----------------------")
            print("The LLM returned invalid JSON.\n")

            print(result)

            return {}