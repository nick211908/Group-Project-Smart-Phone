from dotenv import load_dotenv
import logging, atexit, inspect

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import noise_cancellation, google

from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from newtool import (
    get_weather, search_web, send_email,
    google_custom_search,
)
from tool_app_launcher import open_youtube, open_gmail, open_whatsapp
from helper import generate_message_from_prompt

load_dotenv()
logging.basicConfig(level=logging.INFO)
atexit.register(lambda: logging.info("Exiting the assistant process."))

# ───────────────────── EMAIL DRAFT STATE ─────────────────────
email_draft = {
    "to_email": None,
    "subject": None,
    "message": None,
    "cc_email": None,
    "active": False,
}

# ───────────────────── Assistant Class ───────────────────────
class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            llm=google.beta.realtime.RealtimeModel(
                voice="Aoede",
                temperature=0.8,
            ),
            tools=[
                get_weather, search_web, google_custom_search,
                send_email, open_youtube, open_gmail, open_whatsapp,
               
            ],
        )
        logging.info("Assistant initialized with tools.")

    # ------------ Chat hook ------------
    async def on_text_message(self, message: str, ctx: AgentSession) -> None:
        msg = message.strip().lower()
        responded=False# ─── App Launchers ─────────────────────
        if "youtube" in msg:
            if "search" in msg:
                query = msg.split("search", 1)[1].strip()
                result = await open_youtube(context=None, query=query)
            else:
                result = await open_youtube(context=None)
            await ctx.send_message(result)
            responded = True

        if "gmail" in msg:
           result = await open_gmail(context=None)
           await ctx.send_message(result)
           responded = True

        if "whatsapp" in msg:
            result = await open_whatsapp(context=None)
            await ctx.send_message(result)
            responded = True

        # Now handle custom logic for email only
        if any(p in msg for p in ["send an email", "write an email", "compose email"]):
            email_draft.update({"active": True})
            await ctx.send_message("Sure, Sir. Who should I send it to?")
            return

        if email_draft["active"]:
            if any(p in msg for p in ["cancel", "abort", "discard"]):
               email_draft.update({k: None for k in email_draft})
               email_draft["active"] = False
               await ctx.send_message("Email draft cancelled, Sir.")
               return

            if "send it" in msg or "send the email" in msg:
                if all([email_draft["to_email"], email_draft["subject"], email_draft["message"]]):
                     result = await send_email(
                         context=None,
                         to_email=email_draft["to_email"],
                         subject=email_draft["subject"],
                         message=email_draft["message"],
                         cc_email=email_draft["cc_email"],
                     )
                     await ctx.send_message(f"Check! {result}")
                     email_draft["active"] = False
                else:
                    await ctx.send_message("Missing recipient, subject, or message, Sir.")
                return

            if "@" in msg and " " not in msg:
                email_draft["to_email"] = msg
                await ctx.send_message("Recipient noted. Subject?")
                return

            if msg.startswith("subject "):
                email_draft["subject"] = msg.replace("subject", "").strip()
                await ctx.send_message("Subject recorded. Message body?")
                return

            if msg.startswith("message "):
                email_draft["message"] = msg.replace("message", "").strip()
                await ctx.send_message("Message saved. Say 'send it' when ready.")
                return

            if any(p in msg for p in ["write a message", "draft a message", "generate message"]):
                email_draft["message"] = await generate_message_from_prompt(message)
                await ctx.send_message("Drafted. Say 'send it' or modify anything.")
                return

            await ctx.send_message("Awaiting email details or 'send it', Sir.")
            return
    
        # ─── Fallback to agent LLM chain ───────────────────────────
        if not responded:
            await super().on_text_message(message, ctx)



# ───────────────────── LiveKit entrypoint (for cloud worker) ──
async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            video_enabled=True,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION,
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
