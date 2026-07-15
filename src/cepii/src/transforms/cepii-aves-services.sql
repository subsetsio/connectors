-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Services policy ad-valorem equivalents are sector and partner specific; avoid aggregating sectors or partners as additive trade values.
SELECT
    "Reference to be cited: Lionel Fontagné, Cristina Mitaritonna, Jose Signoret, ""Estimated Tariff Equivalents of Services NTMs"", CEPII, August 2016" AS citation_note,
    "source_file",
    "source_sheet",
    "GTAP_country_code" AS gtap_country_code,
    "sector",
    "eav_2004",
    "Unnamed: 3" AS separator_after_2004,
    "GTAP_country_code.1" AS gtap_country_code_1,
    "sector.1" AS sector_1,
    "eav_2007",
    "Unnamed: 7" AS separator_after_2007,
    "GTAP_country_code.2" AS gtap_country_code_2,
    "sector.2" AS sector_2,
    "eav_2011"
FROM "cepii-aves-services"
