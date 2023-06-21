# * @author        Yasir Aris M <yasiramunandar@gmail.com>
# * @date          2022-12-01 09:12:27
# * @projectName   MissKatyPyro
# * Copyright ©YasirPedia All rights reserved

# Base Docker Using Ubuntu 23.04 and Python 3.11
FROM yasirarism/misskaty-docker:latest

# Set Hostname
ENV HOSTNAME misskaty
# Copy Files
COPY . .
# Set venv
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
# Install modules
RUN pip3 install -r requirements.txt
# Set CMD Bot
CMD ["bash", "start.sh"]
