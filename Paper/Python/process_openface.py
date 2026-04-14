import os
import subprocess
import sys

# Directories
openface_exe_path = r"OpenFace_2.2.0_win_x64\FeatureExtraction.exe"
source_path = r"openface-outputs\real\videos"
target_path = r"openface-outputs\real-output"

video_extensions = ['.avi', '.mp4']


def process_videos(exe, source_dir, target_dir, extensions):
	# Make sure exe exists
	if not os.path.isfile(exe):
		print(f"Error: OpenFace exe not found at '{exe}'")
		sys.exit(1)

	# Make sure source dir exists
	if not os.path.isdir(source_dir):
		print(f"Error: Source video directory not found at '{source_dir}'")
		sys.exit(1)

	# Create target dir if doesnt exist already
	try:
		os.makedirs(target_dir, exist_ok=True)
		print(f"Output will be saved to: '{target_dir}'")
	except OSError as e:
		print(f"Error creating target directory: {e}")
		sys.exit(1)


	print(f"\nStarting processing videos in: '{source_dir}'...")
	processed_count = 0
	skipped_count = 0

	# Iterate through all files in source dir
	for filename in os.listdir(source_dir):
		# Get full path of current item
		source_file_path = os.path.join(source_dir, filename)

		# Check if it's a file and has valid video extension
		if os.path.isfile(source_file_path):
			file_name_lower = filename.lower()
			file_ext = os.path.splitext(file_name_lower)[1]

			if file_ext in extensions:
				print(f"\nProcessing video: {filename}")

				# Command
				command = [
				exe,
				"-f", source_file_path,
				"-aus", # Only want action units in csv
				#"-tracked", # Video with overlay as well
				"-out_dir", target_dir
				]

				print(f"Running command: {' '.join(command)}")

				try:
					result = subprocess.run(command, check=True, capture_output=False, text=True)
					print(f"Successfully processed: {filename}")
					processed_count += 1
				except subprocess.CalledProcessError as e:
					print(f"Error processing {filename}: OpenFace returned an error.")
					print(f"Return code: {e.returncode}")
					print(f"Stderr: {e.stderr}")
					skipped_count += 1
				except Exception as e:
					print(f"An unexpected error occurred while processing {filename}: {e}")
					skipped_count += 1
			else:
				print(f"Skipping non-video file: {filename}")
				pass
		else:
			print(f"Skipping directory: {filename}")
			pass

	print("\n--- Processing Summary ---")
	print(f"Total videos processed sucessfully: {processed_count}")
	print(f"Total files skipped or failed: {skipped_count}")
	print("-" * 40)


if __name__ == "__main__":
	process_videos(
		openface_exe_path,
		source_path,
		target_path,
		video_extensions
		)
	print("\nScript finished.")