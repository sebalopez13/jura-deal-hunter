# JURA ENA 4 Deal Hunter

An automated deal hunter that searches for the best price on the **JURA ENA 4 Fully Automatic Espresso Machine (Nordic White)** every morning and sends an email alert when a deal is found.

## How it works

1. **GitHub Actions** triggers the script every day at 8 AM ET — no manual input needed
2. **Claude AI** searches live across 15+ retailers using web search
3. If a price drops below your threshold, a **Gmail alert** is sent directly to your inbox

## Project structure

```
jura-deal-hunter/
├── .github/
│   └── workflows/
│       └── deal_hunter.yml   # Daily schedule (8 AM ET)
├── src/
│   └── deal_hunter.py        # Main script
└── requirements.txt          # Python dependencies
```

## Configuration

All settings are at the top of `src/deal_hunter.py`:

| Variable | Default | Description |
|---|---|---|
| `PRODUCT_NAME` | JURA ENA 4 Nordic White | Product to search for |
| `BASELINE_PRICE` | $1,199.95 | Reference price (Williams-Sonoma) |
| `ALERT_THRESHOLD_PCT` | 5 | Min % drop to trigger email |
| `RECIPIENT_EMAIL` | sebalopez13@gmail.com | Where alerts are sent |
| `RETAILERS` | 15+ stores | Retailers to search |

## Retailers monitored

Amazon, Williams-Sonoma, Best Buy, Whole Latte Love (new + open box), Costco, shopjura.com, Target, Walmart, Crate & Barrel, Seattle Coffee Gear, 1st in Coffee, eBay (new, open box, refurbished), Google Shopping.

## GitHub Secrets required

| Secret | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `GMAIL_CLIENT_ID` | Google OAuth client ID |
| `GMAIL_CLIENT_SECRET` | Google OAuth client secret |
| `GMAIL_ACCESS_TOKEN` | Gmail access token |
| `GMAIL_REFRESH_TOKEN` | Gmail refresh token |

## Cost

- **GitHub Actions**: free
- **Anthropic API**: ~$0.03–0.05 per daily run (~$1–2/month)
- **Gmail API**: free

## Reusing for other products

Update these 3 lines in `src/deal_hunter.py` and re-enable the workflow:

```python
PRODUCT_NAME   = "Sony WH-1000XM6 Headphones"
BASELINE_PRICE = 399.99
BASELINE_STORE = "Best Buy"
```
