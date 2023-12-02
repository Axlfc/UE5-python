from IPython import display as disp
import torch
import torchaudio
from denoiser import pretrained  # pip3 install -U denoiser
from denoiser.dsp import convert_audio
import os


def generate_denoised_audiofile(audio_input_wav_file):
    # GPU: model = pretrained.dns64().cuda()
    model = pretrained.dns64()
    wav, sr = torchaudio.load(audio_input_wav_file)
    # GPU: wav = convert_audio(wav.cuda(), sr, model.sample_rate, model.chin)
    wav = convert_audio(wav, sr, model.sample_rate, model.chin)

    with torch.no_grad():
        denoised = model(wav[None])[0]

    output_filename = "den_" + audio_input_wav_file[::-1].split("/")[0][::-1]
    print("FILENAME:\t", output_filename)

    torchaudio.save(output_filename, denoised.cpu(), sample_rate=model.sample_rate)


def main():
    # Multiple files to denoise
    path = "/path/to/audiofiles"
    files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for file in files:
        generate_denoised_audiofile(file)


if __name__ == '__main__':
    main()
