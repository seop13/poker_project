import tkinter as tk

from poker.gui import PokerApp


def main():
    root = tk.Tk()
    PokerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
