import graphene
from apiUtils.schemaObjects import SongDto, RoomDto
from common.roomManager import (
    get_room_values,
    Room,
    to_graphene_room,
    get_specific_room,
)

# from common.songManager import Playlist Song, to_graphene_song


class Query(graphene.ObjectType):
    # first declare what objects we return
    # songs = graphene.List(SongDto)
    rooms = graphene.List(RoomDto)
    room = graphene.Field(RoomDto, pin=graphene.String(required=True))

    # then create resolvers that return them
    # def resolve_songs(self, info):
    #     return list(map(to_graphene_song, songQueue))

    def resolve_rooms(self, info):
        return map(to_graphene_room, get_room_values())

    # whenever this is called a user will join the room
    def resolve_room(self, info, pin):
        target_room = get_specific_room(pin)
        target_room.create_user()
        return to_graphene_room(target_room)


# query {
#   room(pin:"1111") {
#         pin
#     usernames
#     songs {
#       title
#       url
#       likes
#       company
#     }
#   }
# }
