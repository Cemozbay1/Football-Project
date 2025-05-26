import psycopg2
from tabulate import tabulate

def fetch_team_stats():
    # Connect to the database
    conn = psycopg2.connect(
        dbname='turkish_football',
        user='postgres',
        password='postgres',
        host='localhost'
    )
    cur = conn.cursor()
    
    try:
        # Execute the query
        query = """
        SELECT 
            t.name,
            s.year,
            ts.matches,
            ts.goalsScored,
            ts.goalsConceded,
            (ts.goalsScored - ts.goalsConceded) as goal_difference,
            ROUND(CAST(ts.goalsScored::float / NULLIF(ts.matches, 0) as numeric), 2) as goals_per_match,
            ROUND(CAST(ts.goalsConceded::float / NULLIF(ts.matches, 0) as numeric), 2) as conceded_per_match
        FROM team_statistics ts
        JOIN teams t ON ts.team_id = t.id
        JOIN seasons s ON ts.season_id = s.id
        WHERE t.name = 'Galatasaray'
        ORDER BY s.year DESC
        LIMIT 5;
        """
        cur.execute(query)
        
        # Fetch the results
        results = cur.fetchall()
        
        # Define headers for better output formatting
        headers = [
            'Team', 'Season', 'Matches', 'Goals For', 'Goals Against',
            'Goal Difference', 'Goals/Match', 'Conceded/Match'
        ]
        
        # Print results in a nice table format
        print("\nGalatasaray Goal Statistics Across Seasons:")
        print(tabulate(results, headers=headers, tablefmt='grid'))
        
        # Calculate improvement or decline
        if len(results) > 1:
            print("\nSeason-by-Season Goal Difference Change:")
            for i in range(len(results)-1):
                current_season = results[i]
                previous_season = results[i+1]
                change = current_season[5] - previous_season[5]  # Index 5 is goal_difference
                print(f"{previous_season[1]} → {current_season[1]}: {'+' if change > 0 else ''}{change}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    fetch_team_stats() 