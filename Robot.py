from abc import ABC, abstractmethod


class InsufficientBatteryError(Exception):
    def __init__(self, name, required, available):
        self.name = name
        self.required = required
        self.available = available
        super().__init__(
            f"{name} needs {required}% battery for this task "
            f"but only has {available}%."
        )


class Robot(ABC):
    manufacturer = "Acme Robotics"
    population = 0

    def __init__(self, name, battery=100):
        self.name = name
        self._battery = 0
        self.battery = battery
        Robot.population += 1

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        self._battery = max(0, min(100, value))

    def __str__(self):
        return f"{self.name} ({self.battery}% battery)"

    def __repr__(self):
        return f"Robot(name={self.name!r}, battery={self.battery})"

    def use_battery(self, amount):
        if amount > self.battery:
            raise InsufficientBatteryError(
                self.name, amount, self.battery
            )
        self.battery -= amount

    @classmethod
    def from_config(cls, config):
        return cls(**config)

    @abstractmethod
    def perform_task(self):
        pass
    
    
class CleaningRobot(Robot):
    def __init__(self, name, battery=100, dust_capacity=500):
        super().__init__(name, battery)
        self.dust_capacity = dust_capacity

    def perform_task(self):
        self.use_battery(10)
        return f"{self.name} cleaned the room."