from dotenv import load_dotenv
from pydantic import BaseSettings, Field


load_dotenv()


TEST_PUBLIC_KEY = """"
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDIzi1aV7xG1BGjwf1ZsCxiMO5j
dYEPVfdPDLbBQtMD4VZlNb4ps2B6bExyLisOUxnlhEqdVn424EHIFRwNAV3eo0Gc
RrEGT4u57+Esqy9QQmvknJaA+oBFlzCpMLV3clQIm6ropbVtgqQtnLH19WJMfal3
nwB/v8Nle2XNQ7DJKwIDAQAB
-----END PUBLIC KEY-----
"""


class AuthSettings(BaseSettings):
    auth_secure_key: str = Field(
        env="AUTH_SECURE_KEY", default="access_token_cookie"
    )
    jwt_algorithm: str = Field(env="JWT_ALGORITHM", default="RS256")
    jwt_secret: str = Field(env="JWT_SECRET", default=TEST_PUBLIC_KEY)

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


auth_settings = AuthSettings()
