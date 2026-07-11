"""Entity-id selection for the hawaii-dbedt connector.

These are the rank-active DBEDT Data Warehouse *leaf category* ids (UHERO
universe 'DBEDT'). They are data, not logic, so they live here and are imported
back into the node module as ``from constants import ENTITY_IDS``. The upstream
renumbered these category ids in July 2026; keep this list aligned with the
persisted collect/accept assets.
"""

ENTITY_IDS = [
    "32341", "32342", "32343", "32344", "32345", "32346", "32347",
    "32349", "32350", "32351", "32352", "32353", "32354", "32355",
    "32357", "32358", "32359",
    "32361", "32362", "32363", "32364", "32365", "32366", "32367",
    "32369", "32370",
    "32372", "32373", "32374", "32375", "32376", "32377", "32378", "32379",
    "32381", "32382", "32383", "32384", "32385", "32386", "32387", "32388",
    "32389", "32390", "32391", "32392", "32393",
    "32395", "32396", "32397", "32398",
    "32400", "32401",
    "32403", "32404", "32405", "32406", "32407", "32408",
]
