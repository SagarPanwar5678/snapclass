import streamlit as st
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists,create_teacher,teacher_login,get_teacher_subjects
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.subject_card import subject_card
def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if 'teacher_login_type' not in st.session_state:
        st.session_state["teacher_login_type"] = "login"

    if "teacher_data" in st.session_state:
        teacher_dashboard()
        return None
    match st.session_state["teacher_login_type"]:
        case "login":
            teacher_screen_login()
        case "register":
            teacher_screen_register()

def teacher_dashboard():
    teacher_data = st.session_state["teacher_data"]
    col1, col2 = st.columns(2,vertical_alignment='center',gap="xxlarge")
    st.subheader(f""" Welcome, {teacher_data['name']}""")
    with col1:
        header_dashboard()
    with col2:
        if st.button("Logout",type="secondary", key="loginbackbtn",shortcut="control+backspace"):
            st.session_state["is_logged_in"] = False
            del st.session_state["teacher_data"]
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"
    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state["current_teacher_tab"] == "take_attendance" else "tertiary"
        if st.button("Take Attendance",width="stretch",icon=":material/ar_on_you:",type=type1):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()
    with tab2:
        type2 = "primary" if st.session_state["current_teacher_tab"] == "manage_subjects" else "tertiary"
        if st.button("Manage Subjects",width="stretch",icon=":material/book_ribbon:",type=type2):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state["current_teacher_tab"] == "attendance_records" else "tertiary"
        if st.button("Attendance Records",width="stretch",icon=":material/cards_stack:",type=type3):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    if st.session_state["current_teacher_tab"] == "take_attendance":
        teacher_tab_take_attendance()
    elif st.session_state["current_teacher_tab"] == "manage_subjects":
        teacher_tab_manage_subjects()
    elif st.session_state["current_teacher_tab"] == "attendance_records":
        teacher_tab_attendance_records()


    footer_dashboard()

def teacher_tab_take_attendance():
    st.header("take ai attendance")

def teacher_tab_manage_subjects():
    teacher_id = st.session_state["teacher_data"]["teacher_id"]
    col1,col2 = st.columns(2)
    with col1:
        st.header("Manage subjects",width="stretch")
    with col2:
        if st.button("create new subject",width="stretch"):
            create_subject_dialog(teacher_id)


    #List all subjects
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥","Students",sub["total_students"]),
                ("🕰️","Classes",sub["total_classes"])
            ]
        def share_btn():
            if st.button(f"Share Code: {sub['name']}",key=f"share){sub["subject_code"]}",icon=":material/share:"):
                share_subject_dialog(sub["name"],sub["subject_code"])
            st.space()

        subject_card(
            name = sub["name"],
            code = sub["subject_code"],
            section = sub["section"],
            stats = stats,
            footer_callback = share_btn
        )
    else:
        st.warning("NO SUBJECTS FOUND. CREATE ONE ABOVE")


def teacher_tab_attendance_records():
    st.header("attendance records")


def login_teacher(username,password):
    if not username or not password:
        return False

    teacher = teacher_login(username,password)

    if teacher:
        st.session_state.user_role="teacher"
        st.session_state.teacher_data=teacher
        st.session_state.is_logged_in=True
        return True

    return False
def teacher_screen_login():
    col1, col2 = st.columns(2,vertical_alignment='center',gap="xxlarge")
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go back to home",type="secondary", key="loginbackbtn",shortcut="control+backspace"):
            st.session_state["login_type"] = None
            st.rerun()
    
    
    st.header("Login using password",text_alignment='center')
    st.space()

    teacher_username = st.text_input("Enter Username",placeholder='Sagar Panwar');
    st.space()
    teacher_pass = st.text_input("Enter Password",type="password",placeholder="abc@123")
    st.divider()

    btnc1,btnc2 = st.columns(2)
    with btnc1:
        if st.button("Login",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
            if login_teacher(teacher_username, teacher_pass):
                st.toast("welcome back!", icon="👋")
                # import time
                # time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username and password code")
    with btnc2:
        if st.button("Register Instead",icon=":material/passkey:",width="stretch",type="primary"):
            st.session_state["teacher_login_type"] = "register"
            st.rerun()
    footer_dashboard()



def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass or not teacher_pass_confirm:
        return False,"All Fields are required!"
    if check_teacher_exists(teacher_username):
        return False, "Username already taken"
    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match"

    try:
        create_teacher(teacher_username,teacher_pass,teacher_name)
        return True,"SuccessFully Created: Login Now"
    except Exception as e:
        print(e)
        return False,"Unexpected Error"
    


    
def teacher_screen_register():
    col1, col2 = st.columns(2,vertical_alignment='center',gap="xxlarge")
    
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go back to home",type="secondary", key="loginbackbtn",shortcut="control+backspace"):
            st.session_state["login_type"] = None
            st.rerun()
    
    st.header("Register your teacher profile")
    st.space()
    teacher_username = st.text_input("Enter Username",placeholder='Sagar Panwar');

    teacher_name = st.text_input("Enter name",placeholder='Sagar Panwar');

    teacher_pass = st.text_input("Enter Password",type="password",placeholder="abc@123")
    teacher_pass_confirm = st.text_input("confirm your Password",type="password",placeholder="abc@123")

    st.divider()

    btnc1,btnc2 = st.columns(2)
    with btnc1:
        if st.button("Register",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
            success,message = register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(1)
                st.session_state["teacher_login_type"] = "login"
                st.rerun()
            else:
                st.error(message)

    with btnc2:
        if st.button("Login Instead",icon=":material/passkey:",width="stretch",type="primary"):
            st.session_state["teacher_login_type"] = "login"
            st.rerun()
    footer_dashboard()

