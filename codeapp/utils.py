# built-in imports
from datetime import date, datetime
import collections
import math
import pickle

# external imports
from flask import current_app
import requests

# internal imports
from codeapp import db
from codeapp.models import Show


def get_data_list() -> list[Show]:
    """
    Function responsible for downloading the dataset from the source, translating it
    into a list of Python objects, and saving each object to a Redis list.
    """

    ##### check if dataset already exists, and if so, return the existing dataset  #####
    # db.delete("dataset_list")  # uncomment if you want to force deletion
    if db.exists("dataset_list") > 0:  # checks if the `dataset` key already exists
        current_app.logger.info("Dataset already downloaded.")
        dataset_stored: list[Show] = []  # empty list to be returned
        raw_dataset: list[bytes] = db.lrange("dataset_list", 0, -1)  # get list from DB
        for raw_item in raw_dataset:
            dataset_stored.append(pickle.loads(raw_item))  # load item from DB
        return dataset_stored

    ################# dataset has not been downloaded, downloading now #################
    current_app.logger.info("Downloading dataset.")
    url: str = "https://onu1.s2.chalmers.se/datasets/amazon_prime_titles.json"
    response = requests.get(url, timeout=200)

    ########################## saving dataset to the database ##########################
    dataset_base: list[Show] = []  # list to store the items
    # for each item in the dataset...
    # data: list[dict[str, str]] = response.json()

    data: list[dict[str, str]] = response.json()

    for item in data:
        # check if the date can be parsed
        date_added: date | None = None
        try:
            date_added = datetime.strptime(item["date_added"], "%B %d, %Y").date()
        except Exception:
            pass

        # check the value of director
        director = None
        if item["director"] is not None and str(item["director"]) != "nan":
            director = item["director"]

        # check the value of cast
        cast = None
        if item["cast"] is not None and str(item["cast"]) != "nan":
            cast = item["cast"]

        # check the value of country
        country = None
        if item["country"] is not None and str(item["country"]) != "nan":
            country = item["country"]

        # check the value of rating
        rating = None
        if item["rating"] is not None and str(item["rating"]) != "nan":
            rating = item["rating"]

        # create a new object
        new_show = Show(
            id=item["show_id"],
            type=item["type"],
            title=item["title"],
            director=director,
            cast=cast,
            country=country,
            date_added=date_added,
            release_year=int(item["release_year"]),
            rating=rating,
            duration=item["duration"],
            listed_in=item["listed_in"],
            description=item["description"],
        )
        # push object to the database list
        db.rpush("dataset_list", pickle.dumps(new_show))
        dataset_base.append(new_show)  # append to the list

    return dataset_base


def calculate_statistics(dataset: list[Show]) -> dict[int, int]:
    """
    Receives the dataset in the form of a list of Python objects, and calculates the
    statistics necessary.
    """
    # create the counter
    counter: dict[int, int] = collections.defaultdict(lambda: 0)
    for item in dataset:
        counter[item.release_year] += 1

    return counter


def prepare_figure(input_figure: str) -> str:
    """
    Method that removes limits to the width and height of the figure. This method must
    not be changed by the students.
    """
    output_figure = input_figure.replace('height="345.6pt"', "").replace(
        'width="460.8pt"', 'width="100%"'
    )
    return output_figure
