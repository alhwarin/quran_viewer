#domain/entities/page_entity.py
class PageEntity:
    def __init__(self, id: int, sura_id_list: list[int], start_id: int, ayas_count: int):
        self.id = id
        self.sura_id_list = sura_id_list  # List of sura IDs on this page
        self.start_id = start_id
        self.ayas_count = ayas_count

    def first_sura_id(self) -> int:
        """Return the first sura ID on the page."""
        return self.sura_id_list[0] if self.sura_id_list else None

    def last_sura_id(self) -> int:
        """Return the last sura ID on the page."""
        return self.sura_id_list[-1] if self.sura_id_list else None
