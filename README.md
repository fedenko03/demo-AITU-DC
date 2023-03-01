# AITU Digital Control

Digital Control is a web application built using the Django web framework that allows university staff to manage keys and track their usage. 
The application uses a MongoDB/PostgreSQL database to store key data and history.

## Features

#### Users:
- Account creation, activation via corporate (@astanait.edu.kz) email.
- Remote sending of requests for taking the key.
- View your key collection history.
- Scanning the QR code at the security for taking/returning the keys.

#### For the administrator:
###### Taking keys:
- Select an available room using an interactive map or a drop-down list.
- Generating a QR code to confirm taking the key or entering data manually.
###### Return of keys:
- Generating a QR code to receive all active user requests or manually searching for an application.
###### History:
- View the entire history of key collection with detailed information.
- Downloading the entire history to an Excel file.

###### Interactive map:
- View information about each room (status, visibility, description, etc.)
- The ability to edit and add new rooms without having to change the code.

###### Other:
- View data about all registered users.
- Locking the admin panel with a one-time PIN.
- Change the administrator password through the appropriate form.
- Tracking of active applications for taking the key in notifications in the upper navbar.
- Separation of access *(users cannot go to the admin pages and vice versa)*

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

## Migrations settings
1. Создать БД. 
2. Настроить DATABASES в ```settings.py```. 
3. Закомментировать ```urls.py```
4. ```python manage.py migrate```
5. Откомментировать ```urls.py```
6. ```python manage.py makemigrations```
7. ```python manage.py migrate```
8. Настройка ```main/middleware.py```: Закомментировать middleware в ```settings.py```
9. Создать суперюзера ```python manage.py createsuperuser```
10. Запустить проект ```python manage.py runserver```
11. Открыть панель администратора и произвести все настройки: 
```KeyTakerSettings```, ```KeyReturnerSettings```, ```PIN```, ```Role```.

## License

Digital Control is released under the [MIT License](https://github.com/fedenko03/DC/blob/add-license/LICENSE).
