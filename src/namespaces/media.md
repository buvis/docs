This hosts media related applications.

## Qbittorrent

### Configuration

1. Connect to WebUI using default credentials: `admin` - `adminadmin`
2. Change the credentials in `Options - Web UI - Authentication`


## Tdarr

### Configuration

1. Transcode options for a library:
  a. Re-order all streams V2:
    - ProcessOrder: codecs,channels,languages,streamTypes
    - channels: 7.1,5.1,2,1
    - streamTypes: video,audio,subtitle
  b. Migz-Remove image formats from file
  c. Migz-Clean audio streams:
    - language: eng,und,ces,cze
    - commentary: false
    - tag_title: false
  d. Keep one audio stream
    - audioCodec: ac3
    - language: depends on library
    - channels: 2
  e. Remove subtitles
  f. Migz-Transcode Using CPU & FFMPEG:
    - container: mkv
    - enable_10bit: false
    - force_conform: false
  g. New file size check
  h. Keep original file dates and times after transcoding
    - server: 127.0.0.1
    - extensions: <empty>
    - log: false
