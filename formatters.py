"""
Модуль форматирования чисел для ru-RU локали.
"""

import math


def fmt_money(n: float, currency: str = "₽") -> str:
    """
    Форматирование денежной суммы в формате ru-RU.
    
    Args:
        n: Сумма для форматирования
        currency: Символ валюты (по умолчанию ₽)
    
    Returns:
        Отформатированная строка типа "1 234 567 ₽"
    
    Examples:
        >>> fmt_money(1234567.89)
        '1 234 568 ₽'
        >>> fmt_money(0)
        '0 ₽'
    """
    # Обработка NaN и inf
    if not math.isfinite(n):
        return "—"
    
    # Округляем до целого
    n = round(n)
    
    # Форматируем с пробелами как разделителями тысяч
    # Используем форматирование Python
    formatted = f"{n:,}".replace(",", " ")
    
    return f"{formatted} {currency}"


def fmt_percent(p: float, digits: int = 0) -> str:
    """
    Форматирование процентов в формате ru-RU.
    
    Args:
        p: Процент для форматирования
        digits: Количество знаков после запятой
    
    Returns:
        Отформатированная строка типа "12,3 %" или "15 %"
    
    Examples:
        >>> fmt_percent(12.345, 1)
        '12,3 %'
        >>> fmt_percent(15)
        '15 %'
    """
    # Обработка NaN и inf
    if not math.isfinite(p):
        return "—"
    
    # Форматируем с запятой как десятичным разделителем
    if digits == 0:
        formatted = f"{p:.0f}"
    else:
        formatted = f"{p:.{digits}f}".replace(".", ",")
    
    return f"{formatted} %"


def fmt_number(n: float, digits: int = 1) -> str:
    """
    Форматирование числа в формате ru-RU.
    
    Args:
        n: Число для форматирования
        digits: Количество знаков после запятой
    
    Returns:
        Отформатированная строка типа "12,3" или "1 234,5"
    
    Examples:
        >>> fmt_number(1234.5, 1)
        '1 234,5'
        >>> fmt_number(12.345, 2)
        '12,35'
    """
    # Обработка NaN и inf
    if not math.isfinite(n):
        return "—"
    
    # Форматируем число
    if digits == 0:
        formatted = f"{n:,.0f}".replace(",", " ")
    else:
        formatted = f"{n:,.{digits}f}".replace(",", " ").replace(".", ",")
    
    return formatted


def fmt_roi(roi: float) -> str:
    """
    Форматирование ROI (Return on Investment).
    
    Args:
        roi: Коэффициент ROI (например, 2.5 = 2.5×)
    
    Returns:
        Отформатированная строка типа "2,5×" или "—"
    
    Examples:
        >>> fmt_roi(2.5)
        '2,5×'
        >>> fmt_roi(None)
        '—'
    """
    if roi is None or not math.isfinite(roi):
        return "—"
    
    formatted = f"{roi:.1f}".replace(".", ",")
    return f"{formatted}×"


def fmt_days(days: float) -> str:
    """
    Форматирование дней с правильным склонением.
    
    Args:
        days: Количество дней
    
    Returns:
        Отформатированная строка типа "5 дней" или "1 день"
    """
    if not math.isfinite(days):
        return "—"
    
    days = int(round(days))
    
    # Склонение: день/дня/дней
    if days % 10 == 1 and days % 100 != 11:
        word = "день"
    elif days % 10 in [2, 3, 4] and days % 100 not in [12, 13, 14]:
        word = "дня"
    else:
        word = "дней"
    
    return f"{days} {word}"
