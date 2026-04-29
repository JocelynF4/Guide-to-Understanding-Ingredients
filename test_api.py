# test_api.py — Phase 3: Test OpenAI API with a sample ingredient list

import sys
sys.stdout.reconfigure(encoding='utf-8')

from openai import OpenAI           # OpenAI SDK
from dotenv import load_dotenv      # reads .env file
import os                           # grabs environment variables

# Load API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Hardcoded sample ingredient list for testing ---
sample_ingredients = """
Water, High Fructose Corn Syrup, Citric Acid, Natural Flavors, 
Sodium Benzoate, Red 40, Yellow 5, Aspartame, Acesulfame Potassium
"""

prompt = f"""
You are a food ingredient analyst. I will give you a list of ingredients from a food or beverage product.
For each ingredient, respond in exactly this format:

[Ingredient Name]
→ What it is: [one plain-English sentence defining the ingredient]
→ Purpose in this product: [one sentence explaining why it's likely included in this specific product]
→ Health flag: ⚠️ [explanation] OR ✅ Generally recognized as safe

Flag these specifically if present:
- Artificial dyes (e.g. Red 40, Yellow 5, Blue 1)
- Preservatives (e.g. sodium benzoate, BHA, BHT, TBHQ)
- Artificial sweeteners (e.g. aspartame, sucralose, acesulfame-K)
- Emulsifiers linked to gut health concerns (e.g. carrageenan, polysorbate 80)
- High-fructose corn syrup
- MSG and flavor enhancers
- Any ingredient with a known regulatory warning or ongoing scientific debate

Be direct but not alarmist. If an ingredient is fine, say so simply.
Use the full ingredient list as context when explaining each ingredient's purpose —
for example, if sugar and cocoa are both present, note that an emulsifier is likely 
helping bind them together.

Here is the ingredient list:
{sample_ingredients}

"""

print("Sending request to OpenAI...\n")

# --- API call ---
response = client.chat.completions.create(
    model="gpt-4o",                     # vision-capable model
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=1500                     # enough for a full ingredient list
)

# --- Print the result ---
print(response.choices[0].message.content)