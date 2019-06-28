from pprint import pprint

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
    PROMPT = "=======================================" + \
    "\nYou are in {{CURRENT_LOCATION}}." + \
    "\n{{DESCRIPTION}}" + \
    "{{ITEM_DESCRIPTION}}" + \
    "{{NPC}}" + \
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
        print("Moving to " + self.current_location.get_door(direction).get_name() + "\n")
        new_room = self.current_location.get_door(direction)
        self.current_location = new_room
        # announce who is in room
        # announce item in the room

    def action_take_item_name(self, item_name):
        if not item_name in self.current_location.what_items():
            return "You cannot take that."
        else:
            item = self.current_location.get_item_by_name(item_name)
            self.current_location.remove_item(item)
            self.bag.add_item(item)
            return f"You put {item_name} in your bag.\n"

    def action_take(self):
        # TODO: change this to work for more than 1 item per room, this just takes the first one for now
        l = self.current_location.what_items()
        if len(l) > 0:
            name = l.pop()
            return self.action_take_item_name(name)
        else:
            return "You cannot take anything."

    def action_greet_npc_name(self, npc_name):
        npc = self.current_location.get_npc_by_name(npc_name)
        # print(npc.get_lines().get_greet())
        return npc.get_lines().get_greet()

    def action_greet(self):
        w = self.current_location.who_is_there()
        if len(w) > 0:
            name = w.pop()
            print("here: " + name)
            s =  name + " says: \"" + self.action_greet_npc_name(name) + "\"\n" 
            npc = self.current_location.get_npc_by_name("Tall dark stranger")
            if npc.has_item():
                s = s + "You have recieved a gleaming red gem the size of a skittle\n"
                self.bag.add_item(npc.give_item())
            return s
        else:
            return "There is no one to greet."

    def get_bag(self):
        return self.bag

    def add_to_bag(self, item):
        self.bag.add_item(item)

    def remove_from_bag(self, item):
        self.bag.remove_item(item)

    def is_won(self):
        #TODO: abstract this, take out literals
        cond1 = self.current_location == self.game_map.get_room("Kitchen") 
        cond2 = "gem" in self.bag.get_names()
        cond3 = "candlestick" in self.bag.get_names()
        return cond1 and cond2 and cond3

    # combine valid directions of travel with other actions into a list of valid actions
    def get_actions(self):
        doors = self.current_location.get_next_location_list()
        actions = doors + self.instructions
        items = self.current_location.what_items()
        return [x.upper() for x in actions]

    def get_prompt(self, actions):
        current_prompt = self.PROMPT.replace("{{CURRENT_LOCATION}}", self.current_location.get_name())
        current_prompt = current_prompt.replace("{{BAG}}", self.bag.to_string())
        current_prompt = current_prompt.replace("{{DESCRIPTION}}", self.current_location.get_description())
        
        #TODO: refactor this
        if len(self.current_location.what_items()) > 0:
            i_name = self.current_location.what_items()[0]
            desc =  self.current_location.get_item_by_name(i_name).get_description()
            current_prompt = current_prompt.replace("{{ITEM_DESCRIPTION}}", "\nYou notice: " + desc)
        else:
            current_prompt = current_prompt.replace("{{ITEM_DESCRIPTION}}", "")

        #TODO: refactor this
        if len(self.current_location.who_is_there()) > 0:
            npc_name =  self.current_location.who_is_there()[0] 
            desc = self.current_location.get_npc_by_name(npc_name).get_description()
            current_prompt = current_prompt.replace("{{NPC}}", "\nYou see someone: " + desc)
        else:
            current_prompt = current_prompt.replace("{{NPC}}", "")

        current_prompt = current_prompt.replace("{{OPTIONS}}", self.current_location.get_next_location_option_string())
        current_prompt = current_prompt.replace("{{INSTRUCTIONS}}", "Choose an action: " + ", ".join(actions))

        return current_prompt

    def prompt_and_execute(self):
        keep_playing = True
        while(keep_playing):
            if self.is_won():
                print("Yay! You won. Goodbye, come again soon.\n")
                keep_playing = False
            else:
                actions = self.get_actions()
                choice = input(self.get_prompt(actions))
                choice = choice.split(" ")
                # print(choice)

                ## TODO: give feedback for why a choice didn't work (ie door doesn't exist)
                ## TODO: abstract this so there are no literals and can link actions to functions outside of game class
                if choice[0].upper() == "QUIT": # TODO fix to ref instead of literal
                    print("Thanks for playing! Come again soon.\n")
                    break
                elif self.current_location.valid_door(choice[0].upper()):
                    self.move_room(choice[0].upper())
                elif choice[0].upper() == "TAKE":
                    print(self.action_take())
                elif choice[0].upper() == "GREET":
                    print(self.action_greet())
                else:
                    print("Not a valid option. Try again\n")
                    continue


class Room:
    def __init__(self, name, items, doors, description, who):
        self.name = name
        self.items = items
        self.doors = doors
        self.description = description
        self.who = who # TODO: abstract this

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

    def leave(self, npc_name):
        self.who.pop(npc_name, None)

    def enter(self, npc):
        self.who[npc.get_name()] = npc

    def who_is_there(self):
        return list(self.who)

    def get_npc_by_name(self, name):
        return self.who[name]

    def what_items(self):
        return self.items.get_names()

    def get_item_by_name(self, name):
        return self.items.get_item_by_name(name)

    def add_item(self, item):
        self.items.add_item(item)

    def remove_item(self, item):
        self.items.remove_item(item)

    def __str__(self):
        return self.name

class NPC:
    def __init__(self, name, description, item, room, lines):
        self.name = name
        self.description = description
        self.room = room
        self.bag = item
        self.lines = lines

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def move_rooms(self, room):
        self.room.leave(self)
        self.room = room
        self.room.enter(self)

    def has_item(self):
        return self.bag != None

    def give_item(self):
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

    def get_greet(self):
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

    def get_names(self):
        return list(self.items)

    def to_string(self):
        s = ""
        if len(self.items) > 0:
            for i in self.items:
                s = s + "\n    " + self.items[i].to_string()
        else:
            s = "Empty"
        return s

def make_Castle():
    game_items = Items()
    game_items.add_item(Item("gem", "a gleaming red gem the size of a skittle"))
    game_items.add_item(Item("candlestick", "a candlestick with a small stub of candle still burning"))

    candle_room_items = Items()
    candle_room_items.add_item(game_items.get_item_by_name("candlestick"))
    # pprint(tmp.to_string())

    castle_map = Game_Map()
    castle_map.add_room(Room("Great hall", Items(), {}, "A large echoing chamber with tapestry on the walls.", {}))
    castle_map.add_room(Room("Narrow hallway", Items(), {}, "A dim torch illuminates the short and narrow passage.", {}))
    castle_map.add_room(Room("Kitchen", candle_room_items, {}, "A fire burns in the hearth with a cauldron hanging over it bubbling.", {}))
    castle_map.add_room(Room("Drawing room", Items(), {}, "A room with huge windows and fancy furniture", {}))

    castle_map.connect_room_by_name("Great hall", "Narrow hallway", Direction.SOUTH, Direction.NORTH)
    castle_map.connect_room_by_name("Narrow hallway", "Kitchen", Direction.EAST, Direction.WEST)
    castle_map.connect_room_by_name("Kitchen", "Drawing room", Direction.NORTH, Direction.SOUTH)
    castle_map.connect_room_by_name("Drawing room", "Great hall", Direction.EAST, Direction.WEST)

    # NPC: item, lines
    NPCs = {
        "Tall dark stranger": NPC("Tall dark stranger", "A man in a tricorne hat and a long cloak covered in dust from the road", game_items.get_item_by_name("gem"), castle_map.get_room("Great hall"),
        lines=Lines(greet="Hullo stranger, here is a present for you.", answer_yes="Yes indeed", answer_no="I'm afraid not"))
    }

    castle_map.get_room("Drawing room").enter(NPCs["Tall dark stranger"])

    prompt_instructions = ["TAKE", "GREET", "QUIT"]
    g = Game(castle_map, game_items, NPCs, castle_map.get_room("Great hall"), prompt_instructions)
    return g


def main():
    g = make_Castle()
    g.prompt_and_execute()



if __name__ == "__main__":
    main()