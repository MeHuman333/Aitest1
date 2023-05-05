
// 创建一个画布
const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");
canvas.width = 600; // 将画布宽度变为600
canvas.height = 600; // 将画布高度变为600
document.body.appendChild(canvas);

// 在画布左边添加文字
const text = document.createElement("p");
text.textContent = "**红色是食物,灰色是障碍,要避开,不然会'Game Over'";
text.style.position = "absolute";
text.style.left = "10px";
text.style.top = canvas.offsetTop + "px";
document.body.appendChild(text);

// 绘制背景
ctx.fillStyle = "#EEE";
ctx.fillRect(0, 0, canvas.width, canvas.height);

// 创建开始按钮
const startButton = document.createElement("button");
startButton.style.position = "absolute"; // 设置按钮的定位方式为绝对定位
startButton.textContent = "开始";
startButton.style.transform = "scale(3)"; // 增大按钮尺寸至3倍
// 计算按钮的位置，使其位于画布中央
startButton.style.top =
  canvas.offsetTop + canvas.height / 2 - startButton.offsetHeight / 2 + "px";
startButton.style.left =
  canvas.offsetLeft + canvas.width / 2 - startButton.offsetWidth / 2 + "px";
document.body.appendChild(startButton);

// 等候点击事件
let waitForClick = true;

// 给按钮增加启动事件
startButton.addEventListener("click", () => {
  waitForClick = false;
  startButton.style.display = "none"; // 隐藏开始菜单
});

// 点击“开始"后才能开始游戏循环
function startGame() {
  if (waitForClick) {
    // 如果没有点击“开始"，程序在此处暂停，等候点击事件
    setTimeout(startGame, 50);
    return;
  }
  gameLoop();
}

startGame();

// 定义贪吃蛇的初始状态

let snake = [{ x: 10, y: 10 }];
let direction = "right";

// 定义食物的初始状态
let food = {
  x: Math.floor(Math.random() * 30),
  y: Math.floor(Math.random() * 30),
};

// 定义障碍的初始状态
let obstacles = [];
let maxObstacles = 4;
let numObstacles = 1;
for (let i = 0; i < numObstacles; i++) {
  obstacles.push({
    x: Math.floor(Math.random() * 30),
    y: Math.floor(Math.random() * 30),
  });
}

// 绘制贪吃蛇、食物和障碍
function draw() {
  // 绘制背景
  ctx.fillStyle = "#EEE";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // 绘制食物
  ctx.fillStyle = "red";
  ctx.fillRect(food.x * 20, food.y * 20, 20, 20); // 将食物大小增大一倍

  // 绘制障碍
  ctx.fillStyle = "gray";
  obstacles.forEach((obstacle) => {
    ctx.fillRect(obstacle.x * 20, obstacle.y * 20, 20, 20); // 将障碍大小增大一倍
  });

  // 绘制贪吃蛇
  ctx.fillStyle = "green";
  snake.forEach((segment) => {
    ctx.fillRect(segment.x * 20, segment.y * 20, 20, 20); // 将贪吃蛇大小增大一倍
  });
}

// 更新贪吃蛇的状态
function update() {
  // 根据方向更新贪吃蛇的头部
  let newHead = { x: snake[0].x, y: snake[0].y };
  if (direction === "right") {
    newHead.x++;
  } else if (direction === "left") {
    newHead.x--;
  } else if (direction === "up") {
    newHead.y--;
  } else if (direction === "down") {
    newHead.y++;
  }

  // 如果贪吃蛇到达边缘，从另一侧出现
  if (newHead.x < 0) {
    newHead.x = 29;
  } else if (newHead.x > 29) {
    newHead.x = 0;
  } else if (newHead.y < 0) {
    newHead.y = 29;
  } else if (newHead.y > 29) {
    newHead.y = 0;
  }

  // 如果贪吃蛇碰到障碍，游戏结束
  if (
    obstacles.some(
      (obstacle) => obstacle.x === newHead.x && obstacle.y === newHead.y
    )
  ) {
    alert("Game Over!");
    window.location.reload();
    return;
  }

  // 将新的头部添加到贪吃蛇的数组中
  snake.unshift(newHead);

  // 如果贪吃蛇吃到了食物，更新食物的位置
  if (snake[0].x === food.x && snake[0].y === food.y) {
    food = {
      x: Math.floor(Math.random() * 30),
      y: Math.floor(Math.random() * 30),
    };
    if (numObstacles < maxObstacles) {
      numObstacles++;
      obstacles.push({
        x: Math.floor(Math.random() * 30),
        y: Math.floor(Math.random() * 30),
      });
    }
  } else {
    // 如果贪吃蛇没有吃到食物，删除尾部
    snake.pop();
  }
}

// 处理键盘事件，改变方向
document.addEventListener("keydown", (event) => {
  if (event.key === "ArrowRight" && direction !== "left") {
    direction = "right";
  } else if (event.key === "ArrowLeft" && direction !== "right") {
    direction = "left";
  } else if (event.key === "ArrowUp" && direction !== "down") {
    direction = "up";
  } else if (event.key === "ArrowDown" && direction !== "up") {
    direction = "down";
  }
});

// 游戏循环
function gameLoop() {
  update();
  draw();
  setTimeout(gameLoop, 150);
}

