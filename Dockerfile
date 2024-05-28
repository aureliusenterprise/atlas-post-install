from aureliusatlas/docker-flink:2.1.45

user root

run apt-get update
run apt-get install -y jq curl

user flink

copy requirements.txt ./

run python -m pip install --no-cache-dir -r requirements.txt

copy *.py ./

copy *.sh ./

copy data/* ./data/

cmd ["./run.sh"]
