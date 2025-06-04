import streamlit as st  # type: ignore
import streamlit.components.v1 as components # type: ignore

# Set page configuration
st.set_page_config(page_title="CareerFinder", page_icon="👜", layout="wide")

# Remove streamlit's borders and apply dark theme
st.markdown("""
    <style>
        /* Remove ALL default Streamlit margins and padding */
        .stApp {
            background-color: #0f0f0f !important;
            margin: 0 !important;
            padding: 0 !important;
            top: 0 !important;
        }
        
        .main {
            background-color: #0f0f0f !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .block-container { 
            padding: 0 !important; 
            background-color: #0f0f0f !important;
            margin: 0 !important;
            max-width: none !important;
            padding-top: 0 !important;
        }
        
        /* Hide Streamlit header and footer completely */
        header[data-testid="stHeader"] {
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        footer {
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove top spacing from main container */
        div[data-testid="stAppViewContainer"] {
            background-color: #0f0f0f !important;
            margin: 0 !important;
            padding: 0 !important;
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# HTML and CSS for the UI with vibrant dark theme
html_code = """
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Poppins', sans-serif;
    }
    
    html, body {
        margin: 0 !important;
        padding: 0 !important;
        background: #0f0f0f !important;
        min-height: 100vh;
    }
    
    body {
        background: #0f0f0f !important;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        width: 100vw;
        overflow-x: hidden;
        overflow-y: auto;
        position: relative;
    }
    
    /* Add subtle animated background pattern */
    body::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 80%, rgba(79, 70, 229, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(124, 58, 237, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(79, 70, 229, 0.05) 0%, transparent 50%);
        z-index: 0;
        pointer-events: none;
    }
    
    .navbar {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        display: flex;
        align-items: center;
        padding: 18px 30px;
        width: 100%;
        box-shadow: 0 4px 20px rgba(79, 70, 229, 0.3);
        position: relative;
        z-index: 1000;
        backdrop-filter: blur(10px);
    }
    
    .navbar .logo {
        font-family: 'Poppins', sans-serif;
        color: white;
        font-size: 2.2rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .navbar .logo:hover {
        transform: scale(1.05) translateY(-2px);
        text-shadow: 0 4px 8px rgba(0,0,0,0.4);
    }
    
    .container {
        background: rgba(45, 45, 45, 0.95);
        width: 90%;
        max-width: 75%;
        margin: 60px auto 40px auto;
        padding: 3rem 2rem;
        border-radius: 20px;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.6),
            0 0 0 1px rgba(255, 255, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        text-align: center;
        border: 1px solid rgba(79, 70, 229, 0.2);
        backdrop-filter: blur(20px);
        position: relative;
        z-index: 2;
        transition: all 0.3s ease;
    }
    
    .container:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.7),
            0 0 0 1px rgba(255, 255, 255, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }

    .quote-container {
        display: flex;
        overflow: hidden;
        white-space: nowrap;
        position: relative;
        width: 100%;
        margin: 30px 0;
    }

    .moving-quotes {
        display: flex;
        gap: 50px;
        animation: moveLeft 15s linear infinite;
        min-width: 200%;
    }

    @keyframes moveLeft {
        0% {
            transform: translateX(0);
        }
        100% {
            transform: translateX(-50%);
        }
    }

    .quote {
        font-style: italic;
        color: #b0b0b0;
        font-size: 1.2rem;
        padding-right: 50px;
        display: inline-block;
        font-weight: 500;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    .button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        padding: 16px 32px;
        font-size: 1.3rem;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        cursor: pointer;
        margin-top: 30px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
        position: relative;
        overflow: hidden;
        text-decoration: none;
        display: inline-block;
    }
    
    .button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .button:hover::before {
        left: 100%;
    }
    
    .button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.6);
        background: linear-gradient(135deg, #5b52f0, #8b47ed);
    }

    h1 {
        margin: 30px 0;
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    h2 {
        font-size: 2rem;
        color: #ffffff;
        margin-bottom: 1.5rem;
        font-weight: 600;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    p {
        font-size: 1.1rem;
        color: #b0b0b0;
        line-height: 1.6;
        font-weight: 400;
    }
    
    .aboutus-container {
        display: flex;
        justify-content: center;
        gap: 30px;
        flex-wrap: wrap;
        margin: 40px 0;
    }

    /* Offering Boxes Section */
    .offering-section {
        padding: 3rem 2rem;
        background: rgba(26, 26, 26, 0.8);
        text-align: center;
        transition: all 0.3s ease;
        border-radius: 20px;
        margin-top: 40px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(79, 70, 229, 0.1);
    }

    .offering-section h2 {
        font-size: 2.5rem;
        margin-bottom: 2rem;
        color: #ffffff;
        background: linear-gradient(135deg, #ffffff, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .offering-section h4 {
        font-size: 2.5rem;
        margin-bottom: 2rem;
        font-family: 'Times New Roman', serif;
        color: #ffffff;
    }

    .offering-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.2rem;
        padding: 0;
        justify-items: center;
        max-width: 800px;
        margin: 0 auto;
    }

    .offering-box {
        background: rgba(45, 45, 45, 0.9);
        border: 2px solid rgba(79, 70, 229, 0.3);
        border-radius: 15px;
        padding: 2rem;
        opacity: 0;
        transform: translateY(50px);
        transition: all 0.5s ease;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        max-width: 350px;
        width: 100%;
    }
    
    .offering-box.show {
        opacity: 1;
        transform: translateY(0);
    }

    .offering-box:hover {
        transform: scale(1.05) translateY(-10px);
        box-shadow: 0 8px 30px rgba(79, 70, 229, 0.4);
        border-color: rgba(79, 70, 229, 0.6);
    }

    .offering-box img {
        width: 180px;  
        height: 180px; 
        object-fit: cover;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .offering-box:hover img {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }

    .offering-box h3 {
        font-size: 1.4rem;
        margin-bottom: 1rem;
        color: #ffffff;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }

    .offering-box p {
        font-size: 1rem;
        color: #b0b0b0;
        line-height: 1.5;
    }

    a {
        text-decoration: none;
        transition: all 0.3s ease;
    }
    
    a:hover {
        transform: translateY(-2px);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .container {
            width: 95%;
            margin: 40px auto;
            padding: 2rem 1.5rem;
        }
        
        .navbar {
            padding: 15px 20px;
        }
        
        .navbar .logo {
            font-size: 1.8rem;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
        
        .offering-container {
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }
        
        .aboutus-container {
            flex-direction: column;
            align-items: center;
        }
        
        .button {
            font-size: 1.1rem;
            padding: 14px 28px;
        }
        
        .quote {
            font-size: 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .container {
            width: 98%;
            padding: 1.5rem 1rem;
        }
        
        .offering-section {
            padding: 2rem 1rem;
        }
        
        .offering-box {
            padding: 1.5rem;
        }
        
        .offering-box img {
            width: 150px;
            height: 150px;
        }
    }
</style>

<script>
    document.addEventListener("DOMContentLoaded", function () {
        const boxes = document.querySelectorAll(".offering-box");

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("show");
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: "0px 0px -50px 0px"
        });

        boxes.forEach(box => observer.observe(box));
    });
</script>

<div class="navbar">
    <div class="logo">👜 CareerFinder</div>
</div>

<div class="container">
    <h1>AI-Powered Career Guidance</h1>
    <h2 style="padding: 20px; margin-bottom: 0;">Find your personalized career for a brighter future</h2>
    
    <div class="quote-container">
        <div class="moving-quotes">
            <span class="quote">"Your career path isn't just a choice—it's a journey. Let AI guide you to where you truly belong."</span>
            <span class="quote">"Discover careers that match your passion and expertise, powered by AI."</span>
            <span class="quote">"AI doesn't just predict your career; it helps you create it."</span>
            <span class="quote">"From skills to success – AI-powered career systems making your next move easier."</span>
        </div>
    </div>

    <button onclick="window.location.href = '/recosystem';" class="button">Find your career!</button>

    <div style="margin: 60px 0;">
        <h2>About Us</h2>
        <p style="margin-bottom: 30px;">We are just 2 Diploma in IT students that are determined to help individuals find the best suited career path to pursue.</p>
        
        <div class="aboutus-container">
            <a href="https://www.youtube.com" target="_blank">
                <div class="offering-box show">
                    <img src="https://static.wikia.nocookie.net/universalstudios/images/f/f2/Shrek2-disneyscreencaps.com-4369.jpg" alt="samuel">
                    <h3>Samuel Wong Yu Yang</h3>
                    <p>Semester 5 Diploma student from SCKL</p>
                </div>
            </a>

            <a href="https://www.youtube.com" target="_blank">
                <div class="offering-box show">
                    <img src="https://static.wikia.nocookie.net/shrek/images/6/61/Shrek3-disneyscreencaps.com-2156.jpg" alt="bryan">
                    <h3>Bryan Wong Chi Kit</h3>
                    <p>Semester 5 Diploma student from SCKL</p>
                </div>
            </a>
        </div>
    </div>
</div>

<section class="offering-section">
    <h2>Our Offerings</h2>
    <div class="offering-container">
        <div class="offering-box">
            <img src="https://www.mooglelabs.com/frontend/assests/images/job-recommended/banner-img.png" alt="AI-Powered Career Recommendations">
            <h3>AI-Powered Career Recommendations</h3>
            <p>This feature allows users to answer some questions to find their best suited careers</p>
        </div>
        <div class="offering-box">
            <img src="https://images.prismic.io/turing/652ebec8fbd9a45bcec81892_Which_Language_Is_Useful_for_NLP_and_Why_62f7833585.webp?auto=format,compress" alt="NLP Resume Parsing">
            <h3>NLP (Natural Language Processing) Features</h3>
            <p>Extracts skills from resumes using NLP and provides personalized insights for companies.</p>
        </div>
        <div class="offering-box">
            <img src="https://www.talentlms.com/blog/wp-content/uploads/2024/07/Learning-Paths_6June2024_Big.png" alt="Learning Path & Course Suggestions">
            <h3>Learning Path & Course Suggestions</h3>
            <p>Recommends courses from third party platforms like Udemy and Coursera to upskill users.</p>
        </div>
        <div class="offering-box">
            <img src="https://www.almawave.com/wp-content/uploads/2024/10/BLOG-CONVERSATION-STUDIO-3.webp" alt="AI chatbot">
            <h3>AI Chatbot</h3>
            <p>An AI-powered chatbot made to offer resume tips, interview advice, and hiring trends using NLP.</p>
        </div>
    </div>
</section>
"""

# Display the UI in Streamlit
components.html(html_code, height=1200, scrolling=True)