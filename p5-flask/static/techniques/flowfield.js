export default class flowfield {
    constructor() {
        this.num_particles = 20;
        this.color = "#ff00ff";
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
        strokeWeight(5);
        for (let i = this.particles.length - 1; i >= 0; i--) {
            let p = this.particles[i];
            point(p.x, p.y);
            p.x++;
            p.y++;

            if (p.x > width || p.y > height) this.particles.splice(i, 1);
        }

        if (this.particles.length == 0) return false;
        return true;
    }
};