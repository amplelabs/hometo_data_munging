Scripts for working with data provided on the City of Toronto website about Homeless Help:

https://www.toronto.ca/community-people/housing-shelter/homeless-help/

This is part of work affiliated with http://hometo.io/ (defunct)

## How to run the scripts

Pre-requisites installed in user's machine:
- bash
- curl
- python3

First download JSON files from Toronto website:

```bash
./collect_data.sh
```

This step will create the following files:
- `homeless-help-meals.json`
- `homeless-help-respitesites.json`
- `homeless-help-shelters.json`

Then convert the JSON to CSV by running:

```bash
python3 transform.py
```

This step will create the following files:
- `homeless-help-meals.csv`
- `homeless-help-respitesites.csv`
- `homeless-help-shelters.csv`
