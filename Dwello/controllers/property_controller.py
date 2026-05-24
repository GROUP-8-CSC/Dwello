from database.db_properties import (
    fetch_properties,
    fetch_all_properties,
    search_by_neighborhood
)


def search_properties_controller(region, budget):

    if not region:
        return []

    try:
        budget = int(budget)

    except ValueError:
        return []

    properties = fetch_properties(
        region,
        budget
    )

    return properties


def fetch_all_properties_controller():

    return fetch_all_properties()


def search_neighborhood_controller(neighborhood):

    if not neighborhood:
        return []

    return search_by_neighborhood(neighborhood)