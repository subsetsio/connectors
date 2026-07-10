"""Dataset-id selections for the california-edd connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "0dfd4f0b-a3e3-4a66-8e49-ad119ec41564",
    "1d0bec3e-c865-4c32-ad9d-3bbf1f5d7db6",
    "2a5f872d-f7fe-49f2-9581-8f1b17ce5b90",
    "3f08b68e-1d1a-4ba4-a07d-1ec3392ed191",
    "3f530a9c-782f-4f34-bf51-9edaa448e0db",
    "4150784a-282a-4862-92bf-c3cf2e8fa722",
    "4275ba49-3a31-4200-852d-faf5b857bb4c",
    "4362f500-87c8-4842-834a-bbc14fe9a771",
    "59218446-5760-4683-b52e-f6210021840a",
    "6411456b-594b-4b73-af57-ce8dd401f2e2",
    "715d1324-ac02-4b11-b922-86bafa6eb80f",
    "74b655ae-6158-41ab-81ef-a02984a17cc1",
    "b16c1546-03e1-4bc2-95d2-863f68b54530",
    "b1ac39b1-33cc-4577-b584-6259406ce835",
    "c9416284-cabe-46a3-bdbc-d00ab5ab58f7",
    "f673ad7c-44ed-4c54-adc7-2f4b23eec557",
    "f9d2aa1a-5f94-468d-b5ef-26b3b9418694",
]
