This hosts media related applications.

## Lidarr

### Configuration

1. Prepend `_LIDARR_ADDITIONS` to `Media Management - Track Naming - Standard Track Format & Multi Disc Format`

## Sonarr

### Configuration

#### Media Management - Episode Naming

- Rename Episodes = true
- Standard Episode Format = {Series Title} ({Series Year}) - S{season:00}E{episode:00} - {Episode Title}
- Daily Episode Format = {Series Title} ({Series Year}) - {Air-Date} - {Episode Title} {Quality Full}
- Anime Episode Format = {Series Title} ({Series Year}) - S{season:00}E{episode:00} - {Episode Title} {Quality Full}
- Season Folder Format = Season {season:00}
- Multi Episode Style = Repeat

## Radarr

Trakt based RSS need to authorize with Trakt from time to time:

1. Settings - Import Lists
2. For each list press `Authenticate with Trakt` button

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

### Backup

1. Go to tdarr web
2. Backups - Create backup
3. Copy backups to your laptop: `POD_NAME=$(kubectl get pods -l=app.kubernetes.io/name=tdarr -n media -o=jsonpath='{range .items..metadata}{.name}{"\n"}{end}'); kubectl cp media/$POD_NAME:/app/server/Tdarr/Backups ~/Downloads/tdarr-backups`
