import psycopg2
from tabulate import tabulate
import re

class FootballChatbot:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='turkish_football',
            user='postgres',
            password='postgres',
            host='localhost'
        )
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()

    def get_team_basic_stats(self, team_name, season=None):
        try:
            query = """
            SELECT 
                t.name,
                s.year,
                ts.matches,
                ts.goalsScored,
                ts.goalsConceded,
                ts.assists,
                ts.cleanSheets,
                ts.averageBallPossession,
                ts.avgRating
            FROM team_statistics ts
            JOIN teams t ON ts.team_id = t.id
            JOIN seasons s ON ts.season_id = s.id
            WHERE t.name ILIKE %s
            """
            params = [f"%{team_name}%"]
            
            if season:
                query += " AND s.year = %s"
                params.append(season)
            
            query += " ORDER BY s.year DESC LIMIT 1"
            
            self.cur.execute(query, params)
            result = self.cur.fetchone()
            
            if result:
                return f"{result[0]} in {result[1]} season:\n" \
                       f"• Played {result[2]} matches\n" \
                       f"• Scored {result[3]} goals and conceded {result[4]} (difference: {result[3]-result[4]})\n" \
                       f"• Made {result[5]} assists\n" \
                       f"• Kept {result[6]} clean sheets\n" \
                       f"• Average possession: {result[7]:.1f}%\n" \
                       f"• Average rating: {result[8]:.2f}"
            return "No data found for the specified team and season."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def get_team_comparison(self, team1, team2, season=None):
        try:
            query = """
            SELECT 
                t.name,
                s.year,
                ts.goalsScored,
                ts.goalsConceded,
                ts.assists,
                ts.averageBallPossession,
                ts.avgRating
            FROM team_statistics ts
            JOIN teams t ON ts.team_id = t.id
            JOIN seasons s ON ts.season_id = s.id
            WHERE t.name ILIKE ANY(%s)
            """
            params = [[f"%{team1}%", f"%{team2}%"]]
            
            if season:
                query += " AND s.year = %s"
                params.append(season)
            
            query += " ORDER BY s.year DESC, t.name LIMIT 2"
            
            self.cur.execute(query, params)
            results = self.cur.fetchall()
            
            if len(results) == 2:
                return f"Comparison between {results[0][0]} and {results[1][0]} in {results[0][1]} season:\n" \
                       f"Goals scored: {results[0][2]} vs {results[1][2]}\n" \
                       f"Goals conceded: {results[0][3]} vs {results[1][3]}\n" \
                       f"Assists: {results[0][4]} vs {results[1][4]}\n" \
                       f"Possession: {results[0][5]:.1f}% vs {results[1][5]:.1f}%\n" \
                       f"Average rating: {results[0][6]:.2f} vs {results[1][6]:.2f}"
            return "Could not find data for both teams in the specified season."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def get_team_form(self, team_name, season=None):
        try:
            query = """
            SELECT 
                t.name,
                s.year,
                ts.matches,
                ts.goalsScored,
                ts.goalsConceded,
                ts.bigChances,
                ts.bigChancesMissed,
                ts.shotsOnTarget,
                ts.avgRating
            FROM team_statistics ts
            JOIN teams t ON ts.team_id = t.id
            JOIN seasons s ON ts.season_id = s.id
            WHERE t.name ILIKE %s
            """
            params = [f"%{team_name}%"]
            
            if season:
                query += " AND s.year = %s"
                params.append(season)
            
            query += " ORDER BY s.year DESC LIMIT 1"
            
            self.cur.execute(query, params)
            result = self.cur.fetchone()
            
            if result:
                conversion_rate = (result[3] / result[5] * 100) if result[5] > 0 else 0
                return f"{result[0]}'s form analysis for {result[1]} season:\n" \
                       f"• Scoring efficiency: {conversion_rate:.1f}% of big chances converted\n" \
                       f"• Created {result[5]} big chances, missed {result[6]}\n" \
                       f"• {result[7]} shots on target in {result[2]} matches\n" \
                       f"• Team's average rating: {result[8]:.2f}"
            return "No form data found for the specified team and season."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def process_query(self, query):
        # Convert query to lowercase for easier matching
        query = query.lower()
        
        # Extract team names and season if present
        season_match = re.search(r'(\d{2}/\d{2})', query)
        season = season_match.group(1) if season_match else None
        
        # Basic stats request
        if "stats" in query or "statistics" in query:
            team_match = re.search(r'(?:stats|statistics).*?(?:for|of)\s+([a-zA-Z\s]+)', query)
            if team_match:
                team = team_match.group(1).strip()
                return self.get_team_basic_stats(team, season)
        
        # Comparison request
        elif "compare" in query or "vs" in query or "versus" in query:
            teams = re.findall(r'(?:compare|vs|versus)\s+([a-zA-Z\s]+)\s+(?:and|vs|versus)\s+([a-zA-Z\s]+)', query)
            if teams:
                team1, team2 = teams[0]
                return self.get_team_comparison(team1.strip(), team2.strip(), season)
        
        # Form analysis request
        elif "form" in query:
            team_match = re.search(r'form.*?(?:for|of)\s+([a-zA-Z\s]+)', query)
            if team_match:
                team = team_match.group(1).strip()
                return self.get_team_form(team, season)
        
        return "I'm sorry, I didn't understand your question. You can ask about:\n" \
               "1. Team stats (e.g., 'Show stats for Galatasaray')\n" \
               "2. Compare teams (e.g., 'Compare Galatasaray and Fenerbahce')\n" \
               "3. Team form (e.g., 'Show form for Galatasaray')\n" \
               "You can also specify a season (e.g., 'Show stats for Galatasaray in 24/25')"

def main():
    print("Welcome to the Turkish Football League Chatbot!")
    print("Ask me about team statistics, comparisons, or form analysis.")
    print("Type 'quit' to exit.")
    
    chatbot = FootballChatbot()
    
    while True:
        user_input = input("\nYour question: ").strip()
        
        if user_input.lower() == 'quit':
            break
        
        response = chatbot.process_query(user_input)
        print("\n" + response)
    
    chatbot.close()
    print("\nGoodbye!")

if __name__ == "__main__":
    main() 