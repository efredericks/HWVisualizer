export default class randomdots  {
    constructor(sk) {
        this.sk = sk;
        this.num_particles = 20;
        this.color = "#ffff00";
        this.particles = [];

        for (let _ = 0; _ < this.num_particles; _++) {
            this.particles.push({
                x: this.sk.random(0,this.sk.width),
                y: this.sk.random(0,this.sk.height),
            });
        }
    }

    update() {
        this.sk.noFill();
        this.sk.stroke(this.sk.color(this.color));
        this.sk.strokeWeight(15);
        for (let i = this.particles.length - 1; i >= 0; i--) {
            let p = this.particles[i];
            this.sk.point(p.x, p.y);
            p.x = this.sk.random(0, this.sk.width);
            p.y = this.sk.random(0, this.sk.height);
        }
        return true;
    }
};