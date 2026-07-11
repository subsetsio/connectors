-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristic" AS characteristic,
    "All biological and biomedical sciences fields" AS all_biological_and_biomedical_sciences_fields,
    "Biochemistry biophysics and molecular biology" AS biochemistry_biophysics_and_molecular_biology,
    "Bioinformatics biostatistics and computational biology" AS bioinformatics_biostatistics_and_computational_biology,
    "Biological and biomedical sciences general" AS biological_and_biomedical_sciences_general,
    "Cell/ cellular biology and anatomy" AS cell_cellular_biology_and_anatomy,
    "Ecology evolutionary biology and epidemiology" AS ecology_evolutionary_biology_and_epidemiology,
    "Genetics and genomics" AS genetics_and_genomics,
    "Microbiology and immunology" AS microbiology_and_immunology,
    "Neurobiology and neurosciences" AS neurobiology_and_neurosciences,
    "Pharmacology and toxicology" AS pharmacology_and_toxicology,
    "Physiology oncology and cancer biology" AS physiology_oncology_and_cancer_biology,
    "Biological and biomedical sciences other" AS biological_and_biomedical_sciences_other
FROM "ncses-nsf25349-tab009-004"
