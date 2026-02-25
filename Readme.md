# Twitter Sentiment Analysis using LLM  
## Prompt Strategies: Reliability & Reasoning

---

## 📌 Project Overview

This project performs sentiment analysis using a Large Language Model (Gemini) with advanced prompt engineering strategies.

Two analytical dimensions are implemented:

- 🔎 **Reasoning** → Detailed explanation of why a sentiment was chosen  
- 📊 **Reliability Score** → Confidence estimation (0.0 – 1.0)

---

## 🧠 Approach

Instead of training deep learning models, this project leverages:

- Structured Prompt Engineering
- Deterministic temperature (0)
- JSON-constrained output
- Reliability scoring

---

## 📝 Prompt Strategy

The model is instructed to:

- Return strictly valid JSON
- Keep order of input texts
- Provide analytical reasoning
- Assign reliability score

---

## 📂 Project Structure
twitter-sentiment-llm/
│
├── data/
│ ├── input.txt
│ └── output.json
│
├── main.py
├── .env.example
├── requirements.txt
└── README.md

---

## 🚀 How to Run

1. Clone the repo
2. Create `.env` file based on `.env.example`
3. Install dependencies
pip install -r requirements.txt

4. Run:
python main.py


---

## 🛠 Technologies Used

- LangChain
- Google Gemini
- Prompt Engineering
- Python

---

## 🎯 Key Difference from Traditional ML

| Traditional ML | LLM Prompt Strategy |
|---------------|--------------------|
| Requires training | No training |
| Fixed architecture | Flexible reasoning |
| Accuracy-based | Explanation-based |

---

## 👤 Author
Mohamed Mahmoud