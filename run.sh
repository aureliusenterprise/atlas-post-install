#!/usr/bin/env bash

set -e

python init_app_search_engines.py
python init_atlas_types.py

if [[ "$UPLOAD_DATA" == "true" ]]
then
    echo "Uploading sample data..."
    ./upload_sample_data.sh
else
    echo "Skipping uploading sample data."
fi
