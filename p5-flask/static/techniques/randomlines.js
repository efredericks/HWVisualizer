const randomlines = class {
    constructor() {
        this.num_particles = 20;
        this.color = "#00ff00";
    }

    update() {
        noFill();
        stroke(color(this.color));
        strokeWeight(2);
        for (let _ = 0; _ < this.num_particles; _++) {
            line(random(width),random(height),random(width), random(height));
        }
        return true;
    }
};