# El-Dahih (v1.0.2) - Google Colab Build Script
# 1. Run this cell to install dependencies
!pip install buildozer cython==0.29.33
!sudo apt-get install -y \
    python3-pip \
    build-essential \
    git \
    python3 \
    python3-dev \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good

# 2. Upload 'mobile_app_v103.zip' to the files sidebar in Colab
# 3. Run this cell to unzip
!unzip mobile_app_v103.zip -d .

# 4. Run buildozer (Press 'y' when prompted)
!buildozer -v android debug
