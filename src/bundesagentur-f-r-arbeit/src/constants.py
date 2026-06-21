# Entity union for bundesagentur-f-r-arbeit — copied from
# data/sources/bundesagentur-f-r-arbeit/work/entity_union.json.
# Each entity is one national statistical table published by the official
# "Statistik der Bundesagentur fuer Arbeit" BIDS API. TABLE_CODES maps each
# entity id to its stable national table code (the part after .../tableFetch/dia/).

ENTITY_IDS = [
    "alo-current",
    "alo-timeseries",
    "bb-current",
    "bb-timeseries",
    "bst-current",
    "bst-timeseries",
    "fst-current",
    "fst-timeseries",
    "grusi-current",
    "grusi-timeseries",
    "lstiii-current",
    "lstiii-timeseries",
    "stea-current",
    "stea-timeseries",
]

TABLE_CODES = {
    "alo-current": "EckwerteTabelleALOD",
    "alo-timeseries": "EckwerteZeitreiheALOD",
    "bb-current": "EckwerteTabelleBB",
    "bb-timeseries": "EckwerteZeitreiheBB",
    "bst-current": "EckwerteTabelleBST",
    "bst-timeseries": "EckwerteZeitreiheBSTD",
    "fst-current": "EckwerteTabelleFSTD",
    "fst-timeseries": "EckwerteZeitreiheFST",
    "grusi-current": "EckwerteTabelleGrusiDBL",
    "grusi-timeseries": "EckwerteZeitreiheGrusiDBL",
    "lstiii-current": "EckwerteTabelleLST",
    "lstiii-timeseries": "EckwerteZeitreiheLST",
    "stea-current": "EckwerteTabelleSTEA",
    "stea-timeseries": "EckwerteZeitreiheSTEAD",
}
