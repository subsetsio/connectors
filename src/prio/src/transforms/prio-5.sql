-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Conflict-site rows are site-year observations; one conflict may have multiple sites or territories.
SELECT
    "id",
    "year",
    "latitude",
    "longitude",
    "radius",
    "conflict_area",
    "conflict_site",
    "conflict_territory",
    "version"
FROM "prio-5"
