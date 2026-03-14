import os
import json
import random
import time
import sys
import pygame


def main():
    print("=== Minecraft Music Player ===")

    mc_path = input("Please enter the complete path of the .minecraft folder:").strip()
    if not os.path.isdir(mc_path):
        print("The path is invalid. Please check and try again.")
        return

    indexes_dir = os.path.join(mc_path, "assets", "indexes")

    index_files = []
    if os.path.isdir(indexes_dir):
        index_files = [f for f in os.listdir(indexes_dir) if f.endswith(".json")]

    if not index_files:
        print(f"The index file was not found in {indexes_dir}.")
        manual = input(
            "Please manually enter the complete path of the index file (press Enter to exit):"
        ).strip()
        if not manual or not os.path.isfile(manual):
            return
        index_path = manual
    else:
        print("\nFound the following index files (versions):")
        for i, f in enumerate(index_files, 1):
            print(f"{i}. {f}")
        choice = input(
            "Please enter the number or directly input the file name (for example, 1.12.json):"
        ).strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(index_files):
                index_path = os.path.join(indexes_dir, index_files[idx])
            else:
                print("Invalid number code")
                return
        else:
            if choice in index_files:
                index_path = os.path.join(indexes_dir, choice)
            else:
                print("The file does not exist.")
                return

    with open(index_path, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    objects = index_data.get("objects", {})
    music_entries = []
    for path, info in objects.items():
        if path.startswith("minecraft/sounds/music/game/"):
            music_entries.append((path, info["hash"]))

    if not music_entries:
        print("No game music was found.")
        return

    print(f"\nA total of {len(music_entries)} pieces of game music have been found:")
    for path, _ in music_entries:
        print(f"  {path}")

    banned = []
    print(
        "\nNow you can remove the music you don't like (enter the full path or partial name, and it supports fuzzy matching)."
    )
    print("Input blank lines to end the removal process.")
    while True:
        ban_input = input("remove > ").strip().lower()
        if not ban_input:
            break
        matched = []
        for path, _ in music_entries:
            if ban_input in path.lower():
                matched.append(path)
        if matched:
            for p in matched:
                if p not in banned:
                    banned.append(p)
                    print(f"  removed: {p}")
        else:
            print("  No matching items were found.")

    final_music = [(path, h) for path, h in music_entries if path not in banned]
    print(f"\nThe final playlist contains {len(final_music)} pieces of music.")
    if not final_music:
        print("No remaining music. Program exits.")
        return
    random.shuffle(final_music)

    try:
        max_interval = float(input("Please enter the maximum interval (seconds):"))
        min_interval = float(input("Please enter the minimum interval (seconds):"))
        if min_interval > max_interval:
            min_interval, max_interval = max_interval, min_interval
    except ValueError:
        print("Invalid input. Using default value of 300 to 600 seconds.")
        min_interval, max_interval = 300, 600

    print("\nStart playing! Press Ctrl+C to exit.")

    objects_dir = os.path.join(mc_path, "assets", "objects")

    try:
        while True:
            pygame.mixer.init()
            pygame.mixer.music.set_volume(0.5)
            path, hash_val = final_music.pop()
            sub_dir = hash_val[:2]
            file_path = os.path.join(objects_dir, sub_dir, hash_val)

            if not os.path.exists(file_path):
                print(f"File lost: {file_path}, skipping...")
                time.sleep(1)
                continue

            print(f"\nPlaying: {path}")
            try:
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.5)
            except Exception as e:
                print(f"Playback error: {e}")

            interval = random.uniform(min_interval, max_interval)
            print(f"Wait for {interval:.1f} seconds before the next song...")
            pygame.mixer.quit()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\nThe playback has ended.")
        pygame.mixer.quit()
        sys.exit(0)


if __name__ == "__main__":
    main()
