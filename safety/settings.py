from os import environ 

SECRET_KEY = environ.get('SECRET_KEY','a64ad786-24f9-45c2-b441-afeaa46ff201')
SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI','sqlite:///intern.db')
SQLALCHEMY_TRACK_MODIFICATIONS=False
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = environ.get('MAIL_USER','InternshipMicrosoft1@gmail.com')
MAIL_PASSWORD = environ.get('MAIL_PASSWORD','eojswxvzkenauatv')
ADMIN_ID='17aa6348-5a9f-4ebd-9225-cbb0cd65982e'
RECAPTCHA_PUBLIC_KEY='6LfTdyUgAAAAALJkCVgq_2wMfYwpa7YmdSgW7PUo'
RECAPTCHA_PRIVATE_KEY='6LfTdyUgAAAAAMNrkU5cPUAfVJzUuHg0L_FMkgnk'
