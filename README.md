# upeem.org

Hello,
Bienvenue sur le site vitrine de l'UPEEM.

## Installation

Pour l'installation vous aurez besoin de virtualenv ou venv.

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements
```

Une fois l'installation du virtualenv terminé, il faut préparer le script pour les variables d'environnements.

```bash
touch scripts/.var.env.sh
```

TRES IMPORTANT: les fichiers finnissants en '.env.sh' ne seront pas synchronisés pour des questions de sécurité.

Pour la [secret key...](https://djecrety.ir/).

```bash
#!/bin/bash

source venv/bin/activate

export DEBUG="1"

export SECRET_KEY=""

export DB_NAME_DEV="name_dev"
export DB_NAME_TEST="name_test"

export DB_USER=""
export DB_PASSWORD=""
export DB_PORT=""
export DB_HOST="127.0.0.1"

export EMAIL_USER=""
export EMAIL_PASSWORD=""
export EMAIL_HOST=""
export EMAIL_PORT=""
export EMAIL_USE_TLS="1"

export ROOT_URLCONF="project.urls"
export DJANGO_SETTINGS_MODULE="project.settings.dev"

export ALLOWED_HOSTS="localhost 127.0.0.1 192.168.1.XXX"
```
