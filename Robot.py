from abc import ABC, abstractmethod
from functools import wraps
import logging



logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


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

def log_action(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        logging.info(f"{self.name}: starting task")
        result = func(self, *args, **kwargs)
        logging.info(f"{self.name}: finished task")
        return result

    return wrapper
    
class CleaningRobot(Robot):
    def __init__(self, name, battery=100, dust_capacity=500):
        super().__init__(name, battery)
        self.dust_capacity = dust_capacity

    @log_action
    def perform_task(self):
        self.use_battery(10)
        return f"{self.name} cleaned the room."
    
    
class DroneRobot(Robot):
    def __init__(self, name, battery=100, max_altitude=120):
        super().__init__(name, battery)
        self.max_altitude = max_altitude

    def perform_task(self):
        self.use_battery(20)
        return f"{self.name} flew to {self.max_altitude}m."
    
    
def run_task_safely(robot, **kwargs):
    try:
        result = robot.perform_task(**kwargs)
    except InsufficientBatteryError as error:
        logging.error(error)
    else:
        print(result)
    finally:
        print(f"{robot.name}: {robot.battery}% battery")
        

def fleet_report(robots):
    for robot in robots:
        print(robot)


def mutable_demo():
    class Buggy:
        items = []

    a = Buggy()
    b = Buggy()

    a.items.append("Apple")

    print("Buggy:")
    print(a.items)
    print(b.items)

    class Fixed:
        def __init__(self):
            self.items = []

    c = Fixed()
    d = Fixed()

    c.items.append("Apple")

    print("Fixed:")
    print(c.items)
    print(d.items)        


def main():
    roomba = CleaningRobot("Roomba", 100)
    drone = DroneRobot.from_config({
        "name": "Aqua-Drone",
        "battery": 15
    })

    print("=== Fleet Report ===")
    fleet_report([roomba, drone])

    print("\n=== Robot Info ===")
    print(repr(roomba))
    print(f"Manufacturer: {Robot.manufacturer}")
    print(f"Population: {Robot.population}")

    print("\n=== Tasks ===")
    run_task_safely(roomba)
    run_task_safely(drone)

    print("\n=== Decorator ===")
    print(CleaningRobot.perform_task.__name__)

    print("\n=== Mutable Attribute Demo ===")
    mutable_demo()


if __name__ == "__main__":
    main()