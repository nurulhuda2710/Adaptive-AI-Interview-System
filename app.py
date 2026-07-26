import streamlit as st

from interview import (
    generate_first_question,
    generate_followup_question,
)

from evaluation import evaluate_interview

from database import (
    create_database,
    save_candidate,
    save_interview,
    save_evaluation
)

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="AI Interview Chatbot",
    page_icon="🤖",
    layout="wide"
)

create_database()

TOTAL_QUESTIONS = 5

# -------------------------------------------------
# Global CSS
# -------------------------------------------------

st.markdown("""
<style>

.block-container{
    padding-top:7rem;
    padding-bottom:7rem;
    max-width:1460px;
}

/* ===========================
   LABELS
=========================== */

div[data-testid="stWidgetLabel"] p{
    font-size:22px !important;
    font-weight:700 !important;
    color:#1f2937 !important;
    line-height:1.4 !important;
}

/* Add a little spacing below labels */
div[data-testid="stWidgetLabel"]{
    margin-bottom:6px !important;
}

div[data-testid="stWidgetLabel"] label p{
    font-size:22px !important;
    font-weight:700 !important;
}

/* ===========================
   TEXTBOX
=========================== */

.stTextInput input{

    font-size:20px !important;
    height:60px;

}

/* ===========================
   DROPDOWN
=========================== */

.stSelectbox div[data-baseweb="select"] > div{

    min-height:60px !important;
    font-size:18px !important;
    font-weight:450 !important;

}

/* Text dalam dropdown */
.stSelectbox div[data-baseweb="select"] span{

    font-size:18px !important;
}

/* Input search dropdown */
.stSelectbox input{

    font-size:18px !important;
}

/* ===========================
   BUTTON
=========================== */

.stButton > button{

    width:180px !important;
    height:60px !important;

    background-color:#1f77b4 !important;
    color:white !important;

    border:none !important;
    border-radius:12px !important;

    font-size:20px !important;
    font-weight:600 !important;

    transition:all 0.3s ease !important;

    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
}

/* Button Text */

.stButton > button p{

    font-size:18px !important;
    font-weight:580 !important;
    color:white !important;

    margin:0 !important;
    padding:0 !important;
}

/* Button Hover */

.stButton > button:hover{

    background-color:#1565a8 !important;
    color:white !important;

    transform:translateY(-2px);
}

/* Button Focus */

.stButton > button:focus{

    box-shadow:none !important;
    outline:none !important;
}
/* ===========================
   PROGRESS BAR
=========================== */

<style>
.stProgress > div > div > div > div{
    background:#7C3AED !important;  

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# Session State
# -------------------------------------------------

if "started" not in st.session_state:
    st.session_state.started = False

if "finished" not in st.session_state:
    st.session_state.finished = False

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "current_question_text" not in st.session_state:
    st.session_state.current_question_text = ""

if "candidate_id" not in st.session_state:
    st.session_state.candidate_id = None

if "candidate_info" not in st.session_state:
    st.session_state.candidate_info = {}

if "interview_history" not in st.session_state:
    st.session_state.interview_history = []

if "answers" not in st.session_state:
    st.session_state.answers = []

# ==========================================
# TEMP: Skip to Interview Page (Testing Only)
# ==========================================

#st.session_state.started = True
#st.session_state.finished = False
#st.session_state.current_question = 1

#st.session_state.candidate_info = {
    #"name": "Nurul Huda",
    #"course": "MSc Applied Computing",
    #"status": "Student",
    #"position": "Business Analyst"
#}

#st.session_state.current_question_text = (
    #"Tell me about yourself and why you are interested in this position."
#)

#st.session_state.interview_history = []

# -------------------------------------------------
# Header
# -------------------------------------------------

#st.title("Adaptive AI Interview System")

col1, col2 = st.columns([0.08, 0.92], vertical_alignment="center")

with col1:
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("images/Graident Ai Robot_resize.png", width=200)

with col2:
    st.markdown("""
    <h1 style="
        margin-bottom:0px;
        font-size:42px;
        font-weight:700;
        color:#1f2937;
        line-height:1;">
        Adaptive AI Interview System
    </h1>

    <p style="
        margin-top:10px;
        margin-bottom:0px;
        font-size:18px;
        color:#6b7280;
        line-height:1.2;">
        Conducting adaptive AI interviews and evaluating candidate responses in real time.
    </p>
     """, unsafe_allow_html=True)

st.divider()

# -------------------------------------------------
# Candidate Information
# -------------------------------------------------

if not st.session_state.started:

    st.subheader("👤 Candidate Information")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        #Name
        st.markdown("""
        <p style="
            font-size:18px;
            font-weight:580;
            margin-bottom:8px;
            color:#1f2937;">
            Full Name <span style="color:red;">*</span>
        </p>
        """, unsafe_allow_html=True)

        candidate_name = st.text_input(
            "",
            label_visibility="collapsed",
            key = "candidate_name"
        )

        #university
        st.markdown("""
        <p style="
            font-size:18px;
            font-weight:580;
            margin-bottom:8px;
            color:#1f2937;">
            🏫 University <span style="color:red;">*</span>
        </p>
        """, unsafe_allow_html=True)

        university = st.selectbox(
            " ",
            [
                "Universiti Teknologi PETRONAS (UTP)",
                "Universiti Teknologi MARA (UiTM)",
                "Universiti Sains Malaysia (USM)",
                "Universiti Utara Malaysia (UUM)",
                "Universiti Teknikal Malaysia Melaka (UTeM)",
                "Universiti Malaysia Perlis (UniMAP)",
                "Other (Please specify)"
            ],
            index=None,
            placeholder="Please select your University",
            label_visibility="collapsed",
            key= "university"
        )

        if university == "Other (Please specify)":
            university = st.text_input("Specify your University Name")

        #study level
        st.markdown("""
                <p style="
                    font-size:18px;
                    font-weight:580;
                    margin-bottom:8px;
                    color:#1f2937;">
                    🎓 Current Study Level <span style="color:red;">*</span>
                </p>
                """, unsafe_allow_html=True)

        study_level = st.selectbox(
            " ",
            [
                "Diploma",
                "Bachelor's Degree",
                "Master's Degree",
                "PhD and above",
                "Other (Please specify)"
            ],
            index=None,
            placeholder="Please select your Current Study Level",
            label_visibility = "collapsed",
            key="study_level"
        )

        if study_level == "Other (Please specify)":
            study_level = st.text_input("Specify your Current Study Level")

    with col2:

        #Course
        st.markdown("""
        <p style="
            font-size:18px;
            font-weight:580;
            margin-bottom:8px;
            color:#1f2937;">
            📚 Course / Programme <span style="color:red;">*</span>
        </p>
        """, unsafe_allow_html=True)

        course = st.text_input(
            "",
            label_visibility="collapsed",
            key="course"
        )

        # Employment status
        st.markdown("""
         <p style="
            font-size:18px;
            font-weight:580;
            margin-bottom:8px;
            color:#1f2937;">
            💼 Current Employment Status <span style="color:red;">*</span>
        </p>
        """, unsafe_allow_html=True)


        status = st.selectbox(
            " ",
            [
                "Student",
                "Fresh Graduate",
                "Employed",
                "Unemployed",
                "Other (Please specify)"
            ],
            index=None,
            placeholder="Please select your Employment Status",
            label_visibility="collapsed",
            key="status"

        )

        if status == "Other (Please specify)":
            status = st.text_input("Specify your current Employment Status")

        #Target Position
        st.markdown("""
         <p style="
                font-size:18px;
                font-weight:580;
                margin-bottom:8px;
                color:#1f2937;">
               👔 Target Position <span style="color:red;">*</span>
         </p>
            """, unsafe_allow_html=True)

        position = st.selectbox(
            " ",
            [
                "Business Analyst",
                "Quality Analyst",
                "Software Engineer",
                "Data Analyst",
                "AI Engineer",
                "Other (Please specify)"
            ],
            index=None,
            placeholder="Please select your Target Position",
            label_visibility = "collapsed",
            key= "position"
        )

        if position == "Other (Please specify)":
            position = st.text_input("Specify your Target Position")


    # -------------------------------------------------
    # Start Interview Button
    # -------------------------------------------------

    st.markdown("<br> ", unsafe_allow_html=True)

    if st.button("🚀 Start Interview"):

        if (
            not candidate_name
            or not university
            or not study_level
            or not status
            or not position
        ):

            st.error("Please complete all required fields.")

        else:

            st.session_state.candidate_info = {
                "name": candidate_name,
                "university": university,
                "study_level": study_level,
                "course": course,
                "status": status,
                "position": position
            }

            candidate_id = save_candidate(
                candidate_name,
                university,
                study_level,
                course,
                status,
                position
            )

            st.session_state.candidate_id = candidate_id
            st.session_state.started = True
            st.session_state.finished = False
            st.session_state.current_question = 1
            st.session_state.answers = []
            st.session_state.interview_history = []

            with st.spinner("Preparing interview..."):
                st.session_state.current_question_text = generate_first_question(
                    st.session_state.candidate_info
                )

            st.rerun()


# -------------------------------------------------
# Interview Screen
# -------------------------------------------------

elif st.session_state.started and not st.session_state.finished:

    # Interview Page CSS
    st.markdown("""
        <style>

        .block-container{
            padding-top:0.9rem !important;
        }

        </style>
        """, unsafe_allow_html=True)

    # Progress
    progress = st.session_state.current_question / TOTAL_QUESTIONS

# -------------------------------------------------
# Sidebar
# -------------------------------------------------id

    with st.sidebar:

        col1, col2 = st.columns([1, 3], vertical_alignment="center")

        with col1:
            st.image("images/chatbot.png", width=60)

        with col2:
            st.markdown("""
            <h2 style="
                margin:0;
                padding-top:10px;
                font-size:28px;
                font-weight:700;
                color:#312E81;">
                Chat with AI
            </h2>
            """, unsafe_allow_html=True)

        st.divider()

        candidate = st.session_state.candidate_info

        st.subheader("👤 Candidate Information")

        st.write(f"**Name:** {candidate.get('name')}")
        st.write(f"**Course / Programme:**")
        st.write(candidate.get("course"))
        st.write(f"**Employment Status:**")
        st.write(candidate.get("status"))
        st.write(f"**Target Position:**")
        st.write(candidate.get("position"))

        st.divider()

        st.subheader("📋 Interview Summary")
        st.write(f"**Total Questions:** {TOTAL_QUESTIONS}")
        st.write(f"**Current Question:** {st.session_state.current_question}")

        st.divider()
        st.subheader("Interview Progress")
        st.progress(progress)
        st.write(
            f"Question {st.session_state.current_question} of {TOTAL_QUESTIONS}"
        )


# -------------------------------------------------
# Chat History
# -------------------------------------------------

    for i, item in enumerate(st.session_state.interview_history, start=1):
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(
                f"**Q {i}/{TOTAL_QUESTIONS}:** {item['question']}"
            )

        with st.container():
            col1, col2 = st.columns([2, 8])

            with col2:
                with st.chat_message("user", avatar="👤"):
                    st.markdown(item["answer"])

# -------------------------------------------------
# Current Question
# -------------------------------------------------

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(
            f"**Q {st.session_state.current_question}/{TOTAL_QUESTIONS}:** "
            f"{st.session_state.current_question_text}"
        )

# -------------------------------------------------
# User Input
# -------------------------------------------------

    answer = st.chat_input("Type your answer here...")

    if answer:

        st.session_state.answers.append(answer)

        st.session_state.interview_history.append(
            {
                "question": st.session_state.current_question_text,
                "answer": answer
            }
        )
        save_interview(
            st.session_state.candidate_id,
            st.session_state.current_question,
            st.session_state.current_question_text,
            answer
        )

        if st.session_state.current_question >= TOTAL_QUESTIONS:

            st.session_state.finished = True

        else:

            st.session_state.current_question += 1

            with st.spinner("🤖 Preparing next question..."):

                st.session_state.current_question_text = (
                    generate_followup_question(
                        st.session_state.candidate_info,
                        st.session_state.interview_history,
                        st.session_state.current_question
                    )
                )

        st.rerun()

# -------------------------------------------------
# Evaluation Report
# -------------------------------------------------

elif st.session_state.finished:

    # Generate evaluation
    evaluation = evaluate_interview(
        st.session_state.candidate_info,
        st.session_state.interview_history
    )

    # Save evaluation into database
    save_evaluation(
        st.session_state.candidate_id,
        evaluation["communication"],
        evaluation["technical"],
        evaluation["problem_solving"],
        evaluation["confidence"],
        evaluation["overall_score"],
        "\n".join(evaluation["strengths"]),
        "\n".join(evaluation["weaknesses"]),
        "\n".join(evaluation["improvement_recommendations"]),
        evaluation["summary"],
        evaluation["final_recommendation"]
    )

    st.success("Interview Completed Successfully")

    st.markdown(
    """

    ## Thank You!

    Thank you for participating in this AI Interview.

    Your responses have been successfully submitted.

    The interview assessment has been recorded successfully.

    We appreciate your time and wish you all the best in your future career.

    😊 Have a great day!

    """)