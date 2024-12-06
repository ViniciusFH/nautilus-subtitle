import sys
import PySimpleGUI as sg
import helpers as H


class Interface():
    def __init__(self) -> None:

        self.languages = {
            "Inglês": "en",
            "Português (br)": "pt-BR",
            "Espanhol": "es"
        }
        self.langOpts = list(self.languages.keys())
        self.selectedLanguage = ""
        self.selectedLangVal = ""

    def getLangVal(self, langName: str) -> str:
        return self.languages[langName]

    def showOptions(self, options, text, size=30):
        layout = [[sg.Text(text)],
                  [sg.Listbox(values=options, size=(
                      size, len(options)), key="options")],
                  [sg.Button("Ok"), sg.Button("Cancelar")]]

        window = sg.Window("Nautilus Subtitle", layout)

        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Cancelar":
            sys.exit()

        window.close()

        return values["options"][0]

    def selectLanguage(self) -> str:

        selectedOption = self.showOptions(self.langOpts, "Selecione a língua:")

        self.selectedLanguage = selectedOption
        self.selectedLangVal = self.getLangVal(selectedOption)

    def selectSub(self, subs):
        subsNames = H.parseSubNames(subs)

        selectedSubName = self.showOptions(subsNames, "Selecione a legenda:", 60)

        selectedSub = H.findDictByValue(subs, "file_name", selectedSubName)
        
        return selectedSub

    def infoMessage(self, message: str) -> None:
        wide = len(message)
        layout = [[sg.Text(message, size=(wide, 1))]]
        window = sg.Window("Mensagem", layout, no_titlebar=True,
                           auto_close=True, auto_close_duration=1)
        window.read()
