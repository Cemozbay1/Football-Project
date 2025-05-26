import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    # Connect to PostgreSQL server
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='postgres',
        host='localhost'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    # Create database if it doesn't exist
    try:
        cur.execute("DROP DATABASE IF EXISTS turkish_football")
        cur.execute("CREATE DATABASE turkish_football")
        print("Database created successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()

def apply_schema():
    # Connect to the new database
    conn = psycopg2.connect(
        dbname='turkish_football',
        user='postgres',
        password='postgres',
        host='localhost'
    )
    cur = conn.cursor()
    
    try:
        # Read and execute the schema file
        with open('schema.sql', 'r') as file:
            schema_sql = file.read()
            cur.execute(schema_sql)
        conn.commit()
        print("Schema applied successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def import_data():
    # Connect to the database
    conn = psycopg2.connect(
        dbname='turkish_football',
        user='postgres',
        password='postgres',
        host='localhost'
    )
    cur = conn.cursor()
    
    try:
        # Read the JSON data
        with open('turkish_football_data.json', 'r') as file:
            data = json.load(file)
            
        # Import seasons
        for season in data:
            cur.execute(
                "INSERT INTO seasons (year) VALUES (%s) RETURNING id",
                (season['year'],)
            )
            season_id = cur.fetchone()[0]
            
            # Import teams and their statistics
            for team in season['teams']:
                # Insert team if not exists
                cur.execute(
                    """
                    INSERT INTO teams (id, name)
                    VALUES (%s, %s)
                    ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name
                    """,
                    (team['id'], team['name'])
                )
                
                # Insert team statistics
                stats = team['statistics']
                stats['season_id'] = season_id
                stats['team_id'] = team['id']
                
                # Create the dynamic SQL query
                columns = ', '.join(stats.keys())
                placeholders = ', '.join(['%s'] * len(stats))
                values = list(stats.values())
                
                query = f"""
                    INSERT INTO team_statistics ({columns})
                    VALUES ({placeholders})
                """
                cur.execute(query, values)
        
        conn.commit()
        print("Data imported successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    create_database()
    apply_schema()
    import_data() 