FROM ubuntu:22.04

RUN apt update && \
    apt install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    git \
    curl \
    fish \
    vim \
    wget \
    tmux \
    && apt clean \
    && rm -rf /var/lib/apt/lists/* \


WORKDIR /root/ctf

RUN apt install python3-dev build-essential

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN chsh -s /bin/fish

RUN curl https://git.io/fisher --create-dirs -sLo ~/.config/fish/functions/fisher.fish
RUN fish -c "fisher install oh-my-fish/theme-bobthefish"

RUN mkdir /root/cmd \
    && cd /root/cmd \
    && git clone https://github.com/pwndbg/pwndbg \
    && cd pwndbg \
    && ./setup.sh

RUN cd /root/cmd \
    && wget https://github.com/0vercl0k/rp/releases/download/v1/rp-lin-x64 \
    && chmod +x rp-lin-x64 \
    && mv rp-lin-x64 /bin/rp++

RUN apt install -y gcc ruby-dev \
    && gem install seccomp-tools

RUN cd /root/cmd \
    && wget https://github.com/io12/pwninit/releases/download/3.3.1/pwninit \
    && chmod +x pwninit \
    && mv ./pwninit /bin/pwninit

RUN cd /root/cmd \
    && wget http://nixos.org/releases/patchelf/patchelf-0.8/patchelf-0.8.tar.bz2 \
    && tar xfa patchelf-0.8.tar.bz2 \
    && cd patchelf-0.8 \
    && ./configure --prefix=/usr/local \
    && make \
    && make install

RUN chmod -R 777 /root

COPY ./tools/tmux-conf.txt /root/.tmux.conf

CMD ["fish"]
