# PoC: Warm Data

## Pieces involved

There is 2 features involved in this PoC: schemas and inheritance

### Schemas

By default, users use schema `public`, but this behaviour is configured with a variable called `search_path`.

This variable works like PATH in shell: it searchs for an object in order.

### Inheritance

PostgreSQL has a feature called inheritance. This feature is the base for table partitioning, but here it's used in a more limited fashion.

## Putting them together

  +-------------+
  |warm.waypoint| // When you select from here, you select data from both tables
  +-------------+
       ^
       |
 +---------------+
 |public.waypoint| // When you select from here, you get data only from this table
 +---------------+

There is 2 database connections, one with the default `public` schema in the `search_path`, and the other with `warm,public` in the `search_path`

## Show me the code

```
docker-compose up -d --build
docker-compose exec web bash

./manage.py shell

from waypoint.models import *
hot = Waypoint.objects.all()
# warm includes data both hot and warm
warm = Waypoint.objects.using("warm").all()

for i in hot:
    print(i)
# returns:
# WAYPOINT[ID=3,CREATED=2020-06-19 22:59:50.124056+00:00,UPDATED=2020-06-19 22:59:50.124056+00:00,DESCRIPTION=hot data]
# WAYPOINT[ID=4,CREATED=2020-06-19 22:59:55.546319+00:00,UPDATED=2020-06-19 22:59:55.546319+00:00,DESCRIPTION=another hot data]
for i in warm:
    print(i)
# returns:
# WAYPOINT[ID=1,CREATED=2019-06-19 22:59:28.725026+00:00,UPDATED=2019-06-19 22:59:28.725026+00:00,DESCRIPTION=warm data]
# WAYPOINT[ID=3,CREATED=2020-06-19 22:59:50.124056+00:00,UPDATED=2020-06-19 22:59:50.124056+00:00,DESCRIPTION=hot data]
# WAYPOINT[ID=4,CREATED=2020-06-19 22:59:55.546319+00:00,UPDATED=2020-06-19 22:59:55.546319+00:00,DESCRIPTION=another hot data]
```

