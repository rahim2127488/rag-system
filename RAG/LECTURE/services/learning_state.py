import copy
import json


class LearningState:
    """
    Stores what the student is currently learning.

    This class is the ONLY owner of the Learning State.

    Other modules must never modify self.state directly.
    They should use get_state() and update_state().
    """

    def __init__(self):

        self.state = {

            "current_topics": [],

            "archived_topics": [],

            "examples_seen": {},

            "comparisons": [],

            "important_facts": [],

            "student_difficulties": [],

            "last_question": "",

            "last_answer_summary": ""

        }

    # --------------------------------------------------
    # Get Current State
    # --------------------------------------------------

    def get_state(self):
        """
        Return a safe copy of the Learning State.
        """

        return copy.deepcopy(self.state)

    # --------------------------------------------------
    # Apply Updates
    # --------------------------------------------------

    def update_state(self, updates):
        """
        Merge updates into the Learning State.

        Parameters
        ----------
        updates : dict
            JSON returned by the Memory Updater.
        """

        if not isinstance(updates, dict):
            return

        for key, value in updates.items():

            if key not in self.state:
                continue

            # Merge lists
            if isinstance(self.state[key], list):

                if isinstance(value, list):

                    for item in value:

                        if item not in self.state[key]:
                            self.state[key].append(item)

            # Merge dictionaries
            elif isinstance(self.state[key], dict):

                if isinstance(value, dict):

                    self.state[key].update(value)

            # Replace scalar values
            else:

                self.state[key] = value

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    def reset(self):
        """
        Reset the Learning State.
        """

        self.__init__()

    # --------------------------------------------------
    # Print
    # --------------------------------------------------

    def print_state(self):
        """
        Pretty-print the Learning State.
        """

        print("\n" + "=" * 60)
        print("Learning State")
        print("=" * 60)

        print(json.dumps(self.state, indent=4))

        print("=" * 60)