# Production Engineering - Week 1 - Portfolio Site

Welcome to the MLH Fellowship! During Week 1, you'll be using Flask to build a portfolio site. This site will be the foundation for activities we do in future weeks so spend time this week making it your own and reflect your personality!

## Tasks

Once you've got your portfolio downloaded and running using the instructions below, you should attempt to complete the following tasks.

For each of these tasks, you should create an [Issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues) and work on them in a new [branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches). When the task has been completed, you should open a [Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) and get another fellow in your pod to give you feedback before merging it in.

*Note: Make sure to include a link to the Issue you're progressing on inside of your Pull Request so your reviewer knows what you're progressing on!*

### GitHub Tasks
- [x] Create Issues for each task below
- [x] Progress on each task in a new branch
- [x] Open a Pull Request when a task is finished to get feedback

### Portfolio Tasks
- [x] Add a photo of yourself to the website
- [x] Add an "About youself" section to the website.
- [x] Add your previous work experiences
- [x] Add your hobbies (including images)
- [x] Add your current/previous education
- [x] Add a map of all the cool locations/countries you visited

### Flask Tasks
- [x] Get your Flask app running locally on your machine using the instructions below.
- [x] Add a template for adding multiple work experiences/education/hobbies using [Jinja](https://jinja.palletsprojects.com/en/3.0.x/api/#basics)
- [x] Create a new page to display hobbies.
- [x] Add a menu bar that dynamically displays other pages in the app


## Getting Started

You need to do all your progress here.

## Installation

Make sure you have python3 and pip installed.

**Python version:** use 3.11 or 3.12. The pinned Flask/Werkzeug 2.0.1 will not
run on Python 3.14 — Werkzeug 2.0.1 calls `ast.Str`, which was removed in 3.14
and raises `AttributeError: module 'ast' has no attribute 'Str'` at startup.

Create and activate virtual environment using virtualenv
```bash
$ python3.12 -m venv python3-virtualenv
$ source python3-virtualenv/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies!

```bash
pip install -r requirements.txt
```

### Database

The app needs a MySQL/MariaDB database. Install and start the server, then
create the database and user:

```bash
$ sudo dnf install mariadb-server        # or your distro's equivalent
$ sudo systemctl enable --now mariadb

$ sudo mariadb -e "
CREATE DATABASE IF NOT EXISTS myportfoliodb;
GRANT ALL PRIVILEGES ON myportfoliodb.* TO 'myportfolio'@'localhost';
FLUSH PRIVILEGES;
"
```

Create the tables (safe to re-run):
```bash
$ python scripts/init-db.py
```

## Usage

Create a .env file using the example.env template (make a copy using the variables inside of the template)

Start flask development server
```bash
$ export FLASK_ENV=development
$ flask run
```

You should get a response like this in the terminal:
```
❯ flask run
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

You'll now be able to access the website at `localhost:5000` or `127.0.0.1:5000` in the browser! 

*Note: The portfolio site will only work on your local machine while you have it running inside of your terminal. We'll go through how to host it in the cloud in the next few weeks!* 

## Deployment

The site runs behind nginx, with gunicorn supervised by systemd:

```
internet -> nginx (:80) -> gunicorn (127.0.0.1:5000) -> Flask
                                    ^
                           systemd (myportfolio.service)
```

Config files live in `deploy/`.

### gunicorn + systemd

```bash
$ sudo cp deploy/myportfolio.service /etc/systemd/system/
$ sudo systemctl daemon-reload
$ sudo systemctl enable --now myportfolio
```

On SELinux systems (Fedora/RHEL), systemd cannot execute binaries under a home
directory — they are labelled `user_home_t`, and the service fails with
`status=203/EXEC` and "Permission denied" even though the file is executable.
Relabel the virtualenv's `bin/` once:

```bash
$ sudo dnf install -y policycoreutils-python-utils
$ sudo semanage fcontext -a -t bin_t "$PWD/python3-virtualenv/bin(/.*)?"
$ sudo restorecon -Rv "$PWD/python3-virtualenv/bin"
```

The rule is persistent, so it survives rebuilding the virtualenv.

### nginx

```bash
$ sudo dnf install -y nginx
$ sudo cp deploy/myportfolio-nginx.conf /etc/nginx/conf.d/myportfolio.conf
$ sudo nginx -t
$ sudo systemctl enable --now nginx
```

If `nginx -t` reports a duplicate default server, comment out the stock
`server { ... }` block in `/etc/nginx/nginx.conf` — this config claims
`default_server` so the site answers on the machine's IP.

Allow nginx to make outbound connections to gunicorn, or every request returns
502 with nothing useful in the error log:

```bash
$ sudo setsebool -P httpd_can_network_connect 1
```

Open the firewall:

```bash
$ sudo firewall-cmd --permanent --add-service=http
$ sudo firewall-cmd --reload
```

### Redeploying

`scripts/redeploy-site.sh` pulls `origin/main`, reinstalls dependencies, applies
any new tables, and restarts gunicorn.

### Verifying

```bash
$ curl -I http://127.0.0.1/                          # expect 200, Server: nginx
$ BASE_URL=http://127.0.0.1 ./scripts/curl-test.sh   # exercises the API
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Run tests

To all tests use the following command:

```sh
python -m unittest discover -s tests -p "test_*.py" -v
```


To run specific test files, run:

```sh
python -m unittest -v tests.<file_name>

# For example
python -m unittest -v tests.test_db
```
