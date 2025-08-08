import os
import json
import sqlite3
from domain.entities.sura_entity import SuraEntity
from domain.entities.page_entity import PageEntity
from domain.entities.reciter_entity import ReciterEntity
from typing import List, Tuple
from typing import Optional

class QuranLocalDataSource:
    def __init__(self, config_path='../config/config.json'):
        self.config_path = config_path
        self.config = self._load_config()
        self.db_file = self.config.get('database_name', 'quran.db')

    def _load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {"database_name": "quran.db"}
        return {"database_name": "quran.db"}



    def get_aya_list(self, sura_id):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("SELECT aya_id FROM Ayas WHERE sura_id=? ORDER BY aya_id", (sura_id,))
        ayas = cur.fetchall()
        conn.close()
        return [aid[0] for aid in ayas]

    def get_quran_text(self, sura_id, aya_id=None):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        if aya_id and aya_id != 0:
            cur.execute("SELECT aya_id, Text FROM Ayas WHERE sura_id=? AND aya_id=?", (sura_id, aya_id))
        else:
            cur.execute("SELECT aya_id, Text FROM Ayas WHERE sura_id=? ORDER BY aya_id", (sura_id,))
        data = cur.fetchall()
        conn.close()
        return data

    def _connect_db(self):
        return sqlite3.connect(self.db_file)


    def get_page_info(self, page_num: int) -> Optional[PageEntity]:
        conn = self._connect_db()
        cur = conn.cursor()

        # Correct column names based on your JSON
        cur.execute("SELECT page, sura_ids, start_id, ayas_count FROM pages WHERE page = ?", (page_num,))
        row = cur.fetchone()
        conn.close()

        if row:
            page_id = row[0]
            sura_ids_str = row[1]  # e.g., "112,113,114"
            start_id = row[2]
            ayas_count = row[3]

            # Convert to list of integers
            sura_id_list = [int(s.strip()) for s in sura_ids_str.split(",") if s.strip().isdigit()]

            return PageEntity(
                id=page_id,
                sura_id_list= sura_id_list,
                start_id= start_id,
                ayas_count= ayas_count
            )

        return None


    def get_quran_text_range(self, sura_id, start_aya, count):
        conn = self._connect_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT aya_id, text FROM Ayas WHERE sura_id=? AND aya_id>=? ORDER BY aya_id LIMIT ?",
            (sura_id, start_aya, count)
        )
        rows = cur.fetchall()
        conn.close()
        return rows
    

    def get_first_page_for_sura(self, sura_id: int) -> Optional[PageEntity]:
        """
        Returns the first PageEntity where the given sura_id is included in the sura_ids field.
        Assumes 'sura_ids' is a comma-separated string like '2,3,4'.
        """
        query = """
            SELECT page, sura_ids, start_id, ayas_count
            FROM pages
            ORDER BY page ASC
        """

        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()

            for row in rows:
                sura_ids_str = row["sura_ids"]
                sura_id_list = [int(s.strip()) for s in sura_ids_str.split(",") if s.strip().isdigit()]

                if sura_id in sura_id_list:
                    return PageEntity(
                        id=row["page"],
                        sura_id_list=sura_id_list,
                        start_id=row["start_id"],
                        ayas_count=row["ayas_count"]
                    )

        return None




    def fetch_page_text(self, page: PageEntity) -> List[Tuple[int, int, str]]:
        """
        Fetch ayas starting from a specific (sura_id, aya_id), using global Quranic ID order.
        Returns ayas as a list of (sura_id, aya_id, text) tuples.
        """
        query = """
            SELECT sura_id, aya_id, text
            FROM Ayas
            WHERE id >= (
                SELECT id FROM Ayas WHERE sura_id = ? AND aya_id = ?
            )
            ORDER BY id
            LIMIT ?
        """

        try:
            with self._connect_db() as conn:
                cur = conn.cursor()
                start_sura_id = page.sura_id_list[0] if page.sura_id_list else None
                print(f"page.id: {page.id} start_sura_id: {start_sura_id} aya_id: {page.start_id} ayas_count: {page.ayas_count}")

                if start_sura_id is None:
                    raise ValueError("PageEntity.sura_id_list is empty or missing.")

                cur.execute(query, (start_sura_id, page.start_id, page.ayas_count))
                result = cur.fetchall()
                return result

        except (sqlite3.Error, ValueError) as e:
            print(f"Error while fetching page text: {e}")
            return []


    def get_sura_info(self, sura_id: int):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Suras WHERE id = ?", (sura_id,))
        row = cur.fetchone()
        return dict(zip([col[0] for col in cur.description], row)) if row else None

    def get_sura_list(self) -> List[SuraEntity]:
        """Fetch all suras and convert them into SuraEntity objects."""
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Suras ORDER BY id")
        rows = cur.fetchall()
        conn.close()

        return [
            SuraEntity(
                id=row[0],
                ayas=row[1],
                start=row[2],
                name=row[3],
                ename=row[4]
            )
            for row in rows
        ]
    

    def get_page_list(self) -> List[PageEntity]:
        """Fetch all pages and convert them into PageEntity objects."""
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("SELECT page, start_id, ayas_count, sura_ids FROM Pages ORDER BY page")
        rows = cur.fetchall()
        conn.close()

        return [
            PageEntity(
                id=row[0],
                start_id=row[1],
                ayas_count=row[2],
                sura_id_list=[int(sid) for sid in row[3].split(',')]
            )
            for row in rows
        ]
    

    def get_reciter_list(self) -> List[ReciterEntity]:
        """Fetch all reciters and convert them into ReciterEntity objects."""
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Reciters ORDER BY id")
        rows = cur.fetchall()
        conn.close()

        return [
            ReciterEntity(
                id=row[0],
                name=row[1],
                ename=row[2],
                key=row[3]
            )
            for row in rows
        ]


    def get_audio_playlist_by_range(self, first_sura, first_aya, last_sura, last_aya, reciter):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        base_folder = "C:\\Flutter\\Quran\\quran_data\\audio\\"
        table_name = f"Audio_{reciter}"

        try:
            # Get all ayas in the range [first_sura:aya .. last_sura:aya], ordered
            cur.execute("""
                SELECT sura_id, aya_id
                FROM Ayas
                WHERE (sura_id > ? OR (sura_id = ? AND aya_id >= ?))
                AND (sura_id < ? OR (sura_id = ? AND aya_id <= ?))
                ORDER BY sura_id, aya_id
            """, (first_sura, first_sura, first_aya, last_sura, last_sura, last_aya))
            aya_list = cur.fetchall()
            playlist = []
            for sura_id, aya_id in aya_list:
                cur.execute(f"""
                    SELECT audio_url
                    FROM '{table_name}'
                    WHERE sura_id = ? AND aya_id = ?
                """, (sura_id, aya_id))
                row = cur.fetchone()
                if row:
                    audio_url = row[0]
                    if audio_url.startswith(('http://', 'https://')):
                        full_path = audio_url
                    elif os.path.isabs(audio_url):
                        full_path = audio_url
                    else:
                        full_path = os.path.join(base_folder, audio_url)
                    playlist.append((sura_id, aya_id, full_path))
                else:
                    print(f"[WARN] No audio found for {sura_id}:{aya_id}")

            return playlist

        except sqlite3.Error as e:
            print(f"[ERROR] SQLite error in get_audio_playlist_by_range: {e}")
            return []

        finally:
            conn.close()



    def get_sura_playlist(self, sura_id, reciter):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        try:
            # Get the first and last aya of the sura
            cur.execute("""
                SELECT MIN(aya_id), MAX(aya_id)
                FROM Ayas
                WHERE sura_id = ?
            """, (sura_id,))
            result = cur.fetchone()
            if not result:
                return []

            first_aya, last_aya = result
            print(f"first_aya: {first_aya} last_aya: {last_aya}")
            return self.get_audio_playlist_by_range(sura_id, first_aya, sura_id, last_aya, reciter)

        except sqlite3.Error as e:
            print(f"[ERROR] in get_sura_playlist: {e}")
            return []
        finally:
            conn.close()


    def get_page_playlist(self, page_number, reciter):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()

        try:
            # Get page metadata
            cur.execute("""
                SELECT sura_id, aya_id, ayas_count
                FROM pages
                WHERE page = ?
            """, (page_number,))
            result = cur.fetchone()
            if not result:
                return []

            start_sura, start_aya, ayas_count = result

            # Get the last aya for the page
            cur.execute("""
                SELECT sura_id, aya_id
                FROM Ayas
                WHERE (sura_id > ?) OR (sura_id = ? AND aya_id >= ?)
                ORDER BY sura_id, aya_id
                LIMIT ?
            """, (start_sura, start_sura, start_aya, ayas_count))
            aya_rows = cur.fetchall()
            if not aya_rows:
                return []

            end_sura, end_aya = aya_rows[-1]

            return self.get_audio_playlist_by_range(start_sura, start_aya, end_sura, end_aya, reciter)

        except sqlite3.Error as e:
            print(f"[ERROR] in get_page_playlist: {e}")
            return []
        finally:
            conn.close()
