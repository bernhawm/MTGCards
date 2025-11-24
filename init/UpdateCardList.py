import requests
import json
import os

# Paths
cards_json_path = "cards.json"

# 1. Get the bulk Scryfall JSON metadata
bulk_api_url = "https://api.scryfall.com/bulk-data/oracle-cards"
print("Fetching Scryfall bulk data metadata...")
metadata = requests.get(bulk_api_url).json()
download_url = metadata["download_uri"]

# 2. Download the latest oracle cards
print(f"Downloading latest oracle cards from {download_url} ...")
response = requests.get(download_url)
response.raise_for_status()
scryfall_cards = response.json()

# 3. Load existing cards.json if it exists
if os.path.exists(cards_json_path):
    print("Loading existing cards.json...")
    with open(cards_json_path, "r", encoding="utf-8") as f:
        local_cards = json.load(f)
else:
    local_cards = []

# 4. Build a set of existing card IDs for quick lookup
existing_ids = {card.get("id") for card in local_cards}

# 5. Compare and append new cards
new_cards = []
for card in scryfall_cards:
    if card.get("id") not in existing_ids:
        new_cards.append(card)

if new_cards:
    print(f"Adding {len(new_cards)} new cards to cards.json...")
    local_cards.extend(new_cards)

    with open(cards_json_path, "w", encoding="utf-8") as f:
        json.dump(local_cards, f, indent=2)
else:
    print("No new cards to add.")

print("Sync complete.")
