# Simplified version and explanation at: https://stackoverflow.com/a/64439347/12866353

import os
import ffmpeg
def compress_video(video_full_path, size_upper_bound, two_pass=True, filename_suffix='cps_'):
    """
    Compress video file to max-supported size.
    :param video_full_path: the video you want to compress.
    :param size_upper_bound: Max video size in KB.
    :param two_pass: Set to True to enable two-pass calculation.
    :param filename_suffix: Add a suffix for new video.
    :return: out_put_name or error
    """
    filename, extension = os.path.splitext(video_full_path)
    extension = '.mp4'
    output_file_name = filename + filename_suffix + extension

    # Adjust them to meet your minimum requirements (in bps), or maybe this function will refuse your video!
    total_bitrate_lower_bound = 11000
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000
    min_video_bitrate = 100000

    # Bitrate reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
    probe = ffmpeg.probe(video_full_path)
    # Video duration, in s.
    print(probe)
    duration = float(probe['format']['duration'])
    # Audio bitrate, in bps.
    audio_bitrate = 0
    # Target total bitrate, in bps.
    target_total_bitrate = (size_upper_bound * 1024 * 8) / (1.073741824 * duration)
    if target_total_bitrate < total_bitrate_lower_bound:
        print('Bitrate is extremely low! Stop compress!')
        return False

    # Best min size, in kB.
    best_min_size = (min_audio_bitrate + min_video_bitrate) * (1.073741824 * duration) / (8 * 1024)
    if size_upper_bound < best_min_size:
        print('Quality not good! Recommended minimum size:', '{:,}'.format(int(best_min_size)), 'KB.')
        # return False

    # Target audio bitrate, in bps.
    audio_bitrate = audio_bitrate

    # target audio bitrate, in bps
    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate

    # Target video bitrate, in bps.
    video_bitrate = target_total_bitrate - audio_bitrate
    if video_bitrate < 1000:
        print('Bitrate {} is extremely low! Stop compress.'.format(video_bitrate))
        return False

    i = ffmpeg.input(video_full_path)
    if two_pass:
        ffmpeg.output(i, os.devnull,
                        **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                        ).overwrite_output().run()
        ffmpeg.output(i, output_file_name,
                        **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                        ).overwrite_output().run()
    else:
        ffmpeg.output(i, output_file_name,
                        **{'c:v': 'libx264', 'b:v': video_bitrate, 'c:a': 'aac', 'b:a': audio_bitrate}
                        ).overwrite_output().run()

    if os.path.getsize(output_file_name) <= size_upper_bound * 1024:
        return output_file_name
    elif os.path.getsize(output_file_name) < os.path.getsize(video_full_path):  # Do it again
        return compress_video(output_file_name, size_upper_bound)
    else:
        return False

if __name__ == '__main__':
    file_name = compress_video('media/[2023_10_28 - 17_10_13]xyzCalibration_cube (2)_39m_0,20mm_230C_PETG_ENDER3_1800.mp4', 50 * 1000)
    print(file_name)