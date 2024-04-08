from python:3.11

env NAMESPACE="demo"

run apt update
run apt install -y jq curl

workdir /usr/src/app

copy requirements.txt ./

run pip install --no-cache-dir -r requirements.txt

copy *.py ./

copy *.sh ./

copy data/ ./data/

cmd ["./run.sh"]
