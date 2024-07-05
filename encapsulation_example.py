class Car:
    def __init__(self, make, model, year):
        self.make = make           # Public attribute
        self._model = model        # Protected attribute
        self.__year = year         # Private attribute

    # Public method
    def get_car_info(self):
        return f"{self.make} {self._model} {self.__year}"

    # Protected method
    def _get_model(self):
        return self._model

    # Private method
    def __get_year(self):
        return self.__year

    # Public method to access the private attribute
    def get_year(self):
        return self.__get_year()

# Create an instance of Car
car = Car("Toyota", "Corolla", 2020)

# Accessing public attribute
print(car.make)  # Output: Toyota

# Accessing protected attribute (not recommended, but possible)
print(car._model)  # Output: Corolla

# Accessing private attribute directly will raise an AttributeError
# print(car.__year)  # Uncommenting this line will raise an error

# Accessing private attribute through a public method
print(car.get_year())  # Output: 2020

# Accessing public method
print(car.get_car_info())  # Output: Toyota Corolla 2020

# Accessing protected method (not recommended, but possible)
print(car._get_model())  # Output: Corolla

# Accessing private method directly will raise an AttributeError
# print(car.__get_year())  # Uncommenting this line will raise an error