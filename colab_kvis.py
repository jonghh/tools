import subprocess
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
def colab_kvis():
    subprocess.run(["apt-get", "install", "fonts-nanum*"])
    path = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'
    font = fm.FontProperties(fname=path, size=12)
    plt.rc('font', family=font.get_name())
    fm._rebuild()
    matplotlib.rcParams['axes.unicode_minus'] = False
