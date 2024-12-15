# 📝 [Blogicum](https://github.com/kopf8/django_sprint4.git)
### <br>➜ https://kopf.pythonanywhere.com/
<br><hr>

## Project tech stack:
- ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
- ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
- ![Django REST Framework](https://img.shields.io/badge/Django%20REST-092E20?style=for-the-badge&logo=django&logoColor=white)
- ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
- ![JSON](https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white)
- ![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white)

<br><hr>
## Project description:

![image](https://github.com/user-attachments/assets/862993b0-3439-4605-9693-6d208a790c4f)


"Blogicum" is a blogging platform. You can run your own blog, read blogs of other authors and comment on their posts. You can attach a photo to each post.
User registration and authorization has been implemented, and the ability to send emails with a registration code has been enabled.
There are three categories of users: regular, administrator and superuser.
The admin area also exists.
The administrator can edit posts and comments of other users, or remove them from publication. Posts can be sorted by authorship, by category, and by location. Pagination is implemented on the site.

### Project website:

[https://yandex-foodgram.hopto.org/](https://kopf.pythonanywhere.com/)
<br><br>
<hr>

## How to run the project:

Clone repository and switch to project directory using command line:

```
git clone git@github.com:kopf8/django_sprint4.git
```

```
cd django_sprint4
```

Create & activate virtual environment:

```
python -m venv .venv
```

* For Linux/macOS:

    ```
    source .venv/bin/activate
    ```

* For Win:

    ```
    source .venv/Scripts/activate
    ```

Upgrade pip:

```
python -m pip install --upgrade pip
```

Install project requirements from file _requirements.txt_:

```
pip install -r requirements.txt
```

Make & run migrations, fill DB with preset data from JSON file:

```
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata db.json
```

To launch server locally, use command:

```
python manage.py runserver
```
and your project will be accessible at `http://127.0.0.1:8000`
<br><hr>

## Project created by:
### [✍️ Maria Kirsanova](https://github.com/kopf8)
on the basis of initial draft project by [Yandex Practicum](https://github.com/yandex-praktikum/django_sprint4).
