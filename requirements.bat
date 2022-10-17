echo "Please make sure you had already done for these things:"
echo "Install CUDA and CUDNN"
echo "Run all of these in Anaconda enviroment"
echo "install pytorch -version==1.10.0"
echo "Choose the Commend by CUDA version"
echo "# CUDA 10.2"
echo "conda install pytorch==1.10.0 torchvision==0.11.0 torchaudio==0.10.0 cudatoolkit=10.2 -c pytorch"
echo "# CUDA 11.3"
echo "conda install pytorch==1.10.0 torchvision==0.11.0 torchaudio==0.10.0 cudatoolkit=11.3 -c pytorch -c conda-forge"
echo "# CPU Only"
echo "conda install pytorch==1.10.0 torchvision==0.11.0 torchaudio==0.10.0 cpuonly -c pytorch"
echo ""
echo "download yolov5 and put in same dir, rename to \'yolov5\'"

pause

mkdir video
pip install beautifulsoup4
pip install requests
pip install html5lib
pip install imutils
pip install pandas
pip install yaml
pip install tqdm
pip install matplotlib
pip install seaborn
pip install psutil