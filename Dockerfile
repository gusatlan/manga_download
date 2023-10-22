FROM ubuntu
RUN apt update;apt install -y firefox python3 python3-pip;apt -y upgrade;apt autoclean;apt autoremove -y;apt clean;pip3 install selenium requests Pillow
RUN mkdir /tmp/downloads;addgroup --gid 1000 gustavooliveira;useradd -m -u 1000 -g 1000 gustavooliveira
COPY /brmanga/main.py /main.py
COPY /brmanga/funcutils.py /funcutils.py
VOLUME /tmp/downloads
USER gustavooliveira
CMD python3 /main.py
