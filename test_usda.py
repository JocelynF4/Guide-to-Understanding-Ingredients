# test_usda.py — confirms USDA FoodData Central API is working

import sys
sys.stdout.reconfigure(encoding='utf-8')

import requests                     # makes HTTP calls to the API
from dotenv import load_dotenv
import os
import json                         # pretty-prints the API response

# Load API key from .env
load_dotenv()
api_key = os.getenv("FDC_API_KEY")

if not api_key:
    print("❌ FDC_API_KEY not found in .env — check your file")
    exit()

print("✅ API key loaded\n")

# --- Search for a test product ---
search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"

params = {
    "api_key": api_key,
    "query": "Cheez-It Original",       # what we're searching for
    "dataType": ["Branded"],             # branded products only
    "pageSize": 5,                       # return top 5 matches
}

print("Searching USDA database for 'Cheez-It Original'...\n")

response = requests.get(search_url, params=params)

if response.status_code != 200:
    print(f"❌ API error: {response.status_code}")
    print(response.text)
    exit()

data = response.json()
foods = data.get("foods", [])

if not foods:
    print("❌ No results found")
    exit()

# --- Print what comes back for each result ---
for i, food in enumerate(foods):
    print(f"--- Result {i+1} ---")
    print(f"Name:         {food.get('description')}")
    print(f"Brand:        {food.get('brandOwner')}")
    print(f"FDC ID:       {food.get('fdcId')}")
    print(f"Ingredients:  {food.get('ingredients', 'NOT FOUND')[:200]}")
    print()