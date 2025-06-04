import streamlit as st # type: ignore
import streamlit.components.v1 as components # type: ignore

# Page configuration
st.set_page_config(
    page_title="CareerFinder", 
    page_icon="👜", 
    layout="wide"
)

# Remove Streamlit default styling and apply dark theme
st.markdown("""
<style>
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
    
    div[data-testid="stAppViewContainer"] {
        background-color: #0f0f0f !important;
        margin: 0 !important;
        padding: 0 !important;
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Main HTML component with vibrant dark theme
html_content = """
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
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
            overflow-x: hidden;
        }
        
        body {
            background: #0f0f0f !important;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            position: relative;
        }
        
        /* Animated background pattern */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 80%, rgba(79, 70, 229, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(124, 58, 237, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(79, 70, 229, 0.08) 0%, transparent 50%);
            z-index: 0;
            pointer-events: none;
            animation: pulse 4s ease-in-out infinite alternate;
        }
        
        @keyframes pulse {
            0% { opacity: 0.8; }
            100% { opacity: 1; }
        }
        
        .navbar {
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 18px 30px;
            box-shadow: 0 4px 20px rgba(79, 70, 229, 0.4);
            position: relative;
            z-index: 1000;
            backdrop-filter: blur(10px);
        }
        
        .logo {
            font-size: 2.2rem;
            font-weight: 700;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .logo:hover { 
            transform: scale(1.05) translateY(-2px);
            text-shadow: 0 4px 8px rgba(0,0,0,0.4);
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
        }
        
        .nav-links a {
            color: white;
            font-size: 1.2rem;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.3s ease;
            padding: 10px 18px;
            border-radius: 8px;
            backdrop-filter: blur(10px);
        }
        
        .nav-links a:hover {
            background: rgba(255,255,255,0.15);
            transform: translateY(-3px);
            box-shadow: 0 4px 15px rgba(255,255,255,0.1);
        }
        
        .search-container {
            position: relative;
            display: flex;
            align-items: center;
        }
        
        .search-bar {
            padding: 14px 50px 14px 20px;
            font-size: 1rem;
            border: 2px solid rgba(255,255,255,0.2);
            border-radius: 25px;
            outline: none;
            width: 350px;
            background: rgba(255,255,255,0.1);
            color: white;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .search-bar::placeholder {
            color: rgba(255,255,255,0.7);
        }
        
        .search-bar:focus {
            border-color: rgba(255,255,255,0.4);
            background: rgba(255,255,255,0.15);
            box-shadow: 0 0 20px rgba(79, 70, 229, 0.3);
        }
        
        .search-icon {
            position: absolute;
            right: 15px;
            background: none;
            border: none;
            font-size: 1.2rem;
            cursor: pointer;
            color: rgba(255,255,255,0.8);
            transition: all 0.3s ease;
        }
        
        .search-icon:hover {
            color: white;
            transform: scale(1.2);
        }
        
        .auth-section {
            position: absolute;
            top: 100px;
            right: 40px;
            display: flex;
            gap: 15px;
            z-index: 999;
        }
        
        .btn {
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: white;
            padding: 12px 24px;
            font-size: 1rem;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
            position: relative;
            overflow: hidden;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn:hover {
            background: linear-gradient(135deg, #5b52f0, #8b47ed);
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(79, 70, 229, 0.6);
        }
        
        .main-content {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 60px 40px;
            position: relative;
            z-index: 2;
        }
        
        .hero-card {
            background: rgba(45, 45, 45, 0.95);
            padding: 50px;
            border-radius: 20px;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.6),
                0 0 0 1px rgba(255, 255, 255, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            text-align: center;
            max-width: 700px;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(79, 70, 229, 0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .hero-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(79, 70, 229, 0.1), transparent);
            animation: shimmer 3s linear infinite;
            pointer-events: none;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        .hero-card:hover {
            transform: translateY(-8px);
            box-shadow: 
                0 12px 40px rgba(0, 0, 0, 0.7),
                0 0 0 1px rgba(255, 255, 255, 0.15),
                inset 0 1px 0 rgba(255, 255, 255, 0.15);
        }
        
        .hero-card h1 {
            font-size: 3rem;
            margin-bottom: 25px;
            font-weight: 700;
            background: linear-gradient(135deg, #ffffff, #e0e7ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            position: relative;
            z-index: 1;
        }
        
        .hero-card p {
            font-size: 1.3rem;
            color: #b0b0b0;
            margin-bottom: 35px;
            line-height: 1.7;
            font-weight: 400;
            position: relative;
            z-index: 1;
        }
        
        .cta-btn {
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: white;
            padding: 18px 36px;
            font-size: 1.3rem;
            font-weight: 600;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(79, 70, 229, 0.4);
            position: relative;
            z-index: 1;
            overflow: hidden;
        }
        
        .cta-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .cta-btn:hover::before {
            left: 100%;
        }
        
        .cta-btn:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 30px rgba(79, 70, 229, 0.6);
            background: linear-gradient(135deg, #5b52f0, #8b47ed);
        }
        
        /* Floating elements animation */
        .floating-element {
            position: absolute;
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, rgba(79, 70, 229, 0.2), rgba(124, 58, 237, 0.2));
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
            z-index: 1;
        }
        
        .floating-element:nth-child(1) {
            top: 20%;
            left: 10%;
            animation-delay: 0s;
        }
        
        .floating-element:nth-child(2) {
            top: 60%;
            right: 15%;
            animation-delay: 2s;
        }
        
        .floating-element:nth-child(3) {
            bottom: 30%;
            left: 5%;
            animation-delay: 4s;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        @media (max-width: 768px) {
            .navbar {
                flex-direction: column;
                gap: 20px;
                padding: 20px;
            }
            
            .nav-links {
                gap: 1rem;
            }
            
            .search-bar {
                width: 280px;
            }
            
            .auth-section {
                position: relative;
                top: 0;
                right: 0;
                margin-top: 20px;
            }
            
            .hero-card {
                padding: 35px 25px;
                margin: 0 20px;
            }
            
            .hero-card h1 {
                font-size: 2.2rem;
            }
            
            .hero-card p {
                font-size: 1.1rem;
            }
            
            .cta-btn {
                font-size: 1.1rem;
                padding: 15px 30px;
            }
            
            .floating-element {
                display: none;
            }
        }
        
        @media (max-width: 480px) {
            .navbar {
                padding: 15px;
            }
            
            .logo {
                font-size: 1.8rem;
            }
            
            .nav-links a {
                font-size: 1rem;
                padding: 8px 12px;
            }
            
            .search-bar {
                width: 250px;
                padding: 12px 40px 12px 15px;
            }
            
            .hero-card {
                padding: 30px 20px;
            }
            
            .hero-card h1 {
                font-size: 1.8rem;
            }
        }
    </style>
</head>
<body>
    <div class="floating-element"></div>
    <div class="floating-element"></div>
    <div class="floating-element"></div>
    
    <nav class="navbar">
        <div class="logo">👜 CareerFinder</div>
        <div class="nav-links">
            <a href="#jobs">Jobs</a>
            <a href="#network">Network</a>
            <a href="#companies">Companies</a>
            <a href="#profile">👤</a>
        </div>
        <div class="search-container">
            <input type="text" placeholder="Search companies, jobs or people" class="search-bar">
            <button class="search-icon">🔍</button>
        </div>
    </nav>
    
    <div class="auth-section">
        <button class="btn">Login</button>
        <button class="btn">Sign Up</button>
    </div>
    
    <main class="main-content">
        <div class="hero-card">
            <h1>Find Your Dream Career</h1>
            <p>Connect with top companies, discover exciting opportunities, and build your professional network all in one place. Let AI guide you to where you truly belong.</p>
            <button class="cta-btn">Get Started</button>
        </div>
    </main>
</body>
</html>
"""

# Render the component
components.html(html_content, height=800, scrolling=True)
