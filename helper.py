from livekit.plugins.google import beta
import logging

# Use the same model as Friday
llm = beta.realtime.RealtimeModel(
    voice="Aoede",
    temperature=0.8,
)

async def generate_message_from_prompt(prompt: str) -> str:
    """Generates an email body from a prompt like 'Write a professional message about project delay'."""
    logging.info(f"Generating email message from prompt: {prompt}")
    try:
        result = await llm.generate(prompt + "\n\nWrite this as a professional email body.")
        message = result.text.strip()
        logging.info("Generated message: " + message)
        return message
    except Exception as e:
        logging.error(f"Error generating message: {e}")
        return "Sorry, I couldn’t generate the message."
