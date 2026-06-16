from app_store.systemd import podman_build


def test_podman_build_passes_build_args(monkeypatch):
    calls = []

    def fake_run(cmd, check):
        calls.append((cmd, check))

    monkeypatch.setattr("subprocess.run", fake_run)

    podman_build(
        "localhost/johnaic/vllm:0.6.2",
        "/tmp/vllm",
        [["APP_VERSION", "0.6.2"]],
    )

    assert calls == [
        (
            [
                "podman",
                "build",
                "-t",
                "localhost/johnaic/vllm:0.6.2",
                "--no-cache",
                "--build-arg",
                "APP_VERSION=0.6.2",
                "/tmp/vllm",
            ],
            True,
        )
    ]
