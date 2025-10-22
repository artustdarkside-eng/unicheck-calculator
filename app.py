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


# === КОНФИГУРАЦИЯ STREAMLIT ===
st.set_page_config(
    page_title="Калькулятор эффекта UniCheck",
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


def create_csv_export(params: Dict[str, Any], results: Dict[str, Any]) -> bytes:
    """Создать CSV с результатами расчёта."""
    rows = []
    
    # Раздел: Входные параметры
    rows.append(['ВХОДНЫЕ ПАРАМЕТРЫ', ''])
    rows.append(['', ''])
    rows.append(['A. План и объёмы', ''])
    rows.append(['План наймов в месяц', params['hires_per_month']])
    rows.append(['Количество проверок на 1 найм', params['checks_per_hire']])
    rows.append(['', ''])
    
    rows.append(['B. Часы и ставки', ''])
    rows.append(['Ставка инженера, ₽/час', params['eng_hourly']])
    rows.append(['Ставка рекрутера, ₽/час', params['rec_hourly']])
    rows.append(['Часы инженера на кандидата (ручной)', params['eng_hours_per_cand_manual']])
    rows.append(['Часы рекрутера на кандидата (ручной)', params['rec_hours_per_cand_manual']])
    rows.append(['Часы инженера на кандидата (UniCheck)', params['eng_hours_per_cand_unicheck']])
    rows.append(['Часы рекрутера на кандидата (UniCheck)', params['rec_hours_per_cand_unicheck']])
    rows.append(['', ''])
    
    rows.append(['C. Сроки процесса', ''])
    rows.append(['Дней до старта теста (ручной)', params['time_to_test_start_manual_days']])
    rows.append(['Дней до старта теста (UniCheck)', params['time_to_test_start_unicheck_days']])
    rows.append(['Длительность теста (ручной)', params['time_to_test_finish_manual_days']])
    rows.append(['Длительность теста (UniCheck)', params['time_to_test_finish_unicheck_days']])
    rows.append(['Стоимость незакрытой позиции, ₽/день', params['vacancy_cost_per_day']])
    rows.append(['', ''])
    
    rows.append(['D. Точность', ''])
    rows.append(['Доля ошибочных наймов (ручной), %', params['bad_hire_rate_manual_pct']])
    rows.append(['Доля ошибочных наймов (UniCheck), %', params['bad_hire_rate_unicheck_pct']])
    rows.append(['Стоимость ошибочного найма, ₽', params['cost_bad_hire']])
    rows.append(['', ''])
    
    rows.append(['E. Стоимость UniCheck', ''])
    rows.append(['Цена проверки, ₽', params['price_per_check']])
    rows.append(['', ''])
    
    rows.append(['F. NPS', ''])
    rows.append(['NPS (ручной процесс)', params['nps_manual']])
    rows.append(['NPS (UniCheck)', params['nps_unicheck']])
    rows.append(['', ''])
    
    # Раздел: Результаты расчётов
    rows.append(['РЕЗУЛЬТАТЫ РАСЧЁТОВ', ''])
    rows.append(['', ''])
    rows.append(['Ключевые метрики', ''])
    rows.append(['Валовая экономия, ₽', results['gross_savings']])
    rows.append(['Стоимость платформы, ₽', results['platform_cost']])
    rows.append(['Net-экономия, ₽', results['net_savings']])
    rows.append(['ROI', results['roi'] if results['roi'] else 'N/A'])
    rows.append(['Сокращение Time-to-Hire, дней', results['delta_tth_days']])
    rows.append(['Улучшение точности, п.п.', results['delta_accuracy_pp']])
    rows.append(['', ''])
    
    rows.append(['Разбивка экономии', ''])
    rows.append(['Экономия человеко-часов, ₽', results['labor_savings']])
    rows.append(['Экономия от ускорения, ₽', results['speed_savings']])
    rows.append(['Экономия от точности, ₽', results['accuracy_savings']])
    rows.append(['Экономия от FP/FN, ₽', results['fpfn_value']])
    rows.append(['Эффект NPS, ₽', results['nps_value']])
    rows.append(['', ''])
    
    rows.append(['Метрики на кандидата', ''])
    rows.append(['Валовая экономия на кандидата, ₽', results['gross_per_candidate']])
    rows.append(['Платформа на кандидата, ₽', results['platform_per_candidate']])
    rows.append(['Net на кандидата, ₽', results['net_per_candidate']])
    rows.append(['', ''])
    
    rows.append(['Метрики на найм', ''])
    rows.append(['Валовая экономия на найм, ₽', results['gross_per_hire']])
    rows.append(['Платформа на найм, ₽', results['platform_per_hire']])
    rows.append(['Net на найм, ₽', results['net_per_hire']])
    
    df = pd.DataFrame(rows, columns=['Показатель', 'Значение'])
    
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

st.sidebar.title("⚙️ Параметры модели")

with st.sidebar:
    # Кнопка сброса параметров
    if st.button("♻️ Сброс параметров", use_container_width=True):
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
        st.markdown("**📂 Сохраненные пресеты**")
        
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
                        st.success(f"✅ Пресет '{selected}' загружен!")
                except Exception as e:
                    st.error(f"❌ Ошибка загрузки: {str(e)}")
        
        st.selectbox(
            "Загрузить пресет",
            options=[""] + saved_presets,
            label_visibility="collapsed",
            key="load_preset_select",
            on_change=load_preset_callback
        )
        
        st.divider()
    
    # A. ПЛАН И ОБЪЁМЫ
    st.subheader("A. План и объёмы")
    
    params = st.session_state.params
    
    params['hires_per_month'] = st.number_input(
        "План наймов в месяц",
        min_value=1,
        max_value=500,
        value=params.get('hires_per_month', 20),
        step=1,
        help="Сколько человек в месяц планируется нанять"
    )
    
    params['checks_per_hire'] = st.number_input(
        "Количество проверок на 1 найм",
        min_value=1,
        max_value=20,
        value=params.get('checks_per_hire', 2),
        step=1,
        help="Сколько проверок нужно провести для одного найма"
    )
    
    # B. ЧАСЫ И СТАВКИ
    st.subheader("B. Часы и ставки")
    
    params['eng_hourly'] = st.number_input(
        "Ставка инженера, ₽/час",
        min_value=500,
        max_value=50000,
        value=params.get('eng_hourly', 4000),
        step=500,
        help="Почасовая ставка инженера при расчёте стоимости проверки"
    )
    
    params['rec_hourly'] = st.number_input(
        "Ставка рекрутера, ₽/час",
        min_value=500,
        max_value=20000,
        value=params.get('rec_hourly', 1500),
        step=100,
        help="Почасовая ставка рекрутера"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        params['eng_hours_per_cand_manual'] = st.number_input(
            "Часы инженера на кандидата (ручной)",
            min_value=0.0,
            max_value=50.0,
            value=float(params.get('eng_hours_per_cand_manual', 1.0)),
            step=0.1,
            format="%.1f"
        )
        params['eng_hours_per_cand_unicheck'] = st.number_input(
            "Часы инженера (UniCheck)",
            min_value=0.0,
            max_value=50.0,
            value=float(params.get('eng_hours_per_cand_unicheck', 0.2)),
            step=0.1,
            format="%.1f"
        )
    
    with col2:
        params['rec_hours_per_cand_manual'] = st.number_input(
            "Часы рекрутера на кандидата (ручной)",
            min_value=0.0,
            max_value=50.0,
            value=float(params.get('rec_hours_per_cand_manual', 0.5)),
            step=0.1,
            format="%.1f"
        )
        params['rec_hours_per_cand_unicheck'] = st.number_input(
            "Часы рекрутера (UniCheck)",
            min_value=0.0,
            max_value=50.0,
            value=float(params.get('rec_hours_per_cand_unicheck', 0.2)),
            step=0.1,
            format="%.1f"
        )
    
    # C. СРОКИ ПРОЦЕССА
    st.subheader("C. Сроки процесса")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Ручной процесс**")
        params['time_to_test_start_manual_days'] = st.number_input(
            "Дней до старта теста",
            min_value=1,
            max_value=30,
            value=params.get('time_to_test_start_manual_days', 3),
            key="manual_start"
        )
        params['time_to_test_finish_manual_days'] = st.number_input(
            "Длительность теста, часов",
            min_value=1,
            max_value=240,
            value=params.get('time_to_test_finish_manual_days', 48),
            key="manual_finish",
            help="Длительность тестирования в часах (8 часов = 1 день)"
        )
    
    with col2:
        st.write("**UniCheck**")
        params['time_to_test_start_unicheck_days'] = st.number_input(
            "Дней до старта теста",
            min_value=0,
            max_value=30,
            value=params.get('time_to_test_start_unicheck_days', 1),
            key="uni_start"
        )
        params['time_to_test_finish_unicheck_days'] = st.number_input(
            "Длительность теста, часов",
            min_value=0,
            max_value=240,
            value=params.get('time_to_test_finish_unicheck_days', 8),
            key="uni_finish",
            help="Длительность тестирования в часах (8 часов = 1 день)"
        )
    
    params['vacancy_cost_per_day'] = st.number_input(
        "Стоимость незакрытой позиции, ₽/день",
        min_value=1000,
        max_value=500000,
        value=params.get('vacancy_cost_per_day', 15000),
        step=1000,
        help="Стоимость задержки при закрытии позиции (упущенная выручка, потери продуктивности)"
    )
    
    # D. ТОЧНОСТЬ
    st.subheader("D. Точность и ошибки")
    
    params['bad_hire_rate_manual_pct'] = st.number_input(
        "Ошибочные наймы (ручной), %",
        min_value=0,
        max_value=50,
        value=params.get('bad_hire_rate_manual_pct', 10),
        help="Доля неудачных наймов при ручном процессе",
        key="bad_hire_manual"
    )
    st.session_state.params['bad_hire_rate_manual_pct'] = params['bad_hire_rate_manual_pct']
    
    params['bad_hire_rate_unicheck_pct'] = st.number_input(
        "Ошибочные наймы (UniCheck), %",
        min_value=0,
        max_value=50,
        value=params.get('bad_hire_rate_unicheck_pct', 7),
        help="Доля неудачных наймов при использовании UniCheck",
        key="bad_hire_unicheck"
    )
    st.session_state.params['bad_hire_rate_unicheck_pct'] = params['bad_hire_rate_unicheck_pct']
    
    params['cost_bad_hire'] = st.number_input(
        "Стоимость ошибочного найма, ₽",
        min_value=100000,
        max_value=10000000,
        value=params.get('cost_bad_hire', 1500000),
        step=100000,
        help="Комбо: зарплата испыт. срока, онбординг, увольнение, рекрутинг, ущерб",
        key="cost_bad_hire"
    )
    st.session_state.params['cost_bad_hire'] = params['cost_bad_hire']
    
    # FP/FN модель
    st.subheader("Детальная модель точности (FP/FN)")
    
    use_fpfn = st.checkbox(
        "🔬 Использовать FP/FN анализ",
        value=st.session_state.params.get('use_fpfn_model', False),
        help="Дополнительно учитывать ложные отказы и ложные одобрения на этапе техскрина"
    )
    params['use_fpfn_model'] = use_fpfn
    st.session_state.params['use_fpfn_model'] = use_fpfn
    
    if use_fpfn:
        params['good_candidates_share'] = st.number_input(
            "Доля реально сильных кандидатов, %",
            min_value=10,
            max_value=80,
            value=params.get('good_candidates_share', 30),
            key="good_candidates_share"
        )
        st.session_state.params['good_candidates_share'] = params['good_candidates_share']
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Ручной процесс**")
            params['fp_rate_manual_pct'] = st.number_input(
                "Ложные одобрения (FP), %",
                min_value=0,
                max_value=50,
                value=params.get('fp_rate_manual_pct', 12),
                key="manual_fp"
            )
            st.session_state.params['fp_rate_manual_pct'] = params['fp_rate_manual_pct']
            
            params['fn_rate_manual_pct'] = st.number_input(
                "Ложные отказы (FN), %",
                min_value=0,
                max_value=50,
                value=params.get('fn_rate_manual_pct', 15),
                key="manual_fn"
            )
            st.session_state.params['fn_rate_manual_pct'] = params['fn_rate_manual_pct']
        
        with col2:
            st.write("**UniCheck**")
            params['fp_rate_unicheck_pct'] = st.number_input(
                "Ложные одобрения (FP), %",
                min_value=0,
                max_value=50,
                value=params.get('fp_rate_unicheck_pct', 8),
                key="uni_fp"
            )
            st.session_state.params['fp_rate_unicheck_pct'] = params['fp_rate_unicheck_pct']
            
            params['fn_rate_unicheck_pct'] = st.number_input(
                "Ложные отказы (FN), %",
                min_value=0,
                max_value=50,
                value=params.get('fn_rate_unicheck_pct', 10),
                key="uni_fn"
            )
            st.session_state.params['fn_rate_unicheck_pct'] = params['fn_rate_unicheck_pct']
        
        # Цены для FP и FN
        st.write("**Стоимость ошибок техскрина**")
        col_prices = st.columns(2)
        with col_prices[0]:
            params['cost_fp'] = st.number_input(
                "Стоимость ложного одобрения (FP), ₽",
                min_value=50000,
                max_value=5000000,
                value=params.get('cost_fp', 300000),
                step=50000,
                help="Цена за приём слабого кандидата",
                key="cost_fp"
            )
            st.session_state.params['cost_fp'] = params['cost_fp']
        
        with col_prices[1]:
            params['cost_fn'] = st.number_input(
                "Стоимость ложного отказа (FN), ₽",
                min_value=50000,
                max_value=5000000,
                value=params.get('cost_fn', 150000),
                step=50000,
                help="Цена за отказ хорошему кандидату (упущенная выгода)",
                key="cost_fn"
            )
            st.session_state.params['cost_fn'] = params['cost_fn']
    else:
        # Устанавливаем дефолты, если не используется модель
        for key in ['good_candidates_share', 'fp_rate_manual_pct', 'fn_rate_manual_pct',
                    'fp_rate_unicheck_pct', 'fn_rate_unicheck_pct', 'cost_fp', 'cost_fn']:
            if key not in params:
                params[key] = get_preset('default').get(key, 0)
    
    # E. СТОИМОСТЬ UNICHECK
    st.subheader("E. Стоимость UniCheck")
    
    params['price_per_check'] = st.number_input(
        "Цена одной проверки, ₽",
        min_value=0,
        max_value=10000,
        value=params.get('price_per_check', 1500),
        step=100
    )
    
    # F. NPS
    st.subheader("F. NPS процесса")
    
    col1, col2 = st.columns(2)
    with col1:
        params['nps_manual'] = st.number_input(
            "NPS (ручной)",
            min_value=-100,
            max_value=100,
            value=params.get('nps_manual', 10)
        )
    with col2:
        params['nps_unicheck'] = st.number_input(
            "NPS (UniCheck)",
            min_value=-100,
            max_value=100,
            value=params.get('nps_unicheck', 40)
        )
    
    use_nps_money = st.checkbox(
        "💰 Переводить ΔNPS в деньги",
        value=st.session_state.params.get('use_nps_money', False),
        help="Если включено, разница NPS будет переведена в денежный эффект"
    )
    params['use_nps_money'] = use_nps_money
    st.session_state.params['use_nps_money'] = use_nps_money
    
    if use_nps_money:
        params['nps_to_value_coef'] = st.number_input(
            "Коэффициент перевода Δ NPS → ₽/найм",
            min_value=0.0,
            max_value=100000.0,
            value=float(params.get('nps_to_value_coef', 0.0)),
            step=1000.0,
            format="%.0f"
        )
    else:
        params['nps_to_value_coef'] = 0.0
    
    st.session_state.params['nps_to_value_coef'] = params['nps_to_value_coef']


# === ОСНОВНОЙ КОНТЕНТ ===

# Заголовок
st.title("📊 Калькулятор эффекта UniCheck")
st.subheader("Сравнение найма с UniCheck vs ручные проверки")

# Синхронизируем params в session_state
st.session_state.params.update(params)

# Выполняем расчёт
results = calculate_economics(**params)

# === СОЗДАЁМ ВКЛАДКИ ===

tab_main = st.container()

# === ОСНОВНОЙ КОНТЕНТ ===
st.subheader("📈 Годовой эффект от применения UniCheck")

# Главные 5 метрик
key_cols = st.columns(5)

with key_cols[0]:
    st.metric(
        "🧑‍💼 Экономия человеко-часов",
        fmt_money(results['labor_savings'])
    )

with key_cols[1]:
    st.metric(
        "⚡ Экономия от ускорения",
        fmt_money(results['speed_savings']),
        delta=f"TTH: -{results['delta_tth_days_yearly']:.0f} дней/год"
    )

with key_cols[2]:
    # Суммарная экономия от точности: базовая модель + FP/FN (если включена)
    total_accuracy_savings = results['accuracy_savings'] + results['fpfn_value']
    delta_accuracy = None
    if params['use_fpfn_model']:
        delta_accuracy = f"Не нанято слабых: {results['bad_hired_avoided_yearly']:.0f} | Не отсеяно сильных: {results['good_rejected_avoided_yearly']:.0f}"
    st.metric(
        "✅ Экономия от точности",
        fmt_money(total_accuracy_savings),
        delta=delta_accuracy
    )

with key_cols[3]:
    st.metric(
        "🌟 NPS эффект",
        fmt_money(results['nps_value']),
        delta=f"ΔNPS = {results['delta_nps']}"
    )

with key_cols[4]:
    st.metric(
        "💎 Итоговая экономия",
        fmt_money(results['net_savings']),
        delta=f"ROI: {fmt_roi(results['roi'])} | Окупаемость: {results['payback_months']:.1f} мес." if results['payback_months'] else "ROI: N/A"
    )

st.divider()

# Визуальный график распределения экономии
st.markdown("### 📊 Из чего состоит валовая экономия")

# Суммарная экономия от точности: базовая модель + FP/FN (если включена)
total_accuracy_savings = results['accuracy_savings'] + results['fpfn_value']

pie_data = {
    'Компонент': ['Человеко-часы', 'Ускорение', 'Точность', 'NPS эффект'],
    'Значение': [
        results['labor_savings'],
        results['speed_savings'],
        total_accuracy_savings,
        results['nps_value']
    ]
}

pie_df = pd.DataFrame(pie_data)

fig = px.pie(
    pie_df,
    values='Значение',
    names='Компонент',
    title="Составляющие валовой экономии",
    hole=0.3
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Таблица сравнения ключевых показателей в денежном выражении
st.markdown("### 📋 Экономический эффект на одну проверку")

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
    'Затраты на труд': table_data['labor'],
    'Простой вакансии (TtH)': table_data['tth'],
    'Ошибочный найм': table_data['accuracy'],
    'Итого на проверку': table_data['total']
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
            x=['Ручной', 'UniCheck', 'Экономия'],
            y=[manual, unicheck, savings],
            text=[fmt_money(manual), fmt_money(unicheck), fmt_money(savings)],
            textposition='auto',
            marker=dict(color=['#FF6B6B', '#4ECDC4', '#45B7D1']),
        ))
        
        fig.update_layout(
            title=f"{component_name}<br><sub>Экономия: {savings_percent:.1f}%</sub>",
            xaxis_title='',
            yaxis_title='Стоимость, ₽',
            height=350,
            showlegend=False,
            template='plotly_white',
            hovermode='x'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Таблица с полной информацией и процентом экономии
st.markdown("**Сводная таблица с процентом экономии:**")
summary_table_data = {
    'Компонент': [
        'Затраты на труд',
        'Простой вакансии (TtH)',
        'Ошибочный найм (точность)',
        'Итого на проверку'
    ],
    'Ручной, ₽': [
        fmt_money(table_data['labor'][0]),
        fmt_money(table_data['tth'][0]),
        fmt_money(table_data['accuracy'][0]),
        fmt_money(table_data['total'][0])
    ],
    'UniCheck, ₽': [
        fmt_money(table_data['labor'][1]),
        fmt_money(table_data['tth'][1]),
        fmt_money(table_data['accuracy'][1]),
        fmt_money(table_data['total'][1])
    ],
    'Экономия, ₽': [
        fmt_money(table_data['labor'][2]),
        fmt_money(table_data['tth'][2]),
        fmt_money(table_data['accuracy'][2]),
        fmt_money(table_data['total'][2])
    ],
    'Экономия, %': [
        f"{(table_data['labor'][2] / (table_data['labor'][0] + 0.01) * 100):.1f}%",
        f"{(table_data['tth'][2] / (table_data['tth'][0] + 0.01) * 100):.1f}%",
        f"{(table_data['accuracy'][2] / (table_data['accuracy'][0] + 0.01) * 100):.1f}%",
        f"{(table_data['total'][2] / (table_data['total'][0] + 0.01) * 100):.1f}%"
    ],
}

summary_df = pd.DataFrame(summary_table_data)
st.dataframe(summary_df, use_container_width=True, hide_index=True)




# === ДИСКЛЕЙМЕР ===

st.caption(
    "⚠️ **Дисклеймер:** Модель ориентировочная и может отличаться от реальных результатов. "
    "Все расчёты основаны на входных параметрах. Рекомендуется валидировать предположения "
    "на реальных данных вашей компании."
)
