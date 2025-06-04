import streamlit as st # type: ignore
import streamlit.components.v1 as components # type: ignore

# Page configuration
st.set_page_config(
    page_title="CareerFinder", 
    page_icon="👜", 
    layout="wide"
)

# Remove Streamlit default styling
st.markdown("""
<style>
    .block-container { padding: 0 !important; }
    .main { background-color: white !important; }
    header, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Main HTML component
html_content = """
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }
        
        body {
            background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)),
                        url('https://media.istockphoto.com/id/535677723/vector/leadership.jpg?s=612x612&w=0&k=20&c=kzFB3FNFh3lcSBZhvs525cV9FSA40nZhQA-bSFWZoa8=');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .navbar {
            background: #4f46e5;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .logo {
            font-size: 2rem;
            font-weight: 700;
            color: white;
            cursor: pointer;
            transition: transform 0.3s ease;
        }
        
        .logo:hover { transform: scale(1.05); }
        
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
            padding: 8px 16px;
            border-radius: 6px;
        }
        
        .nav-links a:hover {
            background: rgba(255,255,255,0.1);
            transform: translateY(-2px);
        }
        
        .search-container {
            position: relative;
            display: flex;
            align-items: center;
        }
        
        .search-bar {
            padding: 12px 50px 12px 20px;
            font-size: 1rem;
            border: none;
            border-radius: 25px;
            outline: none;
            width: 350px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .search-icon {
            position: absolute;
            right: 15px;
            background: none;
            border: none;
            font-size: 1.2rem;
            cursor: pointer;
            color: #666;
            transition: all 0.2s ease;
        }
        
        .search-icon:hover {
            color: #4f46e5;
            transform: scale(1.1);
        }
        
        .auth-section {
            position: absolute;
            top: 80px;
            right: 40px;
            display: flex;
            gap: 15px;
        }
        
        .btn {
            background: #4f46e5;
            color: white;
            padding: 10px 20px;
            font-size: 1rem;
            font-weight: 600;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            background: #4338ca;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        .main-content {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px;
        }
        
        .hero-card {
            background: rgba(255,255,255,0.95);
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            text-align: center;
            max-width: 600px;
            backdrop-filter: blur(10px);
        }
        
        .hero-card h1 {
            font-size: 2.5rem;
            color: #1f2937;
            margin-bottom: 20px;
        }
        
        .hero-card p {
            font-size: 1.1rem;
            color: #6b7280;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        
        .cta-btn {
            background: linear-gradient(45deg, #4f46e5, #7c3aed);
            color: white;
            padding: 15px 30px;
            font-size: 1.2rem;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .cta-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
        }
        
        @media (max-width: 768px) {
            .navbar {
                flex-direction: column;
                gap: 15px;
            }
            
            .search-bar {
                width: 250px;
            }
            
            .auth-section {
                position: relative;
                top: 0;
                right: 0;
                margin-top: 20px;
            }
            
            .hero-card h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
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
            <p>Connect with top companies, discover exciting opportunities, and build your professional network all in one place.</p>
            <button class="cta-btn">Get Started</button>
        </div>
    </main>
</body>
</html>
"""

# Render the component
components.html(html_content, height=800, scrolling=True)