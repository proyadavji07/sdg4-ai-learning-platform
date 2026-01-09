import streamlit as st # type: ignore
from database import create_tables
from ai_engine import explain_concept
from quiz_engine import generate_quiz
from gap_analyzer import analyze_learning_gap
from translator import translate_text

LANGUAGE_MAP = {
    "English": "en-US",
    "Hindi": "hi-IN",
    "Marathi": "mr-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Gujarati": "gu-IN",
    "Punjabi": "pa-IN",
    "Bengali": "bn-IN",
    "Urdu": "ur-IN",
    "French": "fr-FR",
    "German": "de-DE",
    "Spanish": "es-ES",
    "Italian": "it-IT",
    "Portuguese": "pt-PT",
    "Russian": "ru-RU",
    "Chinese": "zh-CN",
    "Japanese": "ja-JP",
    "Korean": "ko-KR",
    "Arabic": "ar-SA"
}

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "user_name" not in st.session_state:
    st.session_state.user_name = None

st.set_page_config(page_title="SDG-4 AI Learning Platform", layout="wide")

st.sidebar.title("Navigation")

if "menu" not in st.session_state:
    st.session_state.menu = "AI Learning Assistant"

if st.sidebar.button("🤖 AI Learning Assistant"):
    st.session_state.menu = "AI Learning Assistant"

if st.sidebar.button("🧪 Learning Gap Quiz"):
    st.session_state.menu = "Learning Gap Quiz"

if st.sidebar.button("🌐 Translation"):
    st.session_state.menu = "Translation"

if st.sidebar.button("🕘 Session History"):
    st.session_state.menu = "Session History"

menu = st.session_state.menu

if "explanation" not in st.session_state:
    st.session_state.explanation = ""

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

if "quiz_result" not in st.session_state:
    st.session_state.quiz_result = None

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

create_tables()

if menu == "AI Learning Assistant":
    st.title("🤖 AI Personalized Learning Assistant")

    # Show chat history
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Type your message...")

    if user_input:
        user_text = user_input.strip()

        # Save user message
        st.session_state.chat_messages.append(
            {"role": "user", "content": user_text}
        )

        with st.chat_message("user"):
            st.markdown(user_text)

        ai_reply = ""

        # ---- GREETING DETECTION ----
        greetings = ["hi", "hello", "hey", "hii", "hiii"]

        lowered = user_text.lower()

        # Detect name introduction
        if "i am" in lowered or "i'm" in lowered or "my name is" in lowered:
            import re
            match = re.search(r"(i am|i'm|my name is)\s+([a-zA-Z]+)", lowered)
            if match:
                name = match.group(2).capitalize()
                st.session_state.user_name = name
                ai_reply = f"Nice to meet you, {name}! 😊 How can I help you in your learning today?"

        # Simple greeting without topic
        elif lowered in greetings:
            if st.session_state.user_name:
                ai_reply = f"Hi {st.session_state.user_name}! 👋 What would you like to learn today?"
            else:
                ai_reply = "Hi there! 👋 What would you like to learn today?"

        # ---- NORMAL LEARNING QUESTION ----
        else:
            with st.spinner("Thinking..."):
                context_name = (
                    f"The learner's name is {st.session_state.user_name}. "
                    if st.session_state.user_name else ""
                )

                ai_reply = explain_concept(
                    f"{context_name}{user_text}",
                    level="Beginner"
                )

        # Show AI response
        with st.chat_message("assistant"):
            st.markdown(ai_reply)

        # Save AI response
        st.session_state.chat_messages.append(
            {"role": "assistant", "content": ai_reply}
        )


if menu == "Learning Gap Quiz":
    st.title("Learning Gap Based Quiz")

    topic = st.text_input("Enter topic for quiz")
    difficulty = st.selectbox("Select quiz difficulty", ["Easy", "Medium", "Hard"])

    if st.button("Generate Quiz"):
        if topic:
            st.session_state.quiz_data = generate_quiz(topic, difficulty)
            st.session_state.quiz_result = None

    if st.session_state.quiz_data:
        user_answers = {}

        for idx, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"**Q{idx+1}. {q['question']}**")
            user_answers[idx] = st.radio(
                "Choose an option",
                q["options"],
                key=f"quiz_{idx}"
            )

        if st.button("Submit Quiz"):
            score = 0
            results = []

            for idx, q in enumerate(st.session_state.quiz_data):
                correct = q["answer"]
                user = user_answers[idx]
                is_correct = user == correct
                if is_correct:
                    score += 1

                results.append({
                    "question": q["question"],
                    "user": user,
                    "correct": correct,
                    "explanation": q["explanation"],
                    "status": is_correct
                })

            accuracy, status = analyze_learning_gap(score, len(st.session_state.quiz_data))

            st.session_state.quiz_result = {
                "score": score,
                "accuracy": accuracy,
                "status": status,
                "details": results
            }

    if st.session_state.quiz_result:
        st.subheader("📊 Quiz Review")

        for i, r in enumerate(st.session_state.quiz_result["details"]):
            if r["status"]:
                st.success(f"Q{i+1}: Correct ✅")
            else:
                st.error(f"Q{i+1}: Incorrect ❌")

            st.write(f"Your Answer: {r['user']}")
            st.write(f"Correct Answer: {r['correct']}")
            st.write(f"Explanation: {r['explanation']}")
            st.divider()

        st.success(f"Final Score: {st.session_state.quiz_result['score']}")
        st.info(f"Accuracy: {st.session_state.quiz_result['accuracy']:.2f}%")
        st.warning(f"Learning Status: {st.session_state.quiz_result['status']}")




if menu == "Translation":
    st.title("Multilingual Translation")

    # Auto-fill explanation text if available
    text_to_translate = st.text_area(
        "Enter text to translate",
        value=st.session_state.explanation or "",
        height=200
    )

    # Language suggestions (dropdown with search)
    target_language = st.selectbox(
        "Translate to language",
        list(LANGUAGE_MAP.keys())
    )

    if st.button("Translate"):
        if text_to_translate:
            with st.spinner("Translating..."):
                st.session_state.translated_text = translate_text(
                    text_to_translate,
                    target_language
                )

    # Show translated output
    if st.session_state.translated_text:
        st.subheader("Translated Output")
        st.write(st.session_state.translated_text)

        if "speak_now" not in st.session_state:
            st.session_state.speak_now = False

        # Speak button
        # Speak button
        if st.button("Speak"):
            st.session_state.speak_now = True

        # Run Text-to-Speech when triggered
        if st.session_state.speak_now:
            speech_lang_code = LANGUAGE_MAP.get(target_language, "en-US")
            speak_text = st.session_state.translated_text.replace("\n", " ").replace('"', '')

            st.components.v1.html(
                f"""
                <html>
                <body>
                <script>
                    const utterance = new SpeechSynthesisUtterance("{speak_text}");
                    utterance.lang = "{speech_lang_code}";
                    window.speechSynthesis.cancel();
                    window.speechSynthesis.speak(utterance);
                </script>
                </body>
                </html>
                """,
                height=0
            )

            # Reset trigger so it doesn't auto-play again
            st.session_state.speak_now = False




if menu == "Session History":
    st.title("🕘 Session History")

    # ---- Chat History ----
    if st.session_state.chat_messages:
        st.subheader("💬 Chat History (AI Learning Assistant)")

        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**AI:** {msg['content']}")
            st.divider()
    else:
        st.info("No chat history yet.")

    # ---- Last Quiz Result ----
    if st.session_state.quiz_result:
        st.subheader("🧪 Last Quiz Result")
        st.write(st.session_state.quiz_result)

    # ---- Last Translation ----
    if st.session_state.translated_text:
        st.subheader("🌐 Last Translation")
        st.write(st.session_state.translated_text)