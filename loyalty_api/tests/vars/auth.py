import os
import time
from typing import Dict

import jwt
from dotenv import load_dotenv


load_dotenv()

TEST_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDIzi1aV7xG1BGjwf1ZsCxiMO5jdYEPVfdPDLbBQtMD4VZlNb4p
s2B6bExyLisOUxnlhEqdVn424EHIFRwNAV3eo0GcRrEGT4u57+Esqy9QQmvknJaA
+oBFlzCpMLV3clQIm6ropbVtgqQtnLH19WJMfal3nwB/v8Nle2XNQ7DJKwIDAQAB
AoGAHNj5zPvDsY0vx43L3sGfbq/G34T2+IQKFlImQxddhzYtGjchTY5Wct/yD4kw
aEtp8f4SVg4h7bJD4QGfWQL0QBGdk84Q5y29vau3XxHMmZn6URHqMs6RciQDzKdB
De/zb1rn3vOQuZIXO+ODhbK4cWPm/u4QyObzSAX2sYigyzkCQQDnaTqyNuE8LLxN
QVxJIaRARr4Y8UvxtS+sVhK4NqeIgw9x+TsDoMeePZuZZ6HW9azzSlGERnMuQnil
GgypQUUXAkEA3iRsB+jN25P5YY5PHTA/XbLCEM/ZhFc78dD4p5j24J2hB1ibBdoa
U9xHfXlV4S/nSYnlqS+0NLlfqBRZ+hxRDQJBAJyL/HA5Xg+mN9CPic3TW1k8Qjd/
bR/bsZ+FLu690oIwH0+8Cec/aisrhEq3560Sz+hZ+2Ffg2XlA9a1E6GgjQsCQQCa
cvxhq22lo4aaW5WKF8eW3/iqM7lqmDRndwHLlUDg/ve84dA3C2OOtvNFvB0HyoSm
zqfNMAu9NL3bYPsGOLXpAkABkLj2TbaFGbMVceGAeVbTR0OrU8DC4x+HcQMBYwsy
BT/C0/PFVtrscU8wbMsXizjYfz5MVyeglVB0ToZeQ8mZ
-----END RSA PRIVATE KEY-----
"""

TEST_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDIzi1aV7xG1BGjwf1ZsCxiMO5j
dYEPVfdPDLbBQtMD4VZlNb4ps2B6bExyLisOUxnlhEqdVn424EHIFRwNAV3eo0Gc
RrEGT4u57+Esqy9QQmvknJaA+oBFlzCpMLV3clQIm6ropbVtgqQtnLH19WJMfal3
nwB/v8Nle2XNQ7DJKwIDAQAB
-----END PUBLIC KEY-----
"""


JWT_EXPIRES_IN = int(os.getenv("JWT_EXPIRES_IN", default=600))
JWT_PRIVATE_KEY = os.getenv("JWT_PRIVATE_KEY", default=TEST_PRIVATE_KEY)
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", default="RS256")


def generate_auth_token(expires_in=JWT_EXPIRES_IN, **kwargs):
    payload = {
        "user_id": kwargs.get("user_id"),
        "email": kwargs.get("email"),
        "verified_mail": kwargs.get("verified_mail"),
        "roles": kwargs.get("roles"),
        "exp": time.time() + expires_in,
    }
    token = jwt.encode(
        payload=payload,
        key=JWT_PRIVATE_KEY,
        algorithm=JWT_ALGORITHM,
    )
    return token


def sign_jwt(
    user_id: str,
) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
    }
    token = generate_auth_token(**payload)
    return token
