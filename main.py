
import os
import sys
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QFileDialog, QComboBox, QMessageBox)
from translator import LibreTranslateClient, TranslationError
from document_generator import save_translation_docx

LANGUAGES = {"Japanese": "ja", "Spanish": "es", "Portuguese": "pt"}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multilingual Document Translation System")
        self.setMinimumSize(520, 260)
        self.input_file = None
        self.file_label = QLabel("No file selected")
        self.language = QComboBox()
        self.language.addItems(LANGUAGES)
        browse = QPushButton("Browse for English .txt file")
        browse.clicked.connect(self.browse_file)
        translate = QPushButton("Translate and create Word document")
        translate.clicked.connect(self.translate_file)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select an English text file:"))
        layout.addWidget(browse)
        layout.addWidget(self.file_label)
        layout.addWidget(QLabel("Choose target language:"))
        layout.addWidget(self.language)
        layout.addWidget(translate)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose text file", "", "Text files (*.txt)")
        if path:
            self.input_file = Path(path)
            self.file_label.setText(str(self.input_file))

    def translate_file(self):
        if not self.input_file:
            QMessageBox.warning(self, "Missing file", "Please select a .txt file.")
            return
        try:
            text = self.input_file.read_text(encoding="utf-8")
            if not text.strip():
                raise ValueError("The selected file is empty.")
            language_name = self.language.currentText()
            target = LANGUAGES[language_name]
            client = LibreTranslateClient(
                os.getenv("LT_API_URL", "https://libretranslate.com"),
                os.getenv("LT_API_KEY", "")
            )
            translated = client.translate(text, source="en", target=target)
            output = self.input_file.with_name(f"{self.input_file.stem}_{target}.docx")
            save_translation_docx(translated, output, f"Translation to {language_name}",
                                  self.input_file.name)
            QMessageBox.information(self, "Complete", f"Saved Word document:\n{output}")
        except (OSError, ValueError, TranslationError) as exc:
            QMessageBox.critical(self, "Translation failed", str(exc))
        except Exception as exc:
            QMessageBox.critical(self, "Unexpected error", str(exc))

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
