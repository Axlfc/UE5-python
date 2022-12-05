import subprocess

# Start recording from the microphone for 5 seconds
record_process = subprocess.Popen(["termux-microphone-record", "-d", "5"])
record_process.wait()

# Convert the recorded audio to text
speech_to_text_process = subprocess.Popen(["termux-speech-to-text", "-l", "en", "-i", "recorded.mp3"], stdout=subprocess.PIPE)

# Read the transcribed text from the output of the speech-to-text command
speech_text = speech_to_text_process.stdout.read().decode("utf-8")
print("You said: " + speech_text)