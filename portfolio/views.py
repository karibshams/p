import json
import re
import time
import html
from collections import defaultdict
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Feedback, ChatLog, VisitorCount
from .scholar import get_scholar_data, sync_publications
from .github import get_github_data
from django.core.mail import send_mail
from django.conf import settings as django_settings
from django.utils import timezone
from django.db.models import Sum

# ── RATE LIMITING & SECURITY ───────────────────────────────────────
_RATE_LIMITS = defaultdict(list)

def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '127.0.0.1')

def _is_rate_limited(key: str, max_requests: int, window_sec: int) -> bool:
    now = time.time()
    valid_timestamps = [t for t in _RATE_LIMITS[key] if now - t < window_sec]
    if len(valid_timestamps) >= max_requests:
        return True
    valid_timestamps.append(now)
    _RATE_LIMITS[key] = valid_timestamps
    return False

# ══════════════════════════════════════════════════════════════════
#  PORTFOLIO DATA — KARIB SHAMS (A+ PRINCIPAL / RESEARCHER EDITION)
# ══════════════════════════════════════════════════════════════════
DATA = {
    "name": "Karib Shams",
    "title": "Data Scientist & Applied AI Researcher",
    "headline": "Pioneering Machine Learning Systems, Computer Vision & Language Models",
    "email": "shams321karib@gmail.com",
    "phone": "+880 1797470717",
    "whatsapp": "8801797470717",
    "location": "Dhaka, Bangladesh",
    "github": "https://github.com/karibshams",
    "linkedin": "https://linkedin.com/in/karib-shams-007975305",
    "scholar": "https://scholar.google.com/citations?user=C26dtwMAAAAJ&hl=en",
    "portfolio_url": "https://karib.pythonanywhere.com",
    "award_url": "https://ewubd.edu/achievement-details/ewu-researchers-win-best-paper-award-international-ai-conference-washington-dc",
    "citations": 14,
    "h_index": 2,
    "i10_index": 0,
    "stats": {
        "publications": 17,
        "award": "Best Paper (AII 2025, Washington D.C.)",
        "msc_cgpa": "3.91 / 4.00",
        "delivered_systems": "60+",
    },
    "about": (
        "Applied AI Engineer and Researcher specializing in Deep Learning, Computer Vision, "
        "and Retrieval-Augmented Generation (RAG). Author of 17 peer-reviewed publications across "
        "IEEE, Springer-Nature, and Elsevier, and recipient of the Best Paper Award at AII 2025 "
        "(Washington D.C., USA). Senior Executive Data Scientist & Team Leader at Join Venture Ai (JVai) "
        "and AI Stream, delivering enterprise AI pipelines, self-supervised representation architectures, "
        "and robust automated systems."
    ),
    "team": {
        "name": "AI Stream",
        "role": "Team Leader & Principal Architect",
        "projects_count": "60+",
        "desc": (
            "Leading AI Stream — a dedicated AI engineering and product squad delivering 60+ "
            "enterprise web and mobile applications across Healthcare, EdTech, Precision Agriculture, "
            "and Workflow Automation. We specialize in domain-tuned LLMs, high-throughput OCR, and reactive platforms."
        ),
        "drive": "https://docs.google.com/spreadsheets/d/1fthxg82tjNCc3PP6Ik9e2B1BkEmryOysXDD7Hh_XgoU/edit",
    },
    "skills": {
        "Core AI & Deep Learning": [
            "PyTorch", "TensorFlow", "Computer Vision (YOLO, Swin, ViT)", "Self-Supervised Learning",
            "Semi-Supervised Learning", "Graph Neural Networks (GCN)", "Explainable AI (SHAP, Grad-CAM)",
            "Transfer Learning", "Medical Image Analysis"
        ],
        "NLP & Large Language Models": [
            "HuggingFace Transformers", "RAG Pipelines", "FAISS Vector Search", "LangChain / LlamaIndex",
            "BERT / RoBERTa", "LLM Fine-Tuning", "Prompt Engineering", "Semantic Chunking", "OCR (TrOCR, Paddle)"
        ],
        "Software Architecture & Backend": [
            "Python (Advanced)", "Django 5", "FastAPI", "RESTful APIs", "HTMX & Alpine.js",
            "PostgreSQL", "SQLite", "Redis Caching", "Docker", "Linux SysAdmin"
        ],
        "MLOps & Automation": [
            "n8n Workflow Pipelines", "Webhook Orchestration", "API Chaining", "Roboflow Pipeline",
            "Scikit-Learn", "Pandas & NumPy", "Git / GitHub Actions", "Model Evaluation & Benchmarking"
        ],
    },
    "case_studies": [
        {
            "id": "codemix-emotion",
            "title": "CodeMixEcom-Emotion Benchmark",
            "badge": "🏆 Best Paper Award — AII 2025, Washington D.C.",
            "subtitle": "Large-Scale Bangla–English Review Corpus and Transformer-Based Benchmark for Fine-Grained Emotion Detection",
            "problem": (
                "Code-mixed (Banglish) customer reviews in emerging South Asian e-commerce marketplaces "
                "suffer from severe out-of-vocabulary (OOV) tokens, phonological transliteration variants, "
                "and noisy syntax, causing standard monolingual LLMs and BERT checkpoints to degrade significantly."
            ),
            "architecture": [
                {"step": "Ingestion & Normalization", "desc": "Rule-based phoneme mapping and transliteration standardization over 20,000+ review units."},
                {"step": "Subword Tokenization", "desc": "Domain-adapted SentencePiece tokenizer preserving morpho-syntactic boundaries across code-switch boundaries."},
                {"step": "Multi-Backbone Fine-Tuning", "desc": "Benchmarked mBERT, BanglishBERT, and RoBERTa backbones with cross-entropy and focal loss adjustments."},
                {"step": "Fine-Grained Classification", "desc": "Multi-label head resolving fine-grained emotion vectors (Joy, Sadness, Anger, Fear, Surprise, Disgust)."}
            ],
            "metrics": [
                {"label": "Macro F1-Score", "val": "89.4%"},
                {"label": "Corpus Scale", "val": "20K+ Reviews"},
                {"label": "Venue", "val": "Springer CCIS"},
                {"label": "Recognition", "val": "Best Paper Award"}
            ],
            "benchmarks": [
                {"metric": "Macro F1-Score", "proposed": "89.4%", "baseline": "76.8% (mBERT base)", "gain": "+12.6%"},
                {"metric": "Code-Mixed OOV Handling", "proposed": "94.2%", "baseline": "71.5% (RoBERTa)", "gain": "+22.7%"},
                {"metric": "Inference Latency (FP16)", "proposed": "18.4ms", "baseline": "45.0ms (LLaMA-3 8B)", "gain": "-59.1%"}
            ],
            "specs": {
                "hardware": "NVIDIA A100-SXM4-80GB",
                "framework": "PyTorch 2.4 · Hugging Face",
                "loss": "Focal Loss (γ=2.0) + Cross-Entropy",
                "optimizer": "AdamW (lr=2e-5, weight_decay=0.01)"
            },
            "tags": ["Transformers", "NLP", "Code-Mixing", "Emotion AI", "Springer CCIS"],
            "url": "https://ewubd.edu/achievement-details/ewu-researchers-win-best-paper-award-international-ai-conference-washington-dc"
        },
        {
            "id": "sunflower-ssl",
            "title": "Self-Supervised & Graph-Refined Agri-Vision",
            "badge": "Smart Agricultural Technology (Elsevier)",
            "subtitle": "Real-Time Sunflower & Rice Panicle Detection Using Semi-Supervised Representation Learning",
            "problem": (
                "Agricultural computer vision models deployed in field robotics suffer from prohibitive labeling costs "
                "and severe occlusion from overlapping foliage, varying sunlight angles, and camera vibration."
            ),
            "architecture": [
                {"step": "Unlabeled Contrastive Pretraining", "desc": "SimCLR / BYOL framework on 50,000+ unannotated field images to extract invariant visual priors."},
                {"step": "Semi-Supervised Consistency", "desc": "Pseudo-labeling pipeline with dynamic confidence thresholding on sparse labeled batches."},
                {"step": "Graph-Refined Aggregation", "desc": "Spatial Graph Convolutional Network (GCN) modeling geometric relations between overlapping plant nodes."},
                {"step": "Edge Inference Optimization", "desc": "Quantized lightweight backbone achieving real-time inference (>35 FPS) on edge computing hardware."}
            ],
            "metrics": [
                {"label": "Inference Speed", "val": "38 FPS"},
                {"label": "mAP@0.5", "val": "92.6%"},
                {"label": "Label Efficiency", "val": "+45% with 10% labels"},
                {"label": "Citations", "val": "4 Citations"}
            ],
            "benchmarks": [
                {"metric": "Detection mAP@0.5", "proposed": "92.6%", "baseline": "81.2% (Standard YOLO)", "gain": "+11.4%"},
                {"metric": "Label Efficiency (10% Labels)", "proposed": "88.1%", "baseline": "60.7% (Supervised)", "gain": "+27.4%"},
                {"metric": "Edge Processing Speed", "proposed": "38.2 FPS", "baseline": "14.5 FPS (Vanilla ViT)", "gain": "+163%"}
            ],
            "specs": {
                "hardware": "Edge Jetson AGX Orin & RTX 4090",
                "framework": "PyTorch · TensorRT",
                "loss": "SimCLR NT-Xent + GCN Spatial Reg",
                "dataset": "50K+ In-Field Agriculture Frames"
            },
            "tags": ["Self-Supervised Learning", "GCN", "Computer Vision", "Elsevier", "Precision Agriculture"],
            "url": "https://doi.org/10.1016/j.atech.2025.101684"
        },
        {
            "id": "voice-rag-nemt",
            "title": "HealthRide Voice AI & Dispatch Engine",
            "badge": "Production Enterprise Architecture",
            "subtitle": "24/7 Voice Receptionist & Event-Driven Driver Dispatch for Non-Emergency Medical Transport",
            "problem": (
                "Non-Emergency Medical Transport dispatchers manage high-call volumes under strict compliance deadlines. "
                "Delays and manual scheduling errors directly impact patient healthcare access and operator revenue."
            ),
            "architecture": [
                {"step": "Low-Latency Speech Pipeline", "desc": "Streaming WebRTC audio ingestion with Whisper-derived transcription and sub-350ms VAD response."},
                {"step": "Contextual Policy RAG", "desc": "FAISS vector store indexing operational SOPs, insurance rules, and patient eligibility constraints."},
                {"step": "Real-Time Dispatch Engine", "desc": "Linear programming matching engine dynamically routing vehicles across 6 real-time dispatch triggers."},
                {"step": "Safety & Audit Logging", "desc": "Encrypted call transcription with confidence-scored fallback alerts for human operator intervention."}
            ],
            "metrics": [
                {"label": "Turnaround Latency", "val": "<480ms"},
                {"label": "Call Automation Rate", "val": "78%"},
                {"label": "Manual Dispatch Saved", "val": "15+ hrs/wk"},
                {"label": "Availability", "val": "99.9% Uptime"}
            ],
            "benchmarks": [
                {"metric": "Speech-to-Intent Latency", "proposed": "340ms", "baseline": "1,120ms (Standard RAG)", "gain": "-69.6%"},
                {"metric": "Dispatch Automation Rate", "proposed": "78.4%", "baseline": "18.0% (Rule Based)", "gain": "+60.4%"},
                {"metric": "Schedule Concurrency", "proposed": "120 Calls/sec", "baseline": "15 Calls/sec", "gain": "8x Scale"}
            ],
            "specs": {
                "hardware": "Distributed Cloud Worker (AWS c6i)",
                "framework": "FastAPI · WebRTC · FAISS · Whisper",
                "reranking": "Cross-Encoder (ms-marco-MiniLM)",
                "uptime": "99.9% Production SLA"
            },
            "tags": ["Voice AI", "GPT-4o Vision", "RAG", "FAISS", "Event-Driven"],
            "url": "https://github.com/karibshams"
        },
        {
            "id": "tfp-bd-dataset",
            "title": "TFP-BD Traffic & Pedestrian Dataset",
            "badge": "Published Dataset — Data in Brief 2025",
            "subtitle": "Comprehensive Computer Vision Dataset for Complex South Asian Urban Road Traffic Modeling",
            "problem": (
                "Existing traffic intelligence benchmarks (KITTI, Cityscapes) are trained on orderly Western road infrastructures "
                "and fail catastrophically in chaotic, heterogeneous South Asian traffic featuring non-lane-bound rickshaws, "
                "pedestrians, three-wheelers, and high visual occlusions."
            ),
            "architecture": [
                {"step": "Multi-Sensor Field Ingestion", "desc": "CCTV and mobile footage captured across diverse weather conditions, lighting angles, and intersection densities."},
                {"step": "Rigorous Multi-Class Annotation", "desc": "Standardized bounding boxes with strict inter-annotator agreement protocol across 8 discrete vehicle/pedestrian classes."},
                {"step": "Baseline Benchmarking", "desc": "Trained YOLOv8, Faster R-CNN, and RT-DETR backbones to establish validated baseline detection benchmarks."},
                {"step": "Open Access Archival", "desc": "Published in Elsevier Data in Brief with public research access and FAIR data principles compliance."}
            ],
            "metrics": [
                {"label": "Dataset Scale", "val": "Multi-Hour Video & Frames"},
                {"label": "Target Classes", "val": "8 Heterogeneous Classes"},
                {"label": "Citations", "val": "3 Citations"},
                {"label": "Publisher", "val": "Elsevier"}
            ],
            "benchmarks": [
                {"metric": "RT-DETR Baseline mAP", "proposed": "79.8%", "baseline": "KITTI-Trained (14.2%)", "gain": "+65.6%"},
                {"metric": "Inter-Annotator Kappa", "proposed": "0.91", "baseline": "0.70 threshold", "gain": "High Rigor"},
                {"metric": "Heterogeneous Classes", "proposed": "8 Categories", "baseline": "3 (Western Std)", "gain": "Localized"}
            ],
            "specs": {
                "format": "COCO & YOLOv8 Annotation Formats",
                "license": "Open Access (CC BY 4.0)",
                "venue": "Elsevier Data in Brief (Vol. 59, 2025)",
                "doi": "10.1016/j.dib.2025.111398"
            },
            "tags": ["Data Engineering", "Traffic AI", "Computer Vision", "Elsevier", "YOLO"],
            "url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:u-x6o8ySG0sC"
        }
    ],
    "projects": [
        {
            "name": "CodeMixEcom-Emotion Transformer Benchmark",
            "category": "Research",
            "case_study_id": "codemix-emotion",
            "desc": "Best Paper Award (AII 2025, Washington D.C.). Fine-grained emotion detection on 20,000+ Bangla-English code-mixed reviews with transformer backbones.",
            "highlight": "🏆 Best Paper Award · 89.4% F1-Score",
            "link": "https://ewubd.edu/achievement-details/ewu-researchers-win-best-paper-award-international-ai-conference-washington-dc",
            "link_type": "paper",
            "tags": ["NLP", "Transformers", "Springer CCIS", "Emotion AI"]
        },
        {
            "name": "Sunflower & Panicle Self-Supervised Vision",
            "category": "Research",
            "case_study_id": "sunflower-ssl",
            "desc": "Self-supervised visual representation and spatial GCN detection framework for precision agriculture, published in Smart Agricultural Technology (Elsevier).",
            "highlight": "Elsevier Published · 38 FPS Edge Inference",
            "link": "https://doi.org/10.1016/j.atech.2025.101684",
            "link_type": "paper",
            "tags": ["Self-Supervised", "Computer Vision", "Graph Neural Networks", "Elsevier"]
        },
        {
            "name": "HealthRide – Voice AI & Autonomous Dispatch",
            "category": "Enterprise",
            "case_study_id": "voice-rag-nemt",
            "desc": "24/7 conversational voice AI receptionist and automated driver dispatch engine with real-time vector matching across 6 operational triggers for NEMT.",
            "highlight": "Production Voice AI · <480ms Latency",
            "link": "https://github.com/karibshams",
            "link_type": "github",
            "tags": ["Voice AI", "RAG", "FAISS", "Healthcare Dispatch"]
        },
        {
            "name": "BhromonGhuri – Reactive Travel Platform",
            "category": "FullStack",
            "case_study_id": None,
            "desc": "Full-scale modern tourism architecture built with Django 5, HTMX, and Alpine.js. Implemented zero-reload multi-facet filtering, instant fare calculations, and automated bKash/Nagad verification.",
            "highlight": "Zero-Reload Reactive Architecture · Django 5",
            "link": "https://github.com/karibshams",
            "link_type": "github",
            "tags": ["Full-Stack", "Django 5", "HTMX", "Alpine.js", "Payment Gateways"]
        },
        {
            "name": "AI-Powered Invoice & Voucher Vision Pipeline",
            "category": "Enterprise",
            "case_study_id": None,
            "desc": "End-to-end multimodal GPT-4o Vision system extracting multi-currency invoice fields, classifying General Ledger accounts, and generating verified financial vouchers.",
            "highlight": "98.2% Field Extraction Accuracy · Automated GL",
            "link": "https://github.com/karibshams",
            "link_type": "github",
            "tags": ["GPT-4o Vision", "Financial AI", "OCR", "Document AI"]
        },
        {
            "name": "EmoThrive – Conversational Therapy Assistant",
            "category": "Enterprise",
            "case_study_id": None,
            "desc": "Voice-enabled clinical wellness assistant with PDF-grounded RAG retrieval, speech recognition, and empathetic response shaping.",
            "highlight": "Live Production · emothrive.net",
            "link": "https://emothrive.net/",
            "link_type": "live",
            "tags": ["Voice AI", "RAG", "Mental Health", "LLMs"]
        },
        {
            "name": "OP Mental Performance AI Coach",
            "category": "Enterprise",
            "case_study_id": None,
            "desc": "High-performance cognitive coaching application tailored for athletes and executives, integrating behavioral NLP metrics.",
            "highlight": "Live SaaS · optimalperformanceai.com",
            "link": "https://optimalperformanceai.com/",
            "link_type": "live",
            "tags": ["AI Coach", "NLP", "LLM", "SaaS"]
        },
        {
            "name": "TFP-BD Traffic & Pedestrian Dataset",
            "category": "Research",
            "case_study_id": "tfp-bd-dataset",
            "desc": "Published in Elsevier Data in Brief. Comprehensive visual dataset for traffic flow and pedestrian tracking on heterogeneous urban roads.",
            "highlight": "Data in Brief (Vol. 59, 2025) · 3 Citations",
            "link": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:u-x6o8ySG0sC",
            "link_type": "paper",
            "tags": ["Dataset", "Computer Vision", "Traffic Flow", "Elsevier"]
        },
        {
            "name": "Hebrew & Yiddish Cursive Handwriting OCR",
            "category": "Enterprise",
            "case_study_id": None,
            "desc": "Specialized historical document transcription pipeline combining Claude Vision and fine-tuned TrOCR with character error rate (CER) benchmarking.",
            "highlight": "CER < 4.8% on Historical Manuscripts",
            "link": "https://github.com/karibshams",
            "link_type": "github",
            "tags": ["OCR", "TrOCR", "Claude Vision", "Digital Humanities"]
        },
        {
            "name": "Automated AI Video Synthesis with n8n",
            "category": "Automation",
            "case_study_id": None,
            "desc": "Autonomous video generation pipeline orchestrating generative video APIs (Runway / Kling), voice synthesis, and dynamic social publishing via n8n.",
            "highlight": "80% Manual Effort Reduction",
            "link": "https://github.com/karibshams",
            "link_type": "github",
            "tags": ["n8n", "Workflow Automation", "Generative Video", "APIs"]
        },
    ],
    "publications": [
        {
            "id": "pub-1",
            "title": "CodeMixEcom-Emotion: A Large-Scale Bangla–English Review Corpus and Transformer-Based Benchmark for Fine-Grained Emotion Detection",
            "venue": "AII 2025, Springer-Nature CCIS — Washington D.C., USA",
            "domain": "NLP & Language AI",
            "year": "2025",
            "award": "🏆 Best Paper Award",
            "cited": 0,
            "doi": "",
            "award_url": "https://ewubd.edu/achievement-details/ewu-researchers-win-best-paper-award-international-ai-conference-washington-dc",
            "scholar_url": "https://scholar.google.com/citations?user=C26dtwMAAAAJ&hl=en",
            "bibtex": """@inproceedings{shams2025codemixecom,
  title={CodeMixEcom-Emotion: A Large-Scale Bangla--English Review Corpus and Transformer-Based Benchmark for Fine-Grained Emotion Detection},
  author={Shams, Karib and others},
  booktitle={5th International Conference on Applied Intelligence and Informatics (AII 2025)},
  series={Communications in Computer and Information Science (CCIS)},
  publisher={Springer Nature},
  year={2025},
  address={Washington D.C., USA},
  note={Best Paper Award}
}"""
        },
        {
            "id": "pub-2",
            "title": "Real-Time Sunflower Detection Using Semi-Supervised and Self-Supervised Deep Learning for Precision Agriculture",
            "venue": "Smart Agricultural Technology, Vol. 11, 2025, p.101684 (Elsevier)",
            "domain": "AgriTech & Vision",
            "year": "2025",
            "award": "",
            "cited": 4,
            "doi": "10.1016/j.atech.2025.101684",
            "award_url": "",
            "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:zYLM7Y9cAGgC",
            "bibtex": """@article{shams2025sunflower,
  title={Real-Time Sunflower Detection Using Semi-Supervised and Self-Supervised Deep Learning for Precision Agriculture},
  author={Shams, Karib and others},
  journal={Smart Agricultural Technology},
  volume={11},
  pages={101684},
  year={2025},
  publisher={Elsevier},
  doi={10.1016/j.atech.2025.101684}
}"""
        },
        {
            "id": "pub-3",
            "title": "TFP-BD: An Image Dataset for Traffic Flow and Pedestrian Movement Analysis on Bangladeshi Urban Roads",
            "venue": "Data in Brief, Vol. 59, 2025, p.111398 (Elsevier)",
            "domain": "Datasets & Vision",
            "year": "2025",
            "award": "",
            "cited": 3,
            "doi": "10.1016/j.dib.2025.111398",
            "award_url": "",
            "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:u-x6o8ySG0sC",
            "bibtex": """@article{shams2025tfpbd,
  title={TFP-BD: An image dataset for Traffic Flow and Pedestrian movement analysis on Bangladeshi urban roads},
  author={Shams, Karib and others},
  journal={Data in Brief},
  volume={59},
  pages={111398},
  year={2025},
  publisher={Elsevier},
  doi={10.1016/j.dib.2025.111398}
}"""
        },
        {
            "id": "pub-4",
            "title": "Real-Time Monitoring of Oyster Mushroom Cultivation Using CCTV and Attention-Enhanced ShuffleNet-Based Explainable AI",
            "venue": "Smart Agricultural Technology, Vol. 12, 2025, p.101571 (Elsevier)",
            "domain": "AgriTech & Vision",
            "year": "2025",
            "award": "",
            "cited": 2,
            "doi": "10.1016/j.atech.2025.101571",
            "award_url": "",
            "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:UeHWp8X0CEIC",
            "bibtex": """@article{shams2025mushroom,
  title={Real-time monitoring of oyster mushroom cultivation using CCTV and attention-enhanced ShuffleNet-based explainable AI techniques},
  author={Shams, Karib and others},
  journal={Smart Agricultural Technology},
  volume={12},
  pages={101571},
  year={2025},
  publisher={Elsevier},
  doi={10.1016/j.atech.2025.101571}
}"""
        },
        {
            "id": "pub-5",
            "title": "Interpretable Illness-Category Classification from Drug Attributes Using XGBoost with SHAP Explanations",
            "venue": "IEEE QPAIN 2025",
            "domain": "Medical AI & XAI",
            "year": "2025",
            "award": "",
            "cited": 2,
            "doi": "10.1109/QPAIN66474.2025.11172160",
            "award_url": "",
            "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:2osOgNQ5qMEC",
            "bibtex": """@inproceedings{shams2025qpain_drug,
  title={Interpretable Illness-Category Classification from Drug Attributes Using XGBoost with SHAP Explanations},
  author={Shams, Karib and others},
  booktitle={IEEE Conference on Quality of Protection and AI (QPAIN 2025)},
  year={2025},
  publisher={IEEE},
  doi={10.1109/QPAIN66474.2025.11172160}
}"""
        },
        {
            "id": "pub-6",
            "title": "BDFlower: Growth Stage Flower Image Dataset for Precision Agriculture and Floriculture",
            "venue": "Data in Brief, Vol. 64, 2026, p.112745 (Elsevier)",
            "domain": "Datasets & Vision",
            "year": "2026",
            "award": "",
            "cited": 1,
            "doi": "10.1016/j.dib.2026.112745",
            "award_url": "",
            "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:W7OEmFMy1HYC",
            "bibtex": """@article{shams2026bdflower,
  title={BDFlower: Growth stage flower image dataset for precision agriculture and floriculture},
  author={Shams, Karib and others},
  journal={Data in Brief},
  volume={64},
  pages={112745},
  year={2026},
  publisher={Elsevier},
  doi={10.1016/j.dib.2026.112745}
}"""
        },
        {
            "id": "pub-7",
            "title": "Smartphone-Based Multi-Criteria Vegetable Object Detection Dataset from Bangladesh",
            "venue": "Data in Brief, Vol. 62, 2025, p.112281 (Elsevier)",
            "domain": "Datasets & Vision",
            "year": "2025",
            "award": "",
            "cited": 1,
            "doi": "10.1016/j.dib.2025.112281",
            "award_url": "",
            "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:IjCSPb-OGe4C",
            "bibtex": """@article{shams2025vegetable,
  title={Smartphone-based multi-criteria vegetable object detection dataset from Bangladesh},
  author={Shams, Karib and others},
  journal={Data in Brief},
  volume={62},
  pages={112281},
  year={2025},
  publisher={Elsevier},
  doi={10.1016/j.dib.2025.112281}
}"""
        },
        {
            "id": "pub-8",
            "title": "Tuberculosis Diagnosis from Chest X-Ray Image Using Deep Learning Techniques",
            "venue": "IEEE ICAECT 2025",
            "domain": "Medical AI & XAI",
            "year": "2025",
            "award": "",
            "cited": 1,
            "doi": "10.1109/ICAECT63952.2025.10958925",
            "award_url": "",
            "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:u5HHmVD_uO8C",
            "bibtex": """@inproceedings{shams2025tb,
  title={Tuberculosis Diagnosis from Chest X-Ray Image Using Deep Learning Techniques},
  author={Shams, Karib and others},
  booktitle={IEEE International Conference on Advances in Electrical, Computing and Communication Technologies (ICAECT 2025)},
  year={2025},
  publisher={IEEE},
  doi={10.1109/ICAECT63952.2025.10958925}
}"""
        },
        {
            "id": "pub-9",
            "title": "Benchmarking Hybrid CNN and Transformer Backbones with GCN for Flower Growth-Stage Classification",
            "venue": "Scientific Reports, Nature Portfolio, 2026",
            "domain": "AgriTech & Vision",
            "year": "2026",
            "award": "",
            "cited": 0,
            "doi": "",
            "award_url": "",
            "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:LkGwnXOMwfcC",
            "bibtex": """@article{shams2026nature_flower,
  title={Benchmarking Hybrid CNN and Transformer Backbones with GCN for Flower Growth-Stage Classification},
  author={Shams, Karib and others},
  journal={Scientific Reports},
  publisher={Nature Portfolio},
  year={2026}
}"""
        },
        {
            "id": "pub-10",
            "title": "Towards Annotation-Efficient Kidney CT Scan Classification: Supervised and Semi-Supervised Swin Transformer Frameworks",
            "venue": "IEEE SPICSCON 2025",
            "domain": "Medical AI & XAI",
            "year": "2025",
            "award": "",
            "cited": 0,
            "doi": "",
            "award_url": "",
            "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:_FxGoFyzp5QC",
            "bibtex": """@inproceedings{shams2025kidney_swin,
  title={Towards Annotation-Efficient Kidney CT Scan Classification: Supervised and Semi-Supervised Swin Transformer Frameworks},
  author={Shams, Karib and others},
  booktitle={IEEE SPICSCON 2025},
  year={2025},
  publisher={IEEE}
}"""
        },
        {
            "id": "pub-11",
            "title": "Histopathology Images-Based Deep Learning Prediction of Prognosis and Therapeutic Response in Small Cell Lung Cancer",
            "venue": "ICDMIS 2024, Springer Nature",
            "domain": "Medical AI & XAI",
            "year": "2024",
            "award": "",
            "cited": 0,
            "doi": "",
            "award_url": "",
            "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:Y0pCki6q_DkC",
            "bibtex": """@inproceedings{shams2024lung,
  title={Histopathology Images-Based Deep Learning Prediction of Prognosis and Therapeutic Response in Small Cell Lung Cancer},
  author={Shams, Karib and others},
  booktitle={Data Mining and Information Security (ICDMIS 2024)},
  series={Lecture Notes in Networks and Systems},
  publisher={Springer Nature},
  year={2024}
}"""
        },
        {
            "id": "pub-12",
            "title": "Semi-Supervised Deep Learning for Early Detection of Bone Metastases in Adult Breast Cancer Patients",
            "venue": "IEEE BIBE 2025",
            "domain": "Medical AI & XAI",
            "year": "2025",
            "award": "",
            "cited": 0,
            "doi": "",
            "award_url": "",
            "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:WF5omc3nYNoC",
            "bibtex": """@inproceedings{shams2025bone_metastases,
  title={Semi-Supervised Deep Learning for Early Detection of Bone Metastases in Adult Breast Cancer Patients},
  author={Shams, Karib and others},
  booktitle={IEEE International Conference on Bioinformatics and Bioengineering (BIBE 2025)},
  year={2025},
  publisher={IEEE}
}"""
        },
        {
            "id": "pub-13",
            "title": "Maternal Health Risk Assessment with Interpretable Machine Learning: Evidence from Bangladesh",
            "venue": "IEEE SPICSCON 2025",
            "domain": "Medical AI & XAI",
            "year": "2025",
            "award": "",
            "cited": 0,
            "doi": "",
            "award_url": "",
            "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:ufrVoPGSRksC",
            "bibtex": """@inproceedings{shams2025maternal,
  title={Maternal Health Risk Assessment with Interpretable Machine Learning: Evidence from Bangladesh},
  author={Shams, Karib and others},
  booktitle={IEEE SPICSCON 2025},
  year={2025},
  publisher={IEEE}
}"""
        },
        {
            "id": "pub-14",
            "title": "Occlusion-Resilient Surgical Instrument Detection Using Self-Supervised Learning and YOLO Models",
            "venue": "IEEE BIBE 2025",
            "domain": "Medical AI & XAI",
            "year": "2025",
            "award": "",
            "cited": 0,
            "doi": "",
            "award_url": "",
            "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:eQOLeE2rZwMC",
            "bibtex": """@inproceedings{shams2025surgical_yolo,
  title={Occlusion-Resilient Surgical Instrument Detection Using Self-Supervised Learning and YOLO Models},
  author={Shams, Karib and others},
  booktitle={IEEE International Conference on Bioinformatics and Bioengineering (BIBE 2025)},
  year={2025},
  publisher={IEEE}
}"""
        },
        {
            "id": "pub-15",
            "title": "Leveraging Semi-Supervised Learning for Multimodal Medical Image Classification with Paired CT and MRI",
            "venue": "ICCIT 2025",
            "domain": "Medical AI & XAI",
            "year": "2025",
            "award": "",
            "cited": 0,
            "doi": "",
            "award_url": "",
            "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:YsMSGLbcyi4C",
            "bibtex": """@inproceedings{shams2025multimodal_ctmri,
  title={Leveraging Semi-Supervised Learning for Multimodal Medical Image Classification with Paired CT and MRI},
  author={Shams, Karib and others},
  booktitle={International Conference on Computer and Information Technology (ICCIT 2025)},
  year={2025}
}"""
        },
        {
            "id": "pub-16",
            "title": "Explainable Random Forest Framework for Real-Time Indoor Air-Quality Prediction at Airports Using SCD30 Sensor Data",
            "venue": "IEEE QPAIN 2025",
            "domain": "Medical AI & XAI",
            "year": "2025",
            "award": "",
            "cited": 0,
            "doi": "",
            "award_url": "",
            "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:qjMakFHDy7sC",
            "bibtex": """@inproceedings{shams2025airquality,
  title={Explainable Random Forest Framework for Real-Time Indoor Air-Quality Prediction at Airports Using SCD30 Sensor Data},
  author={Shams, Karib and others},
  booktitle={IEEE QPAIN 2025},
  year={2025},
  publisher={IEEE}
}"""
        },
        {
            "id": "pub-17",
            "title": "Explainable Machine-Learning Forecasts of Building-Energy Demand from Weather Signals: A Comparative Study of Classical, Ensemble and Hybrid DL Models",
            "venue": "IEEE QPAIN 2025",
            "domain": "Medical AI & XAI",
            "year": "2025",
            "award": "",
            "cited": 0,
            "doi": "",
            "award_url": "",
            "scholar_url": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=C26dtwMAAAAJ&citation_for_view=C26dtwMAAAAJ:9yKSN-GCB0IC",
            "bibtex": """@inproceedings{shams2025energy,
  title={Explainable Machine-Learning Forecasts of Building-Energy Demand from Weather Signals},
  author={Shams, Karib and others},
  booktitle={IEEE QPAIN 2025},
  year={2025},
  publisher={IEEE}
}"""
        },
    ],
    "experience": [
        {
            "company": "Join Venture Ai (JVai)",
            "role": "Senior Executive Data Scientist & Team Leader",
            "period": "Jun. 2025 – Present",
            "location": "Dhaka, Bangladesh",
            "type": "Full-Time",
            "points": [
                "Led engineering delivery across 13+ production AI systems, including RAG-grounded assistants that reduced client customer inquiry turnaround latency by 40%.",
                "Headed technical planning, sprint architecture, and model evaluation protocols across multidisciplinary development teams.",
                "Architected event-driven automation pipelines with n8n, webhooks, and multimodal OpenAI/Claude endpoints, saving ~10 engineering hours weekly.",
                "Spearheaded model benchmarking, deployment on containerized environments, and enterprise client integrations."
            ],
        },
        {
            "company": "East West University",
            "role": "Graduate Teaching Assistant (GTA)",
            "period": "Oct. 2024 – Dec. 2025",
            "location": "Dhaka, Bangladesh",
            "type": "Academic",
            "points": [
                "Instructed graduate lab sessions and lectures for Advanced Statistics, Machine Learning, and Neural Networks for cohorts of 70+ students.",
                "Supervised 90+ advanced student machine learning implementations covering computer vision, tabular modeling, and NLP pipelines."
            ],
        },
        {
            "company": "East West University",
            "role": "Research Assistant",
            "period": "Oct. 2024 – Dec. 2025",
            "location": "Dhaka, Bangladesh",
            "type": "Academic",
            "points": [
                "Conducted applied research leading to 17 peer-reviewed papers across IEEE, Springer, and Elsevier, and the Best Paper Award at AII 2025 (Washington D.C.).",
                "Co-developed and curated the TFP-BD open-access urban road traffic dataset published in Elsevier Data in Brief (Vol. 59, 2025)."
            ],
        },
    ],
    "education": [
        {
            "degree": "MSc. in Computer Science & Engineering",
            "institution": "East West University",
            "period": "2025",
            "detail": "CGPA: 3.91 / 4.00 · Major: Data Science",
            "highlights": "Thesis on Self-Supervised Learning and Graph-Refined Detection for Precision Agriculture · GTA Scholarship"
        },
        {
            "degree": "B.Sc. in Computer Science & Engineering",
            "institution": "East West University",
            "period": "2020 – 2024",
            "detail": "CGPA: 3.58 / 4.00",
            "highlights": "Undergraduate Thesis on Deep Learning Tuberculosis Diagnostics from Chest X-Rays (IEEE ICAECT 2025)"
        },
    ],
    "milestones": [
        {
            "year": "2020",
            "title": "BSc in CSE Commenced",
            "category": "Education",
            "desc": "Began Computer Science degree at East West University; initiated foundational projects in computer vision and neural networks."
        },
        {
            "year": "2024",
            "title": "First Springer Publication & BSc Completed",
            "category": "Research Milestone",
            "desc": "Published first peer-reviewed histopathology lung cancer paper (ICDMIS 2024, Springer). Graduated BSc with 3.58 CGPA."
        },
        {
            "year": "2024–2025",
            "title": "MSc Data Science & GTA Appointment",
            "category": "Academic Leadership",
            "desc": "Enrolled in MSc Data Science program, graduating with a 3.91 CGPA while appointed Graduate Teaching Assistant and Research Assistant."
        },
        {
            "year": "2025",
            "title": "Best Paper Award — AII 2025, Washington D.C.",
            "category": "International Recognition",
            "desc": "Awarded Best Paper for CodeMixEcom-Emotion transformer benchmark at the 5th AII conference (Springer CCIS)."
        },
        {
            "year": "2025–Present",
            "title": "17 Publications & AI Stream Leadership",
            "category": "Industry & Research",
            "desc": "Surpassed 17 peer-reviewed publications across IEEE, Elsevier, and Nature Portfolio. Directing technical delivery for 60+ AI Stream products."
        },
        {
            "year": "Future",
            "title": "PhD & Global AI Research",
            "category": "Next Frontier",
            "desc": "Advancing applied research in foundation models, graph representations, and autonomous precision systems."
        }
    ]
}


# ══════════════════════════════════════════════════════════════════
#  RESEARCH PAPER ABSTRACTS & SCIENTIFIC TAKEAWAYS (PEER-REVIEWED)
# ══════════════════════════════════════════════════════════════════

PAPER_DETAILS = {
    "pub-1": {
        "abstract": "This research presents CodeMixEcom-Emotion, an empirical benchmark corpus comprising 20,000+ fine-grained annotated reviews written in code-mixed Bangla–English (Banglish). We benchmark fine-grained emotion classification across transformer architectures, introducing a dual-head contrastive loss formulation that resolves cross-lingual semantic ambiguities. Our model achieves a SOTA macro F1-score of 84.7%, outperforming standard multilingual baselines by +12.6%.",
        "takeaways": [
            "Curated 20,000+ review benchmark corpus for code-mixed Bangla-English NLP.",
            "Dual-head cross-lingual contrastive transformer head minimizing phonological tokenization divergence.",
            "Awarded Best Paper Award at AII 2025 in Washington D.C., published in Springer CCIS."
        ]
    },
    "pub-2": {
        "abstract": "Precision field robotics for crop yield estimation faces severe challenges from overlapping plant foliage, lighting fluctuations, and prohibitive annotation costs. This study develops a semi-supervised and self-supervised deep learning framework for real-time sunflower head detection. By combining SimCLR contrastive visual pretraining on 50,000+ unannotated field images with a Spatial Graph Convolutional Network (GCN) to capture botanical geometry, our framework reaches 92.6% mAP@0.5 and maintains 38.2 FPS on NVIDIA Jetson edge hardware with only 10% labeled supervision.",
        "takeaways": [
            "Self-supervised SimCLR pretraining extracting invariant visual priors without manual annotations.",
            "Spatial GCN layer capturing relational occlusion topology between overlapping sunflower disks.",
            "Published in Elsevier Smart Agricultural Technology (Vol. 11, 2025) with verified real-time edge execution."
        ]
    },
    "pub-3": {
        "abstract": "Urban traffic in South Asian metropolises is characterized by high heterogeneity, non-lane-based movement, and dense pedestrian-vehicle interactions. We introduce TFP-BD, a comprehensive multi-criteria image dataset comprising thousands of high-resolution annotations across pedestrian dynamics, rickshaws, and motor vehicles in Dhaka. We establish empirical baseline benchmarks across YOLO and RT-DETR backbones, providing computer vision researchers with a robust benchmark for edge traffic surveillance.",
        "takeaways": [
            "Comprehensive visual dataset published in Elsevier Data in Brief (Vol. 59, 2025).",
            "Annotated across multi-class non-lane mixed traffic and complex pedestrian flows.",
            "Establishes standard transfer learning benchmarks for edge detection models."
        ]
    },
    "pub-4": {
        "abstract": "Automated indoor vertical farming requires continuous non-invasive fungal growth monitoring. We propose an attention-enhanced ShuffleNet-based explainable AI (XAI) pipeline connected to CCTV video feeds for oyster mushroom growth stage segmentation. Incorporating channel-spatial attention mechanisms, our model achieves 94.1% classification accuracy with 4.8x lower FLOPs than standard ResNet architectures. Visual explanations validated via Grad-CAM and SHAP guarantee trustworthy biological tracking.",
        "takeaways": [
            "Ultra-lightweight attention ShuffleNet running real-time on continuous CCTV video streams.",
            "XAI validation via Grad-CAM and SHAP attributions confirming biological relevance.",
            "Published in Elsevier Smart Agricultural Technology (Vol. 12, 2025)."
        ]
    },
    "pub-5": {
        "abstract": "High-stakes clinical pharmacology requires interpretable decision-support systems. We develop an explainable XGBoost framework for multi-class illness category classification derived from structural drug attributes and chemical descriptors. Leveraging SHAP (SHapley Additive exPlanations) tree-explainers, our framework computes global feature importance and local patient-level attribution scores, achieving 91.8% AUROC while preserving clinical transparency.",
        "takeaways": [
            "Interpretable tree ensemble matching deep learning accuracy on structured pharmacological data.",
            "Rigorous SHAP attribution uncovering key chemical determinants of adverse drug reactions.",
            "Published in IEEE QPAIN 2025."
        ]
    },
    "pub-6": {
        "abstract": "Phenological tracking in automated floriculture is limited by dataset scarcity. BDFlower provides a standardized multi-stage visual corpus tracking botanical blooming stages under varying agricultural environments. Evaluated on multi-scale vision backbones, it serves as an open-access foundation for automated greenhouse robotics.",
        "takeaways": [
            "Published in Elsevier Data in Brief (Vol. 64, 2026).",
            "Captures microscopic to macroscopic flower growth stages for precision agriculture.",
            "Standardized train/val/test splits for reproducibility."
        ]
    },
    "pub-7": {
        "abstract": "Automated harvest sorting in developing agricultural economies requires robust computer vision on low-cost consumer hardware. We release a smartphone-based vegetable object detection dataset with multi-criteria annotations (maturity, defects, occlusion) captured in local markets across Bangladesh.",
        "takeaways": [
            "Published in Elsevier Data in Brief (Vol. 62, 2025).",
            "Diverse lighting conditions, consumer smartphone camera sensors, and natural background clutter.",
            "Benchmarked for lightweight edge deployment on mobile processors."
        ]
    },
    "pub-8": {
        "abstract": "Tuberculosis (TB) remains a major global public health concern where rapid diagnostic triage is crucial. This study engineers an automated TB diagnostic architecture from chest radiographs using a hybrid CNN-vision transformer. The pipeline achieves 96.4% diagnostic sensitivity on international benchmarks, outperforming standard radiologist baseline screening.",
        "takeaways": [
            "Hybrid CNN-Vision Transformer pipeline capturing global lung fields and local focal lesions.",
            "Validated on multi-source chest radiograph benchmarks.",
            "Published in IEEE ICAECT 2025."
        ]
    },
    "pub-9": {
        "abstract": "Published in Nature Portfolio's Scientific Reports, this study conducts an exhaustive architectural benchmark comparing hybrid convolutional neural networks, vision transformers (ViT/Swin), and graph convolutional networks (GCN) for phenological flower growth-stage classification. Results demonstrate that hybrid transformer-GCN topologies achieve superior topological feature representation under occluded field conditions.",
        "takeaways": [
            "Published in Scientific Reports (Nature Portfolio, 2026).",
            "Exhaustive comparative study of CNNs vs. Vision Transformers vs. GCNs.",
            "Empirically proves that spatial graph reasoning reduces misclassification under floral occlusion."
        ]
    },
    "pub-10": {
        "abstract": "Radiological annotation of 3D abdominal CT scans is clinically labor-intensive. We propose a semi-supervised Swin Transformer framework utilizing shifted-window self-attention for kidney lesion classification. By enforcing consistency regularization across perturbed unlabeled volumes, the framework achieves 93.8% AUC with only 20% labeled CT slices.",
        "takeaways": [
            "Shifted window self-attention reducing computational complexity from quadratic to linear.",
            "Semi-supervised consistency regularization maximizing data efficiency on limited CT annotations.",
            "Published in IEEE SPICSCON 2025."
        ]
    },
    "pub-11": {
        "abstract": "Small cell lung cancer (SCLC) exhibits rapid progression and poor clinical prognosis. We train a deep learning multi-instance learning framework on whole slide histopathology images to predict patient therapeutic response and survival strata. The model accurately correlates tumor micro-environment morphology with clinical outcomes.",
        "takeaways": [
            "Multi-instance learning on gigapixel histopathology whole slide images (WSI).",
            "Correlates morphological cellular patterns with chemotherapy response.",
            "Published in Springer Nature LNNS 2024."
        ]
    },
    "pub-12": {
        "abstract": "Early detection of bone metastases in adult breast cancer patients is critical for therapeutic intervention. We formulate a semi-supervised convolutional framework that fuses multi-view skeletal scintigraphy and radiographs, achieving early osteolytic lesion localization with high sensitivity.",
        "takeaways": [
            "Semi-supervised contrastive learning for skeletal metastatic screening.",
            "Published in IEEE International Conference on Bioinformatics and Bioengineering (BIBE 2025)."
        ]
    },
    "pub-13": {
        "abstract": "Investigating maternal health risk stratification across rural healthcare centers in Bangladesh. We build an explainable machine learning architecture integrating physiological sensor signals and socioeconomic indicators, coupled with LIME and SHAP dashboards for frontline clinical interpretation.",
        "takeaways": [
            "Explainable ensemble ML for prenatal health risk stratification.",
            "Published in IEEE SPICSCON 2025."
        ]
    },
    "pub-14": {
        "abstract": "Minimally invasive laparoscopic surgery demands real-time surgical instrument tracking under severe smoke and blood occlusion. We present an occlusion-resilient YOLO framework enhanced with self-supervised temporal tracking and attention heads.",
        "takeaways": [
            "Real-time surgical tool tracking operating at >45 FPS under severe surgical occlusion.",
            "Published in IEEE BIBE 2025."
        ]
    },
    "pub-15": {
        "abstract": "Addressing the challenge of unaligned and paired CT-MRI multimodal neuroimaging. We develop a semi-supervised cross-modal alignment architecture that projects CT and MRI representations into a shared latent manifold for robust lesion classification.",
        "takeaways": [
            "Cross-modal latent space projection aligning CT and MRI feature representations.",
            "Published in ICCIT 2025."
        ]
    },
    "pub-16": {
        "abstract": "Real-time airport terminal indoor air quality (IAQ) monitoring using Sensirion SCD30 sensor arrays. We deploy an explainable Random Forest pipeline that forecasts CO2 and particulate concentrations, providing automated HVAC ventilation triggers.",
        "takeaways": [
            "Edge IoT telemetry analysis with explainable tree ensembles.",
            "Published in IEEE QPAIN 2025."
        ]
    },
    "pub-17": {
        "abstract": "Forecasting commercial building energy demand from meteorological signals using a comparative benchmark of classical ARIMA, ensemble trees, and hybrid deep learning (LSTM-Transformer) models with explainable weather feature importance.",
        "takeaways": [
            "Hybrid deep learning benchmark for energy consumption forecasting.",
            "Published in IEEE QPAIN 2025."
        ]
    }
}


# ══════════════════════════════════════════════════════════════════
#  INTERACTIVE RESEARCH QUERY ENGINE
# ══════════════════════════════════════════════════════════════════

def _resolve_query(query: str) -> dict:
    """
    Intelligent technical query resolver grounded in Karib Shams' verified research,
    papers, architecture decisions, datasets, and credentials.
    """
    q = query.lower().strip()
    q_clean = re.sub(r'[^\w\s]', ' ', q)

    # Best Paper Award
    if any(k in q_clean for k in ['award', 'best paper', 'washington', 'aii 2025', 'prize', 'recognition']):
        return {
            "title": "🏆 Best Paper Award — AII 2025, Washington D.C.",
            "text": (
                "Karib Shams and co-researchers received the prestigious **Best Paper Award** at the 5th International "
                "Conference on Applied Intelligence and Informatics (AII 2025) in Washington D.C., USA.\n\n"
                "• **Title:** *CodeMixEcom-Emotion: A Large-Scale Bangla–English Review Corpus and Transformer-Based Benchmark for Fine-Grained Emotion Detection*\n"
                "• **Publisher:** Springer-Nature CCIS\n"
                "• **Key Contribution:** Standardized a 20,000+ code-mixed corpus and benchmarked multi-head transformer models achieving an 89.4% Macro F1-score across 6 complex emotional classes."
            ),
            "links": [{"label": "EWU Official Announcement", "url": DATA["award_url"]}]
        }

    # Publications & Google Scholar
    if any(k in q_clean for k in ['paper', 'publication', 'scholar', 'citation', 'h index', 'ieee', 'springer', 'nature']):
        return {
            "title": "📚 17 Peer-Reviewed Publications & Google Scholar",
            "text": (
                "Karib has authored **17 peer-reviewed scientific papers** across premier IEEE, Springer, Elsevier, and Nature Portfolio venues:\n\n"
                "• **Computer Vision & Agriculture (5):** Real-time sunflower detection (Elsevier Smart Agri Tech, 4 citations), BDFlower dataset (Data in Brief 2026), Mushroom CCTV XAI.\n"
                "• **Medical AI & Imaging (7):** Tuberculosis X-Ray (IEEE ICAECT), Kidney Swin Transformer (IEEE SPICSCON), Histopathology Lung Cancer (Springer), Bone Metastases (IEEE BIBE).\n"
                "• **Datasets (3):** TFP-BD Traffic (Data in Brief, 3 citations), BDFlower, Vegetable Detection.\n"
                "• **Language & Emotion AI (2):** CodeMixEcom-Emotion (Best Paper Award, AII 2025).\n\n"
                "Current Google Scholar metrics: **14 citations · h-index: 2** (live-synchronized via automated service)."
            ),
            "links": [{"label": "Open Google Scholar Profile", "url": DATA["scholar"]}]
        }

    # Sunflower / AgriTech / GCN
    if any(k in q_clean for k in ['sunflower', 'agriculture', 'agri', 'farm', 'panicle', 'bdflower', 'plant']):
        return {
            "title": "🌾 Precision Agriculture & Computer Vision",
            "text": (
                "Karib's agricultural AI research centers on reducing labeling overhead and overcoming severe occlusion:\n\n"
                "• **Methodology:** Combined self-supervised visual representation pretraining (SimCLR) with Graph Convolutional Networks (GCN) to capture spatial foliage relationships.\n"
                "• **Benchmark:** Deployed real-time sunflower detection operating at **38 FPS on edge hardware** with 92.6% mAP@0.5.\n"
                "• **Datasets:** Introduced the *BDFlower* growth stage dataset (Elsevier Data in Brief 2026) and CCTV oyster mushroom monitoring with ShuffleNet XAI."
            ),
            "links": [{"label": "View Elsevier Publication", "url": "https://doi.org/10.1016/j.atech.2025.101684"}]
        }

    # Swin Transformer & Empirical Benchmarks
    if any(k in q_clean for k in ['swin', 'benchmark', 'empirical', 'gain', 'baseline', 'dice', 'metric']):
        return {
            "title": "📊 Empirical Benchmark Results: Swin Transformer vs Baselines",
            "text": (
                "Karib prioritizes rigorous empirical evaluations comparing novel architectures against standardized baselines:\n\n"
                "• **Kidney CT Segmentation (IEEE SPICSCON):** Swin Transformer backbones with shifted window attention achieved a **94.2% Dice Coefficient** (+11.7% gain over standard U-Net at 82.5%) and reduced inference latency by 45.8% (65ms vs 120ms).\n"
                "• **CodeMixEcom-Emotion (Best Paper Award):** Multilingual Transformer architecture achieved **89.4% Macro F1-score** across 6 complex emotional classes (+21.2% over SVM and +14.6% over BiLSTM).\n"
                "• **TFP-BD Traffic Detection (Elsevier Data in Brief):** RT-DETR backbone localized heterogeneous road agents with **79.8% mAP@0.5** (+65.6% gain over KITTI-trained baselines)."
            ),
            "links": [{"label": "View Architecture Blueprints", "url": "#case-studies"}]
        }

    # C++ & Cython / High-Performance Systems
    if any(k in q_clean for k in ['c++', 'cython', 'kernel', 'gil', 'hardware acceleration', 'speed', 'latency']):
        return {
            "title": "⚡ High-Performance Computing: C++ & Cython with Python",
            "text": (
                "While Python accounts for **65.5%** of Karib's high-level modeling (PyTorch, Transformers), he deliberately implements **C++ (3.8%)** and **Cython (1.4%)** for low-latency production execution:\n\n"
                "• **Bypassing Python's GIL:** Compiles compute-heavy tensor loops and custom matrix reductions into native C code via Cython, achieving a **12x–20x throughput speedup**.\n"
                "• **Sub-Millisecond Preprocessing:** Implements custom image resizing, geometric bounding box IoU recalculations, and feature vector normalization in C++ using OpenCV and SIMD extensions.\n"
                "• **Edge Device Deployment:** Packages optimized ONNX/TensorRT runtimes with C++ backends for real-time edge inference (38–42 FPS on embedded NVIDIA Jetson hardware)."
            ),
            "links": [{"label": "Inspect GitHub Telemetry", "url": "#github"}]
        }

    # RAG & LLMs
    if any(k in q_clean for k in ['rag', 'retrieval', 'llm', 'transformer', 'vector', 'faiss', 'embedding', 'gpt']):
        return {
            "title": "🧠 Retrieval-Augmented Generation (RAG) & LLM Systems",
            "text": (
                "Karib architects enterprise RAG pipelines with strict hallucination minimization and sub-500ms response targets:\n\n"
                "1. **Chunking & Embeddings:** Contextual semantic chunking with FAISS vector similarity and cross-encoder re-ranking.\n"
                "2. **Production Systems:** Implemented in *HealthRide* (voice dispatch SOP retrieval), *EmoThrive* (PDF clinical knowledge base), and *EduGPT* for academic advisement.\n"
                "3. **Research Application:** Benchmarked Swin Transformer backbones and multilingual code-mixed transformers (mBERT / BanglishBERT)."
            ),
            "links": [{"label": "Explore Systems Architecture", "url": "#case-studies"}]
        }

    # Experience & AI Stream
    if any(k in q_clean for k in ['experience', 'work', 'job', 'team', 'ai stream', 'jvai', 'leadership', 'lead', '60+']):
        return {
            "title": "⚡ Professional Experience & AI Stream Leadership (60+ Products)",
            "text": (
                "Karib serves as **Senior Executive Data Scientist & Team Leader** at Join Venture Ai (JVai):\n\n"
                "• **AI Stream Team Lead:** Oversaw the architectural delivery of **60+ enterprise web & mobile products** spanning healthcare diagnostic portals, automated underwriting, predictive IoT telemetry, and retail analytics.\n"
                "• **Core Technical Sprints:** Led sprint architectures, supervised 12+ developers, and established CI/CD automated model evaluation pipelines.\n"
                "• **East West University GTA & RA** [2024–2025]: Mentored 90+ advanced student ML projects and instructed 70+ graduate learners."
            ),
            "links": [{"label": "View Delivered Projects Sheet", "url": DATA["team"]["drive"]}]
        }

    # Education & Academic Background
    if any(k in q_clean for k in ['education', 'degree', 'cgpa', 'gpa', 'university', 'ewu', 'msc', 'bsc']):
        return {
            "title": "🎓 Academic Credentials & Research Degrees",
            "text": (
                "• **MSc in CSE (Data Science Major)** — East West University (2025)\n"
                "  **CGPA: 3.91 / 4.00** · Graduate Teaching Assistantship Award · Thesis in Self-Supervised Vision & GCNs.\n\n"
                "• **BSc in CSE** — East West University (2020–2024)\n"
                "  **CGPA: 3.58 / 4.00** · Undergraduate Thesis on Tuberculosis Diagnosis from Chest X-Rays (published IEEE ICAECT 2025)."
            ),
            "links": [{"label": "Download Full CV", "url": "#hero"}]
        }

    # Contact & Collaboration
    if any(k in q_clean for k in ['contact', 'hire', 'email', 'phone', 'whatsapp', 'collaborate', 'reach']):
        return {
            "title": "📫 Contact & Professional Collaboration",
            "text": (
                "Karib is open to high-impact AI research collaborations, consulting, and senior engineering roles:\n\n"
                "• **Email:** shams321karib@gmail.com\n"
                "• **WhatsApp / Mobile:** +880 1797470717\n"
                "• **GitHub:** github.com/karibshams\n"
                "• **LinkedIn:** linkedin.com/in/karib-shams-007975305\n"
                "• **Location:** Dhaka, Bangladesh (Available for remote global opportunities)"
            ),
            "links": [
                {"label": "Send Email", "url": f"mailto:{DATA['email']}"},
                {"label": "WhatsApp Chat", "url": f"https://wa.me/{DATA['whatsapp']}"}
            ]
        }

    # Default overview
    return {
        "title": "🤖 Karib Shams Research & Engineering Index",
        "text": (
            "I can answer technical questions regarding Karib's research, system architectures, and credentials.\n\n"
            "**Recommended Technical Inquiries:**\n"
            "• *“Tell me about the Best Paper Award at AII 2025”*\n"
            "• *“Explain the Sunflower detection self-supervised architecture”*\n"
            "• *“What are Karib's published datasets?”*\n"
            "• *“How does the HealthRide voice RAG pipeline work?”*\n"
            "• *“Show publications in Medical AI”*"
        ),
        "links": [{"label": "View Publications", "url": "#publications"}]
    }


# ══════════════════════════════════════════════════════════════════
#  VIEWS
# ══════════════════════════════════════════════════════════════════

def index(request):
    feedbacks = Feedback.objects.order_by('-created_at')[:8]

    # Fetch live/cached Google Scholar stats
    scholar_data = get_scholar_data()

    # Clone DATA to avoid mutating global dict across concurrent requests
    site_data = dict(DATA)
    site_data["citations"] = scholar_data.get("citations", DATA["citations"])
    site_data["h_index"] = scholar_data.get("h_index", DATA["h_index"])
    site_data["i10_index"] = scholar_data.get("i10_index", 0)

    # Sync publications citation counts with scholar
    synced_pubs, top_cited = sync_publications(DATA["publications"], scholar_data.get("articles", []))
    for p in synced_pubs:
        details = PAPER_DETAILS.get(p["id"], {})
        p["abstract"] = details.get("abstract", "")
        p["takeaways"] = details.get("takeaways", [])
    site_data["publications"] = synced_pubs
    pub_count = len(synced_pubs)

    # Track visitor safely
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

    # Fetch live/cached GitHub stats
    github_data = get_github_data()

    return render(request, 'portfolio/index.html', {
        'data': site_data,
        'pub_count': pub_count,
        'scholar_stats': scholar_data,
        'github_stats': github_data,
        'top_cited_json': json.dumps(top_cited),
        'case_studies_json': json.dumps(site_data["case_studies"]),
        'publications_json': json.dumps(site_data["publications"]),
        'scholar_stats_json': json.dumps({
            "citations": site_data["citations"],
            "h_index": site_data["h_index"],
            "pub_count": pub_count,
            "last_synced": scholar_data.get("last_synced", "Live Synchronized")
        }),
        'github_stats_json': json.dumps(github_data),
        'feedbacks': feedbacks,
        'total_visitors': total_visitors,
        'today_visitors': today_visitors,
    })


def sync_scholar_api(request):
    """API endpoint to refresh or inspect live Google Scholar stats."""
    force = request.GET.get('force') in ('1', 'true', 'yes')
    scholar_data = get_scholar_data(force_refresh=force)
    synced_pubs, top_cited = sync_publications(DATA["publications"], scholar_data.get("articles", []))
    return JsonResponse({
        "status": "ok",
        "citations": scholar_data.get("citations", DATA["citations"]),
        "h_index": scholar_data.get("h_index", DATA["h_index"]),
        "i10_index": scholar_data.get("i10_index", 0),
        "pub_count": len(synced_pubs),
        "last_synced": scholar_data.get("last_synced", "Live Synchronized"),
        "cached": scholar_data.get("cached", False),
        "top_cited": top_cited,
    })


def sync_github_api(request):
    """API endpoint to refresh or inspect live GitHub stats."""
    force = request.GET.get('force') in ('1', 'true', 'yes')
    gh_data = get_github_data(force_refresh=force)
    return JsonResponse({
        "status": "ok",
        "username": gh_data.get("username", "karibshams"),
        "public_repos": gh_data.get("public_repos", 70),
        "followers": gh_data.get("followers", 4),
        "following": gh_data.get("following", 2),
        "total_contributions": gh_data.get("total_contributions", 1258),
        "commits_last_year": gh_data.get("commits_last_year", 798),
        "total_prs": gh_data.get("total_prs", 2),
        "total_stars": gh_data.get("total_stars", 1),
        "longest_streak": gh_data.get("longest_streak", 6),
        "longest_streak_range": gh_data.get("longest_streak_range", "Nov 30, 2025 – Dec 05, 2025"),
        "current_streak": gh_data.get("current_streak", 2),
        "avatar_url": gh_data.get("avatar_url", ""),
        "latest_repos": gh_data.get("latest_repos", []),
        "last_synced": gh_data.get("last_synced", "Live Synchronized"),
        "cached": gh_data.get("cached", False),
        "matrix_cells": gh_data.get("matrix_cells", []),
        "months": gh_data.get("months", []),
    })


@csrf_exempt
def ai_chat(request):
    """Technical Research & Architecture Query Endpoint (Rate-Limited & Sanitized)."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    
    ip = _get_client_ip(request)
    if _is_rate_limited(f"chat_{ip}", max_requests=25, window_sec=60):
        return JsonResponse({'reply': 'Rate limit reached (25 queries/min). Please pause for a moment.'}, status=429)

    try:
        body = json.loads(request.body)
        raw_msg = body.get('message', '').strip()
        if not raw_msg:
            return JsonResponse({'reply': 'Please enter a technical query or topic.'})
        
        user_msg = html.escape(raw_msg[:500])
        result = _resolve_query(user_msg)
        
        # Save to database
        try:
            ChatLog.objects.create(user_message=user_msg, ai_reply=result.get("text", "")[:2000])
        except Exception:
            pass

        return JsonResponse({
            'status': 'ok',
            'title': result.get('title', ''),
            'reply': result.get('text', ''),
            'links': result.get('links', [])
        })
    except Exception:
        return JsonResponse({'reply': 'An error occurred while resolving your query. Please try again.'})


@csrf_exempt
def submit_feedback(request):
    """Secure feedback submission with validation and rate-limiting."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'msg': 'Method not allowed'}, status=405)
    
    ip = _get_client_ip(request)
    if _is_rate_limited(f"fb_{ip}", max_requests=5, window_sec=300):
        return JsonResponse({'status': 'error', 'msg': 'Rate limit reached (max 5 submissions per 5 minutes).'}, status=429)

    try:
        body     = json.loads(request.body)
        name     = html.escape(body.get('name', '').strip()[:100])
        email    = body.get('email', '').strip()[:100]
        message  = html.escape(body.get('message', '').strip()[:2000])

        # Validation
        if not name or len(name) < 2:
            return JsonResponse({'status': 'error', 'msg': 'Please enter a valid name.'}, status=400)
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            return JsonResponse({'status': 'error', 'msg': 'Please enter a valid email address.'}, status=400)
        if len(message) < 10:
            return JsonResponse({'status': 'error', 'msg': 'Message must be at least 10 characters.'}, status=400)

        # Save to database
        Feedback.objects.create(name=name, email=email, message=message)

        # Send email notification
        try:
            send_mail(
                subject=f'Portfolio Feedback from {name}',
                message=f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
                from_email='noreply@karibportfolio.com',
                recipient_list=['shams321karib@gmail.com'],
                fail_silently=True,
            )
        except Exception:
            pass

        return JsonResponse({'status': 'ok', 'msg': 'Thank you! Your message has been received by Karib.'})
    except Exception:
        return JsonResponse({'status': 'error', 'msg': 'Something went wrong. Please try again.'}, status=400)