export default class randomdots  {
    constructor(sk, palette) {
        this.sk = sk;
        this.palette = palette;
        this.num_particles = 20;
        // this.color = "#ffff00";
        this.particles = [];

        for (let _ = 0; _ < this.num_particles; _++) {
            let col = sk.color(sk.random(palette));
            col.setAlpha(sk.random(10,220));
            this.particles.push({
                x: this.sk.random(0,this.sk.width),
                y: this.sk.random(0,this.sk.height),
                col: col,
                size: sk.random(1,15),
            });
        }
    }

    update() {
        this.sk.noFill();
        for (let i = this.particles.length - 1; i >= 0; i--) {
            let p = this.particles[i];
            this.sk.strokeWeight(p.size);
            this.sk.stroke(p.col);
            this.sk.point(p.x, p.y);
            p.x = this.sk.random(0, this.sk.width);
            p.y = this.sk.random(0, this.sk.height);
        }
        return true;
    }
};