#!/bin/bash

curl https://www.toronto.ca/app_content/homeless-help-respitesites/ | python -m json.tool > homeless-help-respitesites.json

curl https://www.toronto.ca/app_content/homeless-help-shelters/ | python -m json.tool > homeless-help-shelters.json

curl https://www.toronto.ca/app_content/homeless-help-meals/ | python -m json.tool > homeless-help-meals.json
