# 簡易 pyenv & Python 環境
# docker build -f Dockerfile -t cfiken/python .
# 
FROM ubuntu:20.04

# 定数
ENV PYTHON_VERSION=3.10.5

# 時刻・言語環境設定に必要最小限の apt
# Add ASIA/TOKYO time zone
RUN sed -i.bak -e "s%http://archive.ubuntu.com/ubuntu/%http://ftp.jaist.ac.jp/pub/Linux/ubuntu/%g" /etc/apt/sources.list
ENV TZ=Asia/Tokyo
RUN echo $TZ
RUN echo $TZ > /etc/timezone \
  && ln -s /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
RUN apt-get update && apt-get install -y \
    locales \
    tzdata \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Set environment to japanese
RUN locale-gen ja_JP.UTF-8
ENV LANG=ja_JP.UTF-8
ENV LANGUAGE=ja_JP:ja
ENV LC_ALL=ja_JP.UTF-8

# user
ENV USER=ubuntu GROUP=ubuntu
ENV HOME=/home/$USER
ENV PATH=/home/ubuntu/.local/bin:$PATH
ENV PYENV_ROOT=$HOME/.pyenv
ENV PATH=$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH
ENV PATH=$HOME/.local/bin:$PATH

# volume マウント時にファイルを扱えるよう、ホストマシンのユーザーと uid, gid を合わせる
RUN groupadd -g 1000 -r $GROUP \
  && useradd --create-home --no-log-init -r -s /bin/zsh -u 1000 -g $GROUP $USER

# apt-packages
RUN apt-get update && apt-get install -y \
    make \
    build-essential \
    zsh \
    wget \
    curl \
    git \
    zip \
    tk-dev \
    libbz2-dev \
    libcupti-dev \
    libffi-dev \
    liblzma-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libgl1-mesa-dev \
    pkg-config \
    zlib1g-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER $USER
WORKDIR $HOME

# ユーザー設定全般
RUN mkdir -p ~/.ssh \
  && ssh-keyscan github.com >> .ssh/known_hosts

# Python
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
RUN git clone https://github.com/pyenv/pyenv.git .pyenv \
  && git clone https://github.com/pyenv/pyenv-virtualenv.git .pyenv/plugins/pyenv-virtualenv 
RUN eval "$(pyenv init -)" \
  && pyenv install $PYTHON_VERSION \
  && pyenv global $PYTHON_VERSION \
  && pyenv rehash \
  && curl -sSL https://install.python-poetry.org | python - \
  && rm -rf $HOME/.cache

WORKDIR /app

CMD python --version
