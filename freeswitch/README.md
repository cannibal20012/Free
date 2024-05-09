# FreeSWITCH for Docker

A slim Freeswitch 1.10.11 image based on the [docker-drachtio-freeswitch-mrf](https://github.com/drachtio/docker-drachtio-freeswitch-mrf) image.

## Commands

To run with default options:

```bash
docker run -d --rm \
  --name freeswitch-instance \
  --net=host \
  -v ./conf:/usr/local/freeswitch/conf \
  -v ./log:/usr/local/freeswitch/log  \
  -v ./recordings:/usr/local/freeswitch/recordings \
  -v ./sounds:/usr/local/freeswitch/sounds \
    servicebots/freeswitch freeswitch
```

or:

```bash
./start
```

To jump in to a running container with a freeswitch console:

```bash
docker exec -ti freeswitch-instance fs_cli
```

or:

```bash
./fs_cli
```

To stop the container, execute:

```bash
docker stop -t 0 freeswitch
```

or:

```bash
./stop
```

To remove all data from mount volumes use:

```bash
./start --prune
```

or:

```bash
./stop --prune
```

> Note: you can also jump into the container with `bash` instead of `fs_cli` to get to a shell prompt in the container.

This is a **very** minimal image, with support only for dialplan and event socket (no scripting languages such as lua or javascript are compiled in), no sounds, and a minimal set of modules (see below for the modules.conf.xml showing which modules are being loaded).  As mentioned, it is primarily designed for use with the drachtio-fsrmf framework.

The container exposes the following volumes, which allow you to provide the canned freeswitch sound files from your host machine:

- */usr/local/freeswitch/conf* (to let you provide conf files),
- */usr/local/freeswitch/log* (to let you save freeswitch log files)
- */usr/local/freeswitch/recordings* (to let you save recordings to the host filesystem), and
- */usr/local/freeswitch/sounds* (to let you provide the canned freeswitch sound files),

This container supports the ability to configure the various ports Freeswitch claims, in order to easily run multiple Freeswitch containers on the same host

- *-s*, *--sip-port* the sip port to listen on (default: 5080)
- *-t*, *--tls-port* the tls port to listen on (default: 5081)
- *-e*, *--event-socket-port* the port that Freeswitch event socket listens on (default: 8021)
- *-p*, *--password* the event socket password (default: ClueCon)
- *-c*, *--cookie* the erlang event connection cookie (default: ClueCon)
- *--username* the username for MRF SIP profile (default: ClueCon)
- *--rtp-range-start* the starting UDP port for RTP traffic
- *--rtp-range-end* the ending UDP port for RTP traffic
- *-l*, *--loglevel* the log level for FreeSWITCH instance (default: debug)

An example of starting a container with advanced options:

```bash
docker run -d --rm \
  --name freeswitch-instance \
  --net=host \
  -v ./conf:/usr/local/freeswitch/conf \
  -v ./log:/usr/local/freeswitch/log  \
  -v ./recordings:/usr/local/freeswitch/recordings \
  -v ./sounds:/usr/local/freeswitch/sounds \
    servicebots/freeswitch freeswitch --sip-port 5038 --tls-port 5039 --rtp-range-start 20000 --rtp-range-end 21000
```

## Exposed ports

- **SIP/SIPS:** 5060, 5061, 5080, 5081
- **Websockets:** 5066, 7433
- **EPMD:** 8031
- **Verto:** 8081, 8082
- **RTP:** 64535-65535, 16384-32768

## Overrides from default distribution

Before any changes, run:

```bash
./init_modules.sh
```

`init_modules.sh` will clone default FreeSWITCH and third party modules from [Jambonz repository](https://github.com/jambonz/freeswitch-modules).

All changes are inside the `build/changes` directory. To refresh patches to apply in image build stage, use:

```bash
python3 build/scripts/generate_patches.py
```

To test generated patches, run:

```bash
python3 build/scripts/apply_patches.py
```

## Third party modules

Please refer to available modules in [Jambonz repository](https://github.com/jambonz/freeswitch-modules). All modules there are pre-compiled on this image.

To enable another module, change `autoload_configs/modules.conf.xml` from your mount volume for `/usr/local/freeswitch/conf`. Default configuration is:

```xml
<configuration name="modules.conf" description="Modules">
  <modules>
    ...

    <!-- 3rd Party Applications -->
    <load module="mod_audio_fork"/>
    <!-- <load module="mod_assemblyai_transcribe"/> -->
    <!-- <load module="mod_aws_lex"/> -->
    <!-- <load module="mod_aws_transcribe"/> -->
    <!-- <load module="mod_azure_transcribe"/> -->
    <!-- <load module="mod_azure_tts"/> -->
    <!-- <load module="mod_cobalt_transcribe"/> -->
    <load module="mod_deepgram_transcribe"/>
    <load module="mod_deepgram_tts"/>
    <!-- <load module="mod_dub"/> -->
    <load module="mod_elevenlabs_tts"/>
    <!-- <load module="mod_whisper_tts"/> -->
    <!-- <load module="mod_google_transcribe"/> -->
    <!-- <load module="mod_ibm_transcribe"/> -->
    <!-- <load module="mod_nuance_transcribe"/> -->
    <!-- <load module="mod_nvidia_transcribe"/> -->
    <!-- <load module="mod_playht_tts"/> -->
    <!-- <load module="mod_rimelabs_tts"/> -->
    <!-- <load module="mod_soniox_transcribe"/> -->
    <!-- <load module="mod_jambonz_transcribe"/> -->
    <!-- <load module="mod_dialogflow"/> -->

    ...
  </modules>
</configuration>
```
