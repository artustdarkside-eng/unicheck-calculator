#!/usr/bin/env python3
"""
Быстрый анализ модели экономики UniCheck.
Запуск: python analyze.py
"""

import sys
import os

# Добавить текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from calc import calculate_economics
    from presets import default, bank, retail, smb
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Убедись, что в той же папке есть calc.py и presets.py")
    sys.exit(1)

def analyze():
    """Вывести полный анализ модели."""
    print("\n" + "=" * 80)
    print("АНАЛИЗ МОДЕЛИ КАЛЬКУЛЯТОРА UNICHECK")
    print("=" * 80 + "\n")
    
    for name, preset_func in [
        ("📘 DEFAULT", default),
        ("🏦 BANK", bank),
        ("🛍️ RETAIL", retail),
        ("💼 SMB", smb),
    ]:
        try:
            params = preset_func()
            results = calculate_economics(**params)
            
            hires_year = params['hires_per_month'] * 12
            checks_year = hires_year * params['checks_per_hire']
            tth_reduction = (params['time_to_test_start_manual_days'] + 
                            params['time_to_test_finish_manual_days']) - \
                           (params['time_to_test_start_unicheck_days'] + 
                            params['time_to_test_finish_unicheck_days'])
            
            gross = results['gross_savings']
            
            print(f"{name}")
            print("-" * 80)
            print(f"  Наймов/год: {hires_year:,} | Проверок/год: {checks_year:,}")
            print(f"  Стоимость вакансии: {params['vacancy_cost_per_day']:,} ₽/день | TtH сокращение: {tth_reduction} дней")
            print(f"  Улучшение точности: {params['bad_hire_rate_manual_pct']}% → {params['bad_hire_rate_unicheck_pct']}% | Стоимость ошибки: {params['cost_bad_hire']:,} ₽")
            print()
            
            print(f"  💰 Валовая экономия: {gross:,.0f} ₽")
            print(f"     └─ Труд: {results['labor_savings']:,.0f} ₽ ({results['labor_savings']/gross*100:.1f}%)")
            print(f"     └─ Скорость: {results['speed_savings']:,.0f} ₽ ({results['speed_savings']/gross*100:.1f}%)")
            print(f"     └─ Точность: {results['accuracy_savings']:,.0f} ₽ ({results['accuracy_savings']/gross*100:.1f}%)")
            print()
            
            payback_months = (results['platform_cost'] / gross * 12) if gross > 0 else float('inf')
            
            print(f"  📊 Стоимость платформы: {results['platform_cost']:,.0f} ₽")
            print(f"  ✅ Net-экономия: {results['net_savings']:,.0f} ₽")
            print(f"  🚀 ROI: {results['roi']:.2f}x")
            print(f"  ⏱️  Окупаемость: {payback_months:.1f} месяцев")
            print("\n")
        except Exception as e:
            print(f"❌ Ошибка при анализе {name}: {e}\n")

if __name__ == '__main__':
    analyze()
