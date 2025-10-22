"""
Пресеты входных параметров для различных типов компаний.
"""

from typing import Dict


def default() -> Dict:
    """
    Дефолтный пресет.
    Используется как базовое значение при загрузке приложения и при сбросе параметров.
    """
    return {
        # A. План и объёмы
        'hires_per_month': 20,
        'checks_per_hire': 2,
        
        # B. Часы и ставки
        'eng_hourly': 4000,
        'rec_hourly': 1500,
        'eng_hours_per_cand_manual': 1.0,
        'rec_hours_per_cand_manual': 0.5,
        'eng_hours_per_cand_unicheck': 0.2,
        'rec_hours_per_cand_unicheck': 0.2,
        
        # C. Сроки процесса
        'time_to_test_start_manual_days': 3,
        'time_to_test_start_unicheck_days': 1,
        'time_to_test_finish_manual_days': 48,  # 6 дней × 8 часов = 48 часов
        'time_to_test_finish_unicheck_days': 8,  # 1 день × 8 часов = 8 часов
        'vacancy_cost_per_day': 8000,  # Консервативная оценка
        
        # D. Точность (основная модель)
        'bad_hire_rate_manual_pct': 10,
        'bad_hire_rate_unicheck_pct': 6,
        'cost_bad_hire': 400000,
        
        # D. Точность (FP/FN модель)
        'good_candidates_share': 30,
        'fp_rate_manual_pct': 12,
        'fn_rate_manual_pct': 15,
        'fp_rate_unicheck_pct': 8,
        'fn_rate_unicheck_pct': 10,
        'cost_fp': 300000,
        'cost_fn': 150000,
        
        # E. Стоимость UniCheck
        'price_per_check': 1500,
        
        # F. NPS
        'nps_manual': 10,
        'nps_unicheck': 40,
        'nps_to_value_coef': 0,
        
        # Флаги использования моделей
        'use_fpfn_model': False,
        'use_nps_money': False,
    }


# Список доступных пресетов (только default)
PRESETS = {
    'default': default,
}


def get_preset(name: str) -> Dict:
    """
    Получить пресет по имени.
    
    Args:
        name: Имя пресета. Если не найден, возвращает default.
    
    Returns:
        Словарь с параметрами
    """
    if name in PRESETS:
        return PRESETS[name]()
    else:
        return default()

