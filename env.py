from pyenvloadermeta import EnvLoaderMeta


class Env(metaclass=EnvLoaderMeta):
    REF_ID: str
    SESSION_NAME: str
    API_ID: int
    API_HASH: str
    MIN_POINTS: int
    MAX_POINTS: int
