-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DeelgebiedenGWW" AS deelgebiedengww,
    "Perioden" AS perioden,
    "Inputprijsindex_1" AS inputprijsindex_1,
    "MutatieTenOpzichteVan1JaarEerder_2" AS mutatietenopzichtevan1jaareerder_2,
    "DeelgebiedenGWW_label" AS deelgebiedengww_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-81139ned"
