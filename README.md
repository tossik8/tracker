# Tracker Application
`tracker` is a simple command-line utility for tracking time spent on various projects. It allows you to start and stop sessions, view activity reports, list all projects, and delete projects.

## Features
- **Start Session:** Begin tracking time for a new or existing project.

- **Stop Session:** End an active session for a project.

- **Report Activity:** Get analytics for a specific project, including the number of sessions and total time spent.

- **List Projects:** View all tracked projects.

- **Delete Project:** Remove a project and all its associated sessions.

## Installation
Run:
```
pip install productivity-tracker
```
This will install the `tracker` command globally on your system.

## Usage
The `tracker` command uses subcommands for different operations.

1. **Start a Session**

    To start tracking time for a project:
    ```
    tracker start <project_name>
    ```
    - If `<project_name>` does not exist, it will be created.
    - If a session is already active for the specified project, an error will be raised.

2. **Stop a Session**

    To stop the active session for a project:
    ```
    tracker stop <project_name>
    ```
    - An error will be raised if the project does not exist or if there is no active session for it.

3. **Report Activity**

    To view analytics for a specific project:
    ```
    tracker report <project_name>
    ```
    - Shows the total number of sessions and the total time spent (in hours) on the project.

4. **List Projects**

    To see all projects you are tracking:
    ```
    tracker list
    ```
    - Lists all project IDs and names, along with the total number of projects.

5. **Delete a Project**

    To delete a project and all its associated sessions:
    ```
    tracker delete <project_name>
    ```
    - This action is irreversible. All session data for the project will be removed.

## Database
The application uses an SQLite database named `projects.db`, which will be created automatically in the parent directory of your `src` folder (e.g., in the `tracker` root directory) when you first run any `tracker` command.

The database schema includes two tables:
- projects: Stores project names and their unique IDs.
    - `id`: `INTEGER PRIMARY KEY`
    - `name`: `NOT NULL`

- sessions: Stores individual work sessions linked to projects.
    - `id`: `INTEGER PRIMARY KEY`
    - `project_id`: `NOT NULL` (Foreign Key referencing `projects.id`)
    - `start`: `datetime NOT NULL`
    - `end`: `datetime` (NULLable, indicates an active session)

Foreign key constraints with `ON DELETE CASCADE` are enabled, meaning that deleting a project will automatically delete all its associated sessions.