### Chang port and host
``` 
export FLASK_RUN_PORT=<port>
export FLASK_RUN_HOST=<host>
```

### Allow and disble firewall port
```
sudo ufw allow <port>
sudo ufw deny <port>
```

### ENV Active
```
python3 -m venv .venv
. .venv/bin/activate
```
### ENV Deactive
```
deactivate
```

### Package 
```
pip3 install Flask Flask-Cors
pip install flask-compress
```