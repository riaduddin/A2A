import uuid

import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    Message,
    MessageSendParams,
    Part,
    Role,
    SendMessageRequest,
    TextPart,
)

PUBLIC_AGENT_CARD_PATH = "/.well-known/agent.json"
BASE_URL = "http://localhost:9999"


async def main() -> None:
    async with httpx.AsyncClient() as httpx_client:
        print("Initializing A2AClient with public agent card")
        # Initialize A2ACardResolver
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=BASE_URL,
        )
        print("A2ACardResolver initialized")
        final_agent_card_to_use: AgentCard | None = None
        print("Fetching public agent card: ", final_agent_card_to_use)

        try:
            print(
                f"Fetching public agent card from: {BASE_URL}{PUBLIC_AGENT_CARD_PATH}"
            )
            _public_card = await resolver.get_agent_card()
            print("Fetched public agent card")
            print(_public_card.model_dump_json(indent=2))

            final_agent_card_to_use = _public_card
            print("Final agent card to use:",final_agent_card_to_use)

        except Exception as e:
            print(f"Error fetching public agent card: {e}")
            raise RuntimeError("Failed to fetch public agent card")

        client = A2AClient(
            httpx_client=httpx_client, agent_card=final_agent_card_to_use
        )
        print("A2AClient initialized")

        message_payload = Message(
            role=Role.user,
            messageId=str(uuid.uuid4()),
            parts=[Part(root=TextPart(text="Hello, how are you?"))],
        )
        print("Message payload created:")
        print(message_payload.model_dump_json(indent=2))
        request = SendMessageRequest(
            id=str(uuid.uuid4()),
            params=MessageSendParams(
                message=message_payload,
            ),
        )
        print("Sending message")

        response = await client.send_message(request)
        print("Response:",response)
        print("with proper formatting:")
        print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
