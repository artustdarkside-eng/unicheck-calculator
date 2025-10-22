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
        'hires_per_month': 30,
        'checks_per_hire': 5,
        
        # B. Часы и ставки
        'eng_hourly': 5000,
        'rec_hourly': 2000,
        'eng_hours_per_cand_manual': 2.5,
        'rec_hours_per_cand_manual': 2.0,
        'eng_hours_per_cand_unicheck': 0.0,
        'rec_hours_per_cand_unicheck': 0.5,
        
        # C. Сроки процесса
        'time_to_test_start_manual_days': 3,
        'time_to_test_start_unicheck_days': 1,
        'time_to_test_finish_manual_days': 2,
        'time_to_test_finish_unicheck_days': 1,
        'vacancy_cost_per_day': 7000,
        
        # D. Точность (основная модель)
        'bad_hire_rate_manual_pct': 10,
        'bad_hire_rate_unicheck_pct': 5,
        'cost_bad_hire': 400000,
        
        # D. Точность (FP/FN модель)
        'good_candidates_share': 30,
        'fp_rate_manual_pct': 13,
        'fn_rate_manual_pct': 15,
        'fp_rate_unicheck_pct': 7,
        'fn_rate_unicheck_pct': 9,
        'cost_fp': 300000,
        'cost_fn': 150000,
        
        # E. Стоимость UniCheck
        'price_per_check': 3500,
        
        # F. NPS
        'nps_manual': 75,
        'nps_unicheck': 95,
        'nps_to_value_coef': 1000.0,
        
        # Флаги использования моделей
        'use_fpfn_model': True,
        'use_nps_money': True,
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

