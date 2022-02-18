from tkinter import *
from PIL import ImageTk, Image
window=Tk()
btn=Button(window, text="This is Button widget", fg='blue')
btn.place(x=80, y=100)
window.title('Hello Python')
window.geometry("300x200+10+10")
img = ImageTk.PhotoImage(Image.open("FirePanel.jpeg"))


Label(window,image=img).pack()
window.mainloop()