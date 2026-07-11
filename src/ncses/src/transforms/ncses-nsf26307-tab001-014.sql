-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Year" AS year,
    "Total" AS total,
    "Agricultural and veterinary sciencesa b" AS agricultural_and_veterinary_sciencesa_b,
    "Biological and biomedical sciencesa" AS biological_and_biomedical_sciencesa,
    "Communicationa c d" AS communicationa_c_d,
    "Computer and information sciences" AS computer_and_information_sciences,
    "Family and consumer sciences and human sciencesa c d" AS family_and_consumer_sciences_and_human_sciencesa_c_d,
    "Geosciences atmospheric and ocean sciences" AS geosciences_atmospheric_and_ocean_sciences,
    "Mathematics and statistics" AS mathematics_and_statistics,
    "Multidisciplinary and interdisciplinary sciencesa d" AS multidisciplinary_and_interdisciplinary_sciencesa_d,
    "Natural resources and conservationa" AS natural_resources_and_conservationa,
    "Neurobiology and neurosciencea d" AS neurobiology_and_neurosciencea_d,
    "Physical sciencesa" AS physical_sciencesa,
    "Psychologyb e" AS psychologyb_e,
    "Social sciencesa b" AS social_sciencesa_b
FROM "ncses-nsf26307-tab001-014"
