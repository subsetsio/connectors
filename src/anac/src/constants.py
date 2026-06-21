"""Catalog data for the ANAC connector — the rank-accepted entity union mapped
to how each one is fetched. Pure data, imported by src/nodes/anac.py.

Each value is a fetch descriptor:
  kind="file" : one CSV inside `path` selected by ASCII `match` token
                (used only where a directory holds several distinct datasets).
  kind="dir"  : every CSV directly inside `path` (a single- or multi-file
                snapshot series; nested sub-directories are ignored).
  kind="tree" : every CSV anywhere under `path` (year/month-partitioned series).
  kind="airfares" : sas.anac.gov.br monthly microdata, enumerated by date.

`path` is the directory under https://sistemas.anac.gov.br/dadosabertos/ with
real accents (the fetch code percent-encodes it).
"""

CATALOG = {
    # --- Aerodromos -------------------------------------------------------
    "aerodromos-aerodromos-privados-lista-de-aerodromos-privados-aerodromos-privados-aerodromosprivados": {
        "kind": "file",
        "path": "Aerodromos/Aeródromos Privados/Lista de aeródromos privados",
        "match": "aerodromosprivados",
    },
    "aerodromos-aerodromos-publicos-caracteristicas-gerais-pda-aerodromos-publicos-caracteristicas-gerais": {
        "kind": "dir",
        "path": "Aerodromos/Aeródromos Públicos/Características Gerais",
    },
    "aerodromos-aerodromos-publicos-lista-de-aerodromos-publicos-aerodromospublicos": {
        "kind": "dir",
        "path": "Aerodromos/Aeródromos Públicos/Lista de aeródromos públicos",
    },
    "aerodromos-aerodromos-publicos-pistas-de-pouso-e-decolagem-pda-aerodromos-publicos-pistas-pouso-decolagem": {
        "kind": "dir",
        "path": "Aerodromos/Aeródromos Públicos/Pistas de Pouso e Decolagem",
    },
    # --- Aeronaves --------------------------------------------------------
    "aeronaves-diretrizes-de-aeronavegabilidade-diretrizes-de-aeronavegabilidade": {
        "kind": "dir",
        "path": "Aeronaves/Diretrizes de Aeronavegabilidade",
    },
    "aeronaves-drones-cadastrados-historico-sisant": {
        "kind": "dir",
        "path": "Aeronaves/drones cadastrados/Historico",
    },
    "aeronaves-drones-cadastrados-sisant": {
        "kind": "dir",
        "path": "Aeronaves/drones cadastrados",
    },
    "aeronaves-livro-rab-livro-rab": {
        "kind": "dir",
        "path": "Aeronaves/Livro RAB",
    },
    "aeronaves-rab-dados-aeronaves": {
        "kind": "dir",
        "path": "Aeronaves/RAB",
    },
    "aeronaves-rab-historico-rab-historico-rab": {
        "kind": "dir",
        "path": "Aeronaves/RAB/Historico_RAB",
    },
    # --- Airfares (sas.anac.gov.br) --------------------------------------
    "airfares-domestic": {"kind": "airfares", "sub": "tarifadomestica"},
    "airfares-international": {"kind": "airfares", "sub": "tarifainternacional"},
    # --- Certificação e Outorga ------------------------------------------
    "certificacao-e-outorga-arrecadacao-de-outorgas-de-concessoes-aeroportuarias-arrecadacaodeoutorgas": {
        "kind": "dir",
        "path": "Certificação e Outorga/Arrecadação de Outorgas de Concessões Aeroportuárias",
    },
    "certificacao-e-outorga-dados-gerais-das-autorizacoes-de-aeroportos-autorizacoes-aerodromos": {
        "kind": "dir",
        "path": "Certificação e Outorga/Dados Gerais das Autorizações de Aeroportos",
    },
    "certificacao-e-outorga-dados-gerais-das-concessoes-de-aeroportos-concessoes-aeroportos": {
        "kind": "dir",
        "path": "Certificação e Outorga/Dados Gerais das Concessoes de Aeroportos",
    },
    "certificacao-e-outorga-demonstracoes-contabeis-de-concessoes-aeroportuarias-demonstracoescontabeis": {
        "kind": "dir",
        "path": "Certificação e Outorga/Demonstrações Contábeis de Concessões Aeroportuárias",
    },
    # --- fiscalizacao -----------------------------------------------------
    "fiscalizacao-lista-de-processos-administrativos-sancionadores-listadeprocessosadministrativossancionadores": {
        "kind": "dir",
        "path": "fiscalizacao/Lista de processos administrativos sancionadores",
    },
    "fiscalizacao-operacoes-de-fiscalizacao-fiscalizacoes": {
        "kind": "dir",
        "path": "fiscalizacao/Operações de fiscalização",
    },
    # --- Gestao Interna ---------------------------------------------------
    "gestao-interna-receita-liquida-receita-liquida": {
        "kind": "dir",
        "path": "Gestao Interna/Receita Liquida",
    },
    # --- Operador Aéreo ---------------------------------------------------
    "operador-aereo-demonstracoes-contabeis-de-empresas-brasileiras-de-transporte-aereo-publico-demonstracoes-contabeis": {
        "kind": "dir",
        "path": "Operador Aéreo/Demonstrações Contábeis de Empresas Brasileiras de Transporte Aéreo Público",
    },
    "operador-aereo-empresas-aereas-estrangeiras-pda-empresas-aereas-estrangeiros": {
        "kind": "dir",
        "path": "Operador Aéreo/Empresas Aereas Estrangeiras",
    },
    "operador-aereo-empresas-aereas-nacionais-pda-empresas-aereas-nacionais": {
        "kind": "dir",
        "path": "Operador Aéreo/Empresas Aereas Nacionais",
    },
    # --- Operador Aeroportuário ------------------------------------------
    "operador-aeroportuario-dados-de-movimentacao-aeroportuarias--partitioned": {
        "kind": "tree",
        "path": "Operador Aeroportuário/Dados de Movimentação Aeroportuárias",
    },
    "operador-aeroportuario-tarifas-aeroportuarias-tetos-tarifarios-e-reajustes-tarifarios-tarifas-aeroportuarias": {
        "kind": "dir",
        "path": "Operador Aeroportuário/Tarifas Aeroportuárias Tetos Tarifários e Reajustes Tarifários",
    },
    # --- Pessoal da Aviação Civil ----------------------------------------
    "pessoal-da-aviacao-civil-certificadosmedicos-certificadosmedicosv2-pda-quantidade-de-certificados-medicos-aeronauticos-v2": {
        "kind": "dir",
        "path": "Pessoal da Aviação Civil/CertificadosMedicos/CertificadosMedicosV2",
    },
    "pessoal-da-aviacao-civil-indicadores-pel-indicadorespel": {
        "kind": "dir",
        "path": "Pessoal da Aviação Civil/Indicadores PEL",
    },
    "pessoal-da-aviacao-civil-licencas-emitidas-licencas-emitidas": {
        "kind": "dir",
        "path": "Pessoal da Aviação Civil/Licencas Emitidas",
    },
    # --- Seguranca Operacional -------------------------------------------
    "seguranca-operacional-eventossegurancaoperacional-fauna-fauna": {
        "kind": "dir",
        "path": "Seguranca Operacional/EventosSegurancaOperacional/Fauna",
    },
    "seguranca-operacional-ocorrencia-v-ocorrencia-ampla": {
        "kind": "dir",
        "path": "Seguranca Operacional/Ocorrencia",
    },
    "seguranca-operacional-ocorrencias-de-dificuldades-em-servico-em-aeronaves-ocorrencias-de-dificuldades-em-servicos-em-aeronaves-historico": {
        "kind": "file",
        "path": "Seguranca Operacional/Ocorrências de Dificuldades em Serviço em Aeronaves",
        "match": "historico",
    },
    "seguranca-operacional-ocorrencias-de-dificuldades-em-servico-em-aeronaves-ocorrncias-de-dificuldades-em-servios-em-aeronaves-v2": {
        "kind": "file",
        "path": "Seguranca Operacional/Ocorrências de Dificuldades em Serviço em Aeronaves",
        "match": "v2",
    },
    "seguranca-operacional-recomendacao-de-seguranca-recomendacao-seguranca": {
        "kind": "dir",
        "path": "Seguranca Operacional/Recomendação de Segurança",
    },
    # --- Voos e operações aéreas -----------------------------------------
    "voos-e-operacoes-aereas-dados-do-consumidor-gov-dadosconsumidor": {
        "kind": "dir",
        "path": "Voos e operações aéreas/Dados do consumidor.gov",
    },
    "voos-e-operacoes-aereas-dados-estatisticos-do-transporte-aereo-dados-estatisticos": {
        "kind": "dir",
        "path": "Voos e operações aéreas/Dados Estatísticos do Transporte Aéreo",
    },
    "voos-e-operacoes-aereas-horas-voadas-de-aeronave-horas-voadas": {
        "kind": "dir",
        "path": "Voos e operações aéreas/Horas Voadas de Aeronave",
    },
    "voos-e-operacoes-aereas-monitoramento-slots--partitioned": {
        "kind": "tree",
        "path": "Voos e operações aéreas/Monitoramento Slots",
    },
    "voos-e-operacoes-aereas-percentuais-de-atrasos-e-cancelamentos--partitioned": {
        "kind": "tree",
        "path": "Voos e operações aéreas/Percentuais de atrasos e cancelamentos",
    },
    "voos-e-operacoes-aereas-registro-de-servicos-aereos--partitioned": {
        "kind": "tree",
        "path": "Voos e operações aéreas/Registro de serviços aéreos",
    },
    "voos-e-operacoes-aereas-slots-alocados--partitioned": {
        "kind": "tree",
        "path": "Voos e operações aéreas/Slots Alocados",
    },
    "voos-e-operacoes-aereas-voo-regular-ativo-vra--partitioned": {
        "kind": "tree",
        "path": "Voos e operações aéreas/Voo Regular Ativo (VRA)",
    },
}
