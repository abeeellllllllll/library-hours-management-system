import streamlit as st
import oracledb
import pandas as pd


# DATABASE CONNECTION (THIN MODE)

def get_connection():
    return oracledb.connect(
        user="system",
        password="1404",
        dsn="localhost:1521/XEPDB1"
    )


# PAGE SETUP

st.set_page_config(page_title="Library Hour Management System")
st.title("📚 Library Hour Management System")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Add Student",
        "Add Staff",
        "Delete Student",
        "Assign Library Hours",
        "Log Library Usage",
        "Student Dashboard"
    ]
)


# ADD STUDENT

if menu == "Add Student":

    st.subheader("Add Student")

    student_id = st.number_input("Student ID", step=1)
    name = st.text_input("Name")
    email = st.text_input("Email")
    department = st.text_input("Department")

    if st.button("Add"):

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO student (student_id, name, email, department)
                VALUES (:1, :2, :3, :4)
            """, (int(student_id), name, email, department))

            conn.commit()
            st.success("Student added")

        except Exception as e:
            conn.rollback()
            st.error(e)

        finally:
            cursor.close()


# ADD STAFF

elif menu == "Add Staff":

    st.subheader("Add Staff / Teacher")

    staff_id = st.number_input("Staff ID", step=1)
    name = st.text_input("Staff Name")
    role = st.text_input("Role")

    if st.button("Add Staff"):

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO staff (staff_id, name, role)
                VALUES (:1, :2, :3)
            """, (int(staff_id), name, role))

            conn.commit()
            st.success("Staff added")

        except Exception as e:
            conn.rollback()
            st.error(e)

        finally:
            cursor.close()



# DELETE STUDENT

elif menu == "Delete Student":

    st.subheader("Delete Student")

    student_id = st.number_input("Student ID", step=1)

    if st.button("Delete"):

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                DELETE FROM student
                WHERE student_id = :1
            """, (int(student_id),))

            conn.commit()

        except Exception as e:
            conn.rollback()
            st.error(e)

        finally:
            cursor.close()



# ASSIGN LIBRARY HOURS

elif menu == "Assign Library Hours":

    st.subheader("Assign Library Hours")

    assignment_id = st.number_input("Assignment ID", step=1)
    student_id = st.number_input("Student ID", step=1)
    staff_id = st.number_input("Staff ID", step=1)
    library_id = st.number_input("Library ID", step=1)
    assigned_hours = st.number_input("Assigned Hours", step=1)
    deadline_days = st.number_input("Deadline (days from now)", step=1)

    if st.button("Assign"):

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO library_hours
                (assignment_id, student_id, staff_id, library_id,
                 assigned_hours, deadline_datetime, status)
                VALUES (:1, :2, :3, :4, :5,
                        SYSDATE + :6,
                        'ACTIVE')
            """, (
                int(assignment_id),
                int(student_id),
                int(staff_id),
                int(library_id),
                int(assigned_hours),
                int(deadline_days)
            ))

            conn.commit()
            st.success("Library hours assigned")

        except Exception as e:
            conn.rollback()
            st.error(e)

        finally:
            cursor.close()


# LOG LIBRARY USAGE

elif menu == "Log Library Usage":

    st.subheader("Log Library Usage")

    log_id = st.number_input("Log ID", step=1)
    assignment_id = st.number_input("Assignment ID", step=1)
    hours_used = st.number_input("Hours Used", step=1)

    if st.button("Log"):

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO library_usage
                (log_id, assignment_id, start_time, end_time, hours_used)
                VALUES (:1, :2, SYSDATE - 1/24, SYSDATE, :3)
            """, (
                int(log_id),
                int(assignment_id),
                int(hours_used)
            ))

            conn.commit()
            st.success("Usage logged")

        except Exception as e:
            conn.rollback()
            st.error(e)

        finally:
            cursor.close()


# STUDENT DASHBOARD

elif menu == "Student Dashboard":

    st.subheader("Student Progress Dashboard")

    student_id = st.number_input("Enter Student ID", step=1)

    if st.button("View"):

        conn = get_connection()
        cursor = conn.cursor()

        try:
            query = """
                SELECT 
                lh.assignment_id,
                lh.assigned_hours,
                NVL(SUM(lu.hours_used), 0) AS hours_completed,
                lh.assigned_hours - NVL(SUM(lu.hours_used), 0) AS hours_remaining,
                lh.assigned_datetime,
                lh.deadline_datetime
        FROM library_hours lh
        LEFT JOIN library_usage lu
                ON lh.assignment_id = lu.assignment_id
        WHERE lh.student_id = :student_id
        GROUP BY 
                lh.assignment_id, 
                lh.assigned_hours,
                lh.assigned_datetime,
                lh.deadline_datetime
"""

            cursor.execute(query, {"student_id": int(student_id)})
            rows = cursor.fetchall()

            if rows:
               df = pd.DataFrame(rows, columns=[
                "ASSIGNMENT_ID",
                "ASSIGNED_HOURS",
                "HOURS_COMPLETED",
                "HOURS_REMAINING",
                "ASSIGNED_DATETIME",
                "DEADLINE_DATETIME"])
               st.dataframe(df)
            else:
                st.warning("No assignments found")   
        except Exception as e:
            st.error(e)

        finally:
            cursor.close()