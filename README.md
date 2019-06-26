# GLUG MVIT
<hr>

## Running the website on your localhost

```bash
> python3 -m virtualenv glug_env      # Create a virtual environment.
> cd glug_env                         
> git clone https://github.com/glugmv/glugmv_website.git  # Cloning the repository
> cd glugmv_website
> cd glug
> pip3 install -r requirements.txt     # Installing the requirements
> python3 manage.py makemigrations
> python3 manage.py migrate
> python3 manage.py runserver          # Running the server on the localhost
```
