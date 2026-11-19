"""角色控制器：斜坡、台阶、土狼时间与平台：待实现的核心模块。"""

from __future__ import annotations


def move(pos, delta, ground_normal, step_height, max_slope_deg):
    """返回 (new_pos, grounded)。"""
    raise NotImplementedError

def coyote(last_ground, now, window):
    """返回土狼时间是否仍有效。"""
    raise NotImplementedError

def resolve_penetration(pos, normal, depth):
    """沿法线推出穿透。"""
    raise NotImplementedError
