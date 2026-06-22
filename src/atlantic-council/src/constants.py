"""Reference data for the Atlantic Council Freedom and Prosperity Indexes.

The indicator codebook is fixed domain knowledge (the index hierarchy is not
exposed by any source endpoint), so it lives here as data rather than logic.
`indicator_code` values match the flat keys in chartProfiles/<id>.json records;
each also has a `<code>Rank` sibling key carrying the cross-country rank.
"""

INDICATORS = [
    # Top-level indexes
    {"indicator_code": "freedomIndex", "label": "Freedom Index", "index": "freedom", "subindex": None, "level": "index"},
    {"indicator_code": "prosperityIndex", "label": "Prosperity Index", "index": "prosperity", "subindex": None, "level": "index"},
    # Freedom subindexes
    {"indicator_code": "economicSubindex", "label": "Economic Subindex", "index": "freedom", "subindex": "economic", "level": "subindex"},
    {"indicator_code": "politicalSubindex", "label": "Political Subindex", "index": "freedom", "subindex": "political", "level": "subindex"},
    {"indicator_code": "legalSubindex", "label": "Legal Subindex", "index": "freedom", "subindex": "legal", "level": "subindex"},
    # Economic indicators
    {"indicator_code": "womensEconomicFreedom", "label": "Women's Economic Freedom", "index": "freedom", "subindex": "economic", "level": "indicator"},
    {"indicator_code": "investmentFreedom", "label": "Investment Freedom", "index": "freedom", "subindex": "economic", "level": "indicator"},
    {"indicator_code": "propertyRights", "label": "Property Rights", "index": "freedom", "subindex": "economic", "level": "indicator"},
    {"indicator_code": "tradeFreedom", "label": "Trade Freedom", "index": "freedom", "subindex": "economic", "level": "indicator"},
    # Political indicators
    {"indicator_code": "elections", "label": "Elections", "index": "freedom", "subindex": "political", "level": "indicator"},
    {"indicator_code": "civilLiberties", "label": "Civil Liberties", "index": "freedom", "subindex": "political", "level": "indicator"},
    {"indicator_code": "politicalRights", "label": "Political Rights", "index": "freedom", "subindex": "political", "level": "indicator"},
    {"indicator_code": "legislativeConstraintsOnTheExecutive", "label": "Legislative Constraints on the Executive", "index": "freedom", "subindex": "political", "level": "indicator"},
    # Legal indicators
    {"indicator_code": "bureaucracyAndCorruption", "label": "Bureaucracy and Corruption", "index": "freedom", "subindex": "legal", "level": "indicator"},
    {"indicator_code": "security", "label": "Security", "index": "freedom", "subindex": "legal", "level": "indicator"},
    {"indicator_code": "clarityOfTheLaw", "label": "Clarity of the Law", "index": "freedom", "subindex": "legal", "level": "indicator"},
    {"indicator_code": "judicialIndependenceAndEffectiveness", "label": "Judicial Independence and Effectiveness", "index": "freedom", "subindex": "legal", "level": "indicator"},
    {"indicator_code": "informality", "label": "Informality", "index": "freedom", "subindex": "legal", "level": "indicator"},
    # Prosperity indicators
    {"indicator_code": "income", "label": "Income", "index": "prosperity", "subindex": None, "level": "indicator"},
    {"indicator_code": "health", "label": "Health", "index": "prosperity", "subindex": None, "level": "indicator"},
    {"indicator_code": "inequality", "label": "Inequality", "index": "prosperity", "subindex": None, "level": "indicator"},
    {"indicator_code": "environment", "label": "Environment", "index": "prosperity", "subindex": None, "level": "indicator"},
    {"indicator_code": "minorities", "label": "Minority Rights", "index": "prosperity", "subindex": None, "level": "indicator"},
    {"indicator_code": "education", "label": "Education", "index": "prosperity", "subindex": None, "level": "indicator"},
]

# Maps groupingsManifest.json keys to an entity_type label. The "countries" key
# in that manifest is intentionally absent here — countries come from
# countriesManifest.json so groupings are not double-counted.
GROUPING_KIND = {
    "global": "global",
    "regions": "region",
    "specialStates": "special-state",
    "freedomAndProsperityGroups": "status-group",
}
