"""Static enumeration data for the Berkeley Earth temperature connector.

Berkeley Earth exposes NO directory listing (the S3 bucket denies list-type=2
and the Apache /auto tree returns 403 on directory URLs), so the set of region
slugs cannot be discovered from the server. It must be supplied here. Slugs are
lowercase-hyphenated region names; every entry below was verified HTTP 200 with
real content while probing. This is pull *data* (which regions populate the one
published time-series subset), not connector logic.

Cities (~8000 Local/ station series) are intentionally out of scope: they
require an external station-id list and would 24x the request volume for a long
tail of low-demand series.
"""

# Global products live only on the S3 bucket (not the /auto Apache tree).
# Each is one whitespace-delimited ASCII series with the standard 12-column
# (year, month, monthly/annual/5yr/10yr/20yr anomaly + uncertainty) layout.
# The land+ocean blend is TAVG-only; land-only is published for all three vars.
GLOBAL_PRODUCTS = [
    {"file": "Land_and_Ocean_complete.txt", "variable": "TAVG", "domain": "land_and_ocean"},
    {"file": "Complete_TAVG_complete.txt", "variable": "TAVG", "domain": "land"},
    {"file": "Complete_TMAX_complete.txt", "variable": "TMAX", "domain": "land"},
    {"file": "Complete_TMIN_complete.txt", "variable": "TMIN", "domain": "land"},
]

# Continents / hemispheres reachable on the /auto Regional tree.
CONTINENT_SLUGS = [
    "africa", "asia", "europe", "north-america", "south-america", "oceania",
    "antarctica", "australia", "northern-hemisphere", "southern-hemisphere",
    "contiguous-united-states",
]

# Countries. "georgia" here is the country Georgia; the US state is
# "georgia-(state)" under US_STATE_SLUGS.
COUNTRY_SLUGS = [
    "united-states", "united-kingdom", "france", "germany", "china", "india",
    "brazil", "russia", "canada", "australia", "japan", "mexico", "italy",
    "spain", "south-korea", "north-korea", "indonesia", "saudi-arabia",
    "turkey", "switzerland", "netherlands", "argentina", "sweden", "norway",
    "poland", "belgium", "thailand", "ireland", "austria", "nigeria", "egypt",
    "south-africa", "vietnam", "bangladesh", "iran", "iraq", "pakistan",
    "new-zealand", "greece", "portugal", "denmark", "finland", "czech-republic",
    "czechia", "romania", "ukraine", "hungary", "israel", "chile", "colombia",
    "peru", "venezuela", "kenya", "ethiopia", "morocco", "algeria", "ghana",
    "ivory-coast", "philippines", "malaysia", "singapore", "myanmar", "burma",
    "cambodia", "laos", "nepal", "sri-lanka", "afghanistan", "kazakhstan",
    "uzbekistan", "united-arab-emirates", "qatar", "kuwait", "iceland",
    "luxembourg", "croatia", "serbia", "bulgaria", "slovakia", "slovenia",
    "lithuania", "latvia", "estonia", "belarus", "moldova", "cuba", "jamaica",
    "haiti", "dominican-republic", "guatemala", "honduras", "nicaragua",
    "costa-rica", "panama", "ecuador", "bolivia", "paraguay", "uruguay",
    "georgia",
]

# US states (50). "georgia-(state)" disambiguates from the country.
US_STATE_SLUGS = [
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado",
    "connecticut", "delaware", "florida", "georgia-(state)", "hawaii",
    "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana",
    "maine", "maryland", "massachusetts", "michigan", "minnesota", "mississippi",
    "missouri", "montana", "nebraska", "nevada", "new-hampshire", "new-jersey",
    "new-mexico", "new-york", "north-carolina", "north-dakota", "ohio",
    "oklahoma", "oregon", "pennsylvania", "rhode-island", "south-carolina",
    "south-dakota", "tennessee", "texas", "utah", "vermont", "virginia",
    "washington", "west-virginia", "wisconsin", "wyoming",
]
