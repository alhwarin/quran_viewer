
def test_update_display():
    class MockRenderer:
        def generate_html(self, sura_id, data):
            return "<html>content</html>"

    use_case = UpdateDisplaySettingsUseCase(MockRenderer())
    html = use_case.execute(1, [(1, "Aya")])
    assert html.startswith("<html>")

def test_play_audio():
    class MockAudioPlayer:
        def load_playlist(self, sura_id, reciter): return True
        def play(self): self.played = True
        def __init__(self): self.played = False; self.playlist = type("pl", (), {"setCurrentIndex": lambda s, i: None})()

    player = MockAudioPlayer()
    use_case = PlayAudioUseCase(player)
    use_case.execute(1, "reciter")
    assert player.played