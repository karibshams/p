import json
import re
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Feedback, ChatLog, VisitorCount
from django.core.mail import send_mail
from django.conf import settings as django_settings
from django.utils import timezone
from django.db.models import Sum

# ══════════════════════════════════════════════════════════════════
#  PORTFOLIO DATA — KARIB SHAMS v3
# ══════════════════════════════════════════════════════════════════
DATA = {
    "name": "Karib Shams",
    "title": "Data Scientist & AI Developer",
    "email": "shams321karib@gmail.com",
    "phone": "+880 1797470717",
    "whatsapp": "8801797470717",
    "location": "93 South Bashabo, Dhaka-1214, Bangladesh",
    "github": "https://github.com/karibshams",
    "linkedin": "https://linkedin.com/in/karib-shams-007975305",
    "scholar": "https://scholar.google.com/citations?user=C26dtwMAAAAJ&hl=en",
    "portfolio_url": "https://karib.pythonanywhere.com",
    "award_url": "https://ewubd.edu/achievement-details/ewu-researchers-win-best-paper-award-international-ai-conference-washington-dc",
    "citations": 9,
    "h_index": 2,
    "about": (
        "AI/ML engineer with hands-on experience in deep learning, computer vision, NLP, and RAG "
        "pipelines. Skilled in Python, TensorFlow, PyTorch, Django, and n8n automation, with a "
        "track record of leading teams to build and ship production AI systems. Backed by 17 peer-reviewed "
        "publications, including a Best Paper Award, with a sustained research focus on agricultural "
        "computer vision and graph neural networks. Senior Executive Data Scientist & Team Leader "
        "at Join Venture Ai (JVai) — delivering 60+ real-world AI products with a 45+ member team."
    ),
    "team": {
        "name": "AI Stream",
        "projects_count": "60+",
        "team_members": "45+",
        "systems_delivered": "13+",
        "desc": (
            "I lead AI Stream — a dedicated AI & software team delivering 60+ web and mobile "
            "products. Our work spans RAG systems, voice AI, healthcare platforms, education apps, "
            "e-commerce automation, and full-stack SaaS solutions across diverse industries."
        ),
        "drive": "https://docs.google.com/spreadsheets/d/1fthxg82tjNCc3PP6Ik9e2B1BkEmryOysXDD7Hh_XgoU/edit",
    },
    "skills": {
        "Programming": ["Python", "JavaScript", "HTML/CSS", "SQL", "C/C++", "Java", "Django", "FastAPI"],
        "AI & ML": ["Deep Learning", "Computer Vision", "NLP", "Explainable AI (XAI / SHAP)",
                    "Knowledge Graphs", "Sentiment Analysis", "Semi-Supervised Learning",
                    "Self-Supervised Learning", "RAG Pipelines", "LLMs & Generative AI", "OCR"],
        "Automation & AI Ops": ["n8n Workflows", "LLM Chaining", "Webhook Systems", "API Orchestration",
                                 "Prompt Engineering", "AI Workflow Integration", "OpenAI API", "FAISS"],
        "Tools & Platforms": ["PyTorch / TensorFlow", "Scikit-learn", "Streamlit", "HuggingFace", "Roboflow", "Kaggle",
                               "Jupyter / Colab", "Oracle APEX", "VS Code", "Git", "Linux Admin"],
    },
    "experience": [
        {
            "company": "Join Venture Ai (JVai)",
            "role": "Senior Executive Data Scientist & Team Leader",
            "period": "Jun. 2025 – Oct. 2026",
            "location": "Dhaka, Bangladesh",
            "desc": (
                "AI System Development: Developed 13+ production AI systems, including RAG-based NLP chatbots, cutting client response time by 40%. "
                "Team Leadership: Led a 45+ member AI team across R&D sprints, technical planning, and delivery, completing client-facing features on schedule. "
                "Workflow Automation: Automated n8n workflows with webhook triggers and OpenAI/email APIs, cutting manual processing by 10 hrs/week. "
                "Sales Enablement: Created AI-enabled lead generation tools with the sales team, improving pipeline efficiency and prospect qualification."
            ),
            "points": [
                "AI System Development: Developed 13+ production AI systems, including RAG-based NLP chatbots, cutting client response time by 40%.",
                "Team Leadership: Led a 45+ member AI team across R&D sprints, technical planning, and delivery, completing client-facing features on schedule.",
                "Workflow Automation: Automated n8n workflows with webhook triggers and OpenAI/email APIs, cutting manual processing by 10 hrs/week.",
                "Sales Enablement: Created AI-enabled lead generation tools with the sales team, improving pipeline efficiency and prospect qualification.",
            ],
        },
        {
            "company": "East West University",
            "role": "Graduate Teaching Assistant (GTA)",
            "period": "Oct. 2024 – Dec. 2025",
            "location": "Dhaka, Bangladesh",
            "desc": (
                "Instruction: Taught lectures and lab sessions for Statistics, AI, and Machine Learning courses to a cohort of 70+ graduate students per semester. "
                "Mentorship: Guided 90+ students in advanced ML projects and data analysis assignments, contributing to improved student performance outcomes."
            ),
            "points": [
                "Instruction: Taught lectures and lab sessions for Statistics, AI, and Machine Learning courses to a cohort of 70+ graduate students per semester.",
                "Mentorship: Guided 90+ students in advanced ML projects and data analysis assignments, contributing to improved student performance outcomes.",
            ],
        },
        {
            "company": "East West University",
            "role": "Research Assistant",
            "period": "Oct. 2024 – Dec. 2025",
            "location": "Dhaka, Bangladesh",
            "desc": (
                "Academic Research: Co-authored 17 peer-reviewed publications in Data Science, Computer Vision, and NLP, with 1 Best Paper Award at an international conference. "
                "Dataset Contribution: Supported development of the TFP-BD dataset for traffic flow and pedestrian analysis, published in Data in Brief (Vol. 59, 2025)."
            ),
            "points": [
                "Academic Research: Co-authored 17 peer-reviewed publications in Data Science, Computer Vision, and NLP, with 1 Best Paper Award at an international conference.",
                "Dataset Contribution: Supported development of the TFP-BD dataset for traffic flow and pedestrian analysis, published in Data in Brief (Vol. 59, 2025).",
            ],
        },
    ],
    "projects": [
        {"name": "BhromonGhuri – Full-Stack Travel & Tour Platform", "type": "Professional",
         "desc": "Built a full-scale tourism platform (Django 5, HTMX, Alpine.js) with zero-reload filtering, instant pricing, and bKash/Nagad payment verification. [Live on October]",
         "link": "https://github.com/karibshams", "tags": ["Full-Stack", "Django 5", "HTMX", "Alpine.js", "bKash/Nagad"]},
        {"name": "AI-Powered Invoice Voucher Processing System", "type": "Professional",
         "desc": "Architected a GPT-4o Vision pipeline that extracts invoice data, classifies GL accounts and profit centres, and generates payment vouchers with confidence-based review (Freelance / Fiverr).",
         "link": "#", "tags": ["GPT-4o Vision", "OCR", "Finance AI", "Fiverr Freelance"]},
        {"name": "HealthRide – AI-Driven NEMT Platform", "type": "Professional",
         "desc": "Delivered a 24/7 GPT-4o voice receptionist and AI dispatch engine with real-time driver matching across 6 event triggers for Non-Emergency Medical Transport.",
         "link": "#", "tags": ["Voice AI", "GPT-4o", "Dispatch AI", "Healthcare"]},
        {"name": "Eat at Home – AI Meal Cost Estimator", "type": "Professional",
         "desc": "Designed a GPT-4o meal-cost estimation model with store-tier blending and ZIP-code regional pricing multipliers.",
         "link": "#", "tags": ["GPT-4o", "Computer Vision", "Pricing AI"]},
        {"name": "EmoThrive – AI Therapeutic Assistant", "type": "Professional",
         "desc": "Launched a voice-enabled LLM therapy assistant with PDF-backed knowledge retrieval, integrating speech recognition and a RAG workflow.",
         "link": "https://emothrive.net/", "tags": ["Voice AI", "RAG", "Healthcare", "LLM"]},
        {"name": "OP Mental Performance AI Coach", "type": "Professional",
         "desc": "AI coaching platform for athletes and professionals targeting optimal mental performance and excellence.",
         "link": "https://optimalperformanceai.com/", "tags": ["AI Coach", "NLP", "LLM"]},
        {"name": "VoiceMind AI Mental Wellness App", "type": "Professional",
         "desc": "Mental wellness mobile application powered by voice AI and large language models.",
         "link": "https://lnkd.in/gFUFHn98", "tags": ["Voice AI", "Mental Health", "Mobile"]},
        {"name": "EduGPT – PDF Academic Chatbot", "type": "Professional",
         "desc": "PDF-powered RAG academic chatbot serving CSE and EEE students at East West University with instant answers.",
         "link": "https://github.com/karibshams/cseeeegpt1.0.git", "tags": ["RAG", "Chatbot", "Education"]},
        {"name": "RAG-Based AI System", "type": "Professional",
         "desc": "Deployed a Retrieval-Augmented Generation pipeline using FAISS embeddings and OpenAI LLMs, delivering context-aware responses across 500+ document chunks.",
         "link": "#", "tags": ["RAG", "FAISS", "OpenAI LLM", "Embeddings"]},
        {"name": "n8n AI Video Generation Automation", "type": "Professional",
         "desc": "Orchestrated end-to-end AI video creation using n8n, cutting manual production effort by ~80% through API-chained workflows.",
         "link": "#", "tags": ["n8n", "Workflow Automation", "Video AI", "APIs"]},
        {"name": "Hebrew/Yiddish Handwriting Transcription System", "type": "Professional",
         "desc": "Engineered an OCR pipeline for cursive handwriting using GPT-4o and Claude Vision APIs with CER-based accuracy evaluation.",
         "link": "#", "tags": ["OCR", "Claude Vision", "GPT-4o", "NLP"]},
        {"name": "OCR Text Extraction System", "type": "Professional",
         "desc": "Assembled a scalable OCR engine supporting multi-format document ingestion and structured text output.",
         "link": "https://github.com/karibshams/simple_ocr.git", "tags": ["OCR", "Computer Vision", "Python", "Deep Learning"]},
        {"name": "Nory0929 – Video-Based Auto Marketplace", "type": "Professional",
         "desc": "Produced a multimodal video generation agent using Kling 2.5 and OpenAI that transforms 5+ vehicle images and an optional prompt into 25-second, 720p marketing videos.",
         "link": "#", "tags": ["Video AI", "Multimodal", "Kling 2.5", "OpenAI"]},
        {"name": "MystudyBuddy App", "type": "Professional",
         "desc": "Smart AI study companion enhancing student productivity through personalised learning paths and AI-driven insights.",
         "link": "#", "tags": ["EdTech", "AI", "Productivity"]},
        {"name": "LawyerCity – Legal RAG Advisor", "type": "Professional",
         "desc": "Bilingual RAG-based legal advisor system for LawyerCity Ethiopia — answers legal questions in English and Amharic using FAISS embeddings.",
         "link": "#", "tags": ["RAG", "Bilingual", "Legal AI", "FAISS"]},
        {"name": "Vehicle Detection and Traffic Flow Prediction", "type": "Academic",
         "desc": "Trained deep learning models on the TFP-BD dataset for vehicle detection and traffic flow prediction on Bangladeshi urban roads.",
         "link": "#", "tags": ["Computer Vision", "TFP-BD", "Traffic AI", "Deep Learning"]},
        {"name": "Sunflower & Rice Panicle Detection", "type": "Academic",
         "desc": "Self-supervised visual representation learning for precision agriculture — published in Smart Agricultural Technology.",
         "link": "#", "tags": ["Self-Supervised", "AgriAI", "Vision", "Published"]},
        {"name": "M.Sc. Thesis – SSL & Graph-Refined Detection", "type": "Academic",
         "desc": "Self-Supervised Learning and Graph-Refined Object Detection Framework for Precision Agriculture.",
         "link": "https://github.com/karibshams", "tags": ["Self-Supervised", "Graph Neural Networks", "AgriAI", "MSc Thesis"]},
        {"name": "B.Sc. Thesis – Tuberculosis Diagnosis", "type": "Academic",
         "desc": "Tuberculosis Diagnosis from Chest X-Ray Image Using Deep Learning Techniques (Published in IEEE ICAECT 2025).",
         "link": "https://doi.org/10.1109/ICAECT63952.2025.10958925", "tags": ["Deep Learning", "Medical AI", "Computer Vision", "BSc Thesis"]},
        {"name": "AI Stream — 60+ Delivered Projects", "type": "Team",
         "desc": "Team Lead of AI Stream: 60+ web & mobile AI products across healthcare, education, e-commerce, and automation. 45+ member team.",
         "link": "https://docs.google.com/spreadsheets/d/1fthxg82tjNCc3PP6Ik9e2B1BkEmryOysXDD7Hh_XgoU/edit",
         "tags": ["Team Lead", "45+ Members", "60+ Projects", "AI Products"]},
    ],
    "publications": [
        {"title": "CodeMixEcom-Emotion: A Large-Scale Bangla–English Review Corpus and Transformer-Based Benchmark for Fine-Grained Emotion Detection",
         "venue": "AII 2025, Springer-Nature CCIS — Washington D.C., USA",
         "award": "🏆 Best Paper Award", "cited": 0, "doi": "",
         "award_url": "https://ewubd.edu/achievement-details/ewu-researchers-win-best-paper-award-international-ai-conference-washington-dc",
         "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:zYLM7Y9cAGgC"},
        {"title": "Towards Annotation-Efficient Kidney CT Scan Classification: Supervised and Semi-Supervised Swin Transformer Frameworks",
         "venue": "IEEE SPICSCON 2025", "award": "", "cited": 0, "doi": "", "award_url": "",
         "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:u-x6o8ySG0sC"},
        {"title": "Histopathology Images-Based Deep Learning Prediction of Prognosis and Therapeutic Response in Small Cell Lung Cancer",
         "venue": "ICDMIS 2024, Springer (Data Mining and Information Security, Vol. 5)",
         "award": "", "cited": 0, "doi": "", "award_url": "",
         "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:W7OEmFMy1HYC"},
        {"title": "TFP-BD: An Image Dataset for Traffic Flow and Pedestrian Movement Analysis on Bangladeshi Urban Roads",
         "venue": "Data in Brief, Vol. 59, 2025, p.111398", "award": "", "cited": 2, "doi": "", "award_url": "",
         "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:IjCSPb-OGe4C"},
        {"title": "Tuberculosis Diagnosis from Chest X-Ray Image Using Deep Learning Techniques",
         "venue": "IEEE ICAECT 2025", "award": "", "cited": 1,
         "doi": "10.1109/ICAECT63952.2025.10958925", "award_url": "",
         "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:UeHWp8X0CEIC"},
        {"title": "Real-Time Monitoring of Oyster Mushroom Cultivation Using CCTV and Attention-Enhanced ShuffleNet-Based Explainable AI",
         "venue": "Smart Agricultural Technology, Vol. 12, 2025, p.101571", "award": "", "cited": 1,
         "doi": "10.1016/j.atech.2025.101571", "award_url": "",
         "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:2osOgNQ5qMEC"},
        {"title": "Interpretable Illness-Category Classification from Drug Attributes Using XGBoost with SHAP Explanations",
         "venue": "IEEE QPAIN 2025", "award": "", "cited": 1,
         "doi": "10.1109/QPAIN66474.2025.11172160", "award_url": "",
         "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:u5HHmVD_uO8C"},
        {"title": "Real-Time Sunflower Detection Using Semi-Supervised and Self-Supervised Deep Learning for Precision Agriculture",
         "venue": "Smart Agricultural Technology, 2025, p.101684", "award": "", "cited": 2, "doi": "", "award_url": "",
         "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:LkGwnXOMwfcC"},
        {"title": "BDFlower: Growth Stage Flower Image Dataset for Precision Agriculture and Floriculture",
         "venue": "Data in Brief, 2026, p.112745", "award": "", "cited": 1, "doi": "", "award_url": "",
         "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:YsMSGLbcyi4C"},
        {"title": "Benchmarking Hybrid CNN and Transformer Backbones with GCN for Flower Growth-Stage Classification",
         "venue": "Scientific Reports, Nature Portfolio, 2026", "award": "", "cited": 0, "doi": "", "award_url": "",
         "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:WF5omc3nYNoC"},
        {"title": "Semi-Supervised Deep Learning for Early Detection of Bone Metastases in Adult Breast Cancer Patients",
         "venue": "IEEE BIBE 2025", "award": "", "cited": 0, "doi": "", "award_url": "",
         "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:eQOLeE2rZwMC"},
        {"title": "Maternal Health Risk Assessment with Interpretable Machine Learning: Evidence from Bangladesh",
         "venue": "IEEE SPICSCON 2025", "award": "", "cited": 0, "doi": "", "award_url": "",
         "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:_FxGoFyzp5QC"},
        {"title": "Occlusion-Resilient Surgical Instrument Detection Using Self-Supervised Learning and YOLO Models",
         "venue": "IEEE BIBE 2025", "award": "", "cited": 0, "doi": "", "award_url": "",
         "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:ufrVoPGSRksC"},
        {"title": "Leveraging Semi-Supervised Learning for Multimodal Medical Image Classification with Paired CT and MRI",
         "venue": "ICCIT 2025", "award": "", "cited": 0, "doi": "", "award_url": "",
         "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:d1gkVwhDpl0C"},
        {"title": "Explainable Random Forest Framework for Real-Time Indoor Air-Quality Prediction at Airports Using SCD30 Sensor Data",
         "venue": "IEEE QPAIN 2025", "award": "", "cited": 0, "doi": "", "award_url": "",
         "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:qjMakFHDy7sC"},
        {"title": "Smartphone-Based Multi-Criteria Vegetable Object Detection Dataset from Bangladesh",
         "venue": "Data in Brief, 2025, p.112281", "award": "", "cited": 1, "doi": "", "award_url": "",
         "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:9yKSN-GCB0IC"},
    ],
    "education": [
        {"degree": "MSc. in CSE", "institution": "East West University", "period": "01/2025 – 12/2025", "detail": "CGPA: 3.91 | Major: Data Science"},
        {"degree": "B.Sc. in CSE", "institution": "East West University", "period": "01/2020 – 07/2024", "detail": "CGPA: 3.58"},
        {"degree": "HSC", "institution": "National Ideal College", "period": "2017 – 2019", "detail": ""},
        {"degree": "SSC", "institution": "Motijheel Model School And College", "period": "2016 – 2017", "detail": ""},
    ],
    "references": [
        {"name": "Mohammad Rifat Ahmmad Rashid", "title": "Associate Professor, East West University", "email": "rifat.rashid@ewubd.edu"},
        {"name": "Musharrat Khan", "title": "Senior Lecturer, East West University", "email": "musharrat.khan@ewubd.edu"},
    ],
    "languages": [
        {"name": "English", "level": "Advanced (C1)"},
        {"name": "Bengali", "level": "Native"},
    ],
    "interests": ["Data science and analytics", "Traveling", "Football"],
}

# ══════════════════════════════════════════════════════════════════
#  FREE AI ENGINE — 100% Python, Zero API Cost
# ══════════════════════════════════════════════════════════════════

KB = {
    "greeting": "Hello! 👋 I'm Karib Shams's AI assistant — 100% free, zero API cost. I know everything about his 17 publications, 60+ team projects, Best Paper Award, and can explain any AI/ML concept. What would you like to explore?",

    "who": ("Karib Shams is a Data Scientist & AI Developer based in Dhaka, Bangladesh.\n\n"
            "🎓 Education:\n• MSc CSE — East West University (CGPA 3.91, Data Science major)\n• BSc CSE — East West University (CGPA 3.58)\n\n"
            "💼 Current Role: Senior Executive Data Scientist & Team Leader at Join Venture Ai (JVai)\n"
            "🏆 Award: Best Paper Award — AII 2025, Washington D.C., USA\n"
            "📊 Research: 17 publications, 9 citations, h-index 2\n"
            "⚡ Team: Leads AI Stream — 60+ delivered AI products with 45+ members"),

    "contact": ("📧 Email: shams321karib@gmail.com\n"
                "📱 Phone/WhatsApp: +880 1797470717\n"
                "📍 Location: 93 South Bashabo, Dhaka-1214, Bangladesh\n"
                "💻 GitHub: github.com/karibshams\n"
                "🔗 LinkedIn: linkedin.com/in/karib-shams-007975305\n"
                "🎓 Google Scholar: scholar.google.com/citations?user=C26dtwMAAAAJ\n"
                "🌐 Portfolio: karib.pythonanywhere.com"),

    "award": ("🏆 BEST PAPER AWARD — AII 2025, Washington D.C., USA!\n\n"
              "Karib Shams received the Best Paper Award at the 5th International Conference on "
              "Applied Intelligence and Informatics (AII 2025), held in Washington D.C., USA.\n\n"
              "Winning Paper: 'CodeMixEcom-Emotion: A Large-Scale Bangla–English Review Corpus "
              "and Transformer-Based Benchmark for Fine-Grained Emotion Detection'\n\n"
              "Published in Springer-Nature CCIS proceedings.\n"
              "🔗 EWU Official: ewubd.edu/achievement-details/ewu-researchers-win-best-paper-award-international-ai-conference-washington-dc"),

    "publications": ("📚 Karib has 17 publications across IEEE, Springer, Elsevier, and Nature Portfolio:\n\n"
                     "📊 Stats: 9 citations | h-index: 2\n\n"
                     "🏆 Best Paper: CodeMixEcom-Emotion (AII 2025, Springer)\n"
                     "🫁 Medical: TB X-Ray, Lung Cancer, Kidney CT, Bone Metastases, CT+MRI\n"
                     "🌾 Agriculture: Sunflower detection, BDFlower dataset, Mushroom XAI\n"
                     "🚦 Vision: Traffic dataset (TFP-BD), Surgical instrument detection\n"
                     "💊 Healthcare AI: Drug classification (XGBoost+SHAP), Air quality XAI\n"
                     "🌸 Botany: Flower growth-stage classification (CNN+Transformer+GCN)\n\n"
                     "View profile: scholar.google.com/citations?user=C26dtwMAAAAJ"),

    "education": ("🎓 Karib's Education:\n\n"
                  "• MSc in CSE — East West University (Jan 2025 – Dec 2025)\n  CGPA: 3.91 | Major: Data Science\n\n"
                  "• BSc in CSE — East West University (Jan 2020 – Jul 2024)\n  CGPA: 3.58\n\n"
                  "• Higher Secondary Certificate (HSC) — National Ideal College (2017–2019)\n\n"
                  "• Secondary School Certificate (SSC) — Motijheel Model School And College (2016–2017)"),

    "experience": ("💼 Karib's Professional Experience:\n\n"
                   "1️⃣ Senior Executive Data Scientist & Team Leader\n"
                   "   Join Venture Ai (JVai) — Jun 2025 – Oct 2026 | Dhaka, Bangladesh\n"
                   "   • AI System Development: Developed 13+ production AI systems, including RAG-based NLP chatbots, cutting client response time by 40%.\n"
                   "   • Team Leadership: Led a 45+ member AI team across R&D sprints, technical planning, and delivery, completing client-facing features on schedule.\n"
                   "   • Workflow Automation: Automated n8n workflows with webhook triggers and OpenAI/email APIs, cutting manual processing by 10 hrs/week.\n"
                   "   • Sales Enablement: Created AI-enabled lead generation tools with the sales team, improving pipeline efficiency and prospect qualification.\n\n"
                   "2️⃣ Graduate Teaching Assistant (GTA)\n"
                   "   East West University — Oct 2024 – Dec 2025 | Dhaka, Bangladesh\n"
                   "   • Instruction: Taught lectures and lab sessions for Statistics, AI, and Machine Learning courses to a cohort of 70+ graduate students per semester.\n"
                   "   • Mentorship: Guided 90+ students in advanced ML projects and data analysis assignments, contributing to improved student performance outcomes.\n\n"
                   "3️⃣ Research Assistant\n"
                   "   East West University — Oct 2024 – Dec 2025 | Dhaka, Bangladesh\n"
                   "   • Academic Research: Co-authored 17 peer-reviewed publications in Data Science, Computer Vision, and NLP, with 1 Best Paper Award at an international conference.\n"
                   "   • Dataset Contribution: Supported development of the TFP-BD dataset for traffic flow and pedestrian analysis, published in Data in Brief (Vol. 59, 2025)."),

    "skills": ("⚙️ Karib's Technical Skills:\n\n"
               "Languages: Python, JavaScript, SQL, C, C++, Java, HTML, CSS\n"
               "Frameworks: Django, FastAPI, TensorFlow, PyTorch, Scikit-learn, Streamlit\n"
               "AI & ML: Deep Learning, NLP, Computer Vision, OCR, RAG Pipelines, LLMs, Generative AI, Explainable AI (SHAP), Knowledge Graphs\n"
               "Automation & MLOps: n8n, LLM Chaining, Webhook Systems, OpenAI API, FAISS, Prompt Engineering\n"
               "Tools: Jupyter Notebook, Google Colab, Roboflow, Kaggle, Oracle APEX, VS Code, Git"),

    "projects": ("🚀 Karib's Key Projects:\n\n"
                 "• BhromonGhuri — Full-Stack Travel & Tour Booking Platform (Django 5, HTMX, Alpine.js, bKash/Nagad)\n"
                 "• AI-Powered Invoice Voucher Processing System — Freelance (Fiverr) GPT-4o Vision pipeline\n"
                 "• HealthRide — AI-driven NEMT Platform with 24/7 GPT-4o voice receptionist and dispatch engine\n"
                 "• Eat at Home — AI Meal Cost Estimator with ZIP-code pricing multipliers\n"
                 "• EmoThrive (emothrive.net) — Voice-enabled AI therapeutic assistant with PDF-backed RAG\n"
                 "• OP Mental Performance AI Coach (optimalperformanceai.com)\n"
                 "• RAG-Based AI System — FAISS embeddings + OpenAI LLMs across 500+ document chunks\n"
                 "• Hebrew/Yiddish Handwriting Transcription System — GPT-4o and Claude Vision OCR\n"
                 "• OCR Text Extraction System (github.com/karibshams/simple_ocr.git)\n"
                 "• Nory0929 — Video-Based Auto Marketplace with Kling 2.5 and OpenAI (25s 720p videos)\n"
                 "• Vehicle Detection & Traffic Flow Prediction on TFP-BD dataset\n"
                 "• M.Sc. Thesis — SSL and Graph-Refined Object Detection for Precision Agriculture\n"
                 "• B.Sc. Thesis — Tuberculosis Diagnosis from Chest X-Ray Image (IEEE ICAECT 2025)"),

    "team": ("⚡ AI Stream — Karib's Team:\n\n"
             "Karib leads AI Stream, a dedicated AI & software team that has delivered "
             "60+ web and mobile projects with a 45+ member team.\n\n"
             "Project types: RAG systems, voice AI apps, healthcare platforms, education tools, "
             "e-commerce automation, full-stack SaaS products.\n\n"
             "Industries: Healthcare, Education, Agriculture, Business Automation, Entertainment\n\n"
             "View all 60+ projects: docs.google.com/spreadsheets/d/1fthxg82tjNCc3PP6Ik9e2B1BkEmryOysXDD7Hh_XgoU"),

    # ── AI/ML CONCEPTS ─────────────────────────────────
    "machine_learning": ("🤖 Machine Learning (ML):\n\n"
                         "ML enables systems to learn from data without explicit programming.\n\n"
                         "Types:\n"
                         "• Supervised — learns from labeled data (classification, regression)\n"
                         "• Unsupervised — finds patterns in unlabeled data (clustering)\n"
                         "• Reinforcement — learns via rewards and penalties\n"
                         "• Semi-supervised — uses both labeled + unlabeled data\n"
                         "• Self-supervised — generates labels from data structure itself\n\n"
                         "Key algorithms: Linear Regression, Decision Trees, SVM, Neural Networks, "
                         "Random Forest, XGBoost, K-Means"),

    "deep_learning": ("🧠 Deep Learning:\n\n"
                      "Deep Learning uses multi-layer neural networks to learn hierarchical representations.\n\n"
                      "Key architectures:\n"
                      "• CNN — for images and spatial data\n"
                      "• RNN/LSTM — for sequences and time series\n"
                      "• Transformer — attention-based, powers LLMs\n"
                      "• GAN — generative adversarial networks\n"
                      "• Autoencoder — unsupervised feature learning\n"
                      "• Diffusion Models — for image generation\n\n"
                      "Karib uses deep learning across all his published research."),

    "rag": ("📚 RAG — Retrieval-Augmented Generation:\n\n"
            "RAG combines a retrieval system with a language model:\n\n"
            "How it works:\n"
            "1. User asks a question\n"
            "2. Relevant documents retrieved from knowledge base\n"
            "3. Context + question fed to LLM\n"
            "4. LLM generates a grounded, factual answer\n\n"
            "Advantages:\n"
            "• Reduces hallucinations dramatically\n"
            "• Uses up-to-date knowledge\n"
            "• Answers are citable and verifiable\n\n"
            "Karib built RAG in EmoThrive and EduGPT."),

    "transformer": ("⚡ Transformer Architecture:\n\n"
                    "Introduced in 'Attention is All You Need' (2017), transformers revolutionised AI.\n\n"
                    "Key components:\n"
                    "• Self-attention — each token attends to all others\n"
                    "• Multi-head attention — multiple attention heads in parallel\n"
                    "• Positional encoding — adds position information\n"
                    "• Feed-forward layers — process attention output\n"
                    "• Layer normalisation + residual connections\n\n"
                    "Powers: GPT, BERT, T5, Swin Transformer, ViT\n"
                    "Karib used Swin Transformer for kidney CT classification."),

    "xai": ("🔍 Explainable AI (XAI):\n\n"
            "XAI makes ML models interpretable and transparent.\n\n"
            "Key techniques:\n"
            "• SHAP — SHapley Additive exPlanations (feature importance values)\n"
            "• LIME — Local Interpretable Model-agnostic Explanations\n"
            "• Grad-CAM — visualises CNN attention on images\n"
            "• Feature Importance — from tree-based models\n"
            "• Attention Visualisation — for transformer models\n\n"
            "Karib's XAI publications:\n"
            "• Drug classification with XGBoost+SHAP (IEEE QPAIN 2025)\n"
            "• Mushroom monitoring with ShuffleNet+XAI (Smart Agricultural Technology)"),

    "computer_vision": ("👁️ Computer Vision:\n\n"
                        "CV enables machines to interpret and understand visual data.\n\n"
                        "Key tasks:\n"
                        "• Image Classification — what is in this image?\n"
                        "• Object Detection — where are objects? (YOLO, Faster R-CNN)\n"
                        "• Semantic Segmentation — pixel-level classification\n"
                        "• Instance Segmentation — separate object instances\n"
                        "• Pose Estimation — human body keypoints\n\n"
                        "Karib's CV research: traffic detection, precision agriculture, "
                        "medical imaging (CT, X-ray, histopathology), surgical instrument detection."),

    "nlp": ("💬 Natural Language Processing (NLP):\n\n"
            "NLP enables machines to understand and generate human language.\n\n"
            "Key tasks:\n"
            "• Text Classification — spam, sentiment, intent\n"
            "• Named Entity Recognition (NER)\n"
            "• Machine Translation\n"
            "• Question Answering / RAG\n"
            "• Text Generation — LLMs\n"
            "• Sentiment / Emotion Detection\n\n"
            "Karib's NLP: Bangla-English code-mixed emotion detection "
            "(Best Paper Award, AII 2025)."),

    "yolo": ("🎯 YOLO — You Only Look Once:\n\n"
             "Real-time object detection algorithm that processes the entire image once.\n\n"
             "How it works:\n"
             "• Divides image into S×S grid\n"
             "• Each cell predicts bounding boxes + confidence + class probabilities\n"
             "• Single forward pass — extremely fast\n\n"
             "Versions: YOLOv5, YOLOv7, YOLOv8, YOLOv9, YOLOv10\n\n"
             "Karib used YOLO for:\n"
             "• Vehicle detection on Bangladeshi roads (TFP-BD dataset)\n"
             "• Surgical instrument detection (occlusion-resilient, IEEE BIBE 2025)"),

    "llm": ("🤖 Large Language Models (LLMs):\n\n"
            "LLMs are transformer-based models trained on massive text datasets.\n\n"
            "Examples: GPT-4, Claude, Gemini, LLaMA, Mistral, Falcon\n\n"
            "Capabilities:\n"
            "• Text generation and completion\n"
            "• Question answering\n"
            "• Code generation\n"
            "• Summarisation and translation\n"
            "• Reasoning and analysis\n\n"
            "Key concepts: Pre-training, Fine-tuning, RLHF, Prompt Engineering\n\n"
            "Karib integrates LLMs in EmoThrive, EduGPT, and enterprise RAG systems."),

    "n8n": ("⚙️ n8n — Workflow Automation:\n\n"
            "n8n is an open-source workflow automation tool (self-hostable, free).\n\n"
            "Features:\n"
            "• Visual node-based workflow builder\n"
            "• 400+ integrations (APIs, databases, AI services)\n"
            "• Webhook triggers and HTTP requests\n"
            "• Custom JavaScript/Python code nodes\n"
            "• Self-hosted = full data control\n\n"
            "Karib's n8n projects:\n"
            "• AI Video Generation Pipeline (n8n + Runway ML)\n"
            "• Form-triggered LLM processing\n"
            "• Automated email responses with AI"),

    "semi_supervised": ("📊 Semi-Supervised Learning:\n\n"
                        "Uses a small amount of labeled data + large amount of unlabeled data.\n\n"
                        "Why it matters: Labeling data is expensive and time-consuming.\n\n"
                        "Techniques:\n"
                        "• Pseudo-labeling — use model predictions as labels\n"
                        "• Consistency regularization — stable predictions under perturbations\n"
                        "• MixMatch, FixMatch, FlexMatch\n"
                        "• Mean Teacher — ensemble of model weights\n\n"
                        "Karib's semi-supervised publications:\n"
                        "• Kidney CT scan classification (Swin Transformer, IEEE SPICSCON)\n"
                        "• Bone metastases detection (IEEE BIBE 2025)\n"
                        "• Sunflower detection (Smart Agricultural Technology)"),

    "self_supervised": ("🔄 Self-Supervised Learning:\n\n"
                        "Generates supervisory signals from the data itself — no human labels!\n\n"
                        "Techniques:\n"
                        "• Contrastive Learning (SimCLR, MoCo) — similar samples close, dissimilar far\n"
                        "• Masked Autoencoders (MAE) — predict masked parts of input\n"
                        "• BYOL, DINO — vision self-supervised frameworks\n"
                        "• GPT-style — predict next token\n\n"
                        "Karib's SSL publications:\n"
                        "• Sunflower & rice panicle detection (precision agriculture)\n"
                        "• Surgical instrument detection with YOLO (IEEE BIBE 2025)"),

    "xgboost": ("📈 XGBoost — Extreme Gradient Boosting:\n\n"
                "Powerful ensemble algorithm using gradient boosted decision trees.\n\n"
                "Advantages:\n"
                "• Handles missing data automatically\n"
                "• Built-in L1/L2 regularisation\n"
                "• Extremely fast and scalable\n"
                "• Excellent on tabular/structured data\n"
                "• Feature importance natively\n\n"
                "Karib used XGBoost + SHAP for interpretable illness classification "
                "from drug attributes (IEEE QPAIN 2025)."),

    "data_science": ("📊 Data Science:\n\n"
                     "Data Science extracts knowledge and insights from structured and unstructured data.\n\n"
                     "Workflow:\n"
                     "1. Data Collection & Understanding\n"
                     "2. Data Cleaning & Preprocessing\n"
                     "3. Exploratory Data Analysis (EDA)\n"
                     "4. Feature Engineering\n"
                     "5. Model Building & Evaluation\n"
                     "6. Deployment & Monitoring\n\n"
                     "Karib specialises in Data Science — MSc degree, team leader, and "
                     "multiple published datasets (TFP-BD, BDFlower, Vegetable detection)."),

    "cnn": ("🖼️ Convolutional Neural Networks (CNNs):\n\n"
            "Designed for grid-like data (images, audio spectrograms).\n\n"
            "Key layers:\n"
            "• Convolutional — learn local patterns (edges, textures)\n"
            "• Pooling — reduce spatial dimensions\n"
            "• Batch Normalisation — stabilise training\n"
            "• Fully Connected — final classification\n\n"
            "Architectures: ResNet, VGG, EfficientNet, MobileNet, InceptionNet\n\n"
            "Karib uses CNNs extensively in medical imaging and agricultural vision research."),

    "swin_transformer": ("🪟 Swin Transformer:\n\n"
                         "Hierarchical vision transformer using shifted window attention.\n\n"
                         "Advantages over standard ViT:\n"
                         "• Linear computational complexity (vs quadratic)\n"
                         "• Hierarchical feature maps like CNNs\n"
                         "• Better for dense prediction (detection, segmentation)\n"
                         "• Shifted windows enable cross-window connections\n\n"
                         "Karib used Swin Transformer for kidney CT scan classification "
                         "in supervised + semi-supervised frameworks (IEEE SPICSCON 2025)."),

    "embedding": ("🔢 Embeddings — Vector Representations:\n\n"
                  "Dense vectors that represent discrete objects (words, images, users).\n\n"
                  "Properties: Similar objects have similar vectors.\n\n"
                  "Types:\n"
                  "• Word: Word2Vec, GloVe, FastText\n"
                  "• Contextual: BERT, GPT (context-dependent)\n"
                  "• Image: CNN features, CLIP\n"
                  "• Sentence: Sentence-BERT, E5\n\n"
                  "Karib uses embeddings in RAG systems for semantic search "
                  "— finding relevant documents by meaning, not just keywords."),

    "medical_imaging": ("🏥 Medical Imaging AI:\n\n"
                        "Deep learning applied to healthcare images:\n\n"
                        "Karib's medical AI publications:\n"
                        "• TB Diagnosis from Chest X-Ray (IEEE ICAECT 2025)\n"
                        "• Kidney CT Classification with Swin Transformer (IEEE SPICSCON 2025)\n"
                        "• Small Cell Lung Cancer Histopathology (ICDMIS 2024, Springer)\n"
                        "• Bone Metastases Detection — Breast Cancer (IEEE BIBE 2025)\n"
                        "• Multimodal CT + MRI Classification (ICCIT 2025)\n"
                        "• Surgical Instrument Detection (IEEE BIBE 2025)\n\n"
                        "Models used: U-Net, ResNet, Swin Transformer, YOLO"),

    "precision_agriculture": ("🌾 Precision Agriculture AI:\n\n"
                               "AI applied to farming to optimise yield and efficiency.\n\n"
                               "Karib's AgriAI publications:\n"
                               "• Sunflower Detection — Semi/Self-Supervised (Smart Agricultural Technology, 2 citations)\n"
                               "• BDFlower Dataset — Growth Stage Classification (Data in Brief 2026)\n"
                               "• Flower Classification with CNN+Transformer+GCN (Scientific Reports 2026)\n"
                               "• Oyster Mushroom Monitoring with ShuffleNet+XAI (Smart Agricultural Technology)\n"
                               "• Vegetable Object Detection Dataset (Data in Brief 2025)\n"
                               "• Rice Panicle Detection — Self-Supervised Learning"),

    "python": ("🐍 Python for AI/ML:\n\n"
               "Python is the dominant language for AI and data science.\n\n"
               "Key libraries:\n"
               "• NumPy, Pandas — data manipulation\n"
               "• Matplotlib, Seaborn, Plotly — visualisation\n"
               "• Scikit-learn — classical ML\n"
               "• PyTorch, TensorFlow/Keras — deep learning\n"
               "• HuggingFace Transformers — NLP/LLM\n"
               "• OpenCV, Pillow — computer vision\n"
               "• LangChain, LlamaIndex — RAG/LLM frameworks\n"
               "• FastAPI, Django — web backend\n\n"
               "Karib uses Python as his primary language."),

    "django": ("🌐 Django Web Framework:\n\n"
               "High-level Python web framework for rapid, clean development.\n\n"
               "Features:\n"
               "• MTV architecture (Model-Template-View)\n"
               "• Built-in ORM for database operations\n"
               "• Admin panel out of the box\n"
               "• URL routing, authentication, forms\n"
               "• CSRF protection, middleware\n"
               "• Excellent for REST APIs\n\n"
               "This very portfolio is built with Django!\n"
               "Karib uses Django as his go-to backend framework."),

    "generative_ai": ("🎨 Generative AI:\n\n"
                      "AI that creates new content — text, images, audio, video.\n\n"
                      "Models:\n"
                      "• LLMs (GPT, Claude, Gemini) — text generation\n"
                      "• Diffusion Models (Stable Diffusion, DALL-E, Midjourney) — images\n"
                      "• Runway ML, Sora — AI video generation\n"
                      "• GAN — generative adversarial networks\n"
                      "• VAE — variational autoencoders\n"
                      "• MusicGen, AudioCraft — AI music/audio\n\n"
                      "Karib built an n8n + Runway ML AI video generation pipeline."),

    "knowledge_graph": ("🕸️ Knowledge Graphs:\n\n"
                        "Represent knowledge as entities (nodes) and relationships (edges).\n\n"
                        "Structure: (Entity) --[Relationship]--> (Entity)\n"
                        "Example: (Karib) --[published]--> (CodeMixEcom-Emotion paper)\n\n"
                        "Applications:\n"
                        "• Question answering with structured knowledge\n"
                        "• Entity disambiguation\n"
                        "• Drug interaction analysis\n"
                        "• Recommendation systems\n"
                        "• Fraud detection\n\n"
                        "Karib works with knowledge graphs in his AI research at EWU."),

    "sentiment": ("😊 Sentiment & Emotion Analysis:\n\n"
                  "Determines emotional tone from text.\n\n"
                  "Levels:\n"
                  "• Document-level — overall sentiment\n"
                  "• Sentence-level — per sentence\n"
                  "• Aspect-based — sentiment toward specific aspects\n"
                  "• Emotion detection — joy, anger, fear, sadness, surprise, disgust\n\n"
                  "Approaches: BERT, RoBERTa, Transformer fine-tuning\n\n"
                  "Karib's research: Bangla-English code-mixed emotion detection "
                  "on e-commerce reviews — 🏆 Best Paper Award AII 2025!"),

    "ocr": ("📄 OCR — Optical Character Recognition:\n\n"
            "Converts images of text into machine-readable text.\n\n"
            "Modern approaches:\n"
            "• CRNN — CNN + RNN for sequence recognition\n"
            "• Tesseract — classic open-source OCR engine\n"
            "• PaddleOCR — state-of-the-art multilingual OCR\n"
            "• EasyOCR — easy-to-use deep learning OCR\n"
            "• TrOCR — transformer-based OCR (Microsoft)\n\n"
            "Karib built an OCR text extraction system:\n"
            "github.com/karibshams/simple_ocr"),

    "attention": ("🎯 Attention Mechanism:\n\n"
                  "Allows models to focus on the most relevant parts of input.\n\n"
                  "Math: Attention(Q,K,V) = softmax(QK^T / √dk) × V\n\n"
                  "Types:\n"
                  "• Self-attention — input attends to itself\n"
                  "• Cross-attention — decoder attends to encoder output\n"
                  "• Multi-head — multiple attention heads in parallel\n"
                  "• Sparse attention — efficient for long sequences\n"
                  "• Flash Attention — memory-efficient implementation\n\n"
                  "Powers every modern transformer and LLM."),

    "random_forest": ("🌳 Random Forest:\n\n"
                      "Ensemble of decision trees using bagging (Bootstrap Aggregating).\n\n"
                      "How it works:\n"
                      "• Train N trees on random subsets of data and features\n"
                      "• Final prediction = majority vote (classification) or average (regression)\n\n"
                      "Advantages:\n"
                      "• Robust to overfitting\n"
                      "• Handles missing values\n"
                      "• Provides feature importance\n"
                      "• Works on both classification and regression\n\n"
                      "Karib used Random Forest + XAI for indoor air quality prediction at airports (IEEE QPAIN 2025)."),

    "fallback": ("🤖 I can answer questions about:\n\n"
                 "👤 About Karib: who, contact, award, education, experience, skills, projects, team, publications\n\n"
                 "🧠 AI/ML Concepts: RAG, transformers, deep learning, NLP, computer vision, XAI, "
                 "YOLO, CNN, LLM, n8n, OCR, embeddings, semi-supervised, self-supervised, XGBoost, "
                 "attention, random forest, sentiment analysis, knowledge graphs, medical imaging, "
                 "precision agriculture, generative AI, Python, Django\n\n"
                 "Try: 'What is Karib's best paper award?' or 'Explain RAG in AI'"),
}


def _respond(msg: str) -> str:
    """Free AI engine — pure Python regex matching, zero API cost."""
    m = msg.lower().strip()
    m = re.sub(r'[^\w\s]', ' ', m)

    # Greeting
    if re.search(r'\b(hi|hello|hey|greetings|good morning|good evening|salaam|salam|assalam)\b', m):
        return KB["greeting"]

    # Thanks
    if re.search(r'\b(thanks|thank you|thx|ty|appreciate|jazakallah)\b', m):
        return "You're welcome! 😊 Feel free to ask anything else about Karib's work or any AI/ML concept."

    # Award — check early so it takes priority
    if re.search(r'\b(award|best paper|washington|dc|prize|won|recognition|ewu achievement|conference award|aii 2025)\b', m):
        return KB["award"]

    # Who is Karib
    if re.search(r'\b(who is karib|about karib|tell me about|introduce|karib shams|background)\b', m) or (('karib' in m or 'you' in m) and re.search(r'\b(who|what|tell|describe)\b', m)):
        return KB["who"]

    # Contact
    if re.search(r'\b(contact|email|phone|whatsapp|reach|hire|location|address|number)\b', m):
        return KB["contact"]

    # Publications
    if re.search(r'\b(publication|paper|research|journal|ieee|springer|published|article|conference|citation|h.index|scholar|google scholar)\b', m):
        return KB["publications"]

    # Education
    if re.search(r'\b(education|degree|university|cgpa|gpa|msc|bsc|hsc|ssc|study|studied|academic|college)\b', m):
        return KB["education"]

    # Experience / Work
    if re.search(r'\b(experience|job|work|company|jvai|betopia|teaching|assistant|career|employed)\b', m):
        return KB["experience"]

    # Skills
    if re.search(r'\b(skill|technology|tech stack|tool|proficient|capable|framework|language|know)\b', m):
        return KB["skills"]

    # Team
    if re.search(r'\b(team|ai stream|stream|60\+?|figma|drive|delivered|portfolio team|leading)\b', m):
        return KB["team"]

    # Projects
    if re.search(r'\b(project|built|created|developed|emothrive|edugpt|voicemind|mystudybuddy|ocr system|n8n pipeline|rag system)\b', m):
        return KB["projects"]

    # Swin Transformer (before general transformer)
    if re.search(r'\b(swin|swin transformer|shifted window)\b', m):
        return KB["swin_transformer"]

    # Transformer
    if re.search(r'\b(transformer|attention mechanism|self.attention|bert|vit|vision transformer|gpt architecture)\b', m):
        return KB["transformer"]

    # RAG
    if re.search(r'\b(rag|retrieval.augmented|retrieval augmented|knowledge retrieval|grounding)\b', m):
        return KB["rag"]

    # LLM
    if re.search(r'\b(llm|large language model|gpt|chatgpt|gemini|llama|mistral|claude|language model)\b', m):
        return KB["llm"]

    # XAI / SHAP
    if re.search(r'\b(xai|explainable ai|shap|lime|grad.cam|interpret|feature importance|shapley)\b', m):
        return KB["xai"]

    # Deep Learning
    if re.search(r'\b(deep learning|neural net|backprop|gradient descent|epoch|batch size|loss function|activation)\b', m):
        return KB["deep_learning"]

    # Machine Learning
    if re.search(r'\b(machine learning|ml model|supervised learning|unsupervised|reinforcement learning|ml algorithm)\b', m):
        return KB["machine_learning"]

    # CNN
    if re.search(r'\b(cnn|convolutional neural|resnet|efficientnet|mobilenet|vgg|inception)\b', m):
        return KB["cnn"]

    # YOLO
    if re.search(r'\b(yolo|you only look once|object detection|bounding box|faster rcnn|detection model)\b', m):
        return KB["yolo"]

    # XGBoost
    if re.search(r'\b(xgboost|gradient boost|boosting|gbm|lightgbm|catboost)\b', m):
        return KB["xgboost"]

    # Random Forest
    if re.search(r'\b(random forest|bagging|decision tree|ensemble method)\b', m):
        return KB["random_forest"]

    # NLP
    if re.search(r'\b(nlp|natural language processing|text classification|named entity|ner|machine translation)\b', m):
        return KB["nlp"]

    # Sentiment / Emotion
    if re.search(r'\b(sentiment|emotion detection|opinion mining|bangla|code.mix|codemix)\b', m):
        return KB["sentiment"]

    # Computer Vision
    if re.search(r'\b(computer vision|image recognition|image classification|segmentation|visual ai|image processing)\b', m):
        return KB["computer_vision"]

    # Semi-supervised
    if re.search(r'\b(semi.supervised|pseudo.label|fixmatch|mixmatch|mean teacher)\b', m):
        return KB["semi_supervised"]

    # Self-supervised
    if re.search(r'\b(self.supervised|contrastive learning|simclr|byol|dino|masked autoencoder|mae)\b', m):
        return KB["self_supervised"]

    # n8n
    if re.search(r'\b(n8n|workflow automation|no.code automation|zapier|make\.com|automation tool)\b', m):
        return KB["n8n"]

    # OCR
    if re.search(r'\b(ocr|optical character recognition|text extraction|tesseract|paddleocr|easyocr)\b', m):
        return KB["ocr"]

    # Embeddings
    if re.search(r'\b(embedding|vector representation|word2vec|glove|fasttext|semantic search|vector store)\b', m):
        return KB["embedding"]

    # Attention
    if re.search(r'\b(attention|multi.head attention|query key value|positional encoding|flash attention)\b', m):
        return KB["attention"]

    # Data Science
    if re.search(r'\b(data science|data scientist|eda|exploratory data|feature engineering|data analysis|pandas|numpy)\b', m):
        return KB["data_science"]

    # Python
    if re.search(r'\b(python|pytorch|tensorflow|scikit.learn|keras|huggingface|langchain)\b', m):
        return KB["python"]

    # Django
    if re.search(r'\b(django|flask|fastapi|web framework|backend framework|web development)\b', m):
        return KB["django"]

    # Generative AI
    if re.search(r'\b(generative ai|gan|diffusion model|stable diffusion|dall.e|midjourney|image generation|video generation|runway)\b', m):
        return KB["generative_ai"]

    # Medical Imaging
    if re.search(r'\b(medical imaging|xray|x.ray|ct scan|mri|histopathology|cancer|tuberculosis|lung|kidney|bone metastases|radiology)\b', m):
        return KB["medical_imaging"]

    # Precision Agriculture
    if re.search(r'\b(agriculture|crop|sunflower|rice panicle|flower detection|mushroom|farm|plant detection|bdflower)\b', m):
        return KB["precision_agriculture"]

    # Knowledge Graph
    if re.search(r'\b(knowledge graph|ontology|entity relationship|neo4j|triplet|graph database)\b', m):
        return KB["knowledge_graph"]

    # Generic AI question
    if re.search(r'\b(artificial intelligence|what is ai|ai field|ai overview|explain ai)\b', m):
        return ("🤖 Artificial Intelligence (AI) is the simulation of human intelligence by machines.\n\n"
                "Main subfields:\n"
                "• Machine Learning — learning from data\n"
                "• Deep Learning — multi-layer neural networks\n"
                "• Computer Vision — understanding images\n"
                "• NLP — understanding language\n"
                "• Robotics — physical AI agents\n"
                "• Generative AI — creating new content\n\n"
                f"Karib Shams is a leading AI practitioner with 16 publications, "
                "9 citations, Best Paper Award at AII 2025 (Washington D.C.), and leads "
                "AI Stream — a team with 60+ delivered AI projects. Ask me anything specific!")

    return KB["fallback"]


# ══════════════════════════════════════════════════════════════════
#  VIEWS
# ══════════════════════════════════════════════════════════════════

def index(request):
    feedbacks = Feedback.objects.order_by('-created_at')[:8]
    pub_count = len(DATA["publications"])

    # Track visitor
    try:
        today = timezone.now().date()
        visitor, _ = VisitorCount.objects.get_or_create(date=today)
        if not request.session.get(f'visited_{today}'):
            visitor.count += 1
            visitor.save()
            request.session[f'visited_{today}'] = True
        total_visitors = VisitorCount.objects.aggregate(total=Sum('count'))['total'] or 0
        today_visitors = visitor.count
    except Exception:
        total_visitors = 0
        today_visitors = 0

    return render(request, 'portfolio/index.html', {
        'data': DATA,
        'pub_count': pub_count,
        'feedbacks': feedbacks,
        'total_visitors': total_visitors,
        'today_visitors': today_visitors,
    })


@csrf_exempt
def ai_chat(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    try:
        body = json.loads(request.body)
        user_msg = body.get('message', '').strip()
        if not user_msg:
            return JsonResponse({'reply': 'Please type a message!'})
        reply = _respond(user_msg)
        ChatLog.objects.create(user_message=user_msg, ai_reply=reply)
        return JsonResponse({'reply': reply})
    except Exception:
        return JsonResponse({'reply': 'Something went wrong. Please try again.'})


@csrf_exempt
def submit_feedback(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)
    try:
        body     = json.loads(request.body)
        name     = body.get('name', '').strip()
        email    = body.get('email', '').strip()
        message  = body.get('message', '').strip()

        # Basic validation
        import re
        if not name:
            return JsonResponse({'status': 'error', 'msg': 'Please enter your name.'}, status=400)
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            return JsonResponse({'status': 'error', 'msg': 'Please enter a valid email address.'}, status=400)
        if len(message) < 10:
            return JsonResponse({'status': 'error', 'msg': 'Message must be at least 10 characters.'}, status=400)

        # Save to database
        Feedback.objects.create(name=name, email=email, message=message)

        # Send email notification to Karib
        try:
            send_mail(
                subject=f'New Portfolio Feedback from {name}',
                message=f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
                from_email='noreply@karibportfolio.com',
                recipient_list=['shams321karib@gmail.com'],
                fail_silently=True,
            )
        except Exception:
            pass  # Email fails silently — feedback still saved

        return JsonResponse({'status': 'ok', 'msg': 'Thank you! Your message has been received. Karib will get back to you soon.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'msg': 'Something went wrong. Please try again.'}, status=400)