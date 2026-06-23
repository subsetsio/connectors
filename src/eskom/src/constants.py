"""Static catalog data for the Eskom Data Portal connector.

ENTITY_IDS is the rank-accepted entity union (copied from
data/sources/eskom/work/entity_union.json). PAGE_PATHS maps each entity to its
dashboard page under https://www.eskom.co.za/dataportal/ — the page whose
embedded Power BI 'publish to web' report holds the data. This is data, not
logic: which dashboards we pull, not how.
"""

PAGE_PATHS = {
    "financial-year-load-factor-eskom-ocgt": "ocgt-usage/financial-year-load-factor-eskom-ocgt/",
    "financial-year-load-factor-ipp-ocgt": "ocgt-usage/financial-year-load-factor-ipp-ocgt/",
    "hourly-renewable-generation": "renewables-performance/hourly-renewable-generation/",
    "hourly-uclf-oclf-trend": "outage-performance/hourly-uclfoclf-trend/",
    "monthly-generation-capacity-breakdown": "outage-performance/monthly-eskom-generation-capacity-breakdown/",
    "monthly-generation-unavailability": "outage-performance/monthly-eskom-generation-unavailability/",
    "official-hourly-forecast-next-3-months": "demand-side/official-hourly-forcast-for-next-3-months/",
    "pumped-storage-gas-mlr": "supply-side/pumped-storage-generating-hours-gas-generation-and-manual-load-reduction/",
    "renewable-statistics": "renewables-performance/renewable-statistics/",
    "station-build-up-last-7-days": "supply-side/station-build-up-for-the-last-7-days/",
    "system-hourly-actual-and-forecasted-demand": "demand-side/system-hourly-actual-and-forecasted-demand/",
    "system-hourly-demand-and-available-capacity": "demand-side/system-hourly-demand-and-available-capacity/",
    "total-monthly-ocgt-energy-utilization": "ocgt-usage/total-monthly-ocgt-eskom-ipp-and-gt-energy-utilization/",
    "weekly-energy-demand": "demand-side/weekly-energy-demand/",
    "weekly-generation-capacity-breakdown": "outage-performance/weekly-eskom-generation-capacity-breakdown/",
    "weekly-peak-demand": "demand-side/weekly-peak-demand/",
    "weekly-uclf-oclf-frequency": "outage-performance/weekly-uclfoclf-frequency/",
    "weekly-unplanned-outages": "outage-performance/weekly-unplanned-outages/",
    "wind-generation-weekly-load-factor": "renewables-performance/wind-generation-weekly-load-factor/",
}

ENTITY_IDS = list(PAGE_PATHS.keys())
