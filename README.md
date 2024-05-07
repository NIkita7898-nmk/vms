# Django Project README

The Vendor Management System is a web application built using Django and Django REST Framework, designed to streamline vendor-related operations within an organization. It offers a centralized platform to manage vendor profiles, track purchase orders, and assess vendor performance metrics.

## Prerequisites

Before running the project, make sure you have the following installed on your system:
- Python 3.x
- Django (install via `pip install django`)
- (Optional) Virtual environment (recommended for better package management)

## Installation

1. Clone the repository:

    ```
    git clone https://github.com/yourusername/yourproject.git
    ```

2. Navigate to the project directory:

    ```
    cd vms
    ```

3. Install dependencies:

    ```
    pip install -r requirements.txt
    ```


## Running the Project

### Linux

1. Activate virtual environment (if you're using one):

    ```
    source path/to/your/virtualenv/bin/activate
    ```

2. Run migrations:

    ```
    python manage.py migrate
    ```

3. Start the development server:

    ```
    python manage.py runserver
    ```

4. Access the application at `http://localhost:8000` in your web browser.

### Windows

1. Activate virtual environment (if you're using one):

    ```
    path\to\your\virtualenv\Scripts\activate
    ```

2. Run migrations:

    ```
    python manage.py migrate
    ```

3. Start the development server:

    ```
    python manage.py runserver
    ```

4. Access the application at `http://localhost:8000` in your web browser.



