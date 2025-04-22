# Flask Project Setup Guide

## Prerequisites
Before you start, ensure you have the following installed:
- **Python (>= 3.x)**: Download and install from [python.org](https://www.python.org/downloads/)
- **pip** (Python package manager) (included with Python 3)
- **Virtual Environment** (recommended for dependency management)

## Installation Steps

### 1. Install Python
Download and install Python from [python.org](https://www.python.org/downloads/).  
Verify the installation by running:
```bash
python --version
```

### 2. create a virtual environment
```bash
cd backend
python -m venv venv
```

### 3. Activate the virtual environment
- **Windows**:
```bash
venv\Scripts\activate
```
- **Linux/Mac**:
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Migrate the database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
### 6. Run the application
```bash
python app.py
```
