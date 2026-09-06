from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import hmac
import hashlib
import json
import requests

app = FastAPI(title="Ashgrove Mock Services")

# Sanal Veritabanı (50 Kayıtlı Test Havuzu)
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
        },
        "HS-1001": {"id": "HS-1001", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1002": {"id": "HS-1002", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1003": {"id": "HS-1003", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1004": {"id": "HS-1004", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1005": {"id": "HS-1005", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1006": {"id": "HS-1006", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1007": {"id": "HS-1007", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1008": {"id": "HS-1008", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1009": {"id": "HS-1009", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1010": {"id": "HS-1010", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1011": {"id": "HS-1011", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1012": {"id": "HS-1012", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1013": {"id": "HS-1013", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1014": {"id": "HS-1014", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1015": {"id": "HS-1015", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1016": {"id": "HS-1016", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1017": {"id": "HS-1017", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1018": {"id": "HS-1018", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1019": {"id": "HS-1019", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1020": {"id": "HS-1020", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1021": {"id": "HS-1021", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1022": {"id": "HS-1022", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1023": {"id": "HS-1023", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1024": {"id": "HS-1024", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1025": {"id": "HS-1025", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1026": {"id": "HS-1026", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1027": {"id": "HS-1027", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1028": {"id": "HS-1028", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1029": {"id": "HS-1029", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1030": {"id": "HS-1030", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1031": {"id": "HS-1031", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1032": {"id": "HS-1032", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1033": {"id": "HS-1033", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1034": {"id": "HS-1034", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1035": {"id": "HS-1035", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1036": {"id": "HS-1036", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1037": {"id": "HS-1037", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1038": {"id": "HS-1038", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1039": {"id": "HS-1039", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1040": {"id": "HS-1040", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1041": {"id": "HS-1041", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1042": {"id": "HS-1042", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1043": {"id": "HS-1043", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1044": {"id": "HS-1044", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1045": {"id": "HS-1045", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1046": {"id": "HS-1046", "dealstage": "new_lead", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1047": {"id": "HS-1047", "dealstage": "positive", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}},
        "HS-1048": {"id": "HS-1048", "dealstage": "positive", "lastmodifieddate": datetime.utcnow().isoformat(), "properties": {}}
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
    return {"status": "Ashgrove Mock Services çalışıyor, tüm endpointler aktif!"}

# 0. CRM Mock: Contact Bilgisini Getirme
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

# 1. CRM Mock: Deal Bilgisini Getirme
@app.get("/crm/v3/objects/deals/{deal_id}")
def get_deal(deal_id: str):
    if deal_id not in fake_db["deals"]:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı")
    return fake_db["deals"][deal_id]

# 2. CRM Mock: Deal Aşamasını Güncelleme (409 Çakışma Yönetimli)
@app.patch("/crm/v3/objects/deals/{deal_id}")
def update_deal(deal_id: str, deal_update: DealUpdate):
    if deal_id not in fake_db["deals"]:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı")
    
    # 409 Conflict simülasyonu: Sadece new_lead aşamasındaki kayıtlar değiştirilebilir
    if fake_db["deals"][deal_id]["dealstage"] != "new_lead":
        raise HTTPException(status_code=409, detail="Kayıt siz okuduktan sonra değişmiş (Conflict)")
        
    fake_db["deals"][deal_id]["dealstage"] = deal_update.dealstage
    fake_db["deals"][deal_id]["lastmodifieddate"] = datetime.utcnow().isoformat()
    
    # Denetim şartı (Audit): ccs_changed_by ve ccs_change_reason
    fake_db["deals"][deal_id]["properties"]["ccs_changed_by"] = deal_update.ccs_changed_by
    fake_db["deals"][deal_id]["properties"]["ccs_change_reason"] = deal_update.ccs_change_reason
    
    return fake_db["deals"][deal_id]

# 3. CRM Mock: Activity (Çağrı/Not) Ekleme
@app.post("/crm/v3/objects/activities")
def create_activity(activity: ActivityData):
    fake_db["activities"].append(activity.dict())
    return {"status": "success", "activity": activity}

# 4. Kampanya Listesi (Güncellenmiş Kapsam Versiyonu)
@app.get("/campaign/next-list")
def get_campaign_list(
    date: str = Query(..., description="Ertesi günün tarihi (YYYY-MM-DD)"),
    suppression: str = Query("on", description="Bastırma kuralı: 'on' veya 'off'")
):
    """
    Kampanya Listesi (Dialer'ın ertesi gün arayacağı hastalar)
    Demoda randevusu alınan hastanın listeden çıkıp çıkmadığı buradan kanıtlanacak.
    """
    campaign_list = []
    
    for deal_id, deal in fake_db["deals"].items():
        # Bastırma (Suppression) AÇIK: Sadece "new_lead" olanlar listeye girer.
        if suppression == "on":
            if deal.get("dealstage") == "new_lead":
                campaign_list.append(deal)
        
        # Bastırma KAPALI: Sistemin bozuk/eski halini göstermek için.
        elif suppression == "off":
            campaign_list.append(deal)

    # Yükleme / Değiştirilme tarihine göre sıralama
    campaign_list.sort(key=lambda x: x.get("lastmodifieddate", ""))
    
    return {
        "target_date": date,
        "suppression": suppression,
        "total_patients": len(campaign_list),
        "patients": campaign_list
    }

# 5. Olay Yayıcı - Manuel Tetikleme Ucu (HMAC-SHA256 İmzalı)
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


from fastapi.responses import HTMLResponse

@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    total_deals = len(fake_db["deals"])
    new_leads = sum(1 for d in fake_db["deals"].values() if d["dealstage"] == "new_lead")
    resolved_deals = total_deals - new_leads
    total_activities = len(fake_db["activities"])
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ashgrove CRM & Audit Monitor</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9; }}
            .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }}
            h1 {{ color: #2c3e50; }}
            .metric {{ font-size: 24px; font-weight: bold; color: #27ae60; }}
            .warning {{ color: #e74c3c; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #34495e; color: white; }}
        </style>
    </head>
    <body>
        <h1>Ashgrove Operasyonel İzleme Ekranı</h1>
        <div class="card">
            <h3>Sistem Özeti</h3>
            <p>Toplam İnceleme Altındaki Kayıt: <b>{total_deals}</b></p>
            <p>Askıda / Riskli Kayıt (New Lead): <span class="metric warning">{new_leads}</span></p>
            <p>Çözümlenmiş / Taşınmış Kayıt: <span class="metric">{resolved_deals}</span></p>
            <p>İşlenen Çağrı / Aktivite Sayısı: <b>{total_activities}</b></p>
        </div>
        <div class="card">
            <h3>Canlı CRM Kayıt Durumları</h3>
            <table>
                <tr><th>Deal ID</th><th>Mevcut Aşama (Deal Stage)</th><th>Son Güncelleme</th></tr>
                {"".join([f"<tr><td>{d['id']}</td><td>{d['dealstage']}</td><td>{d['lastmodifieddate']}</td></tr>" for d in fake_db["deals"].values()])}
            </table>
        </div>
    </body>
    </html>
    """
    return html_content