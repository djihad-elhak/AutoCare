Django Backend for Online Appointment Booking System
Project Overview
This Django project facilitates online appointment booking for vehicle services, featuring separate interfaces for customers, workshop staff, and administrators. The system includes functionalities for intuitive appointment forms, real-time repair tracking, centralized appointment management, automated notifications, and service customization.

Features
Customer Interface
Intuitive Appointment Form: A simple and user-friendly form where customers can enter personal information, vehicle details, and select the required service.
Personal Space: A dedicated area where customers can view their appointment history, update personal information, and track the real-time status of their vehicle repair.
Real-time Tracking: Allows customers to see the progress of their vehicle repairs, reducing anxiety and uncertainties.
Workshop Staff Interface
Centralized Appointment List: A dashboard where staff members can view, update, and manage appointment statuses (e.g., car arrived, not repairable, repaired).
Notification System: Automatic email notifications via Gmail to inform customers about their vehicle status, improving communication and customer satisfaction.
Administrator Interface
Service and Staff Management: An interface for adding and managing offered services, staff members, and vehicle types for more efficient organization.
Service Options Customization: The ability to configure and customize service options according to the workshop's specific needs, enhancing flexibility and operational efficiency.
Installation and Setup
Clone the repository:

bash
Copier le code
git clone https://github.com/djihad-elhak/AutoCare
cd AutoCare
Create a virtual environment and activate it:

bash
Copier le code
python3 -m venv env
source env/bin/activate
Install the required packages:

bash
Copier le code
pip install -r requirements.txt
Set up the MySQL database:

Install MySQL and create a database:

sql
Copier le code
CREATE DATABASE appointment_booking CHARACTER SET UTF8;
CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON appointment_booking.* TO 'your_username'@'localhost';
FLUSH PRIVILEGES;
Update the settings.py file to configure the MySQL database:

python
Copier le code
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'appointment_booking',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
Apply the database migrations:

bash
Copier le code
python manage.py migrate
Create a superuser:

bash
Copier le code
python manage.py createsuperuser
Run the development server:

bash
Copier le code
python manage.py runserver
Access the application:
Open your web browser and navigate to http://localhost:8000.

Configuration
Email Notifications
To enable email notifications, configure your email settings in settings.py:

python
Copier le code
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '<your_email>@gmail.com'
EMAIL_HOST_PASSWORD = '<your_email_password>'
Environment Variables
You may also use environment variables for sensitive information. Create a .env file in your project root and add:

bash
Copier le code
EMAIL_HOST_USER=<your_email>@gmail.com
EMAIL_HOST_PASSWORD=<your_email_password>
And update settings.py to use these variables:

python
Copier le code
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
Contributing
Contributions are welcome! Please follow these steps to contribute:

Fork the repository.
Create a new branch for your feature or bugfix.
Commit your changes with a descriptive message.
Push your changes to your forked repository.
Create a pull request to the main repository.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For any inquiries or issues, please contact your_email@example.com.
