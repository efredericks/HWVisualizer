const DIM = 600;
let n;

techniques = [];

function preload() {

}

let scr;
function setup() {
    createCanvas(DIM, DIM).parent('canvasHolder');

    /*** socket things ***/
    socket = io.connect('http://localhost:8081');
    // connecting when there's already a connection
    socket.on('set initial data', (data) => {
        n.value(data.bgColor.color)
    });

    // new data sent from a client
    socket.on('new bgColor', (data) => {
        n.value(data.bgColor.color)
    });

    socket.on("new techniques", (data) => {
        test(JSON.parse(data));
    });


    /*** p5js things ***/

    // n = createSlider(0, 255, 220, 1).parent('bgColor');
    n = createColorPicker("#eeeeee");
    n.input(() => {
        sendColor();
    });

    // read initial list
    // socket.emit("checkForUpdates", null);

    // scr = createElement("script");
    // scr.src = "./techniques/flow-field.js";
    test(['flow-field.js']);
}

function loadTechniques(arr) {
    return new Promise(resolve => {
        setTimeout(() => {
            console.log(arr);
            for (a of arr) {
                if (!techniques.includes(a)) {
                    console.log(`Adding ${a} to list of techniques.`);
                    techniques.push(a);
                    let s = document.createElement("script");
                    s.setAttribute("type", "text/javascript");
                    s.setAttribute("src", `/static/techniques/${a}`);
                    let nodes = document.getElementsByTagName("*");
                    let node = nodes[nodes.length - 1].parentNode;
                    node.appendChild(s);
                }
            }

            // let a = FlowField();


            // let scr = createElement("script");
            // scr.src = "./techniques/flow-field.js";
            // document.head.appendChild(scr.elt);
            // techniques.push(scr);
            resolve('resolved');
        }, 2000);
    });
}

async function test(arr) {
    let a = 'before';
    console.log(a);
    a = await loadTechniques(arr);
    console.log(a);

    // console.log(techniques);
    // a = new FlowField();
    // a.update();
}


let step = 0;
let ff;
function draw() {
    // background(color(n.value()));

    if (typeof FlowField != "undefined" && step == 0) {
        ff = new FlowField();
        step = 1;
    }

    if (step == 1) {
        let retval = ff.update();
        if (!retval) {
            step = 2;
            // console.log("done");
            // noLoop();
        }
    }

    if (step == 2 && typeof RandomDots != "undefined") {
        ff = new RandomDots();
        step = 3;
    }

    if (step == 3)
    ff.update();

    // check for new techniques
    if ((frameCount % 100) == 0) {
        socket.emit("checkForUpdates", null);
    }
}

function sendColor() {
    const data = {
        color: n.value()
    };
    socket.emit('bgColor', data);
}