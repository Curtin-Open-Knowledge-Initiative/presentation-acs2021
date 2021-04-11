from observatory.reports import chart_utils
from observatory.reports.tables import GenericOpenAccessTable, AbstractObservatoryTable, GenericFundersTable

class GroupDevFundersTable(GenericFundersTable):
    """
    Updates to the Funder table to capture funder type
    """

    sql_template = """
    SELECT
      table.id as id,
      table.name as name,
      table.country as country,
      table.country_code as country_code,
      table.region as region,
      table.subregion as subregion,
      years.published_year as published_year,
      years.metrics.total as total,
      funders.name as funder,
      funders.country as funder_country,
      funders.funding_body_type as funder_type,
      funders.count as count,
      funders.oa as oa,
      funders.gold as gold,
      funders.green as green
    FROM `{bq_table}` as table,
      UNNEST(years) as years,
      UNNEST(years.funders) as funders
    WHERE
        years.published_year > {year_range[0]} and
        years.published_year < {year_range[1]} and
        funders.count > 2 
        {scope}
    """


class GenericDisciplinesTable(GenericOpenAccessTable):
    """
    First pass at grabbing discipline level data for analysis
    """

    sql_template = """
    SELECT
      table.id as id,
      table.name as name,
      table.country as country,
      table.country_code as country_code,
      table.region as region,
      table.subregion as subregion,
      table.time_period as published_year,
      table.total_outputs as total,
      discipline.field as field,
      discipline.total_outputs as count,
      discipline.num_oa_outputs as oa,
      discipline.num_gold_outputs as gold,
      discipline.num_green_outputs as green
    FROM `{bq_table}` as table,
      UNNEST(disciplines.level0) as discipline
    WHERE
        table.time_period > {year_range[0]} and
        table.time_period < {year_range[1]}
        {scope}
    """

    def clean_data(self):
        """Clean data
        """

        chart_utils.calculate_percentages(self.df,
                                          ['oa', 'green', 'gold'],
                                          'count')
        chart_utils.calculate_percentages(self.df,
                                          ['count'],
                                          'total')
        super().clean_data()

class GenericEventsTable(AbstractObservatoryTable):
    """Generic table class for Journals
    """

    sql_template = """
SELECT
  table.id as id,
  table.name as name,
  table.country as country,
  table.country_code as country_code,
  table.region as region,
  table.subregion as subregion,
  years.published_year as published_year,
  years.metrics.total as total,
  event.source as source,
  event.count as count,
  event.oa as oa,
  event.gold as gold,
  event.green as green
FROM `{bq_table}` as table,
  UNNEST(years) as years,
  UNNEST(years.events) as event
WHERE
    years.published_year > {year_range[0]} and
    years.published_year < {year_range[1]} and
    event.count > 1 
    {scope}
"""