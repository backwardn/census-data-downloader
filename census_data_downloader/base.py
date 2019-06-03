#! /usr/bin/env python
# -*- coding: utf-8 -*
import os
import logging
import pathlib
from .core import downloaders, decorators
logger = logging.getLogger(__name__)


class BaseDownloader(object):
    """
    Downloads and processes ACS tables from the Census API.
    """
    THIS_DIR = pathlib.Path(__file__).parent
    YEAR_LIST = (
        2017,
        2016,
        2015,
        2014,
        2013,
        2012,
        2011,
        2010,
        2009
    )

    # All available geographies
    # (Subclasses can override this)
    GEO_LIST = (
        "nationwide",
        "states",
        "congressional_districts",
        "counties",
        "places",
        "urban_areas",
        "msas",
        "csas",
        "pumas",
        "aiannh_homelands",
        "zctas",
        "state_legislative_upper_districts",
        "state_legislative_lower_districts",
        "tracts"
    )

    def __init__(
        self,
        api_key=None,
        source="acs5",
        years=None,
        data_dir=None,
        force=False
    ):
        """
        Configuration.
        """
        # Set the inputs
        self.CENSUS_API_KEY = os.getenv("CENSUS_API_KEY", api_key)
        if not self.CENSUS_API_KEY:
            raise NotImplementedError("Census API key required. Pass it as the first argument.")
        self.source = source
        self.force = force

        #
        # Allow custom years for data download, defaulting to most recent year
        #

        # If they want all the years, give it to them.
        if years == "all":
            self.years_to_download = self.YEAR_LIST
        # If the user provides a year give them that.
        elif isinstance(years, int):
            self.years_to_download = [years]
        # Or if they provide years as a list, give those then.
        elif isinstance(years, list):
            self.years_to_download = list(map(int, years))
        # If they provided nothing, default to the latest year of data
        elif years is None:
            self.years_to_download = (max(self.YEAR_LIST),)

        # Validate the years
        for year in self.years_to_download:
            if year not in self.YEAR_LIST:
                error_msg = ("Data only available for the years "
                             f"{self.YEAR_LIST[-1]}-{self.YEAR_LIST[0]}.")
                raise NotImplementedError(error_msg)

        # Set the data directories
        if data_dir:
            self.data_dir = pathlib.Path(str(data_dir))
        else:
            self.data_dir = self.THIS_DIR.joinpath("data")
        self.raw_data_dir = self.data_dir.joinpath("raw")
        self.processed_data_dir = self.data_dir.joinpath("processed")

        # Make sure they exist
        if not self.data_dir.exists():
            self.data_dir.mkdir()
        if not self.raw_data_dir.exists():
            self.raw_data_dir.mkdir()
        if not self.processed_data_dir.exists():
            self.processed_data_dir.mkdir()

    @property
    def censusreporter_url(self):
        """
        Returns the URL of the Census Reporter page explaining the ACS table.
        """
        return f"https://censusreporter.org/tables/{self.RAW_TABLE_NAME}/"

    @decorators.downloader
    def download_nationwide(self):
        """
        Download nationwide data.
        """
        return downloaders.NationwideRawDownloader

    @decorators.downloader
    def download_states(self):
        """
        Download data for all states.
        """
        return downloaders.StatesRawDownloader

    @decorators.downloader
    def download_congressional_districts(self):
        """
        Download data for all Congressional districts.
        """
        return downloaders.CongressionalDistrictsRawDownloader

    @decorators.downloader
    def download_counties(self):
        """
        Download data for all counties.
        """
        return downloaders.CountiesRawDownloader

    @decorators.downloader
    def download_places(self):
        """
        Download data for all Census designated places.
        """
        return downloaders.PlacesRawDownloader

    @decorators.downloader
    def download_tracts(self):
        """
        Download data for all Census tracts in the provided state.
        """
        return downloaders.TractsRawDownloader

    @decorators.downloader
    def download_state_legislative_upper_districts(self):
        """
        Download data for all Census upper legislative districts in the provided state.
        """
        return downloaders.StateLegislativeUpperDistrictsRawDownloader

    @decorators.downloader
    def download_state_legislative_lower_districts(self):
        """
        Download data for all Census lower legislative districts in the provided state.
        """
        return downloaders.StateLegislativeLowerDistrictsRawDownloader

    @decorators.downloader
    def download_urban_areas(self):
        """
        Download data for all urban areas
        """
        return downloaders.UrbanAreasRawDownloader

    @decorators.downloader
    def download_msas(self):
        """
        Download data for Metropolitian Statistical Areas.
        """
        return downloaders.MsasRawDownloader

    @decorators.downloader
    def download_csas(self):
        """
        Download data for Combined Statistical Areas.
        """
        return downloaders.CsasRawDownloader

    @decorators.downloader
    def download_pumas(self):
        """
        Download data for Public Use Microdata Areas.
        """
        return downloaders.PumasRawDownloader

    @decorators.downloader
    def download_aiannh_homelands(self):
        """
        Download data for American Indian home lands.
        """
        return downloaders.AiannhHomelandsRawDownloader

    @decorators.downloader
    def download_zctas(self):
        """
        Download data for Zip Code Tabulation Areas
        """
        return downloaders.ZctasRawDownloader

    def download_everything(self):
        """
        Download 'em all.
        """
        for geo in self.GEO_LIST:
            # Get the downloader function
            dl = getattr(self, f"download_{geo}", None)
            # Validate it
            if not dl or not callable(dl):
                raise NotImplementedError(f"Invalid geography type: {geo}")
            # Run it
            dl()
