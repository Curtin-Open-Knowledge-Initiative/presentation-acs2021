# A Tale of Two Societies

## Code, slides and data for a presentation to the ACS 2021 Spring Meeting

[![DOI](https://zenodo.org/badge/356842271.svg)](https://zenodo.org/badge/latestdoi/356842271)

## Abstract

Open Access is now the dominant mode of scholarly communications, but not in chemistry. The American Chemical 
Society and the Royal Society of Chemistry are unusual amongst scholarly societies for having large publishing 
programs and unusual amongst publishers for having such large and diverse membership. The two societies took 
different approaches in addressing the different open access policies of the UK and the US. This did not lead to 
something so simple as a concentration of UK publishing with the RSC or vice versa but a much more interesting 
set of changes. This talk will make a data-led exploration of how open access is changing chemistry publishing 
and what implications it has for the scholarly societies and their publishing operations.

## Code and approach

Data is derived from the Academic Observatory, a product of the [Curtin Open Knowledge Initiative](http://openknowledge.community). The data is
an integration of resources from [Crossref](https://crossref.org), [Microsoft Academic](https://academic.microsoft.com), 
[Unpaywall](https://unpaywall.org), [GRID](https://grid.ac) and [Open Citations](http://opencitations.net/), 
processed through [an open source workflow system](https://github.com/The-Academic-Observatory/observatory-platform). 

The talk is built in [reveal.js](https://revealjs.com) using [precipy](https://github.com/ananelson/precipy) to 
generate the graphs for the slides. The code pulls data from the observatory and processes it using pandas and 
[plotly](https://plotly.com/python/) to generate interactive HTML figures, which are inserted into the slidedeck. 
The slidedeck is pure HTML5/css/javascript although the css could do with a bunch of work to improve the formatting
on more browsers.

Data snapshots as csv files are also provided for the main datasets used for the plots.

* [institutions.csv](https://github.com/Curtin-Open-Knowledge-Initiative/presentation-acs2021/blob/gh-pages/precipy/institutions.csv)
* [countries.csv](https://github.com/Curtin-Open-Knowledge-Initiative/presentation-acs2021/blob/gh-pages/precipy/countries.csv)
