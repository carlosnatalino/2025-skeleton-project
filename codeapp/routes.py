# pylint: disable=cyclic-import
"""
File that contains all the routes of the application.
This is equivalent to the "controller" part in a model-view-controller architecture.
In the final project, you will need to modify this file to implement your project.
"""
# built-in imports
import io

# external imports
from flask import Blueprint, jsonify, render_template
from flask.wrappers import Response as FlaskResponse
from matplotlib.figure import Figure
from tabulate import tabulate
from werkzeug.wrappers.response import Response as WerkzeugResponse

# internal imports
from codeapp.models import Show
from codeapp.utils import calculate_statistics, get_data_list, prepare_figure

# define the response type
Response = str | FlaskResponse | WerkzeugResponse

bp = Blueprint("bp", __name__, url_prefix="/")


################################### web page routes ####################################


@bp.get("/")  # root route
def home() -> Response:
    # gets dataset
    dataset: list[Show] = get_data_list()

    # get the statistics that is supposed to be shown
    counter: dict[int, int] = calculate_statistics(dataset)

    # convert the dictionary into a list of tuples
    final_list = []
    for key in sorted(counter.keys()):
        final_list.append((key, counter[key]))

    # generate the HTML table
    html_table = tabulate(
        final_list,
        headers=["Year", "Count"],
        tablefmt="html",
        colalign=["left", "left"],
    )

    # make nice formatting -- always use this line
    bootstrap_table = html_table.replace(
        "<table>", """<table class="table table-bordered table-hover">"""
    )

    # render the page
    return render_template("home.html", table=bootstrap_table)


@bp.get("/data/")
def data() -> Response:
    # gets dataset
    dataset: list[Show] = get_data_list()

    # generate the table
    html_table = tabulate(
        dataset[0:100],
        headers=[
            "ID",
            "Type",
            "Title",
            "Director",
            "Cast",
            "Country",
            "Date added",
            "Release year",
            "Duration",
            "Listed in",
            "Description",
            "Rating",
        ],
        tablefmt="html",
    )

    # make nice formatting -- always use this line
    bootstrap_table = html_table.replace(
        "<table>", """<table class="table table-bordered table-hover">"""
    )

    # render the page
    return render_template("data.html", html=bootstrap_table)


@bp.get("/image")
def image() -> Response:
    # gets dataset
    dataset: list[Show] = get_data_list()

    # get the statistics that is supposed to be shown
    counter: dict[int, int] = calculate_statistics(dataset)

    # creating the plot

    fig = Figure()
    fig.gca().bar(
        list(sorted(counter.keys())),
        [counter[x] for x in sorted(counter.keys())],
        color="gray",
        # alpha=0.5,
        zorder=2,
    )
    fig.gca().plot(
        list(sorted(counter.keys())),
        [counter[x] for x in sorted(counter.keys())],
        marker="x",
        color="#25a8a6",
        zorder=1,
    )
    fig.gca().grid(ls=":", zorder=1)
    fig.gca().set_xlabel("Release Year")
    fig.gca().set_ylabel("Number of shows")
    fig.tight_layout()

    ################ START -  THIS PART MUST NOT BE CHANGED BY STUDENTS ################
    # create a string buffer to hold the final code for the plot
    output = io.StringIO()
    fig.savefig(output, format="svg")
    # output.seek(0)
    final_figure = prepare_figure(output.getvalue())
    return FlaskResponse(final_figure, mimetype="image/svg+xml")


@bp.get("/about")
def about() -> Response:
    return render_template("about.html")


################################## web service routes ##################################


@bp.get("/json-dataset")  # root route
def get_json_dataset() -> Response:
    # gets dataset
    dataset: list[Show] = get_data_list()

    # render the page
    return jsonify(dataset)


@bp.get("/json-stats")  # root route
def get_json_stats() -> Response:
    # gets dataset
    dataset: list[Show] = get_data_list()

    # get the statistics that is supposed to be shown
    counter: dict[int, int] = calculate_statistics(dataset)

    # render the page
    return jsonify(counter)
