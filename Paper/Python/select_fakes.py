import os
import shutil
import random
import re

# Directories
REAL_VIDEO_DIR = r"C:\Users\IT102078-admin\Documents\openface-outputs\real\videos"
FAKE_VIDEO_DIR = r"C:\Users\IT102078-admin\OneDrive - University of Bristol\Deepfakes\FaceForesics - Deepfakes\manipulated_sequences\DeepFakeDetection\c23\videos"
TARGET_DIR = r"C:\Users\IT102078-admin\Documents\openface-outputs\fake"


def extract_real_video_parts(filename):
	"""
	Extracts the leading number and the identifier part from the real video filename.
	Example: "01__exit_phone_room.mp4" --> ("01", "__exit_phone_room")

	Returns a tuple (number_string, identifier_string) or (None, None) if the expected format
	('NN__identifier') is not found.
	"""

	base_filename, _ = os.path.splitext(filename) # Remove extension first
	parts = base_filename.split('__', 1) # Split only on the first double underscore

	if len(parts) == 2:
		real_number = parts[0]
		identifier = "__" + parts[1] # Add the '__' back to the identifier part
		# Basic check if the first part looks like a number (optional but good)
		if real_number.isdigit():
			return real_number, identifier
		else:
			print(f"    [-] Warning: Expected leading digits but found '{real_number}' in real filename: {filename}")
			return None, None
	else:
		print(f"    [-] Warning: Could not find '__' separator in real filename format: {filename}")
		return None, None


def find_matching_fakes(real_number, real_identifier, fake_files_list):
	"""
	Finds fake video filenames that match BOTH the real video's leading number AND contain the real
	video's identifier string.

	Matching checks:
	1. Fake filename starts with "real_number_" (e.g., "01__")
	2. Fake filename (base name, case-insensitive) contains the real_identifier.
	"""
	matches = []
	prefix_to_match = real_number + "_"
	real_identifier_lower = real_identifier.lower()

	for fake_file in fake_files_list:
		# Check 1: Does the fake filename start with the correct number prefix?
		if fake_file.startswith(prefix_to_match):
			# Check 2: Does the fake filename contain the identifier?
			fake_base, _ = os.path.splitext(fake_file)
			if real_identifier_lower in fake_base.lower():
				matches.append(fake_file)

	return matches


def main():
	print("--- Deepfake Selection Script Started ---")
	print(f"Real Video Directory: {REAL_VIDEO_DIR}")
	print(f"Fake Video Directory: {FAKE_VIDEO_DIR}")
	print(f"Target Directory: {TARGET_DIR}")
	print("-" * 40)


	# 1. Validate directories
	if not os.path.isdir(REAL_VIDEO_DIR):
		print(f"Error: Real video directory not found.")
		return
	if not os.path.isdir(FAKE_VIDEO_DIR):
		print(f"Error: Fake video directory not found.")
		return

	# Create target directory if it doesnt exist
	try:
		os.makedirs(TARGET_DIR, exist_ok=True)
		print(f"[+] Ensured target directory exists.")
	except OSError as e:
		print(f"Error: could not create target directory: {e}")
		return

	# 3. List real and fake video files
	try:
		real_files = [f for f in os.listdir(REAL_VIDEO_DIR) if os.path.isfile(os.path.join(REAL_VIDEO_DIR, f))]
		fake_files = [f for f in os.listdir(FAKE_VIDEO_DIR) if os.path.isfile(os.path.join(FAKE_VIDEO_DIR, f))]
		print(f"[+] Found {len(real_files)} files in the real video directory.")
		print(f"[+] Found {len(fake_files)} files in the fake video directory.")
	except OSError as e:
		print(f"Error listing files in source directories: {e}")
		return

	print("-" * 40)
	print("--- Starting Matching Process ---")

	# 4. Process each real video file
	copied_count = 0
	skipped_count = 0
	processed_real_identifiers = set()  # keep track

	for i, real_filename in enumerate(real_files):
		print(f"\n[{i+1}/{len(real_files)}] Processing Real Video: {real_filename}")

		# Extract number and identifier
		real_num, real_id = extract_real_video_parts(real_filename)

		if real_num is None or real_id is None:
			skipped_count += 1
			continue

		print(f"   [*] Extracted number: '{real_num}', Identifier: '{real_id}'")

		# Find corresponding fake files
		matching_fakes = find_matching_fakes(real_num, real_id, fake_files)

		if not matching_fakes:
			print(f"   [!] No matching fake videos found for Number '{real_num}' AND Identifier '{real_id}'")
			skipped_count += 1
			continue

		print(f"    [*] Found {len(matching_fakes)} corresponding fake videos:")
		for match_file in matching_fakes[:5]:
			print(f"    - {match_file}")
		if len(matching_fakes) > 5:
			print(f"    - ... and {len(matching_fakes) - 5} more.")

		# Choose one fake file at random
		selected_fake_filename = random.choice(matching_fakes)
		print(f"    [+] Randomly selected: {selected_fake_filename}")

		# Construct full paths for source and destination
		source_path = os.path.join(FAKE_VIDEO_DIR, selected_fake_filename)
		destination_path = os.path.join(TARGET_DIR, selected_fake_filename)

		# Copy the selected file
		try:
			print(f"    [*] Copying {selected_fake_filename} to {TARGET_DIR}...")
			shutil.copy2(source_path, destination_path) # copy2 preserves more metadata
			print(f"    [+] Successfully copied.")
			copied_count += 1
		except OSError as e:
			print(f"    [!] Error copying file {selected_fake_filename}: {e}")
			skipped_count += 1
		except Exception as e: # Catch any other potential errors during copy
			print(f"    [!] An unexpected error occurred during copy: {e}")
			skipped_count += 1

	print("-" * 40)
	print("--- Script Finished ---")
	print(f"Processed {len(real_files)} real video files.")
	print(f"Successfully copied {copied_count} fake video files.")
	print(f"Skipped {skipped_count} real videos (due to no identifier, no matches, or copy errors).")
	print(f"Selected fake videos are in: {TARGET_DIR}")
	print("-" * 40)



if __name__ == "__main__":
	main()