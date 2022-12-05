import sys
import pyaudio
import wave
import process_system
import os
import subprocess

def load_audio_file():
    return wave.open(sys.argv[1], 'rb')


def open_audio_file():
    # Open the audio file
    audio = load_audio_file()
    # Open the audio playback stream
    p = pyaudio.PyAudio()
    stream = p.open(
        format=p.get_format_from_width(audio.getsampwidth()),
        channels=audio.getnchannels(),
        rate=audio.getframerate(),
        output=True,
    )

    # Play the audio
    data = audio.readframes(1024)
    while data:
        stream.write(data)
        data = audio.readframes(1024)

    # Close the audio playback stream
    stream.stop_stream()
    stream.close()
    p.terminate()


def main():
    if process_system.plat() == "Windows":
        open_audio_file()
    elif subprocess.check_output(['uname', '-o']).strip() == b'Android':
        command0 = "pulseaudio -D"
        command = "play " + sys.argv[1]
        command1 = "pulseaudio -k"
        os.system(command0)
        os.system(command)
        os.system(command1)
    else:
        open_audio_file()


if __name__ == '__main__':
    main()


# import unreal_engine as ue
# from unreal_engine.classes import PyActor

# Create a new actor and add it to the level
# actor = PyActor()
# ue.add_actor_to_level(actor)

# Set the actor's location and rotation
# actor.set_actor_location(ue.Vector(0, 0, 100))
# actor.set_actor_rotation(ue.Rotator(0, 45, 0))


