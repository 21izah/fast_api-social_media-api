import os
from dotenv import load_dotenv
from fastapi_mail import FastMail,MessageSchema, ConnectionConfig

load_dotenv()

class Envs:
  MAIL_USERNAME = os.getenv("MAIL_USERNAME")
  MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
  MAIL_FROM =os.getenv("MAIL_FROM")
  MAIL_PORT = os.getenv("MAIL_PORT")
  MAIL_SERVER = os.getenv("MAIL_SERVER")
  MAIL_FROM_NAME= os.getenv("MAIL_FROM_NAME")
  
  
# Define FastAPI-Mail connection configuration
conf = ConnectionConfig(
    MAIL_USERNAME = Envs.MAIL_USERNAME,
    MAIL_PASSWORD = Envs.MAIL_PASSWORD,
    MAIL_FROM = Envs.MAIL_FROM,
    MAIL_PORT = Envs.MAIL_PORT,
    MAIL_SERVER = Envs.MAIL_SERVER,
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS= True,
    # TEMPLATE_FOLDER = "api/templates",


)


# Initialize FastAPI-Mail instance
fm = FastMail(conf)
  
  