#
# This script compiles the HTTP injection rules into a CSV
# readable by multiple products.
#
# Author: Damien MOLINA
#
# 2024-09-30: First version of the script
#
import rules
import csv
import os

# The current directory hosting the script.
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

# In which files the rules will be set.
OUTPUT_FILE = os.path.join(CURRENT_DIR, '../outputs/rules.csv')

# Encode the rule in the Hexadecimal format to avoid
# issues with string interpretations.
def encode_rule(rule: str):
    return rule.encode("utf-8").hex()

# Get the row-representation of the given parameters.
def rule_as_row(type, id, rule):
    return {
        "rule_type": type,
        "rule_id": id,
        "rule": encode_rule(rule),
    }

# Convert rules to a CSV row.
def rules_as_rows(type: str, rules: dict):
    rows = []

    for rule_id in rules:
        rows.append(rule_as_row(type, rule_id, rules[rule_id]))

    return rows


with open(OUTPUT_FILE, 'w') as fd:
    # Open the file as a CSV.
    writter = csv.DictWriter(fd, fieldnames=['rule_type', 'rule_id', 'rule'])

    # Before writting the header, we will add some metadata regarding the rules.
    fd.write("# Version: " + str(rules.version) + "\n")

    # Then, we can add the header.
    writter.writeheader()

    # Write all the rules.
    for rule_type in rules.EXPORTED_RULES:
        writter.writerows(rules_as_rows(type=rule_type, rules=rules.EXPORTED_RULES[rule_type]))
