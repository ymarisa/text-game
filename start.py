class Game:
    def __init__(self):
        self.locations = [
            Room("test", [], [], "foobartest", []),
            Room("test2", [], ["something"], "2foobartest", [])
        ]
        self.items = [
            "gem"
        ]
        self.current_location = self.locations[0]
        self.bag = []
        self.prompt = f"You are in {self.current_location}. {self.current_location.get_description()} \
        {self.current_location.get_next_locations()}"

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
        return ""

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
            next_locations = next_locations + f"{door}: {self.doors[door].get_name()}"

    def __str__(self):
        return self.name

class Person:
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


def main():
    g = Game()
    g.print_locations()



if __name__ == "__main__":
    main()