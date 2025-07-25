# Compound Wallet Risk Scoring

This project assigns a risk score (between 0 and 1000) to Ethereum wallet addresses based on their token transfer history. The goal is to analyze wallet behavior and estimate the potential risk involved in lending to those addresses on platforms like Compound V2 or V3.

## What the Project Does

- Loads a list of Ethereum wallet addresses.
- Fetches token transfer data from Covalent API.
- Extracts features like:
  - Total number of transactions.
  - Total value transferred in ETH.
- Calculates a normalized risk score for each wallet.
- Outputs the results in a CSV file.

## How to Run

1. **Clone the repository** or download the code.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
![image alt](https://github.com/KovidSatyala363/compound-risk-scoring/blob/920c4b39493219ccb25119e0e2a1b99c0403cf64/Screenshot%202025-07-25%20135501.png)
