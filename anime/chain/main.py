import os
import subprocess

def convert_mp4_to_mpd(input_file, output_dir):
    """
    Converts an MP4 video file to MPEG-DASH (MPD) format using ffmpeg.

    Parameters:
        input_file (str): Path to the input MP4 file.
        output_dir (str): Path to the directory where the MPD file will be saved.

    Returns:
        str: Path to the generated MPD file.
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' does not exist.")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Construct output paths
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, f"{base_name}.mpd")

    # FFmpeg command to convert MP4 to MPD
    command = [
        "ffmpeg",
        "-i", input_file,               # Input MP4 file
        "-map", "0",                    # Map all streams
        "-b:v", "1000k",                # Set video bitrate
        "-min_seg_duration", "5000",    # Set minimum segment duration (5 seconds)
        "-use_template", "1",           # Use template for MPD
        "-use_timeline", "1",           # Use timeline for MPD
        "-init_seg_name", "init-$RepresentationID$.mp4",  # Init segment naming
        "-media_seg_name", "chunk-$RepresentationID$-$Number$.m4s",  # Media segment naming
        "-f", "dash",                   # Set format to DASH
        output_file                     # Output MPD file
    ]

    # Execute the command
    subprocess.run(command, check=True)

    return output_file

# Example Usage
try:
    input_mp4 = r"sev.mp4"  # Change this path to your MP4 file
    output_directory = r"out"   # Directory to save the MPD file

    output_mpd = convert_mp4_to_mpd(input_mp4, output_directory)
    print(f"MPD file generated successfully: {output_mpd}")
except Exception as e:
    print(f"Error: {e}")
