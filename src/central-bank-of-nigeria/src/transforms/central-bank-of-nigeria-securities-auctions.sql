-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: One row is one RESULT LINE of an auction, not one auction: a single auction can appear as several rows with different `rateDescription` values (`Issue`, `Maginal` [sic], `Stop`, `Slop` [sic]), so counting rows overstates the number of auctions and summing `totalSubscription` over them double-counts.
-- caution: The `securityType` domain is dirty: `FGN Bonds`, `FGN BOND`, `FGN BONDS`, `FGN Bond`, `Bonds` and `NT Bonds` all denote FGN bonds, and `OMOM` is a typo for `OMO`. Normalise before grouping by security type; the same applies to `netType` (`Purchases` vs `Purchase`).
-- caution: `maturityDate` contains data-entry typos: a handful of rows carry impossible maturity years (2098, 2189) against auction dates in 2001-2026. Sanity-check any computed tenor rather than trusting the maturity date.
-- caution: `tenor` is a free-text label whose convention changes over the series (`91DAY` in recent rows, bare `180` in the earliest ones) — it is a string, not a number of days.
-- caution: `rangeBid` and `successfulBidRates` are free-text low-high rate pairs (e.g. `15.5000 - 18.0000`), not numbers.
-- caution: Naira amounts (`totalSubscription`, `totalSuccessful`, `amtOffered`, `netValue`, `totalAmtRepaid`) are in millions; `rate` and `trueYield` are percent per annum. A `trueYield` of `0.0000` generally means not-reported rather than a zero yield.
SELECT
    "id",
    "auctionDate" AS auctiondate,
    "securityType" AS securitytype,
    "tenor",
    "auctionNo" AS auctionno,
    "auction",
    "week",
    "maturityDate" AS maturitydate,
    CAST("totalSubscription" AS DOUBLE) AS totalsubscription,
    "totalSuccessful" AS totalsuccessful,
    "rangeBid" AS rangebid,
    "successfulBidRates" AS successfulbidrates,
    "rateDescription" AS ratedescription,
    CAST("rate" AS DOUBLE) AS rate,
    "trueYield" AS trueyield,
    "amtOffered" AS amtoffered,
    "totalAmtRepaid" AS totalamtrepaid,
    "netType" AS nettype,
    "netValue" AS netvalue
FROM "central-bank-of-nigeria-securities-auctions"
