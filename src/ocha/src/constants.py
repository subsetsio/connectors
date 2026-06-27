"""OCHA HDX HAPI v2 — the entity union and its endpoint paths.

Each entity id (a collect/rank entity) maps to a HAPI v2 thematic data endpoint
path. The spec id is f"ocha-{entity_id}" (entity ids are already lowercase,
hyphenated, underscore-free). Data, not logic — kept out of the node module.
"""

# entity_id -> HAPI v2 path (relative to the API base)
ENTITY_PATHS = {
    "affected-people-humanitarian-needs": "affected-people/humanitarian-needs",
    "affected-people-idps": "affected-people/idps",
    "affected-people-refugees-persons-of-concern": "affected-people/refugees-persons-of-concern",
    "affected-people-returnees": "affected-people/returnees",
    "climate-rainfall": "climate/rainfall",
    "coordination-context-conflict-events": "coordination-context/conflict-events",
    "coordination-context-funding": "coordination-context/funding",
    "coordination-context-national-risk": "coordination-context/national-risk",
    "coordination-context-operational-presence": "coordination-context/operational-presence",
    "food-security-nutrition-poverty-food-prices-market-monitor": "food-security-nutrition-poverty/food-prices-market-monitor",
    "food-security-nutrition-poverty-food-security": "food-security-nutrition-poverty/food-security",
    "food-security-nutrition-poverty-poverty-rate": "food-security-nutrition-poverty/poverty-rate",
    "geography-infrastructure-baseline-population": "geography-infrastructure/baseline-population",
}

ENTITY_IDS = list(ENTITY_PATHS)
