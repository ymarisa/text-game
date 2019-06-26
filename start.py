NORTH = "North"
SOUTH = "South"
EAST = "East"
WEST = "West"

class Game:
    PROMPT = """You are in {{CURRENT_LOCATION}}. {{DESCRIPTION}} \
        \n{{OPTIONS}}"""
    def __init__(self, locations, items, start_location):
        self.items = items
        # name, items, doors, description, who
        self.locations = locations        
        self.current_location = start_location    #Room object
        self.bag = []

    #for debugging
    def print_locations(self):
        print(len(self.locations))
        for l in self.locations:
            print(l)

    def get_items(self):
        return self.items

    def get_current_location(self):
        return self.current_location

    def get_bag(self):
        return self.bag

    def add_to_bag(self, item):
        self.bag.append(item)

    def is_won(self):
        return self.current_location == self.locations[1] and self.bag.contains("gem")

    def get_prompt(self):
        current_prompt = self.PROMPT.replace("{{CURRENT_LOCATION}}", self.current_location.get_name())
        current_prompt = current_prompt.replace("{{DESCRIPTION}}", self.current_location.get_description())
        current_prompt = current_prompt.replace("{{OPTIONS}}", self.current_location.get_next_locations())
        return current_prompt

# {"North": Room}
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

    def get_next_locations(self):
        next_locations = ""
        for door in self.doors:
            next_locations = next_locations + f"{door}: {self.doors[door].get_name()}\n"
        return next_locations

    def set_door(self, direction, room):
        self.doors[direction] = room

    def __str__(self):
        return self.name

class NPC:
    def __init__(self, item, lines):
        self.location = "test2"
        self.bag = item
        self.lines = lines

    def move_rooms(self, location):
        self.location = location

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

def make_Castle():
    items = [
            "gem",
            "candlestick"
    ]

    locations = {
            "room0": Room("room0", [], {}, "0foobartest", []),
            "room1": Room("room1", [], {}, "1foobartest", []),
            "room2": Room("room2", [items[1]], {}, "2foobartest", []),
    }

    # NPC: item, lines
    NPCs = {
        "Woody": NPC(items[0],
            lines=Lines(greet="Howdy", answer_yes="Yes indeed", answer_no="I'm afraid not"))
    }

    #TODO: change the ref to self.locations
    locations["room0"].set_door(SOUTH, locations["room1"])
    locations["room1"].set_door(NORTH, locations["room0"])

    locations["room1"].set_door(EAST, locations["room2"])
    locations["room2"].set_door(WEST, locations["room1"])
    
    locations["room2"].set_door(EAST, locations["room0"])
    locations["room0"].set_door(WEST, locations["room2"])

    g = Game(locations, items, locations["room0"])
    return g

def main():
    g = make_Castle()
    g.print_locations()
    print(g.get_prompt())



if __name__ == "__main__":
    main()