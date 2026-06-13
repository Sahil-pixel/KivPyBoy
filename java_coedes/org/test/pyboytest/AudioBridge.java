package org.test.pyboytest;

import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioTrack;

public class AudioBridge {

    private AudioTrack audioTrack;

    private static final int SAMPLE_RATE = 44100;

    public AudioBridge() {

        int bufferSize = AudioTrack.getMinBufferSize(
                SAMPLE_RATE,
                AudioFormat.CHANNEL_OUT_STEREO,
                AudioFormat.ENCODING_PCM_16BIT
        );

        audioTrack = new AudioTrack(
                AudioManager.STREAM_MUSIC,
                SAMPLE_RATE,
                AudioFormat.CHANNEL_OUT_STEREO,
                AudioFormat.ENCODING_PCM_16BIT,
                bufferSize,
                AudioTrack.MODE_STREAM
        );

        audioTrack.play();
    }

    //MAIN FUNCTION CALLED FROM PYTHON
    public void sendAudio(byte[] data) {

        if (audioTrack != null){
        android.util.Log.d("AUDIO", "bytes = " + data.length);

        audioTrack.write(data, 0, data.length);
    }
    }

    public void release() {

        if (audioTrack != null) {
            audioTrack.stop();
            audioTrack.release();
            audioTrack = null;
        }
    }
}