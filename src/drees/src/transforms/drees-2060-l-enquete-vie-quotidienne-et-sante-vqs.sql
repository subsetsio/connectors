-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tableau",
    "url_d_acces"
FROM "drees-2060-l-enquete-vie-quotidienne-et-sante-vqs"
