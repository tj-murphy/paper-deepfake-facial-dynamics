import os
import glob
import subprocess

# Input and outpur directories
input_dir = '/Deepfakes/FaceForesics - Deepfakes/original_sequences/actors/c23/videos'
output_dir = '/OpenFace-outputs'

# Make sure output dir exists
os.makedirs(output_dir, exist_ok=True)

# Define video extensions to look for
video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv']

# Collect all videos from input
video_files = []
for ext in video_extensions:
    video_files.extend(glob.glob(os.path.join(input_dir, ext)))

# Path to openface binary
openface_path = 'OpenFace_2.2.0_win_x64/FeatureExtraction.exe'

# Loop through each video file
for video_path in video_files:
    # Extract base filename without extension for naming outputs
    base_name = os.path.splitext(os.path.basename(video_path))[0]

    # Construct the command
    command = [
        openface_path,
        '-f', video_path,   # Input video file
        '-out-dir', output_dir,  # Output directory
        '-of', base_name  # Output filename prefix
    ]

    print("Running command:", ' '.join(command))
    try:
        subprocess.run(command, check=True)
        print(f"Successfully processed {video_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {video_path}: {e}")

