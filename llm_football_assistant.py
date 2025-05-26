import os
import psycopg2
from openai import OpenAI
import json
from typing import Dict, Any, List

class FootballDatabaseManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='turkish_football',
            user='postgres',
            password='postgres',
            host='localhost'
        )
        self.cur = self.conn.cursor()

    def execute_query(self, query: str, params: tuple = None) -> List[tuple]:
        try:
            if params:
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
            return self.cur.fetchall()
        except Exception as e:
            print(f"Database error: {e}")
            return []

    def get_column_names(self) -> List[str]:
        """Get all column names from team_statistics table"""
        query = """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'team_statistics'
        ORDER BY ordinal_position;
        """
        return [col[0] for col in self.execute_query(query)]

    def close(self):
        self.cur.close()
        self.conn.close()

class FootballAssistant:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.db = FootballDatabaseManager()
        
        # Get available columns for context
        self.available_columns = self.db.get_column_names()
        
        # System prompt that explains the assistant's capabilities
        self.system_prompt = f"""
        You are a Turkish Football League expert with access to a comprehensive database.
        The database contains detailed statistics for teams including:
        {', '.join(self.available_columns)}

        Your task is to:
        1. Analyze user questions about Turkish football
        2. Generate appropriate SQL queries to fetch relevant data
        3. Provide detailed, natural language responses using the data

        Important rules:
        - Always verify team names exist before querying
        - Handle season specifications carefully (format: YY/YY)
        - Provide context and insights in your answers
        - If you need multiple data points, use multiple queries
        - Format numbers nicely in responses
        - Use appropriate statistical comparisons when relevant
        """

    def generate_sql_query(self, user_question: str) -> str:
        prompt = f"""
        Based on the user's question, generate a SQL query to fetch the relevant data.
        The database has tables: seasons, teams, and team_statistics with relationships:
        - team_statistics.team_id references teams.id
        - team_statistics.season_id references seasons.id

        User question: {user_question}

        Return only the SQL query without any explanation.
        """

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        
        return response.choices[0].message.content.strip()

    def generate_natural_response(self, user_question: str, query_results: List[tuple], query: str) -> str:
        prompt = f"""
        Generate a natural language response to the user's question using the query results.
        
        User question: {user_question}
        Query executed: {query}
        Query results: {json.dumps(query_results)}

        Provide a detailed, informative response that:
        1. Directly answers the user's question
        2. Includes relevant statistics and context
        3. Adds insights where appropriate
        4. Uses natural, conversational language
        """

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content.strip()

    def answer_question(self, question: str) -> str:
        try:
            # Generate SQL query
            sql_query = self.generate_sql_query(question)
            
            # Execute query and get results
            results = self.db.execute_query(sql_query)
            
            # Generate natural language response
            response = self.generate_natural_response(question, results, sql_query)
            
            return response
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"

    def close(self):
        self.db.close()

def main():
    # Get API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Please set the OPENAI_API_KEY environment variable.")
        return

    print("Welcome to the Turkish Football League AI Assistant!")
    print("Ask me anything about Turkish football statistics.")
    print("Type 'quit' to exit.")

    assistant = FootballAssistant(api_key)

    try:
        while True:
            question = input("\nYour question: ").strip()
            
            if question.lower() == 'quit':
                break
            
            response = assistant.answer_question(question)
            print(f"\n{response}")
    finally:
        assistant.close()

if __name__ == "__main__":
    main() 