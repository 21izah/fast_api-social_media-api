
from pydantic import EmailStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  database_hostname: str
  database_port:str
  database_password:str
  database_name:str
  database_username: str 
  secret_key:str
  algorithm:str
  access_token_expire_minutes:int
  
  MAIL_USERNAME: str
  MAIL_PASSWORD: str
  MAIL_FROM: EmailStr
  MAIL_PORT: int
  MAIL_SERVER: str
  MAIL_FROM_NAME: str 
  MAIL_STARTTLS: bool
  MAIL_SSL_TLS: bool
  USE_CREDENTIALS: bool 
  VALIDATE_CERTS: bool 

  
  class Config:
      env_file = ".env"
  
settings=Settings()