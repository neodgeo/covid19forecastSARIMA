def getData():
    import subprocess

    try:
        subprocess.check_output(["rm -rf COVID-19"],shell=True)
        subprocess.check_output(["git clone https://github.com/CSSEGISandData/COVID-19.git"], shell=True)
    except subprocess.CalledProcessError as e:
        return 'an error occured while trying to get covid data'
    
    return True