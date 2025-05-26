import psycopg2
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
import json
from typing import List, Dict, Any

class FootballDatabaseManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='turkish_football', 
            user='postgres',
            password='postgres',
            host='localhost'
        )
        self.cur = self.conn.cursor()

    def execute_query(self, query: str, params: tuple = None) ->List[tuple]:
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

class LocalFootballAssistant:
    def __init__(self, model_path: str):
        # Initialize Llama model with streaming output
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        
        self.llm = LlamaCpp(
            model_path=model_path,
            temperature=0.1,
            max_tokens=2000,
            n_ctx=2048,
            callback_manager=callback_manager,
            verbose=False
        )
        
        self.db = FootballDatabaseManager()
        self.available_columns = self.db.get_column_names()
        
        # Template for SQL generation
        self.sql_template = PromptTemplate(
            input_variables=["question"],
            template="""You are a SQL expert. Generate a SQL query for the following question.
            The database has these tables:
            - seasons (id, year)
            - teams (id, name)
            - team_statistics (various statistics, linked to teams and seasons)
            
            Available columns in team_statistics:
            {columns}
            
            Question: {question}
            
            Return only the SQL query, nothing else.""".format(
                columns=", ".join(self.available_columns),
                question="{question}"
            )
        )
        
        # Template for natural language response
        self.response_template = PromptTemplate(
            input_variables=["question", "query", "results"],
            template="""You are a Turkish Football League expert.
            Answer the following question using the provided data.
            
            Question: {question}
            SQL Query used: {query}
            Query results: {results}
            
            Provide a detailed, natural language response that answers the question
            and provides relevant insights from the data."""
        )

    def generate_sql_query(self, question: str) -> str:
        prompt = self.sql_template.format(question=question)
        return self.llm.invoke(prompt).strip()

    def generate_response(self, question: str, query: str, results: List[tuple]) -> str:
        prompt = self.response_template.format(
            question=question,
            query=query,
            results=json.dumps(results, indent=2)
        )
        return self.llm.invoke(prompt).strip()

    def answer_question(self, question: str) -> str:
        try:
            # Generate SQL query
            print("\nGenerating SQL query...")
            sql_query = self.generate_sql_query(question)
            print(f"\nExecuting query: {sql_query}")
            
            # Execute query
            results = self.db.execute_query(sql_query)
            print("\nGenerating response...")
            
            # Generate natural language response
            response = self.generate_response(question, sql_query, results)
            return response
            
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def close(self):
        self.db.close()

def main():
    # Path to your downloaded Llama model
    model_path = "models/llama-2-7b-chat.Q4_K_M.gguf"
    
    print("Welcome to the Local Turkish Football League Assistant!")
    print("Ask me anything about Turkish football statistics.")
    print("Type 'quit' to exit.")
    
    try:
        assistant = LocalFootballAssistant(model_path)
        
        while True:
            question = input("\nYour question: ").strip()
            
            if question.lower() == 'quit':
                break
            
            response = assistant.answer_question(question)
            print(f"\nResponse: {response}")
            
    except Exception as e:
        print(f"Error initializing the assistant: {str(e)}")
        print("Please make sure you have downloaded the Llama model and specified the correct path.")
    finally:
        if 'assistant' in locals():
            assistant.close()

if __name__ == "__main__":
    main() 