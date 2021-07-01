# foodgram-project
foodgram-project

project address: `130.193.41.205`

after workflow work finish make migrations

`sudo docker-compose exec web python manage.py migrate --noinput`

after that create superuser

`sudo docker-compose exec web python manage.py createsuperuser`

and collect static

`sudo docker-compose exec web python manage.py collectstatic --noinput`

for downloading cart you need to install wkhtmltopdf:
1. enter to web container

`sudo docker exec -it 'container_id' bash`
2. update apt

`apt update`
3. install wkhtmltopdf

`apt install wkhtmltopdf`
4. and exit

`exit`

Now if you want to test project you may fill db

`sudo docker-compose exec web python manage.py filldb`