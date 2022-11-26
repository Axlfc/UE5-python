import os
from git import Repo  # pip install gitpython
import subprocess
import pkg_resources
import sys
import soundfile as sf
import gdown


def pip_install(package):
    query = []
    pythonpath = 'python'
    query.append(pythonpath)
    query.append('-m pip install ' + package)

    querystring = ""
    final_query = []

    for i in range(len(query)):
        final_query.append(query[i])
        querystring += " " + query[i]

    # Always upgrade pip to the latest version
    subprocess.run(querystring, shell=True)


def check_install_dependencies(repodir):
    x = repodir + "\\" + "pipisupdated.txt"
    if not os.path.exists(x):
        # Capturing installed pip packages
        installed_packages = pkg_resources.working_set
        installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
        installed_packages_names_list = []
        for installedPackage in range(len(installed_packages_list)):
            installed_packages_names_list.append(installed_packages_list[installedPackage].split("=")[0])

        requirements_path = repodir + "\\" + "requirements.txt"
        pipPackages = []
        with open(requirements_path, encoding="utf-16") as f:
            lines = f.readlines()
            for pipPackage in lines:
                pipPackages.append(pipPackage)
        # pipPackages.append("https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.14.0-py3-none-any.whl")
        # pipPackages.append("ipython")
        print(pipPackages)
        for pippackage in pipPackages:
            if pippackage not in installed_packages_names_list:
                pip_install(pippackage)
        # Create external file to avoid constant pip updates and upgrades.
        open(x, 'a').close()


def clone_voice_repo(repodir):
    if not os.path.exists(repodir):
        print("Cloning Real-Time-Voice-Cloning repo")
        os.mkdir(repodir)
        Repo.clone_from("https://github.com/CorentinJ/Real-Time-Voice-Cloning", repodir)

    outputfilepath = repodir + "\\" + "outputs"
    if not os.path.exists(outputfilepath):
        os.mkdir(outputfilepath)


def downloadModels(repoDir):
    x = repoDir + "\\" + "modelsDownloaded.txt"
    encoderURL = "https://drive.google.com/uc?export=download&id=1q8mEGwCkFy23KZsinbuvdKAQLqNKbYf1"
    synthesizerURL = "https://drive.google.com/u/0/uc?id=1EqFMIbvxffxtjiVrtykroF6_mUh-5Z3s"
    vocoderURL = "https://drive.google.com/uc?export=download&id=1cf2NO6FtI0jDuy8AV3Xgn6leO6dHjIgu"

    foldersavemodels = repoDir + "\\" + "saved_models"
    if not os.path.exists(foldersavemodels):
        os.mkdir(foldersavemodels)

    defaultfolder = foldersavemodels + "\\" + "default"
    if not os.path.exists(defaultfolder):
        os.mkdir(defaultfolder)

    outputencoder = defaultfolder + "\\" + "encoder.pt"
    outputsynthesizer = defaultfolder + "\\" + "synthesizer.pt"
    outputvocoder = defaultfolder + "\\" + "vocoder.pt"

    gdown.download(encoderURL, outputencoder, quiet=False)
    gdown.download(synthesizerURL, outputsynthesizer, quiet=False)
    gdown.download(vocoderURL, outputvocoder, quiet=False)
    open(x, 'a').close()

def main():
    repo_dir = os.path.join(os.getcwd().split("\n")[0], "voiceCloning")
    clone_voice_repo(repo_dir)
    check_install_dependencies(repo_dir)
    if not os.path.exists(repo_dir + "\\" + "modelsDownloaded.txt"):
        downloadModels(repo_dir)

    # Initializing all the encoder libraries

    from IPython.display import Audio
    from IPython.utils import io

    sys.path.append(repo_dir)

    from synthesizer.inference import Synthesizer
    from encoder import inference as encoder
    from vocoder import inference as vocoder
    from pathlib import Path
    import numpy as np
    import librosa

    outputencoder = repo_dir + "\\" + "saved_models" + "\\" + "default" + "\\" + "encoder.pt"
    outputsynthesizer = repo_dir + "\\" + "saved_models" + "\\" + "default" + "\\" + "synthesizer.pt"
    outputvocoder = repo_dir + "\\" + "saved_models" + "\\" + "default" + "\\" + "vocoder.pt"

    encoder_weights = Path(outputencoder)
    vocoder_weights = Path(outputvocoder)
    syn_dir = Path(outputsynthesizer)
    encoder.load_model(encoder_weights)
    synthesizer = Synthesizer(syn_dir)
    vocoder.load_model(vocoder_weights)

    text = sys.argv[1]
    audiopath = sys.argv[2]
    in_fpath = Path(audiopath)
    preprocessed_wav = encoder.preprocess_wav(in_fpath)
    original_wav, sampling_rate = librosa.load(str(in_fpath))
    preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
    print("Loaded file succesfully")
    embed = encoder.embed_utterance(preprocessed_wav)
    print("Created the embedding")

    texts = [text]
    embeds = [embed]

    specs = synthesizer.synthesize_spectrograms(texts, embeds)
    spec = specs[0]

    generated_wav = vocoder.infer_waveform(spec)

    generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")

    generated_wav = encoder.preprocess_wav(generated_wav)

    with io.capture_output() as captured:
        specs = synthesizer.synthesize_spectrograms([text], [embed])

    filename = repo_dir + "\\" + "outputs" + "\\" + text[:20].replace(" ", "_").replace(",", "").replace(".", "").replace("'", "") + ".wav"
    sf.write(filename, generated_wav.astype(np.float32), synthesizer.sample_rate)


if __name__ == '__main__':
    main()
