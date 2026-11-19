"""角色控制器：斜坡、台阶、土狼时间与碰撞推出。

坐标约定：Y 轴向上；地面法线为指向角色外侧的方向。
斜坡是否可行走由法线与竖直方向的夹角（而不是高度差）决定。
"""

from __future__ import annotations

import math

# 竖直向上方向（Y 轴）；与地面法线的夹角即坡面倾角。
UP = (0.0, 1.0, 0.0)


def _normalize(vec):
    """返回单位向量；零长度向量返回 ``None``。"""
    length = math.sqrt(sum(component * component for component in vec))
    if length == 0.0:
        return None
    return tuple(component / length for component in vec)


def slope_angle_deg(ground_normal):
    """返回地面倾角（度），即法线与竖直向上方向的夹角。

    零长度法线没有可行走方向，视为完全不可站立（180°）。
    """
    normal = _normalize(ground_normal)
    if normal is None:
        return 180.0
    # 浮点误差可能让余弦略超出 [-1, 1]。
    cos_angle = max(-1.0, min(1.0, sum(a * b for a, b in zip(normal, UP))))
    return math.degrees(math.acos(cos_angle))


def is_walkable(ground_normal, max_slope_deg):
    """斜坡是否可行走：倾角必须严格小于最大坡度。

    恰好等于 ``max_slope_deg`` 时按过陡处理，避免边界上的坡面被当作平地。
    """
    return slope_angle_deg(ground_normal) < max_slope_deg


def move(pos, delta, ground_normal, step_height, max_slope_deg):
    """应用一帧位移，返回 ``(new_pos, grounded)``。

    - ``grounded`` 由地面法线决定：只有可行走（倾角小于
      ``max_slope_deg``）的支撑面才算站立，陡坡与空中均为 ``False``。
    - 站立时允许台阶抬升：向上位移不超过 ``step_height`` 就保留；
      超过则视为台阶过高，垂直分量被截断，角色停在原高度，水平位移照常。
    - 非站立时不做台阶抬升，位移原样应用，垂直运动交给重力层处理。
    """
    px, py, pz = pos
    dx, dy, dz = delta

    if not is_walkable(ground_normal, max_slope_deg):
        return (px + dx, py + dy, pz + dz), False

    if dy > step_height:
        dy = 0.0

    return (px + dx, py + dy, pz + dz), True


def coyote(last_ground, now, window):
    """返回土狼时间是否仍有效。

    土狼时间按秒计算，与帧率无关：离开地面后的 ``window`` 秒内仍可起跳。

    - 时间戳不晚于离开地面的时刻（刚离开地面，或时钟未推进/回拨）一律有效。
    - 窗口边界为开区间：经过时间恰好等于 ``window`` 时已失效。
    """
    elapsed = now - last_ground
    if elapsed <= 0.0:
        return True
    return elapsed < window


def resolve_penetration(pos, normal, depth):
    """沿法线推出穿透，返回修正后的位置。

    ``normal`` 为指向外侧的（单位）法线，``depth`` 为穿透深度：结果等于
    ``pos + normal * depth``。负深度表示沿法线反方向修正，零深度位置不变。
    """
    return tuple(
        coordinate + component * depth
        for coordinate, component in zip(pos, normal)
    )
