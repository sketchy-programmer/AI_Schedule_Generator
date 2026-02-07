<p align="center">
  <img src="https://img.shields.io/badge/AI-Powered-blueviolet?style=for-the-badge" alt="AI Powered"/>
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Flask-2.3-green?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI"/>
  <img src="https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Heroku-Deployed-430098?style=for-the-badge&logo=heroku&logoColor=white" alt="Heroku"/>
</p>

<h1 align="center">
  <br>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Logo" width="80">
  <br>
  AI Schedule Generator
  <br>
</h1>

<h4 align="center">Transform your project documents into structured schedules with the power of AI</h4>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-deployment">Deployment</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-api-configuration">API Config</a>
</p>

---

## Overview

**AI Schedule Generator** is a web application that uses artificial intelligence to automatically generate project schedules from uploaded project documents. Simply upload your project overview (PDF, Word, or text file), and the AI will analyze it to create a comprehensive schedule with tasks, resources, dependencies, and timelines.

The generated schedule can be downloaded as a **formatted Excel spreadsheet** with multiple sheets including a visual Gantt-style timeline.

---

## ✨ Features

<table>
<tr>
<td width="50%">

### Document Processing
- 📄 **PDF** file support
- 📝 **Word** (.docx, .doc) support
- 📃 **Text** file support
- 🔍 Automatic text extraction

</td>
<td width="50%">

### AI-Powered Analysis
- 🤖 **GPT-4o-mini** integration
- 📊 Task identification
- 🔗 Dependency detection
- ⏱️ Duration estimation

</td>
</tr>
<tr>
<td width="50%">

### Schedule Generation
- 📋 Task breakdown with descriptions
- 👥 Resource allocation
- 📈 Timeline visualization
- 🎯 Predecessor relationships

</td>
<td width="50%">

### Export Options
- 📊 **Excel spreadsheet** (.xlsx)
- 📑 Multiple sheets (Tasks, Resources, Timeline, Summary)
- 🎨 Formatted with colors and borders
- 📉 Gantt-style visual timeline

</td>
</tr>
</table>

---

## 🛠 Tech Stack

<table>
<tr>
<td align="center" width="96">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="48" height="48" alt="Python" />
<br>Python
</td>
<td align="center" width="96">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/flask/flask-original.svg" width="48" height="48" alt="Flask" />
<br>Flask
</td>
<td align="center" width="96">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original.svg" width="48" height="48" alt="PostgreSQL" />
<br>PostgreSQL
</td>
<td align="center" width="96">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bootstrap/bootstrap-original.svg" width="48" height="48" alt="Bootstrap" />
<br>Bootstrap
</td>
<td align="center" width="96">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/heroku/heroku-original.svg" width="48" height="48" alt="Heroku" />
<br>Heroku
</td>
<td align="center" width="96">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original.svg" width="48" height="48" alt="Docker" />
<br>Docker
</td>
</tr>
</table>

### Backend
| Technology | Purpose |
|------------|---------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | Core programming language |
| ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) | Web framework |
| ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat&logo=sqlalchemy&logoColor=white) | ORM for database |
| ![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white) | AI/ML processing |
| ![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=flat&logo=gunicorn&logoColor=white) | WSGI HTTP Server |

### Frontend
| Technology | Purpose |
|------------|---------|
| ![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=flat&logo=bootstrap&logoColor=white) | CSS framework |
| ![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=flat&logo=jinja&logoColor=white) | Template engine |
| ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) | Markup |

### Document Processing
| Library | Purpose |
|---------|---------|
| `PyPDF2` | PDF text extraction |
| `python-docx` | Word document parsing |
| `openpyxl` | Excel file generation |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key
- PostgreSQL (for production)

### Local Development

```bash
# Clone the repository
git clone https://github.com/sketchy-programmer/AI_Schedule_Generator.git
cd AI_Schedule_Generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the application
cd project_root
python run.py
```

The app will be available at `http://localhost:5000`

---

## ☁️ Deployment

### Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create a new app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# Set environment variables
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
heroku config:set OPENAI_API_KEY=your-openai-api-key
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Open the app
heroku open
```

### Deploy with Docker

```bash
# Build the image
docker build -t ai-schedule-generator .

# Run the container
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e OPENAI_API_KEY=your-openai-key \
  -e DATABASE_URL=your-database-url \
  ai-schedule-generator
```

### Docker Compose

```bash
# Copy environment file
cp .env.example .env
# Edit .env with your values

# Run with docker-compose
docker-compose up -d
```

---

## 📖 Usage

### 1. Register/Login
Create an account or login to access the dashboard.

### 2. Upload Project Document
- Click **"New Project"** from the dashboard
- Enter a project name
- Upload your project overview document (PDF, DOCX, or TXT)
- Click **"Generate Schedule"**

### 3. View Generated Schedule
The AI will analyze your document and generate:
- **Tasks** with durations and dependencies
- **Resources** with capacity allocations
- **Timeline** with start/end days

### 4. Download Excel Spreadsheet
Click **"Download Excel Spreadsheet"** to get a formatted `.xlsx` file with:

| Sheet | Contents |
|-------|----------|
| **Tasks** | ID, Name, Description, Duration, Start/End Days, Predecessors, Resources |
| **Resources** | Resource names, capacity, assigned tasks |
| **Timeline** | Visual Gantt-style chart with colored bars |
| **Summary** | Project overview and statistics |

---

## ⚙️ API Configuration

### Required Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask secret key for sessions |
| `OPENAI_API_KEY` | Your OpenAI API key |
| `DATABASE_URL` | PostgreSQL connection string |
| `FLASK_ENV` | `development` or `production` |

### Getting an OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or login
3. Navigate to **API Keys**
4. Create a new secret key
5. Copy and save it securely

---

## 📁 Project Structure

```
AI_Schedule_Generator/
├── project_root/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── extensions.py        # Flask extensions (db, login)
│   │   ├── models/
│   │   │   ├── user.py          # User model
│   │   │   └── project.py       # Project model
│   │   ├── routes/
│   │   │   ├── auth.py          # Authentication routes
│   │   │   ├── main.py          # Main routes (dashboard)
│   │   │   └── projects.py      # Project management routes
│   │   ├── services/
│   │   │   ├── ai_processor.py  # OpenAI integration
│   │   │   ├── document_parser.py
│   │   │   └── spreadsheet_export.py
│   │   └── templates/           # Jinja2 HTML templates
│   ├── config.py                # Configuration
│   ├── wsgi.py                  # WSGI entry point
│   └── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Procfile                     # Heroku process file
├── runtime.txt                  # Python version
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ using AI
  <br>
  <a href="https://github.com/sketchy-programmer/AI_Schedule_Generator">
    <img src="https://img.shields.io/github/stars/sketchy-programmer/AI_Schedule_Generator?style=social" alt="GitHub stars">
  </a>
</p>
