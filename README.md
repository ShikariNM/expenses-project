## Expense control[^1]  
*Project development is ongoing*

---

### The purpose

The project is intended to practice my programming skills and demonstrate them.

### Used technologies

- Python 3
- Django
- PostgreSQL
- Gunicorn
- Nginx
- Docker + Docker-compose
- Bootstrap

### Description

Firstly, a user must register and login to use the service. The project itself is quite simple.
It allows a user to CRUD[^2] their recipes and expenses for each recipe, CRUD their categories.
Every expense is assigned to one of categories. A user can watch their categories and respective
expenses filtered by chosen time period. Users can create their groups to unite with each other.
A group creator is an admin of a group. Every user can watch their own expense statistics and
expense statistics of each groupmate.

Nginx is used as reverse proxy server, Gunicorn is used as backend server. Nginx config file is
kept in the directory */deploy/nginx/*. Database is PostgreSQL.

### Deployment

Deployment automation is implemented with Docker + Docker-compose. Dockerfile and docker-compose.yml
are kept in the directory */deploy/*.  

You can deploy and try the project on your own server easily. To do this you need Git, Docker and
Docker-compose. If all of them are installed, follow the steps and execute in your console:

- `git clone https://github.com/ShikariNM/expenses-project.git`
- Create file *expenses-project/deploy/.env* and add the environment variables in it according to  
  *expenses-project/deploy/.env.example* or execute  
  `mv expenses-project/deploy/.env.example expenses-project/deploy/.env`
- `sudo docker compose -f expenses-project/deploy/docker-compose.yml up -d`
- `sudo docker compose -f expenses-project/deploy/docker-compose.yml run --rm web python manage.py migrate`

Now you can visit **127.0.0.1:80** and enjoy the application.

### Deinstallation

To remove all containers, images, volumes and local repo related to the project follow the steps
and execute in your console:

- `sudo docker compose -f expenses-project/deploy/docker-compose.yml down -v`
- `sudo docker rmi deploy-web nginx:1.26.3 postgres:17.2`
- `rm -rf expenses-project`  
  
  > Be attentive with nginx and postgres images. Ensure you don't need it before removal.

---

---

## Контроль расходов

*Разработка проекта продолжается*

---

### Предназначение

Проект предназначен для практики моих навыков программирования и их демонстрации.

### Используемые технологии

- Python 3
- Django
- PostgreSQL
- Gunicorn
- Nginx
- Docker + Docker-compose
- Bootstrap

### Описание

В первую очередь пользователь должен зарегистрироваться и авторизоваться в приложении. Сам по себе
проект довольно простой. Он дает пользователю возможность создавать, читать, изменять, удалять его
чеки и расходы для каждого чека, а также создавать, читать, изменять, удалять свои категории расходов.
Каждый расход относится к одной из категорий. Пользователь может отслеживать свои категории и 
соответствующие расходы, фильтруя их по временному интервалу. Пользователи могут создавать свои группы,
чтобы объединяться с другими пользователями. Создатель группы становится администратором группы.
Каждый пользователь может следить за своей статистикой расходов и статистикой расходов участников
групп, в которых состоит.

Nginx используется как обратный прокси сервер, Gunicorn - как бэкенд сервер. Файл конфигурации
Nginx располагается в директории */deploy/nginx/*. В качестве базы данных используется PostgreSQL.

### Развертывание

Автоматизация развертывания реализована при помощи Docker + Docker-compose. Dockerfile и docker-compose.yml
располагаются в директории */deploy/*.

Вы можете развернуть и испытать проект на своем собственном сервере. Для этого вам понадобятся Git, Docker
и Docker-compose. Если все перечисленное установлено, следуйте инструкциям и выполните в консоли:

- `git clone https://github.com/ShikariNM/expenses-project.git`
- Создайте файл *expenses-project/deploy/.env* и добавьте в него переменные окружения в соответствии с  
  *expenses-project/deploy/.env.example*, или выполните:  
  `mv expenses-project/deploy/.env.example expenses-project/deploy/.env`
- `sudo docker compose -f expenses-project/deploy/docker-compose.yml up -d`
- `sudo docker compose -f expenses-project/deploy/docker-compose.yml run --rm web python manage.py migrate`

Теперь вы можете посетить **127.0.0.1:80** и насладиться приложением.

### Удаление

Чтобы удалить все контейнеры, образы, тома и локальный репозиторий, относящиеся к проекту, следуйте
инструкциям и выполните в консоли:

- `sudo docker compose -f expenses-project/deploy/docker-compose.yml down -v`
- `sudo docker rmi deploy-web nginx:1.26.3 postgres:17.2`
- `rm -rf expenses-project`  

  > Будьте внимательны к образам nginx и postgres. Перед удалением убедитесь, что они вам не нужны.

[^1]: Описание на русском языке ниже.  
[^2]: Create, Read, Update, Delete.
