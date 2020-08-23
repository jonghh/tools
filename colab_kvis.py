import subprocess
import matplotlib as mpl  # 기본 설정 만지는 용도
import matplotlib.font_manager as fm  # 폰트 관련 용도

def colab_kvis():
    subprocess.run(["config InlineBackend.figure_format = 'retina'"])
    subprocess.run(["apt -qq -y install fonts-nanum > /dev/null"])
    path = "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf"    # '/content/drive/My Drive/python_JH/Malgun-Gothic_29382.ttf'
    font = fm.FontProperties(fname=path, size=10)
    plt.rc('font', family=font.get_name())
    fm._rebuild()
    mpl.rcParams['axes.unicode_minus'] = False
    return print("한글 시각화 준비 완료")
