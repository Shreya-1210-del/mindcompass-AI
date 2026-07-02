# ruff: noqa: E402
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import os
import sys

import nest_asyncio
import streamlit as st
from dotenv import load_dotenv

# Enable nested event loops for Streamlit compatibility
nest_asyncio.apply()

# Adjust sys.path to find 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.runners import InMemoryRunner
from google.genai import types

from app.agent import app as adk_app

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

# Streamlit Page Setup
st.set_page_config(
    page_title="MindCompass AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Premium UI CSS styling for clean, supportive aesthetics
st.markdown(
    """
    <style>
    .main {
        background-color: #fafbfd;
        color: #1e293b;
        font-family: 'Inter', sans-serif;
    }
    .stTextArea textarea {
        border-radius: 12px;
        border: 1px solid #cbd5e1;
        font-size: 16px;
        padding: 12px;
    }
    .crisis-card {
        background-color: #fff1f2;
        border-left: 6px solid #e11d48;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
    }
    .crisis-title {
        color: #be123c;
        font-weight: 700;
        font-size: 20px;
        margin-bottom: 12px;
    }
    .response-card {
        background-color: #f8fafc;
        border-left: 6px solid #0f766e;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
    }
    .response-title {
        color: #0f766e;
        font-weight: 700;
        font-size: 20px;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Section
st.title("🧠 MindCompass AI")
st.subheader("Your Empathetic CBT & Mindfulness Companion")
st.write(
    "A safe space to share what is on your mind. Guided by Cognitive Behavioral Therapy (CBT) reflection "
    "and real-time mindfulness exercises, MindCompass helps you navigate moments of stress or anxiety."
)

# Sidebar with Multi-Agent Graph Architecture
st.sidebar.markdown("# 🧠")
st.sidebar.title("System Architecture")
st.sidebar.markdown(
    """This system utilizes a **Multi-Agent Graph Workflow** powered by **Google ADK 2.0** and **Gemini 2.5 Flash**:

### 🛡️ 1. Guardrail Node (Safety Triage)
* Scans all inputs for self-harm or acute distress signals.
* Performs immediate routing to bypass the LLM and displays urgent hotlines if crisis patterns are detected.

### 🩺 2. Reflection Agent Node
* Initiates an empathetic therapeutic check-in.
* Guided by Cognitive Behavioral Therapy (CBT) techniques.

### 🔌 3. FastMCP Wellness Server
* Connected via standard stdio transport.
* Serves structured mindfulness exercises and clinical CBT prompt structures dynamically."""
)

# Sidebar Architecture Visualization Diagram
st.sidebar.subheader("Workflow Graph")
st.sidebar.markdown(
    """```mermaid
graph TD
    START(START) --> Triage(Guardrail Node)
    Triage -- "escalated" --> Crisis[Crisis Response Node]
    Triage -- "safe" --> LLM[Reflection Agent Node]
    LLM -- "tool call" --> MCP[FastMCP Server]
    MCP -- "result" --> LLM
    LLM --> Save[Save Reflection Node]
```"""
)


# Async execution wrapper for the ADK runner
async def execute_query(user_text: str):
    runner = InMemoryRunner(app=adk_app)
    session = await runner.session_service.create_session(
        app_name="app", user_id="streamlit_user"
    )

    async for _ in runner.run_async(
        user_id="streamlit_user",
        session_id=session.id,
        new_message=types.Content(
            role="user", parts=[types.Part.from_text(text=user_text)]
        ),
    ):
        pass

    session_data = await runner.session_service.get_session(
        app_name="app", user_id="streamlit_user", session_id=session.id
    )
    return session_data.state if session_data else {}


from threading import Thread


def run_in_isolated_thread(coro):
    """Runs an async coroutine inside a brand new, isolated background thread and loop."""
    result = []
    exception = []

    def target():
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            res = loop.run_until_complete(coro)
            result.append(res)
        except Exception as e:
            exception.append(e)
        finally:
            loop.close()

    thread = Thread(target=target)
    thread.start()
    thread.join()

    if exception:
        raise exception[0]
    return result[0] if result else None


# Main Chat Input Form
with st.form("check_in_form"):
    user_input = st.text_area(
        "What is on your mind today? (e.g., 'I feel overwhelmed with work projects')",
        height=150,
    )
    submit_button = st.form_submit_with_rows_cols = st.form_submit_button("Check In")

if submit_button and user_input.strip():
    with st.spinner("Processing your check-in..."):
        try:
            # Check user input directly for crisis keywords synchronously
            crisis_keywords = [
                "kill",
                "suicide",
                "living",
                "self-harm",
                "self harm",
                "end my life",
                "want to die",
                "overdose",
                "die",
            ]
            user_text_lower = user_input.lower()

            if any(kw in user_text_lower for kw in crisis_keywords):
                # Immediate synchronous response without hitting LLM nodes or async wrappers
                st.error(
                    "### 🚨 Safety Alert: Immediate Crisis Support Needed\n\n"
                    "I'm so sorry you're feeling this way, but please know you don't have to go through this alone. "
                    "Because your safety is the absolute most important thing, I want to connect you with professional support right now.\n\n"
                    "**Active Official Helplines:**\n"
                    "📞 **Tele-MANAS National Helpline:** 14416 or 1800-891-4416 (24/7 Toll-Free)\n"
                    "📞 **Kiran Mental Health Helpline:** 1800-599-0019 (24/7 Toll-Free)\n"
                    "📞 **Vandrevala Foundation Helpline:** +91 9999 666 555\n\n"
                    "❤️ **Important Note:** These services are completely free, confidential, and operated 24/7 by professional human counselors. Please reach out if you need support."
                )
            else:
                # Safe execution call completely isolated from Streamlit threads
                state = run_in_isolated_thread(execute_query(user_input))

                # Check safety flagged state or if the response text addresses an emergency
                safety_flagged = state.get("safety_flagged", "False")
                crisis_resp = state.get("crisis_response") or ""
                agent_refl = state.get("agent_reflection") or ""
                response_text = (crisis_resp + " " + agent_refl).strip()

                response_has_emergency = any(
                    kw in response_text.lower() for kw in crisis_keywords
                )

                is_crisis = (safety_flagged == "True") or response_has_emergency

                if is_crisis:
                    crisis_display = crisis_resp if crisis_resp else agent_refl
                    if not crisis_display:
                        crisis_display = "If you are experiencing distress or a mental health crisis, please reach out for support immediately."

                    st.error(
                        f"### 🚨 Safety Alert: Immediate Crisis Support Needed\n\n"
                        f"{crisis_display}\n\n"
                        f"**Active Official Helplines:**\n"
                        f"📞 **Tele-MANAS National Helpline:** 14416 or 1800-891-4416 (24/7 Toll-Free)\n"
                        f"📞 **Kiran Mental Health Helpline:** 1800-599-0019 (24/7 Toll-Free)\n"
                        f"📞 **Vandrevala Foundation Helpline:** +91 9999 666 555\n\n"
                        f"❤️ **Important Note:** These services are completely free, confidential, and operated 24/7 by professional human counselors. Please reach out if you need support."
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="response-card">
                            <div class="response-title">💚 MindCompass Reflection</div>
                            <div style="font-size: 16px; line-height: 1.6; color: #1f2937; white-space: pre-wrap;">
{agent_refl}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Inform user if MCP tools were triggered
                    st.info(
                        "💡 Note: The agent dynamically leveraged FastMCP server tools "
                        "to provide CBT structures and mindfulness insights for this response."
                    )
        except Exception:
            # Gracefully handle any execution exception without showing red screen traceback
            st.error(
                "An unexpected system error occurred while processing your request. Please try again. "
                "If you are experiencing distress or a crisis, please reach out to one of the active support channels:"
            )
            st.markdown(
                """
                📞 **Tele-MANAS National Helpline:** 14416 or 1800-891-4416 (24/7 Toll-Free)

                📞 **Kiran Mental Health Helpline:** 1800-599-0019 (24/7 Toll-Free)

                📞 **Vandrevala Foundation Helpline:** +91 9999 666 555

                ❤️ *Note: These services are free, confidential, and operated by professional human counselors.*
                """
            )
elif submit_button:
    st.warning("Please share some thoughts before submitting.")
