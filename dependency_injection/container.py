class ServiceContainer:
    def __init__(self):
        # Infrastructure
        from data.repositories.quran_repository_impl import QuranRepositoryImpl
        from data.repositories.audio_player_repository_impl import AudioPlayerImpl

        # Use Cases
        from domain.use_cases.play_audio_use_case import PlayAudioUseCase
        from domain.use_cases.load_quran_page_use_case import LoadQuranPageUseCase
        from domain.use_cases.update_display_settings_use_case import UpdateDisplaySettingsUseCase
        from domain.use_cases.get_data_list_use_case import GetDataListUseCase

        # Presentation Layer (Controllers, Events)
        from presentation.controllers.quran_viewer_controller import QuranViewerController
        from presentation.controllers.audio_player_controller import AudioPlayerController
        from presentation.events.event_dispatcher import QuranEventDispatcher

        # State
        from presentation.states.quran_state import QuranState

        # Initialize core services
        self.quran_state = QuranState()
        self.repository = QuranRepositoryImpl("config/config.json")
        #self.text_renderer_repository_impl = DisplayRendererRepositoryImpl()
        self.audio_player = AudioPlayerImpl(self.repository.model, self.quran_state)

        # Use Cases
        self.play_audio_uc = PlayAudioUseCase(self.audio_player, self.quran_state)
        self.load_page_uc = LoadQuranPageUseCase(self.repository)
        self.display_update_uc = UpdateDisplaySettingsUseCase(self.repository)
        self.get_data_list_uc = GetDataListUseCase( self.repository)

        # Event Dispatcher
        self.event_dispatcher = QuranEventDispatcher()

        # Controllers (defer QuranViewerController init with web_view via lambda)
        self.quran_viewer_controller = QuranViewerController(
            load_page_uc=self.load_page_uc,
            quran_state=self.quran_state,
            get_data_list_uc = self.get_data_list_uc,
            display_update_uc=self.display_update_uc
        )
        self.event_dispatcher.event_emitted.connect(self.quran_viewer_controller.handle_event)
        self.audio_player_controller = AudioPlayerController(
            self.audio_player,
            self.quran_state
        )
        self.event_dispatcher.event_emitted.connect(self.audio_player_controller.handle_event)
    def get_gui(self):
        from presentation.views.quran_viewer_screen import QuranViewerScreen

        return QuranViewerScreen(
            event_dispatcher=self.event_dispatcher,
            quran_state=self.quran_state
        )
