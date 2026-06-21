"""Dataset-id selections for the apple connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


STOREFRONTS = [
    "ae", "ag", "ai", "al", "am", "ao", "ar", "at", "au", "az",
    "bb", "be", "bf", "bg", "bh", "bj", "bm", "bn", "bo", "br",
    "bs", "bt", "bw", "by", "bz", "ca", "cg", "ch", "cl", "cn",
    "co", "cr", "cv", "cy", "cz", "de", "dk", "dm", "do", "dz",
    "ec", "ee", "eg", "es", "fi", "fj", "fm", "fr", "ga", "gb",
    "gd", "ge", "gh", "gm", "gr", "gt", "gw", "gy", "hk", "hn",
    "hr", "hu", "id", "ie", "il", "in", "iq", "is", "it", "jm",
    "jo", "jp", "ke", "kg", "kh", "kn", "kr", "kw", "ky", "kz",
    "la", "lb", "lc", "lk", "lr", "lt", "lu", "lv", "ly", "ma",
    "md", "me", "mg", "mk", "ml", "mn", "mo", "mr", "ms", "mt",
    "mu", "mv", "mw", "mx", "my", "mz", "na", "ne", "ng", "ni",
    "nl", "no", "np", "nz", "om", "pa", "pe", "pg", "ph", "pk",
    "pl", "pt", "pw", "py", "qa", "ro", "rs", "ru", "rw", "sa",
    "sb", "sc", "se", "sg", "si", "sk", "sl", "sn", "sr", "st",
    "sv", "sz", "tc", "td", "th", "tj", "tm", "tn", "tr", "tt",
    "tw", "tz", "ua", "ug", "us", "uy", "uz", "vc", "ve", "vg",
    "vn", "ye", "za", "zm", "zw",
]
