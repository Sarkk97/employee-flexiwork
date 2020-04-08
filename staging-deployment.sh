rsync -vzrh . root@185.130.207.215:/var/www/PYTHON/flexiwork_backend/temp

ssh root@185.130.207.215 <<-EOF
    cd /var/www/PYTHON/flexiwork_backend
    rm -rf ./backup # Delete previous backup
    mv ./live ./backup # Create new backup
    mv ./temp ./live
    mkdir ./temp # create new temp directory for next deployment
    cd ./live
    cp ../.env .
    
    
    # Install virtual env
    python3 -m venv .virtualenv

    # Activate virtual environment
    source .virtualenv/bin/activate
    
    # upgrade pip
    pip install --upgrade pip

    # Install dependencies
    pip install -r requirements.txt

    # Create migrations
    python manage.py makemigrations --settings=flexiwork.settings.staging
    python manage.py migrate --settings=flexiwork.settings.staging

    # deactivate virtual environment
    deactivate

    # Restart gunicorn to create socket
    systemctl restart flexiwork-gunicorn
EOF