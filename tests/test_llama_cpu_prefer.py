"""Low-VRAM hosts should download Vulkan/CPU llama-server, not CUDA."""

from spock_onboarding.runtime import _pick_linux_assets, _pick_windows_assets


def _asset(name: str) -> dict:
    return {"name": name, "browser_download_url": f"https://example.test/{name}"}


def test_windows_prefer_cpu_picks_vulkan_before_cuda():
    assets = [
        _asset("llama-b1234-bin-win-cuda-12.4-x64.zip"),
        _asset("llama-b1234-bin-win-vulkan-x64.zip"),
        _asset("llama-b1234-bin-win-cpu-x64.zip"),
        _asset("cudart-llama-bin-win-cuda-12.4-x64.zip"),
    ]
    bin_asset, cudart = _pick_windows_assets(assets, prefer_cpu=True)
    assert bin_asset["name"].endswith("bin-win-vulkan-x64.zip")
    assert cudart is None


def test_windows_default_still_prefers_cuda():
    assets = [
        _asset("llama-b1234-bin-win-cuda-12.4-x64.zip"),
        _asset("llama-b1234-bin-win-vulkan-x64.zip"),
        _asset("cudart-llama-bin-win-cuda-12.4-x64.zip"),
    ]
    bin_asset, cudart = _pick_windows_assets(assets, prefer_cpu=False)
    assert "cuda-12.4" in bin_asset["name"]
    assert cudart is not None and "cudart" in cudart["name"]


def test_linux_prefer_cpu_picks_vulkan_or_cpu_before_cuda():
    assets = [
        _asset("llama-b1234-bin-ubuntu-cuda-12.4-x64.tar.gz"),
        _asset("llama-b1234-bin-ubuntu-cpu-x64.tar.gz"),
    ]
    bin_asset, _ = _pick_linux_assets(assets, prefer_cpu=True)
    assert "cpu" in bin_asset["name"]
