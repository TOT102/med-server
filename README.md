# Main idea
The app's aim is to track changes in blood test results over time. These results are typically provided as PDF files by the laboratory that conducts the analysis. However, tracking changes directly in PDF format is inefficient, so the data is parsed into a more usable format. Since the amount of data is relatively small, using a full SQL database would be an overkill. Instead, the information is stored in JSON files. The parsing process is straightforward and done through regular expressions, which can be adjusted to suite different PDF layouts and styles. However, this simplicity comes with a price - the parser currently works only with PDF files provided by [BODIMED](https://bodimed.com/en/). The app is far from perfect but the current version is stable and can be used daily.

## UI
The user interface is very simple and consists of three main sections: 
- one displays a graph of the selected indicator 
- one is for file uploads and downloads
- the third shows the average, minimum, and maximum values of the selected indicator
![Screenshot 2025-07-04 194132](https://github.com/user-attachments/assets/9ca20fb5-18f0-4636-aaf4-e3af11bbdde5)

## Tech stack
<img width="1678" alt="Tech Stack Diagram (Copy)" src="https://github.com/user-attachments/assets/a49a0580-4590-443e-a4d4-f460744ccf7f" />

## Installation && How to run
The app can be started with [gunicorn](https://gunicorn.org/)
```
gunicorn --bind 0.0.0.0:5000 run:app
```
Or can directly be runned in a docker container
```
docker build -t med-server .
docker run -d -p 5000:5000 med-server
```

## Ideas for the future && Issues to be fixed
- Better parser
- Automatic downloading of PDF files directly from [BODIMED](https://bodimed.com/en/)
