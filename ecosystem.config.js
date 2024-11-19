module.exports = {
    apps: [
      {
        name: "ig_backend",
        script: "run.py",
        interpreter: ".venv/bin/python3",
        args: "8200",
        instances: 1,
        exec_mode: "fork" // 또는 "cluster"로 변경 가능
      }
    ]
  };