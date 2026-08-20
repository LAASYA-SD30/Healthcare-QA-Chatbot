import re
import html as html_lib

import streamlit as st

from healthcare_backend import healthcare_chat


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Healthcare QA Chatbot",
    page_icon="🩺",
    layout="centered"
)


# ============================================================
# CUSTOM CSS — PREMIUM DARK MEDICAL AI THEME
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 15% -10%, rgba(45, 212, 191, 0.14) 0%, transparent 40%),
            radial-gradient(circle at 100% 10%, rgba(129, 140, 248, 0.10) 0%, transparent 45%),
            radial-gradient(circle at 50% 100%, rgba(56, 189, 248, 0.08) 0%, transparent 50%),
            #060a0e;
    }

    header[data-testid="stHeader"] {
        background-color: rgba(6, 10, 14, 0.85);
        backdrop-filter: blur(6px);
    }

    .block-container {
        max-width: 800px;
        padding-top: 1.4rem;
        padding-bottom: 5rem;
        margin: 0 auto;
    }

    /* ---------------- HERO ---------------- */

    .hero-wrap {
        text-align: center;
        padding: 16px 10px 6px 10px;
        margin-bottom: 4px;
    }

    .hero-badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 999px;
        background: linear-gradient(90deg, rgba(45,212,191,0.15), rgba(56,189,248,0.12));
        border: 1px solid rgba(45,212,191,0.35);
        color: #5eead4;
        font-size: 11.5px;
        font-weight: 600;
        letter-spacing: 1.2px;
        margin-bottom: 14px;
    }

    .hero-title {
        font-size: 38px;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0 0 8px 0;
        background: linear-gradient(90deg, #2dd4bf 0%, #38bdf8 50%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-subtitle {
        color: #8b9aa5;
        font-size: 14.5px;
        font-weight: 400;
        max-width: 480px;
        margin: 0 auto 16px auto;
        line-height: 1.5;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 999px;
        background: rgba(45, 212, 191, 0.08);
        border: 1px solid rgba(45, 212, 191, 0.25);
        font-size: 12px;
        font-weight: 600;
        color: #5eead4;
        letter-spacing: 0.5px;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #2dd4bf;
        box-shadow: 0 0 8px 2px rgba(45, 212, 191, 0.7);
        animation: pulse-dot 1.8s ease-in-out infinite;
    }

    @keyframes pulse-dot {
        0%   { opacity: 1; }
        50%  { opacity: 0.35; }
        100% { opacity: 1; }
    }

    .section-rule {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(45,212,191,0.25), transparent);
        margin: 22px 0 16px 0;
    }

    /* ---------------- METRICS ---------------- */

    .metric-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 13px;
        padding: 13px 10px;
        text-align: center;
        backdrop-filter: blur(8px);
        transition: border-color 0.2s ease;
    }

    .metric-card:hover {
        border-color: rgba(45,212,191,0.35);
    }

    .metric-value {
        font-size: 20px;
        font-weight: 800;
        background: linear-gradient(90deg, #2dd4bf, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2px;
    }

    .metric-label {
        font-size: 10.5px;
        color: #7a8790;
        font-weight: 500;
        letter-spacing: 0.2px;
        line-height: 1.3;
    }

    /* ---------------- SECTION HEADINGS ---------------- */

    .section-heading {
        font-size: 14.5px;
        font-weight: 700;
        color: #dfe7eb;
        margin-bottom: 3px;
    }

    .section-subheading {
        font-size: 12.5px;
        color: #6b7880;
        margin-bottom: 12px;
    }

    .group-heading {
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: 1px;
        color: #5eead4;
        margin: 14px 0 6px 0;
    }

    /* ---------------- EMPTY STATE ---------------- */

    .empty-state {
        text-align: center;
        padding: 22px 10px 6px 10px;
    }

    .empty-state-icon {
        font-size: 30px;
        margin-bottom: 8px;
        filter: drop-shadow(0 0 14px rgba(45,212,191,0.45));
    }

    .empty-state-title {
        font-size: 17px;
        font-weight: 700;
        color: #e5edf0;
        margin-bottom: 5px;
    }

    .empty-state-sub {
        font-size: 13px;
        color: #7a8790;
        margin-bottom: 18px;
    }

    /* ---------------- BUTTONS (quick questions) ---------------- */

    div[data-testid="stButton"] > button {
        width: 100%;
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        color: #cdd7db !important;
        border-radius: 11px !important;
        padding: 9px 13px !important;
        font-size: 12.5px !important;
        font-weight: 500 !important;
        text-align: left !important;
        transition: all 0.18s ease !important;
        white-space: normal !important;
        height: auto !important;
    }

    div[data-testid="stButton"] > button:hover {
        border-color: rgba(45,212,191,0.45) !important;
        background: rgba(45,212,191,0.06) !important;
        color: #5eead4 !important;
        transform: translateY(-1px);
    }

    div[data-testid="stButton"] > button:focus {
        box-shadow: 0 0 0 2px rgba(45,212,191,0.25) !important;
    }

    /* ---------------- PIPELINE ---------------- */

    .pipeline-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0px;
        margin: 4px 0 2px 0;
    }

    .pipeline-card {
        width: 100%;
        max-width: 440px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 11px;
        padding: 10px 16px;
        text-align: center;
        font-size: 13px;
        font-weight: 600;
        color: #dfe7eb;
    }

    .pipeline-card .pipeline-sub {
        font-size: 10.5px;
        font-weight: 400;
        color: #7a8790;
        margin-top: 2px;
    }

    .pipeline-arrow {
        color: #2dd4bf;
        font-size: 15px;
        line-height: 1;
        margin: 3px 0;
    }

    .pipeline-tag-row {
        display: flex;
        justify-content: center;
        gap: 8px;
        margin: 10px 0 4px 0;
    }

    .pipeline-tag {
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: 0.5px;
        padding: 4px 12px;
        border-radius: 999px;
    }

    .pipeline-tag.ir {
        background: rgba(56, 189, 248, 0.09);
        border: 1px solid rgba(56, 189, 248, 0.25);
        color: #7dd3fc;
    }

    .pipeline-tag.kb {
        background: rgba(167, 139, 250, 0.09);
        border: 1px solid rgba(167, 139, 250, 0.28);
        color: #c4b5fd;
    }

    /* ---------------- INFO SOURCE CARDS ---------------- */

    .source-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 13px;
        padding: 13px 15px;
        margin-bottom: 9px;
    }

    .source-card-title {
        font-size: 13px;
        font-weight: 700;
        color: #5eead4;
        margin-bottom: 2px;
    }

    .source-card-sub {
        font-size: 11.5px;
        color: #8b9aa5;
    }

    .source-card-desc {
        font-size: 10.5px;
        color: #62707a;
        margin-top: 4px;
    }

    /* ---------------- ACTIVE TOPIC / DIALOGUE CONTEXT ---------------- */

    .topic-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 999px;
        background: rgba(167, 139, 250, 0.09);
        border: 1px solid rgba(167, 139, 250, 0.3);
        font-size: 11.5px;
        color: #c4b5fd;
    }

    .topic-badge .topic-label {
        letter-spacing: 0.8px;
        font-weight: 700;
        color: #8b95f0;
        font-size: 10px;
    }

    .dialogue-context {
        font-size: 11px;
        color: #6b7880;
        margin-top: 5px;
        margin-bottom: 4px;
    }

    /* ---------------- CHAT ---------------- */

    div[data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 13px;
        padding: 8px 10px;
        margin-bottom: 8px;
        backdrop-filter: blur(6px);
    }

    div[data-testid="stChatMessage"] p {
        color: #dbe4e8 !important;
        font-size: 14px;
    }

    /* The chatbot's natural-language answer — the visual focus of each
       assistant turn. Metadata below it is intentionally smaller/quieter. */
    .answer-text {
        color: #f2f8fa;
        font-size: 15.5px;
        font-weight: 500;
        line-height: 1.55;
        margin: 1px 0 2px 0;
    }

    .meta-row {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        margin-top: 8px;
        opacity: 0.9;
    }

    .meta-chip {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 3px 9px;
        border-radius: 999px;
        font-size: 9.5px;
        font-weight: 600;
        letter-spacing: 0.2px;
    }

    .chip-source {
        background: rgba(45, 212, 191, 0.09);
        border: 1px solid rgba(45, 212, 191, 0.25);
        color: #5eead4;
    }

    .chip-type {
        background: rgba(129, 140, 248, 0.10);
        border: 1px solid rgba(129, 140, 248, 0.28);
        color: #b4bcfb;
    }

    .chip-topic {
        background: rgba(56, 189, 248, 0.09);
        border: 1px solid rgba(56, 189, 248, 0.25);
        color: #7dd3fc;
    }

    .chip-method {
        background: rgba(45, 212, 191, 0.06);
        border: 1px solid rgba(45, 212, 191, 0.18);
        color: #94e6d9;
    }

    .chip-dataset {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.12);
        color: #aab6bd;
    }

    .chip-similarity {
        background: rgba(167,139,250,0.09);
        border: 1px solid rgba(167,139,250,0.28);
        color: #c4b5fd;
    }

    /* ---------------- KNOWLEDGE LOOKUP CARD ---------------- */

    .knowledge-card {
        background: rgba(56, 189, 248, 0.04);
        border: 1px solid rgba(56, 189, 248, 0.14);
        border-radius: 10px;
        padding: 8px 11px;
        margin-top: 7px;
        opacity: 0.92;
    }

    .knowledge-card-title {
        font-size: 9px;
        font-weight: 700;
        letter-spacing: 1px;
        color: #7dd3fc;
        margin-bottom: 5px;
    }

    .knowledge-row {
        display: flex;
        justify-content: space-between;
        font-size: 11px;
        color: #93a0a8;
        padding: 1.5px 0;
    }

    .knowledge-row b {
        color: #dfe7eb;
        font-weight: 600;
    }

    /* ---------------- OUT-OF-DOMAIN CARD ---------------- */

    .ood-card {
        background: rgba(248, 113, 113, 0.06);
        border: 1px solid rgba(248, 113, 113, 0.25);
        border-radius: 11px;
        padding: 10px 13px;
        margin-top: 9px;
    }

    .ood-card-title {
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: 0.6px;
        color: #fca5a5;
        margin-bottom: 3px;
    }

    .ood-card-sub {
        font-size: 12px;
        color: #f3b4b4;
    }

    /* ---------------- ERROR CARD ---------------- */

    .error-card {
        background: rgba(248, 113, 113, 0.06);
        border: 1px solid rgba(248, 113, 113, 0.25);
        border-radius: 11px;
        padding: 10px 13px;
        margin-top: 6px;
        font-size: 12.5px;
        color: #f3b4b4;
    }

    /* ---------------- DIALOGUE FLOW / SAMPLE QA ---------------- */

    .flow-line {
        font-size: 12.5px;
        color: #cdd7db;
        padding: 5px 0;
    }

    .flow-line b {
        color: #5eead4;
    }

    .flow-arrow {
        color: #4a555c;
        font-size: 12.5px;
        padding-left: 4px;
    }

    .qa-pair {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 10px;
        padding: 10px 13px;
        margin-bottom: 8px;
    }

    .qa-pair .qa-q {
        font-size: 12.5px;
        font-weight: 700;
        color: #7dd3fc;
        margin-bottom: 3px;
    }

    .qa-pair .qa-a {
        font-size: 12.5px;
        color: #cdd7db;
    }

    .qa-pair .qa-note {
        font-size: 11px;
        color: #6b7880;
        font-style: italic;
    }

    /* ---------------- EVAL SUMMARY ---------------- */

    .eval-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 7px 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        font-size: 12.5px;
        color: #cdd7db;
    }

    .eval-row:last-child { border-bottom: none; }

    .eval-row span.eval-score {
        color: #5eead4;
        font-weight: 700;
    }

    /* ---------------- SIDEBAR ---------------- */

    section[data-testid="stSidebar"] {
        background-color: #05080b;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.2rem;
    }

    .sidebar-brand-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 16px;
    }

    .sidebar-brand-icon {
        width: 32px;
        height: 32px;
        flex-shrink: 0;
        border-radius: 9px;
        background: rgba(45,212,191,0.09);
        border: 1px solid rgba(45,212,191,0.28);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
    }

    .sidebar-brand {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.3px;
        color: #5eead4;
        line-height: 1.3;
    }

    .sidebar-brand-sub {
        font-size: 8.5px;
        font-weight: 600;
        letter-spacing: 0.7px;
        color: #5f6f78;
        margin-top: 2px;
    }

    .sidebar-group-label {
        font-size: 9.5px;
        font-weight: 700;
        letter-spacing: 1px;
        color: #4a555c;
        margin: 2px 0 6px 2px;
    }

    /* Navigation buttons: real st.button widgets, restyled as nav-card rows.
       Default (kind="secondary") = inactive item. kind="primary" = active. */
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button {
        width: 100%;
        text-align: left !important;
        justify-content: flex-start !important;
        border-radius: 9px !important;
        padding: 8px 11px !important;
        font-size: 12.5px !important;
        font-weight: 500 !important;
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        color: #93a0a8 !important;
        transition: all 0.16s ease !important;
        white-space: normal !important;
        height: auto !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
        border-color: rgba(45,212,191,0.3) !important;
        color: #cdd7db !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] {
        background: rgba(45,212,191,0.10) !important;
        border: 1px solid rgba(45,212,191,0.4) !important;
        color: #5eead4 !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"]:hover {
        color: #5eead4 !important;
    }

    .nav-sub {
        font-size: 10px;
        color: #5f6f78;
        margin: 2px 0 8px 3px;
        line-height: 1.3;
    }

    .nav-sub.active {
        color: #7dd3fc;
    }

    /* Clear Conversation is always the last sidebar button — give it its
       own CTA look, distinct from the nav buttons above it. */
    section[data-testid="stSidebar"] div[data-testid="stButton"]:last-of-type > button {
        background: linear-gradient(90deg, #14b8a6, #0ea5e9) !important;
        border: none !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        text-align: center !important;
        justify-content: center !important;
        margin-top: 4px;
    }

    .status-card {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 11px;
        padding: 11px 13px;
        margin: 12px 0 10px 0;
    }

    .status-card-title {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1px;
        color: #5f6f78;
        margin-bottom: 9px;
    }

    .status-item {
        display: flex;
        align-items: flex-start;
        gap: 8px;
        margin-bottom: 8px;
    }

    .status-item:last-of-type {
        margin-bottom: 0;
    }

    .status-line-dot {
        width: 6px;
        height: 6px;
        margin-top: 4px;
        border-radius: 50%;
        background: #2dd4bf;
        box-shadow: 0 0 6px 1px rgba(45,212,191,0.6);
        flex-shrink: 0;
    }

    .status-item-label {
        font-size: 11.5px;
        color: #cdd7db;
        font-weight: 600;
        line-height: 1.3;
    }

    .status-item-value {
        font-size: 10px;
        color: #5eead4;
        font-weight: 500;
    }

    .status-footnote {
        margin-top: 10px;
        padding-top: 8px;
        border-top: 1px solid rgba(255,255,255,0.06);
        font-size: 10px;
        color: #5f6f78;
        font-style: italic;
    }

    .project-line {
        font-size: 12px;
        color: #cdd7db;
        font-weight: 600;
        margin-bottom: 3px;
    }

    .project-sub {
        font-size: 10.5px;
        color: #7a8790;
        line-height: 1.5;
    }

    .project-footnote {
        margin-top: 9px;
        padding-top: 8px;
        border-top: 1px solid rgba(255,255,255,0.06);
        font-size: 10.5px;
        color: #7dd3fc;
        font-weight: 600;
    }

    .session-row {
        display: flex;
        justify-content: space-between;
        font-size: 11.5px;
        color: #93a0a8;
        padding: 2.5px 0;
    }

    .session-row b {
        color: #dfe7eb;
        font-weight: 600;
    }

    .session-empty {
        font-size: 12px;
        color: #93a0a8;
        font-weight: 500;
    }

    .session-empty-sub {
        font-size: 10.5px;
        color: #5f6f78;
        margin-top: 2px;
    }

    .sidebar-footer {
        margin-top: 16px;
        padding-top: 11px;
        border-top: 1px solid rgba(255,255,255,0.05);
        font-size: 9.5px;
        color: #4a555c;
        text-align: center;
        line-height: 1.6;
    }

    /* ---------------- CHAT INPUT ---------------- */

    div[data-testid="stChatInput"] {
        background-color: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 14px;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: rgba(45,212,191,0.5);
        box-shadow: 0 0 0 3px rgba(45,212,191,0.12);
    }

    div[data-testid="stChatInput"] textarea {
        color: #e5edf0 !important;
    }

    /* ---------------- EXPANDERS ---------------- */

    div[data-testid="stExpander"] {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 11px;
        margin-bottom: 9px;
    }

    /* ---------------- FOOTER ---------------- */

    .app-footer {
        text-align: center;
        font-size: 10.5px;
        color: #4a555c;
        margin-top: 30px;
        padding-top: 12px;
        border-top: 1px solid rgba(255,255,255,0.05);
    }

    .stCaption, .stCaption p {
        color: #5f6f78 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CONSTANTS
# ============================================================

USER_AVATAR = "🧑"
ASSISTANT_AVATAR = "🩺"

QUESTION_GROUPS = {
    "SYMPTOMS": [
        "What are the symptoms of malaria?",
        "What are the symptoms of asthma?",
    ],
    "CAUSES & RISK": [
        "What causes malaria?",
        "Who is at risk for asthma?",
    ],
    "DIAGNOSIS & PREVENTION": [
        "How is tuberculosis diagnosed?",
        "How can malaria be prevented?",
    ],
}

PIPELINE_STEPS = [
    ("User Question", "Raw question typed or selected by the user"),
    ("Question Classification", "Determines the question type (symptom, cause, risk, diagnosis...)"),
    ("Disease / Topic Detection", "Identifies the medical condition referenced"),
    ("Information Source Selection", "Chooses between structured KB and semantic sources"),
    ("Semantic Retrieval / Structured Lookup", "Queries MedQuAD, Medical Wikipedia, or the KB"),
    ("Relevant Passage", "The retrieved passage or matched structured field"),
    ("Factoid Answer Extraction", "The answer produced from the retrieved content"),
    ("Dialogue State / Follow-up Context", "Stores the current topic for follow-up questions"),
]

DIALOGUE_FLOW_STEPS = [
    "USER QUESTION",
    "QUESTION TYPE",
    "TOPIC / DISEASE DETECTION",
    "CHECK CURRENT CONVERSATION TOPIC",
    "STRUCTURED KNOWLEDGE OR SEMANTIC RETRIEVAL",
    "ANSWER",
    "UPDATE DIALOGUE STATE",
]

SAMPLE_QA_STATIC = [
    ("What are the symptoms of malaria?",
     "fever, chills, sweating, headache, nausea, vomiting, muscle pain"),
    ("Who is at risk for it?",
     "travel or residence in areas where malaria transmission occurs"),
    ("What causes malaria?",
     "infection with Plasmodium parasites transmitted through infected mosquitoes"),
]

SAMPLE_QA_DYNAMIC_QUESTION = "How is tuberculosis diagnosed?"


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_topic" not in st.session_state:
    st.session_state.current_topic = None

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if "active_section" not in st.session_state:
    st.session_state.active_section = "chat_assistant"


def set_active_section(section_key):
    st.session_state.active_section = section_key


def queue_question(text):
    st.session_state.pending_question = text


def get_live_answer(question_text):
    """Look through conversation history for a previously answered question
    and return its actual backend answer. Returns None if never asked."""
    for i, m in enumerate(st.session_state.messages):
        if m["role"] == "user" and m["content"].strip().lower() == question_text.strip().lower():
            if i + 1 < len(st.session_state.messages) and st.session_state.messages[i + 1]["role"] == "assistant":
                return st.session_state.messages[i + 1]["content"]
    return None


# ============================================================
# METADATA / RETRIEVAL CLASSIFICATION HELPERS
# ============================================================

def classify_source(source):
    """Infer retrieval method / dataset label from the backend's source string,
    without inventing anything not implied by the string itself."""
    if not source:
        return None, None, True
    s = source.lower()
    if "no reliable" in s or "not found" in s:
        return None, None, True
    if "medquad" in s:
        return "Semantic Embedding Retrieval", "MedQuAD", False
    if "wikipedia" in s:
        return "Semantic Embedding Retrieval", "Medical Wikipedia", False
    if "structured" in s:
        return "Structured Knowledge Lookup", "Structured Knowledge Base", False
    return None, None, False


# ============================================================
# ANSWER DISPLAY FORMATTING
#
# These helpers only reformat the *presentation* of an answer the backend
# already returned — they never invent, look up, or alter any medical fact.
# ============================================================

STRUCTURED_ANSWER_TEMPLATES = {
    "symptoms": "Common symptoms include {}.",
    "causes": "The main cause is {}.",
    "risk_factors": "People at higher risk may include {}.",
    "susceptibility": "People at higher risk may include {}.",
    "prevention": "Prevention includes {}.",
    "treatment": "Treatment may include {}.",
}


def _split_sentences(text):
    text = (text or "").strip()
    if not text:
        return []
    parts = re.split(r'(?<=[.!?])\s+', text)
    return [p.strip() for p in parts if p.strip()]


def _truncate_to_sentences(text, max_sentences):
    """Keeps only the first `max_sentences` sentences of `text`, exactly as
    retrieved — no rewording of the sentences themselves."""
    sentences = _split_sentences(text)
    if not sentences:
        return (text or "").strip()
    truncated = " ".join(sentences[:max_sentences])
    if not truncated.endswith((".", "!", "?")):
        truncated += "."
    return truncated


def format_structured_answer(raw_answer, question_type):
    """Wraps a raw structured-field value (e.g. a comma-separated symptom
    list) in a short natural-language sentence. The underlying words are
    the same words the backend returned — only the framing is added."""
    if not raw_answer:
        return raw_answer
    raw_clean = raw_answer.strip().rstrip(".")
    qt = (question_type or "").strip().lower()
    template = STRUCTURED_ANSWER_TEMPLATES.get(qt)
    if template:
        return template.format(raw_clean)
    return _truncate_to_sentences(raw_answer, 2)


def format_semantic_answer(raw_answer, question_type):
    """Shortens a MedQuAD / Wikipedia semantic-retrieval answer to at most
    2-3 sentences for display. Diagnosis answers get the same treatment —
    the most relevant leading sentences of the retrieved passage."""
    return _truncate_to_sentences(raw_answer, 3)


def render_assistant_metadata(message):
    """Renders metadata pills, knowledge-lookup card, out-of-domain card, or
    error card for a single assistant message — using only fields actually
    present on the message (never fabricated)."""

    if message.get("error_detail"):
        st.markdown(
            '<div class="error-card">Unable to process this question right now. Please try again.</div>',
            unsafe_allow_html=True
        )
        with st.expander("Technical Details"):
            st.code(message["error_detail"])
        return

    source = message.get("source")
    question_type = message.get("question_type")
    topic = message.get("current_topic")
    passage = message.get("passage")
    similarity = message.get("similarity")

    method, dataset, is_ood = classify_source(source)

    if is_ood:
        st.markdown(
            """
            <div class="ood-card">
                <div class="ood-card-title">OUT-OF-DOMAIN QUERY</div>
                <div class="ood-card-sub">No reliable medical source was found.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    chips = ""
    if source:
        chips += f'<span class="meta-chip chip-source">Source: {source}</span>'
    if method:
        chips += f'<span class="meta-chip chip-method">Method: {method}</span>'
    if dataset:
        chips += f'<span class="meta-chip chip-dataset">Dataset: {dataset}</span>'
    if question_type:
        chips += f'<span class="meta-chip chip-type">Type: {question_type}</span>'
    if topic:
        chips += f'<span class="meta-chip chip-topic">Topic: {topic}</span>'
    # Semantic Similarity only ever applies to genuine semantic retrieval
    # (MedQuAD / Medical Wikipedia). Structured Knowledge Base answers come
    # from an exact field lookup, so no similarity score is shown for them.
    if similarity is not None and dataset != "Structured Knowledge Base":
        try:
            chips += f'<span class="meta-chip chip-similarity">Semantic Similarity: {float(similarity):.2f}</span>'
        except (TypeError, ValueError):
            pass

    if chips:
        st.markdown(f'<div class="meta-row">{chips}</div>', unsafe_allow_html=True)

    if dataset == "Structured Knowledge Base":
        st.markdown(
            f"""
            <div class="knowledge-card">
                <div class="knowledge-card-title">KNOWLEDGE LOOKUP</div>
                <div class="knowledge-row"><span>Disease</span><b>{topic or '—'}</b></div>
                <div class="knowledge-row"><span>Matched Field</span><b>{question_type or '—'}</b></div>
                <div class="knowledge-row"><span>Retrieval Method</span><b>Structured Knowledge Lookup</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if passage:
        expander_title = "View Retrieved Knowledge" if dataset == "Structured Knowledge Base" else "View Retrieved Passage"
        with st.expander(expander_title):
            st.write(passage)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand-row">
            <div class="sidebar-brand-icon">🩺</div>
            <div>
                <div class="sidebar-brand">HEALTHCARE AI</div>
                <div class="sidebar-brand-sub">NLP QUESTION ANSWERING SYSTEM</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    NAV_ITEMS = [
        ("chat_assistant", "🩺  Chat Assistant", "Ask medical questions"),
        ("medical_knowledge", "📚  Medical Knowledge", "Explore information sources"),
        ("conversation_history", "🕘  Conversation History", "Review previous questions"),
    ]

    for section_key, nav_label, nav_sub in NAV_ITEMS:
        is_active = st.session_state.active_section == section_key
        clicked = st.button(
            nav_label,
            key=f"nav_{section_key}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        )
        sub_class = "nav-sub active" if is_active else "nav-sub"
        st.markdown(f'<div class="{sub_class}">{nav_sub}</div>', unsafe_allow_html=True)
        if clicked and not is_active:
            set_active_section(section_key)
            st.rerun()

    st.markdown(
        """
        <div class="status-card">
            <div class="status-card-title">SYSTEM STATUS</div>
            <div class="status-item">
                <span class="status-line-dot"></span>
                <div>
                    <div class="status-item-label">Retrieval Engine</div>
                    <div class="status-item-value">Online</div>
                </div>
            </div>
            <div class="status-item">
                <span class="status-line-dot"></span>
                <div>
                    <div class="status-item-label">Knowledge Base</div>
                    <div class="status-item-value">Ready</div>
                </div>
            </div>
            <div class="status-item">
                <span class="status-line-dot"></span>
                <div>
                    <div class="status-item-label">Semantic Search</div>
                    <div class="status-item-value">Active</div>
                </div>
            </div>
            <div class="status-footnote">All QA components operational</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="status-card">
            <div class="status-card-title">PROJECT</div>
            <div class="project-line">NLP QA SYSTEM</div>
            <div class="project-sub">IR + Knowledge-Based QA<br>Simple Dialogue Management</div>
            <div class="project-footnote">3 Information Sources</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.current_topic:
        session_turns = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
        st.markdown(
            f"""
            <div class="status-card">
                <div class="status-card-title">CURRENT SESSION</div>
                <div class="session-row"><span>Topic</span><b>{st.session_state.current_topic.capitalize()}</b></div>
                <div class="session-row"><span>Conversation Turns</span><b>{session_turns}</b></div>
                <div class="session-row"><span>Dialogue State</span><b>Active</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="status-card">
                <div class="status-card-title">CURRENT SESSION</div>
                <div class="session-empty">No active topic</div>
                <div class="session-empty-sub">Start a conversation below</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.button("🗑️  Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_topic = None
        st.session_state.pending_question = None
        st.rerun()

    st.markdown(
        """
        <div class="sidebar-footer">
            Healthcare QA System<br>
            Information Retrieval • Knowledge QA • Dialogue
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-wrap">
        <div class="hero-badge">AI-POWERED HEALTHCARE ASSISTANT</div>
        <div class="hero-title">🩺 Healthcare QA Chatbot</div>
        <div class="hero-subtitle">Semantic retrieval and knowledge-based question answering for medical information.</div>
        <div class="status-pill"><span class="status-dot"></span> AI SYSTEM ONLINE</div>
    </div>
    """,
    unsafe_allow_html=True
)



# ============================================================
# CONVERSATION RENDERER (shared by Chat Assistant + Conversation History)
# ============================================================

def render_conversation_section(empty_hint=None):
    st.markdown('<div class="section-heading">Conversation</div>', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown(
            f"""
            <div class="empty-state">
                <div class="empty-state-icon">✦</div>
                <div class="empty-state-title">Your medical questions, answered intelligently.</div>
                <div class="empty-state-sub">{empty_hint or "Ask about symptoms, causes, prevention, diagnosis or treatment."}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        for message in st.session_state.messages:

            if message["role"] == "user":
                with st.chat_message("user", avatar=USER_AVATAR):
                    st.write(message["content"])

            else:
                with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
                    if message.get("error_detail"):
                        st.write(message["content"])
                    else:
                        safe_answer = html_lib.escape(message["content"] or "").replace("\n", "<br>")
                        st.markdown(f'<div class="answer-text">{safe_answer}</div>', unsafe_allow_html=True)
                    render_assistant_metadata(message)


# ============================================================
# SAMPLE QUESTIONS — "EXPLORE COMMON QUESTIONS"
# ============================================================

def render_question_group(key_prefix):
    for group_name, questions in QUESTION_GROUPS.items():
        st.markdown(f'<div class="group-heading">{group_name}</div>', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, q in enumerate(questions):
            with cols[i % 2]:
                st.button(
                    q,
                    key=f"{key_prefix}_{group_name}_{i}",
                    on_click=queue_question,
                    args=(q,),
                    use_container_width=True
                )


# ============================================================
# MAIN CONTENT — switches with the sidebar navigation
# ============================================================

if st.session_state.active_section == "medical_knowledge":
    # ============================================================
    # SYSTEM OVERVIEW
    # ============================================================

    st.markdown('<div class="section-heading">System Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheading">Results from the project evaluation set and knowledge sources.</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="metric-card"><div class="metric-value">100%</div><div class="metric-label">Question-Type Accuracy</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="metric-card"><div class="metric-value">100%</div><div class="metric-label">Disease Detection Accuracy</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="metric-card"><div class="metric-value">100%</div><div class="metric-label">Out-of-Domain Rejection</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="metric-card"><div class="metric-value">20</div><div class="metric-label">Evaluation Questions</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:9px'></div>", unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown('<div class="metric-card"><div class="metric-value">19,498</div><div class="metric-label">Medical Wikipedia Records</div></div>', unsafe_allow_html=True)
    with d2:
        st.markdown('<div class="metric-card"><div class="metric-value">16,407</div><div class="metric-label">MedQuAD Questions</div></div>', unsafe_allow_html=True)
    with d3:
        st.markdown('<div class="metric-card"><div class="metric-value">6</div><div class="metric-label">Structured Knowledge Fields</div></div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-rule">', unsafe_allow_html=True)


    # ============================================================
    # QA PIPELINE
    # ============================================================

    st.markdown('<div class="section-heading">QA Pipeline</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheading">How a question flows through retrieval and dialogue management.</div>', unsafe_allow_html=True)

    pipeline_html = '<div class="pipeline-wrap">'
    for i, (title, sub) in enumerate(PIPELINE_STEPS):
        pipeline_html += f'<div class="pipeline-card">{title}<div class="pipeline-sub">{sub}</div></div>'
        if i < len(PIPELINE_STEPS) - 1:
            pipeline_html += '<div class="pipeline-arrow">↓</div>'
    pipeline_html += '</div>'
    st.markdown(pipeline_html, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="pipeline-tag-row">
            <span class="pipeline-tag ir">IR-BASED QA</span>
            <span class="pipeline-tag kb">KNOWLEDGE-BASED QA</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<hr class="section-rule">', unsafe_allow_html=True)


    # ============================================================
    # INFORMATION SOURCES
    # ============================================================

    st.markdown('<div class="section-heading">Information Sources</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheading">Structured and semantic sources the retrieval engine draws from.</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="source-card">
            <div class="source-card-title">MedQuAD</div>
            <div class="source-card-sub">16,407 medical QA pairs</div>
            <div class="source-card-desc">Semantic information retrieval source</div>
        </div>
        <div class="source-card">
            <div class="source-card-title">Medical Wikipedia</div>
            <div class="source-card-sub">19,498 medical records</div>
            <div class="source-card-desc">Semantic retrieval source for broader medical information</div>
        </div>
        <div class="source-card">
            <div class="source-card-title">Structured Knowledge Base</div>
            <div class="source-card-sub">6 disease-specific fields</div>
            <div class="source-card-desc">Symptoms, causes, risk factors, prevention and treatment</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<hr class="section-rule">', unsafe_allow_html=True)


    # ============================================================
    # DIALOGUE FLOW (expandable)
    # ============================================================

    with st.expander("🔀  Dialogue Flow"):
        flow_html = ""
        for i, step in enumerate(DIALOGUE_FLOW_STEPS):
            flow_html += f'<div class="flow-line"><b>{step}</b></div>'
            if i < len(DIALOGUE_FLOW_STEPS) - 1:
                flow_html += '<div class="flow-arrow">↓</div>'
        st.markdown(flow_html, unsafe_allow_html=True)
        st.caption("This is the frame-based dialogue design used to resolve follow-up questions with the stored current topic.")


    # ============================================================
    # EVALUATION SUMMARY (expandable)
    # ============================================================

    with st.expander("📊  Evaluation Summary"):
        st.markdown(
            """
            <div class="eval-row"><span>Question-Type Accuracy</span><span class="eval-score">20/20 (100%)</span></div>
            <div class="eval-row"><span>Disease Detection Accuracy</span><span class="eval-score">20/20 (100%)</span></div>
            <div class="eval-row"><span>Out-of-Domain Rejection</span><span class="eval-score">2/2 (100%)</span></div>
            """,
            unsafe_allow_html=True
        )
        st.caption("Evaluation performed offline using qa_test_set.csv and evaluate.py. This summary is static and is not re-run by the app.")


    # ============================================================
    # SAMPLE QUESTION-ANSWER SET (expandable)
    # ============================================================

    with st.expander("📝  Sample Question-Answer Set"):
        for q, a in SAMPLE_QA_STATIC:
            st.markdown(
                f"""
                <div class="qa-pair">
                    <div class="qa-q">Q: {q}</div>
                    <div class="qa-a">A: {a}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        live_answer = get_live_answer(SAMPLE_QA_DYNAMIC_QUESTION)
        if live_answer:
            st.markdown(
                f"""
                <div class="qa-pair">
                    <div class="qa-q">Q: {SAMPLE_QA_DYNAMIC_QUESTION}</div>
                    <div class="qa-a">A: {live_answer}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="qa-pair">
                    <div class="qa-q">Q: {SAMPLE_QA_DYNAMIC_QUESTION}</div>
                    <div class="qa-note">Ask this question in the chat below to see the live answer returned by the backend.</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown('<hr class="section-rule">', unsafe_allow_html=True)

elif st.session_state.active_section == "conversation_history":

    render_conversation_section(
        empty_hint="No questions yet — ask one from the Chat Assistant tab to see it here."
    )

else:  # "chat_assistant" (default)

    st.markdown('<div class="section-heading">Explore Common Questions</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheading">Tap a question to send it through the chatbot, or type your own below.</div>', unsafe_allow_html=True)
    render_question_group("explore")

    st.markdown('<hr class="section-rule">', unsafe_allow_html=True)

    # ============================================================
    # DIALOGUE CONTEXT / ACTIVE TOPIC
    # ============================================================

    if st.session_state.current_topic:
        turns = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
        st.markdown(
            f"""
            <div class="topic-badge">
                <span class="topic-label">ACTIVE MEDICAL TOPIC</span>
                {st.session_state.current_topic.capitalize()}
            </div>
            <div class="dialogue-context">Current Topic: {st.session_state.current_topic} &nbsp;·&nbsp; Conversation turns: {turns}</div>
            """,
            unsafe_allow_html=True
        )

    # ============================================================
    # CONVERSATION
    # ============================================================

    st.markdown('<div class="section-heading">Conversation</div>', unsafe_allow_html=True)

    if not st.session_state.messages:

        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-state-icon">✦</div>
                <div class="empty-state-title">Your medical questions, answered intelligently.</div>
                <div class="empty-state-sub">Ask about symptoms, causes, prevention, diagnosis or treatment.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        for message in st.session_state.messages:

            if message["role"] == "user":
                with st.chat_message("user", avatar=USER_AVATAR):
                    st.write(message["content"])

            else:
                with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
                    if message.get("error_detail"):
                        st.write(message["content"])
                    else:
                        safe_answer = html_lib.escape(message["content"] or "").replace("\n", "<br>")
                        st.markdown(f'<div class="answer-text">{safe_answer}</div>', unsafe_allow_html=True)
                    render_assistant_metadata(message)



# ============================================================
# PROCESS A QUESTION (shared by quick-question clicks and chat input)
# ============================================================

def process_question(question):

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    try:
        with st.spinner("Analyzing your question..."):
            result = healthcare_chat(
                question,
                st.session_state.current_topic
            )

        raw_answer = result.get("answer", "I'm sorry, I could not find a reliable answer.")
        source = result.get("source", "No reliable source")
        question_type = result.get("question_type", "unknown")
        current_topic = result.get("current_topic", st.session_state.current_topic)
        backend_passage = result.get("passage") or result.get("retrieved_passage")
        similarity = result.get("similarity")
        if similarity is None:
            similarity = result.get("semantic_similarity")
        if similarity is None:
            similarity = result.get("score")

        st.session_state.current_topic = current_topic

        # Turn the raw retrieved value into a short, natural-sounding
        # answer for display. This never changes retrieval, classification,
        # or the underlying facts — only how the same text is presented.
        method, dataset, is_ood = classify_source(source)

        if is_ood:
            display_answer = raw_answer
        elif dataset == "Structured Knowledge Base":
            display_answer = format_structured_answer(raw_answer, question_type)
        elif method == "Semantic Embedding Retrieval":
            display_answer = format_semantic_answer(raw_answer, question_type)
        else:
            display_answer = raw_answer

        # Always keep the full original text available in the "View
        # Retrieved Passage" expander when the display answer shortened it.
        passage = backend_passage
        if not passage and raw_answer and raw_answer.strip() != display_answer.strip():
            passage = raw_answer

        st.session_state.messages.append({
            "role": "assistant",
            "content": display_answer,
            "source": source,
            "question_type": question_type,
            "current_topic": current_topic,
            "passage": passage,
            "similarity": similarity,
        })

    except Exception as e:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Unable to process this question right now. Please try again.",
            "error_detail": f"{type(e).__name__}: {e}",
        })

# ============================================================
# HANDLE QUICK-QUESTION CLICK
# ============================================================

if st.session_state.pending_question:
    q = st.session_state.pending_question
    st.session_state.pending_question = None
    process_question(q)
    st.rerun()

# ============================================================
# CHAT INPUT (Chat Assistant view only)
# ============================================================

if st.session_state.active_section == "chat_assistant":

    question = st.chat_input("Ask about symptoms, causes, prevention, diagnosis...")

    if question:
        process_question(question)
        st.rerun()

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="app-footer">
        AI-generated information is for educational purposes only<br>
        and does not replace professional medical advice.
    </div>
    """,
    unsafe_allow_html=True
)