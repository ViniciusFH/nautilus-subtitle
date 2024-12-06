#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os

home = os.path.expanduser('~')
sys.path.insert(1, home + '/.nautilus-subtitles')

from opensubtitles import OpenSubtitles
from interface import Interface
import helpers as H

OpSub = OpenSubtitles()
I = Interface()


def main():
    I.selectLanguage()
    I.infoMessage(f"Procurando legendas em {I.selectedLanguage}")

    OpSub.setInterface(I)
    OpSub.setLanguage(I.selectedLangVal)
    OpSub.setVideoInfo(H.getVideoInfo())
    OpSub.hashVideo()

    subtitles = OpSub.query()

    if len(subtitles) == 0:
        I.infoMessage("Legenda não encontrada!")
        sys.exit()

    I.infoMessage(f"Encontrei {len(subtitles)} legenda(s)")

    selectedSub = I.selectSub(subtitles)

    OpSub.downloadSelectedSub(selectedSub)

    sys.exit()


main()
