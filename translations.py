"""
Система переводов для калькулятора UniCheck.
"""

TRANSLATIONS = {
    'ru': {
        # Основные элементы интерфейса
        'page_title': 'Калькулятор эффекта UniCheck',
        'language_selector': 'Язык / Language',
        'sidebar_title': 'Параметры расчёта',
        'preset_selector': 'Выберите пресет',
        'load_preset': 'Загрузить пресет',
        'save_preset': 'Сохранить текущие параметры',
        'preset_name': 'Название пресета',
        'save_button': 'Сохранить',
        'download_results': 'Скачать результаты',
        
        # Разделы параметров
        'section_plan': 'A. План и объёмы',
        'section_rates': 'B. Часы и ставки',
        'section_timing': 'C. Сроки процесса',
        'section_accuracy': 'D. Точность и качество найма',
        'section_costs': 'E. Стоимость и ROI',
        'section_nps': 'F. Эффект NPS (опционально)',
        
        # Параметры плана и объёмов
        'hires_per_month': 'Наймов в месяц',
        'hires_per_month_help': 'Сколько человек планируете нанимать ежемесячно',
        'checks_per_hire': 'Проверок на 1 найм',
        'checks_per_hire_help': 'В среднем сколько кандидатов проверяете на одного нанятого',
        
        # Часы и ставки
        'eng_hourly': 'Ставка инженера, ₽/час',
        'rec_hourly': 'Ставка рекрутера, ₽/час',
        'eng_hours_manual': 'Часы инженера на кандидата (ручной)',
        'rec_hours_manual': 'Часы рекрутера на кандидата (ручной)',
        'eng_hours_unicheck': 'Часы инженера на кандидата (UniCheck)',
        'rec_hours_unicheck': 'Часы рекрутера на кандидата (UniCheck)',
        
        # Сроки процесса
        'time_to_test_start_manual': 'Дней до начала тестирования (ручной)',
        'time_to_test_start_unicheck': 'Дней до начала тестирования (UniCheck)',
        'time_to_test_finish_manual': 'Дней на завершение тестирования (ручной)',
        'time_to_test_finish_unicheck': 'Дней на завершение тестирования (UniCheck)',
        'vacancy_cost_per_day': 'Стоимость простоя вакансии, ₽/день',
        
        # Точность
        'bad_hire_rate_manual': 'Доля плохих наймов (ручной), %',
        'bad_hire_rate_unicheck': 'Доля плохих наймов (UniCheck), %',
        'cost_bad_hire': 'Стоимость плохого найма, ₽',
        'good_candidates_share': 'Доля хороших кандидатов, %',
        'fp_rate_manual': 'False Positive (ручной), %',
        'fn_rate_manual': 'False Negative (ручной), %',
        'fp_rate_unicheck': 'False Positive (UniCheck), %',
        'fn_rate_unicheck': 'False Negative (UniCheck), %',
        
        # Стоимость и ROI
        'unicheck_cost_per_check': 'Стоимость 1 проверки UniCheck, ₽',
        'unicheck_setup_cost': 'Стоимость внедрения UniCheck, ₽',
        'discount_rate': 'Ставка дисконтирования, %',
        'analysis_period': 'Период анализа, месяцев',
        
        # NPS
        'enable_nps': 'Учитывать эффект NPS',
        'nps_improvement': 'Рост NPS кандидатов',
        'nps_monetary_value': 'Денежная ценность роста NPS, ₽/мес',
        
        # Результаты
        'results_title': 'Результаты расчёта',
        'total_savings': 'Общая экономия',
        'monthly_savings': 'Ежемесячная экономия',
        'annual_savings': 'Годовая экономия',
        'roi_title': 'Возврат инвестиций (ROI)',
        'payback_period': 'Срок окупаемости',
        'npv': 'Чистая приведенная стоимость (NPV)',
        
        # Компоненты экономии
        'labor_costs': 'Затраты на труд',
        'tth_costs': 'Простой вакансии (TtH)',
        'accuracy_costs': 'Ошибочный найм (точность)',
        'total_per_check': 'Итого на проверку',
        
        # Таблицы
        'component': 'Компонент',
        'manual_cost': 'Ручной, ₽',
        'unicheck_cost': 'UniCheck, ₽',
        'savings_rub': 'Экономия, ₽',
        'savings_percent': 'Экономия, %',
        
        # Графики
        'cost_breakdown_title': 'Разбивка затрат по компонентам',
        'manual': 'Ручной',
        'unicheck': 'UniCheck',
        'savings': 'Экономия',
        
        # Экспорт
        'input_params': 'ВХОДНЫЕ ПАРАМЕТРЫ',
        'calculation_results': 'РЕЗУЛЬТАТЫ РАСЧЁТА',
        
        # Дисклеймер
        'disclaimer': '⚠️ **Дисклеймер:** Модель ориентировочная и может отличаться от реальных результатов. Все расчёты основаны на входных параметрах. Рекомендуется валидировать предположения на реальных данных вашей компании.',
        
        # Слайдеры и элементы управления
        'slider_mode': 'Режим слайдеров',
        'number_input_mode': 'Поля ввода',
        'slider_input_mode': 'Слайдеры',
        
        # Дополнительные переводы
        'unicheck': 'UniCheck',
        'saved_presets': 'Сохраненные пресеты',
        'detailed_accuracy_model': 'Детальная модель точности (FP/FN)',
        'techscreen_errors_cost': 'Стоимость ошибок техскрина',
        'comparison_subtitle': 'Сравнение найма с UniCheck vs ручные проверки',
        'reset_params': 'Сброс параметров',
        'use_fpfn_analysis': 'Использовать FP/FN анализ',
        'fpfn_help': 'Дополнительно учитывать ложные отказы и ложные одобрения на этапе техскрина',
        'nps_enable_help': 'Если включено, разница NPS будет переведена в денежный эффект',
        
        # Метрики
        'labor_hours_savings': 'Экономия человеко-часов',
        'engineers': 'Инженеры',
        'recruiters': 'Рекрутеры',
        'hours_per_year': 'часов/год',
        'speed_savings': 'Экономия от ускорения',
        'tth_days_per_year': 'дней/год',
        'accuracy_savings_metric': 'Экономия от точности',
        'weak_not_hired': 'Не нанято слабых',
        'strong_not_rejected': 'Не отсеяно сильных',
        'nps_effect': 'NPS эффект',
        'total_savings_metric': 'Итоговая экономия',
        'months': 'мес.',
        'payback': 'Окупаемость',
        
        # CSV Export headers
        'csv_indicator': 'Показатель',
        'csv_value': 'Значение',
        'csv_hours_rates': 'B. Часы и ставки',
        'csv_eng_rate': 'Ставка инженера, ₽/час',
        'csv_rec_rate': 'Ставка рекрутера, ₽/час',
        'csv_eng_hours_manual': 'Часы инженера на кандидата (ручной)',
        'csv_rec_hours_manual': 'Часы рекрутера на кандидата (ручной)',
        'csv_eng_hours_unicheck': 'Часы инженера на кандидата (UniCheck)',
        'csv_rec_hours_unicheck': 'Часы рекрутера на кандидата (UniCheck)',
        'csv_timing': 'C. Сроки процесса',
        'csv_days_to_start_manual': 'Дней до старта теста (ручной)',
        'csv_days_to_start_unicheck': 'Дней до старта теста (UniCheck)',
        'csv_test_duration_manual': 'Длительность теста (ручной)',
        'csv_test_duration_unicheck': 'Длительность теста (UniCheck)',
        'csv_vacancy_cost': 'Стоимость незакрытой позиции, ₽/день',
        'csv_accuracy': 'D. Точность',
        'csv_bad_hire_manual': 'Доля ошибочных наймов (ручной), %',
        'csv_bad_hire_unicheck': 'Доля ошибочных наймов (UniCheck), %',
        'csv_bad_hire_cost': 'Стоимость ошибочного найма, ₽',
        'csv_unicheck_cost': 'E. Стоимость UniCheck',
        'csv_price_per_check': 'Цена проверки, ₽',
        'csv_nps_manual': 'NPS (ручной процесс)',
        'csv_results': 'РЕЗУЛЬТАТЫ РАСЧЁТОВ',
        'csv_key_metrics': 'Ключевые метрики',
        'csv_gross_savings': 'Валовая экономия, ₽',
        'csv_platform_cost': 'Стоимость платформы, ₽',
        'csv_net_savings': 'Net-экономия, ₽',
        'csv_tth_reduction': 'Сокращение Time-to-Hire, дней',
        'csv_accuracy_improvement': 'Улучшение точности, п.п.',
        'csv_breakdown': 'Разбивка экономии',
        'csv_labor_savings': 'Экономия человеко-часов, ₽',
        'csv_speed_savings': 'Экономия от ускорения, ₽',
        'csv_accuracy_savings': 'Экономия от точности, ₽',
        'csv_fpfn_savings': 'Экономия от FP/FN, ₽',
        'csv_nps_effect': 'Эффект NPS, ₽',
        'csv_per_candidate': 'Метрики на кандидата',
        'csv_gross_per_candidate': 'Валовая экономия на кандидата, ₽',
        'csv_platform_per_candidate': 'Платформа на кандидата, ₽',
        'csv_net_per_candidate': 'Net на кандидата, ₽',
        'csv_per_hire': 'Метрики на найм',
        'csv_gross_per_hire': 'Валовая экономия на найм, ₽',
        'csv_platform_per_hire': 'Платформа на найм, ₽',
        'csv_net_per_hire': 'Net на найм, ₽',
        
        # Chart and table labels
        'pie_chart_title': 'Составляющие валовой экономии',
        'component_labor': 'Человеко-часы',
        'component_speed': 'Ускорение',
        'component_accuracy': 'Точность',
        'component_nps': 'NPS эффект',
        'chart_savings_label': 'Экономия',
        'chart_cost_label': 'Стоимость, ₽',
        
        # Comparison table
        'table_metric': 'Метрика',
        'table_checks_processed': 'Проверок обработано',
        'table_cost_per_check': 'Стоимость проверки, ₽',
        'table_eng_hours': 'Часы инженера на проверку',
        'table_rec_hours': 'Часы рекрутера на проверку',
        'table_tth': 'Time-to-Hire, дней',
        'table_bad_hire_rate': 'Доля ошибочных наймов, %',
        'table_manual_process': 'Ручной процесс',
        
        # UI messages
        'preset_loaded': 'Пресет загружен',
        'load_error': 'Ошибка загрузки',
        'load_preset_label': 'Загрузить пресет',
        
        # Help texts
        'help_eng_rate': 'Почасовая ставка инженера при расчёте стоимости проверки',
        'help_rec_rate': 'Почасовая ставка рекрутера',
        'help_test_duration': 'Длительность тестирования в часах (8 часов = 1 день)',
        'help_vacancy_cost': 'Стоимость задержки при закрытии позиции (упущенная выручка, потери продуктивности)',
        'help_bad_hire_manual': 'Доля неудачных наймов при ручном процессе',
        'help_bad_hire_unicheck': 'Доля неудачных наймов при использовании UniCheck',
        'help_bad_hire_cost': 'Комбо: зарплата испыт. срока, онбординг, увольнение, рекрутинг, ущерб',
        'help_fp_cost': 'Цена за приём слабого кандидата',
        'help_fn_cost': 'Цена за отказ хорошему кандидату (упущенная выгода)',
        
        # FP/FN labels
        'fp_cost_label': 'Стоимость ложного одобрения (FP), ₽',
        'fn_cost_label': 'Стоимость ложного отказа (FN), ₽',
    },
    
    'en': {
        # Main interface elements
        'page_title': 'UniCheck Effect Calculator',
        'language_selector': 'Language / Язык',
        'sidebar_title': 'Calculation Parameters',
        'preset_selector': 'Select preset',
        'load_preset': 'Load preset',
        'save_preset': 'Save current parameters',
        'preset_name': 'Preset name',
        'save_button': 'Save',
        'download_results': 'Download results',
        
        # Parameter sections
        'section_plan': 'A. Plan and Volumes',
        'section_rates': 'B. Hours and Rates',
        'section_timing': 'C. Process Timeline',
        'section_accuracy': 'D. Accuracy and Hiring Quality',
        'section_costs': 'E. Costs and ROI',
        'section_nps': 'F. NPS Effect (optional)',
        
        # Plan and volumes parameters
        'hires_per_month': 'Hires per month',
        'hires_per_month_help': 'How many people do you plan to hire monthly',
        'checks_per_hire': 'Checks per 1 hire',
        'checks_per_hire_help': 'On average, how many candidates you check per one hired',
        
        # Hours and rates
        'eng_hourly': 'Engineer rate, ₽/hour',
        'rec_hourly': 'Recruiter rate, ₽/hour',
        'eng_hours_manual': 'Engineer hours per candidate (manual)',
        'rec_hours_manual': 'Recruiter hours per candidate (manual)',
        'eng_hours_unicheck': 'Engineer hours per candidate (UniCheck)',
        'rec_hours_unicheck': 'Recruiter hours per candidate (UniCheck)',
        
        # Process timeline
        'time_to_test_start_manual': 'Days to start testing (manual)',
        'time_to_test_start_unicheck': 'Days to start testing (UniCheck)',
        'time_to_test_finish_manual': 'Days to complete testing (manual)',
        'time_to_test_finish_unicheck': 'Days to complete testing (UniCheck)',
        'vacancy_cost_per_day': 'Vacancy idle cost, ₽/day',
        
        # Accuracy
        'bad_hire_rate_manual': 'Bad hire rate (manual), %',
        'bad_hire_rate_unicheck': 'Bad hire rate (UniCheck), %',
        'cost_bad_hire': 'Bad hire cost, ₽',
        'good_candidates_share': 'Good candidates share, %',
        'fp_rate_manual': 'False Positive (manual), %',
        'fn_rate_manual': 'False Negative (manual), %',
        'fp_rate_unicheck': 'False Positive (UniCheck), %',
        'fn_rate_unicheck': 'False Negative (UniCheck), %',
        
        # Costs and ROI
        'unicheck_cost_per_check': 'UniCheck cost per check, ₽',
        'unicheck_setup_cost': 'UniCheck implementation cost, ₽',
        'discount_rate': 'Discount rate, %',
        'analysis_period': 'Analysis period, months',
        
        # NPS
        'enable_nps': 'Include NPS effect',
        'nps_improvement': 'Candidate NPS growth',
        'nps_monetary_value': 'Monetary value of NPS growth, ₽/month',
        
        # Results
        'results_title': 'Calculation Results',
        'total_savings': 'Total Savings',
        'monthly_savings': 'Monthly Savings',
        'annual_savings': 'Annual Savings',
        'roi_title': 'Return on Investment (ROI)',
        'payback_period': 'Payback Period',
        'npv': 'Net Present Value (NPV)',
        
        # Savings components
        'labor_costs': 'Labor Costs',
        'tth_costs': 'Vacancy Idle Time (TtH)',
        'accuracy_costs': 'Wrong Hire (accuracy)',
        'total_per_check': 'Total per check',
        
        # Tables
        'component': 'Component',
        'manual_cost': 'Manual, ₽',
        'unicheck_cost': 'UniCheck, ₽',
        'savings_rub': 'Savings, ₽',
        'savings_percent': 'Savings, %',
        
        # Charts
        'cost_breakdown_title': 'Cost Breakdown by Components',
        'manual': 'Manual',
        'unicheck': 'UniCheck',
        'savings': 'Savings',
        
        # Export
        'input_params': 'INPUT PARAMETERS',
        'calculation_results': 'CALCULATION RESULTS',
        
        # Disclaimer
        'disclaimer': '⚠️ **Disclaimer:** The model is approximate and may differ from actual results. All calculations are based on input parameters. It is recommended to validate assumptions with your company\'s real data.',
        
        # Sliders and controls
        'slider_mode': 'Slider Mode',
        'number_input_mode': 'Number Inputs',
        'slider_input_mode': 'Sliders',
        
        # Additional translations
        'unicheck': 'UniCheck',
        'saved_presets': 'Saved Presets',
        'detailed_accuracy_model': 'Detailed Accuracy Model (FP/FN)',
        'techscreen_errors_cost': 'Technical Screen Errors Cost',
        'comparison_subtitle': 'UniCheck vs Manual Hiring Process Comparison',
        'reset_params': 'Reset Parameters',
        'use_fpfn_analysis': 'Use FP/FN Analysis',
        'fpfn_help': 'Additionally account for false rejections and false approvals at the technical screening stage',
        'nps_enable_help': 'If enabled, NPS difference will be converted to monetary effect',
        
        # Metrics
        'labor_hours_savings': 'Labor Hours Savings',
        'engineers': 'Engineers',
        'recruiters': 'Recruiters',
        'hours_per_year': 'hours/year',
        'speed_savings': 'Speed Savings',
        'tth_days_per_year': 'days/year',
        'accuracy_savings_metric': 'Accuracy Savings',
        'weak_not_hired': 'Weak Not Hired',
        'strong_not_rejected': 'Strong Not Rejected',
        'nps_effect': 'NPS Effect',
        'total_savings_metric': 'Total Savings',
        'months': 'months',
        'payback': 'Payback',
        
        # CSV Export headers
        'csv_indicator': 'Indicator',
        'csv_value': 'Value',
        'csv_hours_rates': 'B. Hours and Rates',
        'csv_eng_rate': 'Engineer rate, ₽/hour',
        'csv_rec_rate': 'Recruiter rate, ₽/hour',
        'csv_eng_hours_manual': 'Engineer hours per candidate (manual)',
        'csv_rec_hours_manual': 'Recruiter hours per candidate (manual)',
        'csv_eng_hours_unicheck': 'Engineer hours per candidate (UniCheck)',
        'csv_rec_hours_unicheck': 'Recruiter hours per candidate (UniCheck)',
        'csv_timing': 'C. Process Timeline',
        'csv_days_to_start_manual': 'Days to test start (manual)',
        'csv_days_to_start_unicheck': 'Days to test start (UniCheck)',
        'csv_test_duration_manual': 'Test duration (manual)',
        'csv_test_duration_unicheck': 'Test duration (UniCheck)',
        'csv_vacancy_cost': 'Vacancy idle cost, ₽/day',
        'csv_accuracy': 'D. Accuracy',
        'csv_bad_hire_manual': 'Bad hire rate (manual), %',
        'csv_bad_hire_unicheck': 'Bad hire rate (UniCheck), %',
        'csv_bad_hire_cost': 'Bad hire cost, ₽',
        'csv_unicheck_cost': 'E. UniCheck Cost',
        'csv_price_per_check': 'Price per check, ₽',
        'csv_nps_manual': 'NPS (manual process)',
        'csv_results': 'CALCULATION RESULTS',
        'csv_key_metrics': 'Key Metrics',
        'csv_gross_savings': 'Gross Savings, ₽',
        'csv_platform_cost': 'Platform Cost, ₽',
        'csv_net_savings': 'Net Savings, ₽',
        'csv_tth_reduction': 'Time-to-Hire Reduction, days',
        'csv_accuracy_improvement': 'Accuracy Improvement, p.p.',
        'csv_breakdown': 'Savings Breakdown',
        'csv_labor_savings': 'Labor Hours Savings, ₽',
        'csv_speed_savings': 'Speed Savings, ₽',
        'csv_accuracy_savings': 'Accuracy Savings, ₽',
        'csv_fpfn_savings': 'FP/FN Savings, ₽',
        'csv_nps_effect': 'NPS Effect, ₽',
        'csv_per_candidate': 'Per Candidate Metrics',
        'csv_gross_per_candidate': 'Gross savings per candidate, ₽',
        'csv_platform_per_candidate': 'Platform per candidate, ₽',
        'csv_net_per_candidate': 'Net per candidate, ₽',
        'csv_per_hire': 'Per Hire Metrics',
        'csv_gross_per_hire': 'Gross savings per hire, ₽',
        'csv_platform_per_hire': 'Platform per hire, ₽',
        'csv_net_per_hire': 'Net per hire, ₽',
        
        # Chart and table labels
        'pie_chart_title': 'Gross Savings Components',
        'component_labor': 'Labor Hours',
        'component_speed': 'Speed',
        'component_accuracy': 'Accuracy',
        'component_nps': 'NPS Effect',
        'chart_savings_label': 'Savings',
        'chart_cost_label': 'Cost, ₽',
        
        # Comparison table
        'table_metric': 'Metric',
        'table_checks_processed': 'Checks Processed',
        'table_cost_per_check': 'Cost per Check, ₽',
        'table_eng_hours': 'Engineer hours per check',
        'table_rec_hours': 'Recruiter hours per check',
        'table_tth': 'Time-to-Hire, days',
        'table_bad_hire_rate': 'Bad hire rate, %',
        'table_manual_process': 'Manual Process',
        
        # UI messages
        'preset_loaded': 'Preset loaded',
        'load_error': 'Load error',
        'load_preset_label': 'Load preset',
        
        # Help texts
        'help_eng_rate': 'Hourly rate of engineer for check cost calculation',
        'help_rec_rate': 'Hourly rate of recruiter',
        'help_test_duration': 'Test duration in hours (8 hours = 1 day)',
        'help_vacancy_cost': 'Cost of vacancy delay (lost revenue, productivity losses)',
        'help_bad_hire_manual': 'Share of unsuccessful hires in manual process',
        'help_bad_hire_unicheck': 'Share of unsuccessful hires using UniCheck',
        'help_bad_hire_cost': 'Combo: probation salary, onboarding, termination, recruiting, damage',
        'help_fp_cost': 'Cost of accepting weak candidate',
        'help_fn_cost': 'Cost of rejecting good candidate (opportunity loss)',
        
        # FP/FN labels
        'fp_cost_label': 'False Positive Cost (FP), ₽',
        'fn_cost_label': 'False Negative Cost (FN), ₽',
    }
}


def get_text(key: str, lang: str = 'ru') -> str:
    """Получить переведенный текст по ключу."""
    return TRANSLATIONS.get(lang, TRANSLATIONS['ru']).get(key, key)


def get_all_texts(lang: str = 'ru') -> dict:
    """Получить все тексты для указанного языка."""
    return TRANSLATIONS.get(lang, TRANSLATIONS['ru'])