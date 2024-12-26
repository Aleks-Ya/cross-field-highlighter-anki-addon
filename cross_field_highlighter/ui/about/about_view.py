import logging
from logging import Logger

from aqt.qt import QDialog, QLabel, QVBoxLayout, QDialogButtonBox, QPushButton, QUrl, QDesktopServices, QWidget
from aqt import utils, Qt, QFont

from ...config.settings import Settings
from ...config.url_manager import UrlManager, UrlType, URL

log: Logger = logging.getLogger(__name__)


class AboutView(QDialog):

    def __init__(self, parent: QWidget, url_manager: UrlManager, desktop_services: QDesktopServices,
                 settings: Settings):
        super().__init__(parent=parent)
        self.__url_manager: UrlManager = url_manager
        self.__settings: Settings = settings
        self.__desktop_services: QDesktopServices = desktop_services

        self.__button_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        # noinspection PyUnresolvedReferences
        self.__button_box.accepted.connect(self.__finished)

        title_label: QLabel = QLabel('"Cross-Field Highlighter" Anki addon')
        font: QFont = title_label.font()
        font.setBold(True)
        font.setPointSize(int(font.pointSize() * 1.5))
        title_label.setFont(font)
        title_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        version_label: QLabel = QLabel(f'Version: {settings.version}')
        version_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        addon_info_page_label: QLabel = self.__get_link_label(
            UrlType.ADDON_INFO_PAGE, "Addon info page", " (rate addon here)")
        support_thread_label: QLabel = self.__get_link_label(
            UrlType.SUPPORT_THREAD, "Support thread in Anki Forum", " (for questions, suggestions, bugs)")
        changelog_label: QLabel = self.__get_link_label(UrlType.CHANGELOG, "Changelog", "")
        cases_label: QLabel = self.__get_link_label(UrlType.CASES, "Test cases", "")
        github_label: QLabel = self.__get_link_label(UrlType.GITHUB, "GitHub", "")
        sonar_qube_label: QLabel = self.__get_link_label(UrlType.SONAR_QUBE, "SonarQube", "")

        open_log_file_button: QPushButton = QPushButton("Open log file")
        open_log_file_button.setFixedWidth(open_log_file_button.sizeHint().width())
        open_log_file_button.setFixedHeight(open_log_file_button.sizeHint().height() + 2)
        # noinspection PyUnresolvedReferences
        open_log_file_button.clicked.connect(self.__on_open_log_file_click)

        open_addon_folder_button: QPushButton = QPushButton("Open addon folder")
        open_addon_folder_button.setFixedWidth(open_addon_folder_button.sizeHint().width())
        open_addon_folder_button.setFixedHeight(open_addon_folder_button.sizeHint().height() + 2)
        # noinspection PyUnresolvedReferences
        open_addon_folder_button.clicked.connect(self.__on_open_addon_folder_click)

        layout: QVBoxLayout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(version_label)
        layout.addSpacing(10)
        layout.addWidget(addon_info_page_label)
        layout.addWidget(support_thread_label)
        layout.addWidget(changelog_label)
        layout.addWidget(cases_label)
        layout.addWidget(github_label)
        layout.addWidget(sonar_qube_label)
        layout.addSpacing(10)
        layout.addWidget(open_log_file_button)
        layout.addWidget(open_addon_folder_button)
        layout.addWidget(self.__button_box)

        self.setLayout(layout)
        self.resize(300, 200)

        # noinspection PyUnresolvedReferences
        self.finished.connect(self.__finished)

        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_view(self) -> None:
        log.debug("Show view")
        # noinspection PyUnresolvedReferences
        self.setWindowTitle("About")
        # noinspection PyUnresolvedReferences
        self.show()
        self.__button_box.setFocus()
        self.adjustSize()

    def __finished(self) -> None:
        log.info("Dialog closed")
        self.hide()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __get_link_label(self, url_type: UrlType, anchor_text: str, comment: str) -> QLabel:
        url: URL = self.__url_manager.get_url(url_type)
        link: str = f'<a href="{url}">{anchor_text}</a>{comment}'
        label: QLabel = QLabel(link)
        label.setOpenExternalLinks(True)
        return label

    def __on_open_log_file_click(self) -> None:
        log_file: str = str(self.__settings.logs_folder / "cross_field_highlighter.log")
        log.debug(f"Opening log file: {log_file}")
        # noinspection PyArgumentList
        url: QUrl = QUrl.fromLocalFile(log_file)
        self.__desktop_services.openUrl(url)

    def __on_open_addon_folder_click(self) -> None:
        module_dir: str = str(self.__settings.module_dir)
        log.debug(f"Opening addon folder: {module_dir}")
        utils.openFolder(module_dir)

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
