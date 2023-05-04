const DIM = 600;
let n;
let techniques = {};
let registry = {};
let activeTechnique, activeTechniqueObj;
let changeOver;
let initialTechnique = false;

function preload() {

}

let scr;
function setup() {
    createCanvas(DIM, DIM).parent('canvasHolder');
    changeOver = 250;

    registry = {};

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
        let _techniques = JSON.parse(data);

        for (t of _techniques) {
            if (!(t in Object.keys(techniques))) {
                loadNewScript(t);
                // techniques[t] = loadNewObject(t);
            }
        }

        // console.log(registry, techniques)

        // test(JSON.parse(data));
    });



    /*** p5js things ***/
    activeTechniqueObj = null;

    // n = createSlider(0, 255, 220, 1).parent('bgColor');
    n = createColorPicker("#eeeeee");
    n.input(() => {
        sendColor();
    });

    // read initial list
    // socket.emit("checkForUpdates", null);

    // scr = createElement("script");
    // scr.src = "./techniques/flow-field.js";
    // test(['flowfield.js']);
    socket.emit("checkForUpdates", null);
}

/*
function loadTechniques(arr) {
    let loadJS = new Promise(resolve => {
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
    return loadJS.then(() => {
        activeTechnique = random(techniques);
        activeTechniqueObj = loadObject(activeTechnique);
    });
}

async function test(arr) {
    // let a = 'before';
    // console.log(a);
    a = await loadTechniques(arr);
    // console.log(a);

    // console.log(techniques);
    // a = new FlowField();
    // a.update();
}
*/

let step = 0;
let ff;
function draw() {
    // background(color(n.value()));

    // if (typeof FlowField != "undefined" && step == 0) {
    //     ff = new FlowField();
    //     step = 1;
    // }

    // if (step == 1) {
    //     let retval = ff.update();
    //     if (!retval) {
    //         step = 2;
    //         // console.log("done");
    //         // noLoop();
    //     }
    // }

    // if (step == 2 && typeof RandomDots != "undefined") {
    //     ff = new RandomDots();
    //     step = 3;
    // }

    // if (step == 3)
    //     ff.update();

    // an active object in memory
    if (activeTechniqueObj != null) {
        activeTechniqueObj.update();
    }

    // check for new techniques
    if ((frameCount % 100) == 0) {
        socket.emit("checkForUpdates", null);

        if (registry != {}) {
            let idx = random(Object.keys(registry));
            // console.log(idx)
            if (registry[idx] != null) {
                activeTechniqueObj = loadNewObject(idx);
            }
        }
        /*
        if (techniques.length > 0) {
            activeTechnique = random(Object.keys(techniques));
            activeTechniqueObj = techniques[activeTechnique];
        }
        */
    }


    // swap technique
    /*
    if (!initialTechnique || ((frameCount % changeOver) == 0)) {
        if (techniques.length > 0) {
            activeTechnique = random(techniques);
            activeTechniqueObj = loadObject(activeTechnique);
            initialTechnique = true;
        }
    }*/
}

function sendColor() {
    const data = {
        color: n.value()
    };
    socket.emit('bgColor', data);
}

// should move this over to global space so we can use window[obj[0]] instead
function loadObject(technique) {
    try {
        let obj = eval(technique.split(".")[0]);
        let _activeObj = new obj();
        if (typeof _activeObj != "undefined") {
            return _activeObj;
        }
        return null;
    }
    catch (e) {
        return null;
    }
}

// https://stackoverflow.com/questions/76175598/restructuring-dynamically-loaded-scripts-within-javascript-program-to-avoid-eval/76175687#76175687
async function loadNewScript(scriptName) {
    const module = await import(`/static/techniques/${scriptName}`);
    registry[scriptName] = module.default;
    // return import(`/static/techniques/${scriptName}`);
}
function loadNewObject(technique) {
    const obj = registry[technique];
    return obj ? new obj() : null;
    // const module = await loadNewScript(technique);
    // const obj = module.default;
    // return new obj();
}