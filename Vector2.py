import math


class Vector2(object):
    def __init__(self, x=0, y=0):
        super(Vector2, self).__init__()
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(y=self.y + other.y, x=self.x + other.x)

    def __sub__(self, other):
        return Vector2(y=self.y - other.y, x=self.x - other.x)

    def __mul__(self, s):
        return Vector2(y=self.y * s, x=self.x * s)

    def __truediv__(self, s):
        return Vector2(y=self.y / s, x=self.x / s)

    def __floordiv__(self, s):
        return Vector2(y=self.y // s, x=self.x // s)

    def __pow__(self, s):
        return Vector2(y=self.y**s, x=self.x**s)

    def __mod__(self, s):
        return Vector2(y=self.y % s, x=self.x % s)

    # def __eq__(self, other):
    #     if self.y == other.y and self.x == other.x:
    #         return True
    #     else:
    #         return False

    # def __le__(self, other):  # <=
    #     if self.y <= other.y and self.x <= other.x:
    #         return True
    #     else:
    #         return False

    # def __ge__(self, other):  # >=
    #     if self.y >= other.y and self.x >= other.x:
    #         return True
    #     else:
    #         return False

    # def __lt__(self, other):  # <
    #     if self.y < other.y and self.x < other.x:
    #         return True
    #     else:
    #         return False

    # def __gt__(self, other):  # >
    #     if self.y > other.y and self.x > other.x:
    #         return True
    #     else:
    #         return False

    # def __ne__(self, other):
    #     return not self.__eq__(other)

    def __repr__(self):
        return f"x:{self.x}/y:{self.y}"

    def to_tuple(self):
        return (self.x, self.y)

    def to_int_tuple(self):
        return (int(self.x), int(self.y))

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def simple_length(self):
        return self.x**2 + self.y**2

    def rotate(self, rad_angle):
        c = math.cos(rad_angle)
        s = math.sin(rad_angle)

        x = c * self.x - s * self.y
        y = s * self.x + c * self.y
        return Vector2(x=x, y=y)

    def normalize(self):
        return self / self.length()

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def is_null(self):
        return self.x == 0 and self.y == 0

    def ln_range_transform(self):
        return int(math.log(max(0.1, self.simple_length()), math.e))

    def artistic_velocity(self):
        return abs(self.x * self.y)

    def round_to_int_with_mod(self, px_grid_size):
        self.x = int(self.x % px_grid_size)
        self.y = int(self.y % px_grid_size)

    def round_to_int(self):
        self.x = int(self.x)
        self.y = int(self.y)
