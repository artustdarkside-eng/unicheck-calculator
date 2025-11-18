# 🆕 New UniCheck Calculator Features

## 🌐 Multi-language Support

The calculator now supports two languages:
- 🇷🇺 **Russian** (default)
- 🇺🇸 **English**

### How to switch language:
1. In the left sidebar, find the "Language / Язык" section
2. Select the desired language from the dropdown
3. The interface will automatically update to the selected language

## 🎛️ Slider Controls for Parameters

Added a new input mode using sliders for more convenient interaction with parameters.

### How to switch input mode:
1. In the left sidebar, find the "Slider Mode" / "Режим слайдеров" section
2. Choose between two modes:
   - **Number Inputs** / **Поля ввода** - classic mode with number input fields
   - **Sliders** / **Слайдеры** - interactive sliders for changing values

### Slider advantages:
- 🎯 Quick parameter adjustment
- 📊 Visual representation of value ranges
- 🔄 Instant result updates when sliding
- 🎮 More intuitive interface

## 🔧 Technical Details

### Translations
- All interface texts are extracted to a separate `translations.py` file
- Easy to add new languages by extending the `TRANSLATIONS` dictionary
- Translations cover all elements: headers, fields, buttons, tables, charts

### Sliders
- Automatic determination of appropriate ranges for each parameter
- Support for both integer and decimal values
- Current values preserved when switching modes

### Compatibility
- All existing features work without changes
- Saved presets are compatible with the new version
- URL parameters are still supported

## 🚀 Running

Application startup remains the same:

```bash
# From the project folder
streamlit run app.py

# Or using virtual environment
.venv/bin/python -m streamlit run app.py
```

## 🎨 Design

- Language switcher placed at the top of the left panel
- Input mode switcher located right after language
- All elements have intuitive icons (🇷🇺🇺🇸 for languages, 🎛️ for modes)
- Design remains consistent across all languages

Enjoy using the calculator! 🎉