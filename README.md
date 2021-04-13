# Djangitos

Django Template for Saas projects.

Join our Discord server to get community and maintainers support: https://discord.gg/tZtrpD45TR

## Set up Process

1. ### Env File Creation
⋅⋅⋅ Create an env file (`.env`) file in the root of the project with the following content:

```
DATABASE_URL=postgresql://djangito:djangito@db/djangito
REDIS_URL=redis://redis/0
DJANGO_SECRET_KEY=123
DJANGO_DEBUG=True
```

2. ### `make build`

⋅⋅⋅ This command will install all the dependencies in [requirements.txt](requirements.txt) with `docker-compose build`.

⋅⋅⋅ After all dependencies are installed, this will run `python manage.py migrate`

⋅⋅⋅ Finally it will create a base Superuser (if None exists) with the following data:

    ⋅⋅* First Name: Admin
    ⋅⋅* Last Name: User
    ⋅⋅* Email: admin@example.com
    ⋅⋅⋅* Password: adminpass

**We Recommend changing the User password once the set up is completed.**

---

## Run the project

### `make run`

This command will run `docker-compose up` and will run your django server in the URL: `localhost:8060`.

---

More available commands in [Makefile](Makefile)
