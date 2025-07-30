import os
from dotenv import load_dotenv

load_dotenv()  # This loads the variables from your .env file

#These are the variables in which we will store our CLIENT_ID and CLIENT_SECRET in
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv("REDIRECT_URI")
IP_ADDRESS = os.getenv("IP_ADDRESS")