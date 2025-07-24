// common-polling.js

const PollingManager = (() => {
    let tasks = [];
    let timer = null;
    const interval = 5000; // 默认轮询间隔：5秒

    function startPolling() {
        if (timer !== null) return; // 防止重复启动

        timer = setInterval(() => {
            tasks.forEach((taskFn) => {
                try {
                    taskFn();
                } catch (err) {
                    console.error("轮询任务出错:", err);
                }
            });
        }, interval);
        console.log("轮询已启动");
    }

    function stopPolling() {
        if (timer) {
            clearInterval(timer);
            timer = null;
            console.log("轮询已停止");
        }
    }

    function register(taskFn) {
        tasks.push(taskFn);
    }

    return {
        register,
        start: startPolling,
        stop: stopPolling
    };
})();
