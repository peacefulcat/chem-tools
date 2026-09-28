"""
分子式解析器 — 支持括号嵌套和水合物
采用递归下降解析

语法：
    formula   →  part ('·' part)*
    part      →  term+
    term      →  atom [count]
              | '(' part ')' [count]
    atom      →  [A-Z][a-z]?
    count     →  [0-9]+

示例：
    parse('H2O')          → {'H': 2, 'O': 1}
    parse('Fe2(SO4)3')    → {'Fe': 2, 'S': 3, 'O': 12}
    parse('CuSO4·5H2O')   → {'Cu': 1, 'S': 1, 'O': 9, 'H': 10}
"""

from collections import defaultdict

from elements import ELEMENTS


def parse(formula: str) -> dict[str, int]:
    """
    解析化学分子式，返回 {元素符号: 原子个数} 字典

    支持：
      - 简单分子式:   H2O, NaCl, C6H12O6
      - 括号嵌套:     Fe2(SO4)3, Mg(OH)2, (Fe(CN)6)3
      - 水合物:       CuSO4·5H2O, Na2CO3·10H2O
      - 点号别名:     CuSO4.5H2O 等效于 CuSO4·5H2O

    参数:
        formula: 化学分子式字符串

    返回:
        {元素符号: 原子个数}

    异常:
        ValueError: 格式错误或包含未知元素
    """
    if not formula or not formula.strip():
        return {}

    # 统一 · 和 . 为分隔符，按水合物拆解
    parts = formula.strip().replace('.', '·').split('·')

    total = defaultdict(int)
    _merge_dicts(total, _parse_part(parts[0]))

    for part in parts[1:]:
        part = part.strip()
        if not part:
            continue
        coef, sub = _split_hydrate_coef(part)
        inner = _parse_part(sub)
        for elem, n in inner.items():
            total[elem] += n * coef

    return dict(total)


# ── 递归下降核心 ──────────────────────────────────────────────


def _parse_part(s: str) -> dict[str, int]:
    """解析不含 · 的一整段分子式。"""
    if not s:
        return {}
    counts, pos = _parse_group(s, 0)
    if pos != len(s):
        raise ValueError(f"位置 {pos} 处出现意外的字符: '{s[pos]}'")
    return dict(counts)


def _parse_group(s: str, i: int):
    """
    从位置 i 开始解析一个「组」（括号单元的顶层或括号内）。

    返回:
        (元素计数 defaultdict, 解析结束的位置)
    """
    counts = defaultdict(int)

    while i < len(s):
        ch = s[i]

        if ch == '(':
            # ── 进入括号子组 ──
            inner, i = _parse_group(s, i + 1)
            if i >= len(s) or s[i] != ')':
                raise ValueError(f"位置 {i}: 缺少配对的 ')'")
            i += 1  # 跳过 )

            mult = _read_int(s, i)
            if mult:
                i += len(str(mult))
            else:
                mult = 1

            for elem, n in inner.items():
                counts[elem] += n * mult

        elif ch == ')':
            # ── 当前组结束 ──
            break

        elif ch.isupper():
            # ── 元素符号 ──
            elem = ch
            i += 1
            while i < len(s) and s[i].islower():
                elem += s[i]
                i += 1

            if elem not in ELEMENTS:
                raise ValueError(f"未知元素符号: '{elem}' (位置 {i - len(elem)})")

            cnt = _read_int(s, i)
            if cnt:
                i += len(str(cnt))
            else:
                cnt = 1

            counts[elem] += cnt

        elif ch in ('·', '.'):
            # 当前组内不应该出现水合物分隔符
            raise ValueError(f"位置 {i}: 水合物分隔符 '{ch}' 出现在了括号内部")

        elif ch.isspace():
            i += 1
            continue

        else:
            raise ValueError(f"位置 {i} 出现意外的字符: '{ch}'")

    return counts, i


# ── 辅助函数 ──────────────────────────────────────────────────


def _read_int(s: str, i: int) -> int:
    """从 i 开始读连续数字；没有数字则返回 0。"""
    if i >= len(s) or not s[i].isdigit():
        return 0
    j = i
    while j < len(s) and s[j].isdigit():
        j += 1
    return int(s[i:j])


def _split_hydrate_coef(part: str) -> tuple[int, str]:
    """
    拆分水合物部分系数与子分子式。

    例:
        '5H2O'   → (5, 'H2O')
        'H2O'    → (1, 'H2O')
        '10H2O'  → (10, 'H2O')
    """
    coef = _read_int(part, 0)
    if coef:
        digits = len(str(coef))
        return coef, part[digits:]
    return 1, part


def _merge_dicts(target: dict, source: dict):
    """将 source 中的整数计数累加到 target 中。"""
    for k, v in source.items():
        target[k] += v


# ── 简易 CLI 测试 ─────────────────────────────────────────────

if __name__ == '__main__':
    test_cases = [
        ('H2O',           {'H': 2, 'O': 1}),
        ('O2',            {'O': 2}),
        ('NaCl',          {'Na': 1, 'Cl': 1}),
        ('C6H12O6',       {'C': 6, 'H': 12, 'O': 6}),
        ('Fe2(SO4)3',     {'Fe': 2, 'S': 3, 'O': 12}),
        ('Mg(OH)2',       {'Mg': 1, 'O': 2, 'H': 2}),
        ('(NH4)2CO3',     {'N': 2, 'H': 8, 'C': 1, 'O': 3}),
        ('(Fe(CN)6)3',    {'Fe': 3, 'C': 18, 'N': 18}),
        ('CuSO4·5H2O',    {'Cu': 1, 'S': 1, 'O': 9, 'H': 10}),
        ('Na2CO3·10H2O',  {'Na': 2, 'C': 1, 'O': 13, 'H': 20}),
        ('CoCl2·6NH3',    {'Co': 1, 'Cl': 2, 'N': 6, 'H': 18}),
        ('',              {}),
    ]

    all_ok = True
    for formula, expected in test_cases:
        try:
            result = parse(formula)
            ok = result == expected
            status = '✅' if ok else '❌'
            if not ok:
                all_ok = False
            print(f" {status}  {formula:<20s} → {result}")
            if not ok:
                print(f"    期望: {expected}")
        except Exception as e:
            print(f" ❌  {formula:<20s} → 异常: {e}")
            all_ok = False

    print()
    print(f"{'='*40}")
    print(f"{'全部通过!' if all_ok else '有失败用例！'} ")
