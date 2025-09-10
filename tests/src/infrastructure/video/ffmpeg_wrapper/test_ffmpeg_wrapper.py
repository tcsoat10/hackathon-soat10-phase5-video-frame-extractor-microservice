import os
import pytest
from unittest.mock import Mock, patch
from src.infrastructure.video.ffmpeg_wrapper import FFmpegWrapper


@patch("src.infrastructure.video.ffmpeg_wrapper.ffmpeg")
def test_extract_frames_success(ffmpeg_mock, tmp_path):
    video_path = "/path/to/video.mp4"
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    files = ["frame_0000.png", "frame_0001.png", "readme.txt"]
    for name in files:
        (output_dir / name).write_text("x")

    pipeline = Mock()
    pipeline.filter.return_value = pipeline
    pipeline.output.return_value = pipeline
    pipeline.run.return_value = None

    ffmpeg_mock.input.return_value = pipeline

    wrapper = FFmpegWrapper()
    extracted = wrapper.extract_frames(video_path, str(output_dir))

    expected = sorted([os.path.join(str(output_dir), f) for f in files if f.endswith(".png")])
    assert extracted == expected

    ffmpeg_mock.input.assert_called_once_with(video_path)
    pipeline.filter.assert_called_once_with("fps", fps="1")
    pipeline.output.assert_called_once_with(os.path.join(str(output_dir), "frame_%04d.png"), start_number=0)
    pipeline.run.assert_called_once_with(capture_stdout=True, capture_stderr=True, quiet=True)


@patch("src.infrastructure.video.ffmpeg_wrapper.ffmpeg")
def test_extract_frames_empty_output_dir_returns_empty(ffmpeg_mock, tmp_path):
    video_path = "/path/to/video.mp4"
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    pipeline = Mock()
    pipeline.filter.return_value = pipeline
    pipeline.output.return_value = pipeline
    pipeline.run.return_value = None

    ffmpeg_mock.input.return_value = pipeline

    wrapper = FFmpegWrapper()
    extracted = wrapper.extract_frames(video_path, str(output_dir))

    assert extracted == []
    ffmpeg_mock.input.assert_called_once_with(video_path)
    pipeline.run.assert_called_once()


@patch("src.infrastructure.video.ffmpeg_wrapper.ffmpeg")
def test_extract_frames_ffmpeg_error_reraises(ffmpeg_mock, tmp_path):
    video_path = "/path/to/video.mp4"
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    class FakeFFmpegError(Exception):
        pass

    err = FakeFFmpegError("boom")
    ffmpeg_mock.Error = FakeFFmpegError
    err.stdout = b"fake-stdout"
    err.stderr = b"fake-stderr"

    pipeline = Mock()
    pipeline.filter.return_value = pipeline
    pipeline.output.return_value = pipeline
    pipeline.run.side_effect = err

    ffmpeg_mock.input.return_value = pipeline

    wrapper = FFmpegWrapper()
    with pytest.raises(FakeFFmpegError):
        wrapper.extract_frames(video_path, str(output_dir))
