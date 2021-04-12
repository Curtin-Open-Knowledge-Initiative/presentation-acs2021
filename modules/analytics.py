# -*- coding: utf-8 -*-
# Copyright 2020 Curtin University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Author: Cameron Neylon

from typing import Union, Tuple, Callable, Optional, List
import json
import pandas as pd
import pydata_google_auth
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

pio.templates['coki_reveal'] = go.layout.Template(
    layout=dict(font_size=18,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                )
                )
)
pio.templates.default = 'simple_white+coki_reveal'

from pathlib import Path

import observatory.reports.chart_utils as chart_utils
from precipy.analytics_function import AnalyticsFunction

from observatory.reports.tables import (
    GenericOpenAccessTable,
    GenericPublishersTable
)

from modules.report_tables import GenericDisciplinesTable

scopes = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/drive',
]
credentials = pydata_google_auth.get_user_credentials(
    scopes,
)

disciplines = ['Chemistry', 'Materials science', 'Biology']
disc = [d.split(' ')[0].lower() for d in disciplines]

FOCUS_YEAR = 2019
YEAR_RANGE = (2009, 2021)
PROJECT_ID = 'academic-observatory'
CACHE_FILENAME = 'cache.h5'


def get_country_data(af: AnalyticsFunction,
                     focus_year=FOCUS_YEAR,
                     year_range=YEAR_RANGE,
                     project_id=PROJECT_ID,
                     data: str = 'current'):
    if data == 'current':
        tables = 'coki_dashboards.country'
    elif data == 'local':
        raise NotImplementedError
    else:  # In this case data must be the path to the relevant BQ table eg observatory.country20210403
        tables = data

    bq_table = f'academic-observatory.{tables}'
    scope = ''
    args = [credentials, project_id, scope, focus_year, year_range, bq_table]
    country_table = GenericPublishersTable(*args)
    c = country_table.df
    country_oa = GenericOpenAccessTable(*args)
    oa = country_oa.df

    scope = f"""AND
(discipline.field in ("{'", "'.join(disciplines)}")
)
    """

    args = [credentials, project_id, scope, focus_year, year_range, bq_table]
    cd_table = GenericDisciplinesTable(*args)
    cd = cd_table.df

    for discipline in disciplines:
        c = c.merge(cd[cd.field == discipline][['country_code',
                                                'published_year',
                                                'count',
                                                'oa',
                                                'gold',
                                                'green']],
                    on=['country_code', 'published_year'],
                    suffixes=(None, f'_{discipline.lower().split(" ")[0]}'))

    c = c.merge(oa[['country_code',
                    'published_year',
                    'oa',
                    'green',
                    'gold',
                    'hybrid',
                    'gold_doaj']],
                on=['country_code', 'published_year'],
                suffixes=(None, '_country')
                )

    with pd.HDFStore(CACHE_FILENAME) as store:
        store['countries'] = c
    af.add_existing_file(CACHE_FILENAME, remove=True)


def get_institution_data(af: AnalyticsFunction,
                         focus_year=FOCUS_YEAR,
                         year_range=YEAR_RANGE,
                         project_id=PROJECT_ID,
                         data: str = 'current'):
    if data == 'current':
        tables = 'coki_dashboards.institution'
    elif data == 'local':
        raise NotImplementedError
    else:  # In this case data must be the path to the relevant BQ table eg observatory.institution20210403
        tables = data

    bq_table = f'academic-observatory.{tables}'
    scope = """AND
country_code in ("GBR", "USA", "NLD")
"""
    args = [credentials, project_id, scope, focus_year, year_range, bq_table]
    inst_table = GenericPublishersTable(*args)
    c = inst_table.df
    inst_oa = GenericOpenAccessTable(*args)
    oa = inst_oa.df

    scope = f"""AND
(country_code in ("GBR", "USA", "NLD"))
AND (discipline.field in ("{'", "'.join(disciplines)}"))
    """

    args = [credentials, project_id, scope, focus_year, year_range, bq_table]
    cd_table = GenericDisciplinesTable(*args)
    cd = cd_table.df

    for discipline in disciplines:
        c = c.merge(cd[cd.field == discipline][['id',
                                                'published_year',
                                                'count',
                                                'oa',
                                                'gold',
                                                'green']],
                    on=['id', 'published_year'],
                    suffixes=(None, f'_{discipline.lower().split(" ")[0]}'))

    c = c.merge(oa[['id',
                    'published_year',
                    'oa',
                    'green',
                    'gold',
                    'hybrid',
                    'gold_doaj']],
                on=['id', 'published_year'],
                suffixes=(None, '_institution')
                )

    with pd.HDFStore(CACHE_FILENAME) as store:
        store['institutions'] = c
    af.add_existing_file(CACHE_FILENAME, remove=True)


def process_country_data(af: AnalyticsFunction):
    c = load_cache_data(af, get_country_data, 'countries')
    chart_utils.calculate_percentages(c,
                                      numer_columns=['count',
                                                     'oa',
                                                     'gold',
                                                     'green'] + [f'count_{d}' for d in disc],
                                      denom_column='total_outputs',
                                      column_name_add='pc_of_total_')

    chart_utils.calculate_percentages(c,
                                      numer_columns=['gold'] + [f'gold_{d}' for d in disc],
                                      denom_column='gold_country',
                                      column_name_add='pc_of_gold_')
    for d in disc:
        chart_utils.calculate_percentages(c,
                                          numer_columns=['count',
                                                         'oa',
                                                         'gold',
                                                         'green'],
                                          denom_column=f'count_{d}',
                                          column_name_add=f'pc_of_{d}_')
        chart_utils.calculate_percentages(c,
                                          numer_columns=['gold'],
                                          denom_column=f'gold_{d}',
                                          column_name_add=f'pc_of_gold_{d}_')
        chart_utils.calculate_percentages(c,
                                          numer_columns=[f'gold_{d}', f'green_{d}'],
                                          denom_column=f'count_{d}',
                                          column_name_add=f'pc_of_{d}_')

    with pd.HDFStore(CACHE_FILENAME) as store:
        store['countries'] = c
    af.add_existing_file(CACHE_FILENAME, remove=True)

    c.to_csv('countries.csv')
    af.add_existing_file('countries.csv', remove=True)


def process_institution_data(af: AnalyticsFunction):
    c = load_cache_data(af, get_institution_data, 'institutions')
    chart_utils.calculate_percentages(c,
                                      numer_columns=['count',
                                                     'oa',
                                                     'gold',
                                                     'green'] + [f'count_{d}' for d in disc],
                                      denom_column='total_outputs',
                                      column_name_add='pc_of_total_')

    chart_utils.calculate_percentages(c,
                                      numer_columns=['gold'] + [f'gold_{d}' for d in disc],
                                      denom_column='gold_institution',
                                      column_name_add='pc_of_gold_')
    for d in disc:
        chart_utils.calculate_percentages(c,
                                          numer_columns=['count',
                                                         'oa',
                                                         'gold',
                                                         'green'],
                                          denom_column=f'count_{d}',
                                          column_name_add=f'pc_of_{d}_')
        chart_utils.calculate_percentages(c,
                                          numer_columns=['gold'],
                                          denom_column=f'gold_{d}',
                                          column_name_add=f'pc_of_gold_{d}_')

        chart_utils.calculate_percentages(c,
                                          numer_columns=[f'gold_{d}', f'green_{d}'],
                                          denom_column=f'count_{d}',
                                          column_name_add=f'pc_of_{d}_')

    with pd.HDFStore(CACHE_FILENAME) as store:
        store['institutions'] = c
    af.add_existing_file(CACHE_FILENAME, remove=True)

    c.to_csv('institutions.csv')
    af.add_existing_file('institutions.csv', remove=True)


def pres_figures(af):
    palette = {'GBR': '#e41a1c',
               'USA': '#377eb8',
               'NLD': '#ff7f00',
               'United Kingdom': '#e41a1c',
               'United States': '#377eb8',
               'Netherlands': '#ff7f00',
               'American Chemical Society (ACS)': '#984ea3',
               'Royal Society of Chemistry (RSC)': '#4daf4a'}

    institutions_data = load_cache_data(af, process_institution_data, 'institutions')
    institutions_data.sort_values(['published_year', 'name'], inplace=True)
    institutions_data.replace('United Kingdom of Great Britain and Northern Ireland',
                              'United Kingdom', inplace=True)
    institutions_data.replace('United States of America',
                              'United States', inplace=True)

    countries_data = load_cache_data(af, process_country_data, 'countries')
    countries_data.sort_values(['published_year', 'name'], inplace=True)
    countries_data.replace('United Kingdom of Great Britain and Northern Ireland',
                           'United Kingdom', inplace=True)

    pivot_countries = countries_data.pivot_table(index=['country_code', 'name', 'published_year'],
                                                 columns='publisher',
                                                 values=['count_chemistry',
                                                         'pc_of_chemistry_count',
                                                         'percent_gold',
                                                         'pc_of_chemistry_gold',
                                                         'pc_of_gold_chemistry_gold',
                                                         'pc_of_chemistry_gold_chemistry',
                                                         'pc_of_chemistry_green_chemistry'])
    pivot_countries = pivot_countries.swaplevel(i=0, j=1, axis=1)
    rsc_countries = pivot_countries['Royal Society of Chemistry (RSC)']
    rsc_countries.reset_index(inplace=True)
    rsc_countries.sort_values(['published_year', 'country_code'], inplace=True)

    acs_countries = pivot_countries['American Chemical Society (ACS)']
    acs_countries.reset_index(inplace=True)
    acs_countries.sort_values(['published_year', 'country_code'], inplace=True)

    pivot_institutions = institutions_data.pivot_table(index=['country_code', 'name', 'published_year'],
                                                       columns='publisher',
                                                       values=['count_chemistry',
                                                               'pc_of_chemistry_count',
                                                               'percent_gold',
                                                               'pc_of_chemistry_gold',
                                                               'pc_of_gold_chemistry_gold',
                                                               'pc_of_chemistry_gold_chemistry',
                                                               'pc_of_chemistry_green_chemistry'])
    pivot_institutions = pivot_institutions.swaplevel(i=0, j=1, axis=1)
    rsc_institutions = pivot_institutions['Royal Society of Chemistry (RSC)']
    rsc_institutions.reset_index(inplace=True)
    rsc_institutions.sort_values(['published_year', 'country_code'], inplace=True)

    acs_institutions = pivot_institutions['American Chemical Society (ACS)']
    acs_institutions.reset_index(inplace=True)
    acs_institutions.sort_values(['published_year', 'country_code'], inplace=True)

    figdata = countries_data[(countries_data.country_code.isin(['USA', 'GBR', 'NLD'])) &
                             (countries_data.published_year.isin(range(2010, 2021))) &
                             (countries_data.publisher.isin(['American Chemical Society (ACS)',
                                                             'Royal Society of Chemistry (RSC)']))]

    # UK alone percent of chemistry
    f = px.line(figdata[figdata.country_code == 'GBR'],
                x='published_year',
                y='pc_of_chemistry_count',
                color='publisher',
                color_discrete_map=palette,
                range_y=(0, 15),
                labels=dict(published_year='Year of Publication',
                            pc_of_chemistry_count='Publisher % of Chemistry',
                            name='Country',
                            publisher='Publisher')
                )

    write_plotly_div(af, f, 'gbr_overtime.html')

    # Add date annotations
    f.add_annotation(x=2012, y=10.15,
                     text='RCUK Mandate\nGold for Gold',
                     showarrow=True,
                     font=dict(size=24,
                               color='dimgrey')
                     )
    f.add_annotation(x=2015, y=13.1,
                     text='HEFCE Mandate',
                     showarrow=True,
                     font=dict(size=24,
                               color='dimgrey')
                     )
    f.add_annotation(x=2017, y=11.35,
                     text='RSC Advances goes OA',
                     showarrow=True,
                     font=dict(size=24,
                               color='dimgrey')
                     )
    write_plotly_div(af, f, 'gbr_overtime_arrows.html')

    # GBR count of chemistry over time
    f = px.line(figdata[figdata.country_code == 'GBR'],
                x='published_year',
                y='count_chemistry',
                color='publisher',
                color_discrete_map=palette,
                #range_y=(0, 15),
                labels=dict(published_year='Year of Publication',
                            count_chemistry='# of Chemistry outputs by year',
                            name='Country',
                            publisher='Publisher')
                )

    write_plotly_div(af, f, 'gbr_count_chem_overtime.html')

    # UK and USA percent of chemistry
    f = px.line(figdata[figdata.country_code.isin(['GBR', 'USA'])],
                x='published_year',
                y='pc_of_chemistry_count',
                color='publisher',
                color_discrete_map=palette,
                facet_row='name',
                range_y=(0, 15),
                labels=dict(published_year='Year of Publication',
                            pc_of_chemistry_count='Publisher % of Chemistry',
                            name='Country',
                            publisher='Publisher')
                )
    f.for_each_annotation(lambda a: a.update(text=a.text.replace("Country=", "")))
    f.update_yaxes(title_text="", row=1, col=1)
    write_plotly_div(af, f, 'gbrusa_overtime.html')

    # US, GBR and NLD percent of chemistry
    f = px.line(figdata,
                x='published_year',
                y='pc_of_chemistry_count',
                color='publisher',
                color_discrete_map=palette,
                facet_row='name',
                range_y=(0, 15),
                labels=dict(published_year='Year of Publication',
                            pc_of_chemistry_count='Publisher % of Chemistry',
                            name='Country',
                            publisher='Publisher')
                )
    f.for_each_annotation(lambda a: a.update(text=a.text.replace("Country=", "")))
    f.update_yaxes(title_text="", row=1, col=1)
    f.update_yaxes(title_text="", row=3, col=1)
    write_plotly_div(af, f, 'countries_overtime.html')

    # Three countries count of articles for each publisher
    f = px.line(figdata,
                x='published_year',
                y='count',
                color='publisher',
                color_discrete_map=palette,
                facet_row='name',
                # range_y=(0, 30),
                labels=dict(published_year='Year of Publication',
                            count='Publisher Count of Articles',
                            name='Country',
                            publisher='Publisher')
                )
    f.for_each_annotation(lambda a: a.update(text=a.text.replace("Country=", "")))
    f.update_yaxes(title_text='', row=1, col=1)
    f.update_yaxes(title_text='', row=3, col=1)
    write_plotly_div(af, f, 'countries_count_overtime.html')

    # Count of chemistry by country
    f = px.line(figdata,
                x='published_year',
                y='count_chemistry',
                facet_row='name',
                # range_y=(0, 30),
                labels=dict(published_year='Year of Publication',
                            count_chemistry='# of Chemistry Outputs',
                            name='Country')
                )
    f.for_each_annotation(lambda a: a.update(text=a.text.replace("Country=", "")))
    f.update_yaxes(title_text='', row=1, col=1)
    f.update_yaxes(title_text='', row=3, col=1)
    write_plotly_div(af, f, 'countries_count_chem_overtime.html')

    # US, GBR and NLD percent of materials
    f = px.line(figdata,
                x='published_year',
                y='pc_of_materials_count',
                color='publisher',
                color_discrete_map=palette,
                facet_row='name',
                range_y=(0, 15),
                labels=dict(published_year='Year of Publication',
                            pc_of_materials_count='Publisher % of Materials',
                            name='Country',
                            publisher='Publisher')
                )
    f.for_each_annotation(lambda a: a.update(text=a.text.replace("Country=", "")))
    f.update_yaxes(title_text="", row=1, col=1)
    f.update_yaxes(title_text="", row=3, col=1)
    write_plotly_div(af, f, 'countries_materials_overtime.html')

    # US, GBR and NLD percent of biology
    f = px.line(figdata,
                x='published_year',
                y='pc_of_biology_count',
                color='publisher',
                color_discrete_map=palette,
                facet_row='name',
                #range_y=(0, 15),
                labels=dict(published_year='Year of Publication',
                            pc_of_biology_count='Publisher % of Biology',
                            name='Country',
                            publisher='Publisher')
                )
    f.for_each_annotation(lambda a: a.update(text=a.text.replace("Country=", "")))
    f.update_yaxes(title_text="", row=1, col=1)
    f.update_yaxes(title_text="", row=3, col=1)
    write_plotly_div(af, f, 'countries_biology_overtime.html')

    # Percent Gold for each publisher by country
    f = px.line(figdata[figdata.country_code.isin(['GBR', 'USA'])],
                x='published_year',
                y='percent_gold',
                color='publisher',
                color_discrete_map=palette,
                facet_row='name',
                range_y=(0, 50),
                labels=dict(published_year='Year of Publication',
                            percent_gold='% Gold for Publisher',
                            name='Country',
                            publisher='Publisher')
                )
    f.for_each_annotation(lambda a: a.update(text=a.text.replace("Country=", "")))
    f.update_yaxes(title_text='', row=1, col=1)
    f.update_yaxes(title_text='', row=3, col=1)
    write_plotly_div(af, f, 'gbrusa_pc_gold_overtime.html')

    # Percent Green for each publisher by country
    f = px.line(figdata,
                x='published_year',
                y='percent_green',
                color='publisher',
                color_discrete_map=palette,
                facet_row='name',
                range_y=(0, 100),
                labels=dict(published_year='Year of Publication',
                            percent_green='% Green for Publisher',
                            name='Country',
                            publisher='Publisher')
                )
    f.for_each_annotation(lambda a: a.update(text=a.text.replace("Country=", "")))
    f.update_yaxes(title_text='', row=1, col=1)
    f.update_yaxes(title_text='', row=3, col=1)
    write_plotly_div(af, f, 'countries_pc_green_overtime.html')

    # Percent of chemistry outputs with each publisher by institution
    scatter_data = institutions_data[
        (institutions_data.publisher.isin(['Royal Society of Chemistry (RSC)', 'American Chemical Society (ACS)'])) &
        (institutions_data.published_year.isin(range(2010, 2021))) &
        (institutions_data.count_chemistry > 50)]
    p = scatter_data.pivot_table(index=['id', 'name', 'country_code', 'country', 'published_year', 'count_chemistry'],
                                 columns='publisher',
                                 values='pc_of_chemistry_count')
    p.reset_index(inplace=True)
    p.sort_values(['published_year', 'id'], inplace=True)
    f = px.scatter(p,
                   x='Royal Society of Chemistry (RSC)',
                   y='American Chemical Society (ACS)',
                   color='country', color_discrete_map=palette,
                   size='count_chemistry',
                   animation_frame='published_year',
                   animation_group='id',
                   hover_name='name',
                   range_x=(0, 50), range_y=(0, 50),
                   labels=dict(country='Country',
                               published_year='Year of Publication'))
    f.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 700
    write_plotly_div(af, f, 'institutions_scatter_pc_chemistry.html')

    # Percent of materials outputs with each publisher by institution
    scatter_data = institutions_data[
        (institutions_data.publisher.isin(['Royal Society of Chemistry (RSC)', 'American Chemical Society (ACS)'])) &
        (institutions_data.published_year.isin(range(2010, 2021))) &
        (institutions_data.count_materials > 50)]
    p = scatter_data.pivot_table(index=['id', 'name', 'country_code', 'country', 'published_year', 'count_materials'],
                                 columns='publisher',
                                 values='pc_of_materials_count')
    p.reset_index(inplace=True)
    p.sort_values(['published_year', 'id'], inplace=True)
    f = px.scatter(p,
                   x='Royal Society of Chemistry (RSC)',
                   y='American Chemical Society (ACS)',
                   color='country', color_discrete_map=palette,
                   size='count_materials',
                   animation_frame='published_year',
                   animation_group='id',
                   hover_name='name',
                   range_x=(0, 50), range_y=(0, 50),
                   labels=dict(country='Country',
                               published_year='Year of Publication'))
    f.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 700
    write_plotly_div(af, f, 'institutions_scatter_pc_materials.html')

    # Percent of biology outputs with each publisher by institution
    scatter_data = institutions_data[
        (institutions_data.publisher.isin(['Royal Society of Chemistry (RSC)', 'American Chemical Society (ACS)'])) &
        (institutions_data.published_year.isin(range(2010, 2021))) &
        (institutions_data.count_materials > 50)]
    p = scatter_data.pivot_table(index=['id', 'name', 'country_code', 'country', 'published_year', 'count_biology'],
                                 columns='publisher',
                                 values='pc_of_biology_count')
    p.reset_index(inplace=True)
    p.sort_values(['published_year', 'id'], inplace=True)
    f = px.scatter(p,
                   x='Royal Society of Chemistry (RSC)',
                   y='American Chemical Society (ACS)',
                   color='country', color_discrete_map=palette,
                   size='count_biology',
                   animation_frame='published_year',
                   animation_group='id',
                   hover_name='name',
                   range_x=(0, 50), range_y=(0, 50),
                   labels=dict(country='Country',
                               published_year='Year of Publication'))
    f.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 700
    write_plotly_div(af, f, 'institutions_scatter_pc_biology.html')

    # Percent of chemistry published gold with each publisher by institution
    p = scatter_data.pivot_table(index=['id', 'name', 'country_code', 'country', 'published_year',
                                        'count_chemistry', 'gold_chemistry'],
                                 columns='publisher',
                                 values='pc_of_gold_chemistry_gold')
    p.reset_index(inplace=True)
    p.sort_values(['published_year', 'id'], inplace=True)
    f = px.scatter(p,
                   x='Royal Society of Chemistry (RSC)',
                   y='American Chemical Society (ACS)',
                   color='country', color_discrete_map=palette,
                   size='count_chemistry',
                   animation_frame='published_year',
                   animation_group='name',
                   hover_name='name',
                   hover_data=['gold_chemistry'],
                   range_x=(0, 50), range_y=(0, 50),
                   labels=dict(country='Country',
                               published_year='Year of Publication',
                               count_chemistry='Total Chemistry Publications',
                               gold_chemistry='Chemistry Published OA'))
    f.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 700
    write_plotly_div(af, f, 'institutions_scatter_pc_gold_chemistry.html')

    i_lag = institutions_data[(institutions_data.published_year.isin(range(2010, 2020))) &
                              (institutions_data.count_chemistry > 50)][
        ['id', 'name', 'published_year', 'country', 'total_outputs',
         'green_institution', 'gold_institution', 'pc_of_chemistry_green_chemistry', 'pc_of_chemistry_gold_chemistry',
         'count_chemistry']]

    i_lag.drop_duplicates(inplace=True)
    i_lag['percent_green'] = i_lag['green_institution'] / i_lag['total_outputs'] * 100
    i_lag['percent_gold'] = i_lag['gold_institution'] / i_lag['total_outputs'] * 100
    i_lag['green_lag'] = i_lag['pc_of_chemistry_green_chemistry'] - i_lag['percent_green']
    i_lag['gold_lag'] = i_lag['pc_of_chemistry_gold_chemistry'] - i_lag['percent_gold']

    f = px.scatter(i_lag,
                   x='green_lag',
                   y='gold_lag',
                   color='country', color_discrete_map=palette,
                   size='count_chemistry',
                   animation_frame='published_year',
                   animation_group='name',
                   hover_name='name',
                   hover_data=['percent_green', 'pc_of_chemistry_green_chemistry', 'percent_gold',
                               'pc_of_chemistry_gold_chemistry'],
                   range_x=(-30, 30), range_y=(-30, 30),
                   labels=dict(country='Country',
                               published_year='Year of Publication',
                               green_lag='Lag in Green OA (%)',
                               gold_lag='Lag in Gold OA (%)',
                               count_chemistry='# of Outputs in Chemistry',
                               percent_green='Green OA for Institution (%)',
                               percent_gold='Gold OA for Institution (%)',
                               pc_of_chemistry_green_chemistry='Green as a Proportion of Chemistry Outputs (%)',
                               pc_of_chemistry_gold_chemistry='Gold as a Proportion of Chemistry Outputs (%)'))
    f.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 700
    f.update_xaxes(showline=False, zeroline=True)
    f.update_yaxes(showline=False, zeroline=True)
    write_plotly_div(af, f, 'institutions_chemistry_lag.html')


def load_cache_data(af: AnalyticsFunction,
                    function_name: Union[str, Callable],
                    element: str):
    """Convenience function for loading preprepared DataFrames from the cache

    :param function_name:
    :param element: Component of the filecache to load
    :param af

    Downloaded query data is collected as DataFrames and stored in and HDFS store as DataFrames. This
    is a convenient function for reloading data from that frame. TODO The contents of the store should
    also be collected in a defined metadata element stored in the Analytics Function.
    """

    if callable(function_name):
        afunction_name = function_name.__name__
    else:
        afunction_name = function_name
    store_filepath = af.path_to_cached_file(
        CACHE_FILENAME, afunction_name)

    with pd.HDFStore(store_filepath) as store:
        df = store[element]

    return df


def write_plotly_div(af: AnalyticsFunction,
                     figure: go.Figure,
                     filename: Union[str, Path],
                     full_html: Optional[bool] = True,
                     include_plotlyjs: Optional[Union[str, bool]] = True,
                     auto_play: Optional[bool] = False):
    h = figure.to_html(filename,
                       full_html=full_html,
                       include_plotlyjs=include_plotlyjs,
                       auto_play=auto_play)

    for f in af.generate_file(filename):
        f.write(h)
