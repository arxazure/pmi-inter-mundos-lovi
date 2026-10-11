# PMI | Protocolo de auditoria documental — versão 1.0

## Fonte primária obrigatória
TSE, planos de governo para a eleição presidencial de 2026, 2º turno: https://www.tse.jus.br/eleicoes/eleicoes-2026-content/propostas-de-governo-dos-candidatos-ao-cargo-de-presidente-da-republica-eleicoes-2026-segundo-turno

## Regras
1. Não atribuir ao plano declarações que não constem do documento original.
2. Para cada item, anotar ID único, candidatura, documento, data de acesso, página, seção, texto transcrito curto, link e hash SHA-256 do PDF quando coletado.
3. Registrar separadamente: **texto do plano**, **declaração da campanha**, **notícia sobre proposta**, **situação normativa** e **resultado observado**.
4. Verificar objetivos, mecanismos, prazos, estimativas de custo, fonte de financiamento, indicadores e competência institucional. Quando inexistentes, registrar **não informado no trecho verificado**, sem inferência.
5. Aplicar perguntas idênticas às candidaturas e evitar pontuação ou ranking.
6. Distinguir fato comprovado, hipótese, cenário, controvérsia e ausência de evidência. Consultar IBGE, Ipea, Tesouro, Banco Central, Inep, Datasus e outras fontes pertinentes com data de referência.
7. Não publicar conclusão substantiva sem revisão humana e trilha de evidências.
8. Corrigir publicamente erros com histórico, data e justificativa.

## Esquema de ficha
`id, candidatura, categoria, documento, url_fonte, pagina, trecho, data_acesso, enunciado_neutro, custo_declarado, prazo_declarado, mecanismo, fontes_secundarias, pontos_nao_especificados, limitacoes, revisor, data_revisao, status`.

## Status permitidos
`fonte-localizada`, `extraido`, `em-conferencia`, `revisado`, `publicado`, `retificado`.

## Divulgação
A ficha é sobre a **proposta documentada**, e não sobre a qualidade geral ou intenção de voto. Avisar quando a fonte for anterior ou posterior ao plano registrado.
