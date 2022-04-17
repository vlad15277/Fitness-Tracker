class InfoMessage:
    """ Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return(f'Тип тренировик:{self.training_type}; '
               f'Длительность: {self.duration:.3f} ч.; '
               f'Дистанция: {self.distance:.3f} км; '
               f'Ср. скорость: {self.speed:.3f} км/ч; '
               f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        av_speed = self.get_distance() / self.duration
        return av_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20
    minuts = 60
    workout_type = 'RUN'

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories_spent = (self.coeff_calorie_1 * self.get_mean_speed()
                          - self.coeff_calorie_2
                          ) * self.weight / self.M_IN_KM * (
                              self.duration * self.minuts)
        return calories_spent


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_3 = 0.035
    coeff_calorie_4 = 0.029
    minuts = 60
    ddos = 2
    workout_type = 'WLK'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories_walk = (self.coeff_calorie_3 * self.weight
                         + (self.get_mean_speed()**self.ddos // self.height
                            ) * self.coeff_calorie_4 * self.weight) * (
                                self.duration * self.minuts)
        return calories_walk


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    coeff_calorie_5 = 1.1
    coeff_calorie_6 = 2
    workout_type = 'SWM'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed_swem = self.length_pool * self.count_pool / (
            self.M_IN_KM / self.duration)
        return speed_swem

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories_swem = (self.get_mean_speed() + self.coeff_calorie_5
                         ) * self.coeff_calorie_6 * self.weight
        return calories_swem


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    training_type = trainings[workout_type]
    training_type = training_type(*data)
    return training_type


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
