import requests
import pandas as pd
import numpy as np
from tqdm import tqdm

# Insert your Covalent API Key here
COVALENT_API_KEY = "your_covalent_api_key"  # Replace with your actual key
BASE_URL = "https://api.covalenthq.com/v1"
CHAIN_ID = 1  # Ethereum Mainnet


# Load wallet addresses from wallet_addresses.txt
def load_wallets(file_path="wallet_addresses.txt"):
    with open(file_path, 'r') as f:
        wallets = [line.strip() for line in f if line.strip()]
    return wallets


# Fetch token transfer transactions for each wallet
def fetch_wallet_transactions(wallet):
    url = f"{BASE_URL}/{CHAIN_ID}/address/{wallet}/transfers_v2/"
    params = {
        "key": COVALENT_API_KEY,
        "page-size": 1000
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["data"]["items"]
    else:
        print(f"Failed to fetch data for {wallet}")
        return []


# Extract features from transactions
def extract_features(transactions):
    tx_count = len(transactions)
    total_value_eth = 0.0
    for tx in transactions:
        try:
            value = float(tx.get("value", 0)) / 1e18  # Convert from Wei to ETH
            total_value_eth += value
        except:
            continue
    return {
        "tx_count": tx_count,
        "total_value_eth": total_value_eth
    }


# Normalize values
def normalize(value, max_value):
    return value / max_value if max_value else 0


# Compute risk score based on features
def compute_score(features, max_tx, max_val):
    tx_score = normalize(features["tx_count"], max_tx) * 500
    val_score = normalize(features["total_value_eth"], max_val) * 500
    return int(tx_score + val_score)


# Main execution function
def main():
    print("Loading wallet addresses...")
    wallets = load_wallets()

    results = []
    tx_counts = []
    val_amounts = []
    wallet_features = {}

    print("Fetching transaction data...")
    for wallet in tqdm(wallets):
        txs = fetch_wallet_transactions(wallet)
        features = extract_features(txs)
        wallet_features[wallet] = features
        tx_counts.append(features["tx_count"])
        val_amounts.append(features["total_value_eth"])

    max_tx = max(tx_counts) if tx_counts else 1
    max_val = max(val_amounts) if val_amounts else 1

    print("Calculating risk scores...")
    for wallet, features in wallet_features.items():
        score = compute_score(features, max_tx, max_val)
        results.append({"wallet_id": wallet, "score": score})

    df = pd.DataFrame(results)
    df.to_csv("wallet_risk_scores.csv", index=False)
    print("Risk scores saved to wallet_risk_scores.csv")


if __name__ == "__main__":
    main()
