load("render.star", "render")
load('http.star', 'http')

def main():
    response = http.get("http://web:8000/latest/")
    data = response.json()
    recent_bird_list = data.get("last_hour")
    if len(recent_bird_list) == 0:
        recent = "It's quiet now"
    else:
        recent = ", ".join(data.get("last_hour"))
    daily_count = str(int(data.get("daily_count", 0)))
    return render.Root(
        delay=30,
        child = render.Column(
            expanded=True,
            main_align="space_evenly",
            cross_align="center",
            children = [
                #render.Box(width=64, height=2, color="#880ED4"),
                render.Text(
                    "Recent birds",
                    font="CG-pixel-3x5-mono",
                    color="#880ED4"
                ),
                render.Marquee(
                    width=64,
                    child=render.Text(recent),
                    offset_start=5,
                    offset_end=32,
                ),
                render.Text(
                    daily_count + " species today",
                    #font="CG-pixel-4x5-mono",
                    font="tom-thumb",
                    color="#880ED4"
                ),
            ]
        )
    )