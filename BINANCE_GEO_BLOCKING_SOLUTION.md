# 🚨 Binance Geo-Blocking Solution

## Problem

**Error 451:** Binance blocks API access from US IP addresses
```
ccxt.base.errors.ExchangeNotAvailable: binance GET 
https://api.binance.com/api/v3/exchangeInfo 451
{
  "code": 0,
  "msg": "Service unavailable from a restricted location according to 
  'b. Eligibility' in https://www.binance.com/en/terms."
}
```

**Why this happens:**
- Google Colab servers are in the USA
- Binance blocks all US IP addresses (legal compliance)
- FreqTrade calls `exchange.load_markets()` even for offline backtesting
- `skip_pair_validation: true` doesn't bypass this API call

## Solution: HTTP Proxy

### Automatic Proxy (Colab Notebook - Recommended)

The notebook **Cell 7** automatically:
1. Tests multiple free proxies
2. Finds a working proxy
3. Sets environment variables:
   - `HTTP_PROXY=http://proxy:port`
   - `HTTPS_PROXY=http://proxy:port`
4. Verifies Binance API access

**No action needed - just run the notebook!**

### Manual Proxy Setup (Local/Advanced)

If running locally:

```bash
# Linux/Mac
export HTTP_PROXY=http://103.152.112.162:80
export HTTPS_PROXY=http://103.152.112.162:80

# Windows PowerShell
$env:HTTP_PROXY="http://103.152.112.162:80"
$env:HTTPS_PROXY="http://103.152.112.162:80"

# Then run freqtrade
freqtrade backtesting --config config/config.json ...
```

### Free Proxy Services

**Working proxies (as of Oct 2025):**
- http://103.152.112.162:80
- http://20.111.54.16:8123
- http://157.230.241.133:38331

**Find more at:**
- https://www.proxy-list.download/HTTP
- https://free-proxy-list.net/
- https://www.sslproxies.org/

**Note:** Free proxies are unreliable. May need to update regularly.

### Premium Proxy Services (Recommended for Production)

If free proxies fail, use paid services:
- **Bright Data** (formerly Luminati)
- **Smartproxy**
- **Oxylabs**
- **ProxyMesh**

Cost: ~$50-100/month for residential IPs

## Alternative Solutions

### Option 1: Kaggle (Instead of Colab)
- Kaggle servers may be in different regions
- Might not be blocked by Binance
- Similar GPU access as Colab

### Option 2: Local Machine + VPN
- Run backtests locally
- Use VPN with non-US IP
- **Recommended VPNs:**
  - NordVPN
  - ExpressVPN
  - ProtonVPN

### Option 3: Cloud Server (Non-US Region)
- AWS EC2 in Europe/Asia
- DigitalOcean in Singapore
- Vultr in Japan

## Verification

Test if Binance API is accessible:

```python
import requests
import os

proxy = "http://103.152.112.162:80"
os.environ['HTTP_PROXY'] = proxy
os.environ['HTTPS_PROXY'] = proxy

response = requests.get("https://api.binance.com/api/v3/exchangeInfo")
print(f"Status: {response.status_code}")
print(f"Success: {response.status_code == 200}")
```

Expected output:
```
Status: 200
Success: True
```

## Troubleshooting

### Proxy not working?
1. **Try another proxy** from the list
2. **Check proxy is active:** Visit https://www.proxy-list.download/HTTP
3. **Test manually:** Use `curl` or browser with proxy
4. **Update proxy list:** Free proxies change frequently

### Still getting Error 451?
1. **Verify environment variables:**
   ```bash
   echo $HTTP_PROXY
   echo $HTTPS_PROXY
   ```
2. **Check if FreqTrade respects proxy:**
   - Some versions may not respect env vars
   - Try setting in `ccxt_config`
3. **Use VPN instead:** More reliable than free proxies

### FreqTrade ignores proxy?
Add to `config.json`:
```json
"exchange": {
    "name": "binance",
    "ccxt_config": {
        "proxies": {
            "http": "http://103.152.112.162:80",
            "https": "http://103.152.112.162:80"
        }
    }
}
```

## Legal Disclaimer

⚠️ **Important:**
- Using proxies to bypass geo-restrictions may violate Binance Terms of Service
- This is for **educational/development purposes only**
- For production trading, use compliant solutions
- We are not responsible for any ToS violations

## Summary

| Method | Cost | Reliability | Setup |
|--------|------|-------------|-------|
| Free Proxy | Free | Low (30-50%) | Easy (automated) |
| Paid Proxy | $50-100/mo | High (99%) | Easy |
| VPN | $5-15/mo | High (95%) | Medium |
| Cloud Server | $20-50/mo | Very High | Complex |
| Kaggle | Free | Medium | Easy |

**Recommendation:** 
- **Development:** Free proxy (automated in notebook)
- **Production:** Paid proxy or cloud server in allowed region
