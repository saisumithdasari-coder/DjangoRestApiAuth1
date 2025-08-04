FROM python:3.6-alpine
WORKDIR /frontend
COPY requirements.txt /frontend
COPY app.py /frontend
COPY templates /frontend/templates
COPY utils.py /frontend
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["python"]
CMD ["app.py"]