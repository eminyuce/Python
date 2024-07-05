class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

def make_animal_speak(animal):
    print(animal.speak())

# Creating instances of Dog and Cat
dog = Dog()
cat = Cat()

# Using the polymorphic function
make_animal_speak(dog)  # Output: Woof!
make_animal_speak(cat)  # Output: Meow!