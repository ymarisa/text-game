class Direction:
    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"
    def is_direction(s):
        if s == Direction.NORTH.upper() or s == Direction.SOUTH.upper() or s == Direction.EAST.upper() or s == Direction.WEST.upper():
            return True
        else:
            return False

class Game:
    PROMPT = "You are in {{CURRENT_LOCATION}}." + \
    "\n{{DESCRIPTION}}" + \
    "\nBag contents: {{BAG}}" + \
    "\n{{OPTIONS}}" + \
    "\n{{INSTRUCTIONS}}\n"

    def __init__(self, game_map, items, npcs, start_location, instructions):
        self.items = items
        self.game_map = game_map
        self.npcs = npcs
        self.current_location = start_location    #Room object
        self.instructions = instructions
        self.bag = Items()

    #for debugging
    def print_locations(self):
        pass

    def get_items(self):
        return self.items

    def get_current_location(self):
        return self.current_location

    def move_room(self, direction):
        print("move to " + self.current_location.get_door(direction).get_name())
        new_room = self.current_location.get_door(direction)
        self.current_location = new_room
        # announce who is in room

    def get_bag(self):
        return self.bag

    def add_to_bag(self, item):
        self.bag.add_item(item)

    def remove_from_bag(self, item):
        self.bag.remove_item(item)

    def is_won(self):
        return self.current_location == self.game_map.get_room("room2") and self.bag.contains("gem")

        # combine valid directions of travel with other actions into a list of valid actions
    def get_actions(self):
        doors = self.current_location.get_next_location_list()
        actions = doors + self.instructions 
        return [x.upper() for x in actions]

    def get_prompt(self, actions):
        current_prompt = self.PROMPT.replace("{{CURRENT_LOCATION}}", self.current_location.get_name())
        current_prompt = current_prompt.replace("{{BAG}}", self.bag.to_string())
        current_prompt = current_prompt.replace("{{DESCRIPTION}}", self.current_location.get_description())
        
        current_prompt = current_prompt.replace("{{OPTIONS}}", self.current_location.get_next_location_option_string())
        current_prompt = current_prompt.replace("{{INSTRUCTIONS}}", "Choose an action: " + ", ".join(actions))

        return current_prompt

    def prompt_and_execute(self):
        actions = self.get_actions()
        if self.is_won():
            print("Yay! You won. Goodbye, come again soon.")
            exit
        while(True):
            choice = input(self.get_prompt(actions))
            choice = choice.upper()
            ## TODO: give feedback for why a choice didn't work (ie door doesn't exist)
            if choice not in actions:
                print("Not a valid option. Try again\n")
                continue
            elif choice == "QUIT": # TODO fix to ref
                print("Thanks for playing! Come again soon.")
                break
            elif Direction.is_direction(choice) and self.current_location.valid_door(choice):
                self.move_room(choice)
            elif choice == "TAKE":
                pass
            elif choice == "GREET":
                pass


class Room:
    def __init__(self, name, items, doors, description, who):
        self.name = name
        self.items = items
        self.doors = doors
        self.description = description
        self.who = who

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_next_location_option_string(self):
        next_locations = ""
        for door in self.doors:
            next_locations = next_locations + f"{door}: {self.doors[door].get_name()}\n"
        return next_locations

    def get_next_location_list(self):
        return list(self.doors)

    def set_door(self, direction, room):
        self.doors[direction.upper()] = room

    def valid_door(self, direction):
        return direction.upper() in list(self.doors)

    def get_door(self, direction):
        return self.doors[direction.upper()]

    def leave(self, npc):
        who.remove(npc)

    def enter(self, npc):
        who.append(npc)

    def who_is_there(self):
        return who

    def __str__(self):
        return self.name

class NPC:
    def __init__(self, name, item, room, lines):
        self.name = name
        self.room = room
        self.bag = item
        self.lines = lines

    def move_rooms(self, room):
        self.room.leave(self)
        self.room = room
        self.room.enter(self)

    def has_key(self):
        return self.bag != None

    def give_key(self):
        item = self.bag
        self.bag = None
        return item

    def get_lines(self):
        return self.lines

class Lines:
    def __init__(self, greet, answer_no, answer_yes):
        self.greet = greet
        self.answer_no = answer_no
        self.answer_yes = answer_yes

    def greet(self):
        return self.greet

    def answer_yes(self):
        return self.answer_yes

    def answer_no(self):
        return self.answer_no

class Game_Map:
    def __init__(self):
        self.rooms = {}

    def add_room(self, room):
        self.rooms[room.get_name()] = room

    def get_room(self, name):
        return self.rooms[name]

    def connect_room(self, room1, room2, direction1, direction2):
        room1.set_door(direction1, room2)
        room2.set_door(direction2, room1)

    def connect_room_by_name(self, room1_name, room2_name, direction1, direction2):
        room1 = self.rooms[room1_name]
        room2 = self.rooms[room2_name]
        self.connect_room(room1, room2, direction1, direction2)

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def to_string(self):
        return f"{self.name}: {self.description}"

class Items:
    def __init__(self):
        self.items = {}

    def add_item(self, item):
        self.items[item.get_name()] = item

    def remove_item(self, item):
        return self.items.pop(item.get_name(), None)

    def get_item_by_name(self, name):
        return self.items[name]

    def to_string(self):
        s = ""
        if len(self.items) > 0:
            for i in self.items:
                s = s + "\n" + i.to_string()
        else:
            s = "Empty"
        return s

def make_Castle():
    # items = {
    #         "gem": "gem description",
    #         "candlestick" : "candlestick description"
    # }

    game_items = Items()
    game_items.add_item(Item("gem", "gem description"))
    game_items.add_item(Item("candlestick", "candlestick description"))


    castle_map = Game_Map()
    castle_map.add_room(Room("room0", [], {}, "0 foobar test description", []))
    castle_map.add_room(Room("room1", [], {}, "1 foobar test description", []))
    castle_map.add_room(Room("room2", [game_items.get_item_by_name("candlestick")], {}, "2 foobar test description", []))
    castle_map.add_room(Room("room3", [], {}, "3 foobar test description", []))

    castle_map.connect_room_by_name("room0", "room1", Direction.SOUTH, Direction.NORTH)
    castle_map.connect_room_by_name("room1", "room2", Direction.EAST, Direction.WEST)
    castle_map.connect_room_by_name("room2", "room3", Direction.NORTH, Direction.SOUTH)
    castle_map.connect_room_by_name("room3", "room0", Direction.EAST, Direction.WEST)

    # NPC: item, lines
    NPCs = {
        "Woody": NPC("Woody", game_items.get_item_by_name("gem"), castle_map.get_room("room0"),
            lines=Lines(greet="Howdy", answer_yes="Yes indeed", answer_no="I'm afraid not"))
    }

    # locations = {
    #         "room0": Room("room0", [], {}, "0 foobar test description", []),
    #         "room1": Room("room1", [], {}, "1 foobar test description", []),
    #         "room2": Room("room2", [items["candlestick"]], {}, "2 foobar test description", []),
    # }

    # #TODO: change the ref to self.locations
    # locations["room0"].set_door(Directions.SOUTH, locations["room1"])
    # locations["room1"].set_door(Directions.NORTH, locations["room0"])

    # locations["room1"].set_door(Directions.EAST, locations["room2"])
    # locations["room2"].set_door(Directions.WEST, locations["room1"])
    
    # locations["room2"].set_door(Directions.EAST, locations["room0"])
    # locations["room0"].set_door(Directions.WEST, locations["room2"])

    prompt_instructions = ["TAKE", "GREET", "QUIT"]
    g = Game(castle_map, game_items, NPCs, castle_map.get_room("room0"), prompt_instructions)
    return g

def main():
    g = make_Castle()
    # g.print_locations()
    g.prompt_and_execute()



if __name__ == "__main__":
    main()