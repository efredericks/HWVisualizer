# Overview

# Running

This application uses a Flask server to handle serving the webpage as well as maintaining socket connections.  By default, the script runs on port `8081`, so ensure that all firewall ports are open.

Additionally, the server must be configured to do a `git pull` as often as desired.  During testing we created a `cron` job to run it every 10 minutes.

At present, each time a technique is selected a *new instance* is generated, so optimize the amount of memory/time that your `constructor` requires!

# Live Editing

A separate webpage is available to communicate with the client display, where visiting the page will present a suite of controls that modify common parameters to all modules.  To access the controls simply visit the link provided by the QR code on the display.

# Contributing a Module 

Modules will be included at runtime and will thus include all standard calls to various p5js functions.  Note that, at this time, we are running in instance mode, so ensure that your constructor accepts the instance to work with all p5.js calls.

Modules must follow ES6 syntax and minimally provide a `constructor` and `update` function, as they will be called in an `Entity System` style pattern.

Additionally, your class name must match your file name as well.  For example, if your file is `myScript.js` then your class name should be `myScript`, as the loader simply parses out the string name of your file and assumes that is its class name.

## Sample Module 

> myScript.js

```
// Author: <Your name>
// Technique: <Human-friendly name>
// Version: 1.0.0
// Description: <Overview of technique>

export default class myScript {
    // initialize class-specific parameters
    constructor(sk) {
        this.sk = sk; // access to p5 instance
    }

    // called once per draw() cycle when this technique is active
    update() {
    }
};
```

## Approval Process

Your script must pass two checks to be included in production: a set of unit tests configured within GitHub and a manual review by the repository owners.

1. The unit tests (TBD) ensure that your script meets expected performance and drawing criteria.

2. Scripts must also pass a manual review process to ensure that not-safe-for-work content is not included (this will be displayed publicly in a school setting) as well as no unsafe code is executed (e.g., security concerns).  If your script attempts to sidestep either of these rules then any future submissions by the author will be rejected without review.