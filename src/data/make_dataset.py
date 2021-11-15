# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import pandas as pd


@click.command()
@click.argument("input_dirpath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path())
def main(
    input_dirpath="../../data/raw/",
    output_filepath="../../data/processed/clean_data.csv",
):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")
    raw_dir = Path(input_dirpath)

    aggReports = None

    def clean_data(x):
        if isinstance(x, str):
            x = x.strip()
        return x

    for p in list(raw_dir.glob("*.csv")):
        curr_df = pd.read_csv(p, encoding="unicode_escape")

        column_map = {x: x.lower().replace(" ", "_") for x in curr_df.columns}
        curr_df = curr_df.rename(columns=column_map)
        curr_df = curr_df.rename(
            columns={"meddra_preferred_terms": "medra_preferred_terms"}
        )
        curr_df = curr_df.applymap(clean_data)

        aggReports = curr_df if aggReports is None else pd.concat([aggReports, curr_df])

    aggReports.to_csv(output_filepath)


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()