"""
creds https://redis.readthedocs.io/en/stable/examples/connection_examples.html        
"""

from typing import overload
from functools import wraps
from redis import Redis
from redis.exceptions import AuthenticationError
import json


class RS:
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        password: str,
        username=None,
        ssl=False,
        ssl_cert_reqs="none",
        protocol=2,
    ):
        self.host = host
        self.port = port
        self.db = db
        self.username = username
        self.password = password
        self.protocol = protocol
        self.ssl = ssl
        self.ssl_cert_reqs = ssl_cert_reqs
        self.conn = None

    def connect(self):
        self.conn = Redis(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            db=self.db,
            protocol=self.protocol,
            ssl=self.ssl,
            ssl_cert_reqs=self.ssl_cert_reqs,
            decode_responses=True,
        )
        return self.check_connection()

    def check_connection(self):
        try:
            return self.conn.ping(), "okay"
        except (AttributeError, AuthenticationError) as err_msg:
            return False, err_msg

    def set(self, key, value):
        if not self.conn:
            self.connect()
        assert not isinstance(self.conn, type(None))
        return self.conn.set(key, value)

    def mset(self, value):
        """value : dict"""
        if not self.conn:
            self.connect()
        return self.conn.mset(value)

    @overload
    def get(self, key: str):
        """key: str"""
        ...

    @overload
    def get(self, key: list):
        """keys: list"""
        ...

    def get(self, key):
        if not self.conn:
            self.connect()
        if not isinstance(key, (str, list)):
            raise KeyError("as key supports only str or list")
        return self.conn.mget(key) if isinstance(key, list) else self.conn.get(key)

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def get_cache(self, func):
        """decorator"""
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            key_parts = [func.__name__] + list(args)
            key = "-".join(key_parts) + ": " + str(sorted(kwargs.items()))

            if self.check_connection()[0]:
                result = self.get(key)
                if result is not None:
                    return result
            value = func(*args, **kwargs)
            if value:
                self.set(key, json.dumps(value))
            return value
            
        return wrapper
