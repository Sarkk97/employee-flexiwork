rsync -vzrh . root@185.130.207.215:/var/www/PYTHON/flexiwork_backend/temp

# ssh root@185.130.207.215 <<-EOF
#     cd /var/www/PYTHON/flexiwork_backend
#     rm -rf ./backup # Delete previous backup
#     mv ./live ./backup # Create new backup
#     mv ./temp ./live
#     mkdir ./temp # create new temp directory for next deployment
#     cd ./live
#     cp ../config/dbconfig.py ./atg_web
    

#     # Install virtual env
#     python3 -m venv .virtualenv

#     # Activate virtual environment
#     source .virtualenv/bin/activate

#     # upgrade pip
#     pip install --upgrade pip

#     # Install dependencies
#     pip install -r requirements.txt

#     # Create migrations (DONT MIGRATE !!! CONNECTION ON STAGING IS TO PROD BB)

#     # deactivate virtual environment
#     deactivate

#     # Restart gunicorn to create socket
#     systemctl restart gunicorn
# EOF