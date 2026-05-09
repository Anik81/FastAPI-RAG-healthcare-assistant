def prompt(query, docs):
    context = "\n---\n".join(d["text"] for d in docs)
    return f"Question: {query}\n\nContext:\n{context}"


def generate_answer(query, docs):
    if not docs:
        return f"No documents found for: {query}"
    sources = ", ".join(d["source"] for d in docs)
    snippets = " ".join(d["text"][:150] for d in docs[:2])
    return (
        f"Based on {len(docs)} retrieved document(s) ({sources}), "
        f"the most relevant information is: {snippets}"
    )