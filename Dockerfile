FROM python

WORKDIR /usr/src/app/

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["python3", "app.py"]
