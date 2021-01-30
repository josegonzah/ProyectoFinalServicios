FROM alpine
RUN  apk add python3
COPY /store.py/
COPY /udp_liquor/
COPY /bank.py/
COPY /bank_udp.py/
COPY /pro.py/
CMD ["python3", "pro.py", 172.17.0.2]

