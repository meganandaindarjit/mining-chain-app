"""
Coin Colorer — выделяет UTXO транзакции по происхождению (входящие/исходящие, родственные/неродственные адреса).
"""

import sys
import requests

def fetch_transaction(txid):
    url = f"https://blockstream.info/api/tx/{txid}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def extract_addresses(tx_part):
    addresses = []
    for entry in tx_part:
        addr = entry.get("scriptpubkey_address")
        if addr:
            addresses.append(addr)
    return addresses

def main(txid):
    print(f"🎨 Анализ транзакции {txid}...")
    try:
        tx = fetch_transaction(txid)
    except Exception as e:
        print("❌ Ошибка при получении транзакции:", e)
        return

    inputs = extract_addresses(tx.get("vin", []))
    outputs = extract_addresses(tx.get("vout", []))

    print("
🟥 Входящие адреса:")
    for addr in inputs:
        print(f"  - {addr}")

    print("
🟩 Исходящие адреса:")
    for addr in outputs:
        if addr in inputs:
            print(f"  - {addr} (🔁 тот же адрес)")
        else:
            print(f"  - {addr}")

    print("
🎯 Всего входов:", len(inputs), "| Всего выходов:", len(outputs))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python coin_colorer.py <txid>")
        sys.exit(1)
    main(sys.argv[1])
