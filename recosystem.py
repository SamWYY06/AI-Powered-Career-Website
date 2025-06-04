import streamlit as st # type: ignore
import pandas as pd # type: ignore
import numpy as np # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
from sklearn.metrics.pairwise import cosine_similarity # type: ignore
from sentence_transformers import SentenceTransformer # type: ignore
import spacy # type: ignore
import re
import os
import warnings

# Setup
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
warnings.filterwarnings("ignore", category=FutureWarning)

# Load models
nlp = spacy.load("en_core_web_sm")
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

# Clean function
def clean_and_postprocess(text):
    if isinstance(text, str):
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.lower().strip()
    return ""

# Load and prepare data
df = pd.read_csv("career_list.csv")
df.fillna("", inplace=True)

# Backup
df["Job Title Original"] = df["Job Title"]
df["Role Original"] = df["Role"]
df["Skills Original"] = df["Skills"]
df["Responsibilities Original"] = df["Responsibilities"]
df["Description Original"] = df["Description"]

# Clean
text_columns = ["Job Title", "Role", "Description", "Skills", "Responsibilities"]
for col in text_columns:
    df[col] = df[col].apply(clean_and_postprocess)

# Combined text
df["combined_text"] = (
    df["Job Title"] * 3 + " " +
    df["Skills"] * 3 + " " +
    df["Description"] * 2 + " " +
    df["Responsibilities"] + " " +
    df["Role"]
)

# TF-IDF and SBERT
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3), min_df=1, max_df=0.9)
tfidf_matrix = vectorizer.fit_transform(df["combined_text"])
sbert_embeddings = sbert_model.encode(df["combined_text"].tolist(), convert_to_tensor=True)

# Recommendation
def recommend_careers(user_input, df, vectorizer, tfidf_matrix, sbert_embeddings, top_n=3):
    user_input_clean = clean_and_postprocess(user_input)
    user_vector_tfidf = vectorizer.transform([user_input_clean])
    tfidf_scores = cosine_similarity(user_vector_tfidf, tfidf_matrix)[0]
    user_vector_sbert = sbert_model.encode([user_input_clean], convert_to_tensor=True)
    sbert_scores = cosine_similarity(user_vector_sbert, sbert_embeddings)[0]
    combined_scores = (tfidf_scores + sbert_scores) / 2
    sorted_indices = np.argsort(combined_scores)[::-1]

    unique_careers, seen_titles = [], set()
    for idx in sorted_indices:
        title = df.iloc[idx]["Job Title Original"]
        if title not in seen_titles:
            seen_titles.add(title)
            unique_careers.append({
                "Job Title": title,
                "Role": df.iloc[idx]["Role Original"],
                "Salary Range (Average)": df.iloc[idx]["Salary Range"],
                "Skills": df.iloc[idx]["Skills Original"],
                "Responsibilities": df.iloc[idx]["Responsibilities Original"],
                "Job Description": df.iloc[idx]["Description Original"],
                "TF-IDF Score": round(tfidf_scores[idx], 3),
                "SBERT Score": round(sbert_scores[idx], 3),
                "Combined Score": round(combined_scores[idx], 3)
            })
        if len(unique_careers) == top_n:
            break
    return pd.DataFrame(unique_careers)

# -------------------------------
#   Page Config and Styling
# -------------------------------
st.set_page_config(
    page_title="CareerFinder - AI Career Recommendations", 
    page_icon="👜", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Reset and base styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body {
        font-family: 'Poppins', sans-serif;
        background: #0f0f0f;
        color: #ffffff;
        overflow-x: hidden;
    }
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header, .stDeployButton {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* Main app container */
    .stApp {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 50%, #16213e 100%);
        min-height: 100vh;
        margin: 0;
        padding: 0;
    }
    
    /* Remove default padding */
    .block-container {
        padding: 0 !important;
        max-width: none !important;
        background: transparent;
    }
    
    /* Animated background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(79, 70, 229, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(124, 58, 237, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(236, 72, 153, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 60% 70%, rgba(14, 165, 233, 0.1) 0%, transparent 50%);
        z-index: -1;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        33% { transform: translate(-30px, -30px) rotate(1deg); }
        66% { transform: translate(30px, -20px) rotate(-1deg); }
    }
    
    /* Navigation bar */
    .navbar {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%);
        padding: 20px 40px;
        box-shadow: 
            0 8px 32px rgba(79, 70, 229, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.1);
        position: sticky;
        top: 0;
        z-index: 1000;
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .logo {
        font-size: 2.5rem;
        font-weight: 800;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .logo:hover {
        transform: scale(1.05) translateY(-2px);
        filter: drop-shadow(0 8px 16px rgba(79, 70, 229, 0.4));
    }
    
    /* Main content container */
    .content-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 60px 40px;
        position: relative;
        z-index: 1;
    }
    
    /* Hero section */
    .hero-section {
        text-align: center;
        margin-bottom: 80px;
        padding: 60px 0;
        background: rgba(45, 45, 45, 0.3);
        border-radius: 30px;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 16px 64px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(79, 70, 229, 0.1), transparent);
        animation: rotate 20s linear infinite;
        z-index: -1;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4f46e5, #7c3aed, #ec4899, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 20px;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: #b0b0b0;
        margin-bottom: 40px;
        font-weight: 500;
        line-height: 1.6;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Question cards */
    .question-card {
        background: rgba(45, 45, 45, 0.8);
        border-radius: 24px;
        padding: 40px;
        margin-bottom: 40px;
        border: 1px solid rgba(79, 70, 229, 0.2);
        backdrop-filter: blur(20px);
        box-shadow: 
            0 16px 64px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .question-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #4f46e5, #7c3aed, #ec4899, transparent);
        transition: left 0.8s ease;
    }
    
    .question-card:hover::before {
        left: 100%;
    }
    
    .question-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(79, 70, 229, 0.4);
        box-shadow: 
            0 24px 80px rgba(79, 70, 229, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    .question-number {
        display: inline-block;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(79, 70, 229, 0.4);
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 8px 24px rgba(79, 70, 229, 0.4); }
        50% { box-shadow: 0 8px 24px rgba(79, 70, 229, 0.6), 0 0 20px rgba(79, 70, 229, 0.3); }
    }
    
    .question-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 12px;
        line-height: 1.4;
    }
    
    .question-example {
        font-size: 1rem;
        color: #9ca3af;
        margin-bottom: 25px;
        font-style: italic;
        font-weight: 400;
    }
    
    /* Enhanced text areas */
    .stTextArea textarea {
        background: rgba(26, 26, 26, 0.9) !important;
        border: 2px solid rgba(79, 70, 229, 0.3) !important;
        border-radius: 16px !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        padding: 20px !important;
        font-family: 'Poppins', sans-serif !important;
        line-height: 1.6 !important;
        resize: vertical !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #4f46e5 !important;
        outline: none !important;
        box-shadow: 
            0 0 0 3px rgba(79, 70, 229, 0.3) !important,
            0 8px 32px rgba(79, 70, 229, 0.2) !important;
        background: rgba(26, 26, 26, 0.95) !important;
        transform: translateY(-2px) !important;
    }
    
    .stTextArea textarea:hover {
        border-color: rgba(79, 70, 229, 0.5) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #6b7280 !important;
        font-style: italic !important;
    }
    
    /* Navigation buttons */
    .nav-buttons {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 60px;
        gap: 20px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed, #ec4899) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 16px 32px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        font-family: 'Poppins', sans-serif !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 24px rgba(79, 70, 229, 0.4) !important;
        position: relative !important;
        overflow: hidden !important;
        min-width: 160px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.6s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.05) !important;
        box-shadow: 0 16px 40px rgba(79, 70, 229, 0.6) !important;
        background: linear-gradient(135deg, #5b52f0, #8b47ed, #f472b6) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(1.02) !important;
    }
    
    /* Results section */
    .results-container {
        margin-top: 80px;
        padding: 60px;
        background: rgba(45, 45, 45, 0.6);
        border-radius: 30px;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 24px 80px rgba(0, 0, 0, 0.4);
        animation: slideInUp 0.8s ease-out;
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(60px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .results-title {
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 40px;
        background: linear-gradient(135deg, #4f46e5, #7c3aed, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Enhanced dataframe styling */
    .stDataFrame {
        border-radius: 20px !important;
        overflow: hidden !important;
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .stDataFrame table {
        background: rgba(26, 26, 26, 0.9) !important;
        backdrop-filter: blur(20px) !important;
    }
    
    .stDataFrame th {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 20px !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stDataFrame td {
        background: rgba(45, 45, 45, 0.8) !important;
        color: #ffffff !important;
        padding: 16px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
    }
    
    .stDataFrame tr:hover td {
        background: rgba(79, 70, 229, 0.1) !important;
        transform: scale(1.01) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Success and info messages */
    .stInfo, .stSuccess {
        background: rgba(45, 45, 45, 0.9) !important;
        border: 1px solid rgba(79, 70, 229, 0.3) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(20px) !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        padding: 20px !important;
        margin: 20px 0 !important;
        box-shadow: 0 8px 24px rgba(79, 70, 229, 0.2) !important;
    }
    
    .stSuccess {
        border-color: rgba(34, 197, 94, 0.3) !important;
        box-shadow: 0 8px 24px rgba(34, 197, 94, 0.2) !important;
    }
    
    .stWarning {
        background: rgba(251, 191, 36, 0.1) !important;
        border: 1px solid rgba(251, 191, 36, 0.3) !important;
        border-radius: 16px !important;
        color: #fbbf24 !important;
        backdrop-filter: blur(20px) !important;
    }
    
    /* Progress indicators */
    .progress-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 40px 0;
        gap: 12px;
    }
    
    .progress-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: rgba(79, 70, 229, 0.3);
        transition: all 0.3s ease;
    }
    
    .progress-dot.active {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
        transform: scale(1.3);
    }
    
    .progress-dot.completed {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.4);
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .content-container {
            padding: 20px;
        }
        
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            text-align: center;
            font-size: 1.1rem;
        }
        
        .question-card {
            padding: 24px;
            margin-bottom: 24px;
        }
        
        .navbar {
            padding: 16px 20px;
        }
        
        .logo {
            font-size: 2rem;
        }
        
        .nav-buttons {
            flex-direction: column;
            gap: 16px;
        }
        
        .stButton > button {
            width: 100% !important;
            min-width: auto !important;
        }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(45, 45, 45, 0.3);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5b52f0, #8b47ed);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
#         Main Application
# -------------------------------

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = 0

# Navigation bar
st.markdown("""
<div class="navbar">
    <div class="logo">👜 CareerFinder</div>
</div>
""", unsafe_allow_html=True)

# Content container
st.markdown('<div class="content-container">', unsafe_allow_html=True)

# Hero section
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">Discover Your Dream Career</h1>
    <p class="hero-subtitle">
        Answer a few questions and let our AI-powered system recommend the perfect career paths tailored to your skills, interests, and aspirations. Your future starts here!
    </p>
</div>
""", unsafe_allow_html=True)

# List of questions and examples
questions_with_examples = [
    {
        "question": "What are the top 3 technical or soft skills you're most confident in?",
        "example": "💡 Examples: coding, writing, public speaking, problem-solving, creativity, leadership"
    },
    {
        "question": "Which types of activities do you enjoy doing in your free time?",
        "example": "🎯 Examples: designing, organizing, teaching, building, analyzing data, creative projects"
    },
    {
        "question": "Which industries or fields are you most interested in?",
        "example": "🏢 Examples: healthcare, finance, education, technology, creative arts, sustainability"
    },
    {
        "question": "What is your current education level and area of study?",
        "example": "🎓 Examples: Diploma in IT, Bachelor's in Business, self-taught coder, Master's in Marketing"
    },
    {
        "question": "What kind of tasks or responsibilities do you see yourself enjoying in a job?",
        "example": "⚡ Examples: leading teams, writing reports, solving technical problems, helping customers, managing projects"
    },
    {
        "question": "What are your top 3 priorities in a career?",
        "example": "🌟 Examples: high salary, work-life balance, career growth, helping others, creativity, flexibility"
    }
]

# Progress indicators
total_pages = (len(questions_with_examples) + 1) // 2
current_page = st.session_state.page

progress_html = '<div class="progress-container">'
for i in range(total_pages):
    if i < current_page:
        progress_html += '<div class="progress-dot completed"></div>'
    elif i == current_page:
        progress_html += '<div class="progress-dot active"></div>'
    else:
        progress_html += '<div class="progress-dot"></div>'
progress_html += '</div>'
st.markdown(progress_html, unsafe_allow_html=True)

# Question display logic
start = st.session_state.page * 2
end = start + 2
current_qs = questions_with_examples[start:end]

with st.form(key=f"form_page_{st.session_state.page}"):
    for idx, q in enumerate(current_qs):
        q_index = start + idx + 1
        
        st.markdown(f'''
        <div class="question-card">
            <div class="question-number">{q_index}</div>
            <h2 class="question-title">{q['question']}</h2>
            <p class="question-example">{q['example']}</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.text_area(
            "Your answer", 
            key=f"q{q_index}", 
            height=120, 
            label_visibility="collapsed",
            placeholder=f"Share your thoughts for question {q_index}..."
        )

    # Navigation buttons
    st.markdown('<div class="nav-buttons">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.page > 0:
            back = st.form_submit_button("← Back", type="secondary")
        else:
            back = False
    
    with col3:
        next_or_submit = "Next →" if end < len(questions_with_examples) else "🚀 Get My Career Recommendations"
        next_clicked = st.form_submit_button(next_or_submit, type="primary")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Navigation logic
    if back and st.session_state.page > 0:
        st.session_state.page -= 1
        st.rerun()

    if next_clicked:
        if end < len(questions_with_examples):
            st.session_state.page += 1
            st.rerun()
        else:
            # Set flag to show results
            st.session_state.show_results = True

# Handle results display OUTSIDE the form
if st.session_state.get('show_results', False):
    # Collect all responses
    combined_input = " ".join([
        st.session_state.get(f"q{i+1}", "") for i in range(len(questions_with_examples))
    ])
    
    if combined_input.strip():
        # Show loading state
        with st.spinner("🔍 Analyzing your responses with AI..."):
            results_df = recommend_careers(
                combined_input, df, vectorizer, tfidf_matrix, sbert_embeddings
            )
        
        # Display results
        st.markdown("""
        <div class="results-container">
            <h2 class="results-title">🎯 Your Personalized Career Recommendations</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.success("✨ Analysis complete! Here are your top career matches based on your responses:")
        
        # Enhanced dataframe display
        st.dataframe(
            results_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Additional insights
        if not results_df.empty:
            top_match = results_df.iloc[0]
            st.info(f"""
            🏆 **Top Match**: {top_match['Job Title']}
            
            💰 **Salary Range**: {top_match['Salary Range (Average)']}
            
            🎯 **Match Score**: {top_match['Combined Score']:.1%}

            🔧 **Key Skills**: {top_match['Skills'][:150]}{'...' if len(top_match['Skills']) > 150 else ''}
            """)
            
            # Show detailed breakdown for top 3 matches
            st.markdown("### 📊 Detailed Career Analysis")
            
            for i, (_, career) in enumerate(results_df.iterrows()):
                with st.expander(f"🎯 **{career['Job Title']}** - Match Score: {career['Combined Score']:.1%}", expanded=(i==0)):
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown(f"""
                        **💼 Role Overview:**
                        {career['Role']}
                        
                        **💰 Salary Range:**
                        {career['Salary Range (Average)']}
                        
                        **🎯 AI Match Scores:**
                        - TF-IDF Score: {career['TF-IDF Score']:.3f}
                        - SBERT Score: {career['SBERT Score']:.3f}
                        - Combined Score: {career['Combined Score']:.3f}
                        """)
                    
                    with col2:
                        st.markdown(f"""
                        **🔧 Required Skills:**
                        {career['Skills']}
                        
                        **📋 Key Responsibilities:**
                        {career['Responsibilities'][:300]}{'...' if len(career['Responsibilities']) > 300 else ''}
                        """)
                    
                    st.markdown(f"""
                    **📝 Job Description:**
                    {career['Job Description'][:400]}{'...' if len(career['Job Description']) > 400 else ''}
                    """)
        
        # Action buttons - NOW OUTSIDE THE FORM
        st.markdown("### 🚀 Next Steps")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Try New Search", key="new_search"):
                # Reset all session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.session_state.page = 0
                st.rerun()
        
        with col2:
            if st.button("📊 View All Results", key="view_all"):
                st.markdown("### 📈 Complete Results Table")
                st.dataframe(
                    results_df,
                    use_container_width=True,
                    hide_index=True
                )
        
        with col3:
            # Download results as CSV
            csv_data = results_df.to_csv(index=False)
            st.download_button(
                label="💾 Download Results",
                data=csv_data,
                file_name="career_recommendations.csv",
                mime="text/csv",
                key="download_results"
            )
        
    else:
        st.warning("⚠️ Please provide answers to the questions to get personalized recommendations.")
        # Reset the flag if no input provided
        st.session_state.show_results = False

# Close content container
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="
    margin-top: 80px; 
    padding: 40px; 
    text-align: center; 
    background: rgba(45, 45, 45, 0.3); 
    border-radius: 20px; 
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
">
    <p style="color: #9ca3af; font-size: 1rem; margin-bottom: 16px;">
        🤖 Powered by AI • Built with ❤️ for Career Discovery
    </p>
    <p style="color: #6b7280; font-size: 0.9rem;">
        Using TF-IDF + SBERT embeddings for intelligent career matching
    </p>
</div>
""", unsafe_allow_html=True)

