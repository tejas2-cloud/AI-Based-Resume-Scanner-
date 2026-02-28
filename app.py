import streamlit as st
import pandas as pd
import os
from src.parser import parse_resume
from src.preprocess import preprocess_text
from src.vectorizer import get_embeddings
from src.matcher import calculate_similarity
from src.ranker import rank_candidates
from src.skill_extractor import extract_skills, get_missing_skills

# UI Configuration
st.set_page_config(page_title="AI Resume Intelligence", page_icon="🚀", layout="wide")

# Advanced Premium CSS
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">

<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Outfit', sans-serif;
    }
    
    /* Header Section */
    .header-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .header-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -1px;
    }
    
    /* Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        text-align: center;
        color: #1e293b; /* Ensure dark text */
    }
    
    .metric-card h2, .metric-card h4, .metric-card h5 {
        color: #764ba2 !important;
        font-weight: 700 !important;
    }
    
    .metric-card p {
        color: #475569 !important;
    }
    
    .candidate-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: transform 0.2s ease;
        color: #1e293b;
    }
    
    .candidate-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        width: 100%;
        box-shadow: 0 4px 15px rgba(118, 75, 162, 0.3);
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(118, 75, 162, 0.4);
    }
    
    /* Skills Tags */
    .skill-tag {
        display: inline-block;
        background: #e0e7ff;
        color: #4338ca;
        padding: 0.2rem 0.8rem;
        border-radius: 50px;
        font-size: 0.85rem;
        margin: 0.2rem;
        font-weight: 500;
    }
    
    .missing-tag {
        display: inline-block;
        background: #fee2e2;
        color: #b91c1c;
        padding: 0.2rem 0.8rem;
        border-radius: 50px;
        font-size: 0.85rem;
        margin: 0.2rem;
        font-weight: 500;
    }

    /* Tabs/Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        color: #764ba2 !important;
        font-weight: 700 !important;
    }
    
    .header-container p {
        font-size: 1.3rem !important;
        color: white !important;
        opacity: 1.0 !important;
        font-weight: 400 !important;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">AI Based Resume Scanner 🚀</h1>
        <p style="font-size: 1.3rem; opacity: 0.9;">Revolutionize your hiring with semantic screening and deep neural analysis</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.markdown("### 📥 Input Center")
    uploaded_files = st.file_uploader("Drop Resumes Here", type=['pdf', 'docx'], accept_multiple_files=True)
    
    st.markdown("---")
    
    st.markdown("### 📝 Job Profile")
    jd_text = st.text_area("Define Requirements", height=300, placeholder="Paste your JD here for semantic alignment...")
    
    st.markdown("---")
    process_btn = st.button("� Rank Candidates Now")

# Main Logic
if process_btn:
    if not uploaded_files:
        st.error("Please upload at least one resume.")
    elif not jd_text.strip():
        st.error("Please provide a job description.")
    else:
        with st.spinner("⚡ Powering up AI Models & Extracting Features..."):
            # Logic remains same but with better feedback
            processed_jd = preprocess_text(jd_text)
            jd_skills = extract_skills(jd_text)
            
            resumes_data = []
            all_processed_resumes = []
            
            # Progress bar for parsing
            parse_progress = st.progress(0, text="Parsing Documents...")
            
            # Ensure directories exist
            save_dir = os.path.join("data", "resumes")
            os.makedirs(save_dir, exist_ok=True)
            
            for i, uploaded_file in enumerate(uploaded_files):
                temp_path = os.path.join(save_dir, uploaded_file.name)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                raw_text = parse_resume(temp_path)
                processed_text = preprocess_text(raw_text)
                resume_skills = extract_skills(raw_text)
                missing_skills = get_missing_skills(resume_skills, jd_skills)
                
                resumes_data.append({
                    "filename": uploaded_file.name,
                    "raw_text": raw_text,
                    "skills": resume_skills,
                    "missing_skills": missing_skills
                })
                all_processed_resumes.append(processed_text)
                parse_progress.progress((i + 1) / len(uploaded_files))

            # Embedding Logic
            all_texts = [processed_jd] + all_processed_resumes
            embeddings = get_embeddings(all_texts)
            scores = calculate_similarity(embeddings[1:], embeddings[0])
            
            for i, score in enumerate(scores):
                resumes_data[i]["score"] = round(score * 100, 2)
            
            ranked_resumes = rank_candidates(resumes_data)
            
            # --- Results Presentation ---
            st.markdown("### � Analytical Overview")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="metric-card"><h5>Total Pool</h5><h2>{len(ranked_resumes)}</h2></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="metric-card"><h5>High Relevance</h5><h2>{len([r for r in ranked_resumes if r["score"] > 70])}</h2></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="metric-card"><h5>Top Match</h5><h2>{ranked_resumes[0]["score"]}%</h2></div>', unsafe_allow_html=True)

            st.markdown("---")
            
            # Interactive Table
            st.markdown("### 🏆 Final Leaderboard")
            res_df = pd.DataFrame(ranked_resumes)
            st.dataframe(
                res_df[["filename", "score"]],
                use_container_width=True,
                column_config={
                    "score": st.column_config.ProgressColumn("Semantic Relevance", format="%f%%", min_value=0, max_value=100),
                    "filename": "Candidate Attachment"
                }
            )

            st.markdown("---")
            st.markdown("### 🧬 Candidate Deep-Dive")
            
            for i, cand in enumerate(ranked_resumes):
                with st.expander(f"⭐ Rank #{i+1}: {cand['filename']} ({cand['score']}%)"):
                    col_a, col_b = st.columns([1, 2])
                    
                    with col_a:
                        st.markdown("**Core Skill Match**")
                        # Skill tags
                        skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in cand['skills']])
                        st.markdown(skills_html if cand['skills'] else "---", unsafe_allow_html=True)
                        
                        st.markdown("**Gap Analysis**")
                        missing_html = "".join([f'<span class="missing-tag">{s}</span>' for s in cand['missing_skills']])
                        st.markdown(missing_html if cand['missing_skills'] else "All skills matched! ✅", unsafe_allow_html=True)
                    
                    with col_b:
                        st.markdown("**Intelligent Summary/Preview**")
                        st.info(cand['raw_text'][:1200] + "...")

else:
    # Landing View
    st.markdown("""
        <div style="text-align: center; padding: 5rem 0;">
            <h2 style="color: #1e293b; font-weight: 300;">Ready to find your best hire?</h2>
            <p style="color: #334155; margin-bottom: 2rem;">Upload your files in the sidebar and click process to begin the magic.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Simple feature boxes
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown('<div class="metric-card"><h4>⚡ Fast</h4><p>Process 100+ resumes in seconds</p></div>', unsafe_allow_html=True)
    with f2:
        st.markdown('<div class="metric-card"><h4>🧠 Smart</h4><p>Context-aware NLP understanding</p></div>', unsafe_allow_html=True)
    with f3:
        st.markdown('<div class="metric-card"><h4>🔒 Private</h4><p>Your data stays on your system</p></div>', unsafe_allow_html=True)
