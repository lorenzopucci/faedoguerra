function on_svg_click(id) {
    window.location.href = `/room/${id}`;
}

// change which floor is focused
function switch_view() {
    floor = window.location.hash.split('#')[1];
    if (window.location.hash == '') floor = '';
    const url_params = new URLSearchParams(window.location.search);

    if (!['', '-1', '0', '1', '2', '3'].includes(floor)) return;

    if (url_params.get('embed') && floor == '') floor = floor_to_focus.toString();

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

    if (url_params.get('embed')) {
        const map = document.getElementById('map-card').innerHTML;
        const ranking = document.getElementById('ranking-wrapper').innerHTML;

        document.body.innerHTML = '';
        if (last_event) document.body.innerHTML = `<div class="full-width-card">${last_event}</div>`;

        document.body.innerHTML += `
            <div class="full-width-card" id="map-card">${map}</div>
            <div class="full-width-card" id="ranking-wrapper">${ranking}</div>
        `;
        document.body.style.backgroundColor = 'rgba(0, 0, 0, 0)';
        document.body.classList.add('embedded-page');
    }
}

function color_room(path, text, color) {
    path.style.fill = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;

    var luminance = 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2];
    text.style.fill = (luminance < 150) ? "white" : "black";
}

function init_room(room) {
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
}

function color_svg(data) {
    data.forEach((room) => {
        init_room(room);

        if (room.floor == 0 && room.svg_id == 32) {
            [[-1, 8], [1, 32], [2, 32], [3, 9]].forEach(vec => {
                room.floor = vec[0];
                room.svg_id = vec[1];
                init_room(room);
            });
        }
    });
}

function fetch_replay_data() {
    fetch('/replay-data').then(res => res.json()).then(res => {
        replay_data = res;
        previous_pos = res.deltas.length;
    });
}

function to_new_color(delta, floor, svg_id) {
    if (!floor) floor = delta.floor;
    if (!svg_id) svg_id = delta.svg_id;

    var path = document.getElementById(`path${floor}${svg_id}`);
    var text = document.getElementById(`text${floor}${svg_id}`);
    if (path != undefined) {
        path.classList.remove('blinking');
        color_room(path, text, delta.new_color);
    }
}

function to_old_color(delta, floor, svg_id) {
    if (!floor) floor = delta.floor;
    if (!svg_id) svg_id = delta.svg_id;

    var path = document.getElementById(`path${floor}${svg_id}`);
    var text = document.getElementById(`text${floor}${svg_id}`);
    if (path != undefined) {
        path.classList.remove('blinking');
        color_room(path, text, delta.old_color);
    }
}

// move through timestamps
function update_view(position) {
    position = parseInt(position);

    if (position >= previous_pos) {
        for (var i = previous_pos; i < position; i++) {
            var delta = replay_data.deltas[i];
            to_new_color(delta);

            if (delta.floor == 0 && delta.svg_id == 32) {
                [[-1, 8], [1, 32], [2, 32], [3, 9]].forEach(vec => {
                    to_new_color(delta, vec[0], vec[1]);
                });
            }
        }
    }
    else {
        for (var i = previous_pos - 1; i >= position; i--) {
            var delta = replay_data.deltas[i];
            to_old_color(delta);

            if (delta.floor == 0 && delta.svg_id == 32) {
                [[-1, 8], [1, 32], [2, 32], [3, 9]].forEach(vec => {
                    to_old_color(delta, vec[0], vec[1]);
                });
            }
        }
    }

    document.getElementById('sns-stats').innerHTML = `SNS: ${replay_data.university_stats[position].sns}%`;
    document.getElementById('sssup-stats').innerHTML = `SSSUP: ${replay_data.university_stats[position].sssup}%`;
    document.getElementById('sns-slider').style.width = `${replay_data.university_stats[position].sns}%`;
    document.getElementById('sssup-slider').style.width = `${replay_data.university_stats[position].sssup}%`;

    ranking = "";
    replay_data.ranking[position].forEach((item, idx) => {
        ranking += `
            <tr>
              <td class="tight">${idx + 1}</td>
              <td>
                <span class="color-square" style="background-color:${item.color};"></span>
                <a href="/player/${item.id}">${item.full_name}</a> (${item.university})
              </td>
              <td class="tight">${item.count}</td>
            </tr>
        `;
    });
    document.getElementById('ranking-body').innerHTML = ranking;

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

    for (var i = 1; i <= replay_data.deltas.length; i++) {
        await sleep(500);

        if (!playing) break;
        update_view(i);
        slider.value = i;
    }

    playing = false;
}

// needed when this page is embedded into another. Tells the parent page to
// adjust the iframe's height
function post_embed_message() {
    if (window.parent) {
        window.parent.postMessage({iframe_height: document.body.scrollHeight}, '*');
    }
}
