# Extraction
```
Steps:
  1. Install Python.
  2. Create Virtual Env
  3. Install Requirements
  3. Use any Database in settings and Migrate
  4. Use Rabbit MQ or any Broker in Settings

```

To Run : 
To run server 
> ./manage.py runserver

> celery -A extraction worker -l info --queues=initiate_crawler


```
```
Completeness
- [x] Crawler
- [ ] Dashboard
