#! /usr/bin/env python
# -*- coding: utf-8 -*
import collections
from census_data_downloader.core.tables import BaseTableConfig
from census_data_downloader.core.decorators import register


@register
class MobilityDownloader(BaseTableConfig):
    PROCESSED_TABLE_NAME = "mobility"
    UNIVERSE = "population 1 year and over"
    RAW_TABLE_NAME = 'B07003'
    RAW_FIELD_CROSSWALK = collections.OrderedDict({
        "001E": "universe",
        "004E": "same_house",
        "007E": "moved_within_county",
        "010E": "moved_from_different_county_in_same_state",
        "013E": "moved_from_different_state",
        "016E": "moved_from_abroad",
    })


@register
class MobilityBySexDownloader(MobilityDownloader):
    PROCESSED_TABLE_NAME = "mobilitybysex"
    RAW_FIELD_CROSSWALK = collections.OrderedDict({
        "001E": "universe",
        "002E": "male_total",
        "003E": "female_total",
        "004E": "total_same_house",
        "005E": "male_same_house",
        "006E": "female_same_house",
        "007E": "total_moved_within_county",
        "008E": "male_moved_within_county",
        "009E": "female_moved_within_county",
        "010E": "total_moved_from_different_county_in_same_state",
        "011E": "male_moved_from_different_county_in_same_state",
        "012E": "female_moved_from_different_county_in_same_state",
        "013E": "total_moved_from_different_state",
        "014E": "male_moved_from_different_state",
        "015E": "female_moved_from_different_state",
        "016E": "total_moved_from_abroad",
        "017E": "male_moved_from_abroad",
        "018E": "female_moved_from_abroad"
    })


@register
class MobilityWhiteDownloader(BaseTableConfig):
    PROCESSED_TABLE_NAME = "mobilitywhite"
    UNIVERSE = "population 1 year and over"
    RAW_TABLE_NAME = 'B07004H'
    RAW_FIELD_CROSSWALK = collections.OrderedDict({
        "001E": "universe",
        "002E": "same_house",
        "003E": "moved_within_county",
        "004E": "moved_from_different_county_in_same_state",
        "005E": "moved_from_different_state",
        "006E": "moved_from_abroad"
    })


@register
class MobilityBlackDownloader(MobilityWhiteDownloader):
    PROCESSED_TABLE_NAME = "mobilityblack"
    RAW_TABLE_NAME = 'B07004B'


@register
class MobilityAsianDownloader(MobilityWhiteDownloader):
    PROCESSED_TABLE_NAME = "mobilityasian"
    RAW_TABLE_NAME = 'B07004D'


@register
class MobilityLatinoDownloader(MobilityWhiteDownloader):
    PROCESSED_TABLE_NAME = "mobilitylatino"
    RAW_TABLE_NAME = 'B07004I'