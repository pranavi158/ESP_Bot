ESP Chatbot

Overview

The ESP Chatbot is an intelligent support solution designed to address inefficiencies in handling employee queries in large organizations. By leveraging cutting-edge technologies, the chatbot automates responses to HR, IT, and event-related questions while offering document processing features for summarization and keyword extraction. Its scalable architecture ensures optimal performance, maintaining response times under five seconds, even with concurrent users.

Features

Natural Language Processing (NLP): Utilizes Dialogflow and spaCy to understand and respond to employee queries effectively.

Document Processing: Supports file uploads for summarization and keyword extraction.

Secure Authentication: Implements two-factor authentication (2FA) using PyOTP for enhanced security.

Professionalism Filters: Ensures responses adhere to professional language standards.

Technologies Used

Backend: Flask (Python)

Frontend: HTML, CSS

Natural Language Processing: Dialogflow, spaCy

Security: PyOTP for 2FA

Other Tools: Node.js, OS module (Python)

Installation and Setup

Clone the repository:

git clone https://github.com/your-username/esp_chatbot.git
cd esp_chatbot

Install dependencies:

pip install -r requirements.txt

Configure Dialogflow credentials by adding the required JSON key file.

Run the Flask server:

python app.py

Access the application in your browser at http://localhost:5000.

Usage

Chatbot: Navigate to the chatbot interface to ask HR, IT, or event-related questions.

Document Processing: Upload documents for quick summarization or keyword extraction.

Authentication: Use 2FA for secure access.
