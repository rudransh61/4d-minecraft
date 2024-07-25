let angle = 0;
let w = 24;
let ma;

let heightScale = 1;

const minHeight = 1;
const maxHeight = 150;

let maxD;

const noiseOffset = 100;
const noiseScale = 0.005;
const timeScale = 0.0002;
let frames = 60;

let cam;
let speed = 5;
let camX = 0;
let camY = 0;
let camZ = 500;
let camRotX = 0;
let camRotY = 0;
let camRotZ = 0;
let time = 0;

function setup() {
  createCanvas(1000, 1000, WEBGL);
  ma = atan(cos(QUARTER_PI));
  maxD = dist(0, 0, 200, 200);
  cam = createCamera();
  cam.setPosition(camX, camY, camZ);
}

function keyPressed() {
  if (key == " ") {
    const options = {
      units: "frames",
      delay: 0
    }
    saveGif("beesandbombs.gif", frames, options);
  }
}

function draw() {
  background(100);
  lights();
  ortho(-800, 800, 800, -800, 0, 2000);

  handleCameraMovement();
  
  cam.lookAt(0, 0, 0);
  rotateX(ma);
  rotateY(-QUARTER_PI);

  noStroke();
  for (let z = 0; z < height * 3; z += w) {
    for (let x = 0; x < width * 3; x += w) {
      push();
      let noiseValue = getNoiseValue(x, z, time);
      let h = 2 * getBoxHeight(noiseValue);
      let color = map(noiseValue, 0, 1, minHeight, maxHeight) / 100;

      let colorname = "#477A1E";
      if (color <= 0.5) {
        colorname = "#006992";
      } else if (color > 0.5 && color < 0.65) {
        colorname = "#f0dbe4";
      } else if (color >= 0.7) {
        colorname = "#1C8F66";
      }

      translate(x - width, -100, z - height );
      fill(colorname);
      box(w, h, w);
      pop();
    }
  }
}

function handleCameraMovement() {
  if (keyIsDown(87)) { // W key
    camX += speed * sin(camRotY);
    camZ -= speed * cos(camRotY);
  }
  if (keyIsDown(83)) { // S key
    camX -= speed * sin(camRotY);
    camZ += speed * cos(camRotY);
  }
  if (keyIsDown(65)) { // A key
    camX -= speed * cos(camRotY);
    camZ -= speed * sin(camRotY);
  }
  if (keyIsDown(68)) { // D key
    camX += speed * cos(camRotY);
    camZ += speed * sin(camRotY);
  }
  if (keyIsDown(69)) { // E key
    camY += speed;
  }
  if (keyIsDown(81)) { // Q key
    camY -= speed;
  }
  if (keyIsDown(70)) { // F key
    time += 100;
  }
  if (keyIsDown(71)) { // G key
    time -= 100;
  }
  if (keyIsDown(LEFT_ARROW)) { // Left arrow key
    camRotY -= 0.05;
  }
  if (keyIsDown(RIGHT_ARROW)) { // Right arrow key
    camRotY += 0.05;
  }
  if (keyIsDown(UP_ARROW)) { // Up arrow key
    camRotX -= 0.05;
  }
  if (keyIsDown(DOWN_ARROW)) { // Down arrow key
    camRotX += 0.05;
  }

  cam.setPosition(camX, camY, camZ);
  cam.lookAt(-10, -10, -10);
//   cam.rotateX(camRotX);
//   cam.rotateY(camRotY);
}

function getNoiseValue(x, z, time) {
  x = x * noiseScale + noiseOffset;
  z = z * noiseScale + noiseOffset;
  time = time * timeScale + noiseOffset;
  return noise(x, z, time);
}

function getBoxHeight(noiseValue) {
  return map(noiseValue, 0, 1, minHeight, maxHeight) * heightScale;
}
