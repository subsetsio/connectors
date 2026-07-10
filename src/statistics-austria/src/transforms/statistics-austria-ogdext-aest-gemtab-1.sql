-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "jahr",
    "gcd",
    "gem_name",
    "bev_absolut",
    "bev_unter15",
    "bev_ueber65",
    "ausl_staatsb",
    "ewtq_15bis64",
    "alq_15plus",
    "edu_15_sek",
    "edu_15_ter",
    "auspendler",
    "phh",
    "hh_size",
    "familien",
    "unt",
    "ast",
    "besch_ast"
FROM "statistics-austria-ogdext-aest-gemtab-1"
