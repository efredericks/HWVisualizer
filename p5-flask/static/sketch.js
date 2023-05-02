const DIM = 600;
let n;
// let socket;

function setup() {
    createCanvas(DIM, DIM).parent('canvasHolder');
    socket = io.connect('http://localhost:8081');

    socket.on('set initial data', (data) => {
        console.log(data);
        n.value(data.bgColor.color)
    });

    socket.on('new bgColor', (data) => {
        console.log(data)
        n.value(data.bgColor.color)
    });

    // n = createSlider(0, 255, 220, 1).parent('bgColor');
    n = createColorPicker("#eeeeee");
    n.input(() => {
        sendColor();
    });
}

function draw() {
    background(color(n.value()));
}

function sendColor() {
    const data = {
        color: n.value()
    };
    socket.emit('bgColor', data);
}