# hadolint global ignore=DL3003,DL4006,SC2035,SC2038,SC2046,SC2086
FROM debian:bullseye-slim AS base
ARG BUILD_CPUS=8
RUN set -ex \
    && (for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done) \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get update && apt-get -y --quiet --allow-remove-essential upgrade \
    && apt-get install -y --quiet --no-install-recommends \
    # base dependencies
    python-is-python3 autoconf automake build-essential ca-certificates cmake \
    curl default-libmysqlclient-dev default-mysql-client dnsutils erlang-dev \
    g++ gcc gdb git gnupg2 gperf haveged htop libavcodec-dev libavfilter-dev \
    libavformat-dev libboost-all-dev libcurl4-openssl-dev libedit-dev \
    libevent-dev libgoogle-perftools-dev libhiredis-dev libip4tc-dev \
    libip6tc-dev libiptc-dev libjpeg-dev libjson-glib-dev libldns-dev \
    liblua5.2-dev liblz4-tool libmp3lame-dev libmpg123-dev libopus-dev \
    libopusfile-dev libpcap-dev libpcre3-dev libpq-dev libre2-dev \
    libshout3-dev libsndfile-dev libspandsp-dev libspeex-dev libspeexdsp-dev \
    libsqlite3-dev libssl-dev libswresample-dev libswscale-dev \
    libtcmalloc-minimal4 libtiff-dev libtool libtool-bin libxmlrpc-core-c3-dev \
    libxtables-dev libz-dev lsb-release lsof make markdown php-dev pkg-config \
    python3-dev redis-tools telnet unixodbc-dev wget yasm zlib1g-dev libdb-dev \
    libncurses5-dev libexpat1-dev libgdbm-dev bison libtpl-dev libtiff5-dev \
    uuid-dev nasm libogg-dev libavresample-dev libsndfile1-dev libflac-dev \
    libvorbis-dev apt-transport-https libatomic1 libfftw3-dev libfltk1.3-dev \
    libsnmp-dev libtiff-tools libuv1-dev libxml2-dev netpbm sox
RUN set -ex \
    && git config --global http.postBuffer 524288000  \
    && git config --global https.postBuffer 524288000 \
    && git config --global advice.detachedHead false \
    && git config --global pull.rebase true
WORKDIR /usr/local/src
COPY ./build/packages/ ./
RUN set -ex \
    && (for f in $(ls -1 *.deb | sort); do dpkg -i $f; done) \
    && apt-get install -y --quiet --no-install-recommends -f \
    && rm -Rf *.deb

FROM base AS grpc
WORKDIR /usr/local/src
RUN git clone --depth 1 --branch v1.57.0 https://github.com/grpc/grpc && cd grpc \
    && git submodule update --init --recursive
RUN cd grpc \
    && mkdir -p cmake/build \
    && cd cmake/build \
    && cmake -DBUILD_SHARED_LIBS=ON -DgRPC_SSL_PROVIDER=package -DBUILD_SHARED_LIBS=ON -DCMAKE_BUILD_TYPE=RelWithDebInfo ../.. \
    && make -j ${BUILD_CPUS} \
    && make install
RUN ldconfig /usr/local/lib

FROM grpc AS grpc-googleapis
WORKDIR /usr/local/src
RUN git clone https://github.com/googleapis/googleapis && cd googleapis && git checkout d81d0b9e6993d6ab425dff4d7c3d05fb2e59fa57 \
    && LANGUAGE=cpp make -j ${BUILD_CPUS}
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}

FROM grpc-googleapis AS nuance-asr-grpc-api
WORKDIR /usr/local/src
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
RUN git clone --depth 1 --branch main https://github.com/drachtio/nuance-asr-grpc-api.git \
    && cd nuance-asr-grpc-api \
    && LANGUAGE=cpp make

FROM grpc-googleapis AS riva-asr-grpc-api
WORKDIR /usr/local/src
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
RUN git clone --depth 1 --branch main https://github.com/drachtio/riva-asr-grpc-api.git \
    && cd riva-asr-grpc-api \
    && LANGUAGE=cpp make

FROM grpc-googleapis AS soniox-asr-grpc-api
WORKDIR /usr/local/src
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
RUN git clone --depth 1 --branch main https://github.com/drachtio/soniox-asr-grpc-api.git \
    && cd soniox-asr-grpc-api \
    && LANGUAGE=cpp make

FROM grpc-googleapis AS cobalt-asr-grpc-api
WORKDIR /usr/local/src
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
RUN git clone --depth 1 --branch main https://github.com/drachtio/cobalt-asr-grpc-api.git \
    && cd cobalt-asr-grpc-api \
    && LANGUAGE=cpp make

FROM base AS websockets
WORKDIR /usr/local/src
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
RUN git clone --depth 1 --branch v4.3.3 https://github.com/warmcat/libwebsockets.git \
    && cd /usr/local/src/libwebsockets \
    && mkdir -p build && cd build && cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo && make && make install

FROM base AS speechsdk
COPY ./build/packages/SpeechSDK-Linux-1.37.0.tar.gz /tmp/
WORKDIR /tmp
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
RUN tar xvfz SpeechSDK-Linux-1.37.0.tar.gz \
    && cd SpeechSDK-Linux-1.37.0 \
    && cp -r include /usr/local/include/MicrosoftSpeechSDK \
    && cp -r lib/ /usr/local/lib/MicrosoftSpeechSDK \
    && cp /usr/local/lib/MicrosoftSpeechSDK/x64/libMicrosoft.*.so /usr/local/lib/ \
    && ls -lrt /usr/local/lib/

FROM base AS freeswitch-modules
WORKDIR /usr/local/src
RUN git clone --depth 1 https://github.com/jambonz/freeswitch-modules.git -b 1.2.11 

FROM base AS spandsp
WORKDIR /usr/local/src
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
RUN git clone https://github.com/freeswitch/spandsp.git && cd spandsp && git checkout 0d2e6ac \
    && ./bootstrap.sh && ./configure && make -j ${BUILD_CPUS} && make install

FROM base AS sofia-sip
WORKDIR /usr/local/src
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
RUN git clone --depth 1 --branch master https://github.com/freeswitch/sofia-sip.git \
    && cd sofia-sip \
    && ./bootstrap.sh && ./configure && make -j ${BUILD_CPUS} && make install

FROM base AS libfvad
WORKDIR /usr/local/src
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
RUN git clone --depth 1 https://github.com/dpirch/libfvad.git \
    && cd libfvad \
    && autoreconf -i && ./configure && make -j ${BUILD_CPUS} && make install

FROM base AS aws-sdk-cpp
WORKDIR /usr/local/src
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
RUN git clone --depth 1 --branch 1.11.283 https://github.com/aws/aws-sdk-cpp.git \
    && cd aws-sdk-cpp \
    && git submodule update --init --recursive
RUN cd /usr/local/src/aws-sdk-cpp \
    && mkdir -p build && cd build \
    && cmake .. -DBUILD_ONLY="lexv2-runtime;transcribestreaming" -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBUILD_SHARED_LIBS=ON -DCMAKE_CXX_FLAGS="-Wno-unused-parameter -Wno-error=nonnull -Wno-error=deprecated-declarations -Wno-error=uninitialized -Wno-error=maybe-uninitialized" \
    && make -j ${BUILD_CPUS} && make install \
    && mkdir -p /usr/local/lib/pkgconfig \
    && find /usr/local/src/aws-sdk-cpp/ -type f -name "*.pc" | xargs cp -t /usr/local/lib/pkgconfig/

FROM base AS aws-c-common
WORKDIR /usr/local/src
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
RUN git clone --depth 1 https://github.com/awslabs/aws-c-common.git \
    && cd aws-c-common \
    && mkdir -p build && cd build \
    && cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBUILD_SHARED_LIBS=OFF -DCMAKE_CXX_FLAGS="-Wno-unused-parameter" \
    && make -j ${BUILD_CPUS} && make install

FROM base AS libks
WORKDIR /usr/local/src
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
RUN set -ex \
    && git clone https://github.com/signalwire/libks.git \
    && cd libks \
    && cmake . -DWITH_LIBBACKTRACE=1 -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=/usr/local \
    && make \
    && make install

FROM base AS freeswitch-sounds
WORKDIR /defaults/sounds
ENV BASE_FS_SOUND=http://files.freeswitch.org/releases/sounds
ENV BITRATES="8 16 32 48"
ENV IFS=" "
RUN set -ex \
    && for BITRATE in $BITRATES; do \
    wget -q "${BASE_FS_SOUND}/freeswitch-sounds-music-${BITRATE}000-1.0.8.tar.gz"; \
    wget -q "${BASE_FS_SOUND}/freeswitch-sounds-en-us-callie-${BITRATE}000-1.0.11.tar.gz"; \
    done \
    && for f in $(ls -1 *.tar.gz); do tar -xzf $f; done \
    && rm -Rf *.tar.gz \
    && cd /defaults/ \
    && chown -R 1000:1000 /defaults/sounds/ \
    && tar -czf sounds.tar.gz sounds \
    && rm -Rf sounds

FROM base AS freeswitch
COPY --from=grpc /usr/local/include/ /usr/local/include/
COPY --from=grpc /usr/local/lib/ /usr/local/lib/
COPY --from=aws-c-common /usr/local/include/ /usr/local/include/
COPY --from=aws-c-common /usr/local/lib/ /usr/local/lib/
COPY --from=aws-sdk-cpp /usr/local/include/ /usr/local/include/
COPY --from=aws-sdk-cpp /usr/local/lib/ /usr/local/lib/
COPY --from=libfvad /usr/local/include/ /usr/local/include/
COPY --from=libfvad /usr/local/lib/ /usr/local/lib/
COPY --from=libks /usr/local/include/ /usr/local/include/
COPY --from=libks /usr/local/lib/ /usr/local/lib/
COPY --from=libks /usr/local/include/libks2/ /usr/local/include/libks2/
COPY --from=sofia-sip /usr/local/bin/ /usr/local/bin/
COPY --from=sofia-sip /usr/local/include/ /usr/local/include/
COPY --from=sofia-sip /usr/local/lib/ /usr/local/lib/
COPY --from=sofia-sip /usr/local/share/sofia-sip/ /usr/local/share/sofia-sip/
COPY --from=spandsp /usr/local/include/ /usr/local/include/
COPY --from=spandsp /usr/local/lib/ /usr/local/lib/
COPY --from=speechsdk /usr/local/include/ /usr/local/include/
COPY --from=speechsdk /usr/local/lib/ /usr/local/lib/
COPY --from=websockets /usr/local/include/ /usr/local/include/
COPY --from=websockets /usr/local/lib/ /usr/local/lib/
WORKDIR /usr/local/src
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
RUN git clone --depth 1 --branch v1.10.11 https://github.com/signalwire/freeswitch.git
COPY --from=freeswitch-modules /usr/local/src/freeswitch-modules/ /usr/local/src/freeswitch/src/mod/applications/
COPY --from=nuance-asr-grpc-api /usr/local/src/nuance-asr-grpc-api /usr/local/src/freeswitch/libs/nuance-asr-grpc-api
COPY --from=riva-asr-grpc-api /usr/local/src/riva-asr-grpc-api /usr/local/src/freeswitch/libs/riva-asr-grpc-api
COPY --from=soniox-asr-grpc-api /usr/local/src/soniox-asr-grpc-api /usr/local/src/freeswitch/libs/soniox-asr-grpc-api
COPY --from=cobalt-asr-grpc-api /usr/local/src/cobalt-asr-grpc-api /usr/local/src/freeswitch/libs/cobalt-asr-grpc-api
COPY --from=grpc-googleapis /usr/local/src/googleapis /usr/local/src/freeswitch/libs/googleapis
COPY --from=freeswitch-sounds --chown=1000:1000 /defaults/ /defaults/
COPY ./build/changes/compile/ /tmp/changes/compile/
COPY ./build/patches/compile/ /tmp/patches/compile/
COPY ./build/scripts/ /tmp/scripts/
RUN set -ex \
    # patches
    && sed -i '/#ifndef cJSON_AS4CPP__h/i #ifndef cJSON__h\n#define cJSON__h' /usr/local/include/aws/core/external/cjson/cJSON.h \
    && echo '#endif' >> /usr/local/include/aws/core/external/cjson/cJSON.h \
    && python3 /tmp/scripts/apply_patches.py --target /usr/local/src/freeswitch --type compile \
    # compilation
    && cd /usr/local/src/freeswitch \
    && ./bootstrap.sh -j \
    && ./configure --enable-tcmalloc=yes --with-lws=yes --with-extra=yes --with-aws=yes \
    && make -j $(nproc)\
    && make install

# initial config
RUN set -ex \
    && cp -frv /usr/local/src/freeswitch/conf/vanilla/autoload_configs/modules.conf.xml /usr/local/freeswitch/conf/autoload_configs \
    && cp -frv /usr/local/src/freeswitch/conf/vanilla/dialplan /usr/local/freeswitch/conf/ \
    && cp -frv /usr/local/src/freeswitch/conf/vanilla/sip_profiles /usr/local/freeswitch/conf/ \
    && chmod -R 770 /usr/local/freeswitch/ /defaults/ \
    && chmod -R 750 /usr/local/freeswitch/bin/* \
    && cp -fr /usr/local/freeswitch/conf /defaults/ \
    && rm -Rf /usr/local/freeswitch/conf/* \
    && chown -R 1000:1000 /usr/local/freeswitch/ /defaults/

FROM debian:bullseye-slim AS final
COPY --from=freeswitch /usr/lib/ /usr/lib/
COPY --from=freeswitch /usr/local/bin/ /usr/local/bin/
COPY --from=freeswitch /usr/local/lib/ /usr/local/lib/
COPY --from=freeswitch --chown=1000:1000 /usr/local/freeswitch/ /usr/local/freeswitch/
COPY --from=freeswitch --chown=1000:1000 /defaults/ /defaults/

WORKDIR /usr/local/freeswitch
ENV KILL_EPMD=1
ENV PATH="/usr/local/freeswitch/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH}"

# runtime dependencies
RUN set -ex \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get update \
    && apt-get install -y --quiet --no-install-recommends \
    python-is-python3 autoconf automake build-essential ca-certificates cmake \
    curl libsqlite3-0 libcurl4 libpcre3 libspeex1 libspeexdsp1 \
    libedit2 libtiff5 libopus0 libsndfile1 libshout3 lua5.2 lua5.2-dev \
    sqlite3 libfreetype6 libedit2 libsndfile1 net-tools unixodbc erlang-base \
    libnode72 nodejs \
    procps psmisc libtpl-dev \
    && ldconfig \
    && rm -rf /var/lib/apt/lists/*

# user/group
RUN set -ex \
    && adduser --gecos "FreeSWITCH" \
    --system --uid 1000 --group --disabled-password \
    --home /usr/local/freeswitch freeswitch

COPY ./entrypoint.sh .
COPY ./build/changes/conf/ /tmp/changes/conf/
COPY ./build/patches/conf/ /tmp/patches/conf/
COPY ./build/scripts/ /tmp/scripts/
RUN set -ex \
    && chmod +x entrypoint.sh \
    && python3 /tmp/scripts/apply_patches.py --target /defaults/conf --type conf \
    && chown -R 1000:1000 /defaults/ \
    && rm -Rf /tmp/changes /tmp/patches /tmp/scripts

# volumes for persistent data
VOLUME ["/usr/local/freeswitch/conf", "/usr/local/freeswitch/log", "/usr/local/freeswitch/recordings", "/usr/local/freeswitch/sounds"]

# ports
# sip/sips
EXPOSE 5060 5061 5080 5081
EXPOSE 8060 8061
# websockets
EXPOSE 5066 7433
# epmd
EXPOSE 8031 4369
# verto
EXPOSE 8081 8082
# rtp
EXPOSE 64535-65535/udp
EXPOSE 16384-32768/udp

ENTRYPOINT ["./entrypoint.sh"]
CMD ["freeswitch"]
