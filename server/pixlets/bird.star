load("render.star", "render")
load('http.star', 'http')

def main():
    response = http.get("http://web:8000/latest/", ttl_seconds = 60)
    data = response.json()

    if len(data.get("last_minute")) < 2:
        bird = data.get("last_minute")[0] if len(data.get("last_minute")) == 1 else ""
        if bird == "":
            return
        return render.Root(
            child = render.Column(
                expanded=True,
                main_align="space_evenly",
                cross_align="center",
                children = [
                    render.Box(width=64, height=2, color="#a00"),
                    render.Text("Now hearing!"),
                    render.Text(bird),
                    render.Box(width=64, height=2, color="#a00"),
                ]
            )
        )
    else:
        birds = ", ".join(data.get("last_minute"))
        if birds == "":
            return
        return render.Root(
            child = render.Column(
                expanded=True,
                main_align="space_evenly",
                cross_align="center",
                children = [
                    render.Box(width=64, height=2, color="#a00"),
                    render.Text("Now hearing!"),
                    render.Marquee(
                        width=64,
                        child=render.Text(birds),
                        offset_start=5,
                        offset_end=32,
                    ),
                    render.Box(width=64, height=2, color="#a00"),
                ]
            )
        )