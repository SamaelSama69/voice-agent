from fastapi import APIRouter
from pydantic import BaseModel

from agent import agent

router = APIRouter()

# Conversation memory
conversation_store = {}

# Keep only recent messages
MAX_MESSAGES = 10

class ChatRequest(BaseModel):
    message: str
    session_id: str


@router.post("/chat")
def chat(data: ChatRequest):

    print("\n" + "=" * 60)
    print("SESSION:", data.session_id)
    print("USER MESSAGE:", data.message)
    print("=" * 60)

    # Create new session
    if data.session_id not in conversation_store:

        conversation_store[data.session_id] = []

        print(f"NEW SESSION CREATED: {data.session_id}")

    messages = conversation_store[data.session_id]

    # Add user message
    messages.append(
        {
            "role": "user",
            "content": data.message
        }
    )

    # Keep only recent messages
    messages = messages[-MAX_MESSAGES:]

    print("\nRECENT CONVERSATION:")

    for m in messages:
        print(m)

    try:

        response = agent.invoke(
            {
                "messages": messages
            }
        )

        print("\nAGENT RESPONSE:")
        print(response)

        assistant_message = ""

        if isinstance(response, dict):

            msgs = response.get("messages", [])

            # Find last AI message
            for msg in reversed(msgs):

                if hasattr(msg, "content"):

                    content = msg.content

                    if content and str(content).strip():
                        assistant_message = content
                        break

            if assistant_message == "":
                assistant_message = (
                    "I couldn't understand the request."
                )

        else:
            assistant_message = str(response)

    except Exception as e:

        print("AGENT ERROR:", str(e))

        assistant_message = (
            "I couldn't complete that request right now."
        )

    # Save assistant response
    messages.append(
        {
            "role": "assistant",
            "content": assistant_message
        }
    )

    # Again trim conversation
    conversation_store[data.session_id] = (
        messages[-MAX_MESSAGES:]
    )

    # Optional cleanup after successful booking
    if (
        "appointment has been successfully booked"
        in assistant_message.lower()
    ):
        conversation_store[data.session_id] = []

        print("SESSION CLEARED AFTER BOOKING")

    print("\nASSISTANT:")
    print(assistant_message)

    print("=" * 60 + "\n")

    return {
        "response": assistant_message
    }