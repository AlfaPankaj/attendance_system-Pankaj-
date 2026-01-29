# To run: streamlit run app.py


import streamlit as st
import cv2
import numpy as np
import pandas as pd
from src.face_utils import register_new_user, recognize_face
from src.database import log_attendance, get_logs, init_db
from src.liveness import LivenessDetector
from src.camera import ThreadedCamera

st.set_page_config(page_title="Medoc Attendance AI", layout="wide")

init_db()

if 'liveness' not in st.session_state:
    st.session_state.liveness = LivenessDetector()

menu = ["Punch Attendance", "Register New User", "Admin Logs"]
choice = st.sidebar.selectbox("Menu", menu)

st.sidebar.markdown("---")
st.sidebar.info("Medoc Health AI Intern Assignment")

if choice == "Punch Attendance":
    st.title("Live Face Attendance")
    st.markdown("**Instructions:** Look at the camera and **blink** to verify you are human.")
    
    if 'logged_users' not in st.session_state:
        st.session_state.logged_users = set()
    
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    
    if 'current_confidence' not in st.session_state:
        st.session_state.current_confidence = 0
    
    if 'last_action' not in st.session_state:
        st.session_state.last_action = {}  
    
    if st.session_state.logged_users:
        st.success(f"**Attendance marked for:** {', '.join(st.session_state.logged_users)}")
    else:
        st.info("No attendance marked yet in this session")
    
    col_reset1, col_reset2 = st.columns([3, 1])
    with col_reset2:
        if st.button("Reset Session", type="secondary", use_container_width=True):
            st.session_state.logged_users.clear()
            st.session_state.current_user = None
            st.session_state.current_confidence = 0
            st.session_state.last_action = {}
            st.success("Session reset! All users cleared.")
            st.rerun()
    
    st.markdown("---")
    
    st.subheader("Attendance Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_mode = st.checkbox("Auto Mode (On Recognition)", value=True)
    
    with col2:
        manual_mode = st.checkbox("Manual Mode (Button Click)", value=True)
    
    if auto_mode and manual_mode:
        st.info("Both modes active: Auto-logging enabled + Manual buttons available")
    elif auto_mode:
        st.info("Auto mode only: Attendance will be marked automatically")
    elif manual_mode:
        st.info("Manual mode only: Use buttons to mark attendance")
    else:
        st.warning("Please enable at least one mode")
    
    st.markdown("---")
    
    run = st.checkbox('📷 Start Camera')
    
    status_text = st.empty()
    recognized_name_display = st.empty()
    
    if manual_mode:
        st.markdown("### Manual Controls")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            punch_in_btn = st.button("🟢 Punch In", use_container_width=True, type="primary")
        with col2:
            punch_out_btn = st.button("🔴 Punch Out", use_container_width=True, type="primary")
        with col3:
            if st.session_state.current_user:
                st.success(f"Ready: {st.session_state.current_user}")
            else:
                st.error("No user detected")
    else:
        punch_in_btn = False
        punch_out_btn = False
    
    st.markdown("---")
    
    if run:
        camera = ThreadedCamera(0)
        
        st_frame = st.empty()
        
        while run:
            frame = camera.get_frame()
            
            if frame is None:
                continue

            is_live, frame = st.session_state.liveness.check_liveness(frame)

            if is_live:
                name, confidence = recognize_face(frame)
                
                if name != "Unknown" and confidence > 0.5:  
                    st.session_state.current_user = name
                    st.session_state.current_confidence = confidence
                    
                    cv2.putText(frame, f"{name} ({int(confidence*100)}%)", (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    if name in st.session_state.last_action:
                        last_action_text = f"Last: {st.session_state.last_action[name]}"
                        cv2.putText(frame, last_action_text, (50, 90), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    
                    recognized_name_display.success(f"Recognized: **{name}** ({int(confidence*100)}%)")
                    
                    if auto_mode and name not in st.session_state.logged_users:
                        from datetime import datetime
                        hour = datetime.now().hour
                        action = "PUNCH_IN" if hour < 14 else "PUNCH_OUT"
                        
                        success, msg = log_attendance(1, name, action)
                        
                        if success:
                            st.session_state.logged_users.add(name)
                            st.session_state.last_action[name] = action
                            status_text.success(f"**Attendance Marked!** {name} - {action} at {datetime.now().strftime('%H:%M:%S')}")
                        else:
                            status_text.warning(f"{msg}")
                    
                    elif auto_mode and name in st.session_state.logged_users:
                        last_action = st.session_state.last_action.get(name, "Unknown")
                        status_text.info(f"ℹ{name} already marked as {last_action} in this session")
                        
                else:
                    st.session_state.current_user = None
                    cv2.putText(frame, "Unknown User", (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    recognized_name_display.warning("Unknown User or Low Confidence")
            else:
                cv2.putText(frame, "PLEASE BLINK TO VERIFY", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

            st_frame.image(frame, channels='BGR')

        camera.stop()

    if manual_mode:
        from datetime import datetime
        
        if punch_in_btn:
            if st.session_state.current_user:
                success, msg = log_attendance(1, st.session_state.current_user, "PUNCH_IN")
                if success:
                    st.session_state.logged_users.add(st.session_state.current_user)
                    st.session_state.last_action[st.session_state.current_user] = "PUNCH_IN"
                    status_text.success(f"**Attendance Marked!** {st.session_state.current_user} - PUNCH_IN at {datetime.now().strftime('%H:%M:%S')}")
                    st.balloons()
                else:
                    status_text.warning(f"{msg}")
            else:
                status_text.error("No user recognized. Please look at the camera and blink.")
        
        if punch_out_btn:
            if st.session_state.current_user:
                success, msg = log_attendance(1, st.session_state.current_user, "PUNCH_OUT")
                if success:
                    st.session_state.last_action[st.session_state.current_user] = "PUNCH_OUT"
                    status_text.success(f"**Attendance Marked!** {st.session_state.current_user} - PUNCH_OUT at {datetime.now().strftime('%H:%M:%S')}")
                    st.balloons()
                else:
                    status_text.warning(f"{msg}")
            else:
                status_text.error("No user recognized. Please look at the camera and blink.")

elif choice == "Register New User":
    st.title("Register New Employee")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name")
        role = st.selectbox("Role", ["Intern", "Developer", "Manager", "Doctor"])
        
    with col2:
        img_file_buffer = st.camera_input("Take a Photo")

    if st.button("Submit Registration"):
        if img_file_buffer is not None and name:
            bytes_data = img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            
            success, msg = register_new_user(cv2_img, name)
            if success:
                st.success(msg)
            else:
                st.error(msg)
        else:
            st.warning("Please enter a name and take a photo.")

elif choice == "Admin Logs":
    st.title("Attendance Logs")
    
    df = get_logs()
    
    if not df.empty:
        st.dataframe(df.style.highlight_max(axis=0))
        
        st.write(f"**Total Records:** {len(df)}")
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download CSV",
            csv,
            "attendance_report.csv",
            "text/csv",
            key='download-csv'
        )
    else:
        st.info("No attendance records found yet. Go to 'Punch Attendance' to add data.")
        
        import os
        db_path = os.path.join("data", "attendance_v.db")
        if os.path.exists(db_path):
            st.caption(f"Database file found at: {db_path} (Size: {os.path.getsize(db_path)} bytes)")
        else:
            st.error(f"Database file NOT found at: {db_path}")