# Hawaii Health Risk Assessment System

The Hawaii Health Risk Assessment System is a Flask-based web application designed to evaluate health risks based on user input. Using a generative AI model (Google Gemini), it provides health insights and allows users to book medical appointments. It also features an admin panel for visualizing user data and appointment statistics.

## Features
- **Health Risk Assessment**: Evaluates health risk based on personal information, lifestyle, medical history, symptoms, and health metrics.
- **Generative AI Insights**: Utilizes Google Gemini to analyze and generate personalized health insights.
- **Appointment Booking**: Users can schedule appointments with doctors.
- **Admin Panel**: View user data, appointments, and visualized charts of risk status and doctor appointments.

---

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- pip (Python package manager)

### Clone the Repository
```bash
$ git clone https://github.com/mmfarabi/Hawaii-Health-Risk-Assessment-System.git
$ cd hawaii-health-risk-system
```

### Set Up Environment
1. Install required dependencies:
   ```bash
   $ pip install -r requirements.txt
   ```
2. Create a `.env` file in the project root and add your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

### Initialize the Database
Run the following command to create the SQLite database:
```bash
$ python -c "from app import create_db; create_db()"
```

---

## Usage

### Running the Application
Start the Flask development server:
```bash
$ python app.py
```

By default, the application will run at `http://127.0.0.1:5000/`.

### Access the Application
1. **Home Page** (`/`): Fill in the health questionnaire and receive personalized health insights.
2. **Results Page** (`/result`): View your health risk status and insights.
3. **Appointment Booking** (`/appointment`): Schedule a medical appointment.
4. **Admin Panel** (`/admin`): Access admin-only dashboards and data visualizations (requires developer access).

---

## Folder Structure
```
|-- app.py                  # Main Flask application
|-- templates/              # HTML templates
|   |-- index.html          # User input form
|   |-- result.html         # Display health insights
|   |-- appointment.html    # Appointment booking form
|   |-- admin.html          # Admin dashboard
|-- static/                 # Static assets (CSS, JS, images)
|-- requirements.txt        # Python dependencies
|-- README.md               # Project documentation
|-- .env                    # Environment variables (not committed)
|-- health_risk_data.db     # SQLite database (auto-created)
```

---

## API Integration
This application integrates the [Google Gemini API](https://developers.google.com/) for generating health insights. Ensure the API key is configured correctly in your `.env` file.

---

## Admin Panel Features
1. **User Data**: View detailed user-submitted health data.
2. **Appointment Data**: Track booked appointments.
3. **Charts**:
   - **Risk Status Distribution**: Pie chart of users categorized by risk status.
   - **Doctor Appointment Distribution**: Pie chart of appointments by doctor.

---

## Troubleshooting
- **Database Errors**: Ensure the database file (`health_risk_data.db`) is writable and exists in the root directory.
- **Google API Errors**: Verify your API key and ensure it has the required permissions.
- **Missing Dependencies**: Run `pip install -r requirements.txt` to install all required packages.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Contribution
Feel free to fork this repository and submit pull requests for improvements or new features.

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## Contact
For any questions or feedback, open an issue on this repository or reach out to the project maintainers.
