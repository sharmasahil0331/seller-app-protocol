import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    OTP_TIMEOUT_IN_MINUTES = 60
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    COOKIE_EXPIRY = 60000
    PORT = 9900
    FLASKS3_BUCKET_NAME = os.getenv('static_bucket_name')
    FLASKS3_FILEPATH_HEADERS = {r'.css$': {'Content-Type': 'text/css; charset=utf-8'},
                                r'.js$': {'Content-Type': 'text/javascript'}}
    FLASKS3_ACTIVE = os.getenv("flask_s3_active", "True") == "True"
    FLASKS3_GZIP = True
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    JWT_TOKEN_LOCATION = ['headers']
    S3_PRIVATE_BUCKET = os.getenv("PRIVATE_BUCKET")
    # below is valid for tokens coming in as part of query_params
    JWT_QUERY_STRING_NAME = "token"
    # Set the secret key to sign the JWTs with
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    DOMAIN = "nic2004:52110"
    CITY_CODE = "std:080"
    COUNTRY_CODE = "IND"
    BAP_TTL = "20"
    BECKN_SECURITY_ENABLED = False
    BPP_PRIVATE_KEY = os.getenv("BPP_PRIVATE_KEY", "some-key")
    BPP_PUBLIC_KEY = os.getenv("BPP_PUBLIC_KEY", "some-key")
    BPP_ID = os.getenv("BPP_ID", "sellerapp-staging.datasyndicate.in")
    BPP_URI = os.getenv("BPP_URI", "https://sellerapp-staging.datasyndicate.in/")
    BPP_UNIQUE_KEY_ID = os.getenv("BPP_UNIQUE_KEY_ID", "351")
    RABBITMQ_QUEUE_NAME = os.getenv("BPP_UNIQUE_KEY_ID", "bpp_protocol")
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
    BPP_CLIENT_ENDPOINT = os.getenv("BPP_CLIENT_ENDPOINT", "client")
    BG_DEFAULT_URL = os.getenv("BG_DEFAULT_URL", "https://pilot-gateway-1.beckn.nsdl.co.in/")
    BG_DEFAULT_URL_FLAG = os.getenv("BG_DEFAULT_URL_FLAG", "True") == "True"


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = True
    RABBITMQ_HOST = "localhost"
    REGISTRY_BASE_URL = "https://pilot-gateway-1.beckn.nsdl.co.in"


class ProductionConfig(Config):
    DEBUG = False
    RABBITMQ_HOST = "rabbitmq"
    REGISTRY_BASE_URL = "https://pilot-gateway-1.beckn.nsdl.co.in"


class PreProductionConfig(Config):
    DEBUG = False
    RABBITMQ_HOST = "rabbitmq"
    REGISTRY_BASE_URL = "https://preprod.registry.ondc.org/ondc"


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig,
    pre_prod=PreProductionConfig,
)

key = Config.SECRET_KEY


def get_config_by_name(config_name, default=None, env_param_name=None):
    config_env = os.getenv(env_param_name or "ENV")
    config_value = default
    if config_env:
        config_value = getattr(config_by_name[config_env](), config_name, default)
    return config_value


def get_email_config_value_for_name(config_name):
    email_config_value = get_config_by_name("SES") or {}
    config = email_config_value.get(config_name)
    return config
