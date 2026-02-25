from dotenv import load_dotenv
import os
import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI

# ==============================
# CONFIG
# ==============================

INPUT_FILE = "data/input.txt"
OUTPUT_FILE = "data/output.json"

# ==============================
# HELPERS
# ==============================

def read_lines(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def save_json(data, file_path: str):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def clean_json_output(text: str):
    """
    Removes markdown wrapping like ```json ... ```
    and extracts pure JSON array.
    """
    # Remove markdown blocks
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    # Extract JSON array
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return match.group()
    
    return text.strip()

# ==============================
# LOAD ENV
# ==============================

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not MODEL_NAME or not GOOGLE_API_KEY:
    raise ValueError("❌ MODEL_NAME or GOOGLE_API_KEY not found in .env file")

# ==============================
# INIT MODEL
# ==============================

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)

# ==============================
# READ INPUT
# ==============================

texts = read_lines(INPUT_FILE)

if not texts:
    raise ValueError("❌ No input texts found.")

print(f"📥 Loaded {len(texts)} texts")

# ==============================
# BUILD PROMPT
# ==============================
prompt = f"""
You are an advanced linguistic sentiment analysis expert.

Analyze the sentiment of the following texts.

Return ONLY a valid JSON array.
Do not add explanations outside JSON.
Keep the same order of input texts.

Each item must follow this exact structure:

{{
"text": "...",
"sentiment": "Positive | Negative | Neutral",
"reasoning": "Detailed analytical explanation explaining why the sentiment was chosen. 
Mention specific words or phrases from the text that influenced the decision. 
If the sentence contains mixed signals, explain which side is stronger and why.",
"reliability": 0.0
}}

Texts:
{json.dumps(texts, ensure_ascii=False)}
"""

# ==============================
# CALL MODEL
# ==============================

try:
    response = llm.invoke(prompt)
    raw_output = response.content
except Exception as e:
    print("❌ Error calling Gemini:", e)
    exit()

# ==============================
# CLEAN OUTPUT
# ==============================

cleaned_output = clean_json_output(raw_output)

try:
    analysis = json.loads(cleaned_output)
except json.JSONDecodeError:
    print("❌ Failed to parse JSON output")
    print("Raw Output:")
    print(raw_output)
    exit()

# ==============================
# SAVE OUTPUT
# ==============================

save_json(analysis, OUTPUT_FILE)

print(f"✅ Done. {len(analysis)} lines saved to {OUTPUT_FILE}")