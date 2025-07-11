# tools.py

import requests
from livekit.agents import function_tool, RunContext
import logging
import os
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import Optional

load_dotenv()
logging.basicConfig(level=logging.INFO)

@function_tool()
async def get_weather(context: RunContext, city: str) -> str:
    try:
        r = requests.get(f"https://wttr.in/{city}?format=3")
        return r.text.strip() if r.status_code == 200 else f"Failed to fetch weather for {city}."
    except Exception as e:
        return f"Error: {e}"

@function_tool()
async def search_web(context: RunContext, query: str) -> str:
    """
    Smart web search.  
    • Defaults to DuckDuckGo.  
    • If the user explicitly says “use Google …” or “search Google for …”
      it switches to Google Custom Search.  
    • If DuckDuckGo returns nothing or errors, it auto‑falls back to Google.
    """
    logging.info(f"[search_web] original query = '{query}'")

    # Detect an explicit Google request
    lowered = query.lower()
    explicit_google = any(
        phrase in lowered
        for phrase in (
            "use google", "search google", "google search", "on google"
        )
    )

    # Strip helper phrases but keep real keywords
    clean = (
        lowered
        .replace("use google to search for", "")
        .replace("search google for", "")
        .replace("search on google for", "")
        .replace("google", "")           # just the literal word
        .strip()
    ) or query   # fallback to original if we stripped everything

    if explicit_google:
        logging.info("[search_web] user requested Google")
        result = await google_custom_search(context, clean)
        return f"{result}\n\n(via Google)"

    # ---------- DuckDuckGo first ----------
    try:
        ddg_result = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info("[search_web] used DuckDuckGo")

        if ddg_result and ddg_result.strip():
            return f"{ddg_result}\n\n(via DuckDuckGo)"
        else:
            logging.warning("[search_web] DDG empty → fallback Google")
            google_result = await google_custom_search(context, query)
            return f"{google_result}\n\n(via Google fallback)"

    except Exception as e:
        logging.error(f"[search_web] DuckDuckGo error ({e}) → fallback Google")
        google_result = await google_custom_search(context, query)
        return f"{google_result}\n\n(via Google fallback)"


@function_tool()
async def google_custom_search(context: RunContext, query: str) -> str:
    """
    Google Custom Search (needs GOOGLE_SEARCH_API_KEY & GOOGLE_CSE_ID).
    Returns top‑3 results or a helpful error string.
    """
    google_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    google_cse_id  = os.getenv("GOOGLE_CSE_ID")

    if not google_api_key or not google_cse_id:
        logging.error("[google_custom_search] Missing GOOGLE_API_KEY or GOOGLE_CSE_ID")
        return "Google API credentials not configured."

    url = "https://www.googleapis.com/customsearch/v1"
    params = { "key": google_api_key, "cx": google_cse_id, "q": query }

    try:
        logging.info(f"[google_custom_search] query='{query}'")
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        items = data.get("items", [])
        if not items:
            logging.warning("[google_custom_search] zero results")
            return "No results found. (via Google)"

        top = []
        for itm in items[:3]:
            title   = itm.get("title", "")
            link    = itm.get("link", "")
            snippet = itm.get("snippet", "")
            top.append(f"{title}\n{link}\n{snippet}")

        return "\n\n".join(top) + "\n\n(via Google)"

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        if status in (400, 403):
            return "Google API key invalid or quota exhausted."
        if status == 429:
            return "Google API rate‑limit hit; try later."
        logging.error(f"[google_custom_search] HTTP {status}: {e}")
        return f"Google search failed (HTTP {status})."

    except Exception as e:
        logging.error(f"[google_custom_search] unexpected error: {e}")
        return f"Google search failed: {e}"
  
@function_tool()    
async def send_email(
    
    context: RunContext,  # type: ignore
    to_email: str,
    subject: str,
    message: str,
    cc_email: Optional[str] = None
    
) -> str:
    print("=== send_email tool triggered ===")
    logging.info("send_email tool triggered")

    logging.info("send_email tool triggered")##
    logging.info(f"Parameters received: to_email={to_email}, subject={subject}, cc_email={cc_email}")##
    """
    Send an email through Gmail.
    
    Args:
        to_email: Recipient email address
        subject: Email subject line
        message: Email body content
        cc_email: Optional CC email address
    """
    
    # Gmail SMTP configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # SSL port for Gmail SMTP
        
    # Get credentials from environment variables
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")  # Use App Password, not regular password
        
    if not gmail_user or not gmail_password:
        logging.error("Gmail credentials not found in environment variables")
        return "Email sending failed: Gmail credentials not configured."
        
    # Create message
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = subject
        
    # Add CC if provided
    recipients = [to_email]
    if cc_email:
        msg['Cc'] = cc_email
        recipients.append(cc_email)
    
    # Attach message body
    msg.attach(MIMEText(message, 'plain'))
        
        # Connect to Gmail SMTP server
    server = None
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        # server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, recipients, msg.as_string())
        logging.info(f"Email sent successfully to {to_email}")
        return f"Email sent successfully to {to_email}"
    except smtplib.SMTPAuthenticationError:
        logging.error("Gmail authentication failed")
        return "Email sending failed: Authentication error. Please check your Gmail credentials."
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
        return f"Email sending failed: SMTP error - {str(e)}"
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return f"An error occurred while sending email: {str(e)}"
    finally:
        if server:
            server.quit()

if __name__ == "__main__":
    logging.info("Logging test — tools.py is working.")

