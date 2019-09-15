FROM python:3.6

ADD code /code
RUN pip install -r /code/pip_requirements.txt

WORKDIR /code
ENV PYTHONPATH '/code'

CMD ["python", "/code/exporter.py"]
