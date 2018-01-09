### Description

This import script takes data from the old database structure of theblacksea.eu 
(and sites built on the same platform) and generates Django / Wagtail seed 
files, according to the [Blacktail project](https://github.com/CRJI/theblacksea.eu)
models specifications.


### Setup

```
$ mkvirtualenv tbs-importer
$ workon tbs-importer    # If not activated automatically
$ pip install -r requirements.txt
```

Next you need to set up your source database credentials.

### Usage

```
$ python import.py <model> [output file]
```

The model name is required, you can find the available options in import.py. 
File name is either made up by combining model name and '.json', or specified 
as a second argument at runtime.

E.g. `python import.py stories ../fixtures/stories.json`

### Loading data into Blacktail

`python manage.py loaddata <fixture name>`

e.g.

`python manage.py loaddata stories`
