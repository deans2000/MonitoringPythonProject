# Monitoring Python Project

## Project Description

This project is a monitoring system that keeps track of employees' working hours. It processes data from two different gates, where employees check in and out during the workday. Based on these check-ins and check-outs, it calculates the total working hours for each employee on a daily basis. If an employee works less than 8 hours a day, an email notification is sent to the employee's manager. The project also includes a web interface for managing employees, uploading data, and viewing statistics.

The project is divided into two main parts:
1. **Data Ingestion and Backup**: The system reads data from a text file (Poarta1.txt) for one gate, validates the entries, stores the data into a MySQL database, and backs up the original data file.
2. **Web Interface**: Through this interface, users can add new employees, upload data in CSV format from another gate (Poarta2), and view statistics for the employees working under a certain manager. The system can be customized to send email notifications based on working hours.

### OOP Principles
The project follows Object-Oriented Programming (OOP) principles. A base class `Poarta` is designed with abstract methods, and the class `Poarta1` inherit from this base class to implement its specific logic.

### Email Notifications
The system is capable of sending email notifications using Gmail when employees work less than 8 hours in a day. A special app password is required for this functionality.

## Setup Instructions

### 1. Python Setup
- Install Python 3.11.x (ensure to tick "Add to PATH" in the installation wizard) via [this link](https://www.python.org/downloads/).
- Open a terminal in a location of your choice and clone the project repository:
    ```
    git clone https://github.com/deans2000/MonitoringPythonProject.git
    ```
- Navigate into the project directory:
    ```
    cd MonitoringPythonProject
    ```
- Create a directory named `intrari`:
    ```
    mkdir intrari
    ```
- Set up a virtual environment:
    ```
    python -m venv myenv
    ```
- Activate the virtual environment:
    ```
    myenv/Scripts/activate
    ```
- Install the required Python packages:
    ```
    pip install -r requirements.txt
    ```

### 2. Configuration
- Create a Python file `Passwords.py` in the root project folder with the following content:
    ```python
    emailPassword="your generated email password"
    mySQLServerPassword="your password for the mysql server"
    ```

- For the email functionality, you need to set up an app password for Gmail:
    1. Navigate to your Google account.
    2. Go to the "Security" section.
    3. Enable 2-Step Verification if it's not already enabled.
    4. Generate an app password in the "App Passwords" section (if you don't see the App passwords section, click [here](https://myaccount.google.com/apppasswords)).
    5. Use the generated password for `emailPassword` in the `Passwords.py` file.

### 3. MySQL Setup
- If you don't already have MySQL, install MySQL Workbench and MySQL Server 8.0.37 from [this link](https://dev.mysql.com/downloads/windows/installer/8.0.html) (or select the appropriate version for your OS).
- During installation, set a root password and use this for `mySQLServerPassword` in `Passwords.py`.
- After installation, open MySQL Workbench, connect to your server, and run the following SQL commands:
    ```sql
    CREATE DATABASE monitoringpythonproject;
    USE monitoringpythonproject;

    CREATE TABLE `access` (
      `data` varchar(100) NOT NULL,
      `sens` varchar(45) NOT NULL,
      `idAngajat` int NOT NULL,
      `idPoarta` int NOT NULL,
      `numePoarta` varchar(45) DEFAULT NULL
    );

    CREATE TABLE `angajati` (
      `ID` int NOT NULL AUTO_INCREMENT,
      `Nume` varchar(45) NOT NULL,
      `Prenume` varchar(45) NOT NULL,
      `Companie` varchar(45) NOT NULL,
      `IdManager` int DEFAULT NULL,
      PRIMARY KEY (`ID`)
    );
    ```

### 4. Running the Application
- Start the application by running:
    ```
    python main.py
    ```

### 5. Testing
#### Example Text File (Poarta1.txt)
- Create a text file named `Poarta1.txt` with the following content and place it in the `intrari` folder:
    ```
    1,2024-06-21T13:49:51.141Z,in;
    1,2024-06-21T13:52:53.142Z,out;
    2,2024-06-22T09:11:42.153Z,in; 
    1,2024-06-21T15:29:32.146Z,in;
    1,2024-06-21T19:32:31.100Z,out;
    4,2024-06-22T14:23:42.153Z,out
    5,2024-06-21T15:29:32.146Z,in;
    6,2024-06-21T20:32:31.100Z,out;
    7,2024-06-21T09:14:25.130Z,in;
    8,2024-06-21T18:00:00.100Z,out;
    9,2024-06-21T09:06:12.135Z,in;

    ```

- The data will automatically be processed and backed up.

#### Example CSV File (Poarta2.csv)
- Create a CSV file named `Poarta2.csv` with the following content:
    ```
    IdPersoana,Data,Sens
    3,2024-06-21T13:49:51.141Z,in
    3,2024-06-21T13:52:53.142Z,out
    4,2024-06-22T09:11:42.153Z,in
    3,2024-06-21T15:29:32.146Z,in
    3,2024-06-21T19:32:31.100Z,out
    1,2024-06-22T09:11:42.153Z,in
    1,2024-06-22T14:23:42.153Z,out
    2,2024-06-22T14:23:42.153Z,out
    5,2024-06-21T19:32:31.100Z,out
    6,2024-06-21T15:29:32.146Z,in
    7,2024-06-21T16:05:03.140Z,out
    8,2024-06-21T09:18:26.150Z,in
    9,2024-06-21T12:45:32.121Z,out
    ```

- You can upload the CSV file via the web interface at `localhost:5000`.

#### Web Interface
- Open your browser and go to `http://localhost:5000` to:
    1. Add new employees.
    2. Upload data via CSV files.
    3. View statistics for employees managed by a specific manager.
  
- To trigger email notifications, ensure that the system clock is set to the time when the check for working hours happens (it's set for 20:00 or 8PM, but you can set it manually in `main.py` line 55).

- Manager emails are set in `main.py` (line 85). Ensure the correct email is assigned for managers by their ID.

## Conclusion
The Monitoring Python Project provides an automated system for employee time tracking, management, and reporting. It features a robust backend and a clean web interface, utilizing Python, Flask, MySQL and html. The integration of email notifications ensures that managers stay informed about employees' working hours.
