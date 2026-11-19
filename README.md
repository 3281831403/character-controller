# 角色控制器：斜坡、台阶、土狼时间与平台

角色在斜坡滑落、台阶卡住、离开平台后土狼时间失效、碰撞穿透。本仓库固定移动与碰撞契约。

- 领域：游戏、图形与多媒体
- 子方向：其他
- 语言/框架：Python 3, pytest
- 初始状态：15 个参数化用例全部失败

## 目录结构

```
README.md
conftest.py
.gitignore
gameplay/__init__.py
gameplay/character_controller.py
tests/test_character_controller.py
```

## 需要修复的 10 个问题

1. 斜坡按地面法线与最大角度判定可行走
2. 台阶高度内的垂直位移自动抬升
3. 离开地面后的土狼时间按秒计算
4. 移动平台位移只对站立角色生效
5. 碰撞穿透按法线与深度推出
6. 固定步长下移动与物理同步
7. 网络纠正后位置平滑，不瞬移
8. 角色半径参与碰撞检测
9. 斜坡上的重力分量正确
10. 输入去重后不重复应用同一帧位移

## 15 条验收契约

    01. move flat — `move`
    02. move step — `move`
    03. move high step — `move`
    04. move slope ok — `move`
    05. move slope steep — `move`
    06. coyote inside — `coyote`
    07. coyote edge — `coyote`
    08. coyote outside — `coyote`
    09. coyote zero — `coyote`
    10. coyote negative — `coyote`
    11. penetrate x — `resolve_penetration`
    12. penetrate y — `resolve_penetration`
    13. penetrate diag — `resolve_penetration`
    14. penetrate zero — `resolve_penetration`
    15. penetrate negative — `resolve_penetration`

## 当前状态

`gameplay/character_controller.py` 只保留函数签名与文档字符串，所有函数体统一
`raise NotImplementedError`。`tests/test_character_controller.py` 使用一个
`@pytest.mark.parametrize` 装载 15 条契约，初始全部失败且没有 collection error。

```bash
python -m pytest -q
```

预期输出包含 `15 failed`。实现 `gameplay/character_controller.py` 后，15 条契约应全部通过。
