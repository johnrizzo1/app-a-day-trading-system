{
  description = "Agentic Trading System";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    devenv.url = "github:cachix/devenv";
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        inputs.devenv.flakeModule
      ];
      systems = [ "x86_64-linux" "x86_64-darwin" "aarch64-darwin" ];

      perSystem = { config, self', inputs', pkgs, system, ... }: {
        devenv.shells.default = {
          name = "trading-system";

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

          languages = {
            python.enable = true;
            python.venv.enable = true;
            python.uv.enable = true;
            javascript.enable = true;
          };

          env = {
            PYTHONPATH = "$PYTHONPATH:${toString ./.}";
          };

          scripts = {
            start-dev.exec = "docker-compose up -d && yarn workspace ui dev";
            start-prod.exec = "docker-compose up -d && yarn workspace ui build && yarn workspace ui start";
            setup-env.exec = "cp -n .env.example .env || true";
          };
        };
      };
    };
}
