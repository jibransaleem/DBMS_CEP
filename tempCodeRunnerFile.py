def show():
    folder_path = r'C:\Users\Z.S computers\Desktop\flask\cep\static\img'
    img =  os.listdir(folder_path)
    return render_template("xyz.html", data  = img)
