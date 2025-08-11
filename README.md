# Mathgnosis

Mathgnosis is a web-based application that provides a suite of mathematical tools. It's built with a Python backend using FastAPI and a Python frontend using Reflex.

## Features

*   **Scientific Calculator:** Perform basic and advanced calculations.
*   **Complex Numbers:** Work with complex number operations.
*   **Matrices:** Perform matrix operations like addition, multiplication, and finding determinants.
*   **Vectors:** Perform vector operations.
*   **Calculus:** Solve calculus problems.
*   **Discrete Maths:** Tools for discrete mathematics.
*   **Statistics:** Perform statistical calculations.
*   **Probability:** Calculate probabilities.
*   **Equations:** Solve various types of equations.
*   **Graphs:** Visualize mathematical functions.
*   **Unit Converter:** Convert between different units.
*   **History:** View a history of your calculations.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.8+
*   Git

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/990aa/Mathgnosis.git
    cd Mathgnosis
    ```

2.  **Create and activate a virtual environment:**

    *   **Windows:**
        ```bash
        python -m venv .venv
        .venv\Scripts\activate
        ```

    *   **macOS/Linux:**
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

The application consists of two parts: a backend server and a frontend client. You'll need to run both to use the application.

1.  **Run the backend server:**

    Open a terminal and run the following command from the project's root directory:

    ```bash
    uvicorn backend.main:app --reload --port 8000
    ```

2.  **Run the frontend client:**

    Open a second terminal and run the following command from the project's root directory:

    ```bash
    reflex init
    reflex run
    ```

The application should now be running at `http://localhost:3000`.

## API Documentation

API documentation is available in the `api_documentation.yaml` file.
