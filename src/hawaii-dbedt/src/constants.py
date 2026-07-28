"""Entity-id selection for the hawaii-dbedt connector.

These are the rank-active DBEDT Data Warehouse *leaf category* ids (UHERO
universe 'DBEDT'). They are data, not logic, so they live here and are imported
back into the node module as ``from constants import ENTITY_IDS``. Upstream has
renumbered these category ids at least twice in July 2026; keep this list
aligned with the persisted collect/accept assets.
"""

ENTITY_IDS = [
    "32410", "32411", "32412", "32413", "32414", "32415", "32416",
    "32418", "32419", "32420", "32421", "32422", "32423", "32424",
    "32426", "32427", "32428",
    "32430", "32431", "32432", "32433", "32434", "32435", "32436",
    "32438", "32439",
    "32441", "32442", "32443", "32444", "32445", "32446", "32447", "32448",
    "32450", "32451", "32452", "32453", "32454", "32455", "32456", "32457",
    "32458", "32459", "32460", "32461", "32462",
    "32464", "32465", "32466", "32467",
    "32469", "32470",
    "32472", "32473", "32474", "32475", "32476", "32477",
]
