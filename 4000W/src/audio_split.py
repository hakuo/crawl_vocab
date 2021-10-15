# Import the AudioSegment class for processing audio and the 
# split_on_silence function for separating out silent chunks.
from pydub import AudioSegment
from pydub.silence import split_on_silence
import time

filename_template = "{folder}/4000W_{index}.{ext}"

# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)


for i in range(3600):
    time.sleep(1)
    idx = i+1
    # Load your audio.
    filename = filename_template.format(index=f'{idx:04d}', ext="mp3", folder="data")
    song = AudioSegment.from_mp3(filename)

    # Split track where the silence is 2 seconds or more and get chunks using 
    # the imported function.
    chunks = split_on_silence (
        # Use the loaded audio.
        song, 
        # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
        min_silence_len = 1000,
        # Consider a chunk silent if it's quieter than -16 dBFS.
        # (You may want to adjust this parameter.)
        silence_thresh = -26
    )

    if(len(chunks) != 3):
        print(("Error at index {index}, len = {length}").format(index=idx, length=len(chunks)))
        continue

    # Process each chunk with your parameters
    for i, chunk in enumerate(chunks):
        # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
        silence_chunk = AudioSegment.silent(duration=500)

        # Add the padding chunk to beginning and end of the entire chunk.
        audio_chunk = silence_chunk + chunk + silence_chunk

        # Normalize the entire chunk.
        normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

        # Export the audio chunk with new bitrate.
        index = f'{idx:04d}' + "_" + str(i)
        fn_export = filename_template.format(index=index, ext="mp3", folder="export")
        # print("Exporting", fn_export)
        normalized_chunk.export(
            fn_export,
            format = "mp3"
        )
