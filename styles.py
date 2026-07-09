import streamlit as st

def load_css():
    st.markdown("""
<style>

/* ---------------- GOOGLE FONT ---------------- */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ---------------- HIDE STREAMLIT ---------------- */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
[data-testid="stSidebarNav"]{
    display:none;
}
/* ---------------- APP ---------------- */

.stApp{
    background:#241A14;
    color:#F5F1EB;
}

/* Main content */

.block-container{
    max-width:1350px;
    padding-top:2rem;
    padding-bottom:2rem;
}

/* ---------------- SIDEBAR ---------------- */

section[data-testid="stSidebar"]{

    background:#31241C;

    border-right:1px solid #4A372A;

}

section[data-testid="stSidebar"] *{

    color:#F5F1EB;

}

section[data-testid="stSidebar"] h3{

    font-size:22px;

    margin-bottom:5px;

}

section[data-testid="stSidebar"] p{

    font-size:15px;

    color:#D9CCBF;

}

/* ---------------- TITLES ---------------- */

h1{

    font-size:58px !important;

    text-align:center;

    font-weight:800 !important;

    color:#FFF8EF;

    letter-spacing:-2px;

}

h2{

    color:#FFF8EF;

}

h3{

    color:#FFF8EF;

}

/* ---------------- PARAGRAPH ---------------- */

p{

    color:#ffffff;

    font-size:17px;

}

/* ---------------- BUTTONS ---------------- */

.stButton > button{

    width:100%;

    height:58px;

    background:#708B75;

    color:#1F1B16;

    border:none;

    border-radius:16px;

    font-size:18px;

    font-weight:700;

    transition:0.3s;

}

.stButton > button:hover{

    background:#C6A15B;

    color:black;

    transform:translateY(-2px);

}

/* ---------------- METRICS ---------------- */

div[data-testid="stMetric"]{

    background:#35271F;

    border:1px solid #4A372A;

    border-radius:18px;

    padding:18px;

}

div[data-testid="stMetricLabel"]{

    color:#D2C6B7;

}

div[data-testid="stMetricValue"]{

    color:white;

    font-size:30px;

    font-weight:700;

}

/* ---------------- INPUTS ---------------- */

.stTextInput input{

    background:#35271F;

    color:white;

    border-radius:14px;

    border:1px solid #4A372A;

}

.stNumberInput input{

    background:#35271F;

    color:white;

    border-radius:14px;

}

.stSelectbox div{

    border-radius:14px;

}

/* ---------------- SLIDER ---------------- */

.stSlider{

    padding-top:10px;

}

/* ---------------- DATAFRAME ---------------- */

[data-testid="stDataFrame"]{

    border-radius:16px;

    overflow:hidden;

}

/* ---------------- PLOTLY ---------------- */

div[data-testid="stPlotlyChart"]{

    background:#35271F;

    border-radius:20px;

    padding:10px;

    border:1px solid #4A372A;

}

/* ---------------- DIVIDER ---------------- */

hr{

    border-color:#4A372A;

}

/* ---------------- INFO BOX ---------------- */

div[data-testid="stAlert"]{

    background:#35271F;

    border:1px solid #4A372A;

    color:white;

    border-radius:16px;

}

/* ---------------- FILE UPLOADER ---------------- */

[data-testid="stFileUploader"]{

    background:#35271F;

    border-radius:18px;

    padding:10px;

}

/* ---------------- RADIO ---------------- */

div[role="radiogroup"]{

    gap:12px;

}

</style>
""", unsafe_allow_html=True)