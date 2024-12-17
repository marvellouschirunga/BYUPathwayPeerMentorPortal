# BYU Pathway Peer Mentor Portal

# Overview

BYU Pathway Peer Mentor Portal is a web application designed to facilitate seamless communication and collaboration among BYU Pathway Mentors. The goal is to create a unified platform where mentors can post questions, participate in discussions, and collaborate on topics relevant to their needs. This project demonstrates my ability to design and implement interactive web applications using Django while integrating dynamic content and user-based interactions.

The application provides:

* Dynamic Web Pages populated with database-driven content.
* User Interactivity, enabling user login, message posting, and real-time collaboration.
* Database Integration to manage rooms, messages, and user details.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>

2. Create  and activate a virtual environment:
    python -m venv venv
    source venv/bin/activate  # On Windows use `.venv\Scripts\activate`

3. Install all dependencies:
    pip install -r 
    requirements.txt

# Running the project
1. Apply migrations:
    python manage.py migrate

2. Run the development server:
     python manage.py runserver

3. Open the app in your browser at http://127.0.0.1:8000/.

## Additional Notes
* Ensure you have Python and pip installed.
* Update the requirements.txt file whenever you add new dependencies.

4. Identify Missing Dependencies
    If you encounter any missing ependencies while running your project, you can install them and update the requirements.txt file accordingly:

    pip install <missing-package>
    pip freeze > requirements.txt


{Provide a link to your YouTube demonstration.  It should be a 4-5 minute demo of the software running (starting the server and navigating through the web pages) and a walkthrough of the code.}

[Software Demo Video](https://youtu.be/gcYBLSkiNVY)

# Web Pages

1. ## Home Page
Displays all available "Huddle Rooms" where users can participate in discussions.
Each room dynamically pulls data from the database, including room name, host, and time created. Also has Recent Activities which Lists user activity such as replies to posts and new room messages. Dynamically pulls data from user activities and timestamps.
2. ## Room Page
Displays details of a specific huddle room.
Users can view past messages, post new messages, and see the list of participants.
Dynamically displays active online users with a green status indicator.
3. ## User Profile Page
Displays user details such as username, avatar, and participation history.
Users can see the rooms they've created or participated in.
4. ## Login/Registration Pages
Allows users to log in or sign up.
User authentication is dynamically managed using Django's built-in auth system.

# Development Environment

Tools:
* Visual Studio Code (Code editor)
* Git and GitHub (Version control)
* SQLite3 (Database)

Programming languages and Libraries:
* Python with Django (Back-end framework)
* HTML, CSS, and JavaScript (Front-end)
* Bootstrap (Responsive design framework)
* Pillow (Image management for avatars)

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [Django Documentation](https://docs.djangoproject.com/)
* [MDN Web Docs](https://developer.mozilla.org/)
* [Stack Overflow](https://stackoverflow.com/)

# Future Work

{Make a list of things that you need to fix, improve, and add in the future.}
* Implement push notifications for new messages or replies in rooms.
* Provide a more personalized dashboard with user statistics and room recommendations.
* Enhance the admin panel to allow better moderation of rooms and messages.





