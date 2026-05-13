import os
import json
import subprocess
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
INDEX_JS = os.path.join(PROJECT_DIR, "index.js")
STREAM_FILE = os.path.join(PROJECT_DIR, "stream.jsonl")
SUMMARY_FILE = os.path.join(PROJECT_DIR, "summary.json")


def _read_non_empty_lines(path):
    with open(path, "r") as f:
        return [line for line in f.read().splitlines() if line.strip()]


def test_index_js_exists():
    assert os.path.isfile(INDEX_JS), f"index.js not found at {INDEX_JS}"


def test_index_js_uses_streaming_sdk_call():
    with open(INDEX_JS, "r") as f:
        content = f.read()

    assert "@inconvoai/node" in content, \
        "Expected @inconvoai/node to be imported in index.js"
    assert "stream: true" in content or "stream:true" in content, \
        "Expected index.js to call the SDK with `stream: true`."
    assert "for await" in content, \
        "Expected index.js to consume the streaming response with `for await`."


def test_run_index_js_produces_outputs():
    env = os.environ.copy()
    for required in ("INCONVO_API_KEY", "INCONVO_AGENT_ID", "INCONVO_DB_URL"):
        assert required in env and env[required], \
            f"Required environment variable {required} is not set in the verifier."

    # Remove any prior output to ensure we test fresh output from the run.
    for path in (STREAM_FILE, SUMMARY_FILE):
        if os.path.exists(path):
            os.remove(path)

    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        env=env,
        timeout=300,
    )
    assert result.returncode == 0, \
        f"'node index.js' failed (exit {result.returncode}).\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"


def test_stream_jsonl_exists_with_multiple_json_lines():
    assert os.path.isfile(STREAM_FILE), f"stream.jsonl not found at {STREAM_FILE}"

    lines = _read_non_empty_lines(STREAM_FILE)
    assert len(lines) > 1, \
        f"Expected more than 1 non-empty line in stream.jsonl, got {len(lines)}."

    parsed_chunks = []
    for idx, line in enumerate(lines):
        try:
            parsed_chunks.append(json.loads(line))
        except json.JSONDecodeError as e:
            pytest.fail(f"Line {idx + 1} of stream.jsonl is not valid JSON: {e}\nLine content: {line!r}")

    completed_events = [
        c for c in parsed_chunks
        if isinstance(c, dict) and c.get("type") == "response.completed"
    ]
    assert len(completed_events) >= 1, \
        f"Expected at least one `response.completed` event in stream.jsonl, got types: " \
        f"{[c.get('type') if isinstance(c, dict) else type(c).__name__ for c in parsed_chunks]}"


def test_summary_json_exists_and_valid():
    assert os.path.isfile(SUMMARY_FILE), f"summary.json not found at {SUMMARY_FILE}"

    with open(SUMMARY_FILE, "r") as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("summary.json is not valid JSON")

    assert isinstance(summary, dict), f"summary.json must be a JSON object, got: {type(summary).__name__}"

    chunk_count = summary.get("chunkCount")
    assert isinstance(chunk_count, int), \
        f"Expected 'chunkCount' in summary.json to be an integer, got: {chunk_count!r}"
    assert chunk_count >= 1, \
        f"Expected 'chunkCount' to be >= 1, got {chunk_count}"

    final_message = summary.get("finalMessage")
    assert isinstance(final_message, str), \
        f"Expected 'finalMessage' to be a string, got: {type(final_message).__name__}"
    assert final_message.strip() != "", \
        "Expected 'finalMessage' to be a non-empty string."


def test_summary_chunk_count_matches_stream_lines():
    with open(SUMMARY_FILE, "r") as f:
        summary = json.load(f)
    chunk_count = summary["chunkCount"]

    lines = _read_non_empty_lines(STREAM_FILE)
    assert chunk_count == len(lines), \
        f"summary.json chunkCount ({chunk_count}) does not match number of non-empty " \
        f"lines in stream.jsonl ({len(lines)})."
