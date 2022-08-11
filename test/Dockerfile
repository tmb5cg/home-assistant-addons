FROM debian:buster

USER root
RUN apt-get update && apt-get upgrade -yq
RUN apt-get install python3 python3-pip jq nano -y

# Install chromium
# RUN apt-get update && apt-get install -y chromium
# RUN ln -s /usr/bin/chromium /usr/bin/chromium-browser

# Tucker test 

RUN apt-get update && \
    apt-get install -y gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    CHROME_VERSION=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /usr/local/bin/

# # Install chrome and dependencies
# RUN apt-get update && apt-get install -y \
#     apt-transport-https \
#     ca-certificates \
#     curl \
#   gnupg \
#     --no-install-recommends \
#     && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
#     && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
#     && apt-get update && apt-get install -y \
#     google-chrome-stable \
#     --no-install-recommends

# # chrome won't run as root
# RUN groupadd chrome && useradd -g chrome -s /bin/bash -G audio,video chrome \
#     && mkdir -p /home/chrome && chown -R chrome:chrome /home/chrome

COPY requirements.txt .
RUN pip3 install -r requirements.txt

# COPY ./coned ./coned
COPY run.py .
COPY run.sh .

CMD cd / && chmod +x /run.sh && /run.sh
