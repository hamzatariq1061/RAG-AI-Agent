
from backend.rag_chain import ask_question

print("RAG AI Agent Started!")
print("Type 'exit' to quit.\n")

while True:
    question = input("Ask a question: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    result = ask_question(question)

    print("\nAI Answer:")
    print(result["answer"])

    print("\nRetrieved Sources:")
    for source in result["sources"]:
        print(
            f"- {source['source']} "
            f"(Page: {source['page']})"
        )

    print("-" * 50)
