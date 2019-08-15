FROM mikestrenk/pydev_img:latest

COPY requirements.txt ./

RUN pip install -r requirements.txt

WORKDIR /usr/src/mailroom

COPY . /usr/src/mailroom

CMD ["zsh"]