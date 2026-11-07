# Campus Find – College Lost and Found Portal

Campus Find is a web-based Lost and Found portal designed to help college students report lost belongings and find items reported by others.

## Features

- Report lost and found items
- View recently reported items
- Search by item name, category, or location
- Filter reports by Lost or Found
- Mark reports as resolved
- SQLite database for storing reports
- Health-check endpoint for deployment monitoring
- Automated tests using GitHub Actions

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Git and GitHub
- GitHub Actions
- Gunicorn

## Project Structure

```text
Campus_Find/
├── app.py
├── requirements.txt
├── Procfile
├── test_app.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── .github/
    └── workflows/
        └── ci.yml
```

## Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/swara-li/Campus_Find.git
   ```

2. Open the project folder:

   ```bash
   cd Campus_Find
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python app.py
   ```

5. Open this address in your browser:

   `http://127.0.0.1:5000`

## Automated Testing

Run the tests using:

```bash
python -m unittest test_app -v
```

GitHub Actions automatically runs the test suite when changes are pushed to the main branch.

## Project Status

The application is developed and tested locally. Cloud deployment is planned.

## Repository

[View Campus Find on GitHub](https://github.com/swara-li/Campus_Find)