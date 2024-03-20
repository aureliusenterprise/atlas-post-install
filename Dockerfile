from python:3.11

env NAMESPACE="demo"

workdir /usr/src/app

copy requirements.txt ./

run pip install --no-cache-dir -r requirements.txt

copy *.py ./

copy *.sh ./

cmd ["./run.sh"]
