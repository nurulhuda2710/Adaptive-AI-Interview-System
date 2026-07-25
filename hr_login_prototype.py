import streamlit as st

st.set_page_config(
    page_title="AI Recruitment Dashboard",
    page_icon="💼",
    layout="wide"
)

# ======================================================
# CSS
# ======================================================

st.markdown("""
<style>

header{
    visibility:hidden;
}

[data-testid="stToolbar"]{
    display:none;
}

.stApp{
    background:#F5F7FB;
}

.block-container{
    padding-top:2rem;
    padding-left:3rem;
    padding-right:3rem;
}

/* Login Card */

.login-card{

    background:white;

    padding:45px;

    border-radius:20px;

    box-shadow:0 10px 30px rgba(0,0,0,.15);

}

/* Text */

.title{

    font-size:40px;

    font-weight:700;

    color:#2d3142;

}

.subtitle{

    color:#666;

    font-size:18px;

    margin-bottom:25px;

}

/* Button */

.stButton>button{

    width:100%;

    height:50px;

    background:#5E35B1;

    color:white;

    border:none;

    border-radius:10px;

    font-size:18px;

    font-weight:600;

}

.stButton>button:hover{

    background:#4527A0;

    color:white;

}

</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================

st.markdown("""
<h1 style="
text-align:center;
font-size:46px;
font-weight:600;
color:#2d3142;
margin-bottom:8px;
">
AI Recruitment System
</h1>

<p style="
text-align:center;
font-size:20px;
color:#777;
margin-bottom:30px;
">
AI-powered recruitment platform for candidate interview assessment.
</p>
""", unsafe_allow_html=True)

st.divider()

# ======================================================
# LOGIN LAYOUT
# ======================================================

left, right = st.columns([1.3,0.8])

# ---------------- LEFT ---------------- #

with left:

    st.image(
        "assets/4872300.jpg",
        use_container_width=True
    )

# ---------------- RIGHT ---------------- #

with right:

    st.markdown(
        "<div style='margin-top:86px;'></div>",
        unsafe_allow_html=True
    )

    st.markdown("""

    <h2 style="
    color:#2d3142;
    margin-bottom:8px;
    font-size:42px;
    font-weight:700;
    ">
    💼 HR Login
    </h2>

    <div class="subtitle">
    Welcome back! Please sign in to access the HR Dashboard.
    </div>

    """, unsafe_allow_html=True)

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

            st.success("Login Successful")

        else:

            st.error("Invalid username or password.")

    st.markdown("</div>", unsafe_allow_html=True)