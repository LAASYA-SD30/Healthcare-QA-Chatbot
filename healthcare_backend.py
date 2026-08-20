import os
import re
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# FILE PATHS
# ============================================================

KNOWLEDGE_FILE = os.path.join(
    BASE_DIR,
    "healthcare_knowledge.csv"
)

MEDQUAD_FILE = os.path.join(
    BASE_DIR,
    "medquad-cleaned-qa.csv"
)

WIKI_FILE = os.path.join(
    BASE_DIR,
    "medical_wikipedia_facts.csv"
)


# ============================================================
# LOAD STRUCTURED HEALTHCARE KNOWLEDGE
# ============================================================

knowledge_base = pd.read_csv(
    KNOWLEDGE_FILE
)

knowledge_base.columns = [
    str(column).strip().lower()
    for column in knowledge_base.columns
]


# ============================================================
# CHECK REQUIRED KNOWLEDGE COLUMNS
# ============================================================

required_columns = [
    "disease",
    "symptoms",
    "causes",
    "risk_factors",
    "prevention",
    "treatment"
]

missing_columns = [
    column
    for column in required_columns
    if column not in knowledge_base.columns
]

if missing_columns:

    raise ValueError(
        "healthcare_knowledge.csv is missing columns: "
        + ", ".join(missing_columns)
    )


# ============================================================
# DISEASE LIST
# ============================================================

DISEASES = sorted(
    knowledge_base["disease"]
    .dropna()
    .astype(str)
    .str.lower()
    .str.strip()
    .unique(),
    key=len,
    reverse=True
)


# ============================================================
# LOAD MEDQUAD DATASET
# ============================================================

print()
print("=" * 70)
print("Loading MedQuAD dataset...")
print("=" * 70)

retrieval_df = pd.read_csv(
    MEDQUAD_FILE
)


# ============================================================
# NORMALIZE COLUMN NAMES
# ============================================================

retrieval_df.columns = [
    str(column).strip().lower()
    for column in retrieval_df.columns
]

print(
    "MedQuAD columns found:",
    retrieval_df.columns.tolist()
)


# ============================================================
# FIND QUESTION COLUMN
# ============================================================

question_candidates = [

    "question",
    "questions",
    "question_text",
    "questiontext",
    "query",
    "queries",
    "input",
    "prompt"
]

question_column = None

for column in question_candidates:

    if column in retrieval_df.columns:

        question_column = column

        break


# ============================================================
# FIND ANSWER COLUMN
# ============================================================

answer_candidates = [

    "answer",
    "answers",
    "answer_text",
    "answertext",
    "response",
    "responses",
    "output",
    "text"
]

answer_column = None

for column in answer_candidates:

    if column in retrieval_df.columns:

        answer_column = column

        break


# ============================================================
# FALLBACK: SEARCH COLUMN NAMES
# ============================================================

if question_column is None:

    for column in retrieval_df.columns:

        column_lower = str(
            column
        ).lower()

        if (
            "question" in column_lower
            or "query" in column_lower
        ):

            question_column = column

            break


if answer_column is None:

    for column in retrieval_df.columns:

        column_lower = str(
            column
        ).lower()

        if (
            "answer" in column_lower
            or "response" in column_lower
        ):

            answer_column = column

            break


# ============================================================
# VALIDATE COLUMNS
# ============================================================

if question_column is None:

    raise ValueError(
        "Could not identify the question column "
        "in medquad-cleaned-qa.csv.\n\n"
        "Columns found:\n"
        + str(retrieval_df.columns.tolist())
    )


if answer_column is None:

    raise ValueError(
        "Could not identify the answer column "
        "in medquad-cleaned-qa.csv.\n\n"
        "Columns found:\n"
        + str(retrieval_df.columns.tolist())
    )


print(
    "Using question column:",
    question_column
)

print(
    "Using answer column:",
    answer_column
)


# ============================================================
# STANDARDIZE COLUMN NAMES
# ============================================================

retrieval_df = retrieval_df.rename(
    columns={
        question_column: "question",
        answer_column: "answer"
    }
)


# ============================================================
# CLEAN MEDQUAD TEXT
# ============================================================

retrieval_df["question"] = (
    retrieval_df["question"]
    .fillna("")
    .astype(str)
)

retrieval_df["answer"] = (
    retrieval_df["answer"]
    .fillna("")
    .astype(str)
)


# Remove empty rows

retrieval_df = retrieval_df[
    (
        retrieval_df["question"]
        .str.strip()
        != ""
    )
    &
    (
        retrieval_df["answer"]
        .str.strip()
        != ""
    )
].reset_index(drop=True)


print(
    "MedQuAD rows:",
    len(retrieval_df)
)


# ============================================================
# ANSWER CLEANING
# ============================================================

def clean_answer(answer):

    if answer is None:

        return ""

    answer = str(answer)

    answer = re.sub(
        r"^\s*Espaol\s*",
        "",
        answer,
        flags=re.IGNORECASE
    )

    answer = re.sub(
        r"\s+",
        " ",
        answer
    )

    answer = answer.replace(
        "metabolismthe",
        "metabolism, the"
    )

    answer = answer.replace(
        "carbohydratessugars",
        "carbohydrates, sugars"
    )

    answer = answer.replace(
        "organsparticularly",
        "organs, particularly"
    )

    answer = answer.replace(
        "brainand",
        "brain, and"
    )

    answer = re.sub(
        r"\s+([,.!?;:])",
        r"\1",
        answer
    )

    return answer.strip()


retrieval_df["clean_answer"] = (
    retrieval_df["answer"]
    .apply(clean_answer)
)


# ============================================================
# LOAD MEDICAL WIKIPEDIA DATASET
# ============================================================

print()
print("=" * 70)
print("Loading Medical Wikipedia dataset...")
print("=" * 70)

wiki_df = pd.read_csv(
    WIKI_FILE
)

wiki_df.columns = [
    str(column).strip().lower()
    for column in wiki_df.columns
]


# ============================================================
# WIKIPEDIA TEXT
# ============================================================

if "text" in wiki_df.columns:

    wiki_df["text"] = (
        wiki_df["text"]
        .fillna("")
        .astype(str)
    )

else:

    wiki_df["text"] = ""


if "medical_area" in wiki_df.columns:

    medical_area = (
        wiki_df["medical_area"]
        .fillna("")
        .astype(str)
    )

else:

    medical_area = pd.Series(
        "",
        index=wiki_df.index
    )


if "tags" in wiki_df.columns:

    tags = (
        wiki_df["tags"]
        .fillna("")
        .astype(str)
    )

else:

    tags = pd.Series(
        "",
        index=wiki_df.index
    )


wiki_semantic_text = (
    wiki_df["text"]
    + " "
    + medical_area
    + " "
    + tags
)


# ============================================================
# LOAD SEMANTIC MODEL
# ============================================================

print()
print("=" * 70)
print("Loading semantic model...")
print("=" * 70)

semantic_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print(
    "Semantic model loaded successfully."
)


# ============================================================
# CREATE MEDQUAD EMBEDDINGS
# ============================================================

print()
print("=" * 70)
print("Creating MedQuAD embeddings...")
print("=" * 70)

medquad_texts = (
    retrieval_df["question"]
    + " "
    + retrieval_df["clean_answer"]
)

medquad_embeddings = semantic_model.encode(
    medquad_texts.tolist(),
    show_progress_bar=True,
    normalize_embeddings=True
)

print(
    "MedQuAD embeddings created."
)

print(
    "Shape:",
    medquad_embeddings.shape
)


# ============================================================
# CREATE WIKIPEDIA EMBEDDINGS
# ============================================================

print()
print("=" * 70)
print("Creating Medical Wikipedia embeddings...")
print("=" * 70)

wiki_embeddings = semantic_model.encode(
    wiki_semantic_text.tolist(),
    show_progress_bar=True,
    normalize_embeddings=True
)

print(
    "Medical Wikipedia embeddings created."
)

print(
    "Shape:",
    wiki_embeddings.shape
)


# ============================================================
# DIALOGUE DETECTION
# ============================================================

def is_dialogue_input(text):

    text = text.lower().strip()


    greetings = [

        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]


    thanks = [

        "thanks",
        "thank you",
        "thankyou"
    ]


    exits = [

        "exit",
        "quit",
        "bye",
        "goodbye"
    ]


    if text in greetings:

        return "greeting"


    if text in thanks:

        return "thanks"


    if text in exits:

        return "exit"


    return None


# ============================================================
# DISEASE DETECTION
# ============================================================

def detect_disease(question):

    q = question.lower().strip()


    # --------------------------------------------------------
    # Direct disease-name matching
    # --------------------------------------------------------

    for disease in DISEASES:

        if disease in q:

            return disease


    # --------------------------------------------------------
    # Disease aliases
    # --------------------------------------------------------

    aliases = {

        "tb":
            "tuberculosis",

        "t.b.":
            "tuberculosis",

        "tubercular":
            "tuberculosis",

        "tuberculous":
            "tuberculosis"
    }


    for alias, disease in aliases.items():

        if (
            alias in q
            and disease in DISEASES
        ):

            return disease


    return None


# ============================================================
# QUESTION TYPE DETECTION
# ============================================================

def detect_question_type(question):

    q = question.lower().strip()


    # --------------------------------------------------------
    # Symptoms
    # --------------------------------------------------------

    if (
        "symptom" in q
        or "signs" in q
        or "sign of" in q
        or "symptoms" in q
    ):

        return "symptoms"


    # --------------------------------------------------------
    # Causes
    # --------------------------------------------------------

    if (
        "cause" in q
        or "caused" in q
        or "why does" in q
        or "why do" in q
    ):

        return "causes"


    # --------------------------------------------------------
    # Susceptibility / Risk
    # --------------------------------------------------------

    if (
        "risk" in q
        or "at risk" in q
        or "susceptible" in q
        or "vulnerable" in q
    ):

        return "susceptibility"


    # --------------------------------------------------------
    # Prevention
    # --------------------------------------------------------

    if (
        "prevent" in q
        or "prevention" in q
        or "avoid" in q
    ):

        return "prevention"


    # --------------------------------------------------------
    # Treatment
    # --------------------------------------------------------

    if (
        "treatment" in q
        or "treated" in q
        or "cure" in q
        or "therapy" in q
        or "solve" in q
        or "manage" in q
        or "management" in q
        or "remedy" in q
        or "what should i do" in q
        or "what can i do" in q
    ):

        return "treatment"


    # --------------------------------------------------------
    # Diagnosis / Tests
    # --------------------------------------------------------

    if (
        "diagnos" in q
        or "test" in q
        or "tests" in q
        or "exam" in q
        or "examination" in q
        or "screening" in q
        or "detect" in q
    ):

        return "exams and tests"


    # --------------------------------------------------------
    # General information
    # --------------------------------------------------------

    return "information"


# ============================================================
# SYMPTOM STATEMENT DETECTION
# ============================================================

def detect_symptom_statement(question):

    question = question.lower().strip()


    symptom_patterns = [

        "i have a ",
        "i have ",
        "i am feeling ",
        "i feel ",
        "i'm feeling ",
        "my head hurts",
        "my stomach hurts",
        "my stomach is hurting",
        "my abdomen hurts",
        "i'm experiencing ",
        "i am experiencing ",
        "i am suffering from ",
        "i'm suffering from "
    ]


    return any(
        question.startswith(pattern)
        for pattern in symptom_patterns
    )


# ============================================================
# FOLLOW-UP QUESTION DETECTION
# ============================================================

def is_followup_question(text):

    text = text.lower().strip()


    followup_phrases = [

        "it",
        "this",
        "that",
        "its",

        "the disease",
        "the condition",
        "the illness",
        "the infection",

        "the symptoms",
        "the symptom",

        "the treatment",
        "the cure",

        "the cause",
        "the causes",

        "the prevention",

        "the risk",

        "how to solve it",
        "how do i solve it",
        "how can i solve it",

        "how to treat it",
        "how can i treat it",
        "how is it treated",

        "how to cure it",
        "how can i cure it",

        "how to manage it",
        "how can i manage it",

        "what should i do",
        "what can i do"
    ]


    for phrase in followup_phrases:

        if phrase in text:

            return True


    return False


# ============================================================
# STRUCTURED KNOWLEDGE BASE ANSWER
# ============================================================

def structured_context_answer(
    question,
    disease,
    question_type
):

    if disease is None:

        return None


    column_map = {

        "symptoms":
            "symptoms",

        "causes":
            "causes",

        "susceptibility":
            "risk_factors",

        "prevention":
            "prevention",

        "treatment":
            "treatment"
    }


    column = column_map.get(
        question_type
    )


    # Diagnosis questions are handled
    # by semantic retrieval.

    if column is None:

        return None


    matches = knowledge_base[
        knowledge_base["disease"]
        .astype(str)
        .str.lower()
        .str.strip()
        == disease.lower().strip()
    ]


    if matches.empty:

        return None


    answer = matches.iloc[0][
        column
    ]


    if (
        answer is None
        or str(answer).strip() == ""
        or str(answer).lower() == "nan"
    ):

        return None


    return {

        "answer":
            str(answer),

        "source":
            "Structured Knowledge Base",

        "question_type":
            question_type,

        "similarity":
            1.0
    }


# ============================================================
# MEDQUAD SEMANTIC RETRIEVAL
# ============================================================

def retrieve_medquad_semantic(
    question,
    top_k=5,
    threshold=0.45
):

    query_embedding = semantic_model.encode(
        [question],
        normalize_embeddings=True
    )


    similarities = (
        medquad_embeddings
        @ query_embedding[0]
    )


    top_indices = (
        similarities
        .argsort()[-top_k:][::-1]
    )


    results = retrieval_df.iloc[
        top_indices
    ].copy()


    results["similarity"] = (
        similarities[top_indices]
    )


    results = results[
        results["similarity"]
        >= threshold
    ]


    return results


# ============================================================
# TOPIC-FILTERED MEDQUAD RETRIEVAL
# ============================================================

def topic_filtered_semantic_qa(
    question,
    topic,
    top_k=5,
    threshold=0.35
):

    if topic is None:

        return None


    topic = str(
        topic
    ).lower().strip()


    query_embedding = semantic_model.encode(
        [question],
        normalize_embeddings=True
    )


    similarities = (
        medquad_embeddings
        @ query_embedding[0]
    )


    temp_df = retrieval_df.copy()


    temp_df["similarity"] = (
        similarities
    )


    # Search disease name in question
    # and answer fields.

    topic_pattern = (
        r"\b"
        + re.escape(topic)
        + r"\b"
    )


    question_match = (
        temp_df["question"]
        .str.lower()
        .str.contains(
            topic_pattern,
            regex=True,
            na=False
        )
    )


    answer_match = (
        temp_df["clean_answer"]
        .str.lower()
        .str.contains(
            topic_pattern,
            regex=True,
            na=False
        )
    )


    filtered_df = temp_df[
        question_match
        | answer_match
    ].copy()


    if filtered_df.empty:

        return None


    filtered_df = filtered_df.sort_values(
        "similarity",
        ascending=False
    ).head(top_k)


    if filtered_df.empty:

        return None


    best = filtered_df.iloc[0]


    if (
        float(best["similarity"])
        < threshold
    ):

        return None


    return {

        "answer":
            clean_answer(
                best["clean_answer"]
            ),

        "source":
            "MedQuAD Semantic IR",

        "question_type":
            detect_question_type(
                question
            ),

        "similarity":
            float(
                best["similarity"]
            )
    }


# ============================================================
# WIKIPEDIA SEMANTIC RETRIEVAL
# ============================================================

def retrieve_wikipedia_semantic(
    question,
    top_k=3,
    threshold=0.45
):

    query_embedding = semantic_model.encode(
        [question],
        normalize_embeddings=True
    )


    similarities = (
        wiki_embeddings
        @ query_embedding[0]
    )


    top_indices = (
        similarities
        .argsort()[-top_k:][::-1]
    )


    results = wiki_df.iloc[
        top_indices
    ].copy()


    results["similarity"] = (
        similarities[top_indices]
    )


    results = results[
        results["similarity"]
        >= threshold
    ]


    return results


# ============================================================
# MEDQUAD ANSWER
# ============================================================

def medquad_answer(
    question,
    topic=None
):

    # --------------------------------------------------------
    # Topic-aware retrieval
    # --------------------------------------------------------

    if topic is not None:

        topic_result = (
            topic_filtered_semantic_qa(
                question,
                topic,
                top_k=5,
                threshold=0.35
            )
        )


        if topic_result is not None:

            topic_result[
                "question_type"
            ] = detect_question_type(
                question
            )

            return topic_result


    # --------------------------------------------------------
    # General semantic retrieval
    # --------------------------------------------------------

    results = retrieve_medquad_semantic(
        question,
        top_k=5,
        threshold=0.45
    )


    if results.empty:

        return None


    best = results.iloc[0]


    return {

        "answer":
            clean_answer(
                best["clean_answer"]
            ),

        "source":
            "MedQuAD Semantic IR",

        "question_type":
            detect_question_type(
                question
            ),

        "similarity":
            float(
                best["similarity"]
            )
    }


# ============================================================
# WIKIPEDIA ANSWER
# ============================================================

def wikipedia_answer(question):

    results = retrieve_wikipedia_semantic(
        question,
        top_k=3,
        threshold=0.45
    )


    if results.empty:

        return None


    best = results.iloc[0]


    answer = clean_answer(
        best["text"]
    )


    if not answer:

        return None


    return {

        "answer":
            answer,

        "source":
            "Medical Wikipedia Semantic IR",

        "question_type":
            detect_question_type(
                question
            ),

        "similarity":
            float(
                best["similarity"]
            )
    }


# ============================================================
# MULTI-SOURCE QA
# ============================================================

def multi_source_qa(
    question,
    current_topic=None
):

    question = question.strip()


    # ========================================================
    # DIALOGUE
    # ========================================================

    dialogue = is_dialogue_input(
        question
    )


    if dialogue == "greeting":

        return {

            "answer":
                "Hello! I'm a healthcare QA assistant. "
                "Ask me a healthcare-related question.",

            "source":
                "Dialogue Manager",

            "question_type":
                "dialogue",

            "similarity":
                1.0
        }


    if dialogue == "thanks":

        return {

            "answer":
                "You're welcome!",

            "source":
                "Dialogue Manager",

            "question_type":
                "dialogue",

            "similarity":
                1.0
        }


    if dialogue == "exit":

        return {

            "answer":
                "Thank you. Goodbye!",

            "source":
                "Dialogue Manager",

            "question_type":
                "dialogue",

            "similarity":
                1.0
        }


    # ========================================================
    # DETECT DISEASE
    # ========================================================

    detected_disease = detect_disease(
        question
    )


    detected_type = detect_question_type(
        question
    )


    # ========================================================
    # SYMPTOM STATEMENT
    # ========================================================

    if detect_symptom_statement(
        question
    ):

        result = medquad_answer(
            question,
            topic=None
        )


        if result is None:

            return {

                "answer":
                    "I'm sorry, I could not find "
                    "a reliable answer to that question.",

                "source":
                    "No reliable source",

                "question_type":
                    "unknown",

                "similarity":
                    0.0
            }


        result[
            "question_type"
        ] = "symptom_statement"


        return result


    # ========================================================
    # DETERMINE CURRENT TOPIC
    # ========================================================

    topic = detected_disease


    if (
        topic is None
        and current_topic is not None
        and is_followup_question(question)
    ):

        topic = current_topic


    # ========================================================
    # STRUCTURED KNOWLEDGE BASE
    # ========================================================

    if topic is not None:

        structured_result = (
            structured_context_answer(
                question,
                topic,
                detected_type
            )
        )


        if structured_result is not None:

            structured_result[
                "current_topic"
            ] = topic

            return structured_result


    # ========================================================
    # MEDQUAD SEMANTIC RETRIEVAL
    # ========================================================

    medquad_result = medquad_answer(
        question,
        topic=topic
    )


    if medquad_result is not None:

        if detected_disease is not None:

            medquad_result[
                "current_topic"
            ] = detected_disease

        else:

            medquad_result[
                "current_topic"
            ] = topic


        if (
            detected_type
            == "exams and tests"
        ):

            medquad_result[
                "question_type"
            ] = "exams and tests"


        return medquad_result


    # ========================================================
    # WIKIPEDIA RETRIEVAL
    # ========================================================

    wiki_result = wikipedia_answer(
        question
    )


    if wiki_result is not None:

        if detected_disease is not None:

            wiki_result[
                "current_topic"
            ] = detected_disease

        else:

            wiki_result[
                "current_topic"
            ] = topic


        return wiki_result


    # ========================================================
    # SAFE FALLBACK
    # ========================================================

    return {

        "answer":
            "I'm sorry, I could not find "
            "a reliable answer to that question.",

        "source":
            "No reliable source",

        "question_type":
            "unknown",

        "similarity":
            0.0,

        "current_topic":
            topic
    }


# ============================================================
# MAIN CHAT FUNCTION
# ============================================================

def healthcare_chat(
    question,
    current_topic=None
):

    question = str(
        question
    ).strip()


    # ========================================================
    # EMPTY QUESTION
    # ========================================================

    if not question:

        return {

            "answer":
                "Please enter a healthcare question.",

            "source":
                "Dialogue Manager",

            "question_type":
                "dialogue",

            "similarity":
                1.0,

            "current_topic":
                current_topic
        }


    # ========================================================
    # DIALOGUE
    # ========================================================

    dialogue = is_dialogue_input(
        question
    )


    if dialogue == "greeting":

        return {

            "answer":
                "Hello! I'm a healthcare QA assistant. "
                "Ask me a healthcare-related question.",

            "source":
                "Dialogue Manager",

            "question_type":
                "dialogue",

            "similarity":
                1.0,

            "current_topic":
                current_topic
        }


    if dialogue == "thanks":

        return {

            "answer":
                "You're welcome!",

            "source":
                "Dialogue Manager",

            "question_type":
                "dialogue",

            "similarity":
                1.0,

            "current_topic":
                current_topic
        }


    if dialogue == "exit":

        return {

            "answer":
                "Thank you. Goodbye!",

            "source":
                "Dialogue Manager",

            "question_type":
                "dialogue",

            "similarity":
                1.0,

            "current_topic":
                None
        }


    # ========================================================
    # DETECT DISEASE
    # ========================================================

    detected_disease = detect_disease(
        question
    )


    # ========================================================
    # RUN QA
    # ========================================================

    result = multi_source_qa(
        question,
        current_topic=current_topic
    )


    # ========================================================
    # UPDATE CURRENT TOPIC
    # ========================================================

    if detected_disease is not None:

        result[
            "current_topic"
        ] = detected_disease

    elif (
        current_topic is not None
        and is_followup_question(question)
    ):

        result[
            "current_topic"
        ] = current_topic

    else:

        result[
            "current_topic"
        ] = result.get(
            "current_topic",
            current_topic
        )


    return result


# ============================================================
# TERMINAL TEST
# ============================================================

if __name__ == "__main__":

    test_questions = [

        "What are the symptoms of malaria?",

        "Who is at risk for it?",

        "How can it be prevented?",

        "What causes it?",

        "How is tuberculosis diagnosed?",

        "I have a headache",

        "I am feeling dizzy",

        "Who won the FIFA World Cup?"

    ]


    current_topic = None


    for question in test_questions:

        result = healthcare_chat(
            question,
            current_topic
        )


        current_topic = result.get(
            "current_topic"
        )


        print()
        print("=" * 70)
        print(
            "USER:",
            question
        )

        print(
            "BOT:",
            result.get(
                "answer"
            )
        )

        print(
            "SOURCE:",
            result.get(
                "source"
            )
        )

        print(
            "TYPE:",
            result.get(
                "question_type"
            )
        )

        print(
            "CURRENT TOPIC:",
            current_topic
        )