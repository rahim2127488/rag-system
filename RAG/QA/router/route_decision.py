from dataclasses import dataclass

from .route import Route


@dataclass
class RouteDecision:

    route: Route

    confidence: float

    reason: str

    response: str | None = None