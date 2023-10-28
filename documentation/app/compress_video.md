## Documentation for `compress_video.py`

### File Description

`compress_video.py` is a module responsible for compressing video files to a specified size.

### Function `compress_video(video_full_path, size_upper_bound, two_pass=True, filename_suffix='cps_')`

```python
def compress_video(video_full_path, size_upper_bound, two_pass=True, filename_suffix='cps_'):
    # ... code ...
```
This function compresses a video file to meet a specified maximum size requirement.

- `video_full_path`: The full path of the video file to be compressed.

- `size_upper_bound`: The maximum size of the compressed video in KB.

- `two_pass`: A boolean indicating whether to use a two-pass compression process (default is True).

- `filename_suffix`: A suffix to be added to the filename of the compressed video (default is 'cps_').

### Returns:

- If successful, returns the filename of the compressed video.
- If unsuccessful, returns False.
### The function performs the following steps:

- Extracts the filename and extension from the video path.

- Sets the extension to .mp4.

- Constructs the output filename with the specified suffix.

- Calculates the total bitrate required to meet the size constraint.

- Verifies that the total bitrate is above a specified lower bound.

- Estimates the best minimum size for the video.

- Checks if the specified upper bound is below the recommended minimum size.

- Computes the target audio bitrate.

- Computes the target video bitrate.

- Checks if the video bitrate is extremely low and returns False.

- Runs the compression process using ffmpeg, either in one or two passes.

- Checks if the resulting file size is within the specified upper bound.

- If the file size is still above the upper bound, recursively calls the compression function.