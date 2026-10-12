#!/usr/bin/env python3
"""Gera 1 boletim por rodada a partir de feed oficial do TSE.
Nunca inventa noticia ou afirma fatos fora do feed; falha fechada sem fonte.
Tres rodadas diarias sao configuradas em GitHub Actions.
"""
from datetime import datetime,timezone,timedelta
from email.utils import parsedate_to_datetime
from html import escape,unescape
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlparse
import hashlib,json,re,xml.etree.ElementTree as ET

BASE="https://salmon-quail-451428.hostingersite.com"
FEED="https://www.tse.jus.br/rss"
TZ=timezone(timedelta(hours=-3))
now=datetime.now(TZ)
folder=Path("radar-eleicoes-2026")
folder.mkdir(exist_ok=True)
items=[]
try:
 request=Request(FEED,headers={"User-Agent":"PMI31Radar/1.0 (+https://github.com/arxazure/pmi-inter-mundos-lovi)"})
 with urlopen(request,timeout=25) as res: data=res.read(2_000_000)
 root=ET.fromstring(data)
 for entry in root.findall(".//item"):
  title=" ".join((entry.findtext("title") or "").split())
  link=(entry.findtext("link") or "").strip()
  date=(entry.findtext("pubDate") or "").strip()
  if not title or not link or urlparse(link).hostname not in {"www.tse.jus.br","tse.jus.br"}:continue
  try:published=parsedate_to_datetime(date).astimezone(TZ)
  except (ValueError,TypeError):continue
  if now-published>timedelta(days=12) or published>now+timedelta(hours=1):continue
  items.append({"title":title,"link":link,"date":published.isoformat()})
except Exception as exc:
 print("Falha na fonte oficial; nao publicar conteudo nao verificado:",type(exc).__name__,str(exc)[:130])
 raise SystemExit(0)
historyfile=folder/"historico.json"
history=json.loads(historyfile.read_text(encoding="utf-8")) if historyfile.exists() else []
seen={x["link"] for x in history}
available=[x for x in items if x["link"] not in seen]
if not available:
 print("Sem nova materia no feed oficial. Nenhuma publicacao artificial.")
 raise SystemExit(0)
item=available[0]
slot="manha" if now.hour<11 else "tarde" if now.hour<17 else "noite"
stamp=now.strftime("%Y-%m-%d")
slug=f"{stamp}-{slot}-{hashlib.sha256(item['link'].encode()).hexdigest()[:9]}"
destination=folder/(slug+".html")
article=f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Radar Eleições 2026 | {escape(item['title'])} | PMI31</title><meta name="description" content="Radar Eleições 2026: curadoria documentada de publicações oficiais, implicações para o cidadão e perguntas de controle social."><link rel="canonical" href="{BASE}/radar-eleicoes-2026/{slug}.html"><link rel="stylesheet" href="../style.css"></head><body><header><a class="logo" href="../index.html">PMI31<small>PROPOSTA INTER MUNDOS</small></a><nav><a href="../radar-eleicoes-2026.html">Radar Eleições 2026</a><a href="../politicas-propostas.html">Propostas</a></nav></header><main><section class="green"><h1>{escape(item['title'])}</h1><p>Radar Eleições 2026 · {now.strftime('%d/%m/%Y %H:%M')} (Brasília) · Fonte: TSE</p></section><section><h2>O que foi publicado</h2><p>O Tribunal Superior Eleitoral publicou uma notícia com o título acima, em {escape(item['date'][:10])}. Esta nota registra a existência da publicação original; para verificar fatos, contexto, eventuais decisões e documentos citados, consulte diretamente a íntegra.</p><p><a href="{escape(item['link'],quote=True)}" target="_blank" rel="noopener noreferrer">Ler notícia integral na fonte oficial (TSE)</a></p><h2>Perguntas para uma análise independente</h2><p>Qual problema público está em discussão? Quais cidadãos são afetados? Qual é a regra aplicável e o órgão competente? Existem números, documentos e mecanismos para fiscalizar resultados? Quais argumentos e limitações precisam ser considerados?</p><p><strong>Transparência editorial:</strong> esta nota foi criada automaticamente a partir de um título e link de fonte institucional. Não é investigação independente, não verifica acusações e não traz juízo favorável ou contrário a candidatos ou partidos. Uma análise aprofundada depende de leitura e conferência humana das fontes.</p><p><a href="../pedido-plebiscito-gpc.html">Conheça o pedido de consulta popular e seus limites legais</a></p></section></main><footer>PMI31 — Proposta Inter Mundos · Comunidade cívica sem filiação partidária.</footer></body></html>"""
destination.write_text(article,encoding="utf-8")
history.insert(0,{**item,"file":destination.name,"created_at":now.isoformat()})
history=history[:300]
historyfile.write_text(json.dumps(history,ensure_ascii=False,indent=2),encoding="utf-8")
cards="".join(f'<article class="card"><h3><a href="radar-eleicoes-2026/{escape(x["file"],quote=True)}">{escape(x["title"])}</a></h3><p>Publicado no radar: {escape(x["created_at"][:10])} · Fonte: TSE · <a href="{escape(x["link"],quote=True)}" rel="noopener" target="_blank">Fonte primária</a></p></article>' for x in history[:40])
index=f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Radar Eleições 2026 — Notícias e consultas públicas | PMI31</title><meta name="description" content="Radar Eleições 2026: curadoria diária de fontes oficiais e perguntas de fiscalização pública, sem apoio partidário."><link rel="canonical" href="{BASE}/radar-eleicoes-2026.html"><link rel="stylesheet" href="style.css"></head><body><header><a class="logo" href="index.html">PMI31<small>PROPOSTA INTER MUNDOS</small></a><nav><a href="index.html">Início</a><a href="radar-pmi31.html">Desempenho nas buscas</a><a href="politicas-propostas.html">Propostas</a></nav></header><main><section class="green"><h1>Radar Eleições 2026</h1><p class="statement">Atualizações de fontes institucionais, perguntas de fiscalização e propostas públicas: sem preferência partidária.</p><p>O coletor procura publicar até três notas de fonte oficial por dia, apenas quando encontra links novos e válidos. Notícias individuais são curadoria automática de títulos, não análises factuais independentes.</p></section><section><h2>Atualizações do radar</h2>{cards}</section></main><footer>PMI31 — Proposta Inter Mundos · Informativo, sem candidatura nem filiação.</footer></body></html>'''
Path("radar-eleicoes-2026.html").write_text(index,encoding="utf-8")
sitemap=Path("sitemap.xml")
if sitemap.exists():
 content=sitemap.read_text(encoding="utf-8")
 for url in [f"{BASE}/radar-eleicoes-2026.html", f"{BASE}/radar-eleicoes-2026/{slug}.html"]:
  entry=f"<url><loc>{url}</loc></url>"
  if entry not in content:content=content.replace("</urlset>",entry+"\n</urlset>")
 sitemap.write_text(content,encoding="utf-8")
print("Nota oficial publicada:",destination)
