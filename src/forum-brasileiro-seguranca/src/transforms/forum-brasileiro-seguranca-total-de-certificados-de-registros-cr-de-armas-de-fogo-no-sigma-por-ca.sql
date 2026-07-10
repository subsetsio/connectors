-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows may mix national, regional, state, capital, or other geography aggregation levels; filter geo_level before aggregating across geography.
SELECT
    "geography",
    "geo_level",
    "year",
    "measure",
    "value"
FROM "forum-brasileiro-seguranca-total-de-certificados-de-registros-cr-de-armas-de-fogo-no-sigma-por-ca"
