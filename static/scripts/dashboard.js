function redirect_to_floor(floor) {
    window.location.href = `/dashboard/${floor}`;
}

function on_svg_click(id) {
    window.location.href = `/room/${id}`;
}

function color_svg(data) {
    data.forEach((room) => {
        var path = document.getElementById(`path${room.floor}${room.svg_id}`);
        var text = document.getElementById(`text${room.floor}${room.svg_id}`);
        var clickable = document.getElementById(`clickable${room.floor}${room.svg_id}`);

        path.style.fill = `rgb(${room.color[0]}, ${room.color[1]}, ${room.color[2]})`;
        clickable.onclick = () => on_svg_click(room.id);

        var luminance = 0.2126 * room.color[0] + 0.7152 * room.color[1] + 0.0722 * room.color[2];
        text.style.fill = (luminance < 150) ? "white" : "black";
        text.textContent = room.label;

        tippy(`#clickable${room.floor}${room.svg_id}`, {
            content: room.tooltip,
            placement: 'top',
        })
    });
}
