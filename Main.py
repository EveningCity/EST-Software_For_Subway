import sys
import window.Main as Main

from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    Dialog = Main.main()
    Dialog.show()
    sys.exit(app.exec_())