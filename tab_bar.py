# Scrolling tab bar with virtual layout and shift.
#
# Example with 7-cell display, tabs "abc" and "def":
#   Tab 1 selected: abc de…
#   Tab 2 selected: …bc def

import re
from kitty.tab_bar import as_rgb, draw_title
from kitty.utils import color_as_int

_title_widths: list[int] = []
_active_idx: int = 0
_shift: int = 0
_GAP = 1
_rendered_titles: list[str] = []
_sgr_re = re.compile(r'\x1b\[[^m]*m')


def _virtual_start(idx):
    return sum(_title_widths[:idx]) + idx * _GAP


def _compute_shift(columns):
    global _shift
    n = len(_title_widths)
    total = sum(_title_widths) + max(0, n - 1) * _GAP
    if total <= columns:
        _shift = 0
        return
    a_start = _virtual_start(_active_idx)
    a_end = a_start + _title_widths[_active_idx]
    if a_end > _shift + columns:
        _shift = a_end - columns
    if a_start < _shift:
        _shift = a_start


def draw_tab(draw_data, screen, tab, before, max_tab_length, index, is_last, extra_data):
    global _title_widths, _active_idx, _shift, _rendered_titles
    idx = index - 1

    if extra_data.for_layout:
        if idx == 0:
            _title_widths = []
            _active_idx = 0
            _rendered_titles = []
        # Measure by drawing with full width
        start_x = screen.cursor.x
        draw_title(draw_data, screen, tab, index, screen.columns)
        _title_widths.append(screen.cursor.x - start_x)
        # Capture the rendered plain text for left-clipping
        # We re-render to get the string (draw_title doesn't return it)
        # Use tab.title as fallback — it won't include template formatting
        _rendered_titles.append(tab.title)
        if tab.is_active:
            _active_idx = idx
        if is_last:
            _compute_shift(screen.columns)
        screen.cursor.x = before + 1
        return screen.cursor.x

    # --- Draw pass ---
    if idx >= len(_title_widths):
        return screen.cursor.x

    v_start = _virtual_start(idx)
    v_end = v_start + _title_widths[idx]
    d_start = v_start - _shift
    d_end = v_end - _shift

    # Off-screen
    if d_end <= 0 or d_start >= screen.columns:
        screen.cursor.x = min(screen.cursor.x, screen.columns - 1)
        return screen.cursor.x

    if d_start >= 0 and d_end <= screen.columns:
        # Fully visible — use draw_title for proper template rendering
        screen.cursor.x = d_start
        draw_title(draw_data, screen, tab, index, _title_widths[idx])
    elif d_start < 0:
        # Left-clipped: …[trailing chars of title]
        screen.cursor.x = 0
        visible = min(d_end, screen.columns)
        if visible <= 1:
            screen.draw('…')
        else:
            chars_to_show = visible - 1  # 1 cell for …
            title = tab.title
            suffix = title[-chars_to_show:] if len(title) > chars_to_show else title
            screen.draw('…')
            screen.draw(suffix)
            screen.cursor.x = visible
    else:
        # Right-clipped: [leading chars]…
        screen.cursor.x = d_start
        available = screen.columns - d_start
        if available <= 1:
            screen.draw('…')
        else:
            # Draw title capped to (available - 2) then append …
            draw_title(draw_data, screen, tab, index, max(1, available - 2))
            # Place … before the last cell
            screen.cursor.x = screen.columns - 2
            screen.draw('…')

    end = screen.cursor.x

    # Separator gap
    if not is_last and 0 <= d_end < screen.columns:
        screen.cursor.x = d_end
        screen.cursor.bg = as_rgb(color_as_int(draw_data.default_bg))
        screen.draw(' ')

    # Prevent outer loop's StopIteration from overwriting our content
    screen.cursor.x = min(screen.cursor.x, screen.columns - 1)
    return end
