"""
JURA ENA 4 Deal Hunter
Searches for the best price across retailers and sends a Gmail alert when a deal is found.
"""

import os
import json
import base64
import anthropic
from datetime import datetime
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

PRODUCT_NAME   = "JURA ENA 4 Fully Automatic Espresso Machine Nordic White"
BASELINE_PRICE = 1199.95
BASELINE_STORE = "Williams-Sonoma"
ALERT_THRESHOLD_PCT = 5
RECIPIENT_EMAIL = "sebalopez13@gmail.com"

RETAILERS = [
    "Amazon", "Williams-Sonoma", "Best Buy",
    "Whole Latte Love", "Costco", "shopjura.com", "Target",
]

def search_for_deals():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    retailer_list = "\n".join(f"- {r}" for r in RETAILERS)
    prompt = f"""Search for the current price of the {PRODUCT_NAME} at each of these retailers:\n\n{retailer_list}\n\nReturn a JSON array only. Each element must have:\n- "retailer": string\n- "price": number or null\n- "url": string or null\n- "in_stock": boolean\n- "notes": string"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}],
    )
    raw = "".join(b.text for b in response.content if b.type == "text").strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip().rstrip("```").strip())

def find_best_deal(results):
    available = [r for r in results if r.get("price") and r.get("in_stock", True)]
    if not available:
        return None
    best = min(available, key=lambda r: r["price"])
    savings = BASELINE_PRICE - best["price"]
    savings_pct = (savings / BASELINE_PRICE) * 100
    if savings_pct >= ALERT_THRESHOLD_PCT:
        best["savings"] = round(savings, 2)
        best["savings_pct"] = round(savings_pct, 1)
        return best
    return None

def get_gmail_service():
    creds = Credentials(
        token=os.environ["GMAIL_ACCESS_TOKEN"],
        refresh_token=os.environ["GMAIL_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["GMAIL_CLIENT_ID"],
        client_secret=os.environ["GMAIL_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/gmail.send"],
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("gmail", "v1", credentials=creds)

def send_deal_alert(deal, all_results):
    today = datetime.now().strftime("%B %d, %Y")
    price_lines = []
    for r in sorted(all_results, key=lambda x: x.get("price") or 9999):
        if r.get("price"):
            marker = " <- BEST DEAL" if r["retailer"] == deal["retailer"] else ""
            price_lines.append(f"  {r['retailer']:<22} ${r['price']:>8.2f}{marker}")
        else:
            price_lines.append(f"  {r['retailer']:<22} {'Not listed':>9}")
    body = f"""Your daily deal hunter found a price drop!\n\nJURA ENA 4 - Nordic White\n\n  Best price today:  ${deal['price']:.2f} at {deal['retailer']}\n  Baseline price:    ${BASELINE_PRICE:.2f} at {BASELINE_STORE}\n  You save:          ${deal['savings']:.2f} ({deal['savings_pct']}% off)\n\n  Buy now: {deal.get('url', 'See retailer website')}\n\nAll prices ({today}):\n\n""" + "\n".join(price_lines) + f"\n\nPrices change fast - act now!\n\nSent by your automated JURA ENA 4 Deal Hunter (threshold: {ALERT_THRESHOLD_PCT}% off)"
    subject = f"Deal alert: JURA ENA 4 - ${deal['price']:.2f} at {deal['retailer']} (save ${deal['savings']:.2f})"
    msg = MIMEText(body)
    msg["to"] = RECIPIENT_EMAIL
    msg["subject"] = subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    get_gmail_service().users().messages().send(userId="me", body={"raw": raw}).execute()
    print(f"Email sent: {subject}")

def main():
    print(f"[{datetime.now().isoformat()}] Starting deal hunt for: {PRODUCT_NAME}")
    results = search_for_deals()
    for r in results:
        print(f"  {r['retailer']}: {'$'+str(r['price']) if r.get('price') else 'N/A'} — {r.get('notes','')}")
    deal = find_best_deal(results)
    if deal:
        print(f"Deal found! ${deal['price']} at {deal['retailer']} ({deal['savings_pct']}% off)")
        send_deal_alert(deal, results)
    else:
        print(f"No deals meet the {ALERT_THRESHOLD_PCT}% threshold today.")

if __name__ == "__main__":
    main()
