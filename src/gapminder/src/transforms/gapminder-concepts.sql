-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Concept ids come from multiple Gapminder DDF repositories; use `repo` with `concept` when disambiguating source metadata.
SELECT
    "concept",
    "concept_type",
    "name",
    "name_short",
    "name_catalog",
    "description",
    "unit",
    "tags",
    "scales",
    "domain",
    "source_url",
    "format",
    "repo"
FROM "gapminder-concepts"
