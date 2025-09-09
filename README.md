Preconfig:
----------
Please set USER,PASSWD and HOST in settings file to read and load netflow data from cisco router! then 
run `python manage.py migrate` and  `python manage.py runserver`.

How to Use:
----------
you can use `[server_IP]/[router_IP]/[Number_of_X_Point]/[Sleep_Time_between_Point]` to read netflow data from router!

Router config:
----------
before use this active netflow in router  like `ip flow ingress`
