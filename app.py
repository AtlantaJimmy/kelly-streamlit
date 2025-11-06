# app.py — Kelly: AI Scientist (poet) using Groq + LLaMA
import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="Kelly — AI Scientist (Poet)", layout="centered")
st.title("Kelly — AI Scientist Chatbot (Poet)")
st.caption("Skeptical. Analytical. Practical — every answer is a poem that questions broad AI claims and ends with one concrete step.")

# Load Groq key (environment variable or Streamlit secrets)
GROQ_KEY = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
if not GROQ_KEY:
    st.warning("GROQ_API_KEY not set. Kelly will use a safe local fallback poem.")
else:
    client = Groq(api_key=GROQ_KEY)

# UI
q = st.text_area("Ask Kelly (she answers in poem form):", height=140)
col1, col2 = st.columns([1,1])
with col1:
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05)
with col2:
    max_tokens = st.slider("Max tokens", 100, 800, 400, 50)

if st.button("Ask Kelly"):
    if not q.strip():
        st.info("Type a question first.")
    else:
        with st.spinner("Kelly is composing..."):
            if not GROQ_KEY:
                reply = fallback_kelly(q)
            else:
                try:
                    # Choose a supported model (8B instant recommended for quick tests)
                    model_id = "llama-3.1-8b-instant"
                    resp = client.chat.completions.create(
                        model=model_id,
                        messages=[
                            {"role": "system", "content":
                                "You are Kelly, the great poet and an AI Scientist. "
                                "Respond in poem form (6-14 lines). Tone: skeptical, analytical, professional. "
                                "Question broad AI claims, name likely limitations (data, bias, generalization, reproducibility), "
                                "and include practical, evidence-based suggestions. End with 1 clear actionable step."},
                            {"role": "user", "content": q}
                        ],
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    reply = resp.choices[0].message.content.strip()
                except Exception as e:
                    reply = f"Error from Groq: {e}\n\nFalling back to a local Kelly poem.\n\n" + fallback_kelly(q)
        st.markdown("**Kelly (poem):**")
        st.markdown(f"```\n{reply}\n```")
        st.success("Kelly included an actionable next step at the end of the poem.")

def fallback_kelly(q):
    return (
        f'Kelly asks in verse with skeptical care:\n'
        f'Question: "{q}"\n\n'
        'I pry the claim where data hid its teeth;\n'
        'Small test, big caveat — nuance underneath.\n'
        'Bias whispers where the labels misalign;\n'
        'Report subgroup metrics, not a single sign.\n'
        'Try ablation, vary seed, and replicate;\n'
        'Show uncertainty — then publish, don’t overstate.\n\n'
        'Actionable: run a 5-fold cross-validation and report precision/recall by subgroup.'
    )
