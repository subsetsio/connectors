# Journey North map taxonomy — the set of public migration-map layers exposed by
# the sightings_json endpoint. Verified live from the season index pages
# (https://maps.journeynorth.org/maps/<year>/{spring,fall}). This taxonomy is
# stable across years; older years simply return fewer/no sightings for a given
# map. Each value is one species + life-stage/event + season layer.
MAP_SLUGS = [
    "barn-swallow-first",
    "hummingbird-other",
    "hummingbird-other-spring",
    "hummingbird-ruby-throated-fall",
    "hummingbird-ruby-throated-first",
    "hummingbird-ruby-throated-spring",
    "ice-out",
    "loon-first",
    "milkweed",
    "milkweed-fall",
    "milkweed-first",
    "monarch-adult-fall",
    "monarch-adult-first",
    "monarch-adult-spring",
    "monarch-egg-fall",
    "monarch-egg-first",
    "monarch-egg-spring",
    "monarch-larva-fall",
    "monarch-larva-first",
    "monarch-larva-spring",
    "monarch-other-fall",
    "monarch-other-spring",
    "monarch-roost-fall",
    "oriole-first-baltimore",
    "practice-any-fall",
    "practice-any-spring",
    "red-winged-blackbird-first",
    "red-winged-blackbird-other-spring",
    "robin-fall",
    "robin-first",
    "signs-fall",
    "signs-spring-other",
    "tulips-bloomed",
    "tulips-spring",
]

# Journey North began collecting observations in 1994; the sightings_json
# endpoint returns data from this epoch forward. Only the START is fixed — the
# END of the range is discovered dynamically at fetch time (the current calendar
# year) so it never goes stale.
START_YEAR = 1994
