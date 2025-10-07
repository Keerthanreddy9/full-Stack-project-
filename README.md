# Travel Bucket List & Tracker
### Full Stack Web Development Project

---

## 📋 Project Overview

**Travel Bucket List & Tracker** is a comprehensive full-stack web application designed to help users plan, organize, and track their travel destinations. The application provides an intuitive interface for managing travel goals with features including destination categorization, priority management, visit tracking, and visual statistics.

This project demonstrates proficiency in:
- Backend development with Flask framework
- Database design and management with SQLite
- Frontend development with HTML5, CSS3, and JavaScript
- RESTful API design
- Responsive UI/UX design with Bootstrap 5
- AJAX and asynchronous operations
- Data visualization with Chart.js

---

## ✨ Key Features

### Core Functionality
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality for travel destinations
- **Visit Tracking**: Mark destinations as visited with automatic date stamping
- **Advanced Filtering**: Filter destinations by continent, category, and visit status
- **Live Search**: Real-time client-side search by place name or country
- **Priority Management**: Categorize destinations by High, Medium, or Low priority
- **Sorting**: Sort destinations by priority level or date added

### Enhanced Features
- **Statistics Dashboard**: Visual analytics with pie charts and bar graphs showing:
  - Visited vs Not Visited destinations
  - Distribution of places by continent
  - Completion progress bar
- **Visited Timeline**: Chronological view of all visited destinations
- **CSV Export**: Export complete destination list for external use
- **Random Destination**: Get random destination suggestions from your bucket list
- **Responsive Design**: Mobile-friendly interface that works on all devices

---

## 🛠️ Technology Stack

### Backend
- **Flask 3.0+**: Python web framework for routing and server-side logic
- **SQLite3**: Lightweight relational database for data persistence
- **Jinja2**: Template engine for dynamic HTML rendering

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Custom styling with CSS variables and animations
- **Bootstrap 5.3**: Responsive UI framework
- **JavaScript (ES6+)**: Client-side interactivity
- **jQuery 3.7**: DOM manipulation and AJAX requests
- **Chart.js 4.4**: Data visualization library

---

## 📁 Project Structure

```
Full Stack Project/
│
├── app.py                      # Main Flask application with routes and database logic
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
│
├── templates/                 # Jinja2 HTML templates
│   ├── base.html             # Base template with navbar and layout
│   ├── home.html             # Landing page with statistics
│   ├── add_place.html        # Form to add new destinations
│   ├── places.html           # List view with filters and actions
│   ├── edit_place.html       # Form to edit existing destinations
│   ├── stats.html            # Statistics dashboard with charts
│   └── timeline.html         # Chronological visited destinations
│
└── static/                    # Static assets
    ├── css/
    │   └── style.css         # Custom CSS with travel theme
    └── js/
        └── main.js           # Client-side JavaScript logic
```

---

## 💾 Database Schema

### Table: `places`

| Column       | Type    | Constraints           | Description                          |
|-------------|---------|----------------------|--------------------------------------|
| id          | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier                    |
| name        | TEXT    | NOT NULL             | Destination name                     |
| country     | TEXT    | NOT NULL             | Country name                         |
| continent   | TEXT    | NOT NULL             | Continent (Asia, Europe, etc.)       |
| category    | TEXT    | NOT NULL             | Type (Beach, Mountain, City, etc.)   |
| description | TEXT    | NOT NULL             | Brief description of the place       |
| priority    | TEXT    | NOT NULL             | Priority level (High, Medium, Low)   |
| visited     | INTEGER | NOT NULL, DEFAULT 0  | Visit status (0 = No, 1 = Yes)       |
| visited_date| TEXT    | NULLABLE             | Date of visit (ISO format)           |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Keerthanreddy9/full-Stack-project-.git
   cd full-Stack-project-
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your web browser
   - Navigate to: `http://127.0.0.1:5000/`
   - The SQLite database will be created automatically on first run

---

## 📡 API Endpoints

| Method | Endpoint              | Description                          |
|--------|----------------------|--------------------------------------|
| GET    | `/`                  | Home page with quick statistics      |
| GET    | `/add`               | Display add destination form         |
| POST   | `/add`               | Submit new destination               |
| GET    | `/places`            | View all destinations with filters   |
| GET    | `/edit/<id>`         | Display edit form for destination    |
| POST   | `/edit/<id>`         | Update destination details           |
| POST   | `/delete/<id>`       | Delete a destination                 |
| POST   | `/toggle_visited/<id>`| Toggle visit status (AJAX)          |
| GET    | `/api/stats`         | JSON API for statistics data         |
| GET    | `/stats`             | Statistics dashboard page            |
| GET    | `/timeline`          | Visited destinations timeline        |
| GET    | `/export.csv`        | Export destinations as CSV           |
| GET    | `/random`            | Get random destination suggestion    |

---

## 🎨 Design Features

### Color Palette
- **Primary**: Turquoise (#06b6d4) - Navigation and primary actions
- **Secondary**: Teal (#14b8a6) - Accents and progress indicators
- **Accent**: Coral/Orange (#f97316) - Highlights and warnings
- **Success**: Emerald (#10b981) - Visited status and confirmations
- **Background**: Light Teal (#f0fdfa) - Clean, modern feel

### UI/UX Highlights
- Clean, modern interface with card-based layouts
- Smooth animations and transitions
- Responsive design for mobile, tablet, and desktop
- Intuitive navigation with clear call-to-action buttons
- Form validation with helpful error messages
- Confirmation modals for destructive actions

---

## 🔒 Security Considerations

- CSRF protection via Flask's secret key
- SQL injection prevention using parameterized queries
- Client-side and server-side form validation
- Environment variable support for sensitive configuration

---

## 🚢 Deployment

The application is deployment-ready for platforms like Render, Heroku, or PythonAnywhere.

### For Heroku/Render:
1. Add `gunicorn` to `requirements.txt`
2. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```
3. Set environment variable: `SECRET_KEY`

---

## 📝 Future Enhancements

- User authentication and multi-user support
- Image upload for destinations
- Map integration (Google Maps API)
- Social sharing features
- Trip planning with itineraries
- Budget tracking per destination
- Weather information integration

---

## 👨‍💻 Author

**Keerthan Reddy**  
GitHub: [@Keerthanreddy9](https://github.com/Keerthanreddy9)

---

## 📄 License

This project is submitted as an academic assignment for educational purposes.

---

## 🙏 Acknowledgments

- Flask documentation and community
- Bootstrap team for the excellent CSS framework
- Chart.js for data visualization capabilities
- Stack Overflow community for troubleshooting support

---

**Project Submission Date**: October 2025  
**Course**: Full Stack Web Development
