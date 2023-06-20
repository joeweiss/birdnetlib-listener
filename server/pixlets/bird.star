load("render.star", "render")
load('http.star', 'http')

def main():
    response = http.get("http://web:8000/latest/")
    data = response.json()
    print(data.get("name"))
    return render.Root(
        child = render.Column(
            expanded=True,
            main_align="space_evenly",
            cross_align="center",
            children = [
                render.Box(width=64, height=2, color="#a00"),
                render.Text("Now hearing!"),
                render.Text(data.get("name")),
                render.Box(width=64, height=2, color="#a00"),
            ]
        )
    )