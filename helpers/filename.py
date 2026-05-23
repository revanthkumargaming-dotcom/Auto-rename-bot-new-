REMOVE_TAGS = [
    "www.",
    "@channel",
    "YTS",
    "RARBG",
    ".com",
    ".in"
]


# CLEAN FILE NAME
def clean_filename(name):

    for tag in REMOVE_TAGS:

        name = name.replace(tag, "")

    return name.strip()


# DETECT QUALITY
def detect_quality(name):

    quality = ""

    if "2160" in name:
        quality = "2160p"

    elif "1440" in name:
        quality = "1440p"

    elif "1080" in name:
        quality = "1080p"

    elif "720" in name:
        quality = "720p"

    elif "480" in name:
        quality = "480p"

    return quality


# DETECT CODEC
def detect_codec(name):

    codec = ""

    if "x265" in name.lower():
        codec = "x265"

    elif "x264" in name.lower():
        codec = "x264"

    elif "hevc" in name.lower():
        codec = "HEVC"

    return codec
