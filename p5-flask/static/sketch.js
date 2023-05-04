const s = (sk) => {
    const DIM = 600;
    const changeOver = 250;
    let n;
    let techniques = {};
    let registry = {};
    let activeTechnique, activeTechniqueObj;
    let initialTechnique = false;
    let scr;

    sk.preload = () => {};

    sk.setup = () => {
        sk.createCanvas(DIM, DIM).parent('canvasHolder');
        sk.noiseDetail(8, 0.85);

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

        // checking to see if a new technique exists in the local folder
        socket.on("new techniques", (data) => {
            let _techniques = JSON.parse(data);

            // load new scripts into memory, loadNewObject instantiates the class
            for (t of _techniques) {
                if (!(t in Object.keys(techniques))) {
                    loadNewScript(t);
                }
            }
        });

        /*** p5js things ***/
        // this is the object that is 'live' and drawing
        activeTechniqueObj = null;

        // n = createSlider(0, 255, 220, 1).parent('bgColor');
        // n = createColorPicker("#eeeeee");
        // n.input(() => {
        //     sendColor();
        // });

        // read initial list
        socket.emit("checkForUpdates", null);

        sk.frameRate(60);
    };

    sk.draw = () => {
        // an active object in memory
        if (activeTechniqueObj != null) {
            activeTechniqueObj.update();
        }

        // check for new techniques and pick a random technique to continue
        if ((sk.frameCount % changeOver) == 0) {
            socket.emit("checkForUpdates", null);

            if (registry != {}) {
                let idx = sk.random(Object.keys(registry));
                // console.log(idx)
                if (registry[idx] != null) {
                    activeTechniqueObj = loadNewObject(idx);
                }
            }
        }
    };

    // function sendColor() {
    //     const data = {
    //         color: n.value()
    //     };
    //     socket.emit('bgColor', data);
    // }

    // https://stackoverflow.com/questions/76175598/restructuring-dynamically-loaded-scripts-within-javascript-program-to-avoid-eval/76175687#76175687
    async function loadNewScript(scriptName) {
        const module = await import(`/static/techniques/${scriptName}`);
        registry[scriptName] = module.default;
    }
    function loadNewObject(technique) {
        const obj = registry[technique];
        return obj ? new obj(sk) : null;
    }
};

let myp5 = new p5(s);