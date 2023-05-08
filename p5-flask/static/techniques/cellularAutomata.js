export default class cellularAutomata {
    constructor(sk, palette) {
        this.sk = sk;
        this.palette = palette;

        this.w = 10;//sk.int(sk.width / this.numCells);
        this.h = sk.int(sk.height / this.w) + 1;
        this.numCells = sk.int(sk.width / this.w) + 1;

        let retinit = this.initCA();

        this.cells = [];

        this.cells = retinit.cells;
        this.ruleset = retinit.ruleset;
        this.generation = 0;
    }

    initCA() {
        let cells = [];
        for (let i = 0; i < this.numCells; i++)
            cells[i] = 0;

        if (this.sk.random() > 0.5)
            cells[this.sk.int(cells.length / 2)] = 1;
        else
            cells[this.sk.int(this.sk.random(0, cells.length - 1))] = 1;

        let ruleset = [];
        if (this.sk.random() > 0.5)
            ruleset = [0, 1, 0, 1, 1, 0, 1, 0];
        else {
            for (let _ = 0; _ < 8; _++)
                ruleset.push(this.sk.random([0, 1]));
        }

        return { cells: cells, ruleset: ruleset };
    }

    wolframCARules(a, b, c, ruleset) {
        if (a == 1 && b == 1 && c == 1) return ruleset[0];
        if (a == 1 && b == 1 && c == 0) return ruleset[1];
        if (a == 1 && b == 0 && c == 1) return ruleset[2];
        if (a == 1 && b == 0 && c == 0) return ruleset[3];
        if (a == 0 && b == 1 && c == 1) return ruleset[4];
        if (a == 0 && b == 1 && c == 0) return ruleset[5];
        if (a == 0 && b == 0 && c == 1) return ruleset[6];
        if (a == 0 && b == 0 && c == 0) return ruleset[7];
        return 0
    }

    wolframCAGenerate(cells, generation, ruleset) {
        let nextgen = [];
        for (let i = 0; i < cells.length; i++)
            nextgen.push(0);

        for (let i = 1; i < cells.length - 1; i++) {
            let left = cells[i - 1];
            let middle = cells[i];
            let right = cells[i + 1];

            nextgen[i] = this.wolframCARules(left, middle, right, ruleset);
        }
        generation++;

        return { nextgen: nextgen, generation: generation };
    }

    update() {
        for (let i = 0; i < this.cells.length; i++) {
            let x = i * this.w;
            let y = this.generation * this.w;

            let drawRect = false;
            if (this.cells[i] == 1) drawRect = true;

            if (drawRect)
                this.sk.rect(x, y, this.w, this.h);
        }

        let retval = this.wolframCAGenerate(this.cells, this.generation, this.ruleset);
        this.cells = retval.nextgen;
        this.generation = retval.generation;

        if (this.generation >= this.h - 1)
            this.generation = 0;
    }
};