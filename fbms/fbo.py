# -*- coding: utf-8 -*-

"""
marksweep.fbobject
~~~~~~~~~~~~~~~~~~

This module contains the classes and methods required to simulate a
facebook user.
"""

__author__ = 'JasonLiu'

from fbms.usr import *
from fbms.utils import graph_query
from itpy import Itpy
from json import dumps


class FBO(object):

    graph = User.singleton.graph()

    def __init__(self, data):
        self.data = data

    def comment(self, message):
        return self.graph.put_comment(self.id, message)

    def like(self):
        return self.graph.put_like(self.id)

    def __getattr__(self, item):
        if item in self.data:
            return self.data[item]
        return getattr(self, item, None)

    def __getitem__(self, item):
        if item in self.data:
            return self.data[item]
        return getattr(self, item, None)

    def __repr__(self):
        return self.data.__repr__()

    def __str__(self, *args, **kwargs):
        return dumps(self.data, *args, **kwargs)

    def _pprint(self):
        print(dumps(self.data, indent=4))


class Like(FBO):
    pass


class Comment(FBO):

    @property
    def user(self):
        return self["from"]

    def get_likes(self, limit=100, all=True):
        source, edge = self.id, "likes"
        return graph_query(
            Like, source, edge, limit=limit, get_all=all
        )

    # def get_replies(self, limit=100, all=True):
    #     source, edge = self.id, "likes"
    #     return graph_query(
    #         Like, source, edge, limit=limit, get_all=all
    #     )


class Post(FBO):

    @property
    def user(self):
        return self["from"]

    @property
    def get_post_id(self):
        """
        :return: facebook post id
        """
        return self["id"].split("_")[1]

    @property
    def get_group_id(self):
        """
        :return: facebook group id of post
        """
        return self.data["id"].split("_")[0]

    def get_comments(self, limit=100, all=True):
        source, edge = self.id, "comments"
        return graph_query(
            Comment, source, edge, limit=limit, get_all=all
        )

    def get_likes(self, limit=100, all=True):
        source, edge = self._id, "likes"
        return graph_query(
            Like, source, edge, limit=limit, get_all=all
        )

    def delete(self):
        return self.graph.delete_object(self.id)

class Group(FBO):

    def get_posts(self, limit=100, all=True):
        """


        :rtype : Itpy
        :param limit:
        :param all:
        :return:
        """
        source, edge = self.id, "feed"
        return graph_query(
            Post, source, edge, limit=limit, get_all=all
        )

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Messages and InboxThreads are not supported at this time
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# class Message(FBObject):
#
#     @property
#     def sender(self):
#         return self.__dict__["from"].name
#
#
# class InboxThread(FBObject):
#
#     def messages(self, limit=1000, all=False):
#         source, edge = self.id, "comments"
#         return lazygen(
#             Message, source, edge, limit=limit, get_all=all
#             )
#
