from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass

    def sleep(self):
        print("This animal is sleeping.")

class Dog(Animal):
    def make_sound(self):
        return "Woof!"

class Cat(Animal):
    def make_sound(self):
        return "Meow!"

# Creating instances of Dog and Cat
dog = Dog()
cat = Cat()

# Using the methods
print(dog.make_sound())  # Output: Woof!
print(cat.make_sound())  # Output: Meow!
dog.sleep()              # Output: This animal is sleeping.
cat.sleep()              # Output: This animal is sleeping.

# Uncommenting the following line will raise an error because we cannot instantiate an abstract class
# animal = Animal()