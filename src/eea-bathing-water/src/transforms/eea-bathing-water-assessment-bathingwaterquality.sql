-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Quality classifications and microbiological percentiles are annual assessment results; compare within a season or bathing water before summarising across years.
SELECT
    "bathingWaterIdentifier" AS bathingwateridentifier,
    "classification",
    "countryCode" AS countrycode,
    "escherichiaColi90thPercentile" AS escherichiacoli90thpercentile,
    "escherichiaColi95thPercentile" AS escherichiacoli95thpercentile,
    "escherichiaColiAverageLog10" AS escherichiacoliaveragelog10,
    "escherichiaColiClassification" AS escherichiacoliclassification,
    "escherichiaColiNumberOfSamples" AS escherichiacolinumberofsamples,
    "escherichiaColiSampleStdDevLog10" AS escherichiacolisamplestddevlog10,
    "intestinalEnterococci90thPercentile" AS intestinalenterococci90thpercentile,
    "intestinalEnterococci95thPercentile" AS intestinalenterococci95thpercentile,
    "intestinalEnterococciAverageLog10" AS intestinalenterococciaveragelog10,
    "intestinalEnterococciClassification" AS intestinalenterococciclassification,
    "intestinalEnterococciNumberOfSamples" AS intestinalenterococcinumberofsamples,
    "intestinalEnterococciSampleStdDevLog10" AS intestinalenterococcisamplestddevlog10,
    "season",
    "UID" AS uid
FROM "eea-bathing-water-assessment-bathingwaterquality"
