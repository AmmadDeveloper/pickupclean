FROM python:3.6.12
RUN mkdir -p /asad
RUN cd /asad
RUN git clone https://github.com/gcucurull/visual-compatibility.git
RUN cd ./visual-compatibility
RUN pip install -r requirements.txt
COPY polyvore-images.tar.gz /asad/visual-compatibility/data/polyvore/
COPY polyvore.tar.gz /asad/visual-compatibility/data/polyvore/
RUN ./data/get_polyvore.sh
RUN ./data/polyvore/process_polyvore.sh
RUN python train.py -d polyvore
RUN python test_fitb.py -lf ./model -k 5




COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/NSeconds
COPY requirements.txt /opt/app/
COPY .pip_cache /opt/app/pip_cache/
COPY . /opt/app/NSeconds/
WORKDIR /opt/app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache
RUN chown -R www-data:www-data /opt/app
COPY start_server.sh /opt/app/
RUN apt update;apt -y install libgl1-mesa-glx
# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/opt/app/start_server.sh"]