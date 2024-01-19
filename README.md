#Benötigt Redis 
sudo apt-get install redis

#Benötigt ffmpeg
sudo apt install ffmpeg

#Benötigt .env Datei mit folgenden Variablen
DJANGO_SECRET = 'your-secret'

MAIL_HOST = ''

EMAIL_USE_TLS = True

EMAIL_PORT = 587

EMAIL_HOST_USER = ''

EMAIL_HOST_PASSWORD = ''

CACHES_PW = 'dein-pw'

QUEUES_PW = 'dein-opw'
