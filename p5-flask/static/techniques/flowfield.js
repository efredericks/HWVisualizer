export default class flowfield {
    constructor(sk) {
        this.sk = sk;
        this.num_particles = 50;
        this.noiseZoom = 0.01;
        this.color = "#ff00ff";
        this.particles = [];
        this.grid = [];

        for (let _ = 0; _ < this.num_particles; _++) {
            this.particles.push({
                x: sk.random(0,sk.width-1),
                y: sk.random(0,sk.height-1),
                col: sk.color(255,0,255)//sk.random(0,255), sk.random(0,255), sk.random(0,255),  sk.random(20.120))
            });
        }

        for (let y = 0; y < this.sk.height; y++) {
            this.grid[y] = [];
            for (let x = 0; x < this.sk.width; x++) {
                let n = this.sk.noise(x * this.noiseZoom, y * this.noiseZoom);
                this.grid[y][x] = this.sk.map(n, 0.0, 1.0, 0.0, this.sk.TWO_PI);
            }
        }
    }

    update() {
        this.sk.noFill();
        this.sk.strokeWeight(5);

        for (let i = this.particles.length - 1; i >= 0; i--) {
            let p = this.particles[i];
            this.sk.stroke(p.col);
            this.sk.point(p.x, p.y);

            let angle = this.grid[this.sk.int(p.y)][this.sk.int(p.x)];
            p.x += this.sk.cos(angle);
            p.y += this.sk.sin(angle);

            if (p.x < 0 || p.x > this.sk.width-1 || p.y < 0 || p.y > this.sk.height-1) this.particles.splice(i, 1);
        }

        if (this.particles.length == 0) return false;
        return true;
    }
};