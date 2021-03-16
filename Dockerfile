FROM Python:3.9.0
RUN mkdir /app
COPY requirements.txt /app/
RUN python -m pip install -r /app/requirements.txt
COPY app.py /app/
COPY database.py /app/
COPY image_processing.py /app/
COPY auth.py /app/
ADD media /app/media
WORKDIR /app
ENTRYPOINT ["python", "app.py"]