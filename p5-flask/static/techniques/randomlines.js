export default class randomlines {
    constructor(sk, palette) {
        this.sk = sk;
        this.palette = palette;
        this.num_particles = 20;
        this.color = sk.color(sk.random(palette));//"#00ff00";
        this.color.setAlpha(sk.random(10,180));
    }

    update() {
        this.sk.noFill();
        this.sk.stroke(this.color);
        this.sk.strokeWeight(2);
        for (let _ = 0; _ < this.num_particles; _++) {
            this.sk.line(this.sk.random(this.sk.width), this.sk.random(this.sk.height), this.sk.random(this.sk.width), this.sk.random(this.sk.height));
        }
        return true;
    }
};
