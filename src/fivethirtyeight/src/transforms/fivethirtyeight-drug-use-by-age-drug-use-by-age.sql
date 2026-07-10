-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age",
    "n",
    "alcohol_use",
    "alcohol_frequency",
    "marijuana_use",
    "marijuana_frequency",
    "cocaine_use",
    "cocaine_frequency",
    "crack_use",
    "crack_frequency",
    "heroin_use",
    "heroin_frequency",
    "hallucinogen_use",
    "hallucinogen_frequency",
    "inhalant_use",
    "inhalant_frequency",
    "pain_releiver_use",
    "pain_releiver_frequency",
    "oxycontin_use",
    "oxycontin_frequency",
    "tranquilizer_use",
    "tranquilizer_frequency",
    "stimulant_use",
    "stimulant_frequency",
    "meth_use",
    "meth_frequency",
    "sedative_use",
    "sedative_frequency"
FROM "fivethirtyeight-drug-use-by-age-drug-use-by-age"
