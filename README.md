# Emotion Feedback App

EmotionFeedbackApp is a web application for collecting and analyzing user emotion feedback. It is built using Django with a mix of HTML, CSS, Python, and JavaScript.

## Features

- **Emotion Feedback:** Users can submit feedback about their emotions.
- **Data Storage:** Feedback is stored in a SQLite database.
- **Web Interface:** Simple, clean front-end built with HTML and CSS.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/bacnguyenne/EmotionFeedbackApp.git
   cd EmotionFeedbackApp
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv env
   # On macOS/Linux:
   source env/bin/activate
   # On Windows:
   env\Scripts\activate
   ```

3. **Install Dependencies**

   This project requires Django. Install it using pip:

   ```bash
   pip install django
   ```

   *If additional dependencies are needed, add them to a requirements file and install with:*

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Apply Migrations**

   Run the following command to set up your database:

   ```bash
   python manage.py migrate
   ```

2. **Start the Development Server**

   ```bash
   python manage.py runserver
   ```

3. **Access the App**

   Open your web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the application.

## Contributing

Contributions are welcome! If you have improvements, bug fixes, or ideas, please fork the repository and open a pull request.
