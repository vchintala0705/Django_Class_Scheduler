# Murray State Schedule - Django Web Application

## Overview
This is a **Django-based web application** that helps students and teachers view and manage their class schedules. The project is built using **Django 3.2.23** and follows an MVC (Model-View-Controller) architecture.

## Project Members
- **Vaishnavi Chintala**  
- **Praharsha Maryala**  

## Features
✅ **Student & Teacher Schedule Views** - View class schedules based on roles  
✅ **Course Filtering** - Search for classes using **CRN, Subject, Instructor, etc.**  
✅ **Bootstrap UI** - Responsive design using Bootstrap  
✅ **Django Admin Panel** - Admin can manage classes and users  

## Project Structure
```plaintext
├── harsha_project_1/               # Django Project Root
│   ├── settings.py                  # Main Django settings
│   ├── urls.py                       # URL Routing
│   ├── asgi.py                        # ASGI Server Configuration
│   ├── wsgi.py                        # WSGI Server Configuration
│   ├── db.sqlite3                     # SQLite Database
│   ├── manage.py                      # Django Management Script
│   ├── templates/                      # HTML Templates
│   │   ├── index.html                  # Homepage
│   │   ├── navbar.html                 # Navigation Bar
│   │   ├── student_schedule.html       # Student Schedule Page
│   │   ├── teacher_schedule.html       # Teacher Schedule Page
│   │   ├── view_content.html           # Course Filtering Page
│   ├── option_1/                        # Django App
│       ├── views.py                     # Business Logic & Rendering
│       ├── models.py                    # Database Models
│       ├── admin.py                     # Admin Panel Configuration
│       ├── apps.py                      # Django App Config
│       ├── tests.py                     # Unit Tests
```

## Installation & Setup
### **1. Clone the Repository**
```sh
git clone https://github.com/your-username/Murray_State_Schedule.git
cd Murray_State_Schedule
```

### **2. Create a Virtual Environment & Install Dependencies**
```sh
python -m venv env
source env/bin/activate  # On Windows: env\Scriptsctivate
pip install -r requirements.txt
```

### **3. Run the Django Application**
```sh
python manage.py migrate
python manage.py runserver
```

Now, open **http://127.0.0.1:8000/** in your browser.

## Usage
- **Home Page (`index.html`)** - Displays options for students & teachers.
- **Filter Courses (`view_content.html`)** - Search for courses by CRN, Subject, or Instructor.
- **Student Schedule (`student_schedule.html`)** - View student class schedules.
- **Teacher Schedule (`teacher_schedule.html`)** - View teacher class schedules.

## Database Configuration
- The project **uses SQLite** (`db.sqlite3`). If needed, you can switch to **PostgreSQL or MySQL** in `settings.py`.
- To reset the database:
  ```sh
  python manage.py flush  # Clears all data
  ```

## Contributors
- **Vaishnavi Chintala**
- **Praharsha Maryala**

## License

Copyright (c) 2024 Vaishnavi Chintala & Praharsha Maryala

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

