from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import hmac
import hashlib
import json
import requests

app = FastAPI(title="Ashgrove Mock Services")

# Sanal Veritabanı
fake_db = {
    "deals": {
        "HS-88214": {
            "id": "HS-88214",
            "dealstage": "new_lead",
            "lastmodifieddate": datetime.utcnow().isoformat(),
            "properties": {}
        },
        "HS-99999": {
            "id": "HS-99999",
            "dealstage": "positive",
            "lastmodifieddate": datetime.utcnow().isoformat(),
            "properties": {}
        }
    },
    "activities": []
}

class DealUpdate(BaseModel):
    dealstage: str
    ccs_finish_code: Optional[str] = None
    ccs_call_id: Optional[str] = None
    ccs_changed_by: str
    ccs_change_reason: str

class ActivityData(BaseModel):
    contact_id: Optional[str] = None
    call_id: str
    outcome: Optional[str] = None
    note: Optional[str] = None
    occurred_at: str

class EventSimulator(BaseModel):
    webhook_url: str
    payload: dict

@app.get("/")
def read_root():
    return {"status": "Ashgrove Mock API çalışıyor, tüm endpointler aktif!"}

# 0. CRM Mock: Contact Bilgisini Getirme[cite: 1]
@app.get("/crm/v3/objects/contacts/{contact_id}")
def get_contact(contact_id: str):
    return {
        "id": contact_id,
        "properties": {
            "firstname": "Jane",
            "lastname": "Doe",
            "clinic_location": "Headingley"
        }
    }

# 1. CRM Mock: Deal Bilgisini Getirme[cite: 1]
@app.get("/crm/v3/objects/deals/{deal_id}")
def get_deal(deal_id: str):
    if deal_id not in fake_db["deals"]:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı")
    return fake_db["deals"][deal_id]

# 2. CRM Mock: Deal Aşamasını Güncelleme (409 Çakışma Yönetimli)[cite: 1]
@app.patch("/crm/v3/objects/deals/{deal_id}")
def update_deal(deal_id: str, deal_update: DealUpdate):
    if deal_id not in fake_db["deals"]:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı")
    
    # 409 Conflict simülasyonu: Sadece new_lead aşamasındaki kayıtlar değiştirilebilir[cite: 1]
    if fake_db["deals"][deal_id]["dealstage"] != "new_lead":
        raise HTTPException(status_code=409, detail="Kayıt siz okuduktan sonra değişmiş (Conflict)")
        
    fake_db["deals"][deal_id]["dealstage"] = deal_update.dealstage
    fake_db["deals"][deal_id]["lastmodifieddate"] = datetime.utcnow().isoformat()
    
    # Denetim şartı (Audit): ccs_changed_by ve ccs_change_reason[cite: 1]
    fake_db["deals"][deal_id]["properties"]["ccs_changed_by"] = deal_update.ccs_changed_by
    fake_db["deals"][deal_id]["properties"]["ccs_change_reason"] = deal_update.ccs_change_reason
    
    return fake_db["deals"][deal_id]

# 3. CRM Mock: Activity (Çağrı/Not) Ekleme[cite: 1]
@app.post("/crm/v3/objects/activities")
def create_activity(activity: ActivityData):
    fake_db["activities"].append(activity.dict())
    return {"status": "success", "activity": activity}

# 4. Kampanya Listesi[cite: 1]
@app.get("/campaign/next-list")
def get_campaign_list(date: str, suppression: str = "off"):
    # Sadece dealstage = new_lead olan kayıtları döndürür[cite: 1]
    results = [deal for deal in fake_db["deals"].values() if deal["dealstage"] == "new_lead"]
    return {"date": date, "suppression": suppression, "total_leads": len(results), "leads": results}

# 5. Olay Yayıcı - Manuel Tetikleme Ucu (HMAC-SHA256 İmzalı)[cite: 1]
SECRET_KEY = b"ashgrove-secret-2026"

@app.post("/simulate-event")
def simulate_event(event: EventSimulator):
    payload_bytes = json.dumps(event.payload, separators=(',', ':')).encode('utf-8')
    signature = hmac.new(SECRET_KEY, payload_bytes, hashlib.sha256).hexdigest()
    
    headers = {
        "Content-Type": "application/json",
        "X-CCS-Signature": signature
    }
    
    try:
        response = requests.post(event.webhook_url, json=event.payload, headers=headers)
        return {"status": "sent", "webhook_response_code": response.status_code}
    except Exception as e:
        return {"status": "failed", "error": str(e)}