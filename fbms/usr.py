# -*- coding: utf-8 -*-

"""
marksweep.user
~~~~~~~~~~~~~~

This module contains User() which models the basic actions a user can go over the Facebook Graph API.

In the future we will need to be able to handle connection pools if we want to crawl more intensely
While not all endpoints have been implemented, a user instance can get all groups, and all inbox messages
from the Graph API along with posting a status to their news feed.
"""

__author__ = 'JasonLiu'

from fbms.fbo import *
from fbms.utils import graph_query
from fbms.config import ACCESS_TOKEN, APP_ID, APP_SECRET

from facebook import GraphAPI
from time import sleep, time


class User(object):
    class __User(object):
        def __init__(self):
            self.call_counter = 0
            self.__graph = GraphAPI(ACCESS_TOKEN)
            self.__graph.extend_access_token(APP_ID, APP_SECRET)
            self.timer = time()

        def _time_since_last_nap(self):
            return time() - self.timer

        @staticmethod
        def graph(self):
            """

            :rtype : GraphAPI
            """
            self.call_counter += 1
            if (self.call_counter > 600 or self._time_since_last_nap() > 600):
                sleep(60)
                self.timer = time()
                self.call_counter = 0
            return self.__graph

    singleton = __User()

    @classmethod
    def get_groups(cls, limit=100, all=True):
        source, edge = "me", "groups"
        return graph_query(Group, source, edge, limit, all)

    # @classmethod
    # def get_status(cls, limit=100, all=True):
    #     source, edge = "me", "???"
    #     return graph_query(cls.singleton.graph, ???, source, edge, limit, all)
    #
    # @classmethod
    # def get_messages(cls, limit=100, all=True):
    #     source, edge = "me", "???"
    #     return graph_query(cls.singleton.graph, ???, source, edge, limit, all)