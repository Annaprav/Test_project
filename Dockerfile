FROM python:3.11

WORKDIR /app

RUN git clone https://github.com/Annaprav/Test_project.git .

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "проверка_гипотез.py", "--server.port=8501", "--server.address=0.0.0.0"]
