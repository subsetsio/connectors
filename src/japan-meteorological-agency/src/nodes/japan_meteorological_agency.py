from subsets_utils import NodeSpec

from nodes.amedas_observations import fetch_amedas_observations
from nodes.amedas_stations import fetch_amedas_stations
from nodes.enso_sst_indices import fetch_enso_sst_indices
from nodes.forecast_areas import fetch_forecast_areas
from nodes.global_temperature_anomaly import fetch_global_temperature_anomaly
from nodes.weather_forecasts import fetch_weather_forecasts


DOWNLOAD_SPECS = [
    NodeSpec(id="japan-meteorological-agency-amedas-observations", fn=fetch_amedas_observations, kind="download"),
    NodeSpec(id="japan-meteorological-agency-amedas-stations", fn=fetch_amedas_stations, kind="download"),
    NodeSpec(id="japan-meteorological-agency-enso-sst-indices", fn=fetch_enso_sst_indices, kind="download"),
    NodeSpec(id="japan-meteorological-agency-forecast-areas", fn=fetch_forecast_areas, kind="download"),
    NodeSpec(id="japan-meteorological-agency-global-temperature-anomaly", fn=fetch_global_temperature_anomaly, kind="download"),
    NodeSpec(id="japan-meteorological-agency-weather-forecasts", fn=fetch_weather_forecasts, kind="download"),
]
