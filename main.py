import csv, io, os, re
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

app = FastAPI(title="AgentData API", version="0.1.0", description="Demo gratuita de validação e conversão de dados brasileiros")
class ValueInput(BaseModel):
    value: str = Field(max_length=256)
class CsvInput(BaseModel):
    csv_text: str = Field(max_length=100000)
    delimiter: str = Field(default=",", min_length=1, max_length=1)
def digits(s): return re.sub(r"\D", "", s)
def check_cpf(value):
    d=digits(value)
    if len(d)!=11 or len(set(d))==1: return False
    for length in (9,10):
        k=(sum(int(d[i])*(length+1-i) for i in range(length))*10)%11
        if (0 if k==10 else k)!=int(d[length]): return False
    return True
def check_cnpj(value):
    d=digits(value)
    if len(d)!=14 or len(set(d))==1: return False
    for length,weights in ((12,[5,4,3,2,9,8,7,6,5,4,3,2]),(13,[6,5,4,3,2,9,8,7,6,5,4,3,2])):
        rem=sum(int(x)*w for x,w in zip(d[:length],weights))%11
        if (0 if rem<2 else 11-rem)!=int(d[length]): return False
    return True
@app.get("/",include_in_schema=False)
def demo(): return FileResponse(Path(__file__).with_name("demo.html"))
@app.get("/health")
def health(): return {"status":"ok","mode":os.getenv("MODE","demo")}
@app.get("/catalog")
def catalog(): return {"name":"AgentData API","payment_status":"demo_only","price_target_usd_per_call":"0.005","endpoints":["POST /validate/cpf","POST /validate/cnpj","POST /normalize/phone","POST /convert/csv-json"]}
@app.post("/validate/cpf")
def cpf(data:ValueInput): return {"valid":check_cpf(data.value),"type":"CPF","digits":digits(data.value)}
@app.post("/validate/cnpj")
def cnpj(data:ValueInput): return {"valid":check_cnpj(data.value),"type":"CNPJ","digits":digits(data.value)}
@app.post("/normalize/phone")
def phone(data:ValueInput):
    d=digits(data.value)
    if d.startswith("55") and len(d) in (12,13): d=d[2:]
    if len(d) not in (10,11) or d[:2]=="00": return {"valid_format":False,"e164":None}
    return {"valid_format":True,"e164":"+55"+d}
@app.post("/convert/csv-json")
def csv_json(data:CsvInput):
    try:
        reader=csv.DictReader(io.StringIO(data.csv_text),delimiter=data.delimiter)
        if not reader.fieldnames or len(reader.fieldnames)>100: raise ValueError("Invalid headers")
        rows=[]
        for row in reader:
            if len(rows)>=1000: raise ValueError("Maximum 1000 rows")
            rows.append(row)
        return {"rows":rows,"count":len(rows)}
    except (csv.Error,ValueError) as e: raise HTTPException(status_code=400,detail=str(e))
