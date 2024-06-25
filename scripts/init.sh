#!/bin/bash

loc_path=`pwd`

alembic init migrations
wait

sed -i "s/^# from myapp import mymodel/from db.models import Base/" ./migrations/env.py
sed -i "s/target_metadata = None/target_metadata = Base.metadata/" ./migrations/env.py

alembic revision --autogenerate -m "init_db"
wait
alembic upgrade heads
wait

# cd tests

# export PYTHONPATH=$loc_path:$PYTHONPATH

# alembic init migrations
# wait

# sed -i "s/^# from myapp import mymodel/from db.models import Base/" ./migrations/env.py
# sed -i "s/target_metadata = None/target_metadata = Base.metadata/" ./migrations/env.py

# alembic revision --autogenerate -m "init_db"
# wait
# alembic upgrade heads
# wait