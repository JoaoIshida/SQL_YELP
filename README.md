# Disclaimer

This Code do not work outside Simon Fraser University's Microsoft SQL System.
A new version working on MySQL will be uploaded in the near future.

> This is a showcase of my knowledge with databases and SQL

# Yelp Database Search Application

This application allows users to search and view data from the Yelp database, including information about businesses and users.

## Usage Instructions

### Requirements

- Python 3.x installed on your system
- Required Python libraries: tkinter(already included in python), pyodbc

### Running the Application

1. Ensure Python is installed.

```python
python --version
```

2. Install the required libraries using pip:

```python
pip install pyodbc
```

### Database Connection

- The application connects to a SQL Server database.
- Modify the database connection details in the code:
- Open main.py in a text editor.
- Modify the connection details in the `conn` variable to match your database configuration:

```python
conn = pyodbc.connect('driver={ODBC Driver 18 for SQL Server};server=YOUR_SERVER_NAME;uid=YOUR_USERNAME;pwd=YOUR_PASSWORD;Encrypt=yes;TrustServerCertificate=yes')
```

### Running the Application

1. Open a terminal or command prompt.
2. Navigate to the directory containing the application files.
3. Run the main.py file:

```python
python main.py
```

4. Enter a valid User ID to log in and access the search functionalities.

### Using the Application

- After logging in, you'll see two tabs: "Business Search" and "User Search."
- Business Search:
- Search for businesses based on criteria like name, city, or minimum stars.
- View and filter the list of businesses.
- User Search:
- Search for users based on criteria like name, review count, or average stars.
- View and filter the list of users.
- Make sure to close the application properly using the window close button.

#### Note

- This readme assumes you have access to a SQL Server database compatible with the provided connection details.
