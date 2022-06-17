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
  d. Remove subtitles
  e. Migz-Transcode Using CPU & FFMPEG:
    - container: mkv
    - enable_10bit: false
    - force_conform: false
  f. New file size check
