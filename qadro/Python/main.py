# -*- coding: utf-8 -*-

"""
Застереження при спробі запустити приклади в середовищі без GPS:
`drone.offboard.stop()` поверне `COMMAND_DENIED` результат, тому що це
вимагає перемикання режиму в положення HOLD, що наразі не підтримується в a
середовище без GPS.
"""

import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)


async def run():
    """ Керування допомогою координат NED положення """

    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Очікування підключення дрона...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Підключено!")
            break

    print("Очікуємо, поки дрон отримає оцінку глобальної позиції...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Глобальна оцінка позиції завершена")
            break

    print("-- Активація")
    await drone.action.arm()

    print("-- Встановлення початкової уставки")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Початок функції offboard ('поза бортом')")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Не вдалося запустити позабортовий режим із кодом помилки: {error._result.result}")
        print("-- Дизактивація")
        await drone.action.disarm()
        return

    print("-- Переміщення 0 м на північ, 0 м на схід, -5 м вниз у межах місцевої системи координат")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -5.0, 0.0))
    await asyncio.sleep(10)

    print("-- Переміщення 5 м на північ, 0 м на схід, -5 м вниз у межах місцевої системи координат, повертаємось обличчям на схід")
    await drone.offboard.set_position_ned(PositionNedYaw(5.0, 0.0, -5.0, 90.0))
    await asyncio.sleep(10)

    print("-- Переміщення 5 м на північ, 10 м на схід, -5 м вниз у межах місцевої системи координат")
    await drone.offboard.set_position_ned(PositionNedYaw(5.0, 10.0, -5.0, 90.0))
    await asyncio.sleep(15)

    print("-- Переміщення 0 м на північ, 10 м на схід, 0 м вниз у межах місцевої системи координат, повертаємось обличчям на південь")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 10.0, 0.0, 180.0))
    await asyncio.sleep(10)

    print("-- Дизактивація")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Не вдалося зупинити позабортовий режим із кодом помилки: {error._result.result}")


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

