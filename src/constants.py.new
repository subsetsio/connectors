"""Catalog data for the ANAC connector — pure data, imported by src/nodes/anac.py.

One CATALOG entry per accept-approved collect entity. `path` is the directory
under https://sistemas.anac.gov.br/dadosabertos/ with real accents (the node
module percent-encodes it). Fetch kinds:

  family      every CSV directly in `path` whose date-stripped stem resolves to
              `family` — several distinct datasets share one ANAC directory, so
              the file set is matched by longest family prefix against FAMILIES.
  dir         every CSV directly in `path` (the directory holds one dataset and
              its file stems are pure dates, e.g. Historico_RAB/2026-06.csv).
  partitioned every CSV anywhere beneath `path`'s four-digit-year subdirectories.
              Non-year siblings are deliberately excluded: they are separate
              collect entities (e.g. deliberacoes-da-diretoria-colegiada holds a
              `reuniao-deliberativa-eletronica` subtree that accept rejected).
  airfares    sas.anac.gov.br monthly microdata, enumerated by date because that
              host serves no directory index.

FAMILIES lists every family anchored at a directory, including families whose
entity accept REJECTED. A rejected sibling still has to be known: ANAC re-encoded
some filenames, so `2019_Fila_Inspe<mojibake>o_Seguran<mojibake>a.csv` and
`2021_Fila_Inspecao_Seguranca.csv` are different families in the same directory,
and dropping the rejected one would silently widen the accepted one's file set.
"""

FAMILIES = {
    "Aerodromos/Aeródromos Privados/Lista de aeródromos privados/Aerodromos Privados": [
        "aerodromosprivados",
    ],
    "Aerodromos/Aeródromos Privados/Lista de aeródromos privados/Helideck": [
        "helidecks",
    ],
    "Aerodromos/Aeródromos Privados/Lista de aeródromos privados/Heliponto": [
        "helipontos",
    ],
    "Aerodromos/Aeródromos Públicos/Aerodromos Excluidos": [
        "aerodromos-publicos-excluidos",
    ],
    "Aerodromos/Aeródromos Públicos/Características Gerais": [
        "pda-aerodromos-publicos-caracteristicas-gerais",
    ],
    "Aerodromos/Aeródromos Públicos/Dados Pátio": [
        "v-aerodromo-publico-dados-patio",
    ],
    "Aerodromos/Aeródromos Públicos/Lista de aeródromos públicos": [
        "aerodromospublicos",
    ],
    "Aerodromos/Aeródromos Públicos/Pistas de Pouso e Decolagem": [
        "pda-aerodromos-publicos-pistas-pouso-decolagem",
    ],
    "Aerodromos/Aeródromos Públicos/Pistas de Táxi": [
        "pda-aerodromos-publicos-pistas-de-taxi",
    ],
    "Aerodromos/Aeródromos Públicos/Posicoes_Estacionamento": [
        "pda-aerodromos-publicos-posicoes-estacionamento",
    ],
    "Aerodromos/Aeródromos Públicos/Programa de Seguranca Aeroportuaria": [
        "psa",
    ],
    "Aerodromos/Aeródromos Públicos/Áreas de Pouso e Decolagem de Helicópteros": [
        "aerodromos-publicos-areas-de-pouso-e-decolagem-de-helicopteros",
    ],
    "Aerodromos/Lista de PZRs Registrados": [
        "pzr-pbzr-registrados",
        "pzr-pezr-registrados",
    ],
    "Aerodromos/PlanoDiretorAeroportuário": [
        "plano-diretor-aeroportuario-aprovados",
        "plano-diretor-aeroportuario-validados",
    ],
    "Aeronaves/Diretrizes de Aeronavegabilidade": [
        "diretrizes-de-aeronavegabilidade",
    ],
    "Aeronaves/Empresas Brasileiras Certificadas para fabricação de Produtos Aeronáuticos": [
        "empresasbrasileirascertificadas",
    ],
    "Aeronaves/Livro RAB": [
        "livro-rab",
    ],
    "Aeronaves/Organizações de Produção": [
        "organizacoes-de-producao",
        "organizaes-de-produo",
    ],
    "Aeronaves/PecasAprovadas": [
        "pecasaprovadas",
    ],
    "Aeronaves/ProcessosAdministrativosRelacionadosaAeronaves": [
        "processos-administrativos-rab",
    ],
    "Aeronaves/ProdutosAeronauticosCertificadosnoBrasil": [
        "produtosaeronauticos",
        "produtosaeronauticos-fabricantes",
    ],
    "Aeronaves/ProdutosAeronauticosGrandesModificacoes": [
        "produtosaeronauticosgrandesmodificacoes",
    ],
    "Aeronaves/RAB": [
        "dados-aeronaves",
    ],
    "Aeronaves/drones cadastrados": [
        "sisant",
    ],
    "Aeronaves/drones cadastrados/Historico": [
        "sisant",
    ],
    "Certificação e Outorga/Arrecadação de Outorgas de Concessões Aeroportuárias": [
        "arrecadacaodeoutorgas",
    ],
    "Certificação e Outorga/Dados Gerais das Autorizações de Aeroportos": [
        "autorizacoes-aerodromos",
    ],
    "Certificação e Outorga/Dados Gerais das Concessoes de Aeroportos": [
        "concessoes-aeroportos",
    ],
    "Certificação e Outorga/Demonstrações Contábeis de Concessões Aeroportuárias": [
        "demonstracoescontabeis",
    ],
    "Certificação e Outorga/Indicadores de Qualidade de Serviços": [
        "atendimento-pnae",
        "atendimento-ponte",
        "disponibilidade-tabela1",
        "disponibilidade-tabela2",
        "eventos-graves",
        "fila-inspecao-seguranca",
        "fila-inspeo-segurana",
        "fluxo-pista",
        "psp",
    ],
    "Certificação e Outorga/Inventário de Bens de Aeroportos Concedidos": [
        "inventariodebens",
    ],
    "Certificação e Outorga/Seguros dos Contratos das Concessões de Aeroportos": [
        "seguros-dos-contratos-das-concessoes-de-aeroportos",
    ],
    "Gestao Interna/Convenios e Congeneres": [
        "convenios-congeneres",
    ],
    "Gestao Interna/Informacoes de Terceirizados": [
        "terceirizados",
    ],
    "Gestao Interna/Informacoes sobre Contratos e Licitacoes": [
        "informacoes-sobre-contratos-e-licitacoes",
    ],
    "Gestao Interna/Informações sobre viagens realizadas - PCDP": [
        "scdp",
    ],
    "Gestao Interna/Lista de TFAC": [
        "lista-tfac",
    ],
    "Gestao Interna/Manifestacoes de Usuarios": [
        "manifestacoesusuarios",
    ],
    "Gestao Interna/Pesquisa de Serviços": [
        "pesquisaservicos",
    ],
    "Gestao Interna/Processos Administrativos Cadastrados": [
        "processos-administrativos-cadastrados",
    ],
    "Gestao Interna/ProgramasCapacitacaoANAC": [
        "programascapacitacaoanac",
    ],
    "Gestao Interna/Receita Liquida": [
        "receita-liquida",
    ],
    "Gestao Interna/TFAC Voo Simples": [
        "tfac",
        "tfacmicro",
    ],
    "Operador Aeroportuário/Tarifas Aeroportuárias Tetos Tarifários e Reajustes Tarifários": [
        "tarifas-aeroportuarias",
    ],
    "Operador Aéreo": [
        "pda-empresas-aereas-nacionais",
    ],
    "Operador Aéreo/Demonstrações Contábeis de Empresas Brasileiras de Transporte Aéreo Público": [
        "demonstracoes-contabeis",
    ],
    "Operador Aéreo/Empresas Aereas Estrangeiras": [
        "pda-empresas-aereas-estrangeiros",
    ],
    "Operador Aéreo/Empresas Aereas Nacionais": [
        "pda-empresas-aereas-nacionais",
    ],
    "Organizações de Formação/Centros de Instrução Homologados AVSEC": [
        "centrosinstrucaohomologados",
    ],
    "Organizações de Formação/Escolas da Aviação Civil": [
        "alunos-estrangeiros",
        "ciac",
        "ciac-cursos",
        "coordenadores",
        "cursos",
        "escolas",
        "examinadores",
    ],
    "Organizações de Formação/Lista de Treinamento de Tipo": [
        "lista-treinamento-tipo-inicial",
        "lista-treinamento-tipo-periodico",
    ],
    "Organizações de Formação/Simuladores de Voo com Qualificação ANAC válida": [
        "simuladores",
    ],
    "Organizações de Manutenção/Oficinas de Manutenção": [
        "oficinasmanutencao",
    ],
    "Organizações de Manutenção/Oficinas de Manutenção/Oficinas_Manutencao_Estrutura_Antiga": [
        "organizacoesdemanutencao",
        "organizacoesdemanutencao-padroes",
        "organizacoesdemanutencao-produtos",
    ],
    "Pessoal da Aviação Civil": [
        "clinicasmedicos",
    ],
    "Pessoal da Aviação Civil/CertificadosMedicos": [
        "certificadosmedicos",
    ],
    "Pessoal da Aviação Civil/CertificadosMedicos/CertificadosMedicosV2": [
        "pda-quantidade-de-certificados-medicos-aeronauticos-v2",
    ],
    "Pessoal da Aviação Civil/Clínicas e Médicos Credenciados": [
        "clinicas-e-medicos-credenciados",
        "clinicasmedicos",
    ],
    "Pessoal da Aviação Civil/Indicadores PEL": [
        "indicadorespel",
    ],
    "Pessoal da Aviação Civil/Licencas Emitidas": [
        "licencas-emitidas",
    ],
    "Pessoal da Aviação Civil/Profissionais Credenciados": [
        "profissionaiscredenciados",
    ],
    "Seguranca Operacional/EventosSegurancaOperacional/Fauna": [
        "fauna",
    ],
    "Seguranca Operacional/Ocorrencia": [
        "v-ocorrencia-ampla",
    ],
    "Seguranca Operacional/Ocorrências de Dificuldades em Serviço em Aeronaves": [
        "ocorrencias-de-dificuldades-em-servicos-em-aeronaves-historico",
        "ocorrncias-de-dificuldades-em-servios-em-aeronaves-v2",
    ],
    "Seguranca Operacional/Recomendação de Segurança": [
        "recomendacao-seguranca",
    ],
    "Voos e operações aéreas/Dados Estatísticos do Transporte Aéreo": [
        "dados-estatisticos",
    ],
    "Voos e operações aéreas/Dados do consumidor.gov": [
        "dadosconsumidor",
    ],
    "Voos e operações aéreas/Dados do consumidor.gov/Dados_Consumidor_Estrutura_Antiga": [
        "dadosdoconsumidor",
    ],
    "Voos e operações aéreas/Horas Voadas de Aeronave": [
        "horas-voadas",
    ],
    "fiscalizacao/Lista de processos administrativos sancionadores": [
        "listadeprocessosadministrativossancionadores",
    ],
    "fiscalizacao/Operações de fiscalização": [
        "fiscalizacoes",
    ],
    "fiscalizacao/Quantidade de Fiscalizacoes de Controle de Qualidade AVSEC": [
        "fiscalizacoes-avsec-aereos",
        "fiscalizacoes-avsec-aerodromos",
    ],
    "fiscalizacao/Quantidade de Providências Administrativas Decorrentes de Controle de Qualidade AVSEC": [
        "providencias-avsec-aereos",
        "providencias-avsec-aerodromos",
    ],
    "regulamentacao/Agenda Regulatória": [
        "agenda-regulatoria",
    ],
    "regulamentacao/Atendimento das demandas oriundas dos órgãos de controle": [
        "atendimento-das-demandas-oriundas-dos-rgos-de-controle-cgutcu",
    ],
}

CATALOG = {
    "aerodromos-aerodromos-privados-lista-de-aerodromos-privados-aerodromos-privados-aerodromosprivados": {
        "kind": "family",
        "path": "Aerodromos/Aeródromos Privados/Lista de aeródromos privados/Aerodromos Privados",
        "family": "aerodromosprivados",
    },
    "aerodromos-aerodromos-privados-lista-de-aerodromos-privados-helideck-helidecks": {
        "kind": "family",
        "path": "Aerodromos/Aeródromos Privados/Lista de aeródromos privados/Helideck",
        "family": "helidecks",
    },
    "aerodromos-aerodromos-privados-lista-de-aerodromos-privados-heliponto-helipontos": {
        "kind": "family",
        "path": "Aerodromos/Aeródromos Privados/Lista de aeródromos privados/Heliponto",
        "family": "helipontos",
    },
    "aerodromos-aerodromos-publicos-aerodromos-excluidos-aerodromos-publicos-excluidos": {
        "kind": "family",
        "path": "Aerodromos/Aeródromos Públicos/Aerodromos Excluidos",
        "family": "aerodromos-publicos-excluidos",
    },
    "aerodromos-aerodromos-publicos-areas-de-pouso-e-decolagem-de-helicopteros-aerodromos-publicos-areas-de-pouso-e-decolagem-de-helicopteros": {
        "kind": "family",
        "path": "Aerodromos/Aeródromos Públicos/Áreas de Pouso e Decolagem de Helicópteros",
        "family": "aerodromos-publicos-areas-de-pouso-e-decolagem-de-helicopteros",
    },
    "aerodromos-aerodromos-publicos-caracteristicas-gerais-pda-aerodromos-publicos-caracteristicas-gerais": {
        "kind": "family",
        "path": "Aerodromos/Aeródromos Públicos/Características Gerais",
        "family": "pda-aerodromos-publicos-caracteristicas-gerais",
    },
    "aerodromos-aerodromos-publicos-dados-patio-v-aerodromo-publico-dados-patio": {
        "kind": "family",
        "path": "Aerodromos/Aeródromos Públicos/Dados Pátio",
        "family": "v-aerodromo-publico-dados-patio",
    },
    "aerodromos-aerodromos-publicos-lista-de-aerodromos-publicos-aerodromospublicos": {
        "kind": "family",
        "path": "Aerodromos/Aeródromos Públicos/Lista de aeródromos públicos",
        "family": "aerodromospublicos",
    },
    "aerodromos-aerodromos-publicos-pistas-de-pouso-e-decolagem-pda-aerodromos-publicos-pistas-pouso-decolagem": {
        "kind": "family",
        "path": "Aerodromos/Aeródromos Públicos/Pistas de Pouso e Decolagem",
        "family": "pda-aerodromos-publicos-pistas-pouso-decolagem",
    },
    "aerodromos-aerodromos-publicos-pistas-de-taxi-pda-aerodromos-publicos-pistas-de-taxi": {
        "kind": "family",
        "path": "Aerodromos/Aeródromos Públicos/Pistas de Táxi",
        "family": "pda-aerodromos-publicos-pistas-de-taxi",
    },
    "aerodromos-aerodromos-publicos-posicoes-estacionamento-pda-aerodromos-publicos-posicoes-estacionamento": {
        "kind": "family",
        "path": "Aerodromos/Aeródromos Públicos/Posicoes_Estacionamento",
        "family": "pda-aerodromos-publicos-posicoes-estacionamento",
    },
    "aerodromos-aerodromos-publicos-programa-de-seguranca-aeroportuaria-psa": {
        "kind": "family",
        "path": "Aerodromos/Aeródromos Públicos/Programa de Seguranca Aeroportuaria",
        "family": "psa",
    },
    "aerodromos-lista-de-pzrs-registrados-pzr-pbzr-registrados": {
        "kind": "family",
        "path": "Aerodromos/Lista de PZRs Registrados",
        "family": "pzr-pbzr-registrados",
    },
    "aerodromos-lista-de-pzrs-registrados-pzr-pezr-registrados": {
        "kind": "family",
        "path": "Aerodromos/Lista de PZRs Registrados",
        "family": "pzr-pezr-registrados",
    },
    "aerodromos-planodiretoraeroportuario-plano-diretor-aeroportuario-aprovados": {
        "kind": "family",
        "path": "Aerodromos/PlanoDiretorAeroportuário",
        "family": "plano-diretor-aeroportuario-aprovados",
    },
    "aerodromos-planodiretoraeroportuario-plano-diretor-aeroportuario-validados": {
        "kind": "family",
        "path": "Aerodromos/PlanoDiretorAeroportuário",
        "family": "plano-diretor-aeroportuario-validados",
    },
    "aeronaves-diretrizes-de-aeronavegabilidade-diretrizes-de-aeronavegabilidade": {
        "kind": "family",
        "path": "Aeronaves/Diretrizes de Aeronavegabilidade",
        "family": "diretrizes-de-aeronavegabilidade",
    },
    "aeronaves-drones-cadastrados-historico-sisant": {
        "kind": "family",
        "path": "Aeronaves/drones cadastrados/Historico",
        "family": "sisant",
    },
    "aeronaves-drones-cadastrados-sisant": {
        "kind": "family",
        "path": "Aeronaves/drones cadastrados",
        "family": "sisant",
    },
    "aeronaves-empresas-brasileiras-certificadas-para-fabricacao-de-produtos-aeronauticos-empresasbrasileirascertificadas": {
        "kind": "family",
        "path": "Aeronaves/Empresas Brasileiras Certificadas para fabricação de Produtos Aeronáuticos",
        "family": "empresasbrasileirascertificadas",
    },
    "aeronaves-livro-rab-livro-rab": {
        "kind": "family",
        "path": "Aeronaves/Livro RAB",
        "family": "livro-rab",
    },
    "aeronaves-organizacoes-de-producao-organizacoes-de-producao": {
        "kind": "family",
        "path": "Aeronaves/Organizações de Produção",
        "family": "organizacoes-de-producao",
    },
    "aeronaves-organizacoes-de-producao-organizaes-de-produo": {
        "kind": "family",
        "path": "Aeronaves/Organizações de Produção",
        "family": "organizaes-de-produo",
    },
    "aeronaves-pecasaprovadas-pecasaprovadas": {
        "kind": "family",
        "path": "Aeronaves/PecasAprovadas",
        "family": "pecasaprovadas",
    },
    "aeronaves-processosadministrativosrelacionadosaaeronaves-processos-administrativos-rab": {
        "kind": "family",
        "path": "Aeronaves/ProcessosAdministrativosRelacionadosaAeronaves",
        "family": "processos-administrativos-rab",
    },
    "aeronaves-produtosaeronauticoscertificadosnobrasil-produtosaeronauticos": {
        "kind": "family",
        "path": "Aeronaves/ProdutosAeronauticosCertificadosnoBrasil",
        "family": "produtosaeronauticos",
    },
    "aeronaves-produtosaeronauticoscertificadosnobrasil-produtosaeronauticos-fabricantes": {
        "kind": "family",
        "path": "Aeronaves/ProdutosAeronauticosCertificadosnoBrasil",
        "family": "produtosaeronauticos-fabricantes",
    },
    "aeronaves-produtosaeronauticosgrandesmodificacoes-produtosaeronauticosgrandesmodificacoes": {
        "kind": "family",
        "path": "Aeronaves/ProdutosAeronauticosGrandesModificacoes",
        "family": "produtosaeronauticosgrandesmodificacoes",
    },
    "aeronaves-rab-dados-aeronaves": {
        "kind": "family",
        "path": "Aeronaves/RAB",
        "family": "dados-aeronaves",
    },
    "aeronaves-rab-historico-rab-historico-rab": {
        "kind": "dir",
        "path": "Aeronaves/RAB/Historico_RAB",
    },
    "airfares-domestic": {
        "kind": "airfares",
        "sub": "tarifadomestica",
    },
    "airfares-international": {
        "kind": "airfares",
        "sub": "tarifainternacional",
    },
    "certificacao-e-outorga-arrecadacao-de-outorgas-de-concessoes-aeroportuarias-arrecadacaodeoutorgas": {
        "kind": "family",
        "path": "Certificação e Outorga/Arrecadação de Outorgas de Concessões Aeroportuárias",
        "family": "arrecadacaodeoutorgas",
    },
    "certificacao-e-outorga-dados-gerais-das-autorizacoes-de-aeroportos-autorizacoes-aerodromos": {
        "kind": "family",
        "path": "Certificação e Outorga/Dados Gerais das Autorizações de Aeroportos",
        "family": "autorizacoes-aerodromos",
    },
    "certificacao-e-outorga-dados-gerais-das-concessoes-de-aeroportos-concessoes-aeroportos": {
        "kind": "family",
        "path": "Certificação e Outorga/Dados Gerais das Concessoes de Aeroportos",
        "family": "concessoes-aeroportos",
    },
    "certificacao-e-outorga-demonstracoes-contabeis-de-concessoes-aeroportuarias-demonstracoescontabeis": {
        "kind": "family",
        "path": "Certificação e Outorga/Demonstrações Contábeis de Concessões Aeroportuárias",
        "family": "demonstracoescontabeis",
    },
    "certificacao-e-outorga-indicadores-de-qualidade-de-servicos-atendimento-pnae": {
        "kind": "family",
        "path": "Certificação e Outorga/Indicadores de Qualidade de Serviços",
        "family": "atendimento-pnae",
    },
    "certificacao-e-outorga-indicadores-de-qualidade-de-servicos-disponibilidade-tabela1": {
        "kind": "family",
        "path": "Certificação e Outorga/Indicadores de Qualidade de Serviços",
        "family": "disponibilidade-tabela1",
    },
    "certificacao-e-outorga-indicadores-de-qualidade-de-servicos-disponibilidade-tabela2": {
        "kind": "family",
        "path": "Certificação e Outorga/Indicadores de Qualidade de Serviços",
        "family": "disponibilidade-tabela2",
    },
    "certificacao-e-outorga-indicadores-de-qualidade-de-servicos-eventos-graves": {
        "kind": "family",
        "path": "Certificação e Outorga/Indicadores de Qualidade de Serviços",
        "family": "eventos-graves",
    },
    "certificacao-e-outorga-indicadores-de-qualidade-de-servicos-fila-inspecao-seguranca": {
        "kind": "family",
        "path": "Certificação e Outorga/Indicadores de Qualidade de Serviços",
        "family": "fila-inspecao-seguranca",
    },
    "certificacao-e-outorga-indicadores-de-qualidade-de-servicos-psp": {
        "kind": "family",
        "path": "Certificação e Outorga/Indicadores de Qualidade de Serviços",
        "family": "psp",
    },
    "certificacao-e-outorga-inventario-de-bens-de-aeroportos-concedidos-inventariodebens": {
        "kind": "family",
        "path": "Certificação e Outorga/Inventário de Bens de Aeroportos Concedidos",
        "family": "inventariodebens",
    },
    "certificacao-e-outorga-seguros-dos-contratos-das-concessoes-de-aeroportos-seguros-dos-contratos-das-concessoes-de-aeroportos": {
        "kind": "family",
        "path": "Certificação e Outorga/Seguros dos Contratos das Concessões de Aeroportos",
        "family": "seguros-dos-contratos-das-concessoes-de-aeroportos",
    },
    "fiscalizacao-decisoes-monocraticas-de-processos-em-segunda-instancia--partitioned": {
        "kind": "partitioned",
        "path": "fiscalizacao/decisoes-monocraticas-de-processos-em-segunda-instancia",
    },
    "fiscalizacao-deliberacoes-da-diretoria-colegiada--partitioned": {
        "kind": "partitioned",
        "path": "fiscalizacao/deliberacoes-da-diretoria-colegiada",
    },
    "fiscalizacao-lista-de-processos-administrativos-sancionadores-listadeprocessosadministrativossancionadores": {
        "kind": "family",
        "path": "fiscalizacao/Lista de processos administrativos sancionadores",
        "family": "listadeprocessosadministrativossancionadores",
    },
    "fiscalizacao-operacoes-de-fiscalizacao-fiscalizacoes": {
        "kind": "family",
        "path": "fiscalizacao/Operações de fiscalização",
        "family": "fiscalizacoes",
    },
    "fiscalizacao-quantidade-de-fiscalizacoes-de-controle-de-qualidade-avsec-fiscalizacoes-avsec-aereos": {
        "kind": "family",
        "path": "fiscalizacao/Quantidade de Fiscalizacoes de Controle de Qualidade AVSEC",
        "family": "fiscalizacoes-avsec-aereos",
    },
    "fiscalizacao-quantidade-de-fiscalizacoes-de-controle-de-qualidade-avsec-fiscalizacoes-avsec-aerodromos": {
        "kind": "family",
        "path": "fiscalizacao/Quantidade de Fiscalizacoes de Controle de Qualidade AVSEC",
        "family": "fiscalizacoes-avsec-aerodromos",
    },
    "fiscalizacao-quantidade-de-providencias-administrativas-decorrentes-de-controle-de-qualidade-avsec-providencias-avsec-aereos": {
        "kind": "family",
        "path": "fiscalizacao/Quantidade de Providências Administrativas Decorrentes de Controle de Qualidade AVSEC",
        "family": "providencias-avsec-aereos",
    },
    "fiscalizacao-quantidade-de-providencias-administrativas-decorrentes-de-controle-de-qualidade-avsec-providencias-avsec-aerodromos": {
        "kind": "family",
        "path": "fiscalizacao/Quantidade de Providências Administrativas Decorrentes de Controle de Qualidade AVSEC",
        "family": "providencias-avsec-aerodromos",
    },
    "fiscalizacao-sessoes-de-julgamento-de-processos-em-segunda-instancia--partitioned": {
        "kind": "partitioned",
        "path": "fiscalizacao/sessoes-de-julgamento-de-processos-em-segunda-instancia",
    },
    "gestao-interna-convenios-e-congeneres-convenios-congeneres": {
        "kind": "family",
        "path": "Gestao Interna/Convenios e Congeneres",
        "family": "convenios-congeneres",
    },
    "gestao-interna-informacoes-de-terceirizados-terceirizados": {
        "kind": "family",
        "path": "Gestao Interna/Informacoes de Terceirizados",
        "family": "terceirizados",
    },
    "gestao-interna-informacoes-sobre-contratos-e-licitacoes-informacoes-sobre-contratos-e-licitacoes": {
        "kind": "family",
        "path": "Gestao Interna/Informacoes sobre Contratos e Licitacoes",
        "family": "informacoes-sobre-contratos-e-licitacoes",
    },
    "gestao-interna-informacoes-sobre-viagens-realizadas-pcdp-scdp": {
        "kind": "family",
        "path": "Gestao Interna/Informações sobre viagens realizadas - PCDP",
        "family": "scdp",
    },
    "gestao-interna-lista-de-tfac-lista-tfac": {
        "kind": "family",
        "path": "Gestao Interna/Lista de TFAC",
        "family": "lista-tfac",
    },
    "gestao-interna-manifestacoes-de-usuarios-manifestacoesusuarios": {
        "kind": "family",
        "path": "Gestao Interna/Manifestacoes de Usuarios",
        "family": "manifestacoesusuarios",
    },
    "gestao-interna-pesquisa-de-servicos-pesquisaservicos": {
        "kind": "family",
        "path": "Gestao Interna/Pesquisa de Serviços",
        "family": "pesquisaservicos",
    },
    "gestao-interna-processos-administrativos-cadastrados-processos-administrativos-cadastrados": {
        "kind": "family",
        "path": "Gestao Interna/Processos Administrativos Cadastrados",
        "family": "processos-administrativos-cadastrados",
    },
    "gestao-interna-programascapacitacaoanac-programascapacitacaoanac": {
        "kind": "family",
        "path": "Gestao Interna/ProgramasCapacitacaoANAC",
        "family": "programascapacitacaoanac",
    },
    "gestao-interna-receita-liquida-receita-liquida": {
        "kind": "family",
        "path": "Gestao Interna/Receita Liquida",
        "family": "receita-liquida",
    },
    "gestao-interna-tfac-voo-simples-tfac": {
        "kind": "family",
        "path": "Gestao Interna/TFAC Voo Simples",
        "family": "tfac",
    },
    "gestao-interna-tfac-voo-simples-tfacmicro": {
        "kind": "family",
        "path": "Gestao Interna/TFAC Voo Simples",
        "family": "tfacmicro",
    },
    "operador-aereo-demonstracoes-contabeis-de-empresas-brasileiras-de-transporte-aereo-publico-demonstracoes-contabeis": {
        "kind": "family",
        "path": "Operador Aéreo/Demonstrações Contábeis de Empresas Brasileiras de Transporte Aéreo Público",
        "family": "demonstracoes-contabeis",
    },
    "operador-aereo-empresas-aereas-estrangeiras-pda-empresas-aereas-estrangeiros": {
        "kind": "family",
        "path": "Operador Aéreo/Empresas Aereas Estrangeiras",
        "family": "pda-empresas-aereas-estrangeiros",
    },
    "operador-aereo-empresas-aereas-nacionais-pda-empresas-aereas-nacionais": {
        "kind": "family",
        "path": "Operador Aéreo/Empresas Aereas Nacionais",
        "family": "pda-empresas-aereas-nacionais",
    },
    "operador-aereo-pda-empresas-aereas-nacionais": {
        "kind": "family",
        "path": "Operador Aéreo",
        "family": "pda-empresas-aereas-nacionais",
    },
    "operador-aeroportuario-dados-de-movimentacao-aeroportuarias--partitioned": {
        "kind": "partitioned",
        "path": "Operador Aeroportuário/Dados de Movimentação Aeroportuárias",
    },
    "operador-aeroportuario-tarifas-aeroportuarias-tetos-tarifarios-e-reajustes-tarifarios-tarifas-aeroportuarias": {
        "kind": "family",
        "path": "Operador Aeroportuário/Tarifas Aeroportuárias Tetos Tarifários e Reajustes Tarifários",
        "family": "tarifas-aeroportuarias",
    },
    "organizacoes-de-formacao-centros-de-instrucao-homologados-avsec-centrosinstrucaohomologados": {
        "kind": "family",
        "path": "Organizações de Formação/Centros de Instrução Homologados AVSEC",
        "family": "centrosinstrucaohomologados",
    },
    "organizacoes-de-formacao-escolas-da-aviacao-civil-alunos-estrangeiros": {
        "kind": "family",
        "path": "Organizações de Formação/Escolas da Aviação Civil",
        "family": "alunos-estrangeiros",
    },
    "organizacoes-de-formacao-escolas-da-aviacao-civil-ciac": {
        "kind": "family",
        "path": "Organizações de Formação/Escolas da Aviação Civil",
        "family": "ciac",
    },
    "organizacoes-de-formacao-escolas-da-aviacao-civil-ciac-cursos": {
        "kind": "family",
        "path": "Organizações de Formação/Escolas da Aviação Civil",
        "family": "ciac-cursos",
    },
    "organizacoes-de-formacao-escolas-da-aviacao-civil-coordenadores": {
        "kind": "family",
        "path": "Organizações de Formação/Escolas da Aviação Civil",
        "family": "coordenadores",
    },
    "organizacoes-de-formacao-escolas-da-aviacao-civil-cursos": {
        "kind": "family",
        "path": "Organizações de Formação/Escolas da Aviação Civil",
        "family": "cursos",
    },
    "organizacoes-de-formacao-escolas-da-aviacao-civil-escolas": {
        "kind": "family",
        "path": "Organizações de Formação/Escolas da Aviação Civil",
        "family": "escolas",
    },
    "organizacoes-de-formacao-escolas-da-aviacao-civil-examinadores": {
        "kind": "family",
        "path": "Organizações de Formação/Escolas da Aviação Civil",
        "family": "examinadores",
    },
    "organizacoes-de-formacao-lista-de-treinamento-de-tipo-lista-treinamento-tipo-inicial": {
        "kind": "family",
        "path": "Organizações de Formação/Lista de Treinamento de Tipo",
        "family": "lista-treinamento-tipo-inicial",
    },
    "organizacoes-de-formacao-lista-de-treinamento-de-tipo-lista-treinamento-tipo-periodico": {
        "kind": "family",
        "path": "Organizações de Formação/Lista de Treinamento de Tipo",
        "family": "lista-treinamento-tipo-periodico",
    },
    "organizacoes-de-formacao-simuladores-de-voo-com-qualificacao-anac-valida-simuladores": {
        "kind": "family",
        "path": "Organizações de Formação/Simuladores de Voo com Qualificação ANAC válida",
        "family": "simuladores",
    },
    "organizacoes-de-manutencao-oficinas-de-manutencao-oficinas-manutencao-estrutura-antiga-organizacoesdemanutencao": {
        "kind": "family",
        "path": "Organizações de Manutenção/Oficinas de Manutenção/Oficinas_Manutencao_Estrutura_Antiga",
        "family": "organizacoesdemanutencao",
    },
    "organizacoes-de-manutencao-oficinas-de-manutencao-oficinas-manutencao-estrutura-antiga-organizacoesdemanutencao-padroes": {
        "kind": "family",
        "path": "Organizações de Manutenção/Oficinas de Manutenção/Oficinas_Manutencao_Estrutura_Antiga",
        "family": "organizacoesdemanutencao-padroes",
    },
    "organizacoes-de-manutencao-oficinas-de-manutencao-oficinas-manutencao-estrutura-antiga-organizacoesdemanutencao-produtos": {
        "kind": "family",
        "path": "Organizações de Manutenção/Oficinas de Manutenção/Oficinas_Manutencao_Estrutura_Antiga",
        "family": "organizacoesdemanutencao-produtos",
    },
    "organizacoes-de-manutencao-oficinas-de-manutencao-oficinasmanutencao": {
        "kind": "family",
        "path": "Organizações de Manutenção/Oficinas de Manutenção",
        "family": "oficinasmanutencao",
    },
    "pessoal-da-aviacao-civil-certificadosmedicos-certificadosmedicos": {
        "kind": "family",
        "path": "Pessoal da Aviação Civil/CertificadosMedicos",
        "family": "certificadosmedicos",
    },
    "pessoal-da-aviacao-civil-certificadosmedicos-certificadosmedicosv2-pda-quantidade-de-certificados-medicos-aeronauticos-v2": {
        "kind": "family",
        "path": "Pessoal da Aviação Civil/CertificadosMedicos/CertificadosMedicosV2",
        "family": "pda-quantidade-de-certificados-medicos-aeronauticos-v2",
    },
    "pessoal-da-aviacao-civil-clinicas-e-medicos-credenciados-clinicas-e-medicos-credenciados": {
        "kind": "family",
        "path": "Pessoal da Aviação Civil/Clínicas e Médicos Credenciados",
        "family": "clinicas-e-medicos-credenciados",
    },
    "pessoal-da-aviacao-civil-clinicas-e-medicos-credenciados-clinicasmedicos": {
        "kind": "family",
        "path": "Pessoal da Aviação Civil/Clínicas e Médicos Credenciados",
        "family": "clinicasmedicos",
    },
    "pessoal-da-aviacao-civil-clinicasmedicos": {
        "kind": "family",
        "path": "Pessoal da Aviação Civil",
        "family": "clinicasmedicos",
    },
    "pessoal-da-aviacao-civil-indicadores-pel-indicadorespel": {
        "kind": "family",
        "path": "Pessoal da Aviação Civil/Indicadores PEL",
        "family": "indicadorespel",
    },
    "pessoal-da-aviacao-civil-licencas-emitidas-licencas-emitidas": {
        "kind": "family",
        "path": "Pessoal da Aviação Civil/Licencas Emitidas",
        "family": "licencas-emitidas",
    },
    "pessoal-da-aviacao-civil-profissionais-credenciados-profissionaiscredenciados": {
        "kind": "family",
        "path": "Pessoal da Aviação Civil/Profissionais Credenciados",
        "family": "profissionaiscredenciados",
    },
    "regulamentacao-agenda-regulatoria-agenda-regulatoria": {
        "kind": "family",
        "path": "regulamentacao/Agenda Regulatória",
        "family": "agenda-regulatoria",
    },
    "regulamentacao-atendimento-das-demandas-oriundas-dos-orgaos-de-controle-atendimento-das-demandas-oriundas-dos-rgos-de-controle-cgutcu": {
        "kind": "family",
        "path": "regulamentacao/Atendimento das demandas oriundas dos órgãos de controle",
        "family": "atendimento-das-demandas-oriundas-dos-rgos-de-controle-cgutcu",
    },
    "seguranca-operacional-eventossegurancaoperacional-fauna-fauna": {
        "kind": "family",
        "path": "Seguranca Operacional/EventosSegurancaOperacional/Fauna",
        "family": "fauna",
    },
    "seguranca-operacional-ocorrencia-v-ocorrencia-ampla": {
        "kind": "family",
        "path": "Seguranca Operacional/Ocorrencia",
        "family": "v-ocorrencia-ampla",
    },
    "seguranca-operacional-ocorrencias-de-dificuldades-em-servico-em-aeronaves-ocorrencias-de-dificuldades-em-servicos-em-aeronaves-historico": {
        "kind": "family",
        "path": "Seguranca Operacional/Ocorrências de Dificuldades em Serviço em Aeronaves",
        "family": "ocorrencias-de-dificuldades-em-servicos-em-aeronaves-historico",
    },
    "seguranca-operacional-ocorrencias-de-dificuldades-em-servico-em-aeronaves-ocorrncias-de-dificuldades-em-servios-em-aeronaves-v2": {
        "kind": "family",
        "path": "Seguranca Operacional/Ocorrências de Dificuldades em Serviço em Aeronaves",
        "family": "ocorrncias-de-dificuldades-em-servios-em-aeronaves-v2",
    },
    "seguranca-operacional-recomendacao-de-seguranca-recomendacao-seguranca": {
        "kind": "family",
        "path": "Seguranca Operacional/Recomendação de Segurança",
        "family": "recomendacao-seguranca",
    },
    "voos-e-operacoes-aereas-dados-do-consumidor-gov-dados-consumidor-estrutura-antiga-dadosdoconsumidor": {
        "kind": "family",
        "path": "Voos e operações aéreas/Dados do consumidor.gov/Dados_Consumidor_Estrutura_Antiga",
        "family": "dadosdoconsumidor",
    },
    "voos-e-operacoes-aereas-dados-do-consumidor-gov-dadosconsumidor": {
        "kind": "family",
        "path": "Voos e operações aéreas/Dados do consumidor.gov",
        "family": "dadosconsumidor",
    },
    "voos-e-operacoes-aereas-dados-estatisticos-do-transporte-aereo-dados-estatisticos": {
        "kind": "family",
        "path": "Voos e operações aéreas/Dados Estatísticos do Transporte Aéreo",
        "family": "dados-estatisticos",
    },
    "voos-e-operacoes-aereas-horas-voadas-de-aeronave-horas-voadas": {
        "kind": "family",
        "path": "Voos e operações aéreas/Horas Voadas de Aeronave",
        "family": "horas-voadas",
    },
    "voos-e-operacoes-aereas-monitoramento-slots--partitioned": {
        "kind": "partitioned",
        "path": "Voos e operações aéreas/Monitoramento Slots",
    },
    "voos-e-operacoes-aereas-percentuais-de-atrasos-e-cancelamentos--partitioned": {
        "kind": "partitioned",
        "path": "Voos e operações aéreas/Percentuais de atrasos e cancelamentos",
    },
    "voos-e-operacoes-aereas-registro-de-servicos-aereos--partitioned": {
        "kind": "partitioned",
        "path": "Voos e operações aéreas/Registro de serviços aéreos",
    },
    "voos-e-operacoes-aereas-slots-alocados--partitioned": {
        "kind": "partitioned",
        "path": "Voos e operações aéreas/Slots Alocados",
    },
    "voos-e-operacoes-aereas-voo-regular-ativo-vra--partitioned": {
        "kind": "partitioned",
        "path": "Voos e operações aéreas/Voo Regular Ativo (VRA)",
    },
}
