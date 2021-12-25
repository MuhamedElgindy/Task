FROM python:"3.6"

EXPOSE 5000

WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY . /app
RUN pip install -r requirements.txt

CMD python app.py


