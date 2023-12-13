import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

def distplot_stat(x,y, title_x, title_y):
    # Визуализация графиков
    st.subheader('Графики распределений')
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

    sns.distplot(x, kde=True, color='skyblue', ax=axes[0])
    axes[0].set_title(f'Распределение выборки - {title_x}')
    axes[0].set_xlabel('Values')
    axes[0].set_ylabel('Frequency  ')

    sns.distplot(y, kde=True, color='salmon', ax=axes[1])
    axes[1].set_title(f'Распределение выборки - {title_y}')
    axes[1].set_xlabel('Values')
    axes[1].set_ylabel('Frequency')

    plt.tight_layout()
    st.pyplot(fig)  

    # Описательная статистика
    st.subheader('Описательная статистика выборок')
    st.write(f'{title_x}\n', x.describe())
    st.write(f'{title_y}\n', y.describe()) 

def U_test(x,y,alpha):
    # Проведение U-теста
    st.subheader('Проведение U-теста')
    statistic, p_value = mannwhitneyu(x,y)
    st.write(f"Статистика U: {statistic}")
    st.write(f"P-значение: {p_value}")

    # Оценка статистической значимости
    st.write(f"Уровень значимости: {alpha}")
    st.subheader('Оценка статистической значимости')
    if p_value < alpha:
        st.write("Различие является статистически значимым - гипотеза принимается.")
    else:
        st.write("Нет статистически значимого различия между выборками - гипотеза отвергается.")


data = None

# Выбор между загрузкой файла и вводом вручную
choice = st.radio("Выбор предоставления данных:", ("Загрузка файла .csv", "Ввод вручную"))

# Если выбрана загрузка файла
if choice == "Загрузка файла .csv":
    st.write("Формат данных:Количество больничных дней, Возраст, Пол")
    uploaded_file = st.file_uploader("Загрузиет csv файл", type="csv")

    # Если файл загружен, загрузить данные из файла
    if uploaded_file is not None:
            data = pd.read_csv(uploaded_file, encoding='cp1251',sep = '\,')

            #Преобразование данных - удаление "
            data.columns = data.columns.str.replace('\"','')
            data= data.applymap(lambda x: str(x).replace('\"', ''))

            st.subheader("Данные загруженные из файла:")
            st.write(data)
    else:
        st.info("Пожалуйста загрузите файл.")

# Если выбран ввод вручную
elif choice == "Ввод вручную":
    # Ввод количества строк таблицы
    num_rows = st.number_input("Введите количесвто строк", min_value=1, value=5, step=1)    
    # Создание пустого DataFrame
    data = pd.DataFrame(columns=["Количество больничных дней", "Возраст", "Пол"])
    
    # Создание виджета для ввода данных
    for i in range(num_rows):
        st.write(f"Введите данные для строки {i + 1}:")

        # Использование уникальных ключей для каждого виджета
        sickness_days = st.number_input(f"Количество больничных дней {i + 1}", min_value=1)
        age = st.number_input(f"Возраст {i + 1}", min_value=18, max_value = 90)
        gender = st.selectbox(f"Пол {i + 1}", ["М", "Ж"])
        
        # Добавление данных в DataFrame
        new_row = pd.Series({"Количество больничных дней": sickness_days, "Возраст": age, "Пол": gender})
        data = pd.concat([data, new_row.to_frame().T], ignore_index=True)

    st.subheader("Данные введенные вручную:")
    st.write(data)


# Если данные были загружены, продолжить выполнение кода
if  (st.button("Продолжить работу")) and (data is not None):
    try:

        #Преобразование типа данных
        data['Количество больничных дней'] = data['Количество больничных дней'].astype('int')
        data['Возраст'] = data['Возраст'].astype('int')

        st.write("Проверка гипотез начинается со сравнения распределний выборок и описательных статистик.Уже по ним можно сделать вывод, однако подтвердив стат. тестом.")
        st.write("Для обоих гипотез будет использовн U-критерий Манна-Уитни.")
        st.write("Почемy именно он ?")
        st.write("U-тест является непараметрическим методом, что делает его менее чувствительным к форме распределения данных. Так же U-тест подходит для небольших и больших выборок.")

        st.subheader('Гипотеза 1')
        st.write(" Мужчины пропускают в течение года более 2 рабочих дней (work_days) по болезни значимо чаще женщин.")

        # Выборки больничных дней для мужчин и женщин
        men = data[(data['Пол'] == 'М') & (data['Количество больничных дней'] > 2)]['Количество больничных дней']
        women = data[(data['Пол'] == 'Ж') & (data['Количество больничных дней'] > 2)]['Количество больничных дней']

        # Проверка наличия данных в выборках перед проведением теста
        if not men.empty and not women.empty:
            # Визуализация графиков и описательной статисики 
            distplot_stat(x=men,y=women,title_x='Мужчины',title_y='Женщины')
            # Проведение U-теста
            U_test(x=men,y=women,alpha=0.05)

        else:
            st.error(f"Выборки доллжны быть ненулевого размера.")

        st.subheader('Гипотеза 2')
        st.write("Работники старше 35 лет (age) пропускают в течение года более 2 рабочих дней (work_days) по болезни значимо чаще своих более молодых коллег.")

        # Выборки больничных дней для старших (35+) и младших  (35-) сотрудников
        older = data[(data['Возраст'] > 35) & (data['Количество больничных дней'] > 2)]['Количество больничных дней']
        younger = data[(data['Возраст'] <= 35) & (data['Количество больничных дней'] > 2)]['Количество больничных дней']

        # Проверка наличия данных в выборках перед проведением теста
        if not older.empty and not younger.empty:
            # Визуализация графиков и описательной статисики 
            distplot_stat(x=older,y=younger,title_x='35+',title_y='35-')
            # Проведение U-теста
            U_test(x=older,y=younger,alpha=0.05)
        else:
            st.error(f"Выборки доллжны быть ненулевого размера.")

    except Exception as e:
        st.warning("Что-то пошло не так")
        st.warning("Возможно данные предоставлены в неправильном формате.")
        st.error(f"Ошибка: {str(e)}")
