# 🔢 HandScript AI — Handwritten Digit Analyzer

A clean, minimal Streamlit web app that uses **Groq** + **Meta Llama 4 Scout** vision AI to analyze handwritten digit samples. Upload an image or PDF and instantly identify which numbers are present in the writing.

---

## ✨ Features

- 📷 Upload handwriting samples as **JPG, PNG, WEBP, or PDF**
- 🧠 AI-powered digit recognition via **Groq's Llama 4 Scout 17B** vision model
- 📄 **Multi-page PDF support** with thumbnail page picker
- 🎨 Clean, minimal **light-themed UI** — optimized for both mobile and desktop
- ⚡ Fast inference powered by Groq's ultra-low-latency API

---

## 🗂 Project Structure

```
hand_writing_analyzer/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .gitignore                      # Excludes secrets and cache files
└── .streamlit/
    ├── config.toml                 # Streamlit theme & server settings
    ├── secrets.toml                # 🔒 Your API key (NOT committed)
    └── secrets.toml.example        # Template for the secrets file
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.9+**
- A free **Groq API key** → [console.groq.com/keys](https://console.groq.com/keys)

---

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/hand_writing_analyzer.git
cd hand_writing_analyzer
```

---

### 2. Install Dependencies

```bash
pip3 install -r requirements.txt
```

This installs:
| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `groq` | Groq Python SDK for LLM API calls |
| `Pillow` | Image loading and processing |
| `pymupdf` | PDF rendering (converts pages to images) |

---

### 3. Add Your Groq API Key

Copy the example secrets file and fill in your key:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Then open `.streamlit/secrets.toml` and replace the placeholder:

```toml
GROQ_API_KEY = "gsk_your_actual_key_here"
```

> ⚠️ **Never commit `secrets.toml`** — it is already listed in `.gitignore` and will not be pushed to GitHub.

Get your free API key at → [console.groq.com/keys](https://console.groq.com/keys)

---

### 4. Run the App

```bash
# If streamlit is on your PATH:
streamlit run app.py

# If not (common on macOS with Python 3.9):
/Users/YOUR_USERNAME/Library/Python/3.9/bin/streamlit run app.py
```

The app will open automatically in your browser at:
```
Local:   http://localhost:8501
Network: http://YOUR_LOCAL_IP:8501   ← accessible from your phone too
```

> **Tip:** To add `streamlit` to your PATH permanently, add this line to `~/.zshrc`:
> ```bash
> export PATH="$HOME/Library/Python/3.9/bin:$PATH"
> ```
> Then run `source ~/.zshrc`.

---

## 🖥 How to Use

1. **Open the app** at `http://localhost:8501`

2. **Upload a handwriting sample**
   - Drag & drop or click the upload area
   - Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`, `.pdf`
   - For PDFs with multiple pages, a thumbnail strip will appear — select the page to analyze

3. **Click "🔍 Analyze Digits"**
   - The AI reads the sample and identifies which digits are present

4. **View results**
   - The unique numbers found in the sample are displayed as visual badges

---

## 🤖 Model Details

| Setting | Value |
|---|---|
| Provider | [Groq](https://groq.com) |
| Model | `meta-llama/llama-4-scout-17b-16e-instruct` |
| Task | Vision — handwritten digit recognition |
| Temperature | `0.2` (low, for consistent results) |

---

## 🔧 Configuration

Streamlit settings live in `.streamlit/config.toml`:

```toml
[theme]
base = "light"
primaryColor = "#6366F1"
backgroundColor = "#FAFAFA"
secondaryBackgroundColor = "#F0F0F5"
textColor = "#1E1E2E"
font = "sans serif"

[server]
maxUploadSize = 10   # Max upload size in MB
```

---

## 🛠 Troubleshooting

| Problem | Fix |
|---|---|
| `streamlit: command not found` | Use full path: `/Users/YOUR_USERNAME/Library/Python/3.9/bin/streamlit run app.py` |
| `API key missing` error | Make sure `.streamlit/secrets.toml` exists with a valid `GROQ_API_KEY` |
| PDF not rendering | Ensure `pymupdf` is installed: `pip3 install pymupdf` |
| Slow first load | Normal — Streamlit loads the app on first request. Subsequent loads are fast. |

---

## 📦 Deploying to Streamlit Cloud (Optional)

1. Push your code to GitHub *(without `secrets.toml`)*
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Under **Advanced settings → Secrets**, add:
   ```toml
   GROQ_API_KEY = "gsk_your_actual_key_here"
   ```
4. Click **Deploy** — your app will be live at a public URL

---

## 📄 License

MIT — free to use, modify, and distribute.
