"""Dataset-id selections for the central-bank-taiwan connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    'BP01D01', 'BP01M01', 'BP01Y01', 'BPF4Y01', 'BPP2Q01', 'BPP2Y01', 'E95GM01', 'E95GY01',
    'EF01M01', 'EF01Y01', 'EF03M01', 'EF03Y01', 'EF05M01', 'EF05Y01', 'EF07M01', 'EF07Y01',
    'EF09M01', 'EF09Y01', 'EF10M01', 'EF11M01', 'EF11Y01', 'EF12M01', 'EF12Y01', 'EF13M01',
    'EF13Y01', 'EF15M01', 'EF15Y01', 'EF17M01', 'EF17Y01', 'EF19M01', 'EF19Y01', 'EF21M01',
    'EF21Y01', 'EF23M01', 'EF23Y01', 'EF25M01', 'EF25Y01', 'EF27M01', 'EF27Y01', 'EF29M01',
    'EF29Y01', 'EF35M01', 'EF35Y01', 'EF37M01', 'EF37Y01', 'EF39M01', 'EF39Y01', 'EF41M01',
    'EF41Y01', 'EF43M01', 'EF43Y01', 'EF45M01', 'EF45Y01', 'EF47M01', 'EF47Y01', 'EF49M01',
    'EF49Y01', 'EF55M01', 'EF55Y01', 'EF57M01', 'EF57Y01', 'EF59M01', 'EF59Y01', 'EF61M01',
    'EF61Y01', 'EF63M01', 'EF63Y01', 'EF64M01', 'EF64Y01', 'EF65M01', 'EF65Y01', 'EF67M01',
    'EF67Y01', 'EF69M01', 'EF69Y01', 'EF70M01', 'EF70Y01', 'EF71D01', 'EF72M01', 'EF72Y01',
    'EF73M01', 'EF73Y01', 'EF99M01', 'EF99Y01', 'EFA1M01', 'EFA1Y01', 'EFA4M01', 'EFA4Y01',
    'EG01M01', 'EG01Y01', 'EG02M01', 'EG02Y01', 'EG03M01', 'EG03Y01', 'EG05M01', 'EG05Y01',
    'EG07M01', 'EG07Y01', 'EG11D01', 'EG11M01', 'EG11Y01', 'EG13D01', 'EG13M01', 'EG13Y01',
    'EG15D01', 'EG15M01', 'EG15Y01', 'EG16D01', 'EG16M01', 'EG16Y01', 'EG17M01', 'EG17Y01',
    'EG19M01', 'EG19Y01', 'EG21M01', 'EG21Y01', 'EG23M01', 'EG23Y01', 'EG25M01', 'EG25Y01',
    'EG27M01', 'EG27Y01', 'EG28D01', 'EG2AM01', 'EG2AY01', 'EG2BM01', 'EG2BY01', 'EG2WM01',
    'EG30D01', 'EG37D01', 'EG37M01', 'EG37Y01', 'EG39Q01', 'EG39Y01', 'EG3WM01', 'EG41M01',
    'EG41Y01', 'EG43M01', 'EG43Y01', 'EG45M01', 'EG46M01', 'EG46Y01', 'EG47M01', 'EG47Y01',
    'EG49M01', 'EG49Y01', 'EG4ZD01', 'EG51D01', 'EG51M01', 'EG52M01', 'EG55D01', 'EG55M01',
    'EG55Y01', 'EG60D01', 'EG60M01', 'EG60Y01', 'EG65M01', 'EG65Y01', 'EG73M01', 'EG73Y01',
    'EG75M01', 'EG75Y01', 'EG77M01', 'EG77Y01', 'EGA4M01', 'EGA4Y01', 'EGA7M01', 'EGA9M01',
    'EGA9Y01', 'EGB4M01', 'EGB4Y01', 'EGC7Q01', 'EH45M01', 'EH45Y01', 'EI75M01', 'EI75Y01',
    'EI77M01', 'EI77Y01', 'EI79M01', 'EI79Y01', 'EI80M01', 'EI81M01', 'EI82M01', 'EI83M01',
    'EI84M01', 'EI85M01', 'EI85Y01', 'EI86M01', 'EI86Y01', 'EI87M01', 'EI87Y01', 'EI97M01',
    'EI97Y01', 'EI98M01', 'EI98Y01', 'EIA1M01', 'FL01_cn', 'FL02_cn',
]
