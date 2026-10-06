# Global Cybersecurity Attacks Data Analytics 🛡️

An interactive web application and data analytics dashboard built with **Python**, **Streamlit**, and **Plotly** to explore, visualize, and analyze global cybersecurity attack trends and patterns.

---

## 🚀 Features

- **Interactive Dashboard:** Dynamic filtering and real-time visualization of cyber attack statistics.
- **Visual Analytics:** Built with Plotly to render responsive charts, including:
  - Target Destination Port distributions (Pie charts).
  - Services Under Pressure breakdown (Horizontal bar charts).
- **Data-Driven Insights:** Powered by a comprehensive cybersecurity telemetry dataset (`cybersecurity_attacks.csv`).
- **Clean Architecture:** Modular separation of concerns between core application logic (`app.py`) and supplementary components (`extras.py`).

---

## 📁 Project Structure

```text
DV cyber attack/
│
├── .idea/                      # PyCharm configuration files
├── venv/                       # Python virtual environment
├── app.py                      # Main Streamlit application entry point
├── extras.py                   # Helper functions and auxiliary layout components
├── cybersecurity_attacks.csv   # Primary dataset containing attack telemetry
└── README.md                   # Project documentation
```

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **Data Processing:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Data Visualization:** [Plotly](https://plotly.com/python/)
- **Language:** Python 3.12+

---

## ⚙️ Installation and Setup

Follow these steps to run the project locally on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/om-rajale/Global-Cybersecurity-Attacks-Data-Analytics.git
cd Global-Cybersecurity-Attacks-Data-Analytics
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
```
* **Activate on Windows (PowerShell):**
  ```powershell
  & "./venv/Scripts/Activate.ps1"
  ```
* **Activate on macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies
Install the required Python libraries:
```bash
pip install streamlit pandas plotly numpy
```

### 4. Run the Streamlit Application
Launch the dashboard locally:
```bash
streamlit run app.py
```

---

## 📊 Usage

Once the application launches, your default web browser will open to the local Streamlit server (typically `http://localhost:8501`). Use the interactive sidebar and filters to explore different attack vectors, port statistics, and service vulnerabilities.

---

## 👨‍💻 Author

**Om Rajale**
- GitHub: [@om-rajale](https://github.com/om-rajale)
