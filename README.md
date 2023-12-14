**README.md**

# Анализ данных о больничных днях 
## Описание проекта
Этот репозиторий содержит код на языке Python для анализа данных о больничных днях. Проект включает в себя веб-приложение, созданное с использованием библиотеки Streamlit, которое позволяет загружать данные о больничных днях и проводить статистический анализ гипотез.

## Структура репозитория
- `Dockerfile`: Файл для создания Docker-образа, если требуется.
- `README.md`: Инструкции и описание проекта (вы читаете его прямо сейчас).
- `requirements.txt`: Файл с перечнем зависимостей, необходимых для запуска приложения.
- `М.Тех_Данные_к_ТЗ_DS.csv`: Пример CSV-файла с данными о больничных днях.
- `М.Тех_ТЗ_DS.pdf`: Техническое задание к проекту в формате PDF.
- `проверка_гипотез.py`: Код для веб-приложения на основе библиотеки Streamlit.
- `проверка_гипотез.ipynb`: Пример использования кода в виде Jupyter Notebook.

## Использование
1. Установите необходимые библиотеки и запустите веб-приложение с помощью команд:
   ```bash
   pip install -r requirements.txt
   streamlit run проверка_гипотез.py
   ```

2. Или запустите с помощью docker:
   ```bash
   docker build -t streamlit .
   docker run -p 8501:8501 streamlit
   ```
   Тогда веб-приложение будет доступно по http://localhost:8501
   
   Остановка всех докеров:
   ```bash
   docker stop $(docker ps -q)
   ```


4. Веб-приложение позволяет загрузить данные о больничных днях в формате CSV или ввести их вручную. После загрузки данных, вы сможете провести статистическией тест для проверки двух гипотез:
   - Мужчины пропускают в течение года более 2 рабочих дней по болезни значимо чаще женщин.
   - Работники старше 35 лет пропускают в течение года более 2 рабочих дней по болезни значимо чаще своих более молодых коллег.

5. Результаты анализа, включая графики распределения данных и статистики тестов, будут отображены в интерфейсе приложения.

## Примечание
- Пример данных (`М.Тех_Данные_к_ТЗ_DS.csv`) предоставлен в репозитории для демонстрации функциональности.
- Ссылка на дашборд: https://testproject-5jgfjjddlbvrb7vjrggne3.streamlit.app.
