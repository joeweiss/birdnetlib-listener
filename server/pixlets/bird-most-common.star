load("render.star", "render")
load('http.star', 'http')

def main():
    response = http.get("http://web:8000/latest/", ttl_seconds = 60)
    data = response.json()
    print(data)

    title = "Most common today"
    key = "most_common"
    color = "#fff26e"

    if len(data.get(key)) < 2:
        bird = data.get(key)[0] if len(data.get(key)) == 1 else ""
        return render.Root(
            child = render.Column(
                expanded=True,
                main_align="space_evenly",
                cross_align="center",
                children = [
                    render.WrappedText(
                        title,
                        font="tom-thumb",
                        align="center"
                    ),
                    render.Box(width=64, height=1, color=color),
                    render.Text(bird),
                ]
            )
        )
    else:
        birds = ", ".join(data.get(key))
        return render.Root(
            child = render.Column(
                expanded=True,
                main_align="space_evenly",
                cross_align="center",
                children = [
                    render.WrappedText(
                        title,
                        font="tom-thumb",
                        align="center"
                    ),
                    render.Box(width=64, height=1, color=color),
                    render.Marquee(
                        width=64,
                        child=render.Text(birds),
                        offset_start=5,
                        offset_end=32,
                    ),
                ]
            )
        )