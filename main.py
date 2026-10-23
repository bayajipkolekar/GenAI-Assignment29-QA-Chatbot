
import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

load_dotenv()


def get_answer(question, model_type="openai", chat_history=None):
    """Get an answer from the selected model using conversation history."""

    if chat_history is None:
        chat_history = []

    if model_type.lower() == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            return "Error: Please configure OPENAI_API_KEY in your .env file."

        model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

    elif model_type.lower() == "ollama":
        model = ChatOllama(
            model="llama3",
            temperature=0
        )

    else:
        return "Error: Choose either 'openai' or 'ollama'."

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a helpful Q&A assistant. "
            "Answer clearly and accurately. "
            "Use conversation history to understand follow-up questions."
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])

    try:
        chain = prompt | model

        response = chain.invoke({
            "question": question,
            "chat_history": chat_history
        })

        return response.content

    except Exception as error:
        return f"Error: {error}"


def main():
    print("=" * 55)
    print("ASSIGNMENT 29: Q&A CHATBOT")
    print("OpenAI + Ollama + Conversation History")
    print("=" * 55)

    print("\nChoose a model:")
    print("1. OpenAI (Cloud Model)")
    print("2. Ollama (Local Model)")
    print("Type 'exit' to quit.")

    choice = input("\nEnter your choice (1 or 2): ").strip()

    if choice == "1":
        model_type = "openai"
    elif choice == "2":
        model_type = "ollama"
    else:
        print("Invalid choice. Please select 1 or 2.")
        return

    print(f"\nSelected model: {model_type}")
    print("Ask your questions below.")
    print("Type 'exit' to stop the chatbot.\n")

    chat_history = []
    question_count = 0

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("\nChatbot: Goodbye, bro!")
            break

        if not question:
            print("Please enter a question.\n")
            continue

        answer = get_answer(
            question=question,
            model_type=model_type,
            chat_history=chat_history
        )

        print(f"\nChatbot: {answer}\n")

        if not answer.startswith("Error:"):
            chat_history.append(HumanMessage(content=question))
            chat_history.append(AIMessage(content=answer))
            question_count += 1

    print(f"\nTotal questions answered: {question_count}")


if __name__ == "__main__":
    main()
