import pvporcupine
import struct

class WakeWordDetector:
    def __init__(self, keyword_path, sensitivity=0.5):
        try:
            self.porcupine = pvporcupine.create(
                keyword_paths=[keyword_path],
                sensitivities=[sensitivity]
            )
        except pvporcupine.PorcupineActivationFailed as e:
            raise Exception(f"Failed to create Porcupine object: {e}")

    def detect_wake_word(self, audio_data):
        pcm = struct.unpack_from("h" * self.porcupine.frame_length, audio_data)
        keyword_index = self.porcupine.process(pcm)
        return keyword_index

    def delete(self):
        if hasattr(self, 'porcupine'):
            self.porcupine.delete()

if __name__ == "__main__":
    keyword_path = "PATH_TO_AIRA_KEYWORD_FILE.ppn"
    sensitivity = 0.5

    wake_word_detector = WakeWordDetector(keyword_path, sensitivity)

    while True:
        # Replace this with your actual audio input source
        audio_data = get_audio_data()
        keyword_index = wake_word_detector.detect_wake_word(audio_data)

        if keyword_index == 0:
            print("Wake word 'AIRA' detected!")
            # Take action when the wake word is detected

    wake_word_detector.delete()
