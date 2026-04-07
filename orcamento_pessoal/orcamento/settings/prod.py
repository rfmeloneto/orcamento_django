import os
from decouple import Config, RepositoryEnv
from .base import *

env_path = os.path.join(BASE_DIR, '.env')
config = Config(RepositoryEnv(env_path))

DEBUG = False

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

STATIC_ROOT = '/home/raimundo/orcamento_django/orcamento_pessoal/staticfiles'