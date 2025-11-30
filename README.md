# UTM System for Drones

A simple, small-scale Unmanned Traffic Management (UTM) demo project built with Flask and a lightweight web frontend showing interactive maps. It demonstrates a basic monitoring interface for drone traffic and a minimal backend to serve the application and persist data (SQLite).

--

## Table of contents

- [Features](#features)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick start](#quick-start)
- [Usage](#usage)
- [Notes](#notes)
- [Contributing](#contributing)
- [License](#license)


## Features

- Flask-based backend (app.py) for serving pages and handling minimal backend tasks
- Simple web UI showing a map, using Leaflet for map interactions
- Static assets (CSS/JS) and two HTML templates: main page and a map view
- Uses a local SQLite database (`utm.db`) for small persistent state


## Tech stack

- Python + Flask
- SQLite (local file storage)
- HTML/CSS/JavaScript + Leaflet.js (for maps)


## Project structure

```
UTM-system-for-drones/
├─ app.py                 # Main Flask application
├─ requirements.txt       # Python dependencies
├─ templates/             # HTML templates (index + map)
├─ static/                # CSS, JS and image assets
└─ utm.db                 # SQLite database (created automatically)
```


## Prerequisites

- Python 3.8+ installed
- Recommended: create a virtual environment for the project


## Quick start (PowerShell)

1. Open a PowerShell terminal in the project root
2. Create and activate a virtual environment (optional but recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Run the Flask app:

```powershell
python app.py
```

By default the app should be accessible at http://127.0.0.1:5000/ — open a browser and visit the main page or the map page.


## Usage

- `index.html` is the main landing page with any UI controls and forms
- `map.html` contains the map interface (uses Leaflet) for visualization
- `app.py` serves the templates and contains any backend endpoints
- `utm.db` will be created/updated automatically when the application runs and performs DB operations