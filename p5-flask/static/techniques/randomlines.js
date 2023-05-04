export default class randomlines {
    constructor(sk) {
        this.sk = sk;
        this.num_particles = 20;
        this.color = "#00ff00";
    }

    update() {
        this.sk.noFill();
        this.sk.stroke(this.sk.color(this.color));
        this.sk.strokeWeight(2);
        for (let _ = 0; _ < this.num_particles; _++) {
            this.sk.line(this.sk.random(this.sk.width), this.sk.random(this.sk.height), this.sk.random(this.sk.width), this.sk.random(this.sk.height));
        }
        return true;
    }
};
