CACHE_SEC=$1

python GCS.py -p infohub-780a5 -k gcs-keyfile.json -f index.html -d mainpage -n index.html -m text/html -c $CACHE_SEC
python GCS.py -p infohub-780a5 -k gcs-keyfile.json -f css/index.css -d mainpage/css -n index.css -m text/css -c $CACHE_SEC
