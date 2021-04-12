<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>A Tale of Two Societies</title>
    <link rel="stylesheet" href="dist/reveal.css">
    <link rel="stylesheet" href="dist/theme/coki.css">
</head>
<body>

<div class="reveal">
    <div class="slides">
        <section>
            <section class="titleslide" data-background="static_assets/background-title.png">
                <div vertical-align="middle">
                    <h1>A Tale of Two Societies</h1>
                    <h2>Are UK and US Chemistry Publishing <br>Diverging on Open Access?</h2>
                </div>
            </section>
            <section class="twocolumn" data-background="static_assets/background-general.png">
                <div class="leftside">
                    <h1>Colophon</h1>
                </div>
                <div class="rightside">
                    <ul>
                        <li>Code and data on Github: <a href="https://github.
com/Curtin-Open-Knowledge-Initiative/presentation-acs2021/">https://github.
com/Curtin-Open-Knowledge-Initiative/presentation-acs2021/</a></li>
                        <li>Presentation on Github: <a href="https://curtin-open-knowledge-initiative.github.
io/presentation-acs2021/">https://curtin-open-knowledge-initiative.github.io/presentation-acs2021/</a></li>
                        <li>Code and presentation at Zenodo: <a href="https://doi.org/10.5281/zenodo.4680986"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.4680986.svg" alt="DOI"></a></li>
                        <li>DOI: <a href="https://doi.org/10.5281/zenodo.4680985">10.5281/zenodo.4680985</a></li>
                    </ul>
                    <p>
                    <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
                        <img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
                        <br />
                        Copyright Cameron Neylon 2020-2021. This slide deck is licensed under a 
                    <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
                    Code is available under an Apache v2.0 license at Github. 
                    </p>
                </div>
            </section>
        </section>
        <section class="sectiondivider" data-background="static_assets/background-section.png">
            <h1>Two societies</h1>
            <h2>...both alike in dignity</h2>
        </section>
        <section class="bigblacktext" data-background="static_assets/background-general.png">
            <h1>In FAIR[?] chemistry where we lay our scene</h1>
        </section>
        <section class="bigblacktext" data-background="static_assets/background-general.png">
            <h1>Different national policy environments on OA 2010-20</h1>
        </section>
        <section class="bigblacktext" data-background="static_assets/background-general.png">
            <h1>...and different publisher responses</h1>
        </section>
        <section class="bigblacktext" data-background="static_assets/background-general.png">
            <img src="static_assets/timeline.png">
        </section>
        <section class="sectiondivider" data-background="static_assets/background-section.png">
            <h1>A quick segue on the data</h1>
            <h2>The Curtin Open Knowledge Initiative</h2>
        </section>
        <section class="pullquoteorange" data-background="static_assets/background-title.png">
            <p>
                "Our goal is to <strong>change the stories that universities tell about themselves</strong>,
                placing open knowledge at the heart of that narrative"
            </p>
        </section>
        <section>
            <section class="twocolumn" data-background="static_assets/background-general.png">
                <div class="leftside">
                    <h1>The Data</h1>
                </div>
                <div class="rightside">
                    <img src="static_assets/data.png">
                </div>
            </section>
            <section class="twocolumn" data-background="static_assets/background-general.png">
                <div class="leftside">
                    <h1>The Data</h1>
                </div>
                <div class="rightside">
                    <p>Data is derived from the following sources</p>
                    <ul>
                        <li>Crossref - weekly dump via Metadata Plus program</li>
                        <li>Unpaywall - Open Access Status data via open data dump (October 2020)</li>
                        <li>Microsoft Academic - Affiliation and authorship data via biweekly dump</li>
                        <li>GRID - Information on organisations via regular data dump</li>
                    </ul>
                    <p>Data is integrated and processed via Observatory Platform, an open source workflow system
                    developed within COKI to integrate data related to scholarly communications. The
                        <a href="https://github.com/The-Academic-Observatory/observatory-platform">code is
                    available on Github</a> including the template for
                        <a href="https://github.com/The-Academic-Observatory/observatory-platform/blob/develop/observatory-dags/observatory/dags/database/sql/aggregate_unpaywall.sql.jinja2">
                            SQL queries which generates the OA
                            status</a> we use from the Unpaywall data. More detail on the OA categories is also
                    provided on the slide below.</p>
                    <p>For this analysis, publisher is defined by the text string in the Crossref metadata,
                    affiliation is derived from the assignment by Microsoft Academic and field is the
                        <a href="https://academic.microsoft.com/topics/185592680">Level Zero
                            field "Chemistry" from Microsoft Academic</a> as provided in the data dump used. Some
                    comparative data for "<a href="https://academic.microsoft.com/topics/192562407">Materials
                            Science</a>" and "<a href="https://academic.microsoft.com/topics/86803240">Biology</a>"
                        is presented in additional slides.</p>
                </div>
            </section>
            <section class="twocolumn" data-background="static_assets/background-general.png">
                <div class="leftside">
                    <h1>Open Access Categories</h1>
                </div>
                <div class="rightside">
                    <p>The following is derived from the template SQL query used to define the OA categories in
                    Observatory Platform. For the most up to date information view the
                        <a href="https://github.com/The-Academic-Observatory/observatory-platform/blob/develop/observatory-dags/observatory/dags/database/sql/aggregate_unpaywall.sql.jinja2">
                            file on Github.</a></p>
                    <h2>AGGREGATE UNPAYWALL QUERY TEMPLATE</h2>
                    <p>This template query contains the SQL that directly interprets Unpaywall
                    data to determine OA categories at the output level. This is therefore
                    the canonical location for the precise definitions used for OA categories.
                    Ideally this file should contain both the queries themselves and
                    a description clear enough for a non-expert in SQL to understand how each
                    category is defined.</p>
                    <p>The current categories of Open Access described in this file are:</p>
                    <ul>
                        <li>is_oa: derived directly from Unpaywall</li>
                        <li>hybrid: accessible at the publisher with a recognised license</li>
                        <li>bronze: accessible at the publisher with no recognised license</li>
                        <li>gold_just_doaj: an article in a journal that is in DOAJ</li>
                        <li>gold: an article that is in a DOAJ journal OR is accessible at the publisher site with a 
                        recognised license (hybrid)</li>
                        <li>green: accessible at any site recognised as a repository (including preprints)</li>
                        <li>green_only: accessible at a repository and not (in a DOAJ journal OR hybrid OR bronze)</li>
                        <li>green_only_ignoring_bronze: accessible at a repository and not (in a DOAJ journal or 
                        hybrid)</li>
                    </ul>
                </div>
            </section>
            <section class="twocolumn" data-background="static_assets/background-general.png">
                <div class="leftside">
                    <h1>Open Access Categories</h1>
                </div>
                <div class="rightside">
                    <p>Levels of open access publishing are as provided by Unpaywall for all outputs with RSC and 
ACS as publisher in Crossref metadata. In the Observatory Platform terminology this is "gold" open access and includes
all articles published in either fully open access (as defined by indexing in DOAJ) and in mixed journals (i.e. 
"hybrid")</p>
                    <p>As defined in the SQL used to generate these categories.</p> 
                    <p>Gold Open Access:</p>
                    <p>gold OA is defined as either the journal being in DOAJ or the best_oa_location being a 
publisher and a license being detected. This works because Unpaywall will set the publisher as the best oa location if
it identifies an accessible publisher copy.</p>
                    <pre><code>
  CASE
    WHEN journal_is_in_doaj OR (best_oa_location.host_type = "publisher" AND best_oa_location.license is not null AND not journal_is_in_doaj) THEN TRUE
    ELSE FALSE
  END
    as gold,</code></pre>
                </div>
            </section>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
            <div class="leftside">
                <h1>Information</h1>
            </div>
            <div class="rightside">
                <div style="padding-top:2%;padding-left:5%;height:90%">
                    <iframe width="650" height="750" src="https://datastudio.google.
com/embed/reporting/0b057fb6-5e07-4643-92b5-6a25138fce6d/page/Bq6OB" frameborder="0" style="border:0" allowfullscreen></iframe>
                    <a href="http://openknowledge.community/dashboards/">http://openknowledge.community/dashboards/</a>
                </div>
            </div>
        </section>
        <section class="sectiondivider" data-background="static_assets/background-section.png">
            <h1>What about publishers?</h1>
            <h2>What can we tell about policy<br> and culture change?</h2>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
                <div class="leftside">
                    <h1>Publisher choice in UK</h1>
                </div>
                <div class="rightside">
                    <iframe data-src="precipy/gbr_overtime.html"></iframe>
                </div>
        </section>
        <section class="twocolumn" 
                 data-background="static_assets/background-general.png"
                 data-transition="fade-in slide-out">
            <div class="leftside">
                <h1>Publisher choice in UK</h1>
            </div>
            <div class="rightside">
                <iframe data-src="precipy/gbr_overtime_arrows.html"></iframe>
            </div>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
            <div class="leftside">
                <h1>Publisher choice by country</h1>
            </div>
            <div class="rightside">
                <iframe data-src="precipy/gbrusa_overtime.html"></iframe>
            </div>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
                <div class="leftside">
                    <h1>Different patterns with OA publishing levels?</h1>
                </div>
                <div class="rightside">
                    <iframe data-src="precipy/gbrusa_pc_gold_overtime.html"></iframe>
                </div>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
            <div class="leftside">
                <h1>Publisher percent of Chemistry by institution</h1>
            </div>
            <div class="rightside">
                <iframe data-src="precipy/institutions_scatter_pc_chemistry.html"></iframe>
            </div>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
            <div class="leftside">
                <h1>Publisher percent of OA publishing in chemistry by institution</h1>
            </div>
            <div class="rightside">
                <iframe data-src="precipy/institutions_scatter_pc_gold_chemistry.html"></iframe>
            </div>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
            <div class="leftside">
                <h1>Parallel effects at the country level</h1>
            </div>
            <div class="rightside">
                <iframe data-src="precipy/countries_overtime.html"></iframe>
            </div>
        </section>
        <section class="sectiondivider" data-background="static_assets/background-section.png">
            <h1>Conclusions</h1>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
            <div class="leftside">
                <h1>Conclusions</h1>
            </div>
            <div class="rightside">
                <ul>
                    <li>
                        <p>There are significant shifts in national patterns that can be associated with changes 
                        in funder policy and with the offerings of RSC and ACS</p>
                    </li>
                    <li>
                        <p>RSC took a significant lead in early open access provision for chemistry, particularly 
                        in the UK but has fallen back</p>
                    </li>
                    <li>
                        <p>National averages don’t tell the full picture. Specific institutions show very different 
                        and quite specific patterns. There are differential policy effects</p>
                    </li>
                    <li>
                        <p>Recent changes are strongly driven by read and publish agreements with substantial
                        shifts in publisher choice corresponding to introduction of deals.</p>
                    </li>
                    <li>
                        <p>There is evidence of concentration of publishing in chemistry with two large 
                        publishers taking up an increasing percentage. Should we be concerned about diversity?</p>
                    </li>
                </ul>
            </div>
        </section>
        <section class="bigblacktext" data-background="static_assets/background-general.png">
            <h1>Chemistry has been following, not leading...</h1>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
            <div class="leftside">
                <h1>Conclusions</h1>
            </div>
            <div class="rightside">
                <iframe data-src="precipy/institutions_chemistry_lag.html"></iframe>
            </div>
        </section>
        <section class="bigblacktext" data-background="static_assets/background-general.png">
            <h1>...but maybe that is starting to change</h1>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
            <div class="leftside">
                <h1>COKI Team</h1>
            </div>
            <div class="rightside">
                <div style="width:45%;float:left">
                    <p><strong>Centre for Culture and Technology</strong></p>
                    <ul>
                        <li>Cameron Neylon</li>
                        <li>Lucy Montgomery</li>
                        <li>Katie Wilson</li>
                        <li>Chun-Kai (Karl) Huang</li>
                        <li>Chloe-Brookes Kenworthy</li>
                        <li>Tim Winkler</li>
                    </ul>
                    <p><strong>Funding from</strong></p>
                    <ul>
                        <li>Research Office at Curtin</li>
                        <li>Faculty of Humanities</li>
                        <li>School of Media, Creative Arts and Social Enquiry</li>
                        <li>Andrew W. Mellon Foundation</li>
                        <li>Arcadia</li>
                    </ul>
                </div>
                <div style="width:45%;float:right">
                    <p><strong>Curtin Institute for Computation</strong></p>
                    <ul>
                        <li>Richard Hosking</li>
                        <li>Rebecca Handcock</li>
                        <li>Aniek Roelofs</li>
                        <li>Jamie Diprose</li>
                        <li>Tuan Chien</li>
                    </ul>
                    <p><strong>Educopia Foundation</strong></p>
                    <ul>
                        <li>Katherine Skinner</li>
                        <li>Rebecca Meyerson</li>
                    </ul>
                </div>
            </div>
        </section>
        <section class="sectiondivider" data-background="static_assets/background-section.png">
            <h1> </h1>
            <h2>@COKIProject - @cameronneylon</h2>
            <h2>http://openknowledge.community
                <ul>
                    <li>Subscribe to the COKI Newsletter</li>
                    <li>View the public dashboards</li>
                </ul>
            </h2>
        </section>
        <section class="sectiondivider" data-background="static_assets/background-section.png">
            <h1>Notes and further information</h1>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
            <div class="leftside">
                <h1>Notes</h1>
            </div>
            <div class="rightside">
                <p>Publisher percentage of chemistry is calculated based on the total count of publications
                assigned in Microsoft Academic to the Level 0 field of "chemistry" as the denominator with the
                total count of publications in Crossref where the publisher name field corresponds to the most
                common variant of the publisher name (<em>Royal Society of Chemistry (RSC)</em> and 
                <em>American Chemical Society (ACS)</em> respectively).</p>
                <p>Strictly these are not percentages and could in theory go to greater than 100%. They are
                also sensitive in magnitude to changes in the Microsoft field assignment. However it is a like
                for like comparison across the two publishers.</p>
                <p>An analysis by journal would also be interesting but currently the metadata for journal
                identification is less reliable with journal names and choice of ISSN provided in Crossref
                metadata changing from year to year for both publishers. Future analysis deploying ISSN-L
                could address this.</p>
            </div>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
            <div class="leftside">
                <h1>Publisher Count by year</h1>
            </div>
            <div class="rightside">
                <iframe data-src="precipy/countries_count_overtime.html"></iframe>
            </div>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
            <div class="leftside">
                <h1>Publisher % Green by year</h1>
            </div>
            <div class="rightside">
                <iframe data-src="precipy/countries_pc_green_overtime.html"></iframe>
            </div>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
            <div class="leftside">
                <h1>Chemistry Count by year</h1>
            </div>
            <div class="rightside">
                <iframe data-src="precipy/countries_count_chem_overtime.html"></iframe>
            </div>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
            <div class="leftside">
                <h1>Publishers % of Materials Field</h1>
            </div>
            <div class="rightside">
                <iframe data-src="precipy/countries_materials_overtime.html"></iframe>
            </div>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
            <div class="leftside">
                <h1>Publishers % of Biology Field</h1>
            </div>
            <div class="rightside">
                <iframe data-src="precipy/countries_materials_overtime.html"></iframe>
            </div>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
            <div class="leftside">
                <h1>Publisher percent of Materials Science by institution</h1>
            </div>
            <div class="rightside">
                <iframe data-src="precipy/institutions_scatter_pc_materials.html"></iframe>
            </div>
        </section>
        <section class="twocolumn" data-background="static_assets/background-general.png">
            <div class="leftside">
                <h1>Publisher percent of Biology by institution</h1>
            </div>
            <div class="rightside">
                <iframe data-src="precipy/institutions_scatter_pc_biology.html"></iframe>
            </div>
        </section>
    </div>
</div>

<script src="dist/reveal.js"></script>
<script type="text/javascript">
		Reveal.initialize({center: false});
</script>
</body>
</html>