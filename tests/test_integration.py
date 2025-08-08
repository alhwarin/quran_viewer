def test_integration_load_and_play():
    class FakeRepo:
        def get_sura_list(self): return [1]
        def get_sura_playlist(self, s, r): return [(1, "/path/to/audio.mp3")]
        def get_page_playlist(self, p, r): return [(1, "/path/to/audio.mp3")]
        def get_quran_text(self, s, a): return [(1, "Some aya")]

    class FakeRenderer:
        def set_font_size(self, size): pass
        def generate_html(self, s, d): return "<html></html>"
        def renderer(self): return self
        def get_font_color(self): pass
        def get_bg_color(self): pass
        def get_highlight_color(self): pass
        def set_font_color(self, c): pass
        def set_bg_color(self, c): pass
        def set_highlight_color(self, c): pass

    class FakeAudio:
        def __init__(self): self.volume = 0; self.played = False; self.stopped = False
        def load_playlist(self, sid, r): return True
        def play(self): self.played = True
        def stop(self): self.stopped = True
        def set_volume(self, v): self.volume = v

    repo = FakeRepo()
    renderer = FakeRenderer()
    audio = FakeAudio()
    from domain.use_cases.play_audio_use_case import PlayAudioUseCase
    #from domain.use_cases.load_quran_text_use_case import LoadQuranTextUseCase
    from domain.use_cases.update_display_settings_use_case import UpdateDisplaySettingsUseCase

    play = PlayAudioUseCase(audio)
    #load = LoadQuranTextUseCase(repo)
    display = UpdateDisplaySettingsUseCase(renderer)

    #assert load.execute(1) == [(1, "Some aya")]
    html = display.execute(1, [(1, "Some aya")])
    assert html.startswith("<html>")
    play.execute(1, "TestReciter")
    assert audio.played
