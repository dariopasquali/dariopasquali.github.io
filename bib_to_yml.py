import bibtexparser
import yaml
import re

def convert_latex_to_html(text):
    bold_pattern = re.compile(r'\\textbf\{(.*?)\}')
    return bold_pattern.sub(r'<b>\1</b>', text)

# Function to parse Biblatex file and convert to YAML
def generate_yaml_publications(bib_file_path):
    # Read the Biblatex file
    with open(bib_file_path, 'r') as bib_file:
        bib_database = bibtexparser.load(bib_file)

    journals = [bib for bib in bib_database.entries if bib['ENTRYTYPE'] == 'article']
    conferences = [bib for bib in bib_database.entries if bib['ENTRYTYPE'] == 'inproceedings']
    events = [bib for bib in bib_database.entries if bib['ENTRYTYPE'] == 'misc']
    
    journals_yaml = []
    conferences_yaml = []
    events_yaml = []

    # Parse the YAML
    for pubs in [journals, conferences, events]:
        for p in pubs:
            # Remove the and
            p['author'] = p['author'].replace(" and ", ", ")            
            # \textbf{} to <b></b>
            for field in p.keys():
                p[field] = convert_latex_to_html(p[field])
                p[field] = p[field].replace("{", "")
                p[field] = p[field].replace("}", "")
                p[field] = p[field].replace("\n", "")
                p[field] = p[field].replace("\\\\", "")
            
    journals_yaml = [{
                    "title": jj['title'],
                    "authors": jj['author'],
                    "journal": jj['journal'],
                    "year": jj['year'],
                    "doi": (f"https://doi.org/{jj['doi']}" if "doi" in jj and "http" not in jj['doi'] 
                        else jj['doi'] if "doi" in jj 
                        else "")
                    } for jj in journals]
    
    conferences_yaml = [{
                    "title": jj['title'],
                    "authors": jj['author'],
                    "journal": jj['booktitle'],
                    "year": jj['year'],
                    "doi": (f"https://doi.org/{jj['doi']}" if "doi" in jj and "http" not in jj['doi'] 
                        else jj['doi'] if "doi" in jj 
                        else "")
                    } for jj in conferences]
    
    events_yaml = [{
                    "title": jj['title'],
                    "authors": jj['author'],
                    "journal": f"{jj['booktitle']} - {jj['address']}",
                    "year": jj['year'],
                    "doi": (f"https://doi.org/{jj['doi']}" if "doi" in jj and "http" not in jj['doi'] 
                        else jj['doi'] if "doi" in jj 
                        else "")
                    } for jj in events]
    

    # Write the list of dictionaries to a YAML file
    with open("_data/journals.yml", 'w') as yaml_file:
        yaml.dump(journals_yaml, yaml_file, default_flow_style=False)
        
    # Write the list of dictionaries to a YAML file
    with open("_data/conferences.yml", 'w') as yaml_file:
        yaml.dump(conferences_yaml, yaml_file, default_flow_style=False)
        
    # Write the list of dictionaries to a YAML file
    with open("_data/events.yml", 'w') as yaml_file:
        yaml.dump(events_yaml, yaml_file, default_flow_style=False)
        
    
generate_yaml_publications("latex/sample.bib")