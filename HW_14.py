# """Створити клас Vehicle (транспортний засіб):
#
# ні від чого не наслідується
# в ініціалізатор класу (__init__ метод) передати
# producer: str
# model: str
# year: int
# tank_capacity: float # обєм паливного баку
# tank_level: float = 0 # початковий параметр рівня паливного баку дорівнює 0, параметр в аргументах не передавати
# maxspeed: int
# fuel_consumption: float # litres/100km споживання пального
# odometer_value: int = 0 # при сході з конвеєра пробіг нульовий, параметр в аргументах не передавати
#
# визначити метод __repr__, яким повертати інформаційну стрічку (наповнення на ваш вибір, проте параметри model and year and odometer_value мають бути передані
#
# написати метод refueling, який не приймає жодного аргумента, заправляє автомобіль на уявній автозаправці до максимума (tank_level = tank_capacity), після чого виводить на екран повідомлення, скільки літрів було заправлено (перша заправка буде повного баку, а в інших випадках величина буде залежати від залишку пального в баку)
#
# написати метод race, який приймає один аргумент (не враховуючи self) - відстань, яку потрібно проїхати, а повертає словник, в якому вказано, скільки авто проїхало, з огляду на заповнення паливного баку перед поїздкою, залишок пального (при малому кілометражі все пальне не використається), та час, за який відбулася дана поїздка, з урахування, що середня швидкість складає 80% від максимальної (витрата пального рівномірна незалежно від швидкості)
#
# за результатами роботи метода в атрибуті tank_level екземпляра класа має зберігатися залишок пального після поїздки (зрозуміло, що не менше 0)
#
# збільшити на величину поїздки показники odometer_value
#
# написати метод lend_fuel, який приймає окрім self ще й other обєкт, в результаті роботи якого паливний бак обєкта, на якому було викликано відповідний метод, наповнюється до максимального рівня за рахунок відповідного зменшення рівня пального у баку дружнього транспортного засобу
#
# вивести на екран повідомлення з текстом типу "Дякую, бро, виручив. Ти залив мені *** літрів пального"
#
# у випадку, якщо бак першого обєкта повний або у другого обєкта немає пального, вивести повідомлення "Нічого страшного, якось розберуся"
#
# написати метод __eq__, який приймає окрім self ще й other обєкт (реалізація магічного методу для оператора порівняння == )
#
# даний метод має повернути True у випадку, якщо 2 обєкта, які порівнюються, однакові за показниками року випуску та пробігу (значення відповідних атрибутів однакові, моделі можуть бути різними)
#
# створіть не менше 2-х обєктів класу, порівняйте їх до інших операцій, заправте їх, покатайтесь на них на різну відстань, перевірте пробіг, позичте один в одного пальне, знову порівняйте"""


class Vehicle:
    def __init__(self,
                 producer: str,
                 model: str,
                 year: int,
                 maxspeed: int,
                 fuel_consumption: float,
                 tank_capacity: float
                 ):
        self.producer = producer
        self.model = model
        self.year = year
        self.maxspeed = maxspeed
        self.fuel_consumption = fuel_consumption  # litres/100km споживання пального
        self.tank_capacity = tank_capacity  # об`єм паливного баку
        self.__tank_level = 0  # початковий рівень палива
        self.__odometer_value = 0  # при сході з конвеєра пробіг нульовий

    def __repr__(self):
        return f'{self.__class__.__name__}({self.producer} {self.model}, {self.year}, {self.odometer_value:.2f} km)'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"`==` is not supported between instances of '{self.__class__.__name__}' and '{type(other)}'")
        return self.year == other.year and self.odometer_value == other.odometer_value

    @property
    def odometer_value(self):
        return self.__odometer_value

    @property
    def tank_level(self):
        return self.__tank_level

    @property
    def max_refueling_capacity(self):
        return self.tank_capacity - self.tank_level

    def refueling(self):
        if self.tank_level < self.tank_capacity:
            print(f"Заправлено {self.max_refueling_capacity} літрів пального!")
            self.__tank_level = self.tank_capacity
        else:
            print("Бак і так вже повний")

    def race(self, distance):
        max_distance = self.tank_level * 100 / self.fuel_consumption  # Максимальна відстань, яку може подолати транспортний засіб з урахуванням поточного залишку палива
        covered_distance = max_distance if max_distance <= distance else distance  # Реальна відстань, яку подолав транспортний засіб
        consumed_fuel = self.fuel_consumption * covered_distance / 100  # Реальна кількість витраченого палива
        avg_speed = int(0.8 * self.maxspeed)  # Середня швидкість
        travel_time = avg_speed / covered_distance

        self.__tank_level -= consumed_fuel
        self.__odometer_value += covered_distance

        return {"covered_distance": covered_distance,
                "tank_level": self.tank_level,
                "travel_time": travel_time
                }

    def lend_fuel(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"`lend_fuel` method is not supported between instances of '{self.__class__.__name__}' and '{type(other)}'")
        if self.tank_level == self.tank_capacity or other.tank_level == 0:
            print("Нічого страшного, якось розберуся")
        else:
            q_fuel_to_lend = self.max_refueling_capacity if self.max_refueling_capacity <= other.tank_level else other.tank_level
            other.__tank_level -= q_fuel_to_lend
            self.__tank_level += q_fuel_to_lend
            print(f"Дякую, бро, виручив. Ти залив мені {q_fuel_to_lend} літрів пального")


if __name__ == '__main__':
    bmw_x5_2014 = Vehicle('BMW', 'X5', 2014, 151, 8.5, 83)
    porsche_911_2017 = Vehicle('Porsche', '911', 2017, 319, 9.0, 64)
    ford_fusion_2014 = Vehicle('Ford', 'Fusion', 2014, 174, 8.2, 64)

    print(f"{bmw_x5_2014} == {porsche_911_2017}: {bmw_x5_2014 == porsche_911_2017}")
    print(f"{bmw_x5_2014} == {ford_fusion_2014}: {bmw_x5_2014 == ford_fusion_2014}")
    print(f"{porsche_911_2017} == {ford_fusion_2014}: {porsche_911_2017 == ford_fusion_2014}")

    bmw_x5_2014.refueling()
    porsche_911_2017.refueling()
    ford_fusion_2014.refueling()

    bmw_x5_2014.race(1050)
    porsche_911_2017.race(500)
    ford_fusion_2014.race(200)

    print(f"Пробіг {bmw_x5_2014}: {bmw_x5_2014.odometer_value:.2f} км")
    print(f"Пробіг {porsche_911_2017}: {porsche_911_2017.odometer_value:.2f} км")
    print(f"Пробіг {ford_fusion_2014}: {ford_fusion_2014.odometer_value:.2f} км")

    porsche_911_2017.lend_fuel(bmw_x5_2014)
    ford_fusion_2014.lend_fuel(porsche_911_2017)

    print(f"{bmw_x5_2014} == {porsche_911_2017}: {bmw_x5_2014 == porsche_911_2017}")
    print(f"{bmw_x5_2014} == {ford_fusion_2014}: {bmw_x5_2014 == ford_fusion_2014}")
    print(f"{porsche_911_2017} == {ford_fusion_2014}: {porsche_911_2017 == ford_fusion_2014}")