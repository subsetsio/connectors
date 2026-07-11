-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Academic year" AS academic_year,
    "LGD" AS lgd,
    "Local Government District" AS local_government_district,
    "APPTYPE" AS apptype,
    "Type of apprenticeship" AS type_of_apprenticeship,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-allapplgd"
