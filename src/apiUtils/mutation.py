import graphene

# import namesgenerator
from apiUtils.schemaObjects import SongDto, RoomDto
from common.roomManager import (
    get_specific_room,
    create_room,
    to_graphene_room,
    reset_rooms,
)
from common.songManager import Playlist, Song
from random import randint
from flask_socketio import SocketIO, emit

# import json
# import __main__
from apiUtils.socket_methods import emit_playlist, emit_usernames

# from __main__ import socketio


class PutSong(graphene.Mutation):
    # what the muatition returns
    songs = graphene.Field(graphene.List(SongDto))

    # arguments that can be passed in to the mutation
    class Arguments:
        pin = graphene.String()
        title = graphene.String()
        url = graphene.String()
        username = graphene.String(required=False, default_value="Host")
        company = graphene.String(required=False, default_value="YOUTUBE")

    # function that resolves the mutation
    def mutate(self, info, pin, title, url, username, company):
        # if info.context.get("is_vip"):
        # username = username.upper()
        player = get_specific_room(pin).playlist
        player.append_song(
            Song(url=url, title=title, company=company, username=username)
        )
        # socket io emitting to everybody in room
        emit_playlist(player.get_serialized_songs())

        # emit("playlist_channel", {"data": message["data"]}, broadcast=True)
        return PutSong(player.get_graphene_songs())


class DequeueSong(graphene.Mutation):
    songs = graphene.Field(graphene.List(SongDto))

    class Arguments:
        pin = graphene.String()
        first = graphene.Int(required=False, default_value=1)

    def mutate(self, info, pin, first):
        player = get_specific_room(pin).playlist
        player.dequeue_songs(first=first)
        emit_playlist(player.get_serialized_songs())

        return DequeueSong(player.get_graphene_songs())


class RemoveSong(graphene.Mutation):
    songs = graphene.Field(graphene.List(SongDto))

    class Arguments:
        pin = graphene.String()
        title = graphene.String()

    def mutate(self, info, pin, title):
        player = get_specific_room(pin).playlist
        song = player.get_specific_song(title)
        player.remove_song(song)
        emit_playlist(player.get_serialized_songs())

        return RemoveSong(player.get_graphene_songs())


class LikeSong(graphene.Mutation):
    songs = graphene.Field(graphene.List(SongDto))

    class Arguments:
        pin = graphene.String()
        title = graphene.String()

    def mutate(self, info, pin, title):
        player = get_specific_room(pin).playlist
        player.like_song(title)
        # socket io emitting to everybody in room
        emit_playlist(player.get_serialized_songs())

        return LikeSong(player.get_graphene_songs())


class AddUser(graphene.Mutation):
    username = graphene.Field(graphene.String)

    class Arguments:
        pin = graphene.String()

    # function that resolves the mutation
    def mutate(self, info, pin):
        room = get_specific_room(pin)
        username = room.create_user()

        # socket io emitting to everybody in room
        emit_usernames(room.usernames)
        return AddUser(username)


class PutRoom(graphene.Mutation):
    room = graphene.Field(RoomDto)

    class Arguments:
        clear = graphene.Boolean(required=False, default_value=False)

    def mutate(self, info, clear):
        if clear:
            reset_rooms()
        return PutRoom(to_graphene_room(create_room()))


class Mutation(graphene.ObjectType):
    put_song = PutSong.Field()
    dequeue_song = DequeueSong.Field()
    remove_song = RemoveSong.Field()
    like_song = LikeSong.Field()
    add_user = AddUser.Field()
    put_room = PutRoom.Field()


# mutation { putSong (title: "t4", url: "u5", pin:"1111") { songs { title url likes } }}
# mutation { putSong (title: "t4", url: "u5", pin:"1111", username: "guy", company:"SPOTIFY") { songs { title url likes username company} }}


# mutation {
#   likeSong(title: "t4", pin:"1111") {
#     songs {
#       title
#       url
#       likes
#     }
#   }
# }


# mutation {
# 	putRoom {
#     room {
#       usernames
#       pin
#       songs {
#         title
#         url
#         likes
#         company
#       }
#     }
#   }
# }
