from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# import queue
from queue import Queue


q = Queue()
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# traversal_path = []

def traverse_path(player, moving):
    q = Queue()
    visited = set()
    q.enqueue([player.current_room.id])
    while q.size() > 0:
        deque = q.dequeue()
        prev_rm = deque[-1]
        if prev_rm not in visited:
            visited.add(prev_rm)
            for i in graph[prev_rm]:
                if graph[prev_rm][i] == "?":
                    return deque
                else:
                    lost = list(deque)
                    lost.append(graph[prev_rm][i])
                    q.enqueue(lost)
    return []


def player_moves(player, queue):
    possible_moves = graph[player.current_room.id]
    new_moves = []

    for moving in possible_moves:
        if possible_moves[moving] == "?":
            new_moves.append(moving)
    if len(new_moves) == 0:
        new_rooms = traverse_path(player, queue)
        room_num = player.current_room.id
        for next in new_rooms:
            for moving in graph[room_num]:
                if graph[room_num][moving] == next:
                    queue.enqueue(moving)
                    room_num = next
                    break

    else:
        queue.enqueue(new_moves[random.randint(0, len(new_moves) - 1)])

#setup attempts at traversal
try_attempts = 300
#setup efficient length
effecient_len = 977
#setup efficient path storage
effecient_path = []


#setup loop for traversal
for i in range(try_attempts):
    player = Player(world.starting_room)
    graph = {}
    new_room = {}

    for moving in player.current_room.get_exits():
        new_room[moving] = "?"
    graph[world.starting_room.id] = new_room

    rev_dir = {"n": "s", "s": "n", "e": "w", "w": "e"}

    q = Queue()
    total_moves = []
    player_moves(player, q)

    while q.size() > 0:
        first = player.current_room.id
        go = q.dequeue()
        player.travel(go)
        total_moves.append(go)
        q_last = player.current_room.id
        graph[first][go] = q_last
        if q_last not in graph:
            graph[q_last] = {}
            for i in player.current_room.get_exits():
                graph[q_last][i] = "?"
        graph[q_last][rev_dir[go]] = first
        if q.size() == 0:
            player_moves(player, q)
    if len(total_moves) < effecient_len:
        effecient_path = total_moves
        effecient_len = len(total_moves)

#assign traversal path to the most efficient path
traversal_path = effecient_path

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
