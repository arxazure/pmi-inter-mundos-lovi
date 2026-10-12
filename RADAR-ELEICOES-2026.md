# Radar Eleições 2026 — operação e limites
- Três agendamentos no GitHub Actions, 08:05, 13:05 e 19:05 (Brasília, UTC-3) em condições normais. GitHub não garante pontualidade e pode desativar cron em repositórios sem atividade.
- Consulta RSS público do TSE e **só publica se houver matéria nova** (sem duplicar conteúdo).
- Notícias automáticas são notas de referência, com título da fonte, data, URL, perguntas de fiscalização e ressalvas; não constituem análises de mérito.
- Fontes precisam ser acessíveis via API. A rota `https://www.tse.jus.br/rss` foi localizada como RSS XML, mas a funcionalidade fim-a-fim **ainda não foi testada** na execução do workflow.
- O workflow gera `radar-eleicoes-2026.html` e artigos `radar-eleicoes-2026/*.html`; sincronização na Hostinger precisa de verificação independente.
- Links internos e `sitemap.xml` são atualizados; envio ao Google Search Console/Bing depende de autenticação dos proprietários.
- `llms.txt` facilita leitura de alguns agentes, sem garantir indexação por IA.
- Para acrescentar análises aprofundadas: ler integralmente documentos, atribuir fatos e cifras com fontes, separar hipóteses e controvérsias, exigir revisão humana.
