# Djangitos

Django Project Template.

Join our Discord server to get community and maintainers support: https://appliku.com/discord


## Quickstart
Download fresh Djangitos project template, rename the project folder and copy local development `.env` file.

```bash
curl -sSL https://github.com/appliku/djangitos/archive/refs/heads/master.zip > djangitos.zip
unzip djangitos.zip


mv djangitos-master myproject
cd myproject
cp start.env .env
```

Run the project with:
```bash
docker-compose up
```

Apply migrations with:
```bash
docker-compose run web python manage.py migrate
```

Create a superuser account:
```bash
docker-compose run web python manage.py makesuperuser
```

The output of the last command will display the login and password for the admin user that was created, like this:

```
admin user not found, creating one
===================================
A superuser was created with email admin@example.com and password xLV9i9D7p8bm
===================================
```

Open [http://0.0.0.0:8060/admin/](http://0.0.0.0:8060/admin/) and login with these credentials.


## Tailwind
`Django-tailwind` is included. Hot-reload is disabled, but when `tailwind` docker-compose process is running it will
update the styles.css file when .html files are updated.

In order to set up tailwind for local development you should run `docker-compose run web python manage.py tailwind install`

