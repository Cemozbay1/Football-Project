# Turkish Football League Database

This project creates a PostgreSQL database for Turkish football league statistics and provides tools to import data from JSON format.

## Prerequisites

- Python 3.7+
- PostgreSQL server installed and running
- Your JSON data file containing the Turkish football league statistics

## Setup

1. Install the required Python packages:
```bash
pip install -r requirements.txt
```

2. Configure PostgreSQL:
   - Make sure PostgreSQL is running
   - Update the database connection settings in `import_data.py` if needed:
     - username (default: 'postgres')
     - password (default: 'postgres')
     - host (default: 'localhost')

3. Prepare your data:
   - Place your JSON data file in the project directory
   - Rename it to `turkish_football_data.json` or update the filename in `import_data.py`

## Usage

Run the import script:
```bash
python import_data.py
```

This will:
1. Create a new database called `turkish_football`
2. Create the necessary tables and indexes
3. Import your JSON data into the database

## Database Structure

The database consists of three main tables:

1. `seasons` - Stores season information
   - id (PRIMARY KEY)
   - year (e.g., "24/25")

2. `teams` - Stores team information
   - id (PRIMARY KEY)
   - name

3. `team_statistics` - Stores detailed statistics for each team per season
   - Contains all team statistics including:
     - Offensive statistics
     - Defensive statistics
     - Passing statistics
     - And more...

## Error Handling

- If the database already exists, the script will notify you and continue
- If any errors occur during the import process, they will be displayed in the console