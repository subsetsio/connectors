"""Dataset-id selections for the bank-of-latvia connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "115", "116", "121", "122", "123", "124", "126", "128", "129", "131", "132",
    "134", "135", "137", "141", "174", "175", "176", "177", "178", "179", "180",
    "181", "185", "187", "189", "193", "194", "195", "197", "198", "199", "200",
    "202", "208", "209", "213", "214", "217", "219", "222", "224", "225", "226",
    "227", "229", "230", "231", "232", "233", "239", "241", "243", "244", "245",
    "246", "250", "252", "254", "255", "256", "258", "260", "261", "264", "266",
    "271", "275", "278", "279", "282", "283", "285", "287", "289", "291", "293",
    "295", "297", "299", "301", "303", "306", "310", "311", "312", "317", "319",
    "321", "323", "325", "327", "329", "331", "333", "334", "336", "337", "339",
    "341", "343", "345", "347", "349", "352", "355", "357", "360", "363", "366",
    "368", "370", "372", "374", "376", "378", "379", "380", "381", "382", "383",
    "384", "385", "386", "387", "388", "390", "391", "392", "394", "396", "398",
    "400", "401", "403", "407",
]
