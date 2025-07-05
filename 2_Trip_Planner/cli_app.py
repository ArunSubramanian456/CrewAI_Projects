from crewai import Crew, LLM
from trip_agents import TripAgents
from trip_tasks import TripTasks
from datetime import datetime, timedelta
import argparse
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv


class TripCrew:
    def __init__(self, origin, cities, date_range, interests):
        self.cities = cities
        self.origin = origin
        self.interests = interests
        self.date_range = date_range
        # self.llm = LLM(model="groq/llama3-8b-8192")
        self.llm = LLM(model="gemini/gemini-2.0-flash")
        # self.llm = LLM(model="openai/gpt-4o-mini")


    def run(self):
        try:
            agents = TripAgents(llm=self.llm)
            tasks = TripTasks()

            city_selector_agent = agents.city_selection_agent()
            local_expert_agent = agents.local_expert()
            travel_concierge_agent = agents.travel_concierge()

            identify_task = tasks.identify_task(
                city_selector_agent,
                self.origin,
                self.cities,
                self.interests,
                self.date_range
            )

            gather_task = tasks.gather_task(
                local_expert_agent,
                self.origin,
                self.interests,
                self.date_range
            )

            plan_task = tasks.plan_task(
                travel_concierge_agent,
                self.origin,
                self.interests,
                self.date_range
            )

            crew = Crew(
                agents=[
                    city_selector_agent, local_expert_agent, travel_concierge_agent
                ],
                tasks=[identify_task, gather_task, plan_task],
                verbose=True
            )

            result = crew.kickoff()
            return result
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

def validate_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format. Please use YYYY-MM-DD")

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if required API keys are set
    required_keys = ['GEMINI_API_KEY', 'SERPER_API_KEY', 'BROWSERLESS_API_KEY', 'GROQ_API_KEY', "OPENAI_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        print(f"Error: Missing required environment variables: {', '.join(missing_keys)}")
        print("Please set them in your .env file or environment.")
        return

    parser = argparse.ArgumentParser(description='AI Travel Planner')
    
    parser.add_argument('--origin', '-o', 
                       type=str, 
                       required=True,
                       help='Your current location (e.g., "San Mateo, CA")')
    
    parser.add_argument('--destination', '-d', 
                       type=str, 
                       required=True,
                       help='Destination city and country (e.g., "Bali, Indonesia")')
    
    parser.add_argument('--start-date', '-s',
                       type=validate_date,
                       required=True,
                       help='Start date of your trip (YYYY-MM-DD)')
    
    parser.add_argument('--end-date', '-e',
                       type=validate_date,
                       required=True,
                       help='End date of your trip (YYYY-MM-DD)')
    
    parser.add_argument('--interests', '-i',
                       type=str,
                       required=True,
                       help='Your interests and trip details (e.g., "2 adults who love swimming, dancing, hiking")')

    args = parser.parse_args()

    # Validate dates
    if args.end_date <= args.start_date:
        print("Error: End date must be after start date")
        return

    # Format date range as string
    date_range = f"{args.start_date} to {args.end_date}"

    print("\n🏖️ VacAIgent - AI Travel Planner")
    print("================================")
    print(f"\nPlanning your trip...")
    print(f"From: {args.origin}")
    print(f"To: {args.destination}")
    print(f"Dates: {date_range}")
    print(f"Interests: {args.interests}")
    print("\nThis may take a few minutes. Please wait while our AI agents work on your perfect trip...\n")

    trip_crew = TripCrew(args.origin, args.destination, date_range, args.interests)
    result = trip_crew.run()

    if result:
        print("\n✨ Your Trip Plan ✨")
        print("===================\n")
        print(result)
    else:
        print("\n❌ Failed to generate trip plan. Please try again.")

if __name__ == "__main__":
    main()


# Alternate to using argparse for testing purposes
# import sys

# def plan_trip(origin, destination):
#     print(f"Planning trip from {origin} to {destination}...")

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python script.py <origin> <destination>")
#         sys.exit(1)
#     origin = sys.argv[1]
#     destination = sys.argv[2]
#     plan_trip(origin, destination)

# How it works:

# When you run:
# python script.py "San Mateo, CA" "Bali, Indonesia"
# sys.argv[1] will be "San Mateo, CA"
# sys.argv[2] will be "Bali, Indonesia"
# These are passed to plan_trip() and processed.

# Basics of argparse:

# argparse is a Python standard library module for parsing command-line arguments.
# You create an ArgumentParser object, define expected arguments, and then parse them from sys.argv.
# It automatically generates help messages and handles errors for missing or invalid arguments.
# Example:
# import argparse

# parser = argparse.ArgumentParser(description="Demo")
# parser.add_argument('--name', type=str, required=True, help='Your name')
# args = parser.parse_args()
# print(f"Hello, {args.name}!")

# When should it be used?

# Use argparse when your script needs to accept user input from the command line (e.g., filenames, options, flags).
# It's best for scripts with multiple or complex arguments, or when you want built-in help and error handling.