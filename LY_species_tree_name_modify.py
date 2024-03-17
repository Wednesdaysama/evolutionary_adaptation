import os
import re

directory = os.getcwd()

for filename in os.listdir(directory):
    if filename.startswith("reroot") and filename.endswith(".txt"):
        species_name = []
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            content = file.read()
            matches = re.findall(r'(?:a|m|o)-[^:]+', content)
            species_name.extend(matches)

        for name in species_name:
            content = content.replace(name, f"{name}_{name}")
            newick = content

        newick_filename = os.path.splitext(filename)[0] + ".newick"
        newick_filepath = os.path.join(directory, newick_filename)
        with open(newick_filepath, 'w') as newick_file:
            newick_file.write(newick)

species_list_demo = []
for filename in os.listdir(directory):
    if filename.endswith("1.newick"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            double_name = file.read()
            double_name_matches = re.findall(r'(?:a|m|o)-[^:]+', double_name)
            species_list_demo.extend(double_name_matches)

species_list_demo_filepath = os.path.join(directory, "species_list_demo.txt")
with open(species_list_demo_filepath, 'w') as species_list_demo_file:
    for name in species_list_demo:
        species_list_demo_file.write(name + "\n")

roots_to_test = []
for filename in os.listdir(directory):
    if filename.startswith("reroot") and filename.endswith(".newick"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            content = file.read()
            roots_to_test.append(os.path.splitext(filename)[0])

roots_to_testfilepath = os.path.join(directory, "roots_to_test.txt")
with open(roots_to_testfilepath, 'w') as roots_to_test_file:
    for name in roots_to_test:
        roots_to_test_file.write(name + "\n")
