function on_svg_click(id) {
    window.location.href = `/room/${id}`;
}

function switch_view() {
    floor = window.location.hash.split('#')[1];
    if (window.location.hash == '') floor = '';

    if (!['', '-1', '0', '1', '2', '3'].includes(floor)) return;

    if (floor == '') {
        document.querySelectorAll('.floor-wrapper').forEach(el => {
            el.style.display = 'block';
            el.classList.remove('floor-focused');
        });
        document.getElementById('general-grid').style.gridTemplateColumns = '30% 35% 35%';
    }
    else {
        document.querySelectorAll('.floor-wrapper').forEach(el => {
            el.style.display = 'none';
        });
        const wrapper = document.getElementById(`floor${floor}-wrapper`)
        wrapper.style.display = 'block';
        wrapper.classList.add('floor-focused');

        document.getElementById('general-grid').style.gridTemplateColumns = 'auto auto auto';
    }
}

function color_room(path, text, color) {
    path.style.fill = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;

    var luminance = 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2];
    text.style.fill = (luminance < 150) ? "white" : "black";
}

function color_svg(data) {
    data.forEach((room) => {
        var path = document.getElementById(`path${room.floor}${room.svg_id}`);
        var text = document.getElementById(`text${room.floor}${room.svg_id}`);
        var clickable = document.getElementById(`clickable${room.floor}${room.svg_id}`);

        color_room(path, text, room.color);
        if (room.blink) path.classList.add('blinking');

        clickable.onclick = () => on_svg_click(room.id);
        text.textContent = room.label;

        tippy(`#clickable${room.floor}${room.svg_id}`, {
            content: room.tooltip,
            placement: 'top',
        });
    });
}

function update_view(position) {
    if (position >= previous_pos) {
        for (var i = previous_pos; i < position; i++) {
            var path = document.getElementById(`path${replay_data[i].floor}${replay_data[i].svg_id}`);
            var text = document.getElementById(`text${replay_data[i].floor}${replay_data[i].svg_id}`);
            if (path != undefined) {
                path.classList.remove('blinking');
                color_room(path, text, replay_data[i].new_color);
            }
        }
    }
    else {
        for (var i = previous_pos - 1; i >= position; i--) {
            var path = document.getElementById(`path${replay_data[i].floor}${replay_data[i].svg_id}`);
            var text = document.getElementById(`text${replay_data[i].floor}${replay_data[i].svg_id}`);
            if (path != undefined) {
                path.classList.remove('blinking');
                color_room(path, text, replay_data[i].old_color);
            }
        }
    }
    previous_pos = position;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function replay() {
    if (playing) return;

    var slider = document.getElementById("replay-slider");
    slider.value = 0;

    playing = true;
    update_view(0);

    for (var i = 1; i <= replay_data.length; i++) {
        await sleep(500);

        if (!playing) break;
        update_view(i);
        slider.value = i;
    }

    playing = false;
}
