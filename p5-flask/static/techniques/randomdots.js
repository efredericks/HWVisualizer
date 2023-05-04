export default class randomdots  {
    constructor() {
        this.num_particles = 20;
        this.color = "#ffff00";
        this.particles = [];

        for (let _ = 0; _ < this.num_particles; _++) {
            this.particles.push({
                x: random(0,1000),//20,
                y: random(0,1000),//20
            });
        }
    }

    update() {
        noFill();
        stroke(color(this.color));
        strokeWeight(15);
        for (let i = this.particles.length - 1; i >= 0; i--) {
            let p = this.particles[i];
            point(p.x, p.y);
            p.x = random(0, width);
            p.y = random(0, height);
        }
        return true;
    }
};