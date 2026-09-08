# Karib Shams — AI & Data Scientist Portfolio

<div align="center">

![Portfolio Preview](https://img.shields.io/badge/Status-Live-00FFC2?style=for-the-badge&logo=vercel)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge)

**🌐 Live:** [karib.pythonanywhere.com](https://karib.pythonanywhere.com)
**🎓 Scholar:** [Google Scholar Profile](https://scholar.google.com/citations?user=C26dtwMAAAAJ&hl=en)
**🏆 Best Paper Award — AII 2025, Washington D.C., USA**

</div>

---

## About

This is the personal portfolio website of **Karib Shams** — Data Scientist, AI Developer, Researcher, and Team Leader of **AI Stream**. Built with Django (Python) and a fully custom futuristic AI-themed frontend.

---

## Features

### Core
- **Futuristic AI/Data Science Theme** — Dark carbon background, neon cyan accents
- **3D Rotating Particle Background** — Built with Three.js
- **Neural Network Canvas** — Animated node connections
- **Custom Cursor** — Neon glowing dot with ring effect
- **Typing Effect** — Cycles through professional roles
- **Smooth Scroll Reveal** — Sections animate on scroll

### AI Robot Guide
- Floating futuristic robot with Karib's photo on the face screen
- Speaks automatically when scrolling to each section (Text-to-Speech)
- Click to open full AI chat panel
- Mute/unmute button for voice control

### Free AI Chat
- 100% free — no API, no cost, always on
- Built-in knowledge base covering all of Karib's research, projects, and skills
- Answers general AI/ML/Data Science questions
- 30+ topic coverage: RAG, transformers, XAI, YOLO, LLM, n8n, and more

### Research & Publications
- 16 publications across IEEE, Springer, Elsevier, Nature Portfolio
- 9 citations · h-index: 2
- Google Scholar links on every paper
- Best Paper Award highlighted with EWU official link
- Research Analytics section with 4 interactive Chart.js visualisations

### Skills & Games
- Skill Radar Chart (spider chart of AI competencies)
- Animated progress bars
- **3 AI Mini Games:**
  - 🧠 AI & ML Quiz (30 random questions)
  - 🤖 Guess the AI Model (10 clue-based questions)
  - 📊 Predict the Output (8 ML scenario questions)
  - ⚡ Typing Speed Game (AI/ML terms, 30 seconds)

### Journey Timeline
- Visual card-based milestone grid (2016 → Now)
- Animated progress bar across years
- Hover effects with 3D lift

### GitHub Activity
- Real contribution heatmap
- GitHub Stats card
- Top Languages card
- GitHub Streak stats
- All live from github.com/karibshams

### Other Features
- **CV Download** — One-click PDF download (easy to update)
- **Dark/Light Mode** — Toggle with saved preference
- **Live Visitor Counter** — Tracks daily and total visits
- **Feedback System** — Stored in database, viewable in admin
- **Mobile Bottom Navigation** — App-style nav on phones
- **Glassmorphism Cards** — Frosted glass project cards
- **Page Transitions** — Smooth curtain animation on load
- **SVG Icon System** — Professional Lucide-style icons (no emojis)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2 (Python 3.11) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| 3D Graphics | Three.js r128 |
| Charts | Chart.js 4.4 |
| Icons | Custom SVG (Lucide-style) |
| Database | SQLite3 |
| Deployment | PythonAnywhere (Free Tier) |
| AI Chat | Custom Python rule-based engine (Free — No API) |
| Voice | Web Speech API (Browser built-in) |

---

## Project Structure

```
p/
├── karib_portfolio/
│   ├── settings.py         # Django configuration
│   ├── urls.py             # Root URL routing
│   └── wsgi.py             # WSGI for deployment
├── portfolio/
│   ├── models.py           # Feedback, ChatLog, VisitorCount
│   ├── views.py            # All data + Free AI engine
│   ├── urls.py             # App URL routes
│   ├── admin.py            # Admin panel config
│   ├── migrations/         # Database migrations
│   ├── templates/
│   │   └── portfolio/
│   │       └── index.html  # Full one-page template
│   └── static/
│       ├── css/main.css    # Complete CSS (1400+ lines)
│       ├── js/main.js      # All JavaScript (1300+ lines)
│       └── img/
│           ├── karib.jpeg              # Profile photo
│           ├── KARIB_SHAMS_latest.pdf  # CV download
│           └── placeholder.svg         # Fallback avatar
├── manage.py
├── requirements.txt
└── README.md
```

---

## Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/karibshams/p.git
cd p

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py migrate

# 6. Run server
python manage.py runserver 8080
```

Open: **http://127.0.0.1:8080**
Admin: **http://127.0.0.1:8080/admin**

---

## Update CV

To update the downloadable CV anytime:
1. Replace `portfolio/static/img/KARIB_SHAMS_latest.pdf` with your new PDF
2. Keep the same filename
3. Run `python manage.py collectstatic --noinput`
4. No code changes needed

---

## Deploy to PythonAnywhere

```bash
# On PythonAnywhere Bash console:
cd ~/p
git pull
python manage.py migrate
python manage.py collectstatic --noinput
```
Then click **Reload** in the Web tab.

---

## Admin Panel

Visit `/admin` to:
- View all feedback messages
- Read AI chat conversation logs
- Monitor daily visitor counts
- Manage all content

---

## Research Highlights

| Metric | Value |
|--------|-------|
| Total Publications | 16 |
| Citations | 9 |
| h-index | 2 |
| Venues | IEEE, Springer, Elsevier, Nature |
| Best Paper Award | AII 2025, Washington D.C. |

**Research domains:** Medical AI · Precision Agriculture · NLP/Emotion Detection · Computer Vision · Explainable AI · Datasets

---

## AI Stream Team

Leading **AI Stream** — a dedicated AI & software team that has delivered **60+ web and mobile products** across healthcare, education, e-commerce, and business automation.

[View All Projects](https://docs.google.com/spreadsheets/d/1fthxg82tjNCc3PP6Ik9e2B1BkEmryOysXDD7Hh_XgoU/edit)

---

## Contact

| Channel | Details |
|---------|---------|
| Email | shams321karib@gmail.com |
| WhatsApp | +880 1797470717 |
| GitHub | [github.com/karibshams](https://github.com/karibshams) |
| LinkedIn | [karib-shams-007975305](https://linkedin.com/in/karib-shams-007975305) |
| Google Scholar | [C26dtwMAAAAJ](https://scholar.google.com/citations?user=C26dtwMAAAAJ&hl=en) |
| Portfolio | [karib.pythonanywhere.com](https://karib.pythonanywhere.com) |

---

## License

MIT License — feel free to use as inspiration. Please do not copy the personal content (bio, publications, projects).

---

<div align="center">
Built with Django · AI Stream · © 2025 Karib Shams
</div>
