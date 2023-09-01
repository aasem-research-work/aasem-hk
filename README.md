# Hisaab Kitaab App

This project is a shop management system built with Python and PyQt5. It is designed to manage credit, debit, and other business transactions.

## Prerequisites

- Python 3.x
- SQLite
- PyQt5
- PyQt5 Designer (Optional but recommended for UI modifications)

## Getting Started

These instructions will help you set up the project on your local machine for development purposes.

### 1. Clone the Repository

First, clone this GitHub repository to your local machine.

```bash
git clone https://github.com/aasem-research-work/aasem-hk.git
cd aasem-hk
```

### 2. Create a Conda Environment

We recommend using Anaconda for managing Python environments. If you haven't installed Anaconda yet, download and install it from [here](https://www.anaconda.com/products/distribution).

After installing Anaconda, open the Anaconda Prompt and create a new environment called `pyqt5` by running:

```bash
conda create --name pyqt5 python=3.8.17
```

Activate the environment:

Mac/Linux:  
```bash
conda activate pyqt5
```

Windows:  
```bash
activate pyqt5
```

Install the required packages in the Anaconda Prompt:

```bash
pip install PyQt5
pip install PyQt5Designer
pip install pyqt5-tools
```

### 3. for developers (optional)


- Install **Sqlite**: https://www.sqlitetutorial.net/download-install-sqlite/
  
- **PyQT5 Editor**:
To Install:  
```pip install pyqt5-tools```

To open the editor:
```pyqt5-tools designer```

- **PyInstaller**:  
  To Install:  
   ```pip install pyinstaller```

  To create:
  ```
  pyinstaller --onefile --windowed main.py
  ```

- Install **Sqlite Studio**:  
  https://sqlitestudio.pl/

  



  

### 4. Run the Application

Make sure to be in the main directory and run:

```bash
python main.py
```

This will launch the application. 

## Contributing

If you would like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.

## License

This project is open-source and available under the MIT License.


