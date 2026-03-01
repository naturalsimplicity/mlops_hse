import os
import sys

# Базовая конфигурация
c = get_config()  # noqa

# Сетевые настройки
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000

# База данных
postgres_user = os.environ.get('POSTGRES_USER', 'jupyterhub_user')
postgres_password = os.environ.get('POSTGRES_PASSWORD', 'password')
postgres_host = os.environ.get('POSTGRES_HOST', 'postgres')
postgres_db = os.environ.get('POSTGRES_DB', 'jupyterhub')

c.JupyterHub.db_url = f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}'

# Секреты
c.JupyterHub.cookie_secret_file = '/srv/jupyterhub/data/jupyterhub_cookie_secret'
c.ConfigurableHTTPProxy.auth_token = os.environ.get('JUPYTERHUB_CRYPT_KEY', '')

# Аутентификация - использование простого аутентификатора для демо
c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'

# Администраторы
c.Authenticator.admin_users = {'admin'}
c.Authenticator.allowed_users = {'admin', 'user1', 'user2'}

# Spawner - используем LocalProcessSpawner для простоты
c.JupyterHub.spawner_class = 'jupyterhub.spawner.SimpleLocalProcessSpawner'

# Настройка Spawner
c.Spawner.default_url = '/lab'
c.Spawner.cmd = ['jupyter-labhub']

# Тайм-ауты
c.Spawner.http_timeout = 120
c.Spawner.start_timeout = 120

# Логирование
c.JupyterHub.log_level = 'INFO'
c.Spawner.debug = True

# Разрешить создание пользователей
c.LocalAuthenticator.create_system_users = False

# Директории
c.Spawner.notebook_dir = '~'

# Административная панель
c.JupyterHub.admin_access = True

# Прокси
c.ConfigurableHTTPProxy.command = ['configurable-http-proxy']
