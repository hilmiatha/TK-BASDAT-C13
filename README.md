
# TK-BASDAT-C13

Welcome to the TK-BASDAT-C13 project! This project is a web application built with Django. Below are instructions for accessing the web application online and running it locally.

## Access the Web Application Online

To access the web application online, visit the following URL:
[https://tk-basdat-c13-production.up.railway.app/](https://tk-basdat-c13-production.up.railway.app/)

## Run the Web Application Locally

To run the web application locally, follow these steps:

### Prerequisites

- Python 3.10 or higher
- Git
- Virtualenv (optional, but recommended)

### Clone the Repository

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/hilmiatha/TK-BASDAT-C13.git
```

Navigate to the project directory:

```bash
cd TK-BASDAT-C13
```

### Set Up a Virtual Environment

It is recommended to use a virtual environment to manage your project dependencies. You can create and activate a virtual environment with the following commands:

#### Windows

```bash
python -m venv env
env\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv env
source env/bin/activate
```

### Install Requirements

Install the required packages using the following command:

```bash
pip install -r requirements.txt
```

### Run the Development Server

After installing the dependencies, you can run the development server with the following command:

```bash
python manage.py runserver
```

The web application should now be accessible at `http://127.0.0.1:8000/`.


