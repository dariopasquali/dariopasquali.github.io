import yaml
import re
import os

def bold_html_to_latex(text):
    bold_pattern = re.compile(r'<b>(.*?)</b>', re.IGNORECASE)
    return bold_pattern.sub(r'\\textbf{\1}', text)
  
def italic_html_to_latex(text):
    bold_pattern = re.compile(r'<i>(.*?)</i>', re.IGNORECASE)
    return bold_pattern.sub(r'\\textit{\1}', text)
  
def filter_links(text):
    a_tag_pattern = re.compile(r'<a\b[^>]*>(.*?)<\/a>', re.IGNORECASE)
    return a_tag_pattern.sub(r'\1', text)

def markdown_to_latex(text):
  text = text.replace("&", "\&")
  text = text.replace("<br>", "\\\\")
  text = bold_html_to_latex(text)
  text = italic_html_to_latex(text)
  text = filter_links(text)
  return text
  

latex_head = """
\\documentclass[10pt,a4paper,ragged2e]{altacv}
\\geometry{left=2cm,right=10cm,marginparwidth=6.8cm,marginparsep=1.2cm,top=1.25cm,bottom=1.25cm}
\\ifxetexorluatex
  \\setmainfont{Carlito}
\\else
  \\usepackage[utf8]{inputenc}
  \\usepackage[T1]{fontenc}
  \\usepackage[default]{lato}
\\fi
\\usepackage[utf8]{inputenc}
\\definecolor{VividPurple}{HTML}{000000}
\\definecolor{SlateGrey}{HTML}{2E2E2E}
\\definecolor{LightGrey}{HTML}{2E2E2E}
\\colorlet{heading}{VividPurple}
\\colorlet{accent}{VividPurple}
\\colorlet{emphasis}{SlateGrey}
\\colorlet{body}{LightGrey}
\\renewcommand{\\itemmarker}{{\\small\\textbullet}}
\\renewcommand{\\ratingmarker}{\\faCircle}
\\addbibresource{sample.bib}

\\usepackage{fancyhdr}
\\pagestyle{fancy}      % Set the page style to fancy
\\fancyhf{}             % Clear the default header and footer
\\fancyfoot[C]{\small \\textit{Autonomously generated from my website content using a Continuous Integration GitHub Pipeline.}}  % Add a small footer at the center

\\usepackage{ragged2e}
\\begin{document}


"""

info_name = "Dario Pasquali".upper()
info_role = "Post Doc @ Istituto Italiano di Tecnologia"
info_email = "dario.psquali@iit.it"
info_email2 = "dario.pasquali93@gmail.com"
info_cel = "(+39) 324 7956801"
info_linkedin = "dario-pasquali"

latex_info = f"""
\\name{{{info_name}}}
\\tagline{{{info_role}}}

\\photo{{3.3cm}}{{me3.jpg}}
\\personalinfo{{
  \\email{{{info_email}}}
  \\email{{{info_email2}}}
  \\phone{{{info_cel}}}
  \\location{{Bologna - Italy}}
  \\homepage{{https://dariopasquali.github.io/}}
  \\linkedin{{{info_linkedin}}}
}}

%% Make the header extend all the way to the right, if you want.
\\begin{{fullwidth}}
\\makecvheader
\\end{{fullwidth}}

"""

latex_work = """
\\AtBeginEnvironment{itemize}{\\small}
\\cvsection[page1sidebar]{About Me}
Experienced Software Engineer specializing in creating end-to-end user interaction systems that integrate Deep Learning with low-level devices.

\\cvsection{Work Experience}

"""

# Parse the work.yml file
with open('_data/work.yml', 'r') as file:
  # Load the contents of the file
  work_experiences = yaml.safe_load(file)
    
for experience in work_experiences:
  if experience['on_cv']:
    latex_exp = f"""\\cvevent{{{markdown_to_latex(experience['title'])}}}{{{markdown_to_latex(experience['group'])}}}{{{experience['from']} -- {experience['to']}}}{{{markdown_to_latex(experience['location']).split("(")[0]}}}
    {markdown_to_latex(experience['description'])}

    \\divider    
    
    """
    
    latex_work += latex_exp
    
latex_page2 = """
\\clearpage

\\begin{fullwidth}

  \\cvsection[page2sidebar]{Organized Events}
  \\printbibliography[heading=pubtype,title=\\empty, type=misc]

  \\cvsection[page2sidebar]{Publications}
  \\nocite{*}

  \\printbibliography[heading=pubtype,title={\\printinfo{\\faFileTextO}{Journal}}, type=article]
  \\divider

  \\printbibliography[heading=pubtype,title={\\printinfo{\\faFileTextO}{Conference Proceedings}}, type=inproceedings]
  
  \\cvsection[page2sidebar]{Foreign Languages: English (Professional Level)}
  \\divider

  \\cvsection[page2sidebar]{Programming Languages, Tools, Methodologies}
  Python, C++, Scala, Arduino; Numpy, Pandas, OpenCV, OpenFace, OpenPose, Tensorflow, Keras, PyTorch, SciPy, Scikit-learn, Seaborn, Hugging Face, Spark; ROS1, ROS2, YARP, PyQt5/6, Jamovi, ChatGPT, Cloudera CDH, Kafka, Kudu, Ansible, Terraform

  \\cvsection[page2sidebar]{About Me} 
  Beyond the lab, I'm passionate about \\textbf{cooking} and homebrewing beer—it’s a lot like programming! I also enjoy \textbf{playing board and card games} with friends every week. As a \\textit{Magic: The Gathering} enthusiast, I'm always on the lookout for interesting strategies to bring to the table.


\\end{fullwidth}
\\end{document}
"""

latex_doc = latex_head + latex_info + latex_work + latex_page2
with open("latex/mmayer.tex", mode='w') as file:
  file.writelines(latex_doc)
  
  
## Build the Right Column
# Education ---------------------------------------

latex_edu = """
\\cvsection{Education}

"""

with open('_data/education.yml', 'r') as file:
  edu_experiences = yaml.safe_load(file)
    
n_exp = len(edu_experiences)
for n, experience in enumerate(edu_experiences):
  exp = f"""\\cvevent{{{markdown_to_latex(experience['title'])}}}{{{markdown_to_latex(experience['institution'])}}}{{{experience['from']} -- {experience['to']}}}{{}}
  {markdown_to_latex(experience['description'])}   
  
  """
  latex_edu += exp
  if n < n_exp-1:
    latex_edu += """
    \\divider
    
    """
   
  
# Projects ------------------------------------------
latex_projects = """
\cvsection{Projects}

"""
projects = []

for file in os.listdir("_projects"):
  filename = os.path.join("_projects", file)
 
  if os.path.isfile(filename):
    with open(filename, 'r', encoding='utf-8') as f:
      project_file = f.read()
      header = project_file.split("---")[1]
      yaml_header = yaml.safe_load(header)
      
      if yaml_header['on_cv']:
        projects.append({
          "name": yaml_header['name'],
          "description": yaml_header['description']
        })
    
for prj in projects:
  exp = f"""\\cvproject{{{markdown_to_latex(prj['name'])}}}
    \\begin{{itemize}}
    \\item {markdown_to_latex(prj['description'])}
    \\end{{itemize}}
    \\smallskip
  
  """
  latex_projects += exp


with open("latex/page1sidebar.tex", mode='w') as file:
  file.writelines(latex_edu + latex_projects)