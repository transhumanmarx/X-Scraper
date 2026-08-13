# X Scraper

X Scraper is a Python-based tool for collecting historical posts from X (formerly Twitter) within a user-defined date range.

The application was designed primarily as a research tool, particularly for academic and social science research.

## Features

- Search posts from a specific X account.
- Define a custom start and end date.
- Process searches using daily date windows.
- Display scraping progress in real time.
- Show the number of posts collected for each day.
- Display the collected posts in a table.
- Export collected data to Excel.
- Preserve scraping results across Streamlit interface updates.
- Launch the application through a Windows batch file.

## Support the project

If you find X Scraper useful for your research or projects, consider supporting its development with a coffee. ☕
Your support helps keep the project maintained and allows me to continue improving it.

[☕ Support me on Ko-fi](https://ko-fi.com/nicohouse97)

## Requirements

- Windows 10 or Windows 11
- Microsoft Edge
- Python 3
- An X account with access to the content being searched
- Internet connection

## 1. Installation

### 1.1 Download the repository

Download or clone this repository to your computer.

### 1.2 Install Python

Make sure Python 3 is installed and available from the command line.

You can check this by opening PowerShell and running:

```bash
python --version
```

###  1.3 Install dependencies

Open PowerShell in the project folder (right click on a blank space while being on the folder) and run:

```bash
python -m pip install -r requirements.txt
```

## 2. Logging in to X in Microsoft Edge

X Scraper uses Microsoft Edge to access X because the scraper connects to a local Edge browser session through Playwright. This allows the application to interact with X in a way that is closer to normal browser use.

For this reason, you need to be logged into your X account in the Microsoft Edge window opened by X Scraper before starting a scraping session.

### Why do I need to log in?

Some X content and search functionality may require an authenticated session. The scraper therefore uses the session that you have already opened in Edge rather than asking you to provide your X username or password to the application. **The scraper does not ask for or store your X password.** The application connects to the local Microsoft Edge session running on your own computer.

The Edge session used by X Scraper is launched with a separate browser profile (`C:\EdgeDebug`). This keeps the scraper's browser session separate from your normal Microsoft Edge profile. 

The source code of this project is publicly available for inspection.

## 3. Running the application

For Windows users, the easiest way to launch the application is to double-click:

`run_X_Scraper.bat` (located in the folder)

The launcher automatically:

1. Opens Microsoft Edge with remote debugging enabled.
2. Starts the Streamlit application.
3. Opens the local application in the browser.

The application will be available at:

`http://localhost:8501`

## 4. Using X Scraper

Once the application is open:

1. Enter the X username you want to search.
2. Select the start date.
3. Select the end date.
4. Click **"Iniciar scraping"**.
5. Wait for the scraping process to finish.
6. Review the results.
7. Download the results as an Excel file if desired.

The results include both:

- A daily summary showing the number of posts collected per day.
- A complete table containing the collected posts.

## 5. Output

Scraping results can be exported as an Excel file directly from the application.


## 6. Project structure

```text
X-Scraper/
│
├── app.py
├── scrape.py
├── run_X_Scraper.bat
├── logo.png
├── musica.mp3
├── requirements.txt
├── README.md
├── .gitignore
│
└── scraper/
    ├── browser.py
    ├── parser.py
    ├── exporter.py
    └── utils.py
```

## 7. Main components

- **`app.py`** — Provides the Streamlit graphical interface and manages the scraping workflow, progress display, results and Excel export.
- **`scrape.py`** — Coordinates the scraping process and connects the different components of the scraper.
- **`scraper/`** — Contains the modules responsible for browser interaction, parsing, data processing and exporting.
- **`run_X_Scraper.bat`** — Windows launcher that automatically starts Microsoft Edge in debugging mode and launches the Streamlit application.

## 8. Research and academic use

X Scraper was developed as a research-oriented tool for collecting historical social media data.

The collected data can be used for descriptive analysis, qualitative research, quantitative analysis and other research applications.

Users are responsible for ensuring that their use of the tool and the data collected complies with applicable laws, platform policies and their institution's research ethics requirements.

## 9. Limitations

The scraper retrieves posts available through the search and browsing process used by the application. It should not be interpreted as a guarantee that every post published by an account during a given period will be retrieved.

Search results and platform behavior may change over time.

The quality and completeness of the resulting dataset should therefore be evaluated according to the requirements of each research project.

## 10. License

This project is currently distributed without a specific open-source license.

If the project is later released under a specific license, this section should be updated accordingly.
