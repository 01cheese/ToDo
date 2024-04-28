import tkinter as tk
from tkinter import colorchooser, filedialog, Scale
from PIL import Image, ImageDraw
import asyncio
import multiprocessing


class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple paint")

        # Создаем холст
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Настройка инструментов
        self.color = 'black'
        self.brush_size = 5
        self.brush_type = tk.ROUND

        # Привязка событий
        self.canvas.bind('<B1-Motion>', self.paint)

        # Создаем меню
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Save', command=self.save_image)
        file_menu.add_command(label='Clean', command=self.clear_canvas)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.root.quit)

        settings_menu = tk.Menu(menu)
        menu.add_cascade(label='Setting', menu=settings_menu)
        settings_menu.add_command(label='Choice color', command=self.choose_color)

    def paint(self, event):
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
        self.canvas.create_line(x1, y1, x2, y2, fill=self.color, width=self.brush_size * 2, capstyle=self.brush_type,
                                smooth=True)

    def choose_color(self):
        self.color = colorchooser.askcolor(color=self.color)[1]

    def clear_canvas(self):
        self.canvas.delete('all')

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()

            # Создаем изображение с белым фоном
            image = Image.new("RGB", (self.canvas.winfo_width(), self.canvas.winfo_height()), "white")
            draw = ImageDraw.Draw(image)

            # Рисуем на изображении линии, соответствующие линиям на холсте
            for item in self.canvas.find_all():
                x1, y1, x2, y2 = self.canvas.coords(item)
                draw.line((x1, y1, x2, y2), fill=self.color, width=self.brush_size * 2)

            image.save(file_path, "PNG")


def run_app():
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()

def main():
    # Запуск Tkinter-приложения в отдельном процессе
    process = multiprocessing.Process(target=run_app)
    process.start()
    process.join()  # Добавьте эту строку, чтобы основной процесс ждал завершения Tkinter-приложения

if __name__ == '__main__':
    main()
