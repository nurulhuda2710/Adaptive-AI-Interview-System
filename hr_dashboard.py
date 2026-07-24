import base64
import streamlit as st
import sqlite3
import pandas as pd

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="AI Recruitment Dashboard",
    page_icon="💼",
    layout="wide"
)

DATABASE = "interview.db"

# ======================================================
# DATABASE CONNECTION
# ======================================================

def get_connection():
    return sqlite3.connect(DATABASE)

# ======================================================
# LOGIN SESSION
# ======================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ======================================================
# LOAD BACKGROUND IMAGE
# ======================================================

def get_base64(file_path):
    with open(file_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

bg_image = get_base64("assets/4872300.jpg")

# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown(f"""
<style>

/* ---------- Background ---------- */

.stApp {{
    background:
        linear-gradient(
            rgba(0,0,0,0.45),
            rgba(0,0,0,0.45)
        ),
        url("data:image/jpg;base64,{bg_image}");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* Hide Streamlit Header */

header {{
    visibility:hidden;
}}

[data-testid="stToolbar"] {{
    display:none;
}}

.block-container {{
    padding-top:5rem;
}}

/* ---------- Login Card ---------- */

div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stTextInput"]) {{
    background:white;
    padding:35px;
    border-radius:20px;
    box-shadow:0px 10px 30px rgba(0,0,0,.35);
    max-width:580px;      /* ubah ikut saiz yang awak nak */
    margin:0 auto;
}}

/* ---------- Textbox ---------- */

.stTextInput input {{
    border-radius:10px;
}}

/* ---------- Button ---------- */

.stButton > button {{

    width:100%;
    height:50px;

    background:#6C63FF;
    color:white;

    border:none;
    border-radius:10px;

    font-size:18px;
    font-weight:bold;

}}

.stButton > button:hover {{

    background:#564FD8;
    color:white;

}}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN PAGE
# ======================================================

if not st.session_state.logged_in:

    left, center, right = st.columns([1.2,2,1.2])

    with center:

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center;">
            <span style="font-size:38px;">💼</span>
            <span style="
                font-size:42px;
                font-weight:700;
                color:#2d3142;
                vertical-align:middle;
            ">
                HR Login
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            "<p style='text-align:center;color:gray;'>"
            "Please login to access the AI Recruitment Dashboard."
            "</p>",
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        username = st.text_input(
            "Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "Login",
            use_container_width=True
        ):

            if username == "hr" and password == "admin123":

                st.session_state.logged_in = True
                st.rerun()

            else:

                st.error("Invalid username or password.")

    st.stop()

# ======================================================
# DASHBOARD CSS
# ======================================================

st.markdown("""
<style>

.stApp{
    background:#F5F7FB !important;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD DATABASE
# ======================================================

conn = get_connection()

candidate_df = pd.read_sql_query("""
SELECT *
FROM candidate
ORDER BY candidate_id DESC
""", conn)


# ======================================================
# PAGE TITLE
# ======================================================

st.title("💼 AI Recruitment Dashboard")


# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title("👥 Candidates")

if candidate_df.empty:

    st.warning("No interview records found.")
    st.stop()

candidate_names = candidate_df["name"].tolist()

selected_name = st.sidebar.selectbox(
    "Select Candidate",
    candidate_names
)

candidate = candidate_df[
    candidate_df["name"] == selected_name
].iloc[0]

candidate_id = candidate["candidate_id"]


# ======================================================
# SIDEBAR - QUICK INFO
# ======================================================

st.sidebar.divider()

st.sidebar.markdown("## 👤 Quick Info")

st.sidebar.write(f"**University:** {candidate['university']}")
st.sidebar.write(f"**Course:** {candidate['course']}")
st.sidebar.write(f"**Target Position:** {candidate['target_position']}")


# ======================================================
# CANDIDATE INFORMATION
# ======================================================

st.header("👤 Candidate Information")

col1, col2 = st.columns(2)

with col1:

    st.write("**Name**")
    st.write(candidate["name"])

    st.write("**University**")
    st.write(candidate["university"])

    st.write("**Study Level**")
    st.write(candidate["study_level"])

with col2:

    st.write("**Course**")
    st.write(candidate["course"])

    st.write("**Employment Status**")
    st.write(candidate["employment_status"])

    st.write("**Target Position**")
    st.write(candidate["target_position"])

st.divider()


# ======================================================
# INTERVIEW TRANSCRIPT
# ======================================================

st.header("💬 Interview Transcript")

transcript = pd.read_sql_query(
    f"""
    SELECT
        question_number,
        question,
        answer
    FROM interview
    WHERE candidate_id={candidate_id}
    ORDER BY question_number
    """,
    conn
)

# Sidebar Information
st.sidebar.write(f"**Questions Answered:** {len(transcript)}/5")

for _, row in transcript.iterrows():

    with st.expander(f"Question {row['question_number']}"):

        st.markdown("**Question**")
        st.info(row["question"])

        st.markdown("**Candidate Answer**")
        st.write(row["answer"])

st.divider()

# ======================================================
# AI EVALUATION
# ======================================================

evaluation = pd.read_sql_query(
    f"""
    SELECT *
    FROM evaluation
    WHERE candidate_id={candidate_id}
    """,
    conn
)

if evaluation.empty:

    st.warning("No AI evaluation available.")

else:

    evaluation = evaluation.iloc[0]

    # ======================================================
    # SIDEBAR - INTERVIEW SUMMARY
    # ======================================================

    st.sidebar.divider()

    st.sidebar.markdown("## 📊 Interview Summary")

    st.sidebar.metric(
        "Overall Score",
        f"{evaluation['overall_score']}/10"
    )

    recommendation = evaluation["final_recommendation"]

    if recommendation == "Suitable for Hiring":

        st.sidebar.success("🟢 Suitable for Hiring")

    elif recommendation == "Needs Further Interview":

        st.sidebar.warning("🟡 Needs Further Interview")

    else:

        st.sidebar.error("🔴 Not Suitable")

    # ======================================================
    # LOGOUT BUTTON
    # ======================================================

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.rerun()

    # ======================================================
    # AI EVALUATION
    # ======================================================

    st.header("📊 AI Evaluation")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Communication",
        f"{evaluation['communication']}/10"
    )

    c2.metric(
        "Technical",
        f"{evaluation['technical']}/10"
    )

    c3.metric(
        "Problem Solving",
        f"{evaluation['problem_solving']}/10"
    )

    c4.metric(
        "Confidence",
        f"{evaluation['confidence']}/10"
    )

    c5.metric(
        "Overall",
        f"{evaluation['overall_score']}/10"
    )

    st.divider()

    # ======================================================
    # STRENGTHS / WEAKNESSES
    # ======================================================

    left, right = st.columns(2)

    with left:

        st.subheader("✅ Strengths")

        strengths = evaluation["strengths"]

        if strengths:
            for item in strengths.split("\n"):
                if item.strip():
                    st.write(f"• {item}")

        st.subheader("⚠️ Weaknesses")

        weaknesses = evaluation["weaknesses"]

        if weaknesses:
            for item in weaknesses.split("\n"):
                if item.strip():
                    st.write(f"• {item}")

    with right:

        st.subheader("📈 Improvement Recommendations")

        recommendations = evaluation["improvement_recommendations"]

        if recommendations:
            for item in recommendations.split("\n"):
                if item.strip():
                    st.write(f"• {item}")

        st.subheader("📝 HR Summary")

        st.info(evaluation["summary"])

    st.divider()

    # ======================================================
    # FINAL RECOMMENDATION
    # ======================================================

    recommendation = evaluation["final_recommendation"]

    if recommendation == "Suitable for Hiring":

        st.success(
            f"🟢 Final Recommendation: {recommendation}"
        )

    elif recommendation == "Needs Further Interview":

        st.warning(
            f"🟡 Final Recommendation: {recommendation}"
        )

    else:

        st.error(
            f"🔴 Final Recommendation: {recommendation}"
        )

# ======================================================
# CLOSE DATABASE
# ======================================================

conn.close()