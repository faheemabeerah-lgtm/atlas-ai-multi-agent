# Atlas AI — Research Multi-Agent Team

A Streamlit research app powered by four CrewAI agents and Groq's OpenAI-compatible API:
1. Lead Web Researcher — searches DuckDuckGo
2. Research Analyst — interprets the findings
3. Fact-Checker — independently searches for corroboration or conflicts
4. Report Writer — produces a source-aware Markdown report

## Deploy

1. Upload the full project folder to a GitHub repository.
2. Open https://share.streamlit.io/ and choose **Create app**.
3. Select your repository, branch `main`, and entrypoint `app.py`.
4. In Advanced settings, select Python 3.12.
5. Deploy, then open app Settings → Secrets and add:

```toml
GROQ_API_KEY = "paste-your-Groq-key-here"
```

6. Save and reboot/restart the app if prompted.

## Important
- Never commit your Groq API key to GitHub.
- `requirements.txt` pins the core package versions to make builds more reproducible.
- This project uses DuckDuckGo search, which may temporarily rate-limit or return incomplete results.
- AI-generated research can be wrong. Verify important claims against the linked sources.
