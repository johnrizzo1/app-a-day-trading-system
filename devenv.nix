{ pkgs, ... }: {
  # https://devenv.sh/basics/
  env.GREET = "trading system environment";

  # https://devenv.sh/packages/
  packages = with pkgs; [
    python311
    poetry
    nodejs_20
    yarn
    docker
    docker-compose
    direnv
    uv
  ];

  languages.python = {
    enable = true;
    version = "3.11";
    venv.enable = true;
    venv.requirements = ./requirements.txt;
  };

  languages.javascript.enable = true;

  # https://devenv.sh/scripts/
  scripts.hello.exec = "echo $GREET";
  scripts.setup-env.exec = "cp -n .env.example .env || true";
  scripts.start-dev.exec = "docker-compose up -d && yarn workspace ui dev";
  scripts.start-prod.exec = "docker-compose up -d && yarn workspace ui build && yarn workspace ui start";

  enterShell = ''
    hello
  '';

  # https://devenv.sh/processes/
  processes.dev.exec = "yarn workspace ui dev";
}
