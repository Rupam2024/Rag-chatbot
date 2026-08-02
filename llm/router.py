import re

from utils.exact_search import (
    get_exact_answer,
    extract_possible_sku
)

from vectorstore.retriever import (
    retrieve,
    has_relevant_context
)

from llm.ollama_client import (
    rag_response,
    hybrid_response,
    fallback_response
)

# Query Categories

DRUG_LOOKUP_KEYWORDS = [
    "composition",
    "manufacturer",
    "company",
    "strength",
    "price",
    "mrp",
    "cost",
    "drug",
    "tablet",
    "capsule",
    "syrup",
    "injection"
]

MEDICAL_KEYWORDS = [
    "uses",
    "side effects",
    "benefits",
    "interaction",
    "contraindication",
    "disease",
    "treatment",
    "fever",
    "pain",
    "infection"
]

ANALYTICS_KEYWORDS = [
    "top",
    "count",
    "average",
    "highest",
    "lowest",
    "statistics",
    "analytics"
]

def is_sku_query(query):

    patterns = [
        r"\d+\s*mg",
        r"tablet",
        r"syrup",
        r"capsule",
        r"injection"
    ]

    for pattern in patterns:

        if re.search(
            pattern,
            query.lower()
        ):
            return True

    return False

# Drug Lookup Route

def route_drug_lookup(query):

    result = retrieve(
        query=query,
        top_k=5
    )

    context = result["context"]

    sources = result["sources"]

    answer = rag_response(
        question=query,
        context=context
    )

    return {
        "route": "RAG",
        "answer": answer,
        "sources": sources
    }

# Medical Route

def route_medical_query(query):

    if has_relevant_context(query):

        result = retrieve(
            query=query,
            top_k=5
        )

        answer = hybrid_response(
            question=query,
            context=result["context"]
        )

        return {
            "route": "HYBRID",
            "answer": answer,
            "sources": result["sources"]
        }

    answer = fallback_response(
        query
    )

    return {
        "route": "LLM",
        "answer": answer,
        "sources": []
    }


# Analytics Route

def route_analytics(query):

    result = retrieve(
        query=query,
        top_k=10
    )

    answer = hybrid_response(
        question=query,
        context=result["context"]
    )

    return {
        "route": "ANALYTICS",
        "answer": answer,
        "sources": result["sources"]
    }

# General Route

def route_general(query):

    if has_relevant_context(query):

        result = retrieve(
            query=query,
            top_k=5
        )

        answer = hybrid_response(
            question=query,
            context=result["context"]
        )

        return {
            "route": "HYBRID",
            "answer": answer,
            "sources": result["sources"]
        }

    answer = fallback_response(
        query
    )

    return {
        "route": "LLM",
        "answer": answer,
        "sources": []
    }


# Main Router

def process_query(query):


    # EXACT PRODUCT SEARCH

    sku_query = extract_possible_sku(
        query
    )
    exact_result = get_exact_answer(
    sku_query
    )

    if exact_result:

        return exact_result

    # EXISTING ROUTER LOGIC

    query_type = classify_query(
        query
    )

    if is_sku_query(query):

        return route_drug_lookup(
            query
        )

    elif query_type == "medical":

        return route_medical_query(
            query
        )

    elif query_type == "analytics":

        return route_analytics(
            query
        )

    else:

        return route_general(
            query
        )

# Pretty Print Sources

def format_sources(sources):

    if not sources:
        return "No sources available."

    text = ""

    for idx, source in enumerate(
        sources,
        start=1
    ):

        text += f"""
Source {idx}

SKU: {source.get('sku')}

Company: {source.get('company')}

Category: {source.get('category')}

Strength: {source.get('strength')}


"""

    return text

# Test

if __name__ == "__main__":

    test_queries = [

        "What is the composition of 37 C 500 MG TABLET?",

        "Who manufactures Sildenafil products?",

        "What are the uses of Paracetamol?",

        "Show top drug categories"

    ]

    for query in test_queries:

        print("\n" + "=" * 60)

        print("QUESTION:")
        print(query)

        result = process_query(
            query
        )

        print("\nROUTE:")
        print(result["route"])

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")
        print(
            format_sources(
                result["sources"]
            )
        )
