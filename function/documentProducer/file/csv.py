import csv


def parse(lines) -> list:
    """ Convert every empty string 'cell' to None and put each line in it's own list """
    modified_lines = []

    reader = csv.reader(lines)
    for row in reader:
        for i in range(len(row)):
            if not row[i].strip():
                row[i] = None
        modified_lines.insert(len(modified_lines), row)

    return modified_lines
