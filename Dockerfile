FROM python

WORKDIR /usr/src/app/

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]
