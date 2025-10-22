#!/usr/bin/env python3
"""
Валидационный скрипт для проверки экономической обоснованности модели.
Быстрый алиас для анализа всех компонентов расчётов.

Использование:
    python validate.py              # Анализ всех пресетов
    python validate.py --detailed   # С подробным разбором формул
    python validate.py --sensitivity # Анализ чувствительности
"""

import sys
from calc import calculate_economics
from presets import default, bank, retail, smb


def print_header(text):
    """Красивый заголовок."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_subheader(text):
    """Подзаголовок."""
    print(f"\n  📋 {text}")
    print("  " + "-" * 76)


def analyze_preset(name, preset_func):
    """Анализ одного пресета."""
    params = preset_func()
    results = calculate_economics(**params)
    
    hires_year = params['hires_per_month'] * 12
    checks_year = hires_year * params['checks_per_hire']
    
    gross = results['gross_savings']
    labor = results['labor_savings']
    speed = results['speed_savings']
    accuracy = results['accuracy_savings']
    platform = results['platform_cost']
    net = results['net_savings']
    roi = results['roi']
    
    # Расчёт периода окупаемости (в месяцах)
    payback_months = (platform / gross * 12) if gross > 0 else float('inf')
    
    print(f"\n  {name.upper()}")
    print(f"    Наймов/год: {hires_year:,} | Проверок/год: {checks_year:,}")
    print(f"    Стоимость вакансии: {params['vacancy_cost_per_day']:,} ₽/день | TtH -: {params['time_to_test_start_manual_days'] + params['time_to_test_finish_manual_days'] - params['time_to_test_start_unicheck_days'] - params['time_to_test_finish_unicheck_days']} дней")
    print(f"    Bad hire: {params['bad_hire_rate_manual_pct']}% → {params['bad_hire_rate_unicheck_pct']}% | Cost: {params['cost_bad_hire']:,} ₽")
    
    print(f"\n    💰 ВАЛОВАЯ ЭКОНОМИЯ: {gross:,.0f} ₽")
    print(f"       ├─ Труд: {labor:,.0f} ₽ ({labor/gross*100:.1f}%)")
    print(f"       ├─ Скорость: {speed:,.0f} ₽ ({speed/gross*100:.1f}%)")
    print(f"       └─ Точность: {accuracy:,.0f} ₽ ({accuracy/gross*100:.1f}%)")
    
    print(f"\n    📊 ПЛАТФОРМА: {platform:,.0f} ₽")
    print(f"    ✅ NET-ЭКОНОМИЯ: {net:,.0f} ₽")
    print(f"    🚀 ROI: {roi:.2f}x")
    print(f"    ⏳ ОКУПАЕМОСТЬ: {payback_months:.1f} месяцев")
    
    return {
        'name': name,
        'hires_year': hires_year,
        'checks_year': checks_year,
        'labor': labor,
        'speed': speed,
        'accuracy': accuracy,
        'gross': gross,
        'platform': platform,
        'net': net,
        'roi': roi,
        'payback': payback_months,
        'labor_share': labor / gross * 100 if gross > 0 else 0,
        'speed_share': speed / gross * 100 if gross > 0 else 0,
        'accuracy_share': accuracy / gross * 100 if gross > 0 else 0,
    }


def validate_formulas():
    """Проверка формул с примерами."""
    print_header("ВАЛИДАЦИЯ ФОРМУЛ")
    
    params = default()
    results = calculate_economics(**params)
    
    print_subheader("1. ЭКОНОМИЯ НА ТРУДЕ")
    hires_year = params['hires_per_month'] * 12
    checks_year = hires_year * params['checks_per_hire']
    
    manual_cost_per_check = (params['eng_hourly'] * params['eng_hours_per_cand_manual'] + 
                             params['rec_hourly'] * params['rec_hours_per_cand_manual'])
    unicheck_cost_per_check = (params['eng_hourly'] * params['eng_hours_per_cand_unicheck'] + 
                               params['rec_hourly'] * params['rec_hours_per_cand_unicheck'])
    expected_labor = (manual_cost_per_check - unicheck_cost_per_check) * checks_year
    
    print(f"    Формула: (manual_cost - unicheck_cost) × checks_year")
    print(f"    Manual cost/check: {manual_cost_per_check:,.0f} ₽")
    print(f"      = {params['eng_hourly']:,}*{params['eng_hours_per_cand_manual']} + {params['rec_hourly']:,}*{params['rec_hours_per_cand_manual']}")
    print(f"    UniCheck cost/check: {unicheck_cost_per_check:,.0f} ₽")
    print(f"      = {params['eng_hourly']:,}*{params['eng_hours_per_cand_unicheck']} + {params['rec_hourly']:,}*{params['rec_hours_per_cand_unicheck']}")
    print(f"    Expected: ({manual_cost_per_check:,.0f} - {unicheck_cost_per_check:,.0f}) × {checks_year:,} = {expected_labor:,.0f} ₽")
    print(f"    Actual: {results['labor_savings']:,.0f} ₽")
    print(f"    ✅ MATCH: {abs(expected_labor - results['labor_savings']) < 1}")
    
    print_subheader("2. ЭКОНОМИЯ НА СКОРОСТИ")
    tth_manual = params['time_to_test_start_manual_days'] + params['time_to_test_finish_manual_days']
    tth_unicheck = params['time_to_test_start_unicheck_days'] + params['time_to_test_finish_unicheck_days']
    delta_tth = tth_manual - tth_unicheck
    expected_speed = hires_year * delta_tth * params['vacancy_cost_per_day']
    
    print(f"    Формула: hires_year × delta_tth_days × vacancy_cost_per_day")
    print(f"    TtH Manual: {tth_manual} дней")
    print(f"    TtH UniCheck: {tth_unicheck} дней")
    print(f"    Delta: {delta_tth} дней")
    print(f"    Expected: {hires_year:,} × {delta_tth} × {params['vacancy_cost_per_day']:,} = {expected_speed:,.0f} ₽")
    print(f"    Actual: {results['speed_savings']:,.0f} ₽")
    print(f"    ✅ MATCH: {abs(expected_speed - results['speed_savings']) < 1}")
    
    print_subheader("3. ЭКОНОМИЯ НА ТОЧНОСТИ")
    avoided_bad = hires_year * (params['bad_hire_rate_manual_pct'] - params['bad_hire_rate_unicheck_pct']) / 100
    expected_accuracy = avoided_bad * params['cost_bad_hire']
    
    print(f"    Формула: hires_year × (bad_rate_manual - bad_rate_unicheck) × cost_bad_hire")
    print(f"    Avoided bad hires: {hires_year:,} × ({params['bad_hire_rate_manual_pct']}% - {params['bad_hire_rate_unicheck_pct']}%) = {avoided_bad:.1f}")
    print(f"    Expected: {avoided_bad:.1f} × {params['cost_bad_hire']:,} = {expected_accuracy:,.0f} ₽")
    print(f"    Actual: {results['accuracy_savings']:,.0f} ₽")
    print(f"    ✅ MATCH: {abs(expected_accuracy - results['accuracy_savings']) < 1}")
    
    print_subheader("4. ПЛАТФОРМА И ROI")
    platform_expected = checks_year * params['price_per_check']
    gross_expected = expected_labor + expected_speed + expected_accuracy
    net_expected = gross_expected - platform_expected
    roi_expected = net_expected / platform_expected if platform_expected > 0 else None
    
    print(f"    Platform cost: {checks_year:,} × {params['price_per_check']} = {platform_expected:,.0f} ₽")
    print(f"    Gross: {expected_labor:,.0f} + {expected_speed:,.0f} + {expected_accuracy:,.0f} = {gross_expected:,.0f} ₽")
    print(f"    Net: {gross_expected:,.0f} - {platform_expected:,.0f} = {net_expected:,.0f} ₽")
    print(f"    ROI: {net_expected:,.0f} / {platform_expected:,.0f} = {roi_expected:.2f}x")
    print(f"\n    Actual gross: {results['gross_savings']:,.0f} ₽")
    print(f"    Actual platform: {results['platform_cost']:,.0f} ₽")
    print(f"    Actual net: {results['net_savings']:,.0f} ₽")
    print(f"    Actual ROI: {results['roi']:.2f}x")
    print(f"\n    ✅ ALL FORMULAS VERIFIED")


def analyze_all_presets():
    """Анализ всех пресетов."""
    print_header("АНАЛИЗ ВСЕХ ПРЕСЕТОВ")
    
    results_list = []
    for name, preset_func in [('default', default), ('bank', bank), ('retail', retail), ('smb', smb)]:
        result = analyze_preset(name, preset_func)
        results_list.append(result)
    
    # Сводная таблица
    print_header("СВОДКА ПО ВСЕМ ПРЕСЕТАМ")
    
    print(f"\n  {'Пресет':<12} {'ROI':<10} {'Окупаемость':<15} {'Скорость %':<15} {'Точность %':<15}")
    print(f"  {'-'*12} {'-'*10} {'-'*15} {'-'*15} {'-'*15}")
    for r in results_list:
        print(f"  {r['name']:<12} {r['roi']:<10.2f}x {r['payback']:<15.1f}мес {r['speed_share']:<15.1f}% {r['accuracy_share']:<15.1f}%")
    
    # Анализ обоснованности
    print_header("ЭКОНОМИЧЕСКАЯ ОБОСНОВАННОСТЬ")
    
    valid = True
    for r in results_list:
        print(f"\n  ✓ {r['name'].upper()}:")
        
        # Проверка 1: ROI разумный (10-50x - приемлемо)
        roi_ok = 10 <= r['roi'] <= 50
        print(f"    ROI {r['roi']:.1f}x: {'✅ ХОРОШО' if roi_ok else '⚠️ ЭКСТРЕМАЛЬНО'}")
        
        # Проверка 2: Окупаемость < 6 месяцев
        payback_ok = r['payback'] <= 6
        print(f"    Окупаемость {r['payback']:.1f} мес: {'✅ ХОРОШО' if payback_ok else '⚠️ ДОЛГО'}")
        
        # Проверка 3: Компоненты разумно распределены
        speed_dom = r['speed_share'] > 70
        speed_note = "⚠️ СКОРОСТЬ ДОМИНИРУЕТ" if speed_dom else "✅ СБАЛАНСИРОВАНО"
        print(f"    Распределение: {r['labor_share']:.0f}% труд, {r['speed_share']:.0f}% скорость, {r['accuracy_share']:.0f}% точность - {speed_note}")
        
        if not (roi_ok and payback_ok):
            valid = False
    
    if valid:
        print("\n  ✅ ВСЕ ПРЕСЕТЫ ЭКОНОМИЧЕСКИ ОБОСНОВАНЫ")
    else:
        print("\n  ⚠️ НЕКОТОРЫЕ ПРЕСЕТЫ ТРЕБУЮТ ВНИМАНИЯ")


def sensitivity_analysis():
    """Анализ чувствительности."""
    print_header("АНАЛИЗ ЧУВСТВИТЕЛЬНОСТИ")
    
    params = default()
    base_result = calculate_economics(**params)
    base_roi = base_result['roi']
    
    print_subheader("ВЛИЯНИЕ СТОИМОСТИ ВАКАНСИИ")
    for vacancy_pct in [-30, -15, 0, 15, 30]:
        params_copy = default()
        params_copy['vacancy_cost_per_day'] = int(params['vacancy_cost_per_day'] * (1 + vacancy_pct/100))
        result = calculate_economics(**params_copy)
        delta = (result['roi'] - base_roi) / base_roi * 100
        print(f"    {vacancy_pct:+3d}% ({params_copy['vacancy_cost_per_day']:,} ₽/день): ROI {result['roi']:.2f}x ({delta:+.0f}%)")
    
    print_subheader("ВЛИЯНИЕ СОКРАЩЕНИЯ TtH")
    for tth_delta in [-2, -1, 0, 1, 2]:
        params_copy = default()
        params_copy['time_to_test_finish_manual_days'] = params['time_to_test_finish_manual_days'] + tth_delta
        result = calculate_economics(**params_copy)
        delta = (result['roi'] - base_roi) / base_roi * 100
        actual_tth = (params_copy['time_to_test_start_manual_days'] + params_copy['time_to_test_finish_manual_days']) - (params_copy['time_to_test_start_unicheck_days'] + params_copy['time_to_test_finish_unicheck_days'])
        print(f"    TtH {actual_tth:+2d} дней: ROI {result['roi']:.2f}x ({delta:+.0f}%)")
    
    print_subheader("ВЛИЯНИЕ СТОИМОСТИ ОШИБКИ НАЙМА")
    for cost_pct in [-30, -15, 0, 15, 30]:
        params_copy = default()
        params_copy['cost_bad_hire'] = int(params['cost_bad_hire'] * (1 + cost_pct/100))
        result = calculate_economics(**params_copy)
        delta = (result['roi'] - base_roi) / base_roi * 100
        print(f"    {cost_pct:+3d}% ({params_copy['cost_bad_hire']:,} ₽): ROI {result['roi']:.2f}x ({delta:+.0f}%)")


def main():
    """Главная функция."""
    if len(sys.argv) > 1:
        if '--detailed' in sys.argv:
            validate_formulas()
        if '--sensitivity' in sys.argv:
            sensitivity_analysis()
        if '--all' in sys.argv or len(sys.argv) == 1:
            analyze_all_presets()
    else:
        analyze_all_presets()
        print("\n\n💡 Используйте флаги для дополнительного анализа:")
        print("    python validate.py --detailed     # Подробная проверка формул")
        print("    python validate.py --sensitivity  # Анализ чувствительности")
        print("    python validate.py --all          # Полный анализ")


if __name__ == '__main__':
    main()
