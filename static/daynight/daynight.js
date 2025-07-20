let toggleCount = 0;

// 切换函数
function toggleMode() {
  toggleCount++;

  // 全局模式切换
  document.body.classList.toggle("night-mode");
  document.body.classList.toggle("day-mode");

  // 圆盘样式切换
  const circle = document.querySelector(".cont_circle");
  circle.classList.toggle("cont_circle_noche");
  circle.classList.toggle("cont_circle_dia");
}

// 初始：页面加载后默认为日间
document.addEventListener("DOMContentLoaded", () => {
  document.body.classList.add("day-mode");
  const circle = document.querySelector(".cont_circle");
  circle.classList.add("cont_circle_dia");
});
