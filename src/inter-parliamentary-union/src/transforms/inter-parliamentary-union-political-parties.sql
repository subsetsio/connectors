-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source can emit duplicate political_party_code rows; de-duplicate by party code and country before counting parties.
SELECT
    "political_party_code",
    "party_name",
    "political_party_country"
FROM "inter-parliamentary-union-political-parties"
