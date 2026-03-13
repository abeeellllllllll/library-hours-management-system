# Library Hour Attendance Management System

## Overview

The **Library Hour Attendance Management System** is a web-based application designed to manage and monitor student library hour requirements. The system allows staff to assign mandatory library hours to students and track their usage through recorded entry and exit times.

The application is built using **Python Streamlit** for the frontend interface and **Oracle SQL** for backend data storage and management.

---

## Features

* Assign library hours to students
* Track student library usage through start and end timestamps
* Monitor completion status of assigned hours
* Store and manage data using an Oracle relational database
* Simple and interactive web interface using Streamlit

---

## Technologies Used

* **Python**
* **Streamlit**
* **Oracle SQL**
* **cx_Oracle** (database connectivity)
* **ER Modeling for database design**

---

## Database Design

The database consists of five main entities that manage student assignments and library usage tracking.

### Library

Stores information about libraries where students can complete their assigned hours.

| Field        | Description                 |
| ------------ | --------------------------- |
| library_id   | Primary key for the library |
| library_name | Name of the library         |

---

### Student

Stores details of students assigned library hours.

| Field      | Description                         |
| ---------- | ----------------------------------- |
| student_id | Primary key identifying the student |
| name       | Student name                        |
| email      | Student email                       |
| department | Student department                  |

---

### Staff

Stores information about staff members responsible for assigning library hours.

| Field    | Description                   |
| -------- | ----------------------------- |
| staff_id | Primary key identifying staff |
| name     | Staff member name             |
| role     | Staff role                    |

---

### Library_Hours

Tracks the assignment of required library hours to students.

| Field             | Description                |
| ----------------- | -------------------------- |
| assignment_id     | Primary key                |
| student_id        | References student         |
| staff_id          | References staff member    |
| library_id        | References library         |
| assigned_hours    | Number of hours assigned   |
| assigned_datetime | Assignment timestamp       |
| deadline_datetime | Deadline to complete hours |
| status            | Completion status          |

---

### Library_Usage

Tracks the actual usage of the library by students.

| Field         | Description                       |
| ------------- | --------------------------------- |
| log_id        | Primary key                       |
| assignment_id | References assigned library hours |
| start_time    | Time student entered the library  |
| end_time      | Time student left the library     |
| hours_used    | Total hours spent                 |

---

## ER Diagram

The database schema and entity relationships are shown below.

![ER Diagram](diagram/er_diagram.png)

---

## Project Structure

```
library-attendance-system
│
├── app.py
├── test_connection.py
├── schema.sql
├── requirements.txt
├── README.md
│
└── diagrams
    └── er_diagram.png
```

---

## How to Run the Project

### 1. Install Dependencies

```
pip install -r requirements.txt
```

### 2. Configure Database Connection

Update the Oracle database credentials in:

```
test_connection.py
```

---

### 3. Run the Streamlit Application

```
streamlit run app.py
```

The application will start locally and open in your browser.

---

## Security Considerations

Database credentials should not be committed to public repositories. It is recommended to use environment variables or configuration files that are excluded using `.gitignore`.

---

## Future Improvements

* Role-based authentication for staff and administrators
* Dashboard analytics for monitoring student usage
* Automated notifications for incomplete library hours
* Integration with institutional authentication systems
