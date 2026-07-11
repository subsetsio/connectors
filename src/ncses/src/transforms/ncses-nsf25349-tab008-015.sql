-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristic" AS characteristic,
    "All humanities fields" AS all_humanities_fields,
    "English language and literature letters" AS english_language_and_literature_letters,
    "Foreign languages literatures and linguistics" AS foreign_languages_literatures_and_linguistics,
    "History" AS history,
    "Philosophy and religious studies" AS philosophy_and_religious_studies,
    "Humanities other" AS humanities_other
FROM "ncses-nsf25349-tab008-015"
