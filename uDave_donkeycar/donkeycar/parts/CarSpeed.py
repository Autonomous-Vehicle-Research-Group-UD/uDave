import math

class Car_Speed:
    first = True
    prev_speed = 0

    def car_Speed(acc_x, acc_y):
        if (acc_x != 0 and acc_y != 0):
            v_sum = acc_x + acc_y

            negative = False

            if v_sum < 0:
                v_sum *= -1
                negative = True

            v_length = math.sqrt(v_sum)

            if negative:
                v_length *= -1

            if Car_Speed.first is False:
                v_length += Car_Speed.prev_speed

            Car_Speed.first = False
            Car_Speed.prev_speed = v_length
        else:
            Car_Speed.first = True
            v_length = 0

        return v_length
