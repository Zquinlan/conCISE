---
layout: posts
    # classes: wide
sidebar:
    nav: "Documentation"
---
# Graphical User Interface
## Classes:
- emittingStream
- mainWindow

## emittingStream
This is a QObject which excepts pyqtSignals and can emit the signal into text. This allows us to capture any messages sent to the console and write it to the text box in the GUI itself.

## mainWindow
Main window of the widget which will start the threading of concise through workflow runner and allow us to capture the print() exports in the workflow directly to the GUI text box.