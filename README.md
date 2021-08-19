#Test case #1

Install dependencies
> pip install -r requirements.txt

Change settings in settings.py for your database and run migrations
> python manage.py makemigrations
 
> python manage.py migrate

Change setting (if needed) for RQ (RQ_QUEUES in settings.py) and run worker
> python manage.py rqworker default

Than run server
> pyhton magage.py runserver

### Methods
#### Add new URL to parse
> POST /tc
> with json {"url":"http://url_to_parse/"}
#### Check statuc
> GET /tc/{id}
> Returns result
