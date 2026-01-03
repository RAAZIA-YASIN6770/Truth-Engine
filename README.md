# Truth Engine

## 1. Project Purpose
The Truth Engine is a deterministic, browser-based logical reasoning system. Its primary function is to present users with logic puzzles containing contradictory statements, requiring the identification of the single false statement based on strict logical deduction. The system is built to demonstrate adherence to formal software engineering practices.

## 2. Engineering Philosophy
This project strictly adheres to IEEE 830 Software Requirements Specifications (SRS) and follows the Iterative Incremental Model. Key engineering principles include:

*   **Determinism**: The logic engine produces binary, reproducible results (Success/Failure) without randomness or heuristic hints.
*   **Traceability**: All features map directly to the SRS and Planning documents.

## 3. Technical Stack
*   **Backend**: Python 3.10+ (Flask)
*   **Frontend**: Semantic HTML5 (Minimalist UI)
*   **Data Storage**: JSON-based scenario definitions
*   **Version Control**: Git

## 4. Installation and Execution
**Prerequisites**: Python 3.10 or higher.

1.  **Clone the repository** (if applicable) or navigate to the project root.

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**:
    ```bash
    python main.py
    ```

4.  **Access the interface**:
    Open a web browser and navigate to `http://localhost:5000`.

## 5. How to Play
1.  **Analyze**: Read the scenario description and the set of statements provided by the AI subsystems.
2.  **Deduce**: Identify the logical contradiction. By definition, exactly one statement is false.
3.  **Select**: Choose the statement believed to be false via the interface.
4.  **Submit**: Click "Analyze Logic" to validate the deduction.