# Dogia REST API

Este é um projeto Django que implementa uma API REST para o sistema Dog.Ia. Ele funciona utilizando uma Rede Neural já treinada, a partir do trabalho [DogFaceNet](https://github.com/GuillaumeMougeot/DogFaceNet), para reconhecer a identidade de cães. O objetivo é aplicar a Rede Neural em um sistema real.

Esse projeto está em desenvolvimento

## Pré-requisitos

Certifique-se de ter os seguintes requisitos instalados antes de começar:

Django==4.2.13
django-cors-headers==4.3.1
django-cron==0.6.0
djangorestframework==3.15.1
numpy==1.26.4
opencv-python==4.9.0.80
pillow==10.3.0
psycopg2-binary==2.9.9
python-dotenv==1.0.1
tensorflow==2.15.0
scipy

## Configuração do Ambiente

1. Clone este repositório para o seu ambiente local.
2. Crie um ambiente virtual Python e ative-o:

```py
python -m venv myenv
source myenv/bin/activate (Linux/Mac)
myenv\Scripts\activate (Windows)
```

3. Instale as dependências necessárias

```py
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente no arquivo `.env`:

```py
SECRET_KEY=é fornecido pelo django
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port
DEBUG=True
```

Sicronizar as migrations do sistema com o seu banco local:
`python manage.py migrate`

Para criar o superuser da sua aplicação django
`python manage.py createsuperuser`


## Iniciando o Servidor de Desenvolvimento

Para iniciar o servidor de desenvolvimento, execute o seguinte comando:

```
python manage.py runserver
```

O servidor será iniciado em http://localhost:8000/.

## Endpoints da API

- `/api/usuarios/`: Endpoint para gerenciar usuários.
- `/api/cachorros/`: Endpoint para gerenciar cachorros.
- `/api/imagens/`: Endpoint para gerenciar imagens de cachorros.

- Os endpoints que começam `/api` são relativos a api desenvolvida
- `/admin`: acessa ao sistema de gerenciamento da aplicação do django, você faz o login com o seu superuser

## Front-end

O django também serve uma build do front-end Angular, disponivel no repositório [Dog.AI_app](https://github.com/BarbaraZamperete/Dog.IA)
Essa build esta no deirótio `dist/`, sendo que os arquivos estaticos da build devem começar com `/assets/`

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE.md para mais detalhes.
