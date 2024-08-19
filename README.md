# AI-Powered Auto Feedback App

This is a Flask-based web application that allows users (teachers and students) to upload academic articles in various formats and receive AI-generated feedback. The feedback is generated using OpenAI's GPT model and is provided in Turkish.

## Technologies Used

- **Python**: The core programming language used in this project.
- **Flask**: A lightweight web framework used to develop the web interface.
- **OpenAI GPT-3.5**: AI model used to generate feedback for uploaded articles.
- **SQLAlchemy**: ORM for handling the SQLite database.
- **Flask-Login**: Handles user authentication and session management.
- **Textract**: Used to extract text from various file formats including `.pdf`, `.docx`, `.rtf`, and `.odt`.
- **PyPDF2**: For extracting text from `.pdf` files.
- **Python-Docx**: For extracting text from `.docx` files.
- **PyRTF3**: For extracting text from `.rtf` files.

## Features

- **User Authentication**: Users can sign up, log in, and access different dashboards depending on whether they are teachers or students.
- **File Upload**: Users can upload articles in `.txt`, `.pdf`, `.docx`, `.rtf`, and `.odt` formats.
- **AI Feedback**: The application generates feedback for uploaded articles using OpenAI GPT-3.5 in Turkish.
- **Teacher Feedback**: Teachers can review and modify the generated feedback.
- **Dashboard**: Users can view their uploaded articles and the feedback received.

## Project Structure

project_root/  
│  
├── app.py # The main Flask application  
├── templates/ # HTML templates for the web pages  
│ ├── index.html  
│ ├── login.html  
│ ├── signup.html  
│ ├── dashboard.html  
│ ├── upload.html  
│ └── result.html  
├── uploads/ # Directory where uploaded files are stored  
├── requirements.txt # Required Python packages  
└── README.md # This readme file  


## Prerequisites

- Python 3.7+
- An OpenAI API key. You can get one from [OpenAI's website](https://beta.openai.com/signup/).

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/auto-feedback-app.git
    cd auto-feedback-app
    ```

2. **Create a virtual environment (optional but recommended)**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the OpenAI API key**:

    In `app.py`, replace `your_openai_api_key` with your actual OpenAI API key:

    ```python
    openai.api_key = 'your_openai_api_key'
    ```

5. **Run the Flask application**:

    ```bash
    python app.py
    ```

6. **Open the app in your browser**:

    Go to `http://127.0.0.1:5000` to view the app.

## How to Use

1. **Sign Up**: Create an account as either a teacher or a student.
2. **Log In**: Log in with your credentials.
3. **Upload an Article**: Go to the upload page and upload an article in one of the supported formats (`.txt`, `.pdf`, `.docx`, `.rtf`, `.odt`).
4. **View Feedback**: The AI-generated feedback is displayed after processing. Teachers can further edit the feedback before submitting it.
5. **Dashboard**: View all uploaded articles and feedback in your dashboard.

## Supported File Formats

- `.txt`
- `.pdf`
- `.docx`
- `.rtf`
- `.odt`

## Troubleshooting

- If the app fails to extract text from a file, ensure that all dependencies are installed correctly.
- For `.rtf` files, ensure that `PyRTF3` is used instead of `pyrtf_ng`.

## Contributing

Feel free to submit issues and pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [OpenAI](https://openai.com/)
- [Textract](https://textract.readthedocs.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
