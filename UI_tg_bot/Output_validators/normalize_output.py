from datetime import time

def normalize_time(raw_time):
    fmt = "%H:%M"
    str_time = time.strftime(raw_time, fmt)
    h,m = str_time.strip().split(":")
    return f"{int(h):02d}:{int(m):02d}"

def format_output(date, notes):
    header = f"📅 {date}"
    if not notes:
        return f"{header}\n\nNo notes yet."
    lines = [f"🕐 {normalize_time(n.start_time)} – {normalize_time(n.end_time)}  {n.text}" for n in notes]
    return header + "\n\n" + "\n".join(lines)