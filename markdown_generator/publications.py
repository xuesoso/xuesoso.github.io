#!/usr/bin/env python
# coding: utf-8

# # Publications markdown generator for academicpages
#
# Takes a TSV of publications with metadata and converts them for use with [academicpages.github.io](academicpages.github.io). This is an interactive Jupyter notebook ([see more info here](http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html)). The core python code is also in `publications.py`. Run either from the `markdown_generator` folder after replacing `publications.tsv` with one containing your data.
#
# TODO: Make this work with BibTex and other databases of citations, rather than Stuart's non-standard TSV format and citation style.
#

# ## Data format
#
# The TSV needs to have the following columns: pub_date, title, venue, excerpt, citation, site_url, and paper_url, with a header at the top.
#
# - `excerpt` and `paper_url` can be blank, but the others must have values.
# - `pub_date` must be formatted as YYYY-MM-DD.
# - `url_slug` will be the descriptive part of the .md file and the permalink URL for the page about the paper. The .md file will be `YYYY-MM-DD-[url_slug].md` and the permalink will be `https://[yourdomain]/publications/YYYY-MM-DD-[url_slug]`
#
# This is how the raw file looks (it doesn't look pretty, use a spreadsheet or other program to edit and create).

# ## Import pandas
#
# We are using the very handy pandas library for dataframes.

# In[1]:


import pandas as pd
import numpy as np


# ## Import TSV
#
# Pandas makes this easy with the read_csv function. We are using a TSV, so we specify the separator as a tab, or `\t`.
#
# I found it important to put this data in a tab-separated values format, because there are a lot of commas in this kind of data and comma-separated values can get messed up. However, you can modify the import statement, as pandas also has read_excel(), read_json(), and others.

# In[3]:


publications = pd.read_csv("publications.csv", sep=",", header=0)
myname = 'Yuan Xue'
publications


# ## Escape special characters
#
# YAML is very picky about how it takes a valid string, so we are replacing single and double quotes (and ampersands) with their HTML encoded equivilents. This makes them look not so readable in raw format, but they are parsed and rendered nicely.

# In[5]:


html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
    }

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)


# ## Creating the markdown files
#
# This is where the heavy lifting is done. This loops through all the rows in the TSV dataframe, then starts to concatentate a big string (```md```) that contains the markdown for each type. It does the YAML metadata first, then does the description for the individual page.

# In[14]:


import os
for row, item in publications.iterrows():

    md_filename = str(item.pub_date) + "-" + item.url_slug + ".md"
    html_filename = str(item.pub_date) + "-" + item.url_slug
    year = item.pub_date

    ## YAML variables

    md = "---\ntitle: \""   + item.title + '"\n'

    md += """collection: publications"""

    md += """\npermalink: /publication/""" + html_filename

    if len(str(item.excerpt)) > 5:
        md += "\nexcerpt: '" + html_escape(item.excerpt) + "'"

    md += "\nyear: " + str(item.pub_date)

    md += "\nvenue: '" + html_escape(item.venue) + "'"

    split_paper_url = item.paper_url.split(';')
    if len(str(split_paper_url[0])) > 5:
        md += "\npaperurl: '" + split_paper_url[0] + "'"

    if len(split_paper_url) > 1:
        md += "\nbiorxiv_url: '" + split_paper_url[-1] + "'"

    md += "\ncitation: '" + html_escape(item.citation).replace(myname, '<b>'+myname+'</b>')+"'"

    md += "\n---"

    ## Markdown description for individual page

    if len(str(item.excerpt)) > 5:
        md += "\n" + html_escape(item.excerpt) + "\n"

    if len(str(split_paper_url[0])) > 5 and item.venue != 'BioRxiv':
        md += "\n[Article available here](" + split_paper_url[0] + ")\n"

    if item.venue == 'BioRxiv':
        md += "\n[Preprint available here](" + split_paper_url[0] + ")\n"

    if len(split_paper_url) > 1:
        md += "\n[Preprint available here](" + split_paper_url[-1] + ")\n"


#     md += "\nRecommended citation: " + item.citation

    md_filename = os.path.basename(md_filename)

    with open("../_publications/" + md_filename, 'w') as f:
        f.write(md)


# These files are in the publications directory, one directory below where we're working from.

# In[6]:


# get_ipython().system('ls ../_publications/')


# In[7]:


# get_ipython().system('cat ../_publications/2009-10-01-paper-title-number-1.md')


# In[ ]:




