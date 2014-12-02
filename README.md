## Prerequisites ##

- python >= 2.5
- pip
- virtualenv/wrapper (optional)
- libxml2-dev libxslt-dev python-dev


## Installation ##
### Creating the environment ###
Create a virtual python environment for the project.
If you're not using virtualenv or virtualenvwrapper you may skip this step.

#### For virtualenvwrapper ####
```bash
mkvirtualenv --no-site-packages lita-env
```

#### For virtualenv ####
```bash
virtualenv --no-site-packages lita-env
cd lita-env
source bin/activate
```

### Clone the code ###
Obtain the url to your git repository.

```bash
git clone <URL_TO_GIT_RESPOSITORY> lita
```

### Install requirements ###
```bash
cd lita
pip install -r requirements.txt
```