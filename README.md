# Kosh Web App

Kosh app is developed using the django web framework for managing the transaction's of the members of the kosh.

# What is Kosh?
Kosh is a Nepali word. In most of the city/villages of Nepal, people wants to save money for a month(we can call it as monthly saving). Saving is around Rs.100 - Rs.1000 approximately(in most of the cases). 

In every tole, there will be one person managing the kosh.

# Installation

Before starting the installation setup, we assume you have the python, git and postgresql installed on your system. If all of them are already installed on your local machine, you are ready to go.

Step 1: First create a directory called kosh, wherever you want to install this app.
		I will be installing on desktop for this example.
			`cd ~/Desktop && mkdir kosh && cd kosh`

Step 2: Let's create a virtual environment for our project.

1. First we have to install **virtualenv** using **pip**
	`pip install virtualenv`

2. Now let;s create a virtualenv
	`virtualenv venv`

3. Don't forget to **activate** your virtaul environment
	`source venv/Scripts/activate`

Step 2: Now clone this repository, use the following command:
```
git clone https://github.com/MuskanBartaula/kosh
```

Step 3: Install requirements, use the following command:
```
pip install -r requirements.txt
```

Step 4: Create a environment variable for your database credentials
```
export DB_USER=<your_user>
export DB_PASSWORD=<your_password>
```

Step 5: Create the database in postgresql.
		`createdb kosh_db`

Step 6: Let's run the migrate command:
		`python manage.py migrate`

Step 7: Create a superuser.
		`python manage.py createsuperuser`

Step 8: Now, let's run the server.
		`python manage.py runserver`

