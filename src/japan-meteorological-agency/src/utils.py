"""Shared base URLs for the Japan Meteorological Agency (JMA) connector.

Two verified, unauthenticated surfaces:

  * bosai JSON family (www.jma.go.jp/bosai) — AMeDAS station registry, latest
    AMeDAS observation snapshot, forecast-area taxonomy, and per-office weather
    forecasts.
  * Tokyo Climate Center bulk CSV/text (ds.data.jma.go.jp/tcc) — global surface
    temperature anomaly series and ENSO/SST monitoring indices.
"""

BOSAI = "https://www.jma.go.jp/bosai"
TCC = "https://ds.data.jma.go.jp/tcc/tcc/products"
