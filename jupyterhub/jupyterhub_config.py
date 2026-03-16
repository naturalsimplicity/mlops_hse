import os


c = get_config()

jupyterhub_port = int(os.environ.get('JUPYTERHUB_PORT', '8100'))
jupyterhub_hub_port = int(os.environ.get('JUPYTERHUB_HUB_PORT', '8101'))

c.JupyterHub.bind_url = f'http://0.0.0.0:{jupyterhub_port}'
c.JupyterHub.hub_bind_url = f'http://0.0.0.0:{jupyterhub_hub_port}'

c.JupyterHub.db_url = 'sqlite:///data/jupyterhub.sqlite'

cookie_secret = os.environ.get('JUPYTERHUB_COOKIE_SECRET', '')
if cookie_secret:
    c.JupyterHub.cookie_secret = bytes.fromhex(cookie_secret)

proxy_token = os.environ.get('JUPYTERHUB_CRYPT_KEY', '')
if proxy_token:
    c.ConfigurableHTTPProxy.auth_token = proxy_token

c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'

c.Authenticator.admin_users = {'admin'}
c.Authenticator.allowed_users = {'admin', 'user1', 'user2'}

c.JupyterHub.spawner_class = 'jupyterhub.spawner.LocalProcessSpawner'

c.Spawner.default_url = '/lab'

c.Spawner.environment = {
    'JUPYTERHUB_SINGLEUSER_APP': 'jupyter_server.serverapp.ServerApp',
}

c.Spawner.cmd = ['jupyterhub-singleuser']

c.Spawner.http_timeout = 180
c.Spawner.start_timeout = 180

c.JupyterHub.log_level = 'INFO'
c.Spawner.debug = True

c.JupyterHub.admin_access = True

c.ConfigurableHTTPProxy.should_start = True
c.ConfigurableHTTPProxy.api_url = 'http://127.0.0.1:8001'

c.JupyterHub.allow_named_servers = True

c.Spawner.notebook_dir = '~'

c.JupyterHub.tornado_settings = {
    'headers': {
        'Content-Security-Policy': "frame-ancestors 'self' *"
    }
}
