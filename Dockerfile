FROM python:3.10
WORKDIR /app
COPY notes.py /app
COPY data.txt /app
RUN pip install flask
CMD ["python", "notes.py"]