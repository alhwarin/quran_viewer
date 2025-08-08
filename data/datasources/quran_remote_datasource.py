import requests
from typing import List, Optional
from domain.entities.sura_entity import SuraEntity
from domain.entities.page_entity import PageEntity


class QuranRemoteDataSource:
    BASE_URL = "https://api.alquran.cloud/v1"

    def __init__(self, edition: str = "ar.alafasy"):
        self.edition = edition

    def get_sura_list(self) -> List[SuraEntity]:
        """Fetch the list of surahs."""
        try:
            response = requests.get(f"{self.BASE_URL}/surah")
            response.raise_for_status()
            suras = response.json()["data"]
            return [
                SuraEntity(
                    id=sura["number"],
                    ayas=sura["numberOfAyahs"],
                    start=0,  # No offset info from API
                    name=sura["name"],
                    ename=sura["englishName"]
                )
                for sura in suras
            ]
        except Exception as e:
            print(f"Error fetching sura list: {e}")
            return []

    def get_aya_list(self, sura_id: int) -> List[int]:
        """Get list of ayah numbers in a surah."""
        try:
            response = requests.get(f"{self.BASE_URL}/surah/{sura_id}")
            response.raise_for_status()
            ayahs = response.json()["data"]["ayahs"]
            return [ayah["numberInSurah"] for ayah in ayahs]
        except Exception as e:
            print(f"Error fetching aya list for sura {sura_id}: {e}")
            return []

    def get_quran_text(self, sura_id: int, aya_id: Optional[int] = None) -> List[tuple]:
        """Get Quran text for a full sura or a single ayah."""
        try:
            if aya_id and aya_id != 0:
                response = requests.get(f"{self.BASE_URL}/ayah/{sura_id}:{aya_id}")
                response.raise_for_status()
                ayah = response.json()["data"]
                return [(ayah["numberInSurah"], ayah["text"])]
            else:
                response = requests.get(f"{self.BASE_URL}/surah/{sura_id}/{self.edition}")
                response.raise_for_status()
                ayahs = response.json()["data"]["ayahs"]
                return [(a["numberInSurah"], a["text"]) for a in ayahs]
        except Exception as e:
            print(f"Error fetching quran text for sura {sura_id}: {e}")
            return []

    def get_audio_url(self, sura_id: int, aya_id: int, reciter: Optional[str] = None) -> Optional[str]:
        """Get audio URL for a specific ayah."""
        reciter_edition = reciter if reciter else self.edition
        try:
            response = requests.get(f"{self.BASE_URL}/ayah/{sura_id}:{aya_id}/{reciter_edition}")
            response.raise_for_status()
            return response.json()["data"]["audio"]
        except Exception as e:
            print(f"Error fetching audio for {sura_id}:{aya_id}: {e}")
            return None

    def get_sura_playlist(self, sura_id: int, reciter: Optional[str] = None) -> List[tuple]:
        """Get audio playlist for a whole surah."""
        reciter_edition = reciter if reciter else self.edition
        try:
            response = requests.get(f"{self.BASE_URL}/surah/{sura_id}/{reciter_edition}")
            response.raise_for_status()
            ayahs = response.json()["data"]["ayahs"]
            # Not all ayahs have 'audio' key. Check before accessing.
            playlist = []
            for a in ayahs:
                audio_url = a.get("audio")
                if audio_url:
                    playlist.append((a["numberInSurah"], audio_url))
            return playlist
        except Exception as e:
            print(f"Error fetching audio playlist for sura {sura_id}: {e}")
            return []

    def get_reciters(self) -> List[str]:
        """Get list of available audio reciters."""
        try:
            response = requests.get(f"{self.BASE_URL}/edition?format=audio&type=versebyverse")
            response.raise_for_status()
            editions = response.json()["data"]
            return [e["identifier"] for e in editions]
        except Exception as e:
            print(f"Error fetching reciters: {e}")
            return []

    def get_page_info(self, page_num: int) -> Optional[PageEntity]:
        """Page info not supported by this API."""
        return None

    def get_ayas_for_page(self, current_page: int) -> List[int]:
        """Not supported by this API."""
        return []

    def get_quran_text_range(self, sura_id: int, start_aya: int, count: int) -> List[tuple]:
        """Get a range of ayahs from a sura."""
        all_ayahs = self.get_quran_text(sura_id)
        # Defensive slice: ensure indices are valid
        start_index = max(start_aya - 1, 0)
        end_index = start_index + count
        return all_ayahs[start_index:end_index]

    def get_first_page_for_sura(self, sura_id: int):
        """Not supported, return default."""
        return 1

    def get_sura_info(self, sura_id: int) -> Optional[dict]:
        """Get metadata about a sura."""
        try:
            response = requests.get(f"{self.BASE_URL}/surah/{sura_id}")
            response.raise_for_status()
            data = response.json()["data"]
            return {
                "id": data["number"],
                "name": data["name"],
                "englishName": data["englishName"],
                "numberOfAyahs": data["numberOfAyahs"],
                "revelationType": data["revelationType"]
            }
        except Exception as e:
            print(f"Error fetching sura info: {e}")
            return None

    def get_sura_list_1(self) -> List[int]:
        """Helper to get list of sura IDs."""
        return [s.id for s in self.get_sura_list()]
