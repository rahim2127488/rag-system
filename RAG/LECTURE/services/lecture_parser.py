from app.assistant.models.concept_state import ConceptState


class LessonParser:
    """
    ==========================================================
                        Lesson Parser
    ==========================================================

    Converts retrieved lesson chunks into an ordered
    list of ConceptState objects.

    Responsibilities:
    - Group chunks belonging to the same concept
    - Preserve concept order
    - Preserve chunk order inside each concept
    - Build ConceptState objects
    - Navigate between concepts

    It does NOT:
    - Retrieve documents
    - Call the LLM
    - Teach
    - Track global learning progress
    """

    def __init__(self):

        self.concepts = []

        self.current_index = 0

    # ==========================================================
    # Public API
    # ==========================================================

    def parse(self, retrieved_chunks):
        """
        Convert retrieved chunks into ordered ConceptState objects.

        Multiple chunks belonging to the same concept are merged
        into one ConceptState.
        """

        self.concepts = []

        self.current_index = 0

        grouped = {}

        # ------------------------------------------------------
        # Group chunks by concept
        # ------------------------------------------------------

        for chunk in retrieved_chunks:

            concept_index = chunk.get(
                "concept_index"
            )

            concept_name = chunk.get(
                "concept"
            )

            # Skip records that do not represent a concept
            if concept_name is None:
                continue

            key = (
                concept_index
                if concept_index is not None
                else concept_name
            )

            if key not in grouped:

                grouped[key] = {
                    "concept_index": concept_index,
                    "concept": concept_name,
                    "chunks": []
                }

            grouped[key]["chunks"].append(chunk)

        # ------------------------------------------------------
        # Sort concepts
        # ------------------------------------------------------

        ordered_groups = sorted(
            grouped.values(),
            key=lambda group: (
                group["concept_index"]
                if group["concept_index"] is not None
                else 999999
            )
        )

        # ------------------------------------------------------
        # Build ConceptState objects
        # ------------------------------------------------------

        for concept_id, group in enumerate(
            ordered_groups,
            start=1
        ):

            chunks = group["chunks"]

            # Sort chunks inside the concept
            chunks.sort(
                key=lambda chunk: (
                    chunk["chunk_index"]
                    if chunk["chunk_index"] is not None
                    else 999999
                )
            )

            # Merge all chunk text belonging to this concept
            content = "\n\n".join(
                chunk["text"]
                for chunk in chunks
                if chunk.get("text")
            )

            first_chunk = chunks[0]

            concept = ConceptState(
                concept_id=concept_id,

                title=group["concept"],

                content=content,

                source_document=first_chunk.get(
                    "document",
                    ""
                ),

                page_number=first_chunk.get(
                    "page",
                    0
                )
            )

            self.concepts.append(
                concept
            )

        return self.concepts

    # ==========================================================
    # Current Concept
    # ==========================================================

    def current_concept(self):

        if not self.concepts:

            return None

        return self.concepts[
            self.current_index
        ]

    # ==========================================================
    # Navigation
    # ==========================================================

    def next_concept(self):

        if self.has_next():

            self.current_index += 1

        return self.current_concept()

    # ----------------------------------------------------------

    def previous_concept(self):

        if self.has_previous():

            self.current_index -= 1

        return self.current_concept()

    # ==========================================================
    # Direct Access
    # ==========================================================

    def get_concept(self, index):

        if index < 0:

            return None

        if index >= len(self.concepts):

            return None

        return self.concepts[index]

    # ==========================================================
    # Navigation Helpers
    # ==========================================================

    def has_next(self):

        return (
            self.current_index
            < len(self.concepts) - 1
        )

    # ----------------------------------------------------------

    def has_previous(self):

        return self.current_index > 0

    # ==========================================================
    # Reset
    # ==========================================================

    def reset(self):

        self.current_index = 0

    # ==========================================================
    # Information
    # ==========================================================

    def total_concepts(self):

        return len(self.concepts)

    # ----------------------------------------------------------

    def current_position(self):

        return self.current_index + 1

    # ----------------------------------------------------------

    def is_finished(self):

        return (
            self.current_index
            >= len(self.concepts) - 1
        )

    # ----------------------------------------------------------

    def get_concepts(self):

        return self.concepts

    # ==========================================================
    # Debug / Inspection
    # ==========================================================

    def print_lesson(self):

        print()

        print("=" * 60)

        print("LESSON STRUCTURE")

        print("=" * 60)

        for concept in self.concepts:

            print(
                f"\nConcept {concept.concept_id}"
            )

            print(
                f"Title : {concept.title}"
            )

            print(
                f"Page  : {concept.page_number}"
            )

            print(
                f"Source: {concept.source_document}"
            )

            preview = concept.content[:120]

            preview = preview.replace(
                "\n",
                " "
            )

            print(
                f"Text  : {preview}..."
            )

        print("=" * 60)