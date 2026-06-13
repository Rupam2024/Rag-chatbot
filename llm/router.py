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
