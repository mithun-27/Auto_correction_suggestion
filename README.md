# 🧠 AI Autocorrection & Auto-Suggestion Tool

A modern AI-powered typing assistant that **auto-corrects spelling** and **predicts the next word** in real time.  
Built using **FastAPI (Python)** + **Tailwind/AlpineJS frontend**, with **DistilGPT-2 AI suggestions** and automatic n-gram fallback for offline use.

---

## 🚀 Features

- 🔤 **Smart Spell Autocorrection**
- 🤖 **AI Next-Word Suggestions** (GPT-2 based)
- ⚡ **Lightweight & Windows-Friendly**
- 🧩 **REST API Ready** (`/api/correct`, `/api/suggest`)
- 🌐 **Modern UI (Tailwind + AlpineJS)** – No build tools needed
- 📦 Can be extended to grammar checkers, editors, or productivity apps

---

## 🧱 Project Structure

```
ai-autocorrect/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ models.py
│  │  ├─ corrector.py
│  │  ├─ ngram.py
│  │  └─ suggester.py   ← DistilGPT-2 suggestions
│  ├─ requirements.txt
│  └─ start.bat         ← One-click startup (Windows)
├─ frontend/
│  ├─ index.html
│  └─ favicon.svg
└─ screenshots/         ← Add your screenshots here
```

---

## ⚒ Installation (Windows)

```bat
cd backend
python -m venv .venv
call .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

If PyTorch fails, install CPU version:
```bat
pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision torchaudio
pip install transformers
```

---

## ▶ Run the App

```bat
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Open in Browser:**  
👉 http://127.0.0.1:8000

**API Docs:**  
👉 http://127.0.0.1:8000/docs

---

## 🛠 API Usage

### 🔁 `/api/correct`
```json
{ "text": "hte quikc borwn fxo" }
```

> Output: `"the quick brown fox"`

### 🤔 `/api/suggest`
```json
{ "context": "I am going", "top_k": 5 }
```

> Output: `["to","home","work","there","now"]`

---

## 🎯 Customize Tips

| Feature        | How to Modify |
|----------------|---------------|
| Stronger spelling | Swap `autocorrect → SymSpell` in `corrector.py` |
| Domain aware suggestions | Change GPT model in `suggester.py` |
| Faster UI updates | Change `@input.debounce.300ms` to `200ms` |

---

## ✅ Test Inputs

| Input                         | Output / Suggestions           |
|------------------------------|--------------------------------|
| `hte quikc borwn fxo`         | `the quick brown fox`          |
| `I am going`                  | `to, home, work, out, now`     |
| `Thank you for`               | `your, the, taking, being`     |

---
## 📸ScreenShot:
### Autocorrection:
<img width="1919" height="869" alt="image" src="https://github.com/user-attachments/assets/9ccdfd71-7f78-4eea-904c-3405033ad078" />

### Autosuggestion:
<img width="1919" height="867" alt="image" src="https://github.com/user-attachments/assets/45629f82-8311-44ac-8b9f-af51a908a66b" />

**NOTE**: Don't worry about the **LOGO**, You can import a SVG logo in the faviocon.svg
---  
# Author: _Mithun_ 
---
