# Healthcare QA Chatbot

## Project Information

**Student Name:** Laasya S D  
**USN:** 1GA23AI021  
**Department:** Artificial Intelligence and Machine Learning  

**Project Title:** Healthcare Question Answering Chatbot using Information Retrieval, Knowledge-Based QA and Dialogue Management

---

## 1. Objective

To design a QA and chatbot system that supports IR-based factoid answering, knowledge-based QA, and simple dialogue management using one or more information sources.

### Expected Outcomes

- Retrieve relevant passages for a question.
- Extract factoid answers from text.
- Query structured knowledge sources.
- Handle simple conversational interactions.
- Evaluate answer quality.

---

## 2. Project Overview

The Healthcare QA Chatbot is an NLP-based question answering system that answers healthcare-related questions using multiple information sources.

The system combines:

- Question classification
- Disease/topic detection
- Semantic information retrieval
- Structured knowledge-based QA
- Factoid answering
- Simple dialogue management
- Out-of-domain rejection
- Evaluation of QA performance

The application is developed using Streamlit and provides an interactive chatbot interface.

---

## 3. Information Sources

The system uses three main sources:

| Source | Purpose |
|---|---|
| MedQuAD | Semantic medical question-answer retrieval |
| Medical Wikipedia | Semantic retrieval of broader medical information |
| Structured Knowledge Base | Disease-specific facts such as symptoms, causes, risk factors and prevention |

### Dataset Size

- MedQuAD: 16,407 records
- Medical Wikipedia: 19,498 records
- Evaluation Set: 20 questions

---

## 4. System Workflow

```text
User Question
      ↓
Question Classification
      ↓
Disease / Topic Detection
      ↓
Retrieval Selection
      ↓
 ┌───────────────────────┐
 │                       │
 ▼                       ▼
Structured Knowledge   Semantic Retrieval
Lookup                    ↓
 │                   Relevant Passage
 └──────────┬────────────┘
            ↓
      Answer Generation
            ↓
    Dialogue State Update
            ↓
         Response

## 5.How to Run
pip install -r requirements.txt
streamlit run app.py


## 6. Evaluation
Question-Type Accuracy: 100% (20/20)
Disease-Detection Accuracy: 100% (20/20)
Out-of-Domain Rejection: 100% (2/2)
