import logging
from datetime import datetime, timezone
from unittest.mock import patch

from src.core.shared.logging_monitor_handler import LoggingMonitoringHandler


@patch("src.core.shared.logging_monitor_handler.requests.post")
def test_emit_uses_custom_formatter(mock_post):
    handler = LoggingMonitoringHandler("http://monitor.local/ingest")
    fmt = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
    handler.setFormatter(fmt)
    record = logging.LogRecord("customLogger", logging.WARNING, "/p", 5, "hello %s", ("world",), None)

    handler.emit(record)

    assert mock_post.called
    payload = mock_post.call_args[1]["json"]
    assert payload["message"] == "WARNING:customLogger:hello world"
    assert payload["level"] == "WARNING"
    assert payload["logger"] == "customLogger"


@patch("src.core.shared.logging_monitor_handler.requests.post")
def test_default_timeout_is_two_seconds(mock_post):
    handler = LoggingMonitoringHandler("http://monitor.local/ingest")
    record = logging.LogRecord("tlogger", logging.DEBUG, "/p", 1, "msg", (), None)

    handler.emit(record)

    assert mock_post.call_count == 1
    assert mock_post.call_args[1]["timeout"] == 2.0


@patch("src.core.shared.logging_monitor_handler.requests.post")
def test_time_is_iso_utc_with_timezone(mock_post):
    handler = LoggingMonitoringHandler("http://monitor.local/ingest")
    record = logging.LogRecord("timelog", logging.INFO, "/p", 1, "msg", (), None)

    handler.emit(record)

    payload = mock_post.call_args[1]["json"]
    dt = datetime.fromisoformat(payload["time"])
    
    assert dt.tzinfo is not None
    assert dt.utcoffset() == timezone.utc.utcoffset(dt)


@patch("src.core.shared.logging_monitor_handler.logging.error")
@patch("src.core.shared.logging_monitor_handler.requests.post")
def test_emit_handles_formatter_exception(mock_post, mock_log_error):
    class BadFormatter(logging.Formatter):
        def format(self, record):
            raise RuntimeError("formatter boom")

    mock_post.side_effect = AssertionError("requests.post should not be called when formatting fails")
    handler = LoggingMonitoringHandler("http://monitor.local/ingest")
    handler.setFormatter(BadFormatter())
    record = logging.LogRecord("badfmt", logging.ERROR, "/p", 1, "msg", (), None)

    handler.emit(record)

    assert mock_post.called is False or mock_post.call_count == 0
    mock_log_error.assert_called_once()
    call_args = mock_log_error.call_args[0]
    assert call_args[0] == "Failed to post log to monitoring service: %s"
    assert isinstance(call_args[1], Exception)
    assert "formatter boom" in str(call_args[1])
