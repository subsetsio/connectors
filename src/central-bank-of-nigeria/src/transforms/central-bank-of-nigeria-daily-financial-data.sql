-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `recDate` is NOT unique: 50 dates carry more than one row. About half of those are exact duplicates of the same observation and the rest are divergent restatements, so summing or averaging by date without deduplicating overstates the day.
-- caution: Every monetary column is a naira amount in millions, and `crr` (cash reserve requirement) is a balance rather than a flow — the columns describe different money-market operations and must not be summed into a total.
SELECT
    "id",
    strptime("recDate", '%d/%m/%Y')::DATE AS recdate,
    CAST("opeBal" AS DOUBLE) AS opebal,
    CAST("rediscBills" AS DOUBLE) AS rediscbills,
    CAST("slFacility" AS DOUBLE) AS slfacility,
    CAST("sdFacility" AS DOUBLE) AS sdfacility,
    CAST("repo" AS DOUBLE) AS repo,
    CAST("revRepo" AS DOUBLE) AS revrepo,
    CAST("omoSales" AS DOUBLE) AS omosales,
    CAST("omoRepay" AS DOUBLE) AS omorepay,
    CAST("pmSales" AS DOUBLE) AS pmsales,
    CAST("pmRepay" AS DOUBLE) AS pmrepay,
    CAST("crr" AS DOUBLE) AS crr,
    CAST("netWdas" AS DOUBLE) AS netwdas,
    CAST("statAlloc" AS DOUBLE) AS statalloc,
    CAST("jvCash" AS DOUBLE) AS jvcash,
    CAST("netClr" AS DOUBLE) AS netclr,
    CAST("ndicPrem" AS DOUBLE) AS ndicprem,
    CAST("oMajor" AS DOUBLE) AS omajor
FROM "central-bank-of-nigeria-daily-financial-data"
