<b>#Benötigt Redis </b>

sudo apt-get install redis

<b>#Benötigt ffmpeg</b>

sudo apt install ffmpeg

<b>#Benötigt .env Datei mit folgenden Variablen</b>

DJANGO_SECRET = 'your-secret'

MAIL_HOST = ''

EMAIL_USE_TLS = True

EMAIL_PORT = 587

EMAIL_HOST_USER = ''

EMAIL_HOST_PASSWORD = ''

CACHES_PW = 'dein-pw'

QUEUES_PW = 'dein-opw'
