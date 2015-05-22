# -*- coding: utf-8 -*-

"""
marksweep.utils
~~~~~~~~~~~~~~~

this module contains functions that help our code stay DRY.

contents:
    lazygen - consumes Facebook Graph properties and returns generators
    that contains the desired nodes or edges. The generator also handles
    pagination when required.
"""

from itpy import Itpy
from fbms.fbo import FBO
from fbms.usr import User

__author__ = 'JasonLiu'

def graph_query(wrapper, source, edges, limit, get_all):
    """


    :type wrapper: FBO
    :type graph: GraphAPI
    :rtype : Itpy

    :param graph:
    :param edges:
    :param source:
    :param wrapper:
    :param limit:
    :param get_all:
    :return:
    """
    return Itpy(api_loop(wrapper, source, edges, limit, get_all))


def api_loop(graph, wrapper, source, edges, limit=100, get_all=False):
    """

    :param graph:
    :param wrapper:
    :param source:
    :param edges:
    :param limit:
    :param get_all:
    :return:
    """
    response = User.singleton.graph.get_connections(source, edges, limit=limit)
    items = (wrapper(item) for item in response["data"])
    for item in items:
        yield item
        # Lazily go to next page if required
        if (get_all and response["data"]):
            try:
                next_page = trim(response["paging"]["next"])
                response = User.singleton.graph.request(next_page)
                items = (wrapper(item) for items in response["data"])
            except KeyError:
                pass


def trim(paging_url):
    """trims the paging url to the uri"""
    return paging_url[26:]
