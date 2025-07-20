FROM python:3.12-slim-bookworm

RUN echo "deb http://mirrors.aliyun.com/debian/ bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        supervisor \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


RUN curl -fsSL https://astral.sh/uv/install.sh -o /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /code

COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
RUN uv sync
COPY . .

EXPOSE 8000

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
