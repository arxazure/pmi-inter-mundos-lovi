"""Coleta dados autenticos do Google Search Console sem dados ficticios.
Requer GSC_PROPERTY e GSC_SERVICE_ACCOUNT_JSON em GitHub Actions secrets.
"""
import datetime as dt
import json
import os
from pathlib import Path
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

property_uri=os.environ["GSC_PROPERTY"].strip()
service_info=json.loads(os.environ["GSC_SERVICE_ACCOUNT_JSON"])
credentials=service_account.Credentials.from_service_account_info(service_info,scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
session=AuthorizedSession(credentials)
end=dt.date.today()-dt.timedelta(days=3)
start=end-dt.timedelta(days=27)
url="https://searchconsole.googleapis.com/webmasters/v3/sites/"+__import__("urllib.parse",fromlist=["quote"]).quote(property_uri,safe="")+"/searchAnalytics/query"
def fetch(dimension):
    result=[]
    for offset in range(0,5000,1000):
        body={"startDate":str(start),"endDate":str(end),"dimensions":[dimension],"rowLimit":1000,"startRow":offset,"dataState":"final"}
        response=session.post(url,json=body,timeout=60)
        response.raise_for_status()
        rows=response.json().get("rows",[])
        for r in rows:
            result.append({dimension:r["keys"][0],"clicks":r["clicks"],"impressions":r["impressions"],"ctr":r["ctr"],"position":r["position"]})
        if len(rows)<1000:break
    return result
queries=fetch("query")
pages=fetch("page")
# Totais da propriedade solicitados sem dimensions, evitando somar linhas parciais.
response=session.post(url,json={"startDate":str(start),"endDate":str(end),"rowLimit":1,"dataState":"final"},timeout=60)
response.raise_for_status()
totals=(response.json().get("rows") or [{}])[0]
def val(key):return totals.get(key,0)
data={"connected":True,"property":property_uri,"period":{"start":str(start),"end":str(end)},"generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),"totals":{"clicks":val("clicks"),"impressions":val("impressions"),"ctr":val("ctr"),"position":val("position")},"queries":queries,"pages":pages,"indexation":"A API Search Analytics mede desempenho, não fornece inventário completo de indexação. Use a inspeção de URL autorizada no Search Console."}
Path("data").mkdir(exist_ok=True)
Path("data/search-console.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"Coleta concluida: {len(queries)} consultas, {len(pages)} paginas, propriedade {property_uri}")
