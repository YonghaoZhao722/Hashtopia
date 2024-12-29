# Vue3 + Flask Project

---

## Installation and Usage

### Backend

1. **Create a virtual environment and install dependencies**
   
   ```bash
   cd flask_backend
   python -m venv venv
   source venv/bin/activate  # On Windows, run venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Initialize the database**
   
   ```bash
   python init_db.py
   ```

3. **Start the backend service**
   
   ```bash
   python run.py
   ```
   
   The service will run at `http://127.0.0.1:8000` by default.

### Frontend

1. **Install dependencies**
   
   ```bash
   cd hashtopia_frontend
   npm install
   ```

2. **Start the frontend service**
   
   ```bash
   npm run dev
   ```
   
   The service will run at `http://localhost:5173` by default.

---

## Usage

1. Start the backend service.
2. Start the frontend service.
3. Open a browser and navigate to `http://localhost:5173`
