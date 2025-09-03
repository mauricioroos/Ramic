
# RAMIC (Django)

## Setup rápido (macOS + Anaconda)
1. conda create --name ramic_env python=3.9 -y
2. conda activate ramic_env
3. pip install -r requirements.txt
4. python manage.py makemigrations && python manage.py migrate
5. python manage.py createsuperuser
6. python manage.py runserver

Acesse /signup para criar conta, depois adicione motores e use Ligar/Desligar (logs automáticos).
