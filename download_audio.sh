#!/bin/bash

# Function to download audio of a video
download_audio() {
    local url=$1
    local output_dir=$2
    echo "Starting audio download for: $url"
    if [ -n "$output_dir" ]; then
        yt-dlp -f bestaudio --extract-audio --audio-format mp3 -o "$output_dir/%(title)s.%(ext)s" "$url"
    else
        yt-dlp -f bestaudio --extract-audio --audio-format mp3 "$url"
    fi
    if [ $? -eq 0 ]; then
        echo "Audio download completed successfully for: $url"
    else
        echo "An error occurred during audio download for: $url"
    fi
}

# Check if at least one URL was provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <YouTube URL> [<YouTube URL>...] [<output directory>]"
    exit 1
fi

# Extract the output directory if provided
output_dir=""
if [ -d "${!#}" ]; then
    output_dir="${!#}"
    set -- "${@:1:$(($#-1))}"
fi

# Loop through all provided URLs and download them in the background
for url in "$@"; do
    download_audio "$url" "$output_dir" &
done

# Wait for all background processes to complete
wait

echo "All audio downloads completed."
