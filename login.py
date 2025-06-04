import streamlit as st # type: ignore
import mysql.connector # type: ignore
import streamlit.components.v1 as components # type: ignore

# DB Connection
def create_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="career_path",
            charset="utf8"
        )
    except mysql.connector.Error as err:
        st.error(f"Database connection failed: {err}")
        return None

# Authentication
def authenticate_user(username, password):
    conn = create_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as err:
        st.error(f"Authentication failed: {err}")
        return None
    finally:
        conn.close()

# Page Configuration
st.set_page_config(
    page_title="CareerFinder - Login", 
    page_icon="👜", 
    layout="wide"
)

# Enhanced CSS with consistent dark background
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
    
    /* Target the main content area */
    section[data-testid="stSidebar"] {
        background-color: #0f0f0f !important;
    }
    
    /* Remove any remaining top margins/padding */
    .css-1d391kg, .css-12oz5g7, .css-z5fcl4, .css-1y4p8pa {
        padding-top: 0 !important;
        margin-top: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        background-color: #0f0f0f !important;
    }
    
    /* Force remove any iframe padding */
    iframe {
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        background-color: #0f0f0f !important;
    }
    
    /* Remove any default body margins */
    html, body {
        margin: 0 !important;
        padding: 0 !important;
        background-color: #0f0f0f !important;
    }
    
    /* Target Streamlit's root container */
    .stApp > div:first-child {
        padding-top: 0 !important;
        margin-top: 0 !important;
        background-color: #0f0f0f !important;
    }
    
    /* Ensure all containers have dark background */
    div[data-testid="stVerticalBlock"] {
        background-color: #0f0f0f !important;
    }
    
    div[data-testid="column"] {
        background-color: #0f0f0f !important;
    }
</style>
""", unsafe_allow_html=True)

# Login form HTML with consistent dark background
def create_login_form():
    return """
    <!DOCTYPE html>
    <html style="margin: 0; padding: 0; background: #0f0f0f;">
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
            }
            
            body {
                background: #0f0f0f !important;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                margin: 0;
                padding: 0;
            }
            
            .navbar {
                background: linear-gradient(135deg, #4f46e5, #7c3aed);
                padding: 18px 30px;
                box-shadow: 0 4px 20px rgba(79, 70, 229, 0.3);
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                width: 100%;
                z-index: 1000;
                margin: 0;
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
            
            .main-content {
                flex: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 40px 20px;
                background: #0f0f0f !important;
                min-height: calc(100vh - 76px);
                margin-top: 76px;
                position: relative;
            }
            
            /* Add subtle animated background pattern */
            .main-content::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: 
                    radial-gradient(circle at 20% 80%, rgba(79, 70, 229, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(124, 58, 237, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 40% 40%, rgba(79, 70, 229, 0.05) 0%, transparent 50%);
                z-index: 1;
            }
            
            .login-card {
                background: rgba(45, 45, 45, 0.95);
                padding: 45px;
                border-radius: 20px;
                box-shadow: 
                    0 8px 32px rgba(0, 0, 0, 0.6),
                    0 0 0 1px rgba(255, 255, 255, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
                max-width: 480px;
                width: 100%;
                border: 1px solid rgba(79, 70, 229, 0.2);
                backdrop-filter: blur(20px);
                position: relative;
                z-index: 2;
                transition: all 0.3s ease;
            }
            
            .login-card:hover {
                transform: translateY(-5px);
                box-shadow: 
                    0 12px 40px rgba(0, 0, 0, 0.7),
                    0 0 0 1px rgba(255, 255, 255, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15);
            }
            
            .login-card h1 {
                text-align: center;
                font-size: 2.5rem;
                color: #ffffff;
                margin-bottom: 15px;
                font-weight: 700;
                background: linear-gradient(135deg, #ffffff, #e0e7ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            
            .welcome-text {
                text-align: center;
                color: #b0b0b0;
                font-size: 1.1rem;
                margin-bottom: 35px;
                font-weight: 500;
                line-height: 1.5;
            }
            
            .form-group {
                margin-bottom: 25px;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 10px;
                font-weight: 600;
                color: #ffffff;
                font-size: 1rem;
            }
            
            .form-control {
                width: 100%;
                padding: 15px 20px;
                border: 2px solid rgba(79, 70, 229, 0.3);
                border-radius: 12px;
                font-size: 1rem;
                transition: all 0.3s ease;
                background: rgba(26, 26, 26, 0.8);
                color: #ffffff;
                backdrop-filter: blur(10px);
            }
            
            .form-control:focus {
                outline: none;
                border-color: #4f46e5;
                box-shadow: 
                    0 0 0 3px rgba(79, 70, 229, 0.3),
                    0 0 20px rgba(79, 70, 229, 0.2);
                color: #ffffff;
                background: rgba(26, 26, 26, 0.9);
                transform: translateY(-2px);
            }
            
            .form-control:hover {
                border-color: rgba(79, 70, 229, 0.5);
                background: rgba(26, 26, 26, 0.9);
            }
            
            .form-control::placeholder {
                color: #808080;
            }
            
            .btn {
                width: 100%;
                background: linear-gradient(135deg, #4f46e5, #7c3aed);
                color: white;
                padding: 16px;
                font-size: 1.1rem;
                font-weight: 600;
                border: none;
                border-radius: 12px;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-top: 15px;
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
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(79, 70, 229, 0.6);
                background: linear-gradient(135deg, #5b52f0, #8b47ed);
            }
            
            .btn-secondary {
                background: rgba(45, 45, 45, 0.8);
                color: #4f46e5;
                border: 2px solid #4f46e5;
                margin-top: 20px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            }
            
            .btn-secondary:hover {
                background: #4f46e5;
                color: white;
                border-color: #4f46e5;
            }
            
            .error-message {
                background: rgba(76, 29, 29, 0.9);
                color: #f87171;
                padding: 15px;
                border-radius: 10px;
                margin: 15px 0;
                border-left: 4px solid #dc2626;
                text-align: center;
                backdrop-filter: blur(10px);
            }
            
            .success-message {
                background: rgba(26, 58, 26, 0.9);
                color: #4ade80;
                padding: 15px;
                border-radius: 10px;
                margin: 15px 0;
                border-left: 4px solid #16a34a;
                text-align: center;
                backdrop-filter: blur(10px);
            }
            
            .divider {
                text-align: center;
                margin: 30px 0;
                position: relative;
                color: #808080;
                font-weight: 500;
            }
            
            .divider::before {
                content: '';
                position: absolute;
                top: 50%;
                left: 0;
                right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, #404040, transparent);
                z-index: 1;
            }
            
            .divider span {
                background: #2d2d2d;
                padding: 0 20px;
                position: relative;
                z-index: 2;
            }
            
            @media (max-width: 768px) {
                .login-card {
                    margin: 20px;
                    padding: 35px 25px;
                }
                
                .login-card h1 {
                    font-size: 2rem;
                }
                
                .main-content {
                    padding: 20px 10px;
                }
                
                .navbar {
                    padding: 15px 20px;
                }
                
                .logo {
                    font-size: 1.8rem;
                }
            }
        </style>
    </head>
    <body>
        <nav class="navbar">
            <div class="logo">👜 CareerFinder</div>
        </nav>
        
        <main class="main-content">
            <div class="login-card">
                <h1>Welcome Back</h1>
                <p class="welcome-text">Sign in to your CareerFinder account and continue your career journey</p>
                
                <div id="login-form">
                    <!-- Form will be populated by Streamlit -->
                </div>
            </div>
        </main>
    </body>
    </html>
    """

# Display the HTML template with full height and no scrolling
components.html(create_login_form(), height=800, scrolling=False)

# Login Logic
def login_form():
    st.markdown("""
    <style>
        /* Ensure Streamlit components match the dark theme */
        .stTextInput > div > div > input {
            border: 2px solid rgba(79, 70, 229, 0.3) !important;
            border-radius: 12px !important;
            padding: 15px 20px !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            background: rgba(26, 26, 26, 0.8) !important;
            color: #ffffff !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #4f46e5 !important;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.3), 0 0 20px rgba(79, 70, 229, 0.2) !important;
            color: #ffffff !important;
            background: rgba(26, 26, 26, 0.9) !important;
            transform: translateY(-2px) !important;
        }
        
        .stTextInput > div > div > input:hover {
            border-color: rgba(79, 70, 229, 0.5) !important;
            background: rgba(26, 26, 26, 0.9) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #808080 !important;
        }
        
        .stTextInput > label {
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            margin-bottom: 10px !important;
        }
        
        .stButton > button {
            width: 100% !important;
            background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
            color: white !important;
            padding: 16px !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 12px !important;
            margin-top: 15px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(79, 70, 229, 0.6) !important;
            background: linear-gradient(135deg, #5b52f0, #8b47ed) !important;
        }
        
        /* Secondary button styling */
        .stButton > button[data-testid="baseButton-secondary"] {
            background: rgba(45, 45, 45, 0.8) !important;
            color: #4f46e5 !important;
            border: 2px solid #4f46e5 !important;
            margin-top: 20px !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
        }
        
        .stButton > button[data-testid="baseButton-secondary"]:hover {
            background: #4f46e5 !important;
            color: white !important;
            border-color: #4f46e5 !important;
        }
        
        /* Enhanced error/success messages */
        .stSuccess {
            background: rgba(26, 58, 26, 0.9) !important;
            color: #4ade80 !important;
            border-left: 4px solid #16a34a !important;
            border-radius: 10px !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .stError {
            background: rgba(76, 29, 29, 0.9) !important;
            color: #f87171 !important;
            border-left: 4px solid #dc2626 !important;
            border-radius: 10px !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* Ensure all text is visible on dark background */
        .stMarkdown p {
            color: #ffffff !important;
        }
        
        /* Form groups spacing */
        .stTextInput {
            margin-bottom: 25px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Center the form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Login form inputs
        username = st.text_input("Username", key="username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", key="password", placeholder="Enter your password")
        
        # Login button
        if st.button("Sign In", key="login_btn"):
            if not username or not password:
                st.error("❌ Please fill in both username and password.")
            else:
                user = authenticate_user(username, password)
                if user:
                    st.success(f"✅ Welcome back, {username}!")
                    st.balloons()
                    # Here you can add logic to redirect to the main app
                    # st.session_state["logged_in"] = True
                    # st.session_state["user"] = user
                else:
                    st.error("❌ Invalid username or password. Please try again.")
        
        # Divider
        st.markdown("""
        <div style="text-align: center; margin: 30px 0; position: relative; color: #808080; font-weight: 500;">
            <div style="position: absolute; top: 50%; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, #404040, transparent); z-index: 1;"></div>
            <span style="background: #0f0f0f; padding: 0 20px; position: relative; z-index: 2;">or</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Register redirect button
        if st.button("Don't have an account? Sign Up", key="register_redirect"):
            if 'page' not in st.session_state:
                st.session_state['page'] = 'register'
            try:
                st.switch_page("register.py")
            except:
                st.info("Please create a register.py file or update the navigation logic.")

# Run the login form
login_form()