import os
import dotenv
dotenv.load_dotenv()

PORT = os.getenv("PORT") # Read params from .env file
DBURL = os.getenv("DBURL")
collName = "lyrics"