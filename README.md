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

#### PyQt5 Editor for developers (optional)
https://www.qt.io/download-qt-installer 
### 3. Install Required Packages

Install the required packages in the Anaconda Prompt:

```bash
conda install pyqt pyqt5-designer  # Add other packages if needed
```

### 4. Set Up the Database

Navigate to the `db` directory and run the following command to initialize the SQLite database:

```bash
sqlite3 mydata.db < initialize.sql
```

### 5. Run the Application

Finally, navigate back to the main directory and run:

```bash
python main.py
```

This will launch the application. You can now perform CRUD operations on your data.

## Contributing

If you would like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.

## License

This project is open-source and available under the MIT License.

## Acknowledgments

- Add any acknowledgments, if any
