FROM devtestdemisto/python3:3.9.8.24399-0317a969c8671c901d5443f8c015d240
RUN mkdir -p /devwork/
WORKDIR /devwork
RUN update-ca-certificates
COPY . .
RUN chown -R :4000 /devwork
RUN chmod -R 775 /devwork
