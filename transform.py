# Python3 data mapper from Toronto City Homeless Help APIs
# https://www.toronto.ca/community-people/housing-shelter/homeless-help/
# to CSV files.

import csv
import json
import sys

# Ordered list of tuples of raw field name to transformed field name
# that we want in the CSV file. Optionally, third item is a lambda
# function to transform from raw to trasnformed if it's not just
# changing the key name for a string value.
shelters_field_mappings = [
    ('address', 'address'),
    ('eligibility', 'eligibility', lambda eligibilities: ','.join(e for e in eligibilities)),
    ('eligibilityNotes', 'eligibility_notes'),
    #('fid', 'fid'),  # do we want/need this?
    ('hours', 'hours'), # TODO try to parse and normalize these to a better format?
    ('latitude', 'latitude'),
    ('longitude', 'longitude'),
    ('orgName', 'organization_name'),
    ('programName', 'program_name'),
    ('services', 'services'),
    ('email', 'email'),
    ('phone', 'phone_number'),
    ('web', 'website'),
]

respitesites_field_mappings = [
    ('address', 'address'),
    ('capacity', 'capacity'),
    ('eligibility', 'eligibility', lambda eligibilities: ','.join(e for e in eligibilities)),
    ('eligibilityNotes', 'eligibility_notes'),
    #('fid', 'fid'),  # do we want/need this?
    ('hours', 'hours'), # TODO try to parse and normalize these to a better format?
    ('latitude', 'latitude'),
    ('longitude', 'longitude'),
    ('orgName', 'organization_name'),
    ('programName', 'program_name'),
    ('service', 'service'),
    ('email', 'email'),
    ('phone', 'phone_number'),
    ('web', 'website'),
]

meals_field_mappings = [
    ('address', 'address'),
    ('eligibility', 'eligibility', lambda eligibilities: ','.join(e for e in eligibilities)),
    ('eligibilityNotes', 'eligibility_notes'),
    ('hours', 'hours'), # TODO try to parse and normalize these to a better format?
    ('latitude', 'latitude'),
    ('longitude', 'longitude'),
    ('orgName', 'organization_name'),
    ('programName', 'program_name'),
    ('services', 'services'),
    ('email', 'email'),
    ('phone', 'phone_number'),
    ('web', 'website'),
    ('monday_meals', 'monday_meals', lambda meals: ','.join(m for m in meals)),
    ('tuesday_meals', 'tuesday_meals', lambda meals: ','.join(m for m in meals)),
    ('tuesday_meals', 'tuesday_meals', lambda meals: ','.join(m for m in meals)),
    ('wednesday_meals', 'wednesday_meals', lambda meals: ','.join(m for m in meals)),
    ('thursday_meals', 'thursday_meals', lambda meals: ','.join(m for m in meals)),
    ('friday_meals', 'friday_meals', lambda meals: ','.join(m for m in meals)),
    ('saturday_meals', 'saturday_meals', lambda meals: ','.join(m for m in meals)),
    ('sunday_meals', 'sunday_meals', lambda meals: ','.join(m for m in meals)),
]

def transform_record(record, field_mappings):
    '''Transform the raw form of a shelter dictionary to one with the
       field names that we want in the CSV file.'''
    # make sure we have all fields
    for fm in field_mappings:
        if fm[0] not in record:
            raise Exception("Field '" + fm[0] + "' not found in record " + str(record))

    transformed = {}
    for fm in field_mappings:
        if len(fm) == 2:
            transformed[fm[1]] = record[fm[0]]
        elif len(fm) == 3:
            mapper_func = fm[2]
            transformed[fm[1]] = mapper_func(record[fm[0]])
        else:
            raise Exception("Bad length " + str(len(fm)) + " on field mapping " + str(fm))
    return transformed

# `records` is 
def csvify_records(records, field_mappings, output_file_handle):
    '''`records` is a list of raw record dictionaries (usually from `parsed_data['data']`)
       `field_mappings` is a list of tuples of the form:
            (raw_field_name,
             transformed_field_name,
             function transforming the raw value to the transformed one) # last one optional
       `output_field_handle` is any writeable file, including sys.stdout.'''
    csv_fieldnames = [fm[1] for fm in field_mappings]
    writer = csv.DictWriter(output_file_handle, csv_fieldnames, dialect=csv.excel_tab)
    writer.writeheader()
    for r in records:
        writer.writerow(transform_record(r, field_mappings))


# Data from https://www.toronto.ca/app_content/homeless-help-shelters/
with open('homeless-help-shelters.json', 'r') as shelters:
    shelters_parsed = json.loads(shelters.read())

with open('homeless-help-shelters.csv', 'w') as shelters_csv:
    csvify_records(shelters_parsed['data'], shelters_field_mappings, shelters_csv)


# Data from https://www.toronto.ca/app_content/homeless-help-respitesites/
with open('homeless-help-respitesites.json', 'r') as respitesites:
    respitesites_parsed = json.loads(respitesites.read())

with open('homeless-help-respitesites.csv', 'w') as respitesites_csv:
    csvify_records(respitesites_parsed['data'], respitesites_field_mappings, respitesites_csv)


# Data from https://www.toronto.ca/app_content/homeless-help-meals/
with open('homeless-help-meals.json', 'r') as meals:
    meals_parsed = json.loads(meals.read())

with open('homeless-help-meals.csv', 'w') as meals_csv:
    csvify_records(meals_parsed['data'], meals_field_mappings, meals_csv)
