# Cs50Final
README.md
⚽ Hunger Football Drive Platform
📌 Introduction

The Hunger Football Drive Platform is a community-driven web application built with Flask that combines sports, charity, and technology into a unique and impactful project. The idea is simple but powerful: volunteers who want to participate in a charity football match can register online, make a mandatory contribution to cover the cost of their customized jersey (₦15,000), and get randomly assigned to one of four football clubs. Volunteers who do not want to play football are not left out—they can still support the cause by donating food items or making a cash contribution.

The ultimate goal of this platform is two-fold:

Raise awareness about hunger while providing practical support in the form of food and donations.

Engage the community through sports, using football as a fun, unifying activity that motivates people to give back.

Every action on this platform—from registering, uploading receipts, and donating food, to exporting rosters and generating leaderboards—is designed to streamline the logistics of managing a football-based food drive.

This project is developed as a CS50 Final Project but is designed to be realistic enough for use by NGOs, student organizations, and communities that want to combine fundraising with sports and awareness campaigns.

🌟 Features

This project includes a wide range of features that address both volunteers who want to play football and volunteers who want to support through donations.

👤 User Features

Register as a volunteer (player or supporter).

Mandatory receipt upload (₦15,000 for players, food/cash donations for supporters).

Automatic player ID generation for football participants.

Random club assignment into one of four teams (e.g., Lions, Eagles, Panthers, Tigers).

View confirmation page after successful registration.

🎽 Player-Specific Features

Custom Player IDs: Each football player gets a unique identifier that can later be used for roster management.

Club Assignment: Players are randomly assigned to a club, ensuring fairness and fun in team formation.

Receipt Upload: Receipts for jersey contributions (₦15,000) are uploaded and stored securely, visible only to the admin.

🏟️ Supporter-Specific Features

Supporters who do not wish to play can:

Donate food items.

Donate cash equivalents (uploaded as receipts).

Non-player donations are also tracked and included in the leaderboard of total contributions.

🛠️ Admin Features

View all uploaded receipts (only admin can access them).

Export Club Rosters in CSV or PDF format, useful for printing or sharing with team coordinators.

Leaderboard Dashboard showing total donations collected (cash + estimated food donations).

Manage all volunteers through the database, with tools to verify contributions.

🎨 UI/UX Features

Color scheme:

General site background: cream.

Headers and navigation bar: green.

Buttons and highlights: white, red, yellow accents.

Responsive design: Works on both desktop and mobile devices.

Simple, clear navigation: Users can easily move between registration, donation, and information pages.

🗂️ Project Structure
HungerFootball/
│
├── app.py                # Main Flask application
├── requirements.txt      # Dependencies for deployment
├── Procfile              # For production servers like Heroku/Render
│
├── static/
│   ├── style.css         # Custom CSS styling
│   └── receipts/         # Uploaded receipts (accessible only to admin)
│
├── templates/
│   ├── layout.html       # Base template for all pages
│   ├── index.html        # Homepage
│   ├── register.html     # Registration form
│   ├── login.html        # Admin login
│   ├── roster.html       # Team rosters (admin view)
│   ├── upload_receipt.html # For uploading receipts
│   ├── apology.html      # Error handling template
│   └── leaderboard.html  # Donation leaderboard
│
├── database.db           # SQLite database (users, donations)
└── README.md             # Documentation

💻 Installation and Setup

Follow these steps to get the project running locally:

1️⃣ Clone the repository
git clone https://github.com/yourusername/hunger-football.git
cd hunger-football

2️⃣ Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Initialize the database

Inside a Python shell:

from app import init_db
init_db()


This will create the necessary tables (users and donations).

5️⃣ Run the app locally
flask run


Visit: http://127.0.0.1:5000

🚀 Deployment

This app is deployable on Heroku, Render, or Railway.

Procfile (already included)
web: gunicorn app:app

Steps (Render Example)

Push your code to GitHub.

Connect your repository to Render.

Add requirements.txt and Procfile.

Set environment to Python 3.11+.

Deploy.

📊 Database Design
Users Table
Column	Type	Notes
id	INT	Primary key, autoincrement
name	TEXT	Volunteer’s name
email	TEXT	Unique, for login/contact
play	TEXT	“yes” or “no” (playing football or supporter)
player_id	TEXT	Unique Player ID (for footballers only)
receipt	TEXT	File path to uploaded receipt
club	TEXT	Club assignment (for footballers only)
Donations Table
Column	Type	Notes
id	INT	Primary key, autoincrement
donor	TEXT	Name or reference
type	TEXT	“cash” or “food”
amount	REAL	Donation amount (₦)
timestamp	DATETIME	Auto-generated when inserted
🧩 How It Works (User Flow)

Landing Page (index.html)

Introduction to the Hunger Football initiative.

Buttons to register as a player or a supporter.

Registration (register.html)

Players select "yes" to play → asked to upload ₦15,000 receipt.

Supporters select "no" → asked to upload a receipt of food/cash donation.

Receipt Upload (upload_receipt.html)

File is saved in /static/receipts/.

Only admins can view uploaded files.

Club Assignment

Players are automatically assigned to a random club.

Confirmation

User gets a confirmation page showing their Player ID or supporter status.

Admin Login (login.html)

Admin views all receipts, rosters, and leaderboard.

Admin can export club rosters to CSV or PDF.

Leaderboard (leaderboard.html)

Displays total donations raised (cash + food).

📈 Example Scenarios
Scenario 1: Player Registration

John registers as a football player.

Uploads a ₦15,000 payment receipt.

System generates a unique Player ID: P-0043.

John is randomly assigned to “Team Eagles.”

Admin can later export a PDF roster of all Eagles.

Scenario 2: Supporter Registration

Mary wants to donate but not play.

She chooses “No” for playing, uploads a food donation receipt.

Mary is registered as a supporter.

Her donation is counted toward the leaderboard.

Scenario 3: Admin Actions

Admin logs in, checks receipts uploaded by players/supporters.

Admin exports all rosters to PDF and CSV.

Admin checks leaderboard showing total donations (₦ + food equivalents).

🔮 Future Improvements

Email confirmations: Send volunteers confirmation emails with their Player ID or supporter badge.

QR Codes: Generate QR codes for quick check-in at match venues.

Payment Gateway Integration: Direct online payments instead of manual receipt upload.

Multiple Events Support: Expand beyond football to include basketball, marathon, or cultural events.

Gamification: Award digital badges to top supporters or highest contributors.

Mobile App Version: Develop a mobile-friendly version or a dedicated app using React Native or Flutter.

🙌 Acknowledgements

Inspired by community-driven charity events and the CS50x Harvard OpenCourseWare Project.

Thanks to the FoodClique Support Initiative for their real-world work on hunger awareness in Nigeria.

Special thanks to CS50 teaching staff and the open-source community for tools that made this project possible.

📢 Conclusion

The Hunger Football Drive Platform is more than just a web app—it is a movement that uses the power of sports to fight hunger. By encouraging community members to either play football or donate, the platform builds a bridge between fun, fitness, and philanthropy.

Built with Flask, SQLite, and Python, and enhanced with modern web practices, this project represents a practical solution that can scale from a small community event to a city-wide or even national initiative.

⚡ Whether you are a player, a supporter, or an organizer, this project provides all the tools needed to make an impact, one goal and one meal at a time.

That’s a little over 1,200 words ✅.

Would you like me to also add screenshots placeholders (like ![screenshot](static/screenshot1.png)) in the README so you can later upload images of your site and make it even more engaging?
