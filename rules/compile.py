#
# This script compiles the HTTP injection rules into a CSV
# readable by multiple products.
#
# Author: Damien MOLINA
#
# 2024-09-30: First version of the script
# 2024-10-03: Generate CSV and JSON in the same script
#
import rules
import os

# The current directory hosting the script.
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = os.path.join(CURRENT_DIR, '../outputs/')

# Get the row-representation of the given parameters.
def rule_as_row(type, id, rule):
    return {
        "rule_type": type,
        "rule_id": id,
        "rule": str(rule).encode("utf-8").hex(),
    }

# Convert rules to a CSV row.
def rules_as_rows(type: str, rules: dict):
    rows = []

    for rule_id in rules:
        rows.append(rule_as_row(type, rule_id, rules[rule_id]))

    return rows

# Compile the rules in the CSV format.
def compile_csv():
    import csv

    with open(os.path.join(OUTPUT_DIR, 'rules.csv'), 'w') as fd:
        # Open the file as a CSV.
        writter = csv.DictWriter(fd, fieldnames=['rule_type', 'rule_id', 'rule'])

        # Before writting the header, we will add some metadata regarding the rules.
        fd.write("# Version: " + str(rules.version) + "\n")

        # Then, we can add the header.
        writter.writeheader()

        # Write all the rules.
        for rule_type in rules.EXPORTED_RULES:
            writter.writerows(rules_as_rows(type=rule_type, rules=rules.EXPORTED_RULES[rule_type]))

# Compile the rules in the JSON format.
def compile_json():
    import json

    # Get all the rules in a single array.
    http_rules = []
    for rule_type in rules.EXPORTED_RULES:
        http_rules = http_rules + rules_as_rows(type=rule_type, rules=rules.EXPORTED_RULES[rule_type])

    with open(os.path.join(OUTPUT_DIR, 'rules.json'), 'w') as fd:
        json.dump({
            "version": rules.version,
            "rules": http_rules
        }, fd, ensure_ascii=False, indent=4)


# Compile all the files.
compile_csv()
compile_json()