# Entity union for nhtsa-fars — the rank-active FARS tables (one Delta table each).
# Copied from data/sources/nhtsa-fars/work/entity_union.json. Data, not logic.
ENTITY_IDS = [
    "accident", "cevent", "crashrf", "damage", "distract", "drimpair",
    "driverrf", "drugs", "factor", "maneuver", "miacc", "midrvacc", "miper",
    "nmcrash", "nmdistract", "nmimpair", "nmprior", "parkwork", "pbtype",
    "person", "personrf", "pvehiclesf", "race", "safetyeq", "vehicle",
    "vehiclesf", "vevent", "violatn", "vision", "vpicdecode",
    "vpictrailerdecode", "vsoe", "weather",
]
