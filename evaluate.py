"""
HEALTHCARE QA CHATBOT
EVALUATION SCRIPT

Runs qa_test_set.csv through healthcare_chat()
and evaluates:

1. Disease detection accuracy
2. Question type accuracy
3. Out-of-domain rejection accuracy

Run:

    python evaluate.py
"""


import csv
import os

from healthcare_backend import healthcare_chat


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

QA_FILE = os.path.join(
    BASE_DIR,
    "qa_test_set.csv"
)

REPORT_FILE = os.path.join(
    BASE_DIR,
    "evaluation_report.csv"
)


# ============================================================
# EVALUATION
# ============================================================

def run_evaluation():

    with open(
        QA_FILE,
        newline="",
        encoding="utf-8"
    ) as f:

        rows = list(
            csv.DictReader(f)
        )


    results = []

    type_correct = 0

    disease_correct = 0

    ood_correct = 0

    ood_total = 0


    # ========================================================
    # TEST EACH QUESTION
    # ========================================================

    for row in rows:

        question = row[
            "question"
        ]

        expected_type = row[
            "expected_type"
        ].strip().lower()

        expected_disease = row[
            "expected_disease"
        ].strip().lower()


        # Every test starts with a fresh topic
        result = healthcare_chat(
            question,
            current_topic=None
        )


        actual_type = str(
            result.get(
                "question_type",
                ""
            )
        ).strip().lower()


        actual_disease = str(
            result.get(
                "current_topic",
                ""
            ) or ""
        ).strip().lower()


        actual_source = result.get(
            "source",
            ""
        )


        # ----------------------------------------------------
        # Compare question type
        # ----------------------------------------------------

        type_match = (
            actual_type
            == expected_type
        )


        # ----------------------------------------------------
        # Compare disease
        # ----------------------------------------------------

        disease_match = (
            actual_disease
            == expected_disease
        )


        # ----------------------------------------------------
        # Store result
        # ----------------------------------------------------

        answer = str(
            result.get(
                "answer",
                ""
            )
        )


        answer_preview = (
            answer[:70] + "..."
            if len(answer) > 70
            else answer
        )


        results.append(
            {
                "question":
                    question,

                "expected_type":
                    row["expected_type"],

                "actual_type":
                    result.get(
                        "question_type"
                    ),

                "type_match":
                    type_match,

                "expected_disease":
                    row["expected_disease"]
                    or "(none)",

                "actual_disease":
                    actual_disease
                    or "(none)",

                "disease_match":
                    disease_match,

                "actual_source":
                    actual_source,

                "answer_preview":
                    answer_preview
            }
        )


        # ----------------------------------------------------
        # Counters
        # ----------------------------------------------------

        if type_match:
            type_correct += 1

        if disease_match:
            disease_correct += 1


        # ----------------------------------------------------
        # Out-of-domain
        # ----------------------------------------------------

        if expected_disease == "":

            ood_total += 1

            if (
                actual_source
                == "No reliable source"
            ):

                ood_correct += 1


    # ========================================================
    # SUMMARY
    # ========================================================

    total = len(rows)


    print()
    print("=" * 70)
    print(
        "HEALTHCARE QA CHATBOT — EVALUATION SUMMARY"
    )
    print("=" * 70)


    if total > 0:

        print(
            f"Total questions tested        : "
            f"{total}"
        )

        print(
            f"Question-type accuracy        : "
            f"{type_correct}/{total} "
            f"({100 * type_correct / total:.1f}%)"
        )

        print(
            f"Disease-detection accuracy    : "
            f"{disease_correct}/{total} "
            f"({100 * disease_correct / total:.1f}%)"
        )


    if ood_total:

        print(
            f"Out-of-domain rejection rate  : "
            f"{ood_correct}/{ood_total} "
            f"({100 * ood_correct / ood_total:.1f}%)"
        )


    print("=" * 70)


    # ========================================================
    # MISMATCHES
    # ========================================================

    print()
    print(
        "Rows with a mismatch:"
    )

    print()


    any_mismatch = False


    for result in results:

        if (
            not result["type_match"]
            or not result["disease_match"]
        ):

            any_mismatch = True

            print(
                f'- "{result["question"]}"'
            )

            print(
                f'    expected type='
                f'{result["expected_type"]}, '
                f'got={result["actual_type"]}'
            )

            print(
                f'    expected disease='
                f'{result["expected_disease"]}, '
                f'got={result["actual_disease"]}'
            )

            print()


    if not any_mismatch:

        print(
            "None — all rows matched "
            "expected type and disease."
        )


    # ========================================================
    # SAVE CSV REPORT
    # ========================================================

    if results:

        with open(
            REPORT_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.DictWriter(
                f,
                fieldnames=list(
                    results[0].keys()
                )
            )

            writer.writeheader()

            writer.writerows(
                results
            )


    print()
    print(
        "Full row-by-row report saved to:"
    )

    print(
        "evaluation_report.csv"
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    run_evaluation()