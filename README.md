# AITU Digital Control

Digital Control is a web application built using the Django web framework that allows university staff to manage keys and track their usage. 
The application uses a MongoDB/PostgreSQL database to store key data and history.

## Features

- Staff can sign keys in and out, and view their history
- Admins can add and manage staff, rooms, and keys
- Staff can search for keys by room or keyword
- Admins can generate reports on key usage

## Requirements

To run Digital Control on your local machine, you will need to have the following software installed:

- Python 3.9
- Django 3.2.16
- MongoDB/PostgreSQL

## Installation

1. Clone the *Digital Control* repository to your local machine.
2. Create a virtual environment for the project and activate it.
3. Install the project dependencies using `pip install -r requirements.txt`.
4. Set up the PostgreSQL or MongoDB database and add the credentials to the `settings.py` file.
5. Run the Django migrations to create the necessary database tables: `python manage.py migrate`.
6. Start the development server: `python manage.py runserver`.

## Usage

Once the development server is running, you can access **Digital Control** by navigating to `http://localhost:8000/` in your web browser. The application provides separate views for staff and admin users, accessible via the navigation bar.

## Contributing

If you would like to contribute to Digital Control, please follow these steps:

1. Fork the repository to your own GitHub account.
2. Create a new branch for your feature or bug fix.
3. Write tests to cover any changes or additions.
4. Implement your feature or bug fix.
5. Ensure all tests pass.
6. Submit a pull request with your changes.

## License

Digital Control is released under the [MIT License](https://github.com/fedenko03/DC/blob/add-license/LICENSE).
