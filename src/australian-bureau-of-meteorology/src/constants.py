"""Static catalog data for the Australian Bureau of Meteorology connector.

Data, not logic: the water parameters we publish and the single canonical
daily timeseries-type we pull for each. BOM Water Data Online (KISTERS KiWIS)
exposes many timeseries variants per station-parameter (raw/received/harmonised
and DailyMin/Max/Mean across 09HR/24HR windows). We publish the quality-
controlled, merged daily series — the headline Water Data Online product —
choosing the aggregation that is meaningful for each parameter:

  * Rainfall / Evaporation -> daily TOTAL to 9am (BOM's standard "rain day").
  * everything else        -> daily MEAN (24h).

ts_name and parameter become columns on the published `values` table, so this
mapping is the set of series, not the schema.
"""

BASE_URL = "https://www.bom.gov.au/waterdata/services"

DAILY_TOTAL = "DMQaQc.Merged.DailyTotal.09HR"
DAILY_MEAN = "DMQaQc.Merged.DailyMean.24HR"

# The 11 named water parameters that carry observation data, mapped to the
# canonical daily timeseries-type we publish for each.
PARAM_DAILY_TSNAME = {
    "Rainfall": DAILY_TOTAL,
    "Evaporation": DAILY_TOTAL,
    "Ground Water Level": DAILY_MEAN,
    "Water Course Level": DAILY_MEAN,
    "Water Course Discharge": DAILY_MEAN,
    "Water Temperature": DAILY_MEAN,
    "Electrical Conductivity @ 25C": DAILY_MEAN,
    "pH": DAILY_MEAN,
    "Turbidity": DAILY_MEAN,
    "Storage Volume": DAILY_MEAN,
    "Storage Level": DAILY_MEAN,
}
