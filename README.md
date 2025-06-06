## Create The Python Environtment

- Clone the repository (if you haven't already):
```
git clone https://github.com/your-username/Tubes3_Stima.git
cd Tubes3_Stima
```

- Create virtual environtment (maybe `python3` depending on your system):
```
python -m venv env
```

- Activate virtual environtment:
  - On Windows:
  ```
  .\env\Scripts\activate.bat
  ```
  - On Linux:
  ```
  source env/bin/activate
  ```

- Install requirements in environtment:
```
pip install -r requirements.txt
```

## Getting the CV Data
- The data used for this application can be found via the link <a href="https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset">here</a>
- Create the folder `/data` in the root directory as the place for the data
- For reference checkout the [project structure](#expected-project-structure) below

## Expected Project Structure
```
Tubes3_Stima/
├── data/                          # PDF input files organized by job categories
│   ├── ACCOUNTANT/
│   ├── ADVOCATE/
│   ├── AGRICULTURE/
│   ├── APPAREL/
│   ├── ARTS/
│   ├── AUTOMOBILE/
│   ├── AVIATION/
│   ├── BANKING/
│   ├── BPO/
│   ├── BUSINESS-DEVELOPMENT/
│   ├── CHEF/
│   ├── CONSTRUCTION/
│   ├── CONSULTANT/
│   ├── DESIGNER/
│   ├── DIGITAL-MEDIA/
│   ├── ENGINEERING/
│   ├── FINANCE/
│   ├── FITNESS/
│   ├── HEALTHCARE/
│   ├── HR/
│   ├── INFORMATION-TECHNOLOGY/
│   ├── PUBLIC-RELATIONS/
│   ├── SALES/
│   └── TEACHER/
│
├── src/                           # Source code for core functionality
│   ├── __init__.py
│   └── ExtractCV.py               # Class to extract continuous text from any PDF
│
├── test/                          # Unit and CLI testing scripts
│   ├── __init__.py
│   └── ExtractCVTest.py           # Run PDF extraction from CLI
│
├── env/                           # Virtual environment (should be excluded in .gitignore)
│
├── .gitignore                     # .gitignore ignores /data and /env
├── requirements.txt               # List of dependencies
└── README.md                      # Project documentation (this file)
```


## UNIT TESTING

### TESTING PDF EXTRACT
testing `src/ExtractCV.py` via root directory
```py
# in root directory of project
python -m test.ExtractCVTest <pdf path relative to root>

# example
python -m test.ExtractCVTest data/ACCOUNTANT/10554236.pdf
```



