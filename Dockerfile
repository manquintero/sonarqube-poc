FROM python:3-slim


RUN adduser --disabled-password --gecos "" sonar
USER sonar
WORKDIR /home/sonar

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --no-warn-script-location
COPY . .

COPY --chown=sonar:sonar entrypoint.sh /entrypoint.sh
RUN chmod 0755 /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
