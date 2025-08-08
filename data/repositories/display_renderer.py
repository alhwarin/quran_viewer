#data/repositories/display_renderer.py
from PyQt5.QtGui import QColor

class DisplayRenderer:
    def __init__(self, font_color=QColor(0, 0, 0), bg_color=QColor(255, 255, 255),
                 highlight_color=QColor("#FFFFAA"), font_size=24):
        self.font_color = font_color
        self.bg_color = bg_color
        self.highlight_color = highlight_color
        self.font_size = font_size
       

    def set_font_color(self, color):
        self.font_color = QColor(color) if isinstance(color, str) else color

    def get_font_color(self):
        return self.font_color

    def set_bg_color(self, color):
        self.bg_color = QColor(color) if isinstance(color, str) else color

    def get_bg_color(self):
        return self.bg_color

    def set_font_size(self, size):
        if isinstance(size, (int, float)) and size > 0:
            self.font_size = size

    def get_font_size(self):
        return self.font_size
    
    def set_highlight_color(self, color):
        self.highlight_color = QColor(color) if isinstance(color, str) else color

    def get_highlight_color(self):
        return self.highlight_color

    def html_aya(self, number, circle_stroke_width=3, decoration_stroke_width=1):
        digits = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩']
        num = ''.join(digits[int(d)] for d in str(number))
        font_color = self.font_color.name()
        font_size_px = self.font_size * 1.1
        svg_size = font_size_px * 1.5
        inner_radius = font_size_px * 0.45
        outer_radius = inner_radius * 1.3
        center = svg_size / 2
        decoration_count = 8

        def get_decoration_path(angle):
            return f"""
                <g transform="rotate({angle})">
                    <path d="
                        M 0,{-inner_radius}
                        C {inner_radius * 0.3},{-outer_radius} {inner_radius * 0.7},{-outer_radius} 0,{-outer_radius}
                        S {-inner_radius * 0.7},{-outer_radius} 0,{-inner_radius}
                        Z
                    " stroke-width="{decoration_stroke_width}"/>
                </g>
            """

        return f"""<svg width="{svg_size}" height="{svg_size}" viewBox="0 0 {svg_size} {svg_size}" xmlns="http://www.w3.org/2000/svg">
            <circle cx="{center}" cy="{center}" r="{outer_radius}" fill="transparent" stroke="{font_color}" stroke-width="1" stroke-dasharray="1,3" opacity="0.3"/>
            <circle cx="{center}" cy="{center}" r="{inner_radius}" fill="transparent" stroke="{font_color}" stroke-width="{circle_stroke_width}"/>
            <g transform="translate({center},{center})" fill="{font_color}" stroke="{font_color}">
                {''.join(get_decoration_path(i * (360 / decoration_count)) for i in range(decoration_count))}
            </g>
            <text x="{center}" y="{center}" text-anchor="middle" dominant-baseline="middle"
                  font-family="Amiri, Traditional Arabic, serif"
                  font-size="{font_size_px*0.5}" fill="{font_color}" font-weight="bold">
                {num}
            </text>
        </svg>"""

    def generate_aya_html(self, sura_id, aya_num, text):
        marker_svg = self.html_aya(aya_num)
        link = f"play-{sura_id}-{aya_num}"

        return f"""
        <span id="aya-{aya_num}" class="aya-inline">
            {text}
            <span class="aya-number">
                <a href="#" onclick="bridge.handleMarkerClick('{link}')">{marker_svg}</a>
            </span>
        </span>
        """
    def generate_css(self):
        return f"""
        <style>
        :root {{
            --highlight-color: {self.highlight_color.name()};
            --highlight-text-color: {self._calculate_contrast_color(self.highlight_color)};
            --font-size: {self.font_size}pt;
        }}
        
        body {{
            font-size: var(--font-size);
            color: {self.font_color.name()};
            background-color: {self.bg_color.name()};
            font-family: 'Scheherazade New', 'Amiri', 'Traditional Arabic', serif;
            line-height: 2.0;
            direction: rtl;
            text-align: justify;
            margin: 20px;
            padding: 10px;
            transition: all 0.3s ease;
        }}
                        /* Header styling */
        .page-header {{
            text-align: center;
            padding: 15px 0;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--gold-color);
        }}

        .sura-name {{
            font-size: 24pt;
            font-weight: bold;
            color: var(--gold-color);
            text-shadow: 1px 1px 1px rgba(0,0,0,0.1);
        }}

        /* Footer styling */
        .page-footer {{
            text-align: center;
            padding: 15px 0;
            margin-top: 20px;
            border-top: 1px solid var(--gold-color);
        }}

        .page-number {{
            font-size: 14pt;
            color: var(--gold-color);
            display: inline-block;
            padding: 0 15px;
            background-color: var(--page-color);
        }}
        .aya-inline {{
            display: inline;
            padding: 0 2px;
            transition: all 0.3s ease;
            position: relative;
            line-height: 1.8;
        }}
        
        .aya-inline.current {{
            #background-color: var(--highlight-color);
            color: var(--highlight-color);
            #color: var(--highlight-text-color);
            border-radius: 4px;
            padding: 2px 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            transform: translateY(-1px);
        }}
        
        .aya-inline.current:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        .aya-number {{
            display: inline-block;
            margin: 0 5px;
            font-size: calc(var(--font-size) * 0.8);
            color: {self._calculate_secondary_color(self.font_color)};
            user-select: none;
        }}
        
        a {{
            text-decoration: none;
            color: inherit;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        @media (max-width: 600px) {{
            body {{
                font-size: calc(var(--font-size) * 0.9);
                margin: 10px;
                padding: 5px;
            }}
        }}

        </style>
        """
    
    def _calculate_contrast_color(self, bg_color):
        """Calculate readable text color for a given background"""
        r, g, b, _ = bg_color.getRgb()
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        return QColor(0, 0, 0) if brightness > 128 else QColor(255, 255, 255)

    def _calculate_secondary_color(self, main_color):
        """Generate a subtle secondary color"""
        h, s, v, _ = main_color.getHsv()
        return QColor.fromHsv(h, int(s * 0.7), int(v * 0.8))

    def generate_html(self, page_number, sura_info_list, quran_data):

        # Start the page container
        page_html = """
        <div class="page-frame">
        """

        # Group ayas by sura_id from quran_data
        from collections import defaultdict
        sura_ayas = defaultdict(list)
        for sid, aid, text in quran_data:
            sura_ayas[sid].append((sid, aid, text))

        # Build HTML for each sura
        for sura_info in sura_info_list:
            sura_id = sura_info["id"]
            sura_name = sura_info["name"]
            # Sura header
            sura_header_html = f"""
            <div class="page-header">
                <div class="sura-name">سورة {sura_name}</div>
            </div>
            """

            # Ayas of the sura
            ayas_html = "\n".join(
                self.generate_aya_html(sid, aid, text) for sid, aid, text in sura_ayas[sura_id]
            )

            page_html += f"{sura_header_html}\n<div class='sura-block'>{ayas_html}</div>\n"

        # Page footer with page number
        footer_html = f"""
            <div class="page-footer">
                <div class="page-number">صفحة {page_number if page_number else ''}</div>
            </div>
        </div>
        """

        # Final HTML
        return f"""
        <html>
        <head>
            <meta charset="UTF-8">
            {self.generate_css()}
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
            <script>
            let bridge = null;
            let currentPlayingAya = null;

            document.addEventListener('DOMContentLoaded', function () {{
                new QWebChannel(qt.webChannelTransport, function (channel) {{
                    bridge = channel.objects.bridge;
                }});
            }});

            function highlightAya(ayaId) {{
                if (currentPlayingAya === ayaId) return;

                if (currentPlayingAya) {{
                    const prevEl = document.getElementById('aya-' + currentPlayingAya);
                    if (prevEl) {{
                        prevEl.classList.remove('current');
                    }}
                }}

                const newEl = document.getElementById('aya-' + ayaId);
                if (newEl) {{
                    newEl.classList.add('current');
                    newEl.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'center',
                        inline: 'center'
                    }});
                    currentPlayingAya = ayaId;

                    const event = new CustomEvent('ayahighlighted', {{ detail: {{ ayaId }} }});
                    document.dispatchEvent(event);
                }}
            }}

            function clearHighlight() {{
                if (!currentPlayingAya) return;
                const el = document.getElementById('aya-' + currentPlayingAya);
                if (el) {{
                    el.classList.remove('current');
                }}
                currentPlayingAya = null;
            }}

            function setHighlightColor(color) {{
                document.documentElement.style.setProperty('--highlight-color', color);
            }}

            function setFontColor(color) {{
                document.body.style.color = color;
            }}

            function setBackgroundColor(color) {{
                document.body.style.backgroundColor = color;
            }}

            function setFontSize(sizePt) {{
                document.body.style.fontSize = sizePt + 'pt';
            }}

            window.highlightAya = highlightAya;
            window.clearHighlight = clearHighlight;
            </script>
        </head>
        <body dir="rtl">
            {page_html}
            <script>
            if (window.initialAyaToHighlight) {{
                highlightAya(window.initialAyaToHighlight);
            }}
            </script>
            {footer_html}
        </body>
        </html>
        """

    
    def generate_html_new_1(self, current_page_number, get_sura_info_list_func, get_quran_data_func):
        """
        Generate HTML for multiple pages according to current page and scrolling rules.

        Args:
        current_page_number (int): The currently active page number
        get_sura_info_list_func (Callable[[int], List[Dict]]): function to get sura info list by page number
        get_quran_data_func (Callable[[int], List[Tuple[int,int,str]]]): function to get quran data by page number
        """

        total_pages = 604

        # Determine pages to render based on rules
        if current_page_number == 1:
            pages_to_render = [1, 2] if total_pages >= 2 else [1]
        elif current_page_number == total_pages:
            pages_to_render = [total_pages-1, total_pages] if total_pages > 1 else [total_pages]
        else:
            # For pages between 2 and last-1
            pages_to_render = [current_page_number-1, current_page_number, current_page_number+1]
            # Clamp values inside valid range
            pages_to_render = [p for p in pages_to_render if 1 <= p <= total_pages]

        def render_page_html(page_num):
            sura_info_list = get_sura_info_list_func(page_num)
            quran_data = get_quran_data_func(page_num)

            # Build page html same as before, but for one page only
            page_html = """
            <div class="page-frame" id="page-{page_num}">
            """.format(page_num=page_num)

            from collections import defaultdict
            sura_ayas = defaultdict(list)
            for sid, aid, text in quran_data:
                sura_ayas[sid].append((sid, aid, text))

            for sura_info in sura_info_list:
                sura_id = sura_info["id"]
                sura_name = sura_info["name"]

                sura_header_html = f"""
                <div class="page-header">
                    <div class="sura-name">سورة {sura_name}</div>
                </div>
                """

                ayas_html = "\n".join(
                    self.generate_aya_html(sid, aid, text) for sid, aid, text in sura_ayas[sura_id]
                )

                page_html += f"{sura_header_html}\n<div class='sura-block'>{ayas_html}</div>\n"

            page_html += f"""
                <div class="page-footer">
                    <div class="page-number">صفحة {page_num}</div>
                </div>
            </div>
            """
            return page_html

        all_pages_html = "\n".join(render_page_html(p) for p in pages_to_render)

        # JS to handle scrollbar position, loading prev/next pages dynamically,
        # and centering scroll on middle page after load
        middle_page_index = pages_to_render.index(current_page_number) if current_page_number in pages_to_render else 0

        js = f"""
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const container = document.getElementById('pages-container');
            const pageFrames = container.getElementsByClassName('page-frame');

            // Scroll to middle page on initial load
            if(pageFrames.length > 0) {{
            const middlePage = pageFrames[{middle_page_index}];
            middlePage.scrollIntoView({{behavior: 'auto', block: 'center'}});
            }}

            let isLoading = false;

            container.addEventListener('scroll', function() {{
            if(isLoading) return;

            const scrollTop = container.scrollTop;
            const scrollHeight = container.scrollHeight;
            const containerHeight = container.clientHeight;

            // near top: load previous pages
            if(scrollTop < 50) {{
                isLoading = true;
                // You should implement a callback to fetch x-2 page, e.g. via Qt bridge or other mechanism
                if(typeof window.loadPreviousPages === 'function') {{
                window.loadPreviousPages();
                }}
                isLoading = false;
            }}

            // near bottom: load next pages
            else if(scrollTop + containerHeight > scrollHeight - 50) {{
                isLoading = true;
                if(typeof window.loadNextPages === 'function') {{
                window.loadNextPages();
                }}
                isLoading = false;
            }}
            }});
        }});
        </script>
        """

        css = self.generate_css()

        return f"""
        <html>
        <head>
        <meta charset="UTF-8">
        {css}
        <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
        <script>
            let bridge = null;
            document.addEventListener('DOMContentLoaded', function () {{
                new QWebChannel(qt.webChannelTransport, function (channel) {{
                    bridge = channel.objects.bridge;
                }});
            }});
        </script>
        {js}
        </head>
        <body dir="rtl">
        <div id="pages-container" style="overflow-y: auto; height: 100vh;">
            {all_pages_html}
        </div>
        </body>
        </html>
        """
