# Simplified version and explanation at: https://stackoverflow.com/a/64439347/12866353

import os
import ffmpeg

import asyncio

async def compress_video(video_full_path, size_upper_bound, two_pass=True, filename_suffix='cps_'):
    # ... Your code for probing and setting up variables ...
    filename, extension = os.path.splitext(video_full_path)
    extension = '.mp4'
    output_file_name = filename + filename_suffix + extension

    # Adjust them to meet your minimum requirements (in bps), or maybe this function will refuse your video!
    total_bitrate_lower_bound = 11000
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000
    min_video_bitrate = 100000
    # Bitrate reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
    probe = await asyncio.to_thread(ffmpeg.probe, video_full_path)
    # Video duration, in s.
    print(probe)
    duration = float(probe['format']['duration'])
    # Audio bitrate, in bps.
    audio_bitrate = 0
    # Target total bitrate, in bps.
    target_total_bitrate = (size_upper_bound * 1024 * 8) / (1.073741824 * duration)
    print(target_total_bitrate)
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
    print(video_bitrate)
    if video_bitrate < 1000:
        print('Bitrate {} is extremely low! Stop compress.'.format(video_bitrate))
        return False
    cmd = [
        'ffmpeg',
        '-i', video_full_path,
        '-c:v', 'libx264',
        '-b:v', f'{video_bitrate}',
        '-c:a', 'aac',
        '-b:a', f'{audio_bitrate}',
        output_file_name
    ]

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    await process.wait()
    print(stderr)
    if os.path.getsize(output_file_name) <= size_upper_bound * 1024:
        return output_file_name
    elif os.path.getsize(output_file_name) < os.path.getsize(video_full_path):
        return await compress_video(output_file_name, size_upper_bound)
    else:
        return False



if __name__ == '__main__':
    async def main():
        file_name = await compress_video('media/[2023_10_28 - 20_19_29]V29D_Fixed_2h1m_0,20mm_230C_PETG_ENDER3_1800cps_.mp4', 50*1000)
        print(file_name)

    asyncio.run(main())