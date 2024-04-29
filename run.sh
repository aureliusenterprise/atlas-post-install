#!/usr/bin/env bash

set -e

python init_app_search_engines.py
python init_atlas_types.py

pushd /opt/flink/py_libs/flink_jobs/
/opt/flink/bin/flink run -d --jobmanager "$JOBMANAGER_URL" -py synchronize_app_search.py
/opt/flink/bin/flink run -d --jobmanager "$JOBMANAGER_URL" -py publish_state.py
popd

if [[ "$UPLOAD_DATA" == "true" ]]
then
    echo "Uploading sample data..."
    ./upload_sample_data.sh
else
    echo "Skipping uploading sample data."
fi
