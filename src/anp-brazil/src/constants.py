# Auto-generated: the rank-accepted entity union and, per entity, the ANP
# dados-abertos category landing slug plus the normalized file-pattern set
# that identifies its CSV/ZIP partitions. Download re-scrapes the category
# page and selects files whose normalized pattern is in this set (robust to
# year-suffix roll-forward). Patterns mirror collect grouping exactly.

ENTITY_MAP = {
    "ppgn-el-producao-petroleo-m3": {"slug": "producao-de-petroleo-e-gas-natural-por-estado-e-localizacao", "patterns": ["ppgn-el/producao-petroleo-m3", "ppgn-el/producao-gas-natural-1000m3"]},
    "ppgn-el-producao-lgn-m3": {"slug": "producao-de-petroleo-e-gas-natural-por-estado-e-localizacao", "patterns": ["ppgn-el/producao-lgn-m3"]},
    "ppgn-el-queima-e-perda-gn-1000m3": {"slug": "producao-de-petroleo-e-gas-natural-por-estado-e-localizacao", "patterns": ["ppgn-el/queima-e-perda-gn-1000m3"]},
    "ppgn-el-consumo-proprio-gn1000m3": {"slug": "producao-de-petroleo-e-gas-natural-por-estado-e-localizacao", "patterns": ["ppgn-el/consumo-proprio-gn1000m3"]},
    "ppgn-el-gn-disponivel-1000m3": {"slug": "producao-de-petroleo-e-gas-natural-por-estado-e-localizacao", "patterns": ["ppgn-el/gn-disponivel-1000m3"]},
    "arquivos-producao-de-biocombustiveis-producao-biodiesel-m3": {"slug": "producao-de-biocombustiveis", "patterns": ["arquivos-producao-de-biocombustiveis/producao-biodiesel-m3"]},
    "arquivos-producao-de-biocombustiveis-producao-etanol-anidro-hidratado-m3": {"slug": "producao-de-biocombustiveis", "patterns": ["arquivos-producao-de-biocombustiveis/producao-etanol-anidro-hidratado-m3"]},
    "vdpb-vendas-derivados-petroleo-e-etanol-vendas-combustiveis-m3": {"slug": "vendas-de-derivados-de-petroleo-e-biocombustiveis", "patterns": ["vdpb/vendas-derivados-petroleo-e-etanol/vendas-combustiveis-m3", "vdpb/vct/vendas-oleo-diesel-tipo-m3"]},
    "vdpb-vcs-vendas-combustiveis-segmento-m3": {"slug": "vendas-de-derivados-de-petroleo-e-biocombustiveis", "patterns": ["vdpb/vcs/vendas-combustiveis-segmento-m3"]},
    "vdpb-vct-vendas-glp-tipo-vasilhame-m3": {"slug": "vendas-de-derivados-de-petroleo-e-biocombustiveis", "patterns": ["vdpb/vct/vendas-glp-tipo-vasilhame-m3"]},
    "vdpb-vendas-por-produtor-vendas-oleo-diesel-produtores-m3": {"slug": "vendas-de-derivados-de-petroleo-e-biocombustiveis", "patterns": ["vdpb/vendas-por-produtor/vendas-oleo-diesel-produtores-m3"]},
    "vdpb-vendas-de-biodiesel-vendas-biodiesel-b100-m3": {"slug": "vendas-de-derivados-de-petroleo-e-biocombustiveis", "patterns": ["vdpb/vendas-de-biodiesel/vendas-biodiesel-b100-m3"]},
    "vdpb-vaehdpm-asfalto-vendas-anuais-de-asfalto-por-municipio": {"slug": "vendas-de-derivados-de-petroleo-e-biocombustiveis", "patterns": ["vdpb/vaehdpm/asfalto/vendas-anuais-de-asfalto-por-municipio", "vdpb/vaehdpm/etanol-hidratado/vendas-anuais-de-etanol-hidratado-por-municipio", "vdpb/vaehdpm/gasolina-c/vendas-anuais-de-gasolina-c-por-municipio", "vdpb/vaehdpm/gasolina-de-aviacao/vendas-anuais-de-gasolina-de-aviacao-por-municipio", "vdpb/vaehdpm/oleo-diesel/vendas-anuais-de-oleo-diesel-por-municipio", "vdpb/vaehdpm/querosene-de-aviacao/vendas-anuais-de-querosene-de-aviacao-por-municipio", "vdpb/vaehdpm/querosene-iluminante/vendas-anuais-de-querosene-iluminante-por-municipio"]},
    "vdpb-vaehdpm-glp-vendas-anuais-de-glp-por-municipio": {"slug": "vendas-de-derivados-de-petroleo-e-biocombustiveis", "patterns": ["vdpb/vaehdpm/glp/vendas-anuais-de-glp-por-municipio"]},
    "vdpb-vaehdpm-oleo-combustivel-vendas-anuais-de-oleo-combustivel-por-municipio": {"slug": "vendas-de-derivados-de-petroleo-e-biocombustiveis", "patterns": ["vdpb/vaehdpm/oleo-combustivel/vendas-anuais-de-oleo-combustivel-por-municipio"]},
    "arquivos-vendas-anuais-de-etanol-hidratado-e-derivados-de-petroleo-por-estado-ve": {"slug": "vendas-de-derivados-de-petroleo-e-biocombustiveis", "patterns": ["arquivos-vendas-anuais-de-etanol-hidratado-e-derivados-de-petroleo-por-estado/vendas-etanol-hidratado-por-estado", "arquivos-vendas-anuais-de-etanol-hidratado-e-derivados-de-petroleo-por-estado/vendas-gasolina-c-por-estado", "arquivos-vendas-anuais-de-etanol-hidratado-e-derivados-de-petroleo-por-estado/vendas-gasolina-aviacao-por-estado", "arquivos-vendas-anuais-de-etanol-hidratado-e-derivados-de-petroleo-por-estado/vendas-glp-por-estado", "arquivos-vendas-anuais-de-etanol-hidratado-e-derivados-de-petroleo-por-estado/vendas-oleo-combustivel-por-estado", "arquivos-vendas-anuais-de-etanol-hidratado-e-derivados-de-petroleo-por-estado/vendas-oleo-diesel-por-estado", "arquivos-vendas-anuais-de-etanol-hidratado-e-derivados-de-petroleo-por-estado/vendas-querosene-aviacao-por-estado", "arquivos-vendas-anuais-de-etanol-hidratado-e-derivados-de-petroleo-por-estado/vendas-querosene-iluminante-por-estado"]},
    "ie-petroleo-importacoes-exportacoes-petroleo": {"slug": "importacoes-e-exportacoes", "patterns": ["ie/petroleo/importacoes-exportacoes-petroleo", "ie/etanol/importacoes-exportacoes-etanol"]},
    "ie-gn-importacao-gas-natural": {"slug": "importacoes-e-exportacoes", "patterns": ["ie/gn/importacao-gas-natural"]},
    "ie-derivados-importacoes-exportacoes-derivados": {"slug": "importacoes-e-exportacoes", "patterns": ["ie/derivados/importacoes-exportacoes-derivados"]},
    "mdpg-asfalto": {"slug": "dados-abertos-movimentacao-de-derivados-de-petroleo", "patterns": ["mdpg/asfalto"]},
    "mdpg-aviacao": {"slug": "dados-abertos-movimentacao-de-derivados-de-petroleo", "patterns": ["mdpg/aviacao"]},
    "mdpg-liquidos": {"slug": "dados-abertos-movimentacao-de-derivados-de-petroleo", "patterns": ["mdpg/liquidos"]},
    "mdpg-glp": {"slug": "dados-abertos-movimentacao-de-derivados-de-petroleo", "patterns": ["mdpg/glp"]},
    "mdpg-lubrificante": {"slug": "dados-abertos-movimentacao-de-derivados-de-petroleo", "patterns": ["mdpg/lubrificante"]},
    "mdpg-solvente": {"slug": "dados-abertos-movimentacao-de-derivados-de-petroleo", "patterns": ["mdpg/solvente"]},
    "mdpg-trr": {"slug": "dados-abertos-movimentacao-de-derivados-de-petroleo", "patterns": ["mdpg/trr"]},
    "mdpg-fornecedores-vendas-diretas": {"slug": "dados-abertos-movimentacao-de-derivados-de-petroleo", "patterns": ["mdpg/fornecedores-vendas-diretas"]},
    "mdpg-movimentacaologistica": {"slug": "dados-abertos-movimentacao-de-derivados-de-petroleo", "patterns": ["mdpg/movimentacaologistica"]},
    "shpc-dsas-ca-ca": {"slug": "serie-historica-de-precos-de-combustiveis", "patterns": ["shpc/dsas/ca/ca", "shpc/dsas/ca/precos-semestrais-ca", "shpc/dsas/glp/glp", "shpc/dsas/glp/precos-semestrais-glp", "shpc/dsan/dados-abertos-precos-diesel-gnv", "shpc/dsan/precos-diesel-gnv", "shpc/dsan/dados-abertos-precos-gasolina-etanol", "shpc/dsan/cados-abertos-preco-gasolina-etanol", "shpc/dsan/precos-gasolina-etanol", "shpc/dsan/dados-abertos-precos-glp", "shpc/dsan/precos-glp", "shpc/qus/ultimas-4-semanas-diesel-gnv", "shpc/qus/ultimas-4-semanas-gasolina-etanol", "shpc/qus/ultimas-4-semanas-glp"]},
}

ENTITY_IDS = list(ENTITY_MAP.keys())
