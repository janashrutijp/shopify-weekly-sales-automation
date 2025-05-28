import os
import ssl
from datetime import datetime, timedelta

import pandas as pd
import requests
from requests.adapters import HTTPAdapter


#  when ran without this, got an error in TLSAdapter)
#  so here i'm customising HTTPS adapter to enforce TLSv1.2

class TLSAdapter(HTTPAdapter):  #  controls how requests makes connections
    def init_poolmanager(self, *args, **kwargs):  #  overriden to inject a custom SSL context
        context = ssl.create_default_context()  #  to create a secure SSL configuration
        context.minimum_version = ssl.TLSVersion.TLSv1_2  #  enforces TLSv1.2
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)  #  returns


def fetch_orders():
    print("📥 Fetching data...")
    shop_url = "xxxxxxxxx"
    access_token = "xxxxxxxxxx"

    endpoint = "/admin/api/2023-07/orders.json"
    base_url = shop_url + endpoint

    # getting orders from past week
    created_at_min = (datetime.utcnow() - timedelta(days=7)).isoformat()

    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }

    params = {
        "status": "any",
        "created_at_min": created_at_min,
        "limit": 250
    }

    session = requests.Session()
    session.mount("https://", TLSAdapter())

    try:
        response = session.get(base_url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if 'orders' not in data:
            print("❌ No orders found in response.")
            return pd.DataFrame()

        # normalising dataframe
        df = pd.json_normalize(data['orders'])
        print(f"✅ {len(df)} orders fetched.")
        return df

    except requests.exceptions.SSLError as e:
        print("❌ SSL Error:", e)
    except requests.exceptions.HTTPError as e:
        print("❌ HTTP Error:", e)
    except requests.exceptions.RequestException as e:
        print("❌ Request Failed:", e)
    except Exception as e:
        print("❌ Unexpected Error:", e)

    return pd.DataFrame()
