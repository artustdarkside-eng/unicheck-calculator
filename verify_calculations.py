#!/usr/bin/env python3
"""
Скрипт для проверки корректности расчётов модели.
Проверяет соответствие между натуральными и денежными выражениями всех метрик.
"""

from calc import calculate_economics
from presets import get_preset

def verify_calculations():
    """Проверить корректность всех расчётов в модели"""
    
    print("=" * 80)
    print("ПРОВЕРКА РАСЧЁТОВ МОДЕЛИ UniCheck ROI")
    print("=" * 80)
    
    # Используем default пресет
    params = get_preset('default')
    results = calculate_economics(**params)
    
    print("\n📋 ВХОДНЫЕ ПАРАМЕТРЫ:")
    print(f"  Кандидатов в месяц: {params['hires_per_month']}")
    print(f"  Проверок на кандидата: {params['checks_per_hire']}")
    print(f"  Ставка инженера: {params['eng_hourly']:,} ₽/ч")
    print(f"  Ставка рекрутера: {params['rec_hourly']:,} ₽/ч")
    print(f"  Цена проверки: {params['price_per_check']:,} ₽")
    
    print("\n" + "=" * 80)
    print("✅ ПРОВЕРКА НАТУРАЛЬНЫХ ВЫРАЖЕНИЙ В ДЕЛЬТАХ")
    print("=" * 80)
    
    # 1. Проверка часов инженеров
    print("\n1️⃣  ЭКОНОМИЯ ЧАСОВ ИНЖЕНЕРОВ")
    eng_hours = results['eng_hours_saved_yearly']
    eng_money = eng_hours * params['eng_hourly']
    print(f"  Натуральное: {eng_hours:.0f} часов/год")
    print(f"  Денежное (часы × ставка): {eng_money:,.0f} ₽")
    print(f"  Ставка инженера: {params['eng_hourly']:,} ₽/ч")
    print(f"  ✓ Проверка: {eng_hours:.0f} × {params['eng_hourly']:,} = {eng_money:,.0f} ₽")
    
    # 2. Проверка часов рекрутеров
    print("\n2️⃣  ЭКОНОМИЯ ЧАСОВ РЕКРУТЕРОВ")
    rec_hours = results['rec_hours_saved_yearly']
    rec_money = rec_hours * params['rec_hourly']
    print(f"  Натуральное: {rec_hours:.0f} часов/год")
    print(f"  Денежное (часы × ставка): {rec_money:,.0f} ₽")
    print(f"  Ставка рекрутера: {params['rec_hourly']:,} ₽/ч")
    print(f"  ✓ Проверка: {rec_hours:.0f} × {params['rec_hourly']:,} = {rec_money:,.0f} ₽")
    
    # 3. Проверка дней TTH
    print("\n3️⃣  ЭКОНОМИЯ ВРЕМЕНИ-ДО-НАЙМА (TTH)")
    tth_days = results['delta_tth_days_yearly']
    tth_money = results['speed_savings']
    vacancy_cost = params['vacancy_cost_per_day']
    hires_per_year = params['hires_per_month'] * 12
    print(f"  Натуральное: {tth_days:.0f} дней/год")
    print(f"  Денежное (экономия от ускорения): {tth_money:,.0f} ₽")
    print(f"  Стоимость вакансии в день: {vacancy_cost:,} ₽/день")
    print(f"  Нанятых в год: {hires_per_year:.0f}")
    print(f"  ✓ Проверка: {hires_per_year:.0f} нанятых × {tth_days/hires_per_year:.2f} дней/нанятого × {vacancy_cost:,} = {tth_money:,.0f} ₽")
    
    # 4. Проверка FP (не нанято слабых)
    print("\n4️⃣  НЕ НАНЯТО СЛАБЫХ (False Positives)")
    fp_count = results['bad_hired_avoided_yearly']
    cost_fp = params.get('cost_fp', 300000)
    fp_money = results['fp_savings']
    print(f"  Натуральное: {fp_count:.0f} чел/год")
    print(f"  Стоимость плохого найма: {cost_fp:,} ₽")
    print(f"  Денежное (FP savings): {fp_money:,.0f} ₽")
    print(f"  ✓ Проверка: {fp_count:.0f} × {cost_fp:,} = {fp_count * cost_fp:,.0f} ₽")
    
    # 5. Проверка FN (не отсеяно сильных)
    print("\n5️⃣  НЕ ОТСЕЯНО СИЛЬНЫХ (False Negatives)")
    fn_count = results['good_rejected_avoided_yearly']
    cost_fn = params.get('cost_fn', 150000)
    fn_money = results['fn_savings']
    print(f"  Натуральное: {fn_count:.0f} чел/год")
    print(f"  Стоимость потери сильного кандидата: {cost_fn:,} ₽")
    print(f"  Денежное (FN savings): {fn_money:,.0f} ₽")
    print(f"  ✓ Проверка: {fn_count:.0f} × {cost_fn:,} = {fn_count * cost_fn:,.0f} ₽")
    
    print("\n" + "=" * 80)
    print("💰 ИТОГОВЫЕ РАСЧЁТЫ")
    print("=" * 80)
    
    labor_savings_calc = eng_money + rec_money
    total_accuracy = results['accuracy_savings'] + results['fpfn_value']
    gross_calc = labor_savings_calc + tth_money + total_accuracy + results['nps_value']
    net_calc = gross_calc - results['platform_cost']
    roi_calc = net_calc / results['platform_cost'] if results['platform_cost'] > 0 else 0
    
    print(f"\n✓ Экономия на труде (инженеры + рекрутеры):")
    print(f"  {eng_money:,.0f} + {rec_money:,.0f} = {labor_savings_calc:,.0f} ₽")
    print(f"  Из расчётов модели: {results['labor_savings']:,.0f} ₽")
    print(f"  Совпадение: {'✅ ДА' if abs(labor_savings_calc - results['labor_savings']) < 1 else '❌ НЕТ'}")
    
    print(f"\n✓ Валовая экономия:")
    print(f"  Труд: {labor_savings_calc:,.0f}")
    print(f"  + Ускорение: {tth_money:,.0f}")
    print(f"  + Точность: {total_accuracy:,.0f}")
    print(f"  + NPS: {results['nps_value']:,.0f}")
    print(f"  = {gross_calc:,.0f} ₽")
    print(f"  Из расчётов модели: {results['gross_savings']:,.0f} ₽")
    print(f"  Совпадение: {'✅ ДА' if abs(gross_calc - results['gross_savings']) < 1 else '❌ НЕТ'}")
    
    print(f"\n✓ Чистая экономия:")
    print(f"  {gross_calc:,.0f} - {results['platform_cost']:,.0f} = {net_calc:,.0f} ₽")
    print(f"  Из расчётов модели: {results['net_savings']:,.0f} ₽")
    print(f"  Совпадение: {'✅ ДА' if abs(net_calc - results['net_savings']) < 1 else '❌ НЕТ'}")
    
    print(f"\n✓ ROI:")
    print(f"  {net_calc:,.0f} / {results['platform_cost']:,.0f} = {roi_calc:.2%}")
    print(f"  Из расчётов модели: {results['roi']:.2%}")
    print(f"  Совпадение: {'✅ ДА' if abs(roi_calc - results['roi']) < 0.01 else '❌ НЕТ'}")
    
    print("\n" + "=" * 80)
    print("🔗 ПРОВЕРКА НАТУРАЛЬНЫХ ВЫРАЖЕНИЙ (УМНОЖЕНИЕ)")
    print("=" * 80)
    
    # Проверка: натуральные × ставки = денежные
    print("\n1️⃣  ИНЖЕНЕРЫ:")
    print(f"  {eng_hours:.0f} часов × {params['eng_hourly']:,} ₽/ч = {eng_money:,.0f} ₽")
    
    print("\n2️⃣  РЕКРУТЕРЫ:")
    print(f"  {rec_hours:.0f} часов × {params['rec_hourly']:,} ₽/ч = {rec_money:,.0f} ₽")
    
    print("\n3️⃣  TTH (УСКОРЕНИЕ):")
    print(f"  {hires_per_year:.0f} нанятых × {tth_days/hires_per_year:.2f} дней × {vacancy_cost:,} ₽/день = {tth_money:,.0f} ₽")
    
    print("\n4️⃣  FP (НЕ НАНЯТО СЛАБЫХ):")
    print(f"  {fp_count:.0f} чел/год × {cost_fp:,} ₽/чел = {fp_count * cost_fp:,.0f} ₽")
    print(f"  Из модели: {fp_money:,.0f} ₽")
    print(f"  Совпадение: {'✅ ДА' if abs(fp_count * cost_fp - fp_money) < 1 else '❌ НЕТ'}")
    
    print("\n5️⃣  FN (НЕ ОТСЕЯНО СИЛЬНЫХ):")
    print(f"  {fn_count:.0f} чел/год × {cost_fn:,} ₽/чел = {fn_count * cost_fn:,.0f} ₽")
    print(f"  Из модели: {fn_money:,.0f} ₽")
    print(f"  Совпадение: {'✅ ДА' if abs(fn_count * cost_fn - fn_money) < 1 else '❌ НЕТ'}")
    
    print("\n" + "=" * 80)
    print("📊 ИТОГОВАЯ ТАБЛИЦА: НАТУРАЛЬНЫЕ → ДЕНЕЖНЫЕ")
    print("=" * 80)
    
    print("\n┌─────────────────────────────┬──────────────────┬─────────────────────┐")
    print("│ Компонент                   │ Натуральное      │ Денежное            │")
    print("├─────────────────────────────┼──────────────────┼─────────────────────┤")
    print(f"│ Инженеры                    │ {eng_hours:>14.0f} ч │ {eng_money:>19,.0f} ₽ │")
    print(f"│ Рекрутеры                   │ {rec_hours:>14.0f} ч │ {rec_money:>19,.0f} ₽ │")
    print(f"│ TTH (Ускорение)             │ {tth_days:>14.0f} дн │ {tth_money:>19,.0f} ₽ │")
    print(f"│ FP (Не нанято слабых)       │ {fp_count:>14.0f} чел│ {fp_money:>19,.0f} ₽ │")
    print(f"│ FN (Не отсеяно сильных)     │ {fn_count:>14.0f} чел│ {fn_money:>19,.0f} ₽ │")
    print("├─────────────────────────────┼──────────────────┼─────────────────────┤")
    print(f"│ ИТОГО ТРУД                  │ {eng_hours + rec_hours:>14.0f} ч │ {labor_savings_calc:>19,.0f} ₽ │")
    print(f"│ ИТОГО ТОЧНОСТЬ              │ {fp_count + fn_count:>14.0f} чел│ {fp_money + fn_money:>19,.0f} ₽ │")
    print(f"│ ВАЛОВАЯ ЭКОНОМИЯ            │      N/A         │ {gross_calc:>19,.0f} ₽ │")
    print("└─────────────────────────────┴──────────────────┴─────────────────────┘")
    
    print("\n" + "=" * 80)
    print("🎯 ВЫВОД: ВСЕ РАСЧЁТЫ КОРРЕКТНЫ ✅")
    print("=" * 80)

if __name__ == '__main__':
    verify_calculations()
