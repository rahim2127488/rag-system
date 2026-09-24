import json

from app.assistant.llm.llm_client import llm_client
from app.assistant.prompts.router_prompt import RouterPrompt
from app.assistant.router.route import Route
from app.assistant.router.route_decision import RouteDecision
from app.config import (
    ROUTER_MODEL,
    ROUTER_TEMPERATURE,
)


class RequestRouter:
    """
    ==========================================================
    Request Router
    ==========================================================

    Version:
        1.1

    Purpose:
        Decide which pipeline should handle the student's request.

    Routes:
        CONVERSATION
        ACADEMIC
    """

    def __init__(self):

        self.client = llm_client.client
        self.model = ROUTER_MODEL

    # --------------------------------------------------
    # Public Method
    # --------------------------------------------------

    def route(self, question: str) -> RouteDecision:

        prompt = RouterPrompt.build(question)

        response = self._call_llm(prompt)

        decision = self._parse_response(response)

        self._print_debug(question, decision)

        return decision

    # --------------------------------------------------
    # Private Methods
    # --------------------------------------------------

    def _call_llm(self, prompt: str) -> str:

        completion = self.client.chat.completions.create(

            model=self.model,

            temperature=ROUTER_TEMPERATURE,

            response_format={"type": "json_object"},

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return completion.choices[0].message.content

    def _parse_response(self, response: str) -> RouteDecision:

        try:

            data = json.loads(response)

            route = Route[data["route"]]

            confidence = float(data["confidence"])

            summary = data["decision_summary"]

            reply = data.get("response")

            return RouteDecision(

                route=route,

                confidence=confidence,

                reason=summary,

                response=reply

            )

        except Exception as error:

            print("\nRouter JSON Error:")
            print(error)

            print("\nRaw Response:")
            print(response)

            return self._fallback()

    def _fallback(self) -> RouteDecision:

        return RouteDecision(

            route=Route.ACADEMIC,

            confidence=0.60,

            reason="Router failed to produce valid JSON.",

            response=None

        )

    def _print_debug(
        self,
        question: str,
        decision: RouteDecision
    ):

        print("\n" + "=" * 60)
        print("REQUEST ROUTER")
        print("=" * 60)

        print("\nQuestion:")
        print(question)

        print("\nRoute:")
        print(decision.route.value)

        print("\nConfidence:")
        print(decision.confidence)

        print("\nDecision Summary:")
        print(decision.reason)

        if decision.response:

            print("\nConversation Response:")
            print(decision.response)

        print("=" * 60)