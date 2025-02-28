```markdown
# Documentation for Web Application for Script Execution and User Management

## 1. Brief Explanation of the Code
This code is the backbone of a simple web application that acts like a control panel for running automated tasks and managing user access. Imagine it as a secure website where authorized users can log in and trigger a series of computer scripts to perform background jobs, like generating reports or updating databases.  It also includes features for administrators to manage user accounts and API keys, ensuring only the right people can access these automated tools.  Think of it as a central hub to control and monitor automated processes in a safe and organized way.

## 2. Detailed Breakdown of Each Part of the Code

### Section 1: Setting Up the Web Application (Configuration and Libraries)
This section is like preparing the foundation and tools needed for the web application to run.

*   **Importing Libraries:** The script starts by importing necessary tools, which are like software modules that provide pre-built functionalities. These tools are:
    *   `flask`: The core library for building the web application itself, handling web pages and user interactions.
    *   `flask_login`:  A tool specifically for managing user logins, sessions, and security.
    *   `functools.wraps`:  A utility for making functions work correctly when they are used as special decorators (explained later).
    *   `subprocess`:  A tool for running other computer programs (the scripts that this web app will execute).
    *   `os`:  A tool for interacting with the computer's operating system, like finding files and paths.
    *   `secrets`:  A tool for generating secure random numbers, used for creating API keys.
    *   `json`:  A tool for working with JSON data, a common format for storing and exchanging data.
    *   `datetime`:  A tool for working with dates and times, used for logging when actions happen in the application.
*   **Creating the Web Application:** It sets up the Flask web application itself, giving it a secret key. This secret key is like a password for the application itself, used for security purposes (it should be kept very safe and changed in a real-world setup).
*   **Setting up Login Management:** It configures `flask_login` to handle user logins. It specifies which web page to show when someone needs to log in ('/login') and sets messages to display to users about needing to log in.
*   **Defining File Locations:** It specifies where important files are located:
    *   `USERS_FILE`:  The location of the file (`users.json`) that stores user information (usernames, passwords, roles).
    *   `ENV_FILE`: The location of the file (`.env`) used to store API tokens.
*   **Loading and Saving User Data:** It defines functions to load user information from `users.json` when the application starts and to save any changes to user information back to this file. If the `users.json` file doesn't exist or is empty, it sets up default 'admin' and 'usuario' (user) accounts.
*   **Loading and Saving API Tokens:** It defines functions to load API tokens from the `.env` file and to save new tokens to this file. API tokens are like special keys that allow other applications to securely access certain features of this web application.
*   **Initializing User Data:** It loads the user information at the beginning of the script, so the application knows about the existing users.

### Section 2: Managing Users and Login Security
This section explains how the web application handles user accounts and ensures secure access.

*   **User Class:** It defines a 'User' class. This is like a blueprint for creating user objects within the application. Each user object will have:
    *   `id`: A unique identifier (username).
    *   `role`:  The user's role (like 'admin' or 'user'), which determines what they are allowed to do.
    *   Functions to check if a user is an admin and to get their API token.
*   **User Loading Function:** It sets up a function (`load_user`) that `flask_login` uses to retrieve user information based on a user ID (username). This function checks if the user ID exists in the loaded user data and, if so, creates a 'User' object for that user.
*   **Requiring Admin Role Function:** It defines a special function called `require_admin`. This is used as a 'decorator', which is like adding extra security checks to certain parts of the web application. When `@require_admin` is placed above a function, it means only users with the 'admin' role are allowed to access that function. If a non-admin user tries to access it, they will get an error message.
*   **Login and Logout Routes:** It sets up web addresses (routes) for:
    *   `/login`: This is the page where users can log in. It handles both displaying the login form and processing the submitted login details (username and password). It checks if the provided credentials are correct and, if so, logs the user in and redirects them to the dashboard.
    *   `/logout`: This is the page users can visit to log out. It logs the user out of the application and redirects them back to the login page with a success message.
*   **Dashboard Route:** It sets up a route for `/dashboard`. This is the main page users see after logging in. It is protected by `@login_required`, meaning only logged-in users can access it.

### Section 3: Running Automated Scripts
This section details how the web application allows users to execute pre-defined computer scripts.

*   **Executing Script Sequence Route:** It defines a web address `/ejecutar_secuencia` (meaning 'execute sequence') that, when accessed by a logged-in user, will run a series of Python scripts.
    *   **Script List:** It defines a list of script file names (`scripts`). These are the scripts that will be executed in order.
    *   **Running Scripts:** It loops through each script in the list:
        *   It constructs the full path to the script file on the computer.
        *   It uses the `subprocess.run` command to execute each script using `python3`. It captures the output (both normal output and error messages) from each script.
        *   It records the output or any errors from each script.
    *   **Returning Results:** After running all the scripts, it combines the output from each script into a single text message and displays it to the user.
*   **Executing Borrado Script Route:** It defines another web address `/ejecutar_borrado` (meaning 'execute deletion'). This route is similar to the previous one, but it executes a single script named 'Alpha_Espai_#borrado.py'. It's likely designed for a specific 'deletion' task. It also captures the output and any errors and displays a message indicating success or failure.
*   **API Endpoint for Script Execution:** It sets up an API endpoint `/api/ejecutar_secuencia` that can be accessed via a POST request (often used by other computer systems or applications).
    *   **Similar Script Execution Logic:** This API endpoint performs the same sequence of script executions as the `/ejecutar_secuencia` route.
    *   **Real-time Output Capture:**  It uses `subprocess.Popen` to run the scripts, which allows it to capture the output of each script in real-time, line by line, as it's running. This output is then printed to the application's log.
    *   **JSON Response:** Instead of displaying text on a webpage, this API endpoint returns the results in JSON format. JSON is a structured data format that is easy for computers to read and process. The JSON response includes:
        *   `script`: The name of the script that was executed.
        *   `output`: The output (or error message) from the script.
        *   `status`:  Whether the script execution was 'success' or 'error'.

### Section 4: API Token Management Features
This section explains how the web application allows administrators to manage API tokens.

*   **Generating API Token Route:** It sets up an API endpoint `/api/token` (accessible via POST request) that allows administrators to generate a new API token for their user account. It is protected by `@login_required` and `@require_admin`, so only logged-in admins can use it.
    *   **Generating Token:** It uses `secrets.token_urlsafe` to create a cryptographically secure random token.
    *   **Saving Token:** It uses the `save_token` function to store this new token in the `.env` file, associated with the admin user's username.
    *   **JSON Response:** It returns a JSON response containing a success message and the newly generated token.
*   **Listing API Tokens Route:** It sets up an API endpoint `/api/tokens` (accessible via GET request) that allows administrators to list the API tokens. It's also admin-protected.
    *   **Loading Tokens:** It uses the `load_tokens` function to retrieve all stored API tokens from the `.env` file.
    *   **JSON Response:** It returns a JSON response with a success indicator and a list of tokens (in this case, it seems to only return the token for the currently logged-in admin user).

### Section 5: User Account Management Features
This section describes how administrators can manage user accounts within the web application.

*   **Listing Users Route:** It sets up an API endpoint `/admin/users` (accessible via GET request) that allows administrators to get a list of all users in the system. It is admin-protected.
    *   **Retrieving User Data:** It accesses the `USERS` dictionary, which holds user information.
    *   **JSON Response:** It returns a JSON response containing a list of users, with each user's username and role.
*   **Creating User Route:** It sets up an API endpoint `/admin/users` (accessible via POST request) that allows administrators to create new user accounts. It is admin-protected.
    *   **Receiving User Data:** It expects to receive user details (username, password, role) in JSON format in the request.
    *   **Validating Input:** It checks if the required username and password are provided, if the username already exists, and if the provided role is valid ('admin' or 'user').
    *   **Creating User:** If the input is valid, it adds a new user entry to the `USERS` dictionary with the provided details.
    *   **Saving User Data:** It uses the `save_users` function to save the updated user data to the `users.json` file.
    *   **JSON Response:** It returns a JSON response indicating success and including the details of the newly created user.
*   **Updating User Route:** It sets up an API endpoint `/admin/users/<username>` (accessible via PUT request) that allows administrators to update an existing user's password or role. It is admin-protected and requires the username of the user to be updated to be specified in the URL.
    *   **Finding User:** It checks if the specified username exists in the `USERS` dictionary.
    *   **Updating User Data:** It allows updating the 'password' and/or 'role' of the user based on the JSON data received in the request. It also validates the provided role.
    *   **Saving User Data:** It saves the updated user data to `users.json`.
    *   **JSON Response:** It returns a JSON response indicating success and including the updated user details.
*   **Deleting User Route:** It sets up an API endpoint `/admin/users/<username>` (accessible via DELETE request) that allows administrators to delete a user account. It's admin-protected and requires the username to be deleted in the URL.
    *   **Finding User:** It checks if the specified username exists.
    *   **Preventing Deletion of Self or Admin:** It prevents administrators from deleting their own account or the default 'admin' account.
    *   **Deleting User:** If deletion is allowed, it removes the user entry from the `USERS` dictionary.
    *   **Saving User Data:** It saves the updated user data to `users.json`.
    *   **JSON Response:** It returns a JSON response confirming successful deletion.

### Section 6: Logging and Log Management Features
This section explains how the web application records actions and allows administrators to manage these logs.

*   **Saving Log Function:** It defines a function `save_log` that records actions performed in the application.
    *   **Log Entry Details:** For each action, it records the timestamp, the action description, and the user ID who performed the action.
    *   **Storing Logs:** It stores the logs in a JSON file named `logs.json`. It loads existing logs, adds the new log entry, and then saves the updated log data back to the file.
*   **Getting Logs Route:** It sets up an API endpoint `/get_logs` (accessible via GET request) that allows administrators to retrieve the logs. It is admin-protected.
    *   **Loading Logs:** It tries to load the logs from `logs.json`.
    *   **JSON Response:** If successful, it returns a JSON response with a success indicator and the list of logs. If there are no logs or an error occurs, it returns a JSON response indicating failure and an error message.
*   **Deleting Logs Route:** It sets up an API endpoint `/borrar_logs` (meaning 'delete logs', accessible via POST request) that allows administrators to clear all the logs. It is admin-protected.
    *   **Clearing Logs:** It overwrites the `logs.json` file with an empty list, effectively deleting all log entries.
    *   **Logging the Action:** It uses `save_log` to record the log deletion action itself.
    *   **JSON Response:** It returns a JSON response indicating success or failure.

### Section 7: Running the Web Application
This section explains how the web application is started.

*   **Main Execution Block:** The `if __name__ == '__main__':` block ensures that the following code only runs when the script is executed directly (not when it's imported as a library into another script).
*   **Starting the Flask Application:** It starts the Flask development server using `app.run(debug=True, host='0.0.0.0', port=5001)`.
    *   `debug=True`:  Enables debug mode, which is helpful during development as it automatically reloads the application when code changes and provides detailed error messages. **It should be disabled in a production environment.**
    *   `host='0.0.0.0'`: Makes the application accessible from any computer on the network (not just the local machine).
    *   `port=5001`:  Specifies the port number (5001) on which the web application will be accessible.

## 3. Inputs Used

| Input Name | Type | Description | Constraints | Source |
|------------|------|-------------|-------------|------------------|
| **users.json** | JSON file | Stores user account information, including usernames, passwords, and roles ('admin' or 'user'). | Must be a valid JSON file. The structure should be a dictionary where keys are usernames and values are dictionaries containing 'password' and 'role'. | Located in the same directory as the script, or as defined by `USERS_FILE` variable. |
| **.env** | Text file | Stores API tokens. Each token is associated with a username. | Each line should be in the format `USER_TOKEN_[username]=[token]`. | Located in the same directory as the script, or as defined by `ENV_FILE` variable. |
| **Web Requests (Login Form)** | HTTP POST request | User credentials (username and password) submitted through the login form on the `/login` page. | Username and password are expected as form data. | User interaction via web browser on the `/login` page. |
| **Web Requests (API - Script Execution)** | HTTP POST request |  Request to execute a sequence of scripts via the `/api/ejecutar_secuencia` endpoint. |  No specific data input in the request body for this endpoint in the current code, but it expects a valid login session or API token for authorization. | External application or system making an API call to `/api/ejecutar_secuencia`. |
| **Web Requests (API - Token Generation)** | HTTP POST request | Request to generate a new API token for the currently logged-in admin user via the `/api/token` endpoint. | No specific data input in the request body. Requires admin user authentication. | User interaction via web browser or external application making an API call to `/api/token`. |
| **Web Requests (API - User Management)** | HTTP GET, POST, PUT, DELETE requests with JSON data | Requests to list, create, update, or delete user accounts via the `/admin/users` and `/admin/users/<username>` endpoints. | Requires admin user authentication. POST and PUT requests expect user details (username, password, role) in JSON format in the request body. | User interaction via web browser or external application making API calls to `/admin/users` endpoints. |
| **Web Requests (API - Log Management)** | HTTP GET, POST requests | Requests to retrieve logs via `/get_logs` and delete logs via `/borrar_logs` endpoints. | Requires admin user authentication. | User interaction via web browser or external application making API calls to `/get_logs` or `/borrar_logs`. |

## 4. Outputs Generated

| Output Name | Type | Description | Conditions | Destination |
|-------------|------|-------------|------------|-----------------------|
| **Web Pages (HTML)** | HTML pages | Dynamic web pages served by the Flask application, including login page, dashboard, and potentially error pages. | Generated in response to user requests to different routes (e.g., `/`, `/login`, `/dashboard`). | Displayed in the user's web browser. |
| **API Responses (JSON)** | JSON data | Structured data returned by the API endpoints in JSON format. | Generated in response to API requests to endpoints like `/api/ejecutar_secuencia`, `/api/token`, `/api/tokens`, `/admin/users`, `/get_logs`, `/borrar_logs`. | Sent back to the client (web browser or external application) that made the API request. |
| **logs.json** | JSON file | Stores a log of actions performed within the web application, including login attempts, script executions, and user management actions. | Updated every time a loggable action occurs (login, logout, script execution, API token generation, user management, log deletion). | Saved in the same directory as the script. |
| **Updated .env** | Text file | The `.env` file is modified to store newly generated API tokens. | Updated when an admin user generates a new API token via the `/api/token` endpoint. | Saved in the same directory as the script. |

## 5. Final Summary
This web application acts as a secure control panel for automating tasks and managing user access.  Think of it like a locked room with a control board inside. Only authorized personnel (users with logins) can enter the room (access the web application). Inside, they can press buttons (trigger scripts) to make automated processes run, like generating reports or updating systems.  Administrators, who have special keys to the room (admin accounts), can also manage who else is allowed to enter (create, modify, delete user accounts) and issue special access cards (API tokens) for other automated systems to interact with the control panel securely.  The application also keeps a logbook (logs.json) of all activities, so administrators can track what's been happening.  Essentially, it provides a user-friendly and secure way to run and monitor automated tasks and manage user permissions, making complex backend processes easier to control and oversee.
```