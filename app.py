"""
Streamlit приложение "Калькулятор эффекта UniCheck".

Сравнение найма с UniCheck против ручных проверок с расчётом экономического эффекта.
"""

import streamlit as st
import pandas as pd
import io
import json
import os
from typing import Dict, Any
from urllib.parse import urlencode
import plotly.express as px
import plotly.graph_objects as go

from calc import calculate_economics, calculate_single_check_economics
from formatters import fmt_money, fmt_percent, fmt_roi, fmt_days, fmt_number
from presets import get_preset, PRESETS
from translations import get_text, get_all_texts


# === ИНИЦИАЛИЗАЦИЯ ЯЗЫКА ===
if 'language' not in st.session_state:
    st.session_state.language = 'ru'

# Получение текстов для текущего языка
def t(key: str) -> str:
    return get_text(key, st.session_state.language)

# === КОНФИГУРАЦИЯ STREAMLIT ===
st.set_page_config(
    page_title=t('page_title'),
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Скрыть дефолтный меню и футер
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .main {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)


# === ФУНКЦИИ ВСПОМОГАТЕЛЬНЫЕ ===

def get_query_params() -> Dict[str, Any]:
    """Получить параметры из URL query string."""
    params = st.query_params
    result = {}
    
    # Преобразуем значения в нужные типы
    if params:
        for key, value in params.items():
            if isinstance(value, list):
                value = value[0]
            
            # Пробуем преобразовать в int
            try:
                result[key] = int(value)
            except (ValueError, TypeError):
                # Пробуем в float
                try:
                    result[key] = float(value)
                except (ValueError, TypeError):
                    # Оставляем как строка
                    if value.lower() in ('true', 'false'):
                        result[key] = value.lower() == 'true'
                    else:
                        result[key] = value
    
    return result


def update_query_params(params: Dict[str, Any]) -> None:
    """Обновить URL query string."""
    # Фильтруем None и пустые значения
    filtered = {k: v for k, v in params.items() if v is not None}
    st.query_params.update(filtered)


def create_csv_export(params: Dict[str, Any], results: Dict[str, Any], lang: str = 'ru') -> bytes:
    """Создать CSV с результатами расчёта."""
    rows = []
    
    # Раздел: Входные параметры
    rows.append([get_text('input_params', lang), ''])
    rows.append(['', ''])
    rows.append([get_text('section_plan', lang), ''])
    rows.append([get_text('hires_per_month', lang), params['hires_per_month']])
    rows.append([get_text('checks_per_hire', lang), params['checks_per_hire']])
    rows.append(['', ''])
    
    rows.append([get_text('csv_hours_rates', lang), ''])
    rows.append([get_text('csv_eng_rate', lang), params['eng_hourly']])
    rows.append([get_text('csv_rec_rate', lang), params['rec_hourly']])
    rows.append([get_text('csv_eng_hours_manual', lang), params['eng_hours_per_cand_manual']])
    rows.append([get_text('csv_rec_hours_manual', lang), params['rec_hours_per_cand_manual']])
    rows.append([get_text('csv_eng_hours_unicheck', lang), params['eng_hours_per_cand_unicheck']])
    rows.append([get_text('csv_rec_hours_unicheck', lang), params['rec_hours_per_cand_unicheck']])
    rows.append(['', ''])
    
    rows.append([get_text('csv_timing', lang), ''])
    rows.append([get_text('csv_days_to_start_manual', lang), params['time_to_test_start_manual_days']])
    rows.append([get_text('csv_days_to_start_unicheck', lang), params['time_to_test_start_unicheck_days']])
    rows.append([get_text('csv_test_duration_manual', lang), params['time_to_test_finish_manual_days']])
    rows.append([get_text('csv_test_duration_unicheck', lang), params['time_to_test_finish_unicheck_days']])
    rows.append([get_text('csv_vacancy_cost', lang), params['vacancy_cost_per_day']])
    rows.append(['', ''])
    
    rows.append([get_text('csv_accuracy', lang), ''])
    rows.append([get_text('csv_bad_hire_manual', lang), params['bad_hire_rate_manual_pct']])
    rows.append([get_text('csv_bad_hire_unicheck', lang), params['bad_hire_rate_unicheck_pct']])
    rows.append([get_text('csv_bad_hire_cost', lang), params['cost_bad_hire']])
    rows.append(['', ''])
    
    rows.append([get_text('csv_unicheck_cost', lang), ''])
    rows.append([get_text('csv_price_per_check', lang), params['price_per_check']])
    rows.append(['', ''])
    
    rows.append([get_text('section_nps', lang), ''])
    rows.append([get_text('csv_nps_manual', lang), params['nps_manual']])
    rows.append([get_text('unicheck', lang) + ' NPS', params['nps_unicheck']])
    rows.append(['', ''])
    
    # Раздел: Результаты расчётов
    rows.append([get_text('csv_results', lang), ''])
    rows.append(['', ''])
    rows.append([get_text('csv_key_metrics', lang), ''])
    rows.append([get_text('csv_gross_savings', lang), results['gross_savings']])
    rows.append([get_text('csv_platform_cost', lang), results['platform_cost']])
    rows.append([get_text('csv_net_savings', lang), results['net_savings']])
    rows.append(['ROI', results['roi'] if results['roi'] else 'N/A'])
    rows.append([get_text('csv_tth_reduction', lang), results['delta_tth_days']])
    rows.append([get_text('csv_accuracy_improvement', lang), results['delta_accuracy_pp']])
    rows.append(['', ''])
    
    rows.append([get_text('csv_breakdown', lang), ''])
    rows.append([get_text('csv_labor_savings', lang), results['labor_savings']])
    rows.append([get_text('csv_speed_savings', lang), results['speed_savings']])
    rows.append([get_text('csv_accuracy_savings', lang), results['accuracy_savings']])
    rows.append([get_text('csv_fpfn_savings', lang), results['fpfn_value']])
    rows.append([get_text('csv_nps_effect', lang), results['nps_value']])
    rows.append(['', ''])
    
    rows.append([get_text('csv_per_candidate', lang), ''])
    rows.append([get_text('csv_gross_per_candidate', lang), results['gross_per_candidate']])
    rows.append([get_text('csv_platform_per_candidate', lang), results['platform_per_candidate']])
    rows.append([get_text('csv_net_per_candidate', lang), results['net_per_candidate']])
    rows.append(['', ''])
    
    rows.append([get_text('csv_per_hire', lang), ''])
    rows.append([get_text('csv_gross_per_hire', lang), results['gross_per_hire']])
    rows.append([get_text('csv_platform_per_hire', lang), results['platform_per_hire']])
    rows.append([get_text('csv_net_per_hire', lang), results['net_per_hire']])
    
    df = pd.DataFrame(rows, columns=[get_text('csv_indicator', lang), get_text('csv_value', lang)])
    
    buffer = io.StringIO()
    df.to_csv(buffer, index=False, sep=';', encoding='utf-8-sig')
    return buffer.getvalue().encode('utf-8-sig')


def create_comparison_table(params: Dict[str, Any], results: Dict[str, Any]) -> pd.DataFrame:
    """Создать таблицу сравнения UniCheck vs Ручной процесс."""
    
    total_checks = results['total_checks']
    candidates_unicheck = results['candidates_unicheck']
    
    data = {
        'Метрика': [
            'Проверок обработано',
            'Стоимость проверки, ₽',
            'Часы инженера на проверку',
            'Часы рекрутера на проверку',
            'Time-to-Hire, дней',
            'Доля ошибочных наймов, %',
        ],
        'Ручной процесс': [
            f"{total_checks:,}",
            f"{results['manual_cost_per_check']:,.0f}",
            f"{params['eng_hours_per_cand_manual']:.1f}",
            f"{params['rec_hours_per_cand_manual']:.1f}",
            f"{results['tth_manual_days']}",
            f"{params['bad_hire_rate_manual_pct']}",
        ],
        'UniCheck': [
            f"{candidates_unicheck:,}",
            f"{results['unicheck_cost_per_check'] + params['price_per_check']:,.0f}",
            f"{params['eng_hours_per_cand_unicheck']:.1f}",
            f"{params['rec_hours_per_cand_unicheck']:.1f}",
            f"{results['tth_unicheck_days']}",
            f"{params['bad_hire_rate_unicheck_pct']}",
        ],
    }
    
    return pd.DataFrame(data)


# === ИНИЦИАЛИЗАЦИЯ СЕССИИ ===

# Инициализируем состояние session_state для параметров
if "params" not in st.session_state:
    # Первый запуск - загружаем дефолтный пресет
    st.session_state.params = get_preset('default')
    
    # Если есть query params - перезаписываем
    query_params = get_query_params()
    if query_params:
        st.session_state.params.update(query_params)


# === SIDEBAR: ПАРАМЕТРЫ ===

with st.sidebar:
    # Переключатель языка
    st.markdown("### " + t('language_selector'))
    language = st.selectbox(
        "Language",
        options=['ru', 'en'],
        format_func=lambda x: '🇷🇺 Русский' if x == 'ru' else '🇺🇸 English',
        index=0 if st.session_state.language == 'ru' else 1,
        key='language_selector',
        label_visibility='hidden'
    )
    
    if language != st.session_state.language:
        st.session_state.language = language
        st.rerun()
    
    st.divider()

st.sidebar.title("⚙️ " + t('sidebar_title'))

with st.sidebar:
    # Переключатель режима ввода
    st.markdown("### " + t('slider_mode'))
    input_mode = st.radio(
        "Input Mode",
        options=['number', 'slider'],
        format_func=lambda x: t('number_input_mode') if x == 'number' else t('slider_input_mode'),
        horizontal=True,
        key='input_mode',
        label_visibility='hidden'
    )
    
    st.divider()
    
    # Кнопка сброса параметров
    if st.button("♻️ " + t('reset_params'), use_container_width=True):
        st.session_state.params = get_preset('default')
        st.rerun()
    
    st.divider()
    
    # Загрузка сохраненных пресетов
    import os
    import json
    
    presets_dir = "saved_presets"
    saved_presets = []
    
    if os.path.exists(presets_dir):
        saved_presets = [f[:-5] for f in os.listdir(presets_dir) if f.endswith('.json')]
        saved_presets.sort()
    
    if saved_presets:
        st.markdown("**📂 " + t('saved_presets') + "**")
        
        def load_preset_callback():
            """Callback для загрузки пресета при выборе из selectbox."""
            selected = st.session_state.get("load_preset_select", "")
            if selected:
                preset_file = os.path.join(presets_dir, f"{selected}.json")
                try:
                    with open(preset_file, 'r', encoding='utf-8') as f:
                        loaded_preset = json.load(f)
                        # Полностью заменить текущие параметры загруженными
                        st.session_state.params = loaded_preset
                        st.session_state.preset_loaded = True
                        st.success(f"✅ {t('preset_loaded')} '{selected}'!")
                except Exception as e:
                    st.error(f"❌ {t('load_error')}: {str(e)}")
        
        st.selectbox(
            t('load_preset_label'),
            options=[""] + saved_presets,
            label_visibility="collapsed",
            key="load_preset_select",
            on_change=load_preset_callback
        )
        
        st.divider()
    
    # Функция для создания элементов управления
    def create_input(key, label, min_val, max_val, default_val, step=1.0, help_text="", format_str=None):
        """Создает слайдер или number_input в зависимости от режима."""
        value = params.get(key, default_val)
        
        if st.session_state.get('input_mode', 'number') == 'slider':
            if format_str == "%.1f":
                return st.slider(
                    label,
                    min_value=float(min_val),
                    max_value=float(max_val),
                    value=float(value),
                    step=float(step),
                    help=help_text,
                    key=f"slider_{key}"
                )
            else:
                return st.slider(
                    label,
                    min_value=min_val,
                    max_value=max_val,
                    value=value,
                    step=step,
                    help=help_text,
                    key=f"slider_{key}"
                )
        else:
            if format_str == "%.1f":
                return st.number_input(
                    label,
                    min_value=float(min_val),
                    max_value=float(max_val),
                    value=float(value),
                    step=float(step),
                    format=format_str,
                    help=help_text,
                    key=f"number_{key}"
                )
            else:
                return st.number_input(
                    label,
                    min_value=min_val,
                    max_value=max_val,
                    value=value,
                    step=step,
                    help=help_text,
                    key=f"number_{key}"
                )

    # A. ПЛАН И ОБЪЁМЫ
    st.subheader("A. " + t('section_plan'))
    
    params = st.session_state.params
    
    params['hires_per_month'] = create_input(
        'hires_per_month',
        t('hires_per_month'),
        1, 500, 20, 1,
        t('hires_per_month_help')
    )
    
    params['checks_per_hire'] = create_input(
        'checks_per_hire',
        t('checks_per_hire'),
        1, 20, 2, 1,
        t('checks_per_hire_help')
    )
    
    # B. ЧАСЫ И СТАВКИ
    st.subheader("B. " + t('section_rates'))
    
    params['eng_hourly'] = create_input(
        'eng_hourly',
        t('eng_hourly'),
        500, 50000, 4000, 500,
        t('help_eng_rate')
    )
    
    params['rec_hourly'] = create_input(
        'rec_hourly',
        t('rec_hourly'),
        500, 20000, 1500, 100,
        t('help_rec_rate')
    )
    
    col1, col2 = st.columns(2)
    with col1:
        params['eng_hours_per_cand_manual'] = create_input(
            'eng_hours_per_cand_manual',
            t('eng_hours_manual'),
            0.0, 50.0, 1.0, 0.1,
            "", "%.1f"
        )
        params['eng_hours_per_cand_unicheck'] = create_input(
            'eng_hours_per_cand_unicheck',
            t('eng_hours_unicheck'),
            0.0, 50.0, 0.2, 0.1,
            "", "%.1f"
        )
    
    with col2:
        params['rec_hours_per_cand_manual'] = create_input(
            'rec_hours_per_cand_manual',
            t('rec_hours_manual'),
            0.0, 50.0, 0.5, 0.1,
            "", "%.1f"
        )
        params['rec_hours_per_cand_unicheck'] = create_input(
            'rec_hours_per_cand_unicheck',
            t('rec_hours_unicheck'),
            0.0, 50.0, 0.2, 0.1,
            "", "%.1f"
        )
    
    # C. СРОКИ ПРОЦЕССА
    st.subheader("C. " + t('section_timing'))
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**" + t('manual') + "**")
        params['time_to_test_start_manual_days'] = create_input(
            'time_to_test_start_manual_days',
            t('time_to_test_start_manual'),
            1, 30, 3, 1
        )
        params['time_to_test_finish_manual_days'] = create_input(
            'time_to_test_finish_manual_days',
            t('time_to_test_finish_manual'),
            1, 240, 48, 1,
            t('help_test_duration')
        )
    
    with col2:
        st.write("**UniCheck**")
        params['time_to_test_start_unicheck_days'] = create_input(
            'time_to_test_start_unicheck_days',
            t('time_to_test_start_unicheck'),
            0, 30, 1, 1
        )
        params['time_to_test_finish_unicheck_days'] = create_input(
            'time_to_test_finish_unicheck_days',
            t('time_to_test_finish_unicheck'),
            0, 240, 8, 1,
            t('help_test_duration')
        )
    
    params['vacancy_cost_per_day'] = create_input(
        'vacancy_cost_per_day',
        t('vacancy_cost_per_day'),
        1000, 500000, 15000, 1000,
        t('help_vacancy_cost')
    )
    
    # D. ТОЧНОСТЬ
    st.subheader("D. " + t('section_accuracy'))
    
    params['bad_hire_rate_manual_pct'] = create_input(
        'bad_hire_rate_manual_pct',
        t('bad_hire_rate_manual'),
        0, 50, 10, 1,
        t('help_bad_hire_manual')
    )
    st.session_state.params['bad_hire_rate_manual_pct'] = params['bad_hire_rate_manual_pct']
    
    params['bad_hire_rate_unicheck_pct'] = create_input(
        'bad_hire_rate_unicheck_pct',
        t('bad_hire_rate_unicheck'),
        0, 50, 7, 1,
        t('help_bad_hire_unicheck')
    )
    st.session_state.params['bad_hire_rate_unicheck_pct'] = params['bad_hire_rate_unicheck_pct']
    
    params['cost_bad_hire'] = create_input(
        'cost_bad_hire',
        t('cost_bad_hire'),
        100000, 10000000, 1500000, 100000,
        t('help_bad_hire_cost')
    )
    st.session_state.params['cost_bad_hire'] = params['cost_bad_hire']
    
    # FP/FN модель
    st.subheader(t('detailed_accuracy_model'))
    
    use_fpfn = st.checkbox(
        "🔬 " + t('use_fpfn_analysis'),
        value=st.session_state.params.get('use_fpfn_model', False),
        help=t('fpfn_help')
    )
    params['use_fpfn_model'] = use_fpfn
    st.session_state.params['use_fpfn_model'] = use_fpfn
    
    if use_fpfn:
        params['good_candidates_share'] = create_input(
            'good_candidates_share',
            t('good_candidates_share'),
            10, 80, 30, 1
        )
        st.session_state.params['good_candidates_share'] = params['good_candidates_share']
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**" + t('manual') + "**")
            params['fp_rate_manual_pct'] = create_input(
                'fp_rate_manual_pct',
                t('fp_rate_manual'),
                0, 50, 12, 1
            )
            st.session_state.params['fp_rate_manual_pct'] = params['fp_rate_manual_pct']
            
            params['fn_rate_manual_pct'] = create_input(
                'fn_rate_manual_pct',
                t('fn_rate_manual'),
                0, 50, 15, 1
            )
            st.session_state.params['fn_rate_manual_pct'] = params['fn_rate_manual_pct']
        
        with col2:
            st.write("**UniCheck**")
            params['fp_rate_unicheck_pct'] = create_input(
                'fp_rate_unicheck_pct',
                t('fp_rate_unicheck'),
                0, 50, 8, 1
            )
            st.session_state.params['fp_rate_unicheck_pct'] = params['fp_rate_unicheck_pct']
            
            params['fn_rate_unicheck_pct'] = create_input(
                'fn_rate_unicheck_pct',
                t('fn_rate_unicheck'),
                0, 50, 10, 1
            )
            st.session_state.params['fn_rate_unicheck_pct'] = params['fn_rate_unicheck_pct']
        
        # Цены для FP и FN
        st.write("**" + t('techscreen_errors_cost') + "**")
        col_prices = st.columns(2)
        with col_prices[0]:
            params['cost_fp'] = create_input(
                'cost_fp',
                t('fp_cost_label'),
                50000, 5000000, 300000, 50000,
                t('help_fp_cost')
            )
            st.session_state.params['cost_fp'] = params['cost_fp']
        
        with col_prices[1]:
            params['cost_fn'] = create_input(
                'cost_fn',
                t('fn_cost_label'),
                50000, 5000000, 150000, 50000,
                t('help_fn_cost')
            )
            st.session_state.params['cost_fn'] = params['cost_fn']
    else:
        # Устанавливаем дефолты, если не используется модель
        for key in ['good_candidates_share', 'fp_rate_manual_pct', 'fn_rate_manual_pct',
                    'fp_rate_unicheck_pct', 'fn_rate_unicheck_pct', 'cost_fp', 'cost_fn']:
            if key not in params:
                params[key] = get_preset('default').get(key, 0)
    
    # E. СТОИМОСТЬ UNICHECK
    st.subheader("E. " + t('section_costs'))
    
    params['price_per_check'] = create_input(
        'price_per_check',
        t('unicheck_cost_per_check'),
        0, 10000, 1500, 100
    )
    
    # F. NPS
    st.subheader("F. " + t('section_nps'))
    
    col1, col2 = st.columns(2)
    with col1:
        params['nps_manual'] = create_input(
            'nps_manual',
            "NPS (" + t('manual') + ")",
            -100, 100, 10, 1
        )
    with col2:
        params['nps_unicheck'] = create_input(
            'nps_unicheck',
            "NPS (UniCheck)",
            -100, 100, 40, 1
        )
    
    use_nps_money = st.checkbox(
        "💰 " + t('enable_nps'),
        value=st.session_state.params.get('use_nps_money', False),
        help=t('nps_enable_help')
    )
    params['use_nps_money'] = use_nps_money
    st.session_state.params['use_nps_money'] = use_nps_money
    
    if use_nps_money:
        params['nps_to_value_coef'] = create_input(
            'nps_to_value_coef',
            t('nps_monetary_value'),
            0.0, 100000.0, 0.0, 1000.0,
            "", "%.0f"
        )
    else:
        params['nps_to_value_coef'] = 0.0
    
    st.session_state.params['nps_to_value_coef'] = params['nps_to_value_coef']


# === ОСНОВНОЙ КОНТЕНТ ===

# Заголовок
st.title("📊 " + t('page_title'))
st.subheader(t('comparison_subtitle'))

# Синхронизируем params в session_state
st.session_state.params.update(params)

# Фильтруем параметры для calculate_economics (убираем лишние ключи)
valid_keys = {
    'hires_per_month', 'checks_per_hire', 'eng_hourly', 'rec_hourly',
    'eng_hours_per_cand_manual', 'rec_hours_per_cand_manual', 
    'eng_hours_per_cand_unicheck', 'rec_hours_per_cand_unicheck',
    'time_to_test_start_manual_days', 'time_to_test_start_unicheck_days',
    'time_to_test_finish_manual_days', 'time_to_test_finish_unicheck_days',
    'vacancy_cost_per_day', 'bad_hire_rate_manual_pct', 'bad_hire_rate_unicheck_pct',
    'cost_bad_hire', 'good_candidates_share', 'fp_rate_manual_pct', 'fn_rate_manual_pct',
    'fp_rate_unicheck_pct', 'fn_rate_unicheck_pct', 'price_per_check',
    'nps_manual', 'nps_unicheck', 'nps_to_value_coef', 'use_nps_money',
    'cost_fp', 'cost_fn', 'use_fpfn_model'
}

filtered_params = {k: v for k, v in params.items() if k in valid_keys}

# Выполняем расчёт
results = calculate_economics(**filtered_params)

# === СОЗДАЁМ ВКЛАДКИ ===

tab_main = st.container()

# === ОСНОВНОЙ КОНТЕНТ ===
st.subheader("📈 " + t('annual_savings'))

# Главные 5 метрик
key_cols = st.columns(5)

with key_cols[0]:
    st.metric(
        "🧑‍💼 " + t('labor_hours_savings'),
        fmt_money(results['labor_savings'])
    )
    st.metric(
        t('engineers'),
        "",
        delta=f"{results['eng_hours_saved_yearly']:.0f} " + t('hours_per_year')
    )
    st.metric(
        t('recruiters'),
        "",
        delta=f"{results['rec_hours_saved_yearly']:.0f} " + t('hours_per_year')
    )

with key_cols[1]:
    st.metric(
        "⚡ " + t('speed_savings'),
        fmt_money(results['speed_savings']),
        delta=f"TTH: -{results['delta_tth_days_yearly']:.0f} " + t('tth_days_per_year')
    )

with key_cols[2]:
    # Суммарная экономия от точности: базовая модель + FP/FN (если включена)
    total_accuracy_savings = results['accuracy_savings'] + results['fpfn_value']
    st.metric(
        "✅ " + t('accuracy_savings_metric'),
        fmt_money(total_accuracy_savings)
    )
    if params['use_fpfn_model']:
        st.metric(
            t('weak_not_hired'),
            "",
            delta=f"{results['bad_hired_avoided_yearly']:.0f}"
        )
        st.metric(
            t('strong_not_rejected'),
            "",
            delta=f"{results['good_rejected_avoided_yearly']:.0f}"
        )

with key_cols[3]:
    st.metric(
        "🌟 " + t('nps_effect'),
        fmt_money(results['nps_value']),
        delta=f"ΔNPS = {results['delta_nps']}"
    )

with key_cols[4]:
    st.metric(
        "💎 " + t('total_savings_metric'),
        fmt_money(results['net_savings']),
        delta=f"ROI: {fmt_roi(results['roi'])} | " + t('payback') + f": {results['payback_months']:.1f} " + t('months') if results['payback_months'] else "ROI: N/A"
    )

st.divider()

# Визуальный график распределения экономии
st.markdown("### 📊 " + t('cost_breakdown_title'))

# Суммарная экономия от точности: базовая модель + FP/FN (если включена)
total_accuracy_savings = results['accuracy_savings'] + results['fpfn_value']

pie_data = {
    t('component'): [t('component_labor'), t('component_speed'), t('component_accuracy'), t('component_nps')],
    t('csv_value'): [
        results['labor_savings'],
        results['speed_savings'],
        total_accuracy_savings,
        results['nps_value']
    ]
}

pie_df = pd.DataFrame(pie_data)

fig = px.pie(
    pie_df,
    values=t('csv_value'),
    names=t('component'),
    title=t('pie_chart_title'),
    hole=0.3
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Таблица сравнения ключевых показателей в денежном выражении
st.markdown("### 📋 " + t('total_per_check'))

# Расчёт всех значений на одну проверку (динамически пересчитывается)
def calculate_table_data(results, params):
    manual_labor_cost_per_check = results['manual_cost_per_check']
    unicheck_labor_cost_per_check = results['unicheck_cost_per_check'] + params['price_per_check']
    labor_savings_per_check = manual_labor_cost_per_check - unicheck_labor_cost_per_check

    # TtH экономия на одну проверку
    # На одного найма: сокращение TtH × стоимость вакансии в день
    tth_cost_per_hire_manual = results['tth_manual_days'] * params['vacancy_cost_per_day']
    tth_cost_per_hire_unicheck = results['tth_unicheck_days'] * params['vacancy_cost_per_day']
    # На одну проверку (разделить на количество проверок на найм)
    tth_cost_per_check_manual = tth_cost_per_hire_manual / params['checks_per_hire']
    tth_cost_per_check_unicheck = tth_cost_per_hire_unicheck / params['checks_per_hire']
    tth_savings_per_check = tth_cost_per_check_manual - tth_cost_per_check_unicheck

    # Точность на одну проверку (базовая модель + FP/FN если включена)
    # На одного найма: вероятность ошибки × стоимость ошибки
    accuracy_cost_per_hire_manual = (params['bad_hire_rate_manual_pct'] / 100) * params['cost_bad_hire']
    accuracy_cost_per_hire_unicheck = (params['bad_hire_rate_unicheck_pct'] / 100) * params['cost_bad_hire']
    
    # Добавляем FP/FN компонент если модель включена
    if params['use_fpfn_model']:
        # FP/FN стоимости на один найм (пропорционально от общей экономии)
        fpfn_cost_per_hire = results['fpfn_value'] / results['total_checks'] * params['checks_per_hire']
        # Добавляем к ручному процессу, так как UniCheck исправляет эти ошибки
        accuracy_cost_per_hire_manual += fpfn_cost_per_hire
    
    # На одну проверку (разделить на количество проверок на найм)
    accuracy_cost_per_check_manual = accuracy_cost_per_hire_manual / params['checks_per_hire']
    accuracy_cost_per_check_unicheck = accuracy_cost_per_hire_unicheck / params['checks_per_hire']
    accuracy_savings_per_check = accuracy_cost_per_check_manual - accuracy_cost_per_check_unicheck

    total_savings_per_check = labor_savings_per_check + tth_savings_per_check + accuracy_savings_per_check

    # Итоговые стоимости (сумма труда + TtH + точность)
    manual_total_per_check = manual_labor_cost_per_check + tth_cost_per_check_manual + accuracy_cost_per_check_manual
    unicheck_total_per_check = unicheck_labor_cost_per_check + tth_cost_per_check_unicheck + accuracy_cost_per_check_unicheck

    return {
        'labor': (manual_labor_cost_per_check, unicheck_labor_cost_per_check, labor_savings_per_check),
        'tth': (tth_cost_per_check_manual, tth_cost_per_check_unicheck, tth_savings_per_check),
        'accuracy': (accuracy_cost_per_check_manual, accuracy_cost_per_check_unicheck, accuracy_savings_per_check),
        'total': (manual_total_per_check, unicheck_total_per_check, total_savings_per_check)
    }

table_data = calculate_table_data(results, params)

# Подготовка данных для столбчатых диаграмм
components_data = {
    t('labor_costs'): table_data['labor'],
    t('tth_costs'): table_data['tth'],
    t('accuracy_costs'): table_data['accuracy'],
    t('total_per_check'): table_data['total']
}

# Создаём 4 диаграммы в сетке 2x2
cols = st.columns(2)

for idx, (component_name, (manual, unicheck, savings)) in enumerate(components_data.items()):
    with cols[idx % 2]:
        # Расчёт процента экономии
        savings_percent = (savings / (manual + 0.01) * 100)
        
        # Создаём столбчатую диаграмму для каждого компонента
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=[t('manual'), t('unicheck'), t('savings')],
            y=[manual, unicheck, savings],
            text=[fmt_money(manual), fmt_money(unicheck), fmt_money(savings)],
            textposition='auto',
            marker=dict(color=['#FF6B6B', '#4ECDC4', '#45B7D1']),
        ))
        
        fig.update_layout(
            title=f"{component_name}<br><sub>{t('chart_savings_label')}: {savings_percent:.1f}%</sub>",
            xaxis_title='',
            yaxis_title=t('chart_cost_label'),
            height=350,
            showlegend=False,
            template='plotly_white',
            hovermode='x'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Таблица с полной информацией и процентом экономии
st.markdown("**" + t('results_title') + ":**")
summary_table_data = {
    t('component'): [
        t('labor_costs'),
        t('tth_costs'),
        t('accuracy_costs'),
        t('total_per_check')
    ],
    t('manual_cost'): [
        fmt_money(table_data['labor'][0]),
        fmt_money(table_data['tth'][0]),
        fmt_money(table_data['accuracy'][0]),
        fmt_money(table_data['total'][0])
    ],
    t('unicheck_cost'): [
        fmt_money(table_data['labor'][1]),
        fmt_money(table_data['tth'][1]),
        fmt_money(table_data['accuracy'][1]),
        fmt_money(table_data['total'][1])
    ],
    t('savings_rub'): [
        fmt_money(table_data['labor'][2]),
        fmt_money(table_data['tth'][2]),
        fmt_money(table_data['accuracy'][2]),
        fmt_money(table_data['total'][2])
    ],
    t('savings_percent'): [
        f"{(table_data['labor'][2] / (table_data['labor'][0] + 0.01) * 100):.1f}%",
        f"{(table_data['tth'][2] / (table_data['tth'][0] + 0.01) * 100):.1f}%",
        f"{(table_data['accuracy'][2] / (table_data['accuracy'][0] + 0.01) * 100):.1f}%",
        f"{(table_data['total'][2] / (table_data['total'][0] + 0.01) * 100):.1f}%"
    ],
}

summary_df = pd.DataFrame(summary_table_data)
st.dataframe(summary_df, use_container_width=True, hide_index=True)




# === ДИСКЛЕЙМЕР ===

st.caption(t('disclaimer'))
