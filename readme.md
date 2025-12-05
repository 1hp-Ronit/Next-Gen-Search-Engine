# 🔎 Multi-Source AI Search & Answering Agent

This project is a **multi-source AI-powered search and answer engine** built using:

- **Flask** (for the web server & API)
- **LangChain + LangGraph** (to control agent reasoning and tool orchestration)
- **Bright Data API** (to scrape Google, Bing, Reddit, X, ChatGPT & Perplexity)
- **OpenAI (ChatGPT)** (for intelligent answer synthesis)

The agent is designed to:
✅ Always use **at least two tools**  
✅ Aggregate responses  
✅ Provide **summarized information + sources**  
✅ Support both **JSON API** and **HTML interface**

---

## 🚀 Features

- Search via:
  - Google
  - Bing
  - Reddit
  - X (Twitter)
  - ChatGPT (via BrightData scraping)
  - Perplexity AI (via BrightData scraping)

- Automatic answer aggregation
- Real-time web search
- REST API endpoint support
- Flask web UI
- Secure API keys using `.env`

---


## .env
The .env manages env variables and stores API keys, database passwords and tokens securely.
Create a .env with the following api keys/ids:
BRIGHTDATA_API_KEY -> https://brightdata.com/
BRIGHTDATA_SERP_ZONE -> https://brightdata.com/cp/zones
BRIGHTDATA_GPT_DATASET_ID -> https://brightdata.com/cp/scrapers/api/gd_m7aof0k82r803d5bjm/pdp/overview?id=hl_7ace47eb
BRIGHTDATA_PERPLEXITY_DATASET_ID -> https://brightdata.com/cp/scrapers/api/gd_m7dhdot1vw9a7gc1n/pdp/overview?id=hl_7ace47eb
OPENAI_API_KEY -> https://platform.openai.com/api-keys

