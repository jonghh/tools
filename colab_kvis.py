import matplotlib
import matplotlib.font_manager as fm
def colab_kvis():
    fm.get_fontconfig_fonts()
    font_path = "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf"
    font_name = fm.FontProperties(fname=font_path).get_name()
    matplotlib.rc('font', family=font_name)
    return print("한글 폰트 시각화 준비 완료")
