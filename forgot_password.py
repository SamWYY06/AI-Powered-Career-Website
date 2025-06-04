import streamlit as st  # type: ignore
import mysql.connector  # type: ignore
import random
import string
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage

# ---------------- DB CONNECTION ---------------- #
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="career_path",
        charset="utf8"
    )

# ------------- CHECK IF EMAIL EXISTS ------------- #
def is_registered_email(email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# ---------------- OTP GENERATION ---------------- #
def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

# ---------------- SEND EMAIL ---------------- #
def send_otp_email(receiver_email, otp):
    msg = EmailMessage()
    msg['Subject'] = 'CareerFinder - Password Reset OTP'
    msg['From'] = 'donotreplytothis0001@gmail.com'  # Email that is going to send the OTP
    msg['To'] = receiver_email
    msg.set_content(f"Your OTP code is: {otp}\n\nThis code will expire in 5 minutes.")

    # Gmail SMTP (Requires App Password)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('donotreplytothis0001@gmail.com', 'careerfinder2025')  # 🔁 CHANGE THIS
        smtp.send_message(msg)

# ---------------- STORE OTP ---------------- #
def store_otp(email, otp):
    conn = create_connection()
    cursor = conn.cursor()
    expiry = datetime.now() + timedelta(minutes=5)
    cursor.execute("INSERT INTO password_reset_otps (email, otp, expires_at) VALUES (%s, %s, %s)", (email, otp, expiry))
    conn.commit()
    conn.close()

# ---------------- VERIFY OTP ---------------- #
def verify_otp(email, entered_otp):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM password_reset_otps 
        WHERE email = %s AND otp = %s AND expires_at >= NOW()
    """, (email, entered_otp))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# ---------------- STREAMLIT UI ---------------- #
st.set_page_config(page_title="Forgot Password", layout="centered")
st.title("🔐 Forgot Password")

# Track steps
if "step" not in st.session_state:
    st.session_state.step = 1

# Step 1: Enter registered email
if st.session_state.step == 1:
    email = st.text_input("Enter your registered email")

    if st.button("Send OTP"):
        if is_registered_email(email):
            otp = generate_otp()
            store_otp(email, otp)
            try:
                send_otp_email(email, otp)
                st.session_state.email = email
                st.session_state.step = 2
                st.success("✅ OTP sent to your email.")
            except Exception as e:
                st.error(f"Failed to send OTP. Error: {e}")
        else:
            st.error("❌ This email is not registered.")

# Step 2: Verify OTP
elif st.session_state.step == 2:
    st.write(f"OTP has been sent to: **{st.session_state.email}**")
    entered_otp = st.text_input("Enter the OTP you received")

    if st.button("Verify OTP"):
        if verify_otp(st.session_state.email, entered_otp):
            st.success("✅ OTP Verified!")
            st.session_state.step = 3
        else:
            st.error("❌ Invalid or expired OTP.")

# Step 3: Reset password
elif st.session_state.step == 3:
    new_password = st.text_input("Enter new password", type="password")
    confirm_password = st.text_input("Confirm new password", type="password")

    if st.button("Reset Password"):
        if new_password != confirm_password:
            st.error("❌ Passwords do not match.")
        else:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password = %s WHERE email = %s", (new_password, st.session_state.email))
            conn.commit()
            conn.close()
            st.success("✅ Password has been reset! You can now log in.")
            st.session_state.step = 1  # Reset steps
