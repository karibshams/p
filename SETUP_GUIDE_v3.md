# Karib Shams Portfolio v3 — Complete Setup Guide

## ✅ What's New in v3
- 🔢 Updated phone/WhatsApp number: +880 1797470717
- 🏆 EWU Best Paper Award official link added throughout
- 📚 All 16 publications from Google Scholar with citations & DOI links
- 🧠 AI Quiz: 30 unique random questions, no repeats, with explanations after each answer
- 💬 AI Chat: 100% free, zero API, zero cost — pure Python knowledge base
- ⚡ AI Stream team section with 60+ projects drive link
- 🔍 Project filter: All / Professional / Academic / AI Stream
- 🎨 Gold award accent for Best Paper highlighted throughout
- 📁 .gitignore included for clean GitHub push

---

## 📁 Project Structure
```
portfolio_v3/
├── .gitignore                        ← Git ignore rules
├── manage.py                         ← Django management
├── requirements.txt                  ← Dependencies
├── karib_portfolio/
│   ├── settings.py                   ← Django config
│   ├── urls.py                       ← Root URLs
│   └── wsgi.py                       ← Deployment WSGI
└── portfolio/
    ├── models.py                     ← Feedback + ChatLog DB
    ├── views.py                      ← All data + Free AI engine
    ├── urls.py                       ← App URLs
    ├── admin.py                      ← Admin config
    ├── templates/portfolio/
    │   └── index.html                ← Full one-page template
    └── static/
        ├── css/main.css              ← Premium CSS
        ├── js/main.js                ← All JS (Quiz, Chat, Canvas)
        └── img/
            ├── karib.jpg             ← ⚠️ ADD YOUR PHOTO HERE
            └── placeholder.svg       ← Fallback avatar
```

---

## 🚀 Step 1 — Add Your Profile Photo
Place your photo at:
```
portfolio/static/img/karib.jpg
```
**Requirements:** Square crop recommended (500×500px+), face centred, JPG format.

---

## 💻 Step 2 — Run Locally (VS Code)

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows PowerShell:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up database
python manage.py migrate

# 5. (Optional) Create admin user
python manage.py createsuperuser

# 6. Collect static files
python manage.py collectstatic

# 7. Run on custom port (e.g. 8080)
python manage.py runserver 8080
# OR default port 8000:
python manage.py runserver
```

**Open:** http://127.0.0.1:8080  
**Admin:** http://127.0.0.1:8080/admin

---

## 🔢 Step 3 — Change the Local Port
Django runs on port 8000 by default. To change it:

```bash
# Run on port 8080
python manage.py runserver 8080

# Run on port 5000
python manage.py runserver 5000

# Run on specific IP + port (accessible on your network)
python manage.py runserver 0.0.0.0:8080
```

---

## 📤 Step 4 — Push to GitHub

```bash
# 1. Initialise git (if new repo)
git init

# 2. Add all files (.gitignore already excludes db, pyc, venv)
git add .

# 3. Commit
git commit -m "Karib Shams Portfolio v3 — AI/Data Scientist"

# 4. Add your GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 5. Push
git push -u origin main
```

**What .gitignore excludes:** `__pycache__`, `.pyc`, `db.sqlite3`, `venv/`, `staticfiles/`, `.env`, `.DS_Store`

---

## 🌐 Step 5 — Deploy on PythonAnywhere (Free)

### A. Create Account
Go to https://www.pythonanywhere.com → Sign up free.  
Your URL will be: `https://yourusername.pythonanywhere.com`

### B. Upload Files
In PythonAnywhere **Bash console:**
```bash
# Option 1: Clone from GitHub (recommended)
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git ~/portfolio_v3

# Option 2: Upload the zip via Files tab, then unzip:
cd ~ && unzip karib_portfolio_v3.zip
```

### C. Create Virtual Environment
```bash
mkvirtualenv --python=python3.10 karib_env
workon karib_env
pip install django
```

### D. Configure Web App
1. Go to **Web** tab → **Add a new web app**
2. Choose: **Manual configuration** → **Python 3.10**
3. Set fields:
   - **Source code:** `/home/yourusername/portfolio_v3`
   - **Working directory:** `/home/yourusername/portfolio_v3`
   - **Virtualenv:** `/home/yourusername/.virtualenvs/karib_env`

### E. Edit WSGI Configuration File
Click the WSGI file link in the Web tab. Replace ALL content with:
```python
import os
import sys

path = '/home/yourusername/portfolio_v3'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'karib_portfolio.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
Replace `yourusername` with your actual PythonAnywhere username.

### F. Static Files
In **Web** tab → **Static files** section, add:
| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/portfolio_v3/staticfiles` |

Then in Bash console:
```bash
cd ~/portfolio_v3
workon karib_env
python manage.py collectstatic --noinput
python manage.py migrate
```

### G. Update settings.py for Production
Edit `karib_portfolio/settings.py`:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
```

### H. Reload & Go Live
Click **Reload** in the Web tab → Visit your live site!

---

## 🤖 AI Chat — How It Works (Zero Cost)
The `/api/chat/` endpoint uses a **100% free Python knowledge base**:

- Receives the user's message
- Matches it against 30+ regex patterns covering:
  - Karib's personal info, publications, projects, team, skills, education, contact
  - AI/ML concepts: RAG, transformers, deep learning, NLP, CV, XAI, YOLO, LLM, n8n, OCR, embeddings, XGBoost, sentiment analysis, knowledge graphs, medical imaging, precision agriculture, generative AI, Python, Django, and more
- Returns a detailed, formatted response
- Saves the conversation to SQLite database
- **No API key, no external calls, no cost — ever**

---

## 🧠 Quiz Game — 30 Questions
- 30 carefully crafted AI/ML questions covering ML, Deep Learning, Transformers, NLP, Computer Vision, XAI, Data Science, Semi/Self-supervised Learning, and n8n
- **Shuffled randomly** every time — no repeated question order
- Shows explanation after each answer
- Score tracking with grade at the end (Outstanding / Great / Good / Keep Learning)

---

## 🔧 Admin Panel
Visit `/admin` to:
- Read all feedback messages with email
- View all AI chat conversations
- Manage everything without touching code

---

## ✏️ Customisation
- **Change any data:** Edit `DATA` dict in `portfolio/views.py`
- **Add quiz questions:** Add to `ALL_QS` array in `portfolio/static/js/main.js`
- **Add AI chat topics:** Add to `KB` dict + `_respond()` in `portfolio/views.py`
- **Change colors:** Edit `:root` variables in `portfolio/static/css/main.css`
- **Change port:** `python manage.py runserver 8080`
