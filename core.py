import requests
from pathlib import Path


def get_image_url(api_key: str):
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data: dict = response.json()
        image_url: str = data["url"]
        return image_url
    except requests.exceptions.HTTPError as e:
        print(e)
        return None


def image_download(image_url: str, save_path: Path):
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        with open(save_path, "wb") as f:
            f.write(response.content)
        return True

    except requests.exceptions.HTTPError as e:
        print(e)
        return False


def main():
    api_key: str = "my_api_key"
    image_url = get_image_url(api_key)
    if image_url:
        image_dir = Path.home() / "Pictures" / "NASA_Daily_BG"
        image_dir.mkdir(parents=True, exist_ok=True)
        image_path = image_dir / "nasa_daily.jpg"
        if image_download(image_url, image_path):
            print(f"image downloaded successfully to {image_path}")
        else:
            print(f"image download failed")
    else:
        print("failed to get image URL")


main()
