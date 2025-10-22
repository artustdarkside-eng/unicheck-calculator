"""
Smoke-тесты модуля calc.py.

Проверяют корректность формул, краевые случаи и основные сценарии.
"""

import pytest
from calc import calculate_economics, calculate_single_check_economics
from presets import default, bank, retail, smb


class TestCalculateEconomics:
    """Тесты для calculate_economics."""
    
    def test_zero_hires_returns_zero_savings(self):
        """
        Сценарий 1: 0 наймов → все эффекты = 0, ROI = None.
        """
        params = default()
        params['hires_per_month'] = 0
        params['checks_per_hire'] = 2
        
        result = calculate_economics(**params)
        
        assert result['gross_savings'] == 0
        assert result['platform_cost'] == 0
        assert result['net_savings'] == 0
        assert result['roi'] is None
        assert result['labor_savings'] == 0
        assert result['speed_savings'] == 0
        assert result['accuracy_savings'] == 0
    
    def test_equal_params_zero_labor_savings(self):
        """
        Сценарий 2: При равных параметрах ручного и UniCheck → экономия труда = 0.
        """
        params = default()
        # Делаем параметры идентичными
        params['eng_hours_per_cand_manual'] = 1.0
        params['eng_hours_per_cand_unicheck'] = 1.0
        params['rec_hours_per_cand_manual'] = 0.5
        params['rec_hours_per_cand_unicheck'] = 0.5
        params['bad_hire_rate_manual_pct'] = 10
        params['bad_hire_rate_unicheck_pct'] = 10
        params['time_to_test_start_manual_days'] = 3
        params['time_to_test_start_unicheck_days'] = 3
        params['time_to_test_finish_manual_days'] = 7
        params['time_to_test_finish_unicheck_days'] = 7
        
        result = calculate_economics(**params)
        
        # Экономия труда должна быть 0
        assert result['labor_savings'] == 0
        # Экономия от ускорения должна быть 0
        assert result['speed_savings'] == 0
        # Экономия от точности должна быть 0
        assert result['accuracy_savings'] == 0
    
    def test_lower_bad_hire_rate_increases_savings(self):
        """
        Сценарий 3: Понижение bad_hire_rate_unicheck уменьшает ущерб → экономия растёт.
        """
        params_high_error = default()
        params_high_error['bad_hire_rate_unicheck_pct'] = 10  # Высокая ошибка
        
        params_low_error = default()
        params_low_error['bad_hire_rate_unicheck_pct'] = 3   # Низкая ошибка
        
        result_high = calculate_economics(**params_high_error)
        result_low = calculate_economics(**params_low_error)
        
        # При низкой ошибке экономия должна быть выше
        assert result_low['accuracy_savings'] > result_high['accuracy_savings']
        assert result_low['net_savings'] > result_high['net_savings']
    
    def test_fpfn_model_increases_value(self):
        """
        Сценарий 4: Включение FP/FN с лучшими метриками UniCheck увеличивает fpfn_value.
        """
        params = default()
        params['use_fpfn_model'] = False
        
        result_without_fpfn = calculate_economics(**params)
        
        params['use_fpfn_model'] = True
        # Делаем UniCheck лучше в FP/FN
        params['fp_rate_manual_pct'] = 15
        params['fn_rate_manual_pct'] = 18
        params['fp_rate_unicheck_pct'] = 8
        params['fn_rate_unicheck_pct'] = 10
        
        result_with_fpfn = calculate_economics(**params)
        
        # FP/FN value должно быть положительным
        assert result_with_fpfn['fpfn_value'] > 0
        # Общая экономия должна вырасти
        assert result_with_fpfn['gross_savings'] > result_without_fpfn['gross_savings']
    
    def test_zero_price_prevents_division(self):
        """
        Сценарий 5: price_per_check = 0 → не делим на 0, ROI = None.
        """
        params = default()
        params['price_per_check'] = 0
        
        result = calculate_economics(**params)
        
        # Не должно быть исключения
        assert result['platform_cost'] == 0
        assert result['roi'] is None  # Не можем считать ROI без платформы
    
    def test_adoption_pct_edge_cases(self):
        """
        Сценарий 6: checks_per_hire = 0 и max.
        """
        params = default()
        
        # checks_per_hire = 0 → никто не проходит UniCheck
        params['checks_per_hire'] = 0
        result_zero = calculate_economics(**params)
        assert result_zero['candidates_unicheck'] == 0
        assert result_zero['platform_cost'] == 0
        
        # checks_per_hire = 5 → все 5 проверок 
        params['checks_per_hire'] = 5
        result_full = calculate_economics(**params)
        total_checks = result_full['total_checks']
        assert result_full['candidates_unicheck'] == total_checks
        assert result_full['platform_cost'] > 0
    
    def test_csv_export_contains_key_rows(self):
        """
        Сценарий 7: Результаты содержат ключевые поля.
        """
        params = default()
        result = calculate_economics(**params)
        
        # Проверяем, что результат содержит ключевые поля
        required_fields = [
            'gross_savings', 'platform_cost', 'net_savings', 'roi',
            'labor_savings', 'speed_savings', 'accuracy_savings',
            'total_checks', 'candidates_unicheck'
        ]
        
        for field in required_fields:
            assert field in result, f"Missing field: {field}"
    
    def test_results_are_non_negative(self):
        """
        Сценарий 8: Экономия не может быть отрицательной (проверка логики max(0, ...)).
        """
        params = default()
        result = calculate_economics(**params)
        
        # Все компоненты экономии должны быть >= 0
        assert result['labor_savings'] >= 0
        assert result['speed_savings'] >= 0
        assert result['accuracy_savings'] >= 0
        assert result['fpfn_value'] >= 0
        assert result['nps_value'] >= 0
    
    def test_presets_are_valid(self):
        """
        Проверка, что все пресеты дают корректные результаты.
        """
        presets = [default(), bank(), retail(), smb()]
        
        for preset in presets:
            result = calculate_economics(**preset)
            
            # Должна быть валидная экономия
            assert isinstance(result['gross_savings'], (int, float))
            assert result['gross_savings'] >= 0
            # Метрики должны быть числами
            assert isinstance(result['delta_tth_days'], (int, float))
            assert result['delta_tth_days'] >= 0


class TestSingleCheckEconomics:
    """Тесты для calculate_single_check_economics."""
    
    def test_single_check_cost_comparison(self):
        """Проверка логики расчёта стоимости на одной проверке."""
        result = calculate_single_check_economics(
            eng_hourly=4000,
            rec_hourly=1500,
            eng_hours_manual=1.0,
            rec_hours_manual=0.5,
            eng_hours_unicheck=0.2,
            rec_hours_unicheck=0.2,
            price_per_check=1500,
        )
        
        # Ручная стоимость: 4000*1 + 1500*0.5 = 4750
        assert result['manual_cost'] == 4750
        
        # UniCheck труд: 4000*0.2 + 1500*0.2 = 1100
        assert result['unicheck_cost_labor'] == 1100
        
        # UniCheck всего: 1100 + 1500 = 2600
        assert result['unicheck_cost_total'] == 2600
        
        # Экономия: 4750 - 2600 = 2150
        assert result['savings'] == 2150
    
    def test_single_check_zero_price(self):
        """При цене = 0, экономия максимальна."""
        result = calculate_single_check_economics(
            eng_hourly=4000,
            rec_hourly=1500,
            eng_hours_manual=1.0,
            rec_hours_manual=0.5,
            eng_hours_unicheck=0.2,
            rec_hours_unicheck=0.2,
            price_per_check=0,
        )
        
        # UniCheck без платформы дешевле
        assert result['savings'] > 0
        assert result['unicheck_platform_cost'] == 0


# === ЗАПУСК ТЕСТОВ ===

if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
