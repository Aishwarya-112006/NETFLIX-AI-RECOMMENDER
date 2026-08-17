import os
import gdown

def download_models():

    files = {
        "movie_list.pkl": "1xYahoNJmSL2jJmEY0M91MngWz8slv1-h",
        "similarity.pkl": "190VD3AnaY09CpxP_VXTxKtFCzv01hjwy"
    }

    for filename, file_id in files.items():

        if not os.path.exists(filename):

            print(f"Downloading {filename}...")

            url = f"https://drive.google.com/uc?id={file_id}"

            gdown.download(
                url,
                filename,
                quiet=False
            )

            print(f"{filename} downloaded successfully!")

        else:

            print(f"{filename} already exists.")