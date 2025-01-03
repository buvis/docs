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

### Transcode Options

1. Re-order all streams V2:
   - ProcessOrder: codecs,channels,languages,streamTypes
   - channels: 7.1,5.1,2,1
   - streamTypes: video,audio,subtitle
2. Migz-Remove image formats from file
3. Migz-Clean audio streams:
   - language: eng,en,und,ces,cze,cs,cz
   - commentary: false
   - tag_title: false
4. Keep one audio stream
   - audioCodec: ac3
   - language: eng,en,und,ces,cze,cs,cz
   - channels: 2
5. Drpeppershaker Extract Embedded Subtitles And Optionally Remove Them
   - remove_subs: yes
6. Migz Transcode Using CPU & FFMPEG
   - container: mkv
   - enable_10bit: false
   - force_conform: false
7. New file size check
8. Keep original file dates and times after transcoding
   - log: false

### Backup

1. Go to tdarr web
2. Backups - Create backup
3. Copy backups to your laptop: `POD_NAME=$(kubectl get pods -l=app.kubernetes.io/name=tdarr -n media -o=jsonpath='{range .items..metadata}{.name}{"\n"}{end}'); kubectl cp media/$POD_NAME:/app/server/Tdarr/Backups ~/Downloads/tdarr-backups`
