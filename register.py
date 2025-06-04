import streamlit as st # type: ignore
import mysql.connector # type: ignore
import streamlit.components.v1 as components # type: ignore

# Database Connection
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

# Register function
def register_user(user_type, data):
    conn = create_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()

        # Check if user already exists
        if user_type == "User":
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", 
                         (data['username'], data['email']))
        else:
            cursor.execute("SELECT * FROM employers WHERE company_email = %s", 
                         (data['company_email'],))

        if cursor.fetchone():
            return False

        # Insert new user
        if user_type == "User":
            cursor.execute("""
                INSERT INTO users (first_name, last_name, username, email, password, phone, dob)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (data['first_name'], data['last_name'], data['username'], 
                  data['email'], data['password'], data['phone'], data['dob']))
        else:
            cursor.execute("""
                INSERT INTO employers (company_name, company_email, company_phone)
                VALUES (%s, %s, %s)
            """, (data['company_name'], data['company_email'], data['company_phone']))

        conn.commit()
        return True
    
    except mysql.connector.Error as err:
        st.error(f"Registration failed: {err}")
        return False
    finally:
        conn.close()

# Page Configuration
st.set_page_config(
    page_title="CareerFinder - Register", 
    page_icon="👜", 
    layout="wide"
)

# Enhanced CSS with consistent dark background (matching login page)
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

# Registration form HTML with vibrant dark theme (matching login page)
def create_registration_form():
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
            
            .register-card {
                background: rgba(45, 45, 45, 0.95);
                padding: 45px;
                border-radius: 20px;
                box-shadow: 
                    0 8px 32px rgba(0, 0, 0, 0.6),
                    0 0 0 1px rgba(255, 255, 255, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
                max-width: 580px;
                width: 100%;
                border: 1px solid rgba(79, 70, 229, 0.2);
                backdrop-filter: blur(20px);
                position: relative;
                z-index: 2;
                transition: all 0.3s ease;
            }
            
            .register-card:hover {
                transform: translateY(-5px);
                box-shadow: 
                    0 12px 40px rgba(0, 0, 0, 0.7),
                    0 0 0 1px rgba(255, 255, 255, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15);
            }
            
            .register-card h1 {
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
            
            .user-type-selector {
                display: flex;
                background: rgba(26, 26, 26, 0.8);
                border-radius: 15px;
                padding: 8px;
                margin-bottom: 25px;
                border: 2px solid rgba(79, 70, 229, 0.3);
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(10px);
            }
            
            .user-type-btn {
                flex: 1;
                padding: 16px 20px;
                background: transparent;
                border: none;
                border-radius: 10px;
                font-weight: 600;
                font-size: 1rem;
                cursor: pointer;
                transition: all 0.3s ease;
                color: #b0b0b0;
                position: relative;
                overflow: hidden;
            }
            
            .user-type-btn.active {
                background: linear-gradient(135deg, #4f46e5, #7c3aed);
                color: white;
                box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
                transform: translateY(-2px);
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            
            .user-type-btn:not(.active):hover {
                background: rgba(45, 45, 45, 0.6);
                color: #ffffff;
                transform: translateY(-1px);
            }
            
            .user-type-indicator {
                text-align: center;
                margin-bottom: 25px;
                padding: 15px;
                background: linear-gradient(135deg, rgba(79, 70, 229, 0.2), rgba(124, 58, 237, 0.2));
                border-radius: 12px;
                border: 1px solid rgba(79, 70, 229, 0.3);
                backdrop-filter: blur(10px);
            }
            
            .user-type-indicator .type-label {
                font-size: 0.9rem;
                color: #b0b0b0;
                font-weight: 600;
                margin-bottom: 5px;
            }
            
            .user-type-indicator .type-value {
                font-size: 1.2rem;
                color: #ffffff;
                font-weight: 700;
                background: linear-gradient(135deg, #ffffff, #e0e7ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
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
            
            .form-row {
                display: flex;
                gap: 20px;
            }
            
            .form-row .form-group {
                flex: 1;
            }
            
            .section-title {
                color: #ffffff;
                font-size: 1.3rem;
                font-weight: 600;
                margin: 30px 0 20px 0;
                padding-bottom: 10px;
                border-bottom: 2px solid rgba(79, 70, 229, 0.3);
                background: linear-gradient(135deg, #ffffff, #e0e7ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
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
                .register-card {
                    margin: 20px;
                    padding: 35px 25px;
                }
                
                .register-card h1 {
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
                
                .form-row {
                    flex-direction: column;
                    gap: 0;
                }
            }
        </style>
    </head>
    <body>
        <nav class="navbar">
            <div class="logo">👜 CareerFinder</div>
        </nav>
        
        <main class="main-content">
            <div class="register-card">
                <h1>Create Account</h1>
                <p class="welcome-text">Join CareerFinder and start your journey to find the perfect career path</p>
                
                <!-- User Type Selector with Visual Feedback -->
                <div class="user-type-selector">
                    <button class="user-type-btn active" onclick="selectUserType('user')" id="user-btn">
                        👤 Individual User
                    </button>
                    <button class="user-type-btn" onclick="selectUserType('employer')" id="employer-btn">
                        🏢 Employer
                    </button>
                </div>
                
                <!-- Current Selection Indicator -->
                <div class="user-type-indicator" id="user-type-indicator">
                    <div class="type-label">Registering as:</div>
                    <div class="type-value" id="selected-type">Individual User</div>
                </div>
                
                <div id="registration-form">
                    <!-- Form will be populated by Streamlit -->
                </div>
            </div>
        </main>
        
        <script>
            function selectUserType(type) {
                // Update button states
                const userBtn = document.getElementById('user-btn');
                const employerBtn = document.getElementById('employer-btn');
                const indicator = document.getElementById('selected-type');
                
                if (type === 'user') {
                    userBtn.classList.add('active');
                    employerBtn.classList.remove('active');
                    indicator.textContent = 'Individual User';
                } else {
                    employerBtn.classList.add('active');
                    userBtn.classList.remove('active');
                    indicator.textContent = 'Employer';
                }
                
                // Trigger Streamlit update (this would need to be connected to your Streamlit logic)
                console.log('Selected user type:', type);
            }
        </script>
    </body>
    </html>
    """

# Display the HTML template
components.html(create_registration_form(), height=900, scrolling=False)

# Registration Logic with dark theme styling
def registration_form():
    st.markdown("""
    <style>
        /* Ensure Streamlit components match the dark theme */
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stDateInput > div > div > input {
            border: 2px solid rgba(79, 70, 229, 0.3) !important;
            border-radius: 12px !important;
            padding: 15px 20px !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            background: rgba(26, 26, 26, 0.8) !important;
            color: #ffffff !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div:focus-within,
        .stDateInput > div > div > input:focus {
            border-color: #4f46e5 !important;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.3), 0 0 20px rgba(79, 70, 229, 0.2) !important;
            color: #ffffff !important;
            background: rgba(26, 26, 26, 0.9) !important;
            transform: translateY(-2px) !important;
        }
        
        .stTextInput > div > div > input:hover,
        .stSelectbox > div > div:hover,
        .stDateInput > div > div > input:hover {
            border-color: rgba(79, 70, 229, 0.5) !important;
            background: rgba(26, 26, 26, 0.9) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #808080 !important;
        }
        
        .stTextInput > label,
        .stSelectbox > label,
        .stDateInput > label {
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            margin-bottom: 10px !important;
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div > div {
            color: #ffffff !important;
        }
        
        .stSelectbox [data-baseweb="select"] {
            background: rgba(26, 26, 26, 0.8) !important;
            border: 2px solid rgba(79, 70, 229, 0.3) !important;
        }
        
        .stSelectbox [data-baseweb="select"]:hover {
            border-color: rgba(79, 70, 229, 0.5) !important;
        }
        
        /* Date input styling */
        .stDateInput > div > div > input {
            color: #ffffff !important;
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
        .stMarkdown p, .stMarkdown h3 {
            color: #ffffff !important;
        }
        
        /* Section titles */
        .stMarkdown h3 {
            font-size: 1.3rem !important;
            font-weight: 600 !important;
            margin: 30px 0 20px 0 !important;
            padding-bottom: 10px !important;
            border-bottom: 2px solid rgba(79, 70, 229, 0.3) !important;
            background: linear-gradient(135deg, #ffffff, #e0e7ff) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
        }
        
        /* User Type Display */
        .user-type-display {
            background: linear-gradient(135deg, rgba(79, 70, 229, 0.2), rgba(124, 58, 237, 0.2)) !important;
            border: 1px solid rgba(79, 70, 229, 0.3) !important;
            border-radius: 12px !important;
            padding: 15px !important;
            margin-bottom: 25px !important;
            text-align: center !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .user-type-display .label {
            font-size: 0.9rem !important;
            color: #b0b0b0 !important;
            font-weight: 600 !important;
            margin-bottom: 5px !important;
        }
        
        .user-type-display .value {
            font-size: 1.2rem !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            background: linear-gradient(135deg, #ffffff, #e0e7ff) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
        }
        
        .user-icon {
            font-size: 1.5rem !important;
            margin-right: 8px !important;
        }
        
        /* Form groups spacing */
        .stTextInput, .stSelectbox, .stDateInput {
            margin-bottom: 25px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Center the form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # User type selection with visual indicator
        user_type = st.selectbox("Choose Account Type:", ["Individual User", "Employer"], key="user_type")
        
        # Display current selection prominently
        if user_type == "Individual User":
            st.markdown("""
            <div class="user-type-display">
                <div class="label">You are registering as:</div>
                <div class="value"><span class="user-icon">👤</span>Individual User</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="user-type-display">
                <div class="label">You are registering as:</div>
                <div class="value"><span class="user-icon">🏢</span>Employer</div>
            </div>
            """, unsafe_allow_html=True)
        
        data = {}
        
        if user_type == "Individual User":
            st.markdown("### 👤 Personal Information")
            
            col_a, col_b = st.columns(2)
            with col_a:
                data['first_name'] = st.text_input("First Name", placeholder="Enter your first name")
            with col_b:
                data['last_name'] = st.text_input("Last Name", placeholder="Enter your last name")
            
            data['username'] = st.text_input("Username", placeholder="Choose a unique username")
            data['email'] = st.text_input("Email Address", placeholder="your.email@example.com")
            data['password'] = st.text_input("Password", type="password", placeholder="Create a strong password")
            data['phone'] = st.text_input("Phone Number", placeholder="Enter your phone number")
            data['dob'] = st.date_input("Date of Birth", help="Select your date of birth")
            
            if st.button("🚀 Create Individual Account"):
                # Validate required fields
                if all([data['first_name'], data['last_name'], data['username'], 
                       data['email'], data['password'], data['phone'], data['dob']]):
                    
                    # Convert date to string format for database
                    data['dob'] = data['dob'].strftime('%Y-%m-%d')
                    
                    if register_user("User", data):
                        st.success("🎉 Account created successfully! Welcome to CareerFinder!")
                        st.balloons()
                        st.markdown("""
                        <div style="text-align: center; margin-top: 20px;">
                            <p style="color: #4ade80; font-weight: 600;">
                                You can now login with your credentials to start exploring career opportunities!
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("❌ Registration failed. Username or email may already exist.")
                else:
                    st.error("⚠️ Please fill in all required fields.")
        
        else:  # Employer registration
            st.markdown("### 🏢 Company Information")
            
            data['company_name'] = st.text_input("Company Name", placeholder="Enter your company name")
            data['company_email'] = st.text_input("Company Email", placeholder="company@example.com")
            data['company_phone'] = st.text_input("Company Phone", placeholder="Enter company phone number")
            
            # Additional company details (optional)
            st.markdown("### 📋 Additional Details (Optional)")
            company_size = st.selectbox("Company Size", 
                                      ["Select...", "1-10 employees", "11-50 employees", 
                                       "51-200 employees", "201-1000 employees", "1000+ employees"])
            
            industry = st.selectbox("Industry", 
                                  ["Select...", "Technology", "Healthcare", "Finance", "Education", 
                                   "Manufacturing", "Retail", "Consulting", "Marketing", "Other"])
            
            company_description = st.text_area("Company Description", 
                                             placeholder="Brief description of your company (optional)",
                                             height=100)
            
            if st.button("🏢 Create Employer Account"):
                # Validate required fields
                if all([data['company_name'], data['company_email'], data['company_phone']]):
                    if register_user("Employer", data):
                        st.success("🎉 Employer account created successfully! Welcome to CareerFinder!")
                        st.balloons()
                        st.markdown("""
                        <div style="text-align: center; margin-top: 20px;">
                            <p style="color: #4ade80; font-weight: 600;">
                                You can now start posting job opportunities and finding the right candidates!
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("❌ Registration failed. Company email may already exist.")
                else:
                    st.error("⚠️ Please fill in all required company fields.")
        
        # Divider and Login Link
        st.markdown("""
        <div class="divider">
            <span>Already have an account?</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔑 Go to Login", key="login_redirect"):
            st.markdown("""
            <script>
                window.location.href = "/login";  // Adjust this to your login page URL
            </script>
            """, unsafe_allow_html=True)
            st.info("Redirecting to login page...")

# Execute the registration form
if __name__ == "__main__":
    registration_form()