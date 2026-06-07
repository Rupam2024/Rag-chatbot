from langchain_ollama import OllamaLLM
import time

# ----------------------------------
# Configuration
# ----------------------------------

MODEL_NAME = "llama3"

# ----------------------------------
# Load Model
# ----------------------------------

class OllamaClient:

    def __init__(self):

        self.llm = OllamaLLM(
            model=MODEL_NAME,
            temperature=0.2
        )

    # ----------------------------------
    # Basic Generation
    # ----------------------------------

    def generate(
        self,
        prompt
    ):

        try:

            response = self.llm.invoke(
                prompt
            )

            return response

        except Exception as e:

            return (
                f"Error generating response: {str(e)}"
            )

    # ----------------------------------
    # Generation with Timing
    # ----------------------------------

    def generate_with_metrics(
        self,
        prompt
    ):

        start_time = time.time()

        try:

            response = self.llm.invoke(
                prompt
            )

            end_time = time.time()

            return {
                "response": response,
                "response_time": round(
                    end_time - start_time,
                    2
                )
            }

        except Exception as e:

            return {
                "response": str(e),
                "response_time": 0
            }

    # ----------------------------------
    # Fallback LLM Answer
    # ----------------------------------

    def fallback_answer(
        self,
        question
    ):

        prompt = f"""
You are a pharmaceutical assistant.

The answer was not found in the local drug database.

Provide a general answer using your knowledge.

Mention clearly:

'This information was not found in the local database.'

Question:
{question}

Answer:
"""

        return self.generate(
            prompt
        )

    # ----------------------------------
    # RAG-Based Answer
    # ----------------------------------

    def rag_answer(
        self,
        question,
        context
    ):

        prompt = f"""
You are an expert pharmaceutical AI assistant.

Answer ONLY using the information provided below.

If information is missing,
state:

'This information was not found in the local database.'

DATABASE CONTEXT:

{context}

QUESTION:

{question}

ANSWER:
"""

        return self.generate(
            prompt
        )

    # ----------------------------------
    # Hybrid RAG Answer
    # ----------------------------------

    def hybrid_answer(
        self,
        question,
        context
    ):

        prompt = f"""
You are an expert pharmaceutical AI assistant.

Use the database information first.

If the answer cannot be found
in the database,
use your general medical knowledge.

When using general knowledge,
clearly state:

'This information was not found in the local database.'

DATABASE:

{context}

QUESTION:

{question}

FINAL ANSWER:
"""

        return self.generate(
            prompt
        )

    # ----------------------------------
    # Drug Comparison
    # ----------------------------------

    def compare_drugs(
        self,
        drug1_context,
        drug2_context
    ):

        prompt = f"""
Compare the following two drugs.

DRUG 1:
{drug1_context}

DRUG 2:
{drug2_context}

Provide comparison in:

1. Product Name
2. Company
3. Strength
4. Composition
5. MRP
6. Summary
"""

        return self.generate(
            prompt
        )

    # ----------------------------------
    # Drug Report Summary
    # ----------------------------------

    def generate_report_summary(
        self,
        context
    ):

        prompt = f"""
Create a concise pharmaceutical report.

DATA:

{context}

Generate:

1. Product Overview
2. Manufacturer
3. Composition
4. Strength
5. Pricing Information
6. Key Insights
"""

        return self.generate(
            prompt
        )


# ----------------------------------
# Singleton Instance
# ----------------------------------

client = OllamaClient()

# ----------------------------------
# Helper Functions
# ----------------------------------

def generate_response(
    prompt
):

    return client.generate(
        prompt
    )


def rag_response(
    question,
    context
):

    return client.rag_answer(
        question,
        context
    )


def hybrid_response(
    question,
    context
):

    return client.hybrid_answer(
        question,
        context
    )


def fallback_response(
    question
):

    return client.fallback_answer(
        question
    )


def compare_drug_response(
    drug1_context,
    drug2_context
):

    return client.compare_drugs(
        drug1_context,
        drug2_context
    )


def report_summary(
    context
):

    return client.generate_report_summary(
        context
    )


# ----------------------------------
# Test
# ----------------------------------

if __name__ == "__main__":

    test_prompt = """
What is Paracetamol?
"""

    result = generate_response(
        test_prompt
    )

    print(result)
