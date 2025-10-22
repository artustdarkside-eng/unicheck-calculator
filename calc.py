"""
Модуль расчётов экономического эффекта UniCheck.

Все формулы реализованы как чистые функции.
Логика:
1. Экономия человеко-часов проверки
2. Экономия от ускорения процесса (сокращение Time-to-Hire)
3. Экономия от повышения точности (снижение bad hire)
4. Экономия от снижения FP/FN на этапе техскрина
5. Эффект NPS (качественный или денежный)
6. Стоимость платформы UniCheck
7. Итоговые метрики: валовая экономия, net-экономия, ROI
"""

from typing import Dict, Optional, Tuple
import math


def calculate_economics(
    # A. План и объёмы
    hires_per_month: int,
    checks_per_hire: int,
    
    # B. Часы и ставки
    eng_hourly: int,
    rec_hourly: int,
    eng_hours_per_cand_manual: float,
    rec_hours_per_cand_manual: float,
    eng_hours_per_cand_unicheck: float,
    rec_hours_per_cand_unicheck: float,
    
    # C. Сроки процесса
    time_to_test_start_manual_days: int,
    time_to_test_start_unicheck_days: int,
    time_to_test_finish_manual_days: int,
    time_to_test_finish_unicheck_days: int,
    vacancy_cost_per_day: int,
    
    # D. Точность (основная модель)
    bad_hire_rate_manual_pct: int,
    bad_hire_rate_unicheck_pct: int,
    cost_bad_hire: int,
    
    # D. Точность (FP/FN модель)
    good_candidates_share: int,
    fp_rate_manual_pct: int,
    fn_rate_manual_pct: int,
    fp_rate_unicheck_pct: int,
    fn_rate_unicheck_pct: int,
    
    # E. Стоимость UniCheck
    price_per_check: int,
    
    # F. NPS
    nps_manual: int,
    nps_unicheck: int,
    nps_to_value_coef: float,
    use_nps_money: bool,
    
    # D. Параметры цены FP/FN (опциональные)
    cost_fp: int = 300000,
    cost_fn: int = 150000,
    use_fpfn_model: bool = False,
) -> Dict:
    """
    Главная функция расчёта всех экономических метрик.
    
    Returns:
        Словарь с результатами расчётов и диагностической информацией.
    """
    
    # === 1. Базовые величины ===
    hires_per_year = hires_per_month * 12
    total_checks = hires_per_year * checks_per_hire
    candidates_unicheck = total_checks  # Все проверки идут через UniCheck
    
    # === 2. Экономия человеко-часов проверки ===
    manual_cost_per_check = (
        eng_hours_per_cand_manual * eng_hourly +
        rec_hours_per_cand_manual * rec_hourly
    )
    unicheck_cost_per_check = (
        eng_hours_per_cand_unicheck * eng_hourly +
        rec_hours_per_cand_unicheck * rec_hourly
    )
    labor_savings_per_check = max(0, manual_cost_per_check - unicheck_cost_per_check)
    labor_savings = labor_savings_per_check * total_checks
    
    # === 3. Экономия от ускорения процесса (Time-to-Hire) ===
    # Преобразуем часы в дни (предполагаем 8-часовой рабочий день)
    tth_manual_days = time_to_test_start_manual_days + (time_to_test_finish_manual_days / 8)
    tth_unicheck_days = time_to_test_start_unicheck_days + (time_to_test_finish_unicheck_days / 8)
    delta_tth_days = max(0, tth_manual_days - tth_unicheck_days)
    
    # Сокращение Time-to-Hire в год (дни × количество нанятых в год)
    delta_tth_days_yearly = delta_tth_days * hires_per_year
    
    # Экономия считается за одну позицию за счет ускорения поиска
    # На каждую позицию экономим delta_tth_days * vacancy_cost_per_day
    speed_savings = hires_per_year * delta_tth_days * vacancy_cost_per_day
    
    # === 4. Экономия от повышения точности ===
    # Две альтернативные модели: базовая (bad hire %) и детальная (FP/FN)
    # Используем детальную модель, если она включена, иначе базовую
    
    accuracy_savings_basic = 0
    fpfn_value = 0
    avoided_bad = 0
    bad_before = 0
    bad_after = 0
    avoided_fp = 0
    avoided_fn = 0
    fp_savings = 0
    fn_savings = 0
    
    if use_fpfn_model:
        # === Детальная модель (FP/FN на этапе техскрина) ===
        good_candidates = total_checks * good_candidates_share / 100
        bad_candidates = total_checks - good_candidates
        
        # False Positives (приняли слабых) - каждый стоит cost_fp
        manual_fp = bad_candidates * fp_rate_manual_pct / 100
        unicheck_fp = bad_candidates * fp_rate_unicheck_pct / 100
        avoided_fp = max(0, manual_fp - unicheck_fp)
        fp_savings = avoided_fp * cost_fp
        
        # False Negatives (отказали сильным) - каждый стоит cost_fn
        manual_fn = good_candidates * fn_rate_manual_pct / 100
        unicheck_fn = good_candidates * fn_rate_unicheck_pct / 100
        avoided_fn = max(0, manual_fn - unicheck_fn)
        fn_savings = avoided_fn * cost_fn
        
        fpfn_value = fp_savings + fn_savings
        # ВАЖНО: При включении FP/FN модели базовая модель НЕ считается
        # чтобы избежать дублирования расчета ошибок найма
    else:
        # === Базовая модель (bad hire rate %) ===
        bad_before = hires_per_year * bad_hire_rate_manual_pct / 100
        bad_after = hires_per_year * bad_hire_rate_unicheck_pct / 100
        avoided_bad = max(0, bad_before - bad_after)
        accuracy_savings_basic = avoided_bad * cost_bad_hire
    
    # === 6. Эффект NPS ===
    delta_nps = max(0, nps_unicheck - nps_manual)
    nps_value = 0
    if use_nps_money and nps_to_value_coef > 0:
        nps_value = delta_nps * nps_to_value_coef * hires_per_year
    
    # === 7. Стоимость платформы UniCheck ===
    platform_cost = candidates_unicheck * price_per_check
    
    # === 8. Итоговые метрики ===
    gross_savings = labor_savings + speed_savings + accuracy_savings_basic + fpfn_value + nps_value
    net_savings = gross_savings - platform_cost
    
    # ROI (возврат на инвестиции)
    if platform_cost > 0:
        roi = net_savings / platform_cost
    else:
        roi = None
    
    # Payback Period (период окупаемости в месяцах)
    monthly_net_savings = net_savings / 12
    if monthly_net_savings > 0:
        payback_months = platform_cost / monthly_net_savings
    else:
        payback_months = None
    
    # Метрики на кандидата
    if candidates_unicheck > 0:
        gross_per_candidate = gross_savings / candidates_unicheck
        platform_per_candidate = platform_cost / candidates_unicheck
        net_per_candidate = net_savings / candidates_unicheck
    else:
        gross_per_candidate = 0
        platform_per_candidate = 0
        net_per_candidate = 0
    
    # Метрики на найм
    if hires_per_year > 0:
        gross_per_hire = gross_savings / hires_per_year
        platform_per_hire = platform_cost / hires_per_year
        net_per_hire = net_savings / hires_per_year
    else:
        gross_per_hire = 0
        platform_per_hire = 0
        net_per_hire = 0
    
    # Метрика изменения точности (процентные пункты)
    delta_accuracy_pp = max(0, bad_hire_rate_manual_pct - bad_hire_rate_unicheck_pct)
    
    return {
        # === Главные метрики ===
        'gross_savings': gross_savings,
        'platform_cost': platform_cost,
        'net_savings': net_savings,
        'roi': roi,
        'payback_months': payback_months,
        'delta_tth_days': delta_tth_days,
        'delta_tth_days_yearly': delta_tth_days_yearly,
        'delta_accuracy_pp': delta_accuracy_pp,
        
        # === Разбивка экономии ===
        'labor_savings': labor_savings,
        'speed_savings': speed_savings,
        'accuracy_savings': accuracy_savings_basic,
        'fpfn_value': fpfn_value,
        'fp_savings': fp_savings,
        'fn_savings': fn_savings,
        'nps_value': nps_value,
        
        # === Метрики на кандидата ===
        'gross_per_candidate': gross_per_candidate,
        'platform_per_candidate': platform_per_candidate,
        'net_per_candidate': net_per_candidate,
        
        # === Метрики на найм ===
        'gross_per_hire': gross_per_hire,
        'platform_per_hire': platform_per_hire,
        'net_per_hire': net_per_hire,
        
        # === Диагностика ===
        'total_checks': total_checks,
        'candidates_unicheck': candidates_unicheck,
        'manual_cost_per_check': manual_cost_per_check,
        'unicheck_cost_per_check': unicheck_cost_per_check,
        'labor_savings_per_check': labor_savings_per_check,
        'tth_manual_days': tth_manual_days,
        'tth_unicheck_days': tth_unicheck_days,
        'bad_before': bad_before,
        'bad_after': bad_after,
        'avoided_bad': avoided_bad,
        'avoided_fp': avoided_fp,
        'avoided_fn': avoided_fn,
        'delta_nps': delta_nps,
    }


def calculate_single_check_economics(
    # Параметры для одной проверки
    eng_hourly: int,
    rec_hourly: int,
    eng_hours_manual: float,
    rec_hours_manual: float,
    eng_hours_unicheck: float,
    rec_hours_unicheck: float,
    price_per_check: int,
) -> Dict:
    """
    Расчёт экономики на уровне одной проверки.
    
    Returns:
        Словарь с метриками для одной проверки.
    """
    manual_cost = eng_hours_manual * eng_hourly + rec_hours_manual * rec_hourly
    unicheck_cost_labor = eng_hours_unicheck * eng_hourly + rec_hours_unicheck * rec_hourly
    unicheck_cost_total = unicheck_cost_labor + price_per_check
    
    savings = manual_cost - unicheck_cost_total
    savings_pct = (savings / manual_cost * 100) if manual_cost > 0 else 0
    
    return {
        'manual_cost': manual_cost,
        'unicheck_cost_labor': unicheck_cost_labor,
        'unicheck_platform_cost': price_per_check,
        'unicheck_cost_total': unicheck_cost_total,
        'savings': savings,
        'savings_pct': savings_pct,
    }
